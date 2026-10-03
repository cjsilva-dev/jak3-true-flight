#!/usr/bin/env python3
"""Turn an on-device ground scan (mapscan.sh output: MS/MR/MSEND lines) into flight-map.gc.

usage: mapgen.py <jak2|jak3> <scan.txt> <repo goal_src/jakN dir> [--preview out.txt] [--skip a,b]

--skip leaves scanned levels out of the map (waspala: the palace level carries a desert backdrop with
collision, which would claim the desert around Spargus).

Each scanned level becomes one trimmed grid of bytes (0 = no ground, else (height+130 m)/2 m + 1).
The streamer (flight-stream.gc) looks levels up in these grids instead of guessing from checkpoints.
"""
import sys, re, collections

def groups(level_info_path, names):
    """Area groups: two mapped levels are in one area when some checkpoint of the game loads both,
    (Coordinates can't say: in Jak 3, Haven and Spargus overlap in world space.)"""
    s = open(level_info_path).read()
    parent = {n: n for n in names}
    def find(a):
        while parent[a] != a: a = parent[a]
        return a
    for m in re.finditer(r":name \"([^\"]+)\"\s+:level '([\w-]+)(.*?):want-sound", s, re.S):
        wants = [w for w in re.findall(r":name '([\w-]+) :display\?", m.group(3)) if w in parent]
        if m.group(2) in parent: wants.append(m.group(2))
        for w in wants[1:]: parent[find(w)] = find(wants[0])
    # ...or when they hang off the same master level (Jak 3: every Haven district names ctywide;
    # the north and south halves of its Haven never share a checkpoint, but the wall between them
    # can be flown over)
    masters = {}
    cur = None
    for line in s.split('\n'):
        m = re.match(r"\(define ([\w-]+) \(new 'static 'level-load-info", line)
        if m: cur = m.group(1)
        m = re.search(r":master-level '([\w-]+)", line)
        if m and cur in parent: masters.setdefault(m.group(1), []).append(cur)
    for same in masters.values():
        for w in same[1:]: parent[find(w)] = find(same[0])
    roots = []
    out = []
    for n in names:
        r = find(n)
        if r not in roots: roots.append(r)
        out.append(roots.index(r))
    return out

def load(path):
    levels = collections.OrderedDict()
    cur = None
    for line in open(path, errors='replace'):
        p = line.split()
        if not p: continue
        if p[0] == 'MS' and len(p) == 6:
            cur = dict(name=p[1], x0=int(p[2]), z0=int(p[3]), nx=int(p[4]), nz=int(p[5]), rows={})
            levels[p[1]] = cur            # a re-scan replaces the earlier one
        elif p[0] == 'MR' and cur and p[1] == cur['name']:
            cur['rows'][int(p[2])] = [int(v) for v in p[3:]]
        elif p[0] == 'MSEND' and cur and p[1] == cur['name']:
            cur['hits'] = int(p[2]); cur['done'] = True
    out = collections.OrderedDict()
    for name, lv in levels.items():
        if not lv.get('done'): sys.exit(f'{name}: scan incomplete')
        if len(lv['rows']) != lv['nz'] or any(len(r) != lv['nx'] for r in lv['rows'].values()):
            sys.exit(f'{name}: grid size mismatch')
        g = [lv['rows'][i] for i in range(lv['nz'])]
        if sum(1 for r in g for v in r if v) != lv['hits']: sys.exit(f'{name}: hit count mismatch')
        if lv['hits'] == 0: sys.exit(f'{name}: no ground at all')
        # trim to the occupied box
        zs = [i for i, r in enumerate(g) if any(r)]
        xs = [i for i in range(lv['nx']) if any(r[i] for r in g)]
        z_a, z_b, x_a, x_b = zs[0], zs[-1], xs[0], xs[-1]
        g = [r[x_a:x_b + 1] for r in g[z_a:z_b + 1]]
        out[name] = dict(name=name, x0=lv['x0'] + x_a, z0=lv['z0'] + z_a, nx=x_b - x_a + 1, nz=z_b - z_a + 1, g=g, hits=lv['hits'])
    return out

def height(b): return (b - 1) * 2 - 130

