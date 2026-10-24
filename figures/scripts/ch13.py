"""Figures for Chapter 13 — Power System Structure.

Run from the repository root:  python figures/scripts/ch13.py
"""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy.interpolate import PchipInterpolator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, arrow, box, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

CH = "13"
BLUE, VERM, GREEN, PINK, ORANGE, SKY = COLORS[:6]


# ---------------------------------------------------------------- drawing helpers
def line(ax, xs, ys, lw=1.2, color=INK, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def busbar(ax, x0, x1, y, lw=3.2, color=INK):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, solid_capstyle="butt", zorder=4)


def gen(ax, x, y, r=0.38, fc="white"):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=1.2, zorder=5))
    t = np.linspace(-1, 1, 40)
    ax.plot(x + 0.55 * r * t, y + 0.25 * r * np.sin(np.pi * t), color=INK, lw=1.0, zorder=6)


def xfmr(ax, x, y, r=0.26, vertical=True):
    """Two-winding transformer as two overlapping circles centred on (x, y)."""
    d = 0.62 * r
    c = [(x, y + d), (x, y - d)] if vertical else [(x - d, y), (x + d, y)]
    for cx, cy in c:
        ax.add_patch(Circle((cx, cy), r, fc="none", ec=INK, lw=1.1, zorder=5))
    return (r + d)


def cb(ax, x, y, s=0.32, fc=INK, ec=INK, **kw):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=ec, lw=1.1, zorder=6, **kw))


def disc_v(ax, x, y, h=0.36):
    """Vertical disconnector (open-blade symbol drawn closed) centred at (x, y)."""
    ax.plot([x, x], [y - h / 2, y + h / 2], color="white", lw=2.6, zorder=5)
    ax.plot([x, x + 0.13], [y - h / 2, y + h / 2 - 0.02], color=INK, lw=1.1, zorder=6)
    ax.plot([x - 0.08, x + 0.08], [y + h / 2, y + h / 2], color=INK, lw=1.1, zorder=6)


def disc_h(ax, x, y, w=0.36):
    ax.plot([x - w / 2, x + w / 2], [y, y], color="white", lw=2.6, zorder=5)
    ax.plot([x - w / 2, x + w / 2 - 0.02], [y, y + 0.13], color=INK, lw=1.1, zorder=6)
    ax.plot([x + w / 2, x + w / 2], [y - 0.08, y + 0.08], color=INK, lw=1.1, zorder=6)


def ct_v(ax, x, y, r=0.13):
    ax.add_patch(Circle((x, y), r, fc="none", ec=INK, lw=0.9, zorder=6))


