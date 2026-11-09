#!/usr/bin/env python3
"""Install EQEmu modules into a server source tree.

    python tools/modules.py list
    python tools/modules.py check
    python tools/modules.py install --server <dir> [--quests <dir>] [--base eqemu|nms] <module> ... | --all
    python tools/modules.py sql --server <dir> (--mysql "<command>" | --out <file>)
    python tools/modules.py test --repo <git repo> --ref <commit> --base eqemu|nms [--server-subdir <dir>]
                                 [--quests-subdir <dir>] [<module> ...]

See docs/FRAMEWORK.md for the module format and what install changes.
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Extra module folders (the tests use this), separated like PATH
MODULES_DIRS = [os.path.join(ROOT, 'modules')] + [d for d in os.environ.get('EQMOD_MODULES_DIR', '').split(os.pathsep) if d]
BASES = ('eqemu', 'nms')
LOCK = 'modules.lock.json'
HOOK = 'eqemu-modules hook'
SOURCE_LISTS = {'zone': 'zone_sources', 'zone_headers': 'zone_headers', 'gm_commands': 'gm_command_sources'}
ACCESS = re.compile(r'^AccountStatus::\w+$')


class Fail(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------------------
# Modules


def load_modules():
    mods = {}
    for top in MODULES_DIRS:
        if not os.path.isdir(top):
            continue
        for name in sorted(os.listdir(top)):
            path = os.path.join(top, name, 'module.json')
            if os.path.isfile(path):
                with open(path, encoding='utf-8') as fh:
                    m = json.load(fh)
                m['_dir'] = os.path.dirname(path)
                m['_folder'] = name
                mods[m.get('name', name)] = m
    return mods


def problems(mods):
    """Every problem in the module definitions, as text."""
    out = []
    for name, m in mods.items():
        where = f'modules/{m["_folder"]}'
        if name != m['_folder']:
            out.append(f'{where}: name "{name}" does not match its folder')
        for key in ('title', 'description', 'bases'):
            if not m.get(key):
                out.append(f'{where}: missing "{key}"')
        for b in m.get('bases', []):
            if b not in BASES:
                out.append(f'{where}: unknown base "{b}"')
        for r in m.get('requires', []):
            if r not in mods:
                out.append(f'{where}: requires unknown module "{r}"')
            elif not set(m.get('bases', [])) <= set(mods[r].get('bases', [])):
                out.append(f'{where}: supports a base that its requirement "{r}" does not')
        for key, files in m.get('sources', {}).items():
            if key not in SOURCE_LISTS:
                out.append(f'{where}: unknown source list "{key}" (use {", ".join(SOURCE_LISTS)})')
                continue
            for f in files:
                if not any(os.path.isfile(p) for p in source_candidates(m, key, f)):
                    out.append(f'{where}: source "{f}" is not in the module files')
        for c in m.get('commands', []):
            for key in ('name', 'access', 'function', 'description'):
                if not c.get(key):
                    out.append(f'{where}: command {c.get("name", "?")} is missing "{key}"')
            if c.get('access') and not ACCESS.match(c['access']):
                out.append(f'{where}: command {c["name"]} access must look like AccountStatus::Player')
        for b in m.get('bases', []):
            for p in patch_files(m, b):
                if not p.endswith('.patch'):
                    out.append(f'{where}: {os.path.relpath(p, m["_dir"])} is not a .patch file')
    try:
        order(mods, list(mods))
    except Fail as e:
        out.append(str(e))
    return out


def source_candidates(m, key, f):
    rel = os.path.join('zone', f)
    yield os.path.join(m['_dir'], 'files', 'server', rel)
    for b in BASES:
        yield os.path.join(m['_dir'], b, 'files', 'server', rel)


def order(mods, wanted):
    """The wanted modules plus everything they require, requirements first."""
    done, seen, out = set(), [], []

    def visit(name, chain):
        if name in done:
            return
        if name in chain:
            raise Fail('modules require each other in a loop: ' + ' -> '.join(chain + [name]))
        if name not in mods:
            raise Fail(f'unknown module "{name}"' + (f' (required by {chain[-1]})' if chain else ''))
        for r in mods[name].get('requires', []):
            visit(r, chain + [name])
        done.add(name)
        out.append(name)

    for w in wanted:
        visit(w, [])
    return out


def walk(top):
    if not os.path.isdir(top):
        return
    for d, _, files in os.walk(top):
        for f in sorted(files):
            yield os.path.join(d, f)


def patch_files(m, base):
    for area in ('server', 'quests'):
        for p in sorted(walk(os.path.join(m['_dir'], base, 'patches', area))):
            yield p


def sql_files(m, base):
    files = list(walk(os.path.join(m['_dir'], 'sql'))) + list(walk(os.path.join(m['_dir'], base, 'sql')))
    return sorted((f for f in files if f.endswith('.sql')), key=os.path.basename)


# ---------------------------------------------------------------------------------------------------------------------
# Target trees


def detect_base(server):
    if not os.path.isfile(os.path.join(server, 'zone', 'CMakeLists.txt')):
        raise Fail(f'{server} is not an EQEmu server source folder (no zone/CMakeLists.txt)')
    return 'nms' if os.path.isfile(os.path.join(server, 'zone', 'nms_waypoints.cpp')) else 'eqemu'


def git(cwd, *args, check=True):
    r = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise Fail(f'git {" ".join(args)} failed in {cwd}:\n{r.stderr.strip()}')
    return r


def git_top(path):
    r = git(path, 'rev-parse', '--show-toplevel', check=False)
    return os.path.normpath(r.stdout.strip()) if r.returncode == 0 else None


def dirty(path):
    top = git_top(path)
    if not top:
        return False
    return bool(git(path, 'status', '--porcelain', '--', '.').stdout.strip())


def apply_patch(target, patch):
    """Apply one patch with paths relative to target; return None or the error text."""
    top = git_top(target)
    if top:
        prefix = os.path.relpath(os.path.normpath(target), top).replace('\\', '/')
        args = ['apply', '--whitespace=nowarn'] + ([f'--directory={prefix}'] if prefix != '.' else [])
        cwd = top
    else:
        args, cwd = ['apply', '--whitespace=nowarn'], target
    r = git(cwd, *args, '--check', patch, check=False)
    if r.returncode == 0:
        git(cwd, *args, patch)
        return None
    return r.stderr.strip()


def insert_hook(path, line, anchor, after=None, place='before'):
    """Put one hook line next to the first anchor line (after the optional 'after' line). Safe to run twice."""
    with open(path, encoding='utf-8', newline='') as fh:
        text = fh.read()
    if HOOK in text:
        return
    eol = '\r\n' if '\r\n' in text else '\n'
    lines = text.split(eol)
    start = 0
    if after:
        start = next((i for i, l in enumerate(lines) if re.search(after, l)), None)
        if start is None:
            raise Fail(f'{path}: could not find "{after}" to place the module hook')
    at = next((i for i in range(start, len(lines)) if re.search(anchor, lines[i])), None)
    if at is None:
        raise Fail(f'{path}: could not find "{anchor}" to place the module hook')
    indent = re.match(r'\s*', lines[at]).group(0) if place == 'before' else ''
    lines.insert(at if place == 'before' else at + 1, indent + line)
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(eol.join(lines))


def install_hooks(server):
    insert_hook(os.path.join(server, 'zone', 'CMakeLists.txt'),
                f'include(${{CMAKE_CURRENT_SOURCE_DIR}}/modules.cmake OPTIONAL) # {HOOK}',
                r'^\s*add_library\(gm_commands_zone\b', place='before')
    rules = os.path.join(server, 'common', 'ruletypes.h')
    if has_custom_rules(server):
        insert_hook(rules, f'#include "modules_rules.h" // {HOOK}',
                    r'^RULE_CATEGORY_END\(\)', after=r'^RULE_CATEGORY\(Custom\)')
    else:
        # Stock EQEmu has no Custom category: modules_rules.h brings its own, after the last category
        insert_hook(rules, f'#include "modules_rules.h" // {HOOK}', r'^#undef RULE_CATEGORY\b')
    insert_hook(os.path.join(server, 'zone', 'command.h'),
                f'#include "modules_commands.h" // {HOOK}',
                r'^void command_zone\(Client', place='after')
    insert_hook(os.path.join(server, 'zone', 'command.cpp'),
                f'#include "modules_commands.inc" // {HOOK}',
                r'command_add\("zone",')


def has_custom_rules(server):
    """True when the base's own ruletypes.h has a Custom rule category (NMS does, stock EQEmu does not)."""
    with open(os.path.join(server, 'common', 'ruletypes.h'), encoding='utf-8', errors='replace') as fh:
        return any(re.match(r'RULE_CATEGORY\(Custom\)', l) for l in fh)