def emit(game, levels, path, grp):
    names = list(levels)
    cells = []; dims = []
    for n in names:
        lv = levels[n]
        dims += [lv['x0'], lv['z0'], lv['nx'], lv['nz'], len(cells)]
        for r in lv['g']: cells += r
    o = []
    o.append(';;-*-Lisp-*-\n(in-package goal)\n')
    o.append(f';; name: flight-map.gc ({"Jak II / Dark Flight" if game == "jak2" else "Jak 3 / True Flight"})')
    o.append(';; GENERATED -- do not edit by hand. The real ground of every area the flight streamer manages,')
    o.append(';; scanned in the running game (four rays per 16 m cell, against one level\'s collision at a time).')
    o.append(';; One grid of bytes per level: 0 = this level has no ground in the cell, otherwise the lowest')
    o.append(';; ground found there as (height + 130 m) / 2 m + 1. flight-stream.gc looks levels up here; a level')
    o.append(';; that is not in this file is left to the game\'s own triggers. To add or refresh an area, scan it')
    o.append(';; again and regenerate (tools/flight-map in this repo: fs-mapscan.gc, mapscan.sh, mapgen.py).')
    o.append(';;')
    for i, n in enumerate(names):
        lv = levels[n]
        o.append(f';;   {n:10s} area {grp[i]}  {lv["nx"]:3d} x {lv["nz"]:3d} cells at ({lv["x0"]*16}, {lv["z0"]*16}) m, {lv["hits"]} with ground')
    o.append('')
    o.append('(defconstant FS-MAP-CELL (meters 16))')
    o.append("(define *fs-map-names* (new 'static 'boxed-array :type symbol")
    o.append('                         ' + ' '.join("'" + n for n in names) + '))')
    o.append(';; the area each level belongs to: levels some checkpoint of the game loads together (worlds overlap')
    o.append(';; in coordinates -- Jak 3\'s Haven and Spargus do -- so a lookup only answers within Jak\'s area)')
    o.append(f"(define *fs-map-groups* (new 'static 'array uint8 {len(grp)} " + ' '.join(str(g) for g in grp) + '))')
    o.append(';; per level: x0 z0 (in cells) nx nz, and where its grid starts in *fs-map-cells*')
    o.append(f"(define *fs-map-dims* (new 'static 'array int32 {len(dims)}")
    for i in range(0, len(dims), 5):
        o.append('                        ' + ' '.join(str(v) for v in dims[i:i + 5]))
    o.append('                        ))')
    o.append(f"(define *fs-map-cells* (new 'static 'array uint8 {len(cells)}")
    for i in range(0, len(cells), 40):
        o.append('  ' + ' '.join(str(v) for v in cells[i:i + 40]))
    o.append('  ))')
    open(path, 'w').write('\n'.join(o) + '\n')
    return len(cells)

def preview(levels, path):
    """All levels on one grid; each cell shows the letter of the level with the highest ground, '+' where two overlap."""
    x_a = min(l['x0'] for l in levels.values()); x_b = max(l['x0'] + l['nx'] for l in levels.values())
    z_a = min(l['z0'] for l in levels.values()); z_b = max(l['z0'] + l['nz'] for l in levels.values())
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    lines = [f'{letters[i]} = {n}' for i, n in enumerate(levels)]
    lines.append(f'x {x_a*16}..{x_b*16} m (left to right), z {z_a*16}..{z_b*16} m (top to bottom), lowercase/+ = two levels have ground in the cell')
    for z in range(z_a, z_b):
        row = ''
        for x in range(x_a, x_b):
            best = None; cnt = 0
            for i, l in enumerate(levels.values()):
                ix, iz = x - l['x0'], z - l['z0']
                if 0 <= ix < l['nx'] and 0 <= iz < l['nz'] and l['g'][iz][ix]:
                    cnt += 1
                    if best is None or l['g'][iz][ix] > best[1]: best = (i, l['g'][iz][ix])
            row += '.' if best is None else (letters[best[0]] if cnt == 1 else '+')
        lines.append(row)
    open(path, 'w').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    game, scan, src = sys.argv[1:4]
    levels = load(scan)
    if '--skip' in sys.argv:
        for n in sys.argv[sys.argv.index('--skip') + 1].split(','): levels.pop(n, None)
    grp = groups(f'{src}/engine/level/level-info.gc', list(levels))
    n = emit(game, levels, f'{src}/engine/target/flight-map.gc', grp)
    print(f'{game}: {len(levels)} levels, {n} bytes, areas: ' + '; '.join(' '.join(nm for nm, g in zip(levels, grp) if g == k) for k in sorted(set(grp))))
    if '--preview' in sys.argv: preview(levels, sys.argv[sys.argv.index('--preview') + 1])