# ---------------------------------------------------------------- Figure 13.1
def fig_13_1():
    """Supply chain from generator to customer with voltage levels and losses.

    Drawn as a two-row chain (generation and transmission on top, left to right;
    distribution below, returning right to left) so that every block is legible.
    """
    fig, ax = schematic(6.8, 5.0, xlim=(-0.2, 17), ylim=(-0.45, 12.4))
    w, h, fs = 2.5, 1.8, 7.6
    y1, y2 = 8.2, 3.25                         # bottoms of row 1 and row 2
    c1, c2 = y1 + h / 2, y2 + h / 2             # centre lines
    TX, DX = "#EEF3F8", "#E8F0E0"
    # row 1
    box(ax, 0.0, y1, w, h, "Generator\n22 kV\n1,000 MVA", fc="#FCE9DC", fontsize=fs)
    box(ax, 3.5, y1, w, h, "GSU\ntransformer\n22/400 kV", fc=TX, fontsize=fs)
    tx = 8.1
    pts = np.array([[tx - 0.8, c1 - 0.6], [tx + 0.8, c1 - 0.6], [tx, c1 + 0.65]])
    for i in range(3):
        a_, b_ = pts[i], pts[(i + 1) % 3]
        line(ax, [a_[0], b_[0]], [a_[1], b_[1]], lw=1.6, color=BLUE)
    for p_ in pts:
        ax.add_patch(Rectangle((p_[0] - 0.17, p_[1] - 0.17), 0.34, 0.34, fc=BLUE, ec=BLUE, zorder=5))
    ax.text(tx, y1 - 0.2, "400 kV meshed\ntransmission", ha="center", va="top", fontsize=fs, color=BLUE)
    box(ax, 10.1, y1, w, h, "Bulk-supply\nsubstation\n400/132 kV", fc=TX, fontsize=fs)
    arrow(ax, 2.5, c1, 3.5, c1)
    ax.text(3.0, c1 + 0.12, "22 kV", ha="center", va="bottom", fontsize=7.4)
    arrow(ax, 6.0, c1, 7.05, c1)
    ax.text(6.52, c1 + 0.12, "400 kV", ha="center", va="bottom", fontsize=7.4)
    arrow(ax, 9.15, c1, 10.1, c1)
    ax.text(9.62, c1 + 0.12, "400 kV", ha="center", va="bottom", fontsize=7.4)
    # 132 kV subtransmission: right then down to row 2
    xs = 15.6
    line(ax, [12.6, xs], [c1, c1], lw=1.3)
    arrow(ax, xs, c1, xs, y2 + h)
    ax.text(xs + 0.15, (c1 + y2 + h) / 2, "132 kV\nsub-\ntransmission", ha="left", va="center", fontsize=7.6)
    # bulk loads on the 132 kV line
    for xl, txt in ((12.95, "Data centre\n132 kV"), (15.25, "Steel works\n132 kV")):
        box(ax, xl - 1.1, 10.75, 2.2, 1.0, txt, fc="#FDF3D9", fontsize=7.4)
        arrow(ax, xl, c1, xl, 10.75)
    ax.add_patch(Circle((12.95, c1), 0.07, fc=INK, zorder=6))
    ax.add_patch(Circle((15.25, c1), 0.07, fc=INK, zorder=6))
    # row 2, right to left
    blocks2 = [(15.6, "Primary\nsubstation\n132/33 kV", TX), (11.5, "Primary\nsubstation\n33/11 kV", TX),
               (7.4, "Distribution\ntransformer\n11/0.4 kV\n1 MVA", TX), (2.7, "LV customers\n400/230 V", DX)]
    for xc, txt, fc in blocks2:
        bw = w
        box(ax, xc - bw / 2, y2, bw, h, txt, fc=fc, fontsize=fs)
    arrow(ax, 15.6 - w / 2, c2, 11.5 + w / 2, c2)
    ax.text(14.0, c2 + 0.12, "33 kV", ha="center", va="bottom", fontsize=7.4)
    arrow(ax, 11.5 - w / 2, c2, 7.4 + w / 2, c2)
    ax.text(9.45, c2 + 0.12, "11 kV", ha="center", va="bottom", fontsize=7.4)
    ax.text(9.45, c2 - 0.12, "radial\nfeeder", ha="center", va="top", fontsize=7.4)
    arrow(ax, 7.4 - w / 2, c2, 2.7 + w / 2, c2)
    ax.text(5.1, c2 + 0.12, "0.4 kV", ha="center", va="bottom", fontsize=7.4)
    # embedded generation at 33 kV and 0.4 kV
    box(ax, 12.6, 1.25, 2.0, 1.0, "Wind farm\n33 kV", fc=DX, fontsize=7.4)
    arrow(ax, 13.6, 2.25, 13.6, c2 - 0.02)
    box(ax, 11.75, 6.1, 2.6, 1.0, "Solar plant\n50 MW, 33 kV", fc=DX, fontsize=7.4)
    arrow(ax, 13.2, 6.1, 13.2, c2 + 0.02)
    for xj in (13.6, 13.2):
        ax.add_patch(Circle((xj, c2), 0.07, fc=INK, zorder=6))
    box(ax, 1.7, 1.25, 2.0, 1.0, "Rooftop PV\n0.4 kV", fc=DX, fontsize=7.4)
    arrow(ax, 2.7, 2.25, 2.7, y2)
    # losses bar
    yl, hl = -0.35, 1.15
    segs = [("GSU\n0.3 %", 0.12), ("Transmission\n1.5–3 %", 0.35),
            ("Subtransmission\nand primary  1–2 %", 0.28), ("MV and LV\ndistribution  3–5 %", 0.6)]
    widths = [2.2, 3.6, 4.7, 4.7]
    x0 = 1.6
    cmap = plt.get_cmap("Oranges")
    ax.text(x0 - 0.1, yl + hl / 2, "Typical\nlosses", ha="right", va="center", fontsize=7.8, fontweight="bold")
    for (txt, sh), wd in zip(segs, widths):
        ax.add_patch(Rectangle((x0, yl), wd, hl, fc=cmap(0.12 + 0.6 * sh), ec=INK, lw=0.8))
        ax.text(x0 + wd / 2, yl + hl / 2, txt, ha="center", va="center", fontsize=7.4, color=INK)
        x0 += wd
    save(fig, CH, "fig-13-1-supply-chain-voltage-levels")