def c_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def macro(name):
    return 'EQMOD_' + re.sub(r'[^A-Z0-9]', '_', name.upper())


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)


def generate(server, mods, names, base):
    head = '// Generated by eqemu-modules tools/modules.py. Do not edit: install again instead.\n'
    rules, decls, adds, cmake = [head], [head], [head], ['# ' + head[3:]]
    defines = [head, '#pragma once\n', f'#define EQMOD_BASE_{base.upper()} 1\n']
    for n in names:
        m = mods[n]
        defines.append(f'#define {macro(n)} 1\n')
        rf = os.path.join(m['_dir'], 'rules.h')
        if os.path.isfile(rf):
            with open(rf, encoding='utf-8') as fh:
                rules.append(f'// {n}\n' + fh.read().rstrip('\n') + '\n')
        for c in m.get('commands', []):
            decls.append(f'void {c["function"]}(Client *c, const Seperator *sep);\n')
            adds.append(f'\t\tcommand_add({c_string(c["name"])}, {c_string(c["description"])}, '
                        f'{c["access"]}, {c["function"]}) ||\n')
        for key, files in m.get('sources', {}).items():
            if files:
                cmake.append(f'list(APPEND {SOURCE_LISTS[key]} {" ".join(files)}) # {n}\n')
    if not has_custom_rules(server):
        rules = rules[:1] + ['RULE_CATEGORY(Custom)\n'] + rules[1:] + ['RULE_CATEGORY_END()\n']
    write(os.path.join(server, 'common', 'modules_rules.h'), ''.join(rules))
    write(os.path.join(server, 'zone', 'modules_commands.h'), ''.join(decls))
    write(os.path.join(server, 'zone', 'modules_commands.inc'), ''.join(adds))
    write(os.path.join(server, 'zone', 'modules.cmake'), ''.join(cmake))
    write(os.path.join(server, 'common', 'modules.h'), ''.join(defines))


