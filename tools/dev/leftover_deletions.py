#!/usr/bin/env python3
"""List lines the source change deleted from the base that an installed tree still has.

    python tools/dev/leftover_deletions.py --tree <installed tree> --repo <source repo> --base <ref> --head <ref>
                                           [--prefix <subdir>]

Install modules into a clean checkout of the base first. For every file install changed, the lines head deleted or
replaced that are still there untouched are printed with head's version beside them. Each one either belongs to a
module that hasn't been moved yet, or is a deletion a module's patch missed (see extract_patch.py's b selector).
"""
import argparse, difflib, subprocess, sys


def show(repo, ref, path):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=repo, capture_output=True)
    return r.stdout.decode('latin-1').splitlines() if r.returncode == 0 else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--tree', required=True)
    p.add_argument('--repo', required=True)
    p.add_argument('--base', required=True)
    p.add_argument('--head', required=True)
    p.add_argument('--prefix', default='', help='subfolder of --tree and --repo to compare (default: all)')
    a = p.parse_args()
    files = subprocess.run(['git', 'diff', '--name-only', '--', a.prefix or '.'], cwd=a.tree, capture_output=True,
                           text=True, check=True).stdout.split()
    found = 0
    for f in files:
        base, head = show(a.repo, a.base, f), show(a.repo, a.head, f)
        if base is None or head is None:
            continue
        with open(f'{a.tree}/{f}', encoding='latin-1') as fh:
            inst = fh.read().splitlines()
        kept = set()
        for tag, i1, i2, _, _ in difflib.SequenceMatcher(None, base, inst, autojunk=False).get_opcodes():
            if tag == 'equal':
                kept.update(range(i1, i2))
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, head, autojunk=False).get_opcodes():
            if tag not in ('delete', 'replace'):
                continue
            left = [i for i in range(i1, i2) if i in kept and base[i].strip()]
            if not left:
                continue
            found += len(left)
            print(f'{f}: base {i1 + 1}-{i2} -> head {j1 + 1}-{j2}' + (' (deleted)' if tag == 'delete' else ''))
            for i in range(i1, i2):
                print('  -', base[i])
            for j in range(j1, min(j2, j1 + 4)):
                print('  +', head[j])
            if j2 - j1 > 4:
                print(f'  + ... {j2 - j1 - 4} more')
    print(f'{found} line(s) left', file=sys.stderr)


if __name__ == '__main__':
    main()