# ---------------------------------------------------------------- Figure 13.2
def fig_13_2():
    """Meshed 400 kV ring feeding radial 132 kV and 11 kV distribution."""
    fig, ax = schematic(6.8, 5.6, xlim=(0, 17), ylim=(-0.3, 13.6))
    S = {"A": (3.0, 11.0), "B": (8.0, 12.6), "C": (13.0, 11.0), "D": (11.4, 7.7), "E": (4.6, 7.7)}
    hw = 0.75
    # lines: ring + diagonals; A-B double circuit
    # (from, offset along its busbar, to, offset)
    pairs = [("A", 0.55, "B", -0.6), ("B", 0.6, "C", -0.45), ("C", 0.45, "D", 0.55), ("D", -0.55, "E", 0.55),
             ("E", -0.45, "A", -0.2), ("B", 0.2, "D", 0.0), ("B", -0.2, "E", 0.0)]
    for p, op, q, oq in pairs:
        (x0, y0), (x1, y1) = S[p], S[q]
        x0, x1 = x0 + op, x1 + oq
        if (p, q) == ("A", "B"):
            dx, dy = x1 - x0, y1 - y0
            n = np.array([-dy, dx]) / np.hypot(dx, dy) * 0.13
            for sgn in (-1, 1):
                line(ax, [x0 + sgn * n[0], x1 + sgn * n[0]], [y0 + sgn * n[1], y1 + sgn * n[1]], lw=1.3, color=BLUE)
        else:
            line(ax, [x0, x1], [y0, y1], lw=1.3, color=BLUE)
    for k, (x, y) in S.items():
        busbar(ax, x - hw, x + hw, y, lw=4)
        if k in ("C", "D"):
            ax.text(x + hw + 0.12, y + 0.1, k, ha="left", va="bottom", fontsize=10, fontweight="bold", color=INK)
        else:
            ax.text(x - hw - 0.12, y + 0.1, k, ha="right", va="bottom", fontsize=10, fontweight="bold",
                    color=INK)
    ax.text(8.0, 9.55, "400 kV meshed transmission\n(8 circuits; A–B double circuit)", ha="center",
            va="center", fontsize=8, color=BLUE, bbox=dict(fc="white", ec="none", pad=1.5))
    # generators at A
    xa, ya = S["A"]
    for i, gx in enumerate([xa - 0.45, xa + 0.45]):
        line(ax, [gx, gx], [ya, ya + 0.35])
        xfmr(ax, gx, ya + 0.62, r=0.2)
        line(ax, [gx, gx], [ya + 0.88, ya + 1.0])
        gen(ax, gx, ya + 1.3, r=0.3)
    ax.text(xa - 1.0, ya + 1.3, "2 × 660 MW\ncoal", ha="right", va="center", fontsize=8)
    # CCGT at C
    xc, yc = S["C"]
    line(ax, [xc, xc], [yc, yc + 0.35])
    xfmr(ax, xc, yc + 0.62, r=0.2)
    line(ax, [xc, xc], [yc + 0.88, yc + 1.0])
    gen(ax, xc, yc + 1.3, r=0.3)
    ax.text(xc + 0.5, yc + 1.3, "1,200 MW\nCCGT", ha="left", va="center", fontsize=8)
    # HVDC at E
    xe, ye = S["E"]
    line(ax, [xe - hw, 2.35], [ye, ye])
    ax.add_patch(Rectangle((1.45, ye - 0.45), 0.9, 0.9, fc="white", ec=INK, lw=1.1, zorder=5))
    ax.plot([1.45, 2.35], [ye - 0.45, ye + 0.45], color=INK, lw=0.9, zorder=6)
    ax.text(1.68, ye + 0.2, "~", ha="center", va="center", fontsize=9, zorder=7)
    ax.text(2.12, ye - 0.22, "=", ha="center", va="center", fontsize=9, zorder=7)
    line(ax, [1.45, 0.3], [ye, ye], lw=1.3, color=VERM, ls="--")
    ax.text(0.1, ye + 0.65, "HVDC converter:\n1,000 MW link to\nneighbouring\nsynchronous area", ha="left",
            va="bottom", fontsize=7.6, color=VERM)
    # D: two 240 MVA transformers to 132 kV
    xd, yd = S["D"]
    y132 = 5.7
    for tx in (xd - 0.45, xd + 0.45):
        line(ax, [tx, tx], [yd, yd - 0.4])
        xfmr(ax, tx, yd - 0.85, r=0.22)
        line(ax, [tx, tx], [yd - 1.13, y132])
    ax.text(xd - 0.8, yd - 0.85, "2 × 240 MVA\n400/132 kV", ha="right", va="center", fontsize=7.6)
    busbar(ax, xd - 0.9, xd + 0.9, y132, lw=3.2, color=GREEN)
    ax.text(xd - 0.95, y132 + 0.12, "D 132 kV", ha="right", va="bottom", fontsize=7.6, color=GREEN)
    # 132 kV double-circuit ring: D132 -> P3 -> P2 -> P1 -> D132
    P = {"P1": (6.4, 4.7), "P2": (10.8, 2.6), "P3": (15.2, 4.3)}
    ring = [(xd + 0.6, y132), P["P3"], P["P2"], P["P1"], (xd - 0.6, y132)]
    for (x0, y0), (x1, y1) in zip(ring[:-1], ring[1:]):
        dx, dy = x1 - x0, y1 - y0
        n = np.array([-dy, dx]) / np.hypot(dx, dy) * 0.09
        for sgn in (-1, 1):
            line(ax, [x0 + sgn * n[0], x1 + sgn * n[0]], [y0 + sgn * n[1], y1 + sgn * n[1]], lw=1.0, color=GREEN)
    for k, (x, y) in P.items():
        busbar(ax, x - 0.5, x + 0.5, y, lw=3.2, color=GREEN)
    ax.text(P["P3"][0] + 0.1, P["P3"][1] + 0.2, "Primary\nsubstation 3", ha="center", va="bottom", fontsize=7.4)
    ax.text(P["P2"][0] + 0.7, P["P2"][1] - 0.05, "Primary\nsubstation 2", ha="left", va="center", fontsize=7.4)
    ax.text(13.6, 1.55, "132 kV double-circuit ring", ha="center", va="center", fontsize=7.6, color=GREEN)
    # P1: two 30 MVA 132/11 kV transformers, 11 kV bus, four radial feeders
    x1, y1 = P["P1"]
    y11 = 2.9
    for tx in (x1 - 0.35, x1 + 0.35):
        line(ax, [tx, tx], [y1, y1 - 0.35])
        xfmr(ax, tx, y1 - 0.8, r=0.2)
        line(ax, [tx, tx], [y1 - 1.06, y11])
    ax.text(x1 - 0.65, y1 + 0.15, "Primary substation 1\n2 × 30 MVA, 132/11 kV", ha="right", va="bottom",
            fontsize=7.4)
    busbar(ax, 1.4, 7.0, y11, lw=3.0, color=ORANGE)
    ax.text(1.3, y11, "11 kV", ha="right", va="center", fontsize=7.6, color="#9A6400")
    fx = [2.0, 3.6, 5.2, 6.6]
    ybot = 0.55
    for i, x in enumerate(fx):
        cb(ax, x, y11 - 0.38, s=0.24)
        line(ax, [x, x], [y11, ybot if i < 2 else 0.25], lw=1.1, color=ORANGE)
        ax.annotate("", xy=(x - 0.22, 1.55), xytext=(x - 0.22, 2.2),
                    arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.2, mutation_scale=10))
        for yy in ((1.85, 1.0) if i < 2 else (1.85, 1.0)):   # 11/0.4 kV distribution substations
            line(ax, [x, x + 0.2], [yy, yy], lw=0.9, color=ORANGE)
            xfmr(ax, x + 0.43, yy, r=0.12, vertical=False)
    for x in fx[:2]:
        ax.plot([x - 0.15, x + 0.15], [ybot, ybot], color=ORANGE, lw=1.0)
    # NOP between feeders 3 and 4 at their far ends
    xa3, xa4 = fx[2], fx[3]
    yn = 0.25
    line(ax, [xa3, xa3 + 0.35], [yn, yn], lw=1.1, color=ORANGE)
    line(ax, [xa4 - 0.35, xa4], [yn, yn], lw=1.1, color=ORANGE)
    ax.plot([xa3 + 0.35, xa4 - 0.38], [yn, yn + 0.32], color=INK, lw=1.3)
    ax.plot([xa4 - 0.35, xa4 - 0.35], [yn - 0.1, yn + 0.1], color=INK, lw=1.3)
    ax.text((xa3 + xa4) / 2, yn - 0.12, "NOP", ha="center", va="top", fontsize=7.6, fontweight="bold")
    ax.text(7.55, 1.45, "radial 11 kV feeders\n(arrows: power flow;\n" + "small symbols: 11/0.4 kV\nsubstations)",
            ha="left", va="center", fontsize=7.2, color=VERM)
    # divider between layers
    ax.plot([0, 17], [6.75, 6.75], color="#BBBBBB", lw=0.8, ls=":")
    ax.text(16.95, 6.85, "transmission (meshed)", ha="right", va="bottom", fontsize=7.4, color="#666666")
    ax.text(16.95, 6.65, "distribution (radial)", ha="right", va="top", fontsize=7.4, color="#666666")
    save(fig, CH, "fig-13-2-grid-architecture-mesh-radial")