def copy_files(m, base, area, dest):
    """Copy a module's new files; return the copied paths relative to dest."""
    out = []
    for top in (os.path.join(m['_dir'], 'files', area), os.path.join(m['_dir'], base, 'files', area)):
        for src in walk(top):
            rel = os.path.relpath(src, top)
            dst = os.path.join(dest, rel)
            if os.path.exists(dst):
                raise Fail(f'{m["name"]}: {area} file {rel} already exists in {dest}')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            out.append(rel.replace('\\', '/'))
    return out


def repo_version():
    r = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else 'unknown'


def install(server, quests, wanted, base=None, allow_dirty=False, log=print):
    mods = load_modules()
    bad = problems(mods)
    if bad:
        raise Fail('the module definitions have problems; run "check":\n  ' + '\n  '.join(bad))
    server = os.path.abspath(server)
    found = detect_base(server)
    base = base or found
    if base != found:
        log(f'note: {server} looks like {found}, installing for {base} as asked')
    if os.path.exists(os.path.join(server, LOCK)):
        raise Fail(f'modules are already installed in {server} ({LOCK}). Start from a clean tree to change the set.')
    for path in (server, quests):
        if path and dirty(path) and not allow_dirty:
            raise Fail(f'{path} has uncommitted changes. Commit or stash them first (or pass --allow-dirty).')
    names = order(mods, wanted)
    for n in names:
        if base not in mods[n]['bases']:
            raise Fail(f'{n} does not support the {base} base')

    install_hooks(server)
    lock = {'base': base, 'repository_version': repo_version(),
            'installed': datetime.datetime.now().isoformat(timespec='seconds'), 'modules': []}
    for n in names:
        m = mods[n]
        entry = {'name': n, 'server_files': copy_files(m, base, 'server', server), 'quest_files': [], 'patches': []}
        if quests:
            entry['quest_files'] = copy_files(m, base, 'quests', quests)
        elif any(walk(os.path.join(m['_dir'], 'files', 'quests'))) or any(walk(os.path.join(m['_dir'], base, 'files', 'quests'))):
            log(f'warning: {n} has quest files; pass --quests to install them')
        for p in patch_files(m, base):
            area = os.path.basename(os.path.dirname(p))
            target = server if area == 'server' else quests
            if target is None:
                log(f'warning: {n}: skipped quest patch {os.path.basename(p)}; pass --quests to apply it')
                continue
            err = apply_patch(target, p)
            if err:
                raise Fail(f'{n}: {os.path.relpath(p, m["_dir"])} does not apply:\n{err}')
            entry['patches'].append(os.path.relpath(p, m['_dir']).replace('\\', '/'))
        lock['modules'].append(entry)
        log(f'installed {n}')
    generate(server, mods, names, base)
    write(os.path.join(server, LOCK), json.dumps(lock, indent=1) + '\n')
    return names


