#!/usr/bin/env python3
"""Cut one module's lines out of a combined change into a patch against the base.

    python tools/dev/extract_patch.py --repo <git repo> --base <ref> --head <ref> [--prefix <subdir>]
                                      --file <path> --lines 10-20,35-36 [--file ... --lines ...] [--out <patch>]

--lines are line numbers in the head version of the file. Lines added at head inside those ranges are kept; everything
else stays as it is in the base. A replaced block is taken whole when all of its new lines are selected, and left
alone when none are. Paths in the patch are relative to --prefix.

When the module requires another module that edits the same files, pass that module's patch with --after: the hunks
are then cut against the base with it applied, so they still fit when install applies them in order.
"""
import argparse, difflib, os, subprocess, sys, tempfile


def show(repo, ref, path):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=repo, capture_output=True)
    if r.returncode:
        sys.exit(f'git show {ref}:{path} failed: {r.stderr.decode().strip()}')
    return r.stdout.decode('latin-1').splitlines(keepends=True)


def patched(lines, name, patches):
    """The base file after the given patches (a required module's), so this module's hunks fit on top of them."""
    if not patches:
        return lines
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='latin-1', newline='') as fh:
            fh.write(''.join(lines))
        for p in patches:
            # autocrlf off: a global core.autocrlf would otherwise turn every line of the result into a change
            r = subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', '--whitespace=nowarn', f'--include={name}',
                                os.path.abspath(p)],
                               cwd=tmp, capture_output=True, text=True)
            if r.returncode:
                sys.exit(f'{p} does not apply to {name}: {r.stderr.strip()}')
        with open(path, encoding='latin-1', newline='') as fh:
            return fh.read().splitlines(keepends=True)


def ranges(text):
    out = set()
    for part in text.split(','):
        a, _, b = part.partition('-')
        out.update(range(int(a), int(b or a) + 1))
    return out


def shift_inserts(ops, head, keep):
    """Head lines (0-based) that count as added, after sliding inserts the selection says the diff misplaced.

    An added block whose first k lines equal the k lines just after it can be matched either way: the diff may take
    the old 'return; }' as the end of the new block, so the new block lands inside the code above it. When the
    selection covers the block shifted down by k (and none of its first k lines), the shifted block is the added
    one."""
    added = set()
    for tag, i1, i2, j1, j2 in ops:
        if tag != 'insert':
            if tag == 'replace':
                added.update(range(j1, j2))
            continue
        block = set(range(j1, j2))
        if not all(j + 1 in keep for j in block):
            for k in range(1, j2 - j1):
                moved = set(range(j1 + k, j2 + k))
                if (head[j1:j1 + k] == head[j2:j2 + k] and all(j + 1 in keep for j in moved)
                        and not any(j + 1 in keep for j in range(j1, j1 + k))):
                    block = moved
                    break
        added |= block
    return added


def cut(base, head, keep, name, warn):
    result = []
    ops = difflib.SequenceMatcher(None, base, head, autojunk=False).get_opcodes()
    added = shift_inserts(ops, head, keep)
    for tag, i1, i2, j1, j2 in ops:
        if tag == 'delete':
            result += base[i1:i2]
            continue
        if tag == 'equal':
            result += [head[j] for j in range(j1, j2) if j not in added or j + 1 in keep]
            continue
        chosen = [j for j in range(j1, j2) if j + 1 in keep]
        if tag == 'insert':
            result += [head[j] for j in range(j1, j2) if j not in added or j + 1 in keep]
        elif len(chosen) == j2 - j1:
            result += head[j1:j2]
        elif not chosen:
            result += base[i1:i2]
        else:
            warn(f'{name}: head lines {j1 + 1}-{j2} replace base lines {i1 + 1}-{i2} and only some are selected; '
                 'kept the base lines and added the selected ones after them')
            result += base[i1:i2] + [head[j] for j in chosen]
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--base', required=True)
    p.add_argument('--head', required=True)
    p.add_argument('--prefix', default='')
    p.add_argument('--file', action='append', required=True)
    p.add_argument('--lines', action='append', required=True)
    p.add_argument('--after', action='append', default=[],
                   help="a required module's patch: cut against the base with it applied (repeatable, in order)")
    p.add_argument('--out')
    a = p.parse_args()
    if len(a.file) != len(a.lines):
        sys.exit('give one --lines for each --file')
    prefix = a.prefix.strip('/') + '/' if a.prefix else ''
    out = []
    for f, l in zip(a.file, a.lines):
        base, head = patched(show(a.repo, a.base, prefix + f), f, a.after), show(a.repo, a.head, prefix + f)
        new = cut(base, head, ranges(l), f, lambda m: print('warning: ' + m, file=sys.stderr))
        for line in difflib.unified_diff(base, new, 'a/' + f, 'b/' + f, n=3):
            out.append(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n')
    text = ''.join(out)
    if a.out:
        with open(a.out, 'w', encoding='latin-1', newline='') as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


if __name__ == '__main__':
    main()
