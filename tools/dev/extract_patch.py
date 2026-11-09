#!/usr/bin/env python3
"""Cut one module's lines out of a combined change into a patch against the base.

    python tools/dev/extract_patch.py --repo <git repo> --base <ref> --head <ref> [--prefix <subdir>]
                                      --file <path> --lines 10-20,35-36 [--file ... --lines ...] [--out <patch>]

--lines are line numbers in the head version of the file. Lines added at head inside those ranges are kept; everything
else stays as it is in the base. A replaced block is taken whole when all of its new lines are selected, and left
alone when none are. Paths in the patch are relative to --prefix.
"""
import argparse, difflib, subprocess, sys


def show(repo, ref, path):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=repo, capture_output=True)
    if r.returncode:
        sys.exit(f'git show {ref}:{path} failed: {r.stderr.decode().strip()}')
    return r.stdout.decode('latin-1').splitlines(keepends=True)


def ranges(text):
    out = set()
    for part in text.split(','):
        a, _, b = part.partition('-')
        out.update(range(int(a), int(b or a) + 1))
    return out


def cut(base, head, keep, name, warn):
    result = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, head, autojunk=False).get_opcodes():
        if tag == 'equal' or tag == 'delete':
            result += base[i1:i2]
            continue
        chosen = [j for j in range(j1, j2) if j + 1 in keep]
        if tag == 'insert':
            result += [head[j] for j in chosen]
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
    p.add_argument('--out')
    a = p.parse_args()
    if len(a.file) != len(a.lines):
        sys.exit('give one --lines for each --file')
    prefix = a.prefix.strip('/') + '/' if a.prefix else ''
    out = []
    for f, l in zip(a.file, a.lines):
        base, head = show(a.repo, a.base, prefix + f), show(a.repo, a.head, prefix + f)
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