# ---------------------------------------------------------------------------------------------------------------------
# SQL

TRACK = ("CREATE TABLE IF NOT EXISTS `module_sql` (`module` varchar(64) NOT NULL, `file` varchar(255) NOT NULL, "
         "`applied_at` datetime NOT NULL DEFAULT current_timestamp(), PRIMARY KEY (`module`, `file`));\n")


def installed(server):
    path = os.path.join(server, LOCK)
    if not os.path.isfile(path):
        raise Fail(f'no modules are installed in {server} (no {LOCK})')
    with open(path, encoding='utf-8') as fh:
        lock = json.load(fh)
    return lock['base'], [e['name'] for e in lock['modules']]


def pending_sql(server):
    base, names = installed(server)
    mods = load_modules()
    for n in names:
        if n not in mods:
            raise Fail(f'{n} is installed but not in this repository')
        for f in sql_files(mods[n], base):
            yield n, f


def sql(server, mysql=None, out=None, log=print):
    files = list(pending_sql(server))
    if out:
        parts = [TRACK]
        for n, f in files:
            with open(f, encoding='utf-8') as fh:
                parts.append(f'-- {n}: {os.path.basename(f)}\n{fh.read().rstrip()}\n'
                             f"INSERT IGNORE INTO `module_sql` (`module`, `file`) VALUES ('{n}', '{os.path.basename(f)}');\n")
        write(os.path.abspath(out), '\n'.join(parts))
        log(f'wrote {len(files)} SQL files to {out}')
        return
    done_text = run_sql(mysql, TRACK + "SELECT CONCAT('EQMOD|', `module`, '|', `file`) FROM `module_sql`;\n")
    done = {tuple(l.strip().split('|')[1:3]) for l in done_text.splitlines() if l.strip().startswith('EQMOD|')}
    todo = [(n, f) for n, f in files if (n, os.path.basename(f)) not in done]
    for n, f in todo:
        with open(f, encoding='utf-8') as fh:
            body = fh.read()
        run_sql(mysql, body.rstrip() + '\n' +
                f"INSERT INTO `module_sql` (`module`, `file`) VALUES ('{n}', '{os.path.basename(f)}');\n")
        log(f'applied {n}: {os.path.basename(f)}')
    log(f'{len(todo)} applied, {len(files) - len(todo)} already in the database')