# ---------------------------------------------------------------- Figure 13.3
def fig_13_3():
    """Breaker-and-a-half 400 kV switchyard, three diameters."""
    fig, ax = schematic(6.8, 5.5, xlim=(0, 17), ylim=(-1.4, 12.3))
    yB1, yB2 = 11.0, 1.4
    busbar(ax, 0.6, 16.6, yB1, lw=4.5)
    busbar(ax, 0.6, 16.6, yB2, lw=4.5)
    ax.text(0.5, yB1, "Bus 1\n400 kV", ha="right", va="center", fontsize=8.5, fontweight="bold")
    ax.text(0.5, yB2, "Bus 2\n400 kV", ha="right", va="center", fontsize=8.5, fontweight="bold")
    xs = [1.6, 7.0, 12.4]
    ycb = [9.5, 6.2, 2.9]          # breakers top, middle, bottom
    ynode = [7.85, 4.55]            # upper and lower circuit connection points
    circuits = [("G", "G1", "22/400 kV\n800 MVA GSU"), ("L", "L1", ""),
                ("L", "L2", ""), ("T", "T1", "400/132 kV\n240 MVA"),
                ("G", "G2", "22/400 kV\n800 MVA GSU"), ("T", "T2", "400/132 kV\n240 MVA")]
    for d, x in enumerate(xs):
        line(ax, [x, x], [yB2, yB1], lw=1.3)
        for y in ycb:
            disc_v(ax, x, y + 0.65)
            disc_v(ax, x, y - 0.65)
            cb(ax, x, y, s=0.5)
            ct_v(ax, x, y + 0.36, r=0.11)
        for y in ynode:
            ax.add_patch(Circle((x, y), 0.07, fc=INK, ec=INK, zorder=7))
        ax.text(x, yB1 + 0.35, f"Diameter {d + 1}", ha="center", va="bottom", fontsize=8.2)
        for j, y in enumerate(ynode):
            kind, name, sub = circuits[2 * d + j]
            x0 = x
            line(ax, [x0, x0 + 1.2], [y, y], lw=1.2)
            disc_h(ax, x0 + 0.65, y)
            if kind == "L":
                ax.annotate("", xy=(x0 + 2.7, y), xytext=(x0 + 1.2, y),
                            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=11))
                ax.text(x0 + 2.85, y, f"Line {name}", ha="left", va="center", fontsize=8.5)
            elif kind == "G":
                r = 0.27
                xfmr(ax, x0 + 1.2 + 0.43, y, r=r, vertical=False)
                line(ax, [x0 + 1.2 + 0.86, x0 + 2.55], [y, y])
                gen(ax, x0 + 2.95, y, r=0.38)
                ax.text(x0 + 2.95, y + 0.55, name, ha="center", va="bottom", fontsize=8.5, fontweight="bold")
                ax.text(x0 + 1.63, y - 0.4, sub, ha="center", va="top", fontsize=7.0)
            else:
                r = 0.27
                xfmr(ax, x0 + 1.2 + 0.43, y, r=r, vertical=False)
                ax.annotate("", xy=(x0 + 3.0, y), xytext=(x0 + 2.06, y),
                            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=10))
                ax.text(x0 + 1.63, y + 0.4, name, ha="center", va="bottom", fontsize=8.5, fontweight="bold")
                ax.text(x0 + 1.63, y - 0.4, sub, ha="center", va="top", fontsize=7.0)
                ax.text(x0 + 3.05, y, "132 kV", ha="left", va="center", fontsize=7.4)
    # highlight middle breaker of diameter 1 as open
    x = xs[0]
    cb(ax, x, ycb[1], s=0.5, fc="white", ec=VERM)
    ax.add_patch(Rectangle((x - 0.42, ycb[1] - 0.42), 0.84, 0.84, fc="none", ec=VERM, lw=1.2, ls="--", zorder=7))
    ax.text(x - 0.5, ycb[1], "open", ha="right", va="center", fontsize=7.6, color=VERM)
    note = ("Middle breaker of diameter 1 open (dashed): G1 is still connected through its top breaker to Bus 1\n"
            "and L1 through its bottom breaker to Bus 2, so both circuits stay in service.")
    ax.text(8.6, 0.25, note, ha="center", va="center", fontsize=7.6, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FBE3D6", ec=VERM, lw=0.8))
    # legend
    yl = -1.05
    cb(ax, 2.0, yl, s=0.3)
    ax.text(2.3, yl, "circuit breaker", ha="left", va="center", fontsize=7.4)
    disc_v(ax, 5.3, yl)
    ax.text(5.6, yl, "disconnector", ha="left", va="center", fontsize=7.4)
    ct_v(ax, 8.3, yl, r=0.11)
    ax.text(8.55, yl, "current transformer", ha="left", va="center", fontsize=7.4)
    ax.text(16.6, yl, "3 breakers per 2 circuits", ha="right", va="center", fontsize=7.4, style="italic")
    save(fig, CH, "fig-13-3-breaker-and-a-half-substation")


# ---------------------------------------------------------------- Figure 13.4
def fig_13_4():
    """AC versus DC transmission cost and break-even distances."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw=dict(width_ratios=[1.55, 1]))
    x = np.linspace(0, 1200, 400)
    ac, dc = 0.15 + 0.00085 * x, 0.55 + 0.0003 * x
    xb = 0.40 / 0.00055
    a1.axvspan(600, 800, color="#EEEEEE", zorder=0)
    a1.plot(x, ac, color=BLUE, label="AC overhead line")
    a1.plot(x, dc, color=VERM, label="DC overhead line")
    a1.plot(xb, 0.15 + 0.00085 * xb, "o", color=INK, ms=5, zorder=5)
    a1.annotate(f"break-even ≈ {xb:.0f} km\n(range 600–800 km)", xy=(xb, 0.15 + 0.00085 * xb),
                xytext=(250, 1.55), fontsize=8.5, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    a1.text(1190, 0.15 + 0.00085 * 1190 + 0.06, "AC", color=BLUE, ha="right", va="bottom", fontsize=9)
    a1.text(1190, 0.55 + 0.0003 * 1190 - 0.07, "DC", color=VERM, ha="right", va="top", fontsize=9)
    a1.text(20, 0.62, "two converter\nstations", fontsize=7.8, color=VERM, va="bottom")
    a1.set(xlim=(0, 1200), ylim=(0, 3.0), xlabel="Distance (km)",
           ylabel="Relative total cost\n(1.0 = 1,000 km AC line)")
    a1.set_title("(a) Overhead lines", fontsize=10, loc="left")
    xc = np.linspace(0, 200, 300)
    acc, dcc = 0.1 + 0.008 * xc, 0.55 + 0.0025 * xc
    xbc = 0.45 / 0.0055
    a2.axvspan(50, 100, color="#EEEEEE", zorder=0)
    a2.plot(xc, acc, color=BLUE, ls="--", label="AC cable")
    a2.plot(xc, dcc, color=VERM, ls="--", label="DC cable")
    a2.plot(xbc, 0.1 + 0.008 * xbc, "o", color=INK, ms=5, zorder=5)
    a2.annotate(f"break-even ≈ {xbc:.0f} km\n(range 50–100 km)", xy=(xbc, 0.1 + 0.008 * xbc),
                xytext=(100, 0.2), fontsize=8.5, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    a2.text(148, 1.72, "AC cable", color=BLUE, ha="right", va="bottom", fontsize=9)
    a2.text(197, 0.72, "DC cable", color=VERM, ha="right", va="top", fontsize=9)
    a2.set(xlim=(0, 200), ylim=(0, 3.0), xlabel="Distance (km)")
    a2.set_title("(b) Submarine or underground cables", fontsize=10, loc="left")
    fig.tight_layout()
    save(fig, CH, "fig-13-4-ac-dc-breakeven")


# ---------------------------------------------------------------- Figure 13.5
def demand_curve(t):
    th = [0, 2, 4, 6, 7.5, 9, 11, 12, 13, 14, 15, 16.5, 18, 19, 19.5, 20.5, 22, 23, 24]
    dh = [25.6, 24.4, 24.0, 25.0, 27.4, 30.0, 31.5, 31.95, 32.0, 32.2, 33.0, 34.4, 36.6, 38.0, 37.6, 35.2, 30.2, 27.0, 25.6]
    return PchipInterpolator(th, dh)(t)


def solar_curve(t):
    s = np.clip(np.sin(np.pi * (t - 6) / 14), 0, None) ** 2
    return np.where((t > 6) & (t < 20), 16.0 * s, 0.0)


def fig_13_5():
    """Daily demand, solar and net load (duck curve)."""
    fig, ax = new_fig(6.4, 3.9)
    t = np.linspace(0, 24, 1441)
    d, s = demand_curve(t), solar_curve(t)
    n = d - s
    ax.fill_between(t, 0, s, color=ORANGE, alpha=0.35, lw=0, label="Solar output")
    ax.plot(t, d, color=BLUE, label="Total demand")
    ax.plot(t, n, color=INK, ls="--", label="Net load (demand − solar)")
    i_min = np.argmin(n[600:960]) + 600
    i_max = np.argmax(n[960:1260]) + 960
    tmin, nmin, tmax, nmax = t[i_min], n[i_min], t[i_max], n[i_max]
    ax.plot([tmin, tmax], [nmin, nmax], "o", color=INK, ms=4)
    ax.annotate(f"minimum net load\n{nmin:.0f} GW at about 13:00",
                xy=(tmin, nmin), xytext=(8.2, 8.0), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.annotate("", xy=(tmax - 0.15, nmax), xytext=(tmax - 0.15, nmin),
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.6, mutation_scale=12))
    ax.plot([tmin, tmax - 0.15], [nmin, nmin], color=VERM, lw=0.8, ls=":")
    hm = lambda t_: f"{int(round(t_ * 60)) // 60:02d}:{int(round(t_ * 60)) % 60:02d}"  # noqa: E731
    ax.text(tmax + 0.25, (nmin + nmax) / 2 - 3,
            f"evening ramp\n≈ {nmax - nmin:.0f} GW\n{hm(round(tmin))}–{hm(tmax)}",
            ha="left", va="center", fontsize=8.5, color=VERM)
    ax.text(13, 5.5, "solar\n(peak 16 GW)", ha="center", va="center", fontsize=8.5, color="#8A5A00")
    ax.set(xlim=(0, 24), ylim=(0, 40), xlabel="Time of day", ylabel="Power (GW)")
    ax.set_xticks(range(0, 25, 3), [f"{h:02d}:00" for h in range(0, 25, 3)])
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, CH, "fig-13-5-daily-load-and-net-load")
    return nmin, tmin, nmax, tmax


# ---------------------------------------------------------------- Figure 13.6
def fig_13_6():
    """Screening curves above the load-duration curve."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1, 1], hspace=0.12))
    h = np.linspace(0, 8760, 500)
    techs = [("OCGT", 60, 0.120, VERM), ("CCGT", 110, 0.065, ORANGE), ("Coal", 230, 0.035, INK)]
    for name, F, V, c in techs:
        a1.plot(h, F + V * h, color=c, label=f"{name}: {F} + {V:.3f} h")
    h1, h2 = 50 / 0.055, 120 / 0.030
    for hx in (h1, h2):
        for a in (a1, a2):
            a.axvline(hx, color="#777777", ls="--", lw=0.9)
    a1.plot([h1, h2], [60 + 0.12 * h1, 230 + 0.035 * h2], "o", color=INK, ms=4)
    a1.text(h1 + 80, 60 + 0.12 * h1 - 70, f"{h1:,.0f} h", fontsize=8.5)
    a1.text(h2 + 80, 230 + 0.035 * h2 - 75, f"{h2:,.0f} h", fontsize=8.5)
    a1.set(ylim=(0, 1200), ylabel="Annual cost\n(USD/kW-yr)")
    a1.legend(loc="upper left", fontsize=8.2)
    # load-duration curve
    ldc = PchipInterpolator([0, 300, h1, 2200, h2, 6500, 8760], [10.0, 9.25, 8.6, 7.55, 6.4, 5.3, 4.5])
    y = ldc(h)
    a2.fill_between(h, 0, np.minimum(y, 6.4), color="#9DB7CF", lw=0)
    a2.fill_between(h, 6.4, np.clip(y, 6.4, 8.6), where=y > 6.4, color="#F3C77A", lw=0)
    a2.fill_between(h, 8.6, np.clip(y, 8.6, 10), where=y > 8.6, color="#EE9B76", lw=0)
    a2.plot(h, y, color=INK)
    for yy in (6.4, 8.6):
        a2.axhline(yy, color="#555555", lw=0.6, ls=":")
    a2.text(5600, 3.2, "Baseload (coal)  0–6.4 GW", ha="center", va="center", fontsize=8.5)
    a2.text(5600, 7.5, "CCGT  6.4–8.6 GW (2.2 GW)", ha="left", va="center", fontsize=8.5)
    a2.annotate("", xy=(2300, 7.5), xytext=(5550, 7.5),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=9))
    a2.text(5600, 9.3, "OCGT  8.6–10 GW (1.4 GW)", ha="left", va="center", fontsize=8.5)
    a2.annotate("", xy=(330, 9.3), xytext=(5550, 9.3),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=9))
    a2.set(xlim=(0, 8760), ylim=(0, 10.5), ylabel="Demand (GW)", xlabel="Hours per year")
    a2.set_xticks([0, 909, 2000, 4000, 6000, 8760], ["0", "909", "2,000", "4,000", "6,000", "8,760"])
    fig.align_ylabels([a1, a2])
    save(fig, CH, "fig-13-6-screening-and-load-duration")


if __name__ == "__main__":
    fig_13_1()
    fig_13_2()
    fig_13_3()
    fig_13_4()
    print(fig_13_5())
    fig_13_6()
