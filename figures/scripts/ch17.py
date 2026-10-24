"""Figures for Chapter 17 — Per-Unit Systems and Network Modeling.

Run from the repository root:  python figures/scripts/ch17.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Circle, Polygon  # noqa: E402
import schemdraw  # noqa: E402
from schemdraw import elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402

schemdraw.use("matplotlib")
CH = "17"


# ------------------------------------------------------------ SLD symbols
def _bus(ax, x0, x1, y, name, lw=3.2, name_x=None):
    ax.plot([x0, x1], [y, y], color=INK, lw=lw, solid_capstyle="butt", zorder=4)
    nx = x0 - 0.15 if name_x is None else name_x
    ax.text(nx, y, name, ha="right", va="center", fontsize=8, fontweight="bold",
            bbox=dict(boxstyle="square,pad=0.25", fc="white", ec=INK, lw=0.9), zorder=6)


def _cb(ax, x, y, s=0.32):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.1, zorder=5))


def _ct(ax, x, y, r=0.13):
    ax.add_patch(Circle((x, y), r, fc="none", ec=INK, lw=1.0, zorder=5))


def _tx_v(ax, x, y, r=0.38, oltc=False):
    """Two-winding transformer, vertical (circles above each other)."""
    for dy in (r * 0.6, -r * 0.6):
        ax.add_patch(Circle((x, y + dy), r, fc="white", ec=INK, lw=1.1, zorder=5))
        ax.add_patch(Circle((x, y + dy), r, fc="none", ec=INK, lw=1.1, zorder=6))
    if oltc:
        ax.annotate("", xy=(x + 0.55, y + 0.65), xytext=(x - 0.55, y - 0.65),
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=8), zorder=7)


def fig_17_1():
    fig, ax = schematic(6.8, 5.0, xlim=(-1.6, 12.6), ylim=(-0.9, 15.2))
    lab = dict(fontsize=7.5, color=INK, va="center", ha="left")
    xm = 3.0
    # grid infeed
    for i in range(3):
        ax.plot([xm - 0.5 + 0.12 * i, xm + 0.5 - 0.12 * i], [14.9 - 0.13 * i] * 2, color=INK, lw=1.4)
    ax.plot([xm, xm], [14.5, 14.9], color=INK, lw=1.1)
    ax.text(xm + 0.7, 14.75, "utility grid 132 kV: fault level 3000 MVA, X/R = 10", **lab)
    _bus(ax, xm - 1.0, xm + 1.0, 14.5, "132 kV")
    ax.plot([xm, xm], [14.5, 9.8], color=INK, lw=1.1, zorder=1)
    _cb(ax, xm, 13.75)
    ax.text(xm + 0.35, 13.75, "132 kV CB", **lab)
    _ct(ax, xm, 13.15)
    _tx_v(ax, xm, 12.0, oltc=True)
    ax.text(xm + 0.75, 12.0, "T1  60 MVA  132/33 kV  Dyn11\nZ = 12 %, X/R = 30\nOLTC ±10 % in 1.25 % steps", **lab)
    _ct(ax, xm, 10.85)
    _cb(ax, xm, 10.3)
    _bus(ax, xm - 1.0, xm + 1.6, 9.8, "33A")
    ax.text(xm + 1.75, 9.8, "33 kV main switchboard", **lab)
    # cable to plant substation
    ax.plot([xm + 0.8, xm + 0.8], [9.8, 6.9], color=INK, lw=1.1, zorder=1)
    _cb(ax, xm + 0.8, 9.3)
    ax.plot([xm + 0.8] * 2, [8.95, 7.75], color=INK, lw=2.6, zorder=2)
    ax.text(xm + 1.15, 8.35, "33 kV XLPE cable, 5 km\n0.13 + j0.11 Ω/km", **lab)
    _cb(ax, xm + 0.8, 7.4)
    _bus(ax, xm - 0.2, xm + 1.8, 6.9, "33B")
    ax.text(xm + 1.95, 6.9, "plant substation 33 kV", **lab)
    # T2
    x2 = xm + 0.8
    ax.plot([x2, x2], [6.9, 4.2], color=INK, lw=1.1, zorder=1)
    _cb(ax, x2, 6.45)
    _ct(ax, x2, 5.95)
    _tx_v(ax, x2, 5.15)
    ax.text(x2 + 0.75, 5.35, "T2  20 MVA  33/6.6 kV  Dyn1\nZ = 8 %, X/R = 15, off-circuit taps", **lab)
    # neutral earthing resistor on the 6.6 kV star point
    ax.plot([x2 - 0.25, x2 - 1.35, x2 - 1.35], [4.75, 4.75, 4.55], color=INK, lw=1.0)
    ax.add_patch(Rectangle((x2 - 1.47, 3.95), 0.24, 0.6, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.plot([x2 - 1.35, x2 - 1.35], [3.95, 3.75], color=INK, lw=1.0)
    for i in range(3):
        ax.plot([x2 - 1.55 + 0.07 * i, x2 - 1.15 - 0.07 * i], [3.75 - 0.09 * i] * 2, color=INK, lw=1.0)
    ax.text(x2 - 1.6, 4.25, "NER\n400 A", fontsize=7.5, ha="right", va="center")
    _ct(ax, x2, 4.55)
    # 6.6 kV board and feeders
    yb = 3.6
    _bus(ax, -0.3, 12.0, yb, "6.6 kV")
    ax.plot([x2, x2], [4.2, yb], color=INK, lw=1.1)
    _cb(ax, x2, 3.95)
    fL, fM, fC, fT = 0.7, 4.7, 7.3, 10.2
    for xf in (fL, fM, fC, fT):
        ax.plot([xf, xf], [yb, 2.5], color=INK, lw=1.1, zorder=1, ls="--" if xf == fM else "-")
        _cb(ax, xf, 3.15)
    ft = dict(fontsize=7.5, ha="center", va="top")
    # existing load
    ax.annotate("", xy=(fL, 1.7), xytext=(fL, 2.55),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, mutation_scale=12))
    ax.text(fL + 0.3, 2.05, "existing\nload 15 MW,\n7 Mvar", fontsize=7.5, ha="left", va="center")
    # proposed motor (dashed)
    ax.add_patch(Circle((fM, 2.0), 0.5, fc="white", ec=INK, lw=1.1, ls="--", zorder=5))
    ax.text(fM, 2.0, "M", fontsize=9, ha="center", va="center", zorder=6)
    ax.text(fM, 1.35, "proposed motor\n5 MW (5.92 MVA)\nX\u2033 = 0.17 pu, X/R = 10", **ft)
    # capacitor bank
    ax.plot([fC, fC], [2.5, 2.2], color=INK, lw=1.1)
    ax.plot([fC - 0.3, fC + 0.3], [2.2, 2.2], color=INK, lw=1.4)
    ax.plot([fC - 0.3, fC + 0.3], [2.0, 2.0], color=INK, lw=1.4)
    ax.plot([fC, fC], [2.0, 1.75], color=INK, lw=1.1)
    for i in range(3):
        ax.plot([fC - 0.22 + 0.07 * i, fC + 0.22 - 0.07 * i], [1.75 - 0.09 * i] * 2, color=INK, lw=1.0)
    ax.text(fC + 0.45, 2.0, "capacitor\nbank\n2.5 Mvar", fontsize=7.5, ha="left", va="center")
    # 6.6/0.4 kV transformer to MCC
    _tx_v(ax, fT, 2.0, r=0.3)
    ax.plot([fT, fT], [1.5, 0.7], color=INK, lw=1.1)
    _bus(ax, fT - 0.6, fT + 1.4, 0.7, "0.4 kV", lw=2.6, name_x=fT - 0.75)
    ax.text(fT + 0.45, 2.05, "2 MVA\n6.6/0.4 kV", fontsize=7.5, ha="left", va="center")
    ax.text(fT + 0.4, 0.35, "400 V MCC", **ft)
    ax.text(-1.5, -0.6, "\u25a1 circuit breaker     \u25cb current transformer     dashed: proposed",
            fontsize=7, color="#555555")
    save(fig, CH, "fig-17-1-plant-single-line")


# ------------------------------------------------------ 17.2 tap-changer pi
def fig_17_2():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.axis("off")
    ax.set_aspect("equal")
    d = schemdraw.Drawing(canvas=ax)
    d.config(fontsize=9, unit=2.5, lw=1.1)
    # top: ideal transformer a:1 in series with admittance y
    yt, gt = 7.0, 4.6
    bi = d.add(elm.Dot().at((0, yt)).label("bus $i$", loc="top"))
    d.add(elm.Line().at((0, yt)).to((1.6, yt)))
    tr = d.add(elm.Transformer(t1=4, t2=4).anchor("p1").at((1.6, yt)).label("$a\\,:\\,1$", loc="top", ofst=0.3))
    d.add(elm.Line().at(tr.s1).to((4.6, yt)))
    d.add(elm.ResistorIEC().at((4.6, yt)).to((7.4, yt)).label("$y=1/(jX)$", ofst=0.15))
    d.add(elm.Line().at((7.4, yt)).to((8.6, yt)))
    d.add(elm.Dot().at((8.6, yt)).label("bus $j$", loc="top"))
    d.add(elm.Line().at(tr.p2).to((tr.p2[0], gt)))
    d.add(elm.Line().at(tr.s2).to((tr.s2[0], gt)))
    d.add(elm.Line().at((0, gt)).to((8.6, gt)).color("#777777"))
    d.add(elm.Gap().at((0, gt)).to((0, yt)).label(("–", "$V_i$", "+"), ofst=-0.6))
    d.add(elm.Gap().at((8.6, gt)).to((8.6, yt)).label(("–", "$V_j$", "+"), ofst=0.5))
    # bottom: equivalent pi
    yb, gb = 2.4, 0.0
    d.add(elm.Dot().at((0, yb)).label("bus $i$", loc="top"))
    d.add(elm.Line().at((0, yb)).to((1.6, yb)))
    d.add(elm.Dot().at((1.6, yb)))
    d.add(elm.ResistorIEC().at((2.4, yb)).to((6.2, yb)))
    d.add(elm.Line().at((1.6, yb)).to((2.4, yb)))
    d.add(elm.Line().at((6.2, yb)).to((7.0, yb)))
    d.add(elm.Dot().at((7.0, yb)))
    d.add(elm.Line().at((7.0, yb)).to((8.6, yb)))
    d.add(elm.Dot().at((8.6, yb)).label("bus $j$", loc="top"))
    d.add(elm.ResistorIEC().at((1.6, yb)).to((1.6, gb)))
    d.add(elm.ResistorIEC().at((7.0, yb)).to((7.0, gb)))
    d.add(elm.Line().at((0, gb)).to((8.6, gb)).color("#777777"))
    d.add(elm.Gap().at((0, gb)).to((0, yb)).label(("–", "$V_i$", "+"), ofst=-0.6))
    d.add(elm.Gap().at((8.6, gb)).to((8.6, yb)).label(("–", "$V_j$", "+"), ofst=0.5))
    d.draw(show=False)
    ax.text(4.3, yb + 0.55, "$y/a$\n$-j9.524$ pu", ha="center", va="bottom", fontsize=9)
    ax.text(1.95, 1.2, "$y(1-a)/a^2$\n$+j0.454$ pu\n(capacitive)", ha="left", va="center", fontsize=8.5)
    ax.text(6.65, 1.2, "$y(a-1)/a$\n$-j0.476$ pu\n(inductive)", ha="right", va="center", fontsize=8.5)
    ax.text(5.6, gt + 0.12, "reference (neutral)", ha="center", va="bottom", fontsize=8, color="#666666")
    ax.text(4.3, gb - 0.35, "reference (neutral)", ha="center", va="top", fontsize=8, color="#666666")
    ax.text(-0.9, 8.4, "(a) transformer with off-nominal tap", fontsize=9, fontweight="bold")
    ax.text(-0.9, 3.95, "(b) equivalent π in per unit,  X = 0.10 pu (y = −j10),  a = 1.05",
            fontsize=9, fontweight="bold")
    ax.set_xlim(-1.0, 9.6)
    ax.set_ylim(-0.8, 8.9)
    save(fig, CH, "fig-17-2-off-nominal-tap-pi")


# ------------------------------------------------- 17.3 three-winding star
def _zbox(ax, p0, p1, label, frac=0.5, w=0.32, L=1.1, lab_off=(0.0, 0.0), ha="left"):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    v = p1 - p0
    n = np.linalg.norm(v)
    u = v / n
    c = p0 + v * frac
    a, b = c - u * L / 2, c + u * L / 2
    ax.plot([p0[0], a[0]], [p0[1], a[1]], color=INK, lw=1.1)
    ax.plot([b[0], p1[0]], [b[1], p1[1]], color=INK, lw=1.1)
    nrm = np.array([-u[1], u[0]]) * w / 2
    ax.add_patch(Polygon([a + nrm, b + nrm, b - nrm, a - nrm], fc="white", ec=INK, lw=1.1, zorder=4))
    ax.text(c[0] + lab_off[0], c[1] + lab_off[1], label, ha=ha, va="center", fontsize=9)


def fig_17_3():
    fig, ax = schematic(6.6, 4.0, xlim=(0, 13.2), ylim=(-0.6, 7.4))
    # left: three-winding transformer symbol
    cx, cy, r = 2.4, 3.9, 0.85
    centres = {"P": (cx, cy + 0.55), "S": (cx - 0.55, cy - 0.45), "T": (cx + 0.55, cy - 0.45)}
    for k, (x, y) in centres.items():
        ax.add_patch(Circle((x, y), r, fc="none", ec=INK, lw=1.2))
    ax.plot([cx, cx], [cy + 1.4, cy + 2.4], color=INK, lw=1.1)
    ax.plot([cx - 1.2, cx - 1.9], [cy - 1.0, cy - 1.7], color=INK, lw=1.1)
    ax.plot([cx + 1.2, cx + 1.9], [cy - 1.0, cy - 1.7], color=INK, lw=1.1)
    ax.text(cx, cy + 2.55, "P: 132 kV, 60 MVA", ha="center", va="bottom", fontsize=8.5)
    ax.text(cx - 1.95, cy - 1.85, "S: 33 kV\n60 MVA", ha="center", va="top", fontsize=8.5)
    ax.text(cx + 1.95, cy - 1.85, "T: 11 kV\n20 MVA", ha="center", va="top", fontsize=8.5)
    ax.annotate("", xy=(5.9, 3.9), xytext=(4.7, 3.9),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, mutation_scale=12))
    # right: star equivalent
    n = np.array([9.0, 3.6])
    P = np.array([9.0, 6.6])
    S = np.array([6.6, 1.3])
    T = np.array([11.4, 1.3])
    _zbox(ax, n, P, "$Z_p = j0.067$", lab_off=(0.35, 0.0))
    _zbox(ax, n, S, "$Z_s = j0.133$", lab_off=(-0.35, 0.15), ha="right")
    _zbox(ax, n, T, "$Z_t = j0.267$", lab_off=(0.35, 0.15))
    ax.add_patch(Circle(n, 0.09, fc=INK, zorder=5))
    ax.text(n[0] - 0.3, n[1] + 0.35, "star point\n(fictitious)", fontsize=7.5, va="bottom", ha="right",
            color="#555555")
    for pt, name in [(P, "P (132 kV)"), (S, "S (33 kV)"), (T, "T (11 kV)")]:
        ax.add_patch(Circle(pt, 0.11, fc="white", ec=INK, lw=1.1, zorder=5))
    ax.text(P[0], P[1] + 0.25, "P (132 kV)", ha="center", va="bottom", fontsize=8.5)
    ax.text(S[0], S[1] - 0.25, "S (33 kV)", ha="center", va="top", fontsize=8.5)
    ax.text(T[0], T[1] - 0.25, "T (11 kV)", ha="center", va="top", fontsize=8.5)
    ax.text(0.1, -0.25, "All values in pu on 100 MVA.  Test values:  $Z_{ps}$ = 0.200,  $Z_{pt}$ = 0.333,  $Z_{st}$ = 0.400 pu",
            fontsize=8.5, va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#F4F4F4", ec="#BBBBBB", lw=0.8))
    save(fig, CH, "fig-17-3-three-winding-star")


# -------------------------------------------------------- 17.4 load models
def fig_17_4():
    fig, ax = new_fig(6.4, 3.9)
    V = np.linspace(0.7, 1.1, 200)
    ax.axvspan(0.95, 1.05, color="#EAF2FA", zorder=0)
    ax.text(1.0, 0.43, "normal\noperating range", ha="center", va="bottom", fontsize=8, color="#336699")
    curves = [
        (0, "constant power, $n=0$", COLORS[7]),
        (0.18, "industrial, $n=0.18$", COLORS[4]),
        (1.0, "constant current, $n=1$", COLORS[2]),
        (1.2, "residential summer, $n=1.2$", COLORS[3]),
        (2.0, "constant impedance, $n=2$", COLORS[0]),
    ]
    ax.set_xlim(0.7, 1.1)
    ax.set_ylim(0.25, 1.25)
    fig.canvas.draw()

    def tag(x, f, df, text, c, above):
        y = f(x)
        p0 = ax.transData.transform((x, y))
        p1 = ax.transData.transform((x + 0.01, y + 0.01 * df(x)))
        ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
        dy = 0.012 if above else -0.012
        ax.text(x, y + dy, text, color=c, fontsize=8, rotation=ang, rotation_mode="anchor",
                ha="left", va="bottom" if above else "top")

    for n, lab, c in curves:
        ax.plot(V, V ** n, color=c)
    q = V ** 3.5
    m = q <= 1.25
    ax.plot(V[m], q[m], color=COLORS[1], ls="--")
    tag(0.712, lambda v: v ** 0, lambda v: 0.0, curves[0][1], curves[0][2], True)
    tag(0.712, lambda v: v ** 0.18, lambda v: 0.18 * v ** -0.82, curves[1][1], curves[1][2], False)
    tag(0.775, lambda v: v, lambda v: 1.0, curves[2][1], curves[2][2], True)
    tag(0.775, lambda v: v ** 1.2, lambda v: 1.2 * v ** 0.2, curves[3][1], curves[3][2], False)
    tag(0.80, lambda v: v ** 2, lambda v: 2 * v, curves[4][1], curves[4][2], False)
    tag(0.76, lambda v: v ** 3.5, lambda v: 3.5 * v ** 2.5, "$Q/Q_0$ commercial, $n_q=3.5$ (dashed)",
        COLORS[1], False)
    ax.annotate("1.40 at 1.1 pu\n(off scale)", xy=(V[m][-1], 1.25), xytext=(1.0, 1.17), fontsize=7.5,
                ha="right", va="center", color=COLORS[1],
                arrowprops=dict(arrowstyle="-|>", lw=0.7, color=COLORS[1], mutation_scale=7))
    ax.plot([0.7, 1.1], [0.49, 1.21], "o", ms=3.5, color=COLORS[0], clip_on=False, zorder=5)
    ax.text(0.705, 0.475, "0.49", fontsize=7.5, color=COLORS[0], va="top")
    ax.text(1.095, 1.21, "1.21", fontsize=7.5, color=COLORS[0], ha="right", va="bottom")
    ax.plot([0.7], [0.7 ** 3.5], "o", ms=3.5, color=COLORS[1], clip_on=False, zorder=5)
    ax.text(0.705, 0.7 ** 3.5 - 0.005, "0.29", fontsize=7.5, color=COLORS[1], va="top")
    ax.set_xlabel("Supply voltage $\\bar V$ (pu)")
    ax.set_ylabel("$P/P_0$  (or $Q/Q_0$)")
    ax.grid(True, color=GRID, lw=0.5)
    save(fig, CH, "fig-17-4-load-models")


# ---------------------------------------------------- 17.5 four-bus network
def _min_degree_order(adj):
    """Minimum-degree ordering of a symmetric graph (adjacency as list of sets), with fill tracking."""
    g = [set(s) for s in adj]
    alive = set(range(len(g)))
    order = []
    while alive:
        v = min(alive, key=lambda i: (len(g[i]), i))
        nb = list(g[v])
        for a in nb:
            g[a].discard(v)
            for b in nb:
                if a != b:
                    g[a].add(b)
        alive.discard(v)
        g[v] = set()
        order.append(v)
    return np.array(order)


def _synthetic_grid(n=2000, seed=7):
    """Planar-like transmission topology: nearest-neighbour links on random points, mean degree ~3."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    from scipy.spatial import Delaunay
    tri = Delaunay(pts)
    edges = set()
    for s in tri.simplices:
        for i in range(3):
            a, b = sorted((s[i], s[(i + 1) % 3]))
            edges.add((a, b))
    edges = np.array(sorted(edges))
    L = np.linalg.norm(pts[edges[:, 0]] - pts[edges[:, 1]], axis=1)
    keep = edges[np.argsort(L)]
    # keep a spanning tree plus the shortest extra edges until mean degree ~ 3
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.sparse import coo_matrix
    W = coo_matrix((L, (edges[:, 0], edges[:, 1])), shape=(n, n))
    T = minimum_spanning_tree(W).tocoo()
    chosen = set(zip(T.row.tolist(), T.col.tolist()))
    chosen = {tuple(sorted(e)) for e in chosen}
    target = int(1.5 * n)
    for a, b in keep:
        if len(chosen) >= target:
            break
        chosen.add((int(a), int(b)))
    adj = [set() for _ in range(n)]
    for a, b in chosen:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def fig_17_5():
    fig = plt.figure(figsize=(6.8, 4.3))
    ax = fig.add_axes([0.0, 0.0, 0.6, 1.0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.6)
    ax.set_aspect("equal")
    ax.axis("off")
    pos = {1: (1.6, 6.6), 2: (8.0, 6.6), 4: (4.8, 4.2), 3: (6.4, 1.6)}
    for b, (x, y) in pos.items():
        ax.plot([x - 0.8, x + 0.8], [y, y], color=INK, lw=3.2, solid_capstyle="butt", zorder=4)
    ax.text(pos[1][0] - 0.95, pos[1][1], "1", fontsize=10, fontweight="bold", ha="right", va="center")
    ax.text(pos[2][0] + 0.95, pos[2][1], "2", fontsize=10, fontweight="bold", ha="left", va="center")
    ax.text(pos[4][0] - 0.95, pos[4][1], "4", fontsize=10, fontweight="bold", ha="right", va="center")
    ax.text(pos[3][0] + 0.95, pos[3][1], "3", fontsize=10, fontweight="bold", ha="left", va="center")

    def line(p, q, lab, off, ha="center"):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.1, zorder=2)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ax.text(mx + off[0], my + off[1], lab, fontsize=8, ha=ha, va="center", color=COLORS[0])

    line((pos[1][0] + 0.3, pos[1][1]), (pos[4][0] - 0.3, pos[4][1]), "0.02 + j0.08", (-0.3, -0.45), ha="right")
    line((pos[2][0] - 0.3, pos[2][1]), (pos[4][0] + 0.3, pos[4][1]), "0.01 + j0.06", (-0.35, 0.15), ha="right")
    line((pos[3][0] - 0.4, pos[3][1]), (pos[4][0], pos[4][1]), "0.015 + j0.09", (-0.25, 0.0), ha="right")
    line((pos[2][0] + 0.4, pos[2][1]), (pos[3][0] + 0.5, pos[3][1]), "0.02 + j0.12", (0.25, 0.0), ha="left")
    # generator at bus 1
    gx, gy = pos[1][0], pos[1][1] + 1.0
    ax.plot([gx, gx], [pos[1][1], gy - 0.4], color=INK, lw=1.1)
    ax.add_patch(Circle((gx, gy), 0.4, fc="white", ec=INK, lw=1.1, zorder=5))
    ax.text(gx, gy, "G", ha="center", va="center", fontsize=9, zorder=6)
    ax.text(gx + 0.55, gy, "generator\n$X_d''$ = 0.20 pu", fontsize=8, va="center")
    # grid infeed at bus 2
    ix, iy = pos[2][0], pos[2][1]
    ax.plot([ix, ix], [iy, iy + 0.75], color=INK, lw=1.1)
    for i in range(3):
        ax.plot([ix - 0.45 + 0.12 * i, ix + 0.45 - 0.12 * i], [iy + 0.75 + 0.13 * i] * 2, color=INK, lw=1.4)
    ax.text(ix - 0.6, iy + 0.95, "grid infeed\n0.05 pu", fontsize=8, va="center", ha="right")
    # load at bus 3
    ax.annotate("", xy=(pos[3][0], pos[3][1] - 0.95), xytext=(pos[3][0], pos[3][1]),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, mutation_scale=12))
    ax.text(pos[3][0] + 0.2, pos[3][1] - 0.7, "load", fontsize=8, va="center")
    ax.text(pos[4][0] + 0.25, pos[4][1] - 0.35, "passive tee", fontsize=8, va="top", ha="left")
    # fault levels
    fl = dict(fontsize=8, color=COLORS[1], fontweight="bold")
    ax.text(pos[1][0], pos[1][1] - 0.3, "1056 MVA", ha="center", va="top", **fl)
    ax.text(pos[2][0] + 0.45, pos[2][1] - 0.3, "2304 MVA", ha="left", va="top", **fl)
    ax.text(pos[3][0] - 0.85, pos[3][1] - 0.35, "984 MVA", ha="right", va="top", **fl)
    ax.text(0.2, 0.35, "132 kV, impedances in pu on 100 MVA;\nfault levels (orange) from $Z_{kk}$ of $\\mathbf{Z}_{bus}$",
            fontsize=7.5, va="bottom", color="#444444")

    # right top: 4x4 sparsity pattern of Ybus
    axm = fig.add_axes([0.64, 0.50, 0.30, 0.44])
    nz = np.zeros((4, 4), bool)
    for i in range(4):
        nz[i, i] = True
    for i, j in [(0, 3), (1, 2), (1, 3), (2, 3)]:
        nz[i, j] = nz[j, i] = True
    for i in range(4):
        for j in range(4):
            axm.add_patch(Rectangle((j, 3 - i), 1, 1, fc=COLORS[0] if nz[i, j] else "white",
                                    ec=INK, lw=0.8))
    axm.set_xlim(0, 4)
    axm.set_ylim(0, 4)
    axm.set_aspect("equal")
    axm.set_xticks(np.arange(4) + 0.5)
    axm.set_xticklabels(["1", "2", "3", "4"])
    axm.set_yticks(np.arange(4) + 0.5)
    axm.set_yticklabels(["4", "3", "2", "1"])
    axm.xaxis.tick_top()
    axm.tick_params(length=0, labelsize=8)
    for s in axm.spines.values():
        s.set_visible(False)
    axm.set_title("$\\mathbf{Y}_{bus}$: 10 nonzero, 6 zero", fontsize=8.5, y=-0.13)

    # right bottom: 2000-bus pattern after minimum-degree ordering
    axs = fig.add_axes([0.67, 0.02, 0.25, 0.30])
    adj = _synthetic_grid()
    order = _min_degree_order(adj)
    inv = np.empty_like(order)
    inv[order] = np.arange(len(order))
    rows, cols = [], []
    for i, nb in enumerate(adj):
        rows.append(inv[i])
        cols.append(inv[i])
        for j in nb:
            rows.append(inv[i])
            cols.append(inv[j])
    n = len(adj)
    density = len(rows) / n ** 2 * 100
    axs.plot(cols, rows, color=COLORS[0], marker="s", markersize=0.7, markeredgewidth=0, ls="none")
    axs.set_xlim(0, n)
    axs.set_ylim(n, 0)
    axs.set_aspect("equal")
    axs.set_xticks([])
    axs.set_yticks([])
    for s in axs.spines.values():
        s.set_visible(True)
        s.set_color("#888888")
        s.set_linewidth(0.8)
    axs.set_title(f"2000-bus model, {density:.2f} % nonzero\n(minimum-degree ordering)", fontsize=7.5)
    save(fig, CH, "fig-17-5-four-bus-network")


if __name__ == "__main__":
    fig_17_1()
    fig_17_2()
    fig_17_3()
    fig_17_4()
    fig_17_5()