def run_sql(mysql, text):
    r = subprocess.run(mysql, shell=True, input=text, capture_output=True, text=True)
    if r.returncode:
        raise Fail(f'the SQL command failed:\n{r.stderr.strip()}')
    return r.stdout


# ---------------------------------------------------------------------------------------------------------------------
# Test


def test(repo, ref, base, server_subdir, quests_subdir, wanted, log=print):
    """Install each module alone, then all of them together, into a scratch worktree of the base."""
    mods = load_modules()
    wanted = wanted or [n for n, m in mods.items() if base in m['bases']]
    work = tempfile.mkdtemp(prefix='eqmod-test-')
    wt = os.path.join(work, 'tree')
    git(repo, 'worktree', 'add', '--detach', '--quiet', wt, ref)
    failed = []
    try:
        server = os.path.join(wt, server_subdir)
        quests = os.path.join(wt, quests_subdir) if quests_subdir else None
        runs = [[n] for n in wanted] + ([wanted] if len(wanted) > 1 else [])
        for run in runs:
            git(wt, 'reset', '--hard', '--quiet')
            git(wt, 'clean', '-fdq')
            label = ', '.join(run) if len(run) == 1 else f'all {len(run)} together'
            try:
                install(server, quests, run, base=base, log=lambda *_: None)
                log(f'ok    {label}')
            except Fail as e:
                failed.append(label)
                log(f'FAIL  {label}\n      ' + str(e).replace('\n', '\n      '))
    finally:
        git(repo, 'worktree', 'remove', '--force', wt, check=False)
        shutil.rmtree(work, ignore_errors=True)
    return failed


# ---------------------------------------------------------------------------------------------------------------------


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list', help='list the modules')
    sub.add_parser('check', help='check the module definitions')
    i = sub.add_parser('install', help='install modules into a server source tree')
    i.add_argument('--server', required=True, help='server source folder (has zone/ and common/)')
    i.add_argument('--quests', help='quests folder; quest files are skipped without it')
    i.add_argument('--base', choices=BASES, help='override the detected base')
    i.add_argument('--all', action='store_true', help='every module that supports the base')
    i.add_argument('--allow-dirty', action='store_true', help='install into a tree with uncommitted changes')
    i.add_argument('modules', nargs='*')
    s = sub.add_parser('sql', help="apply the installed modules' SQL")
    s.add_argument('--server', required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--mysql', help='shell command that runs SQL from stdin against the server database')
    g.add_argument('--out', help='write every SQL file into one script instead')
    t = sub.add_parser('test', help='install into a scratch worktree of a base commit')
    t.add_argument('--repo', required=True)
    t.add_argument('--ref', required=True)
    t.add_argument('--base', choices=BASES, required=True)
    t.add_argument('--server-subdir', default='.')
    t.add_argument('--quests-subdir')
    t.add_argument('modules', nargs='*')
    a = p.parse_args()
    try:
        if a.cmd == 'list':
            for n, m in load_modules().items():
                req = f' (needs {", ".join(m["requires"])})' if m.get('requires') else ''
                print(f'{n:22} {"+".join(m.get("bases", [])):10} {m.get("title", "")}{req}')
        elif a.cmd == 'check':
            bad = problems(load_modules())
            print('\n'.join(bad) if bad else 'ok')
            return 1 if bad else 0
        elif a.cmd == 'install':
            mods = load_modules()
            wanted = a.modules
            if a.all:
                base = a.base or detect_base(os.path.abspath(a.server))
                wanted = [n for n, m in mods.items() if base in m['bases']]
            if not wanted:
                raise Fail('name the modules to install, or pass --all')
            names = install(a.server, a.quests, wanted, a.base, a.allow_dirty)
            print(f'{len(names)} modules installed. Next: build the server, then run "sql" for the database.')
        elif a.cmd == 'sql':
            sql(os.path.abspath(a.server), a.mysql, a.out)
        elif a.cmd == 'test':
            failed = test(os.path.abspath(a.repo), a.ref, a.base, a.server_subdir, a.quests_subdir, a.modules)
            return 1 if failed else 0
    except Fail as e:
        print(f'error: {e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
