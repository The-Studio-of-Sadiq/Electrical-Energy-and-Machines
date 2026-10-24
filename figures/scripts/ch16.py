"""Figures for Chapter 16 — Energy Storage.

Run from the repository root:  python figures/scripts/ch16.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch  # noqa: E402
import schemdraw  # noqa: E402
from schemdraw import elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402

schemdraw.use("matplotlib")
CH = "16"


# ---------------------------------------------------------------- 16.1 Ragone
def fig_16_1():
    fig, ax = new_fig(6.6, 4.6)
    regions = [  # name, E range (Wh/kg), P range (W/kg), colour, label position (E, P)
        ("Electrolytic\ncapacitors", (0.01, 0.1), (1e4, 1e5), "#777777", (0.032, 3.2e4)),
        ("Super-\ncapacitors", (1, 10), (1e3, 2e4), COLORS[0], (2.4, 6.5e3)),
        ("Flywheels (system)", (5, 30), (1e3, 1e4), COLORS[3], (7.5, 740)),
        ("Lead-acid", (25, 40), (50, 300), COLORS[4], (31, 28)),
        ("NiCd", (40, 60), (100, 500), COLORS[6], (49, 600)),
        ("LTO", (60, 100), (1000, 4000), COLORS[5], (78, 5.6e3)),
        ("LFP", (100, 180), (200, 2000), COLORS[2], (135, 120)),
        ("NMC", (150, 270), (300, 3000), COLORS[1], (300, 4.4e3)),
        ("H$_2$ fuel-cell system\n(700 bar tank)", (300, 1000), (50, 500), "#888888", (550, 22)),
    ]
    # constant-discharge-time diagonals: P = E / t
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 1000)
    ax.set_ylim(1, 1e5)
    E = np.logspace(-2, 3, 50)
    p1 = ax.transData.transform((1, 1))
    p2 = ax.transData.transform((10, 10))
    ang = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    for t_h, lab, Ex in [(0.001, "3.6 s", 45), (0.01, "36 s", 450), (0.1, "6 min", 600),
                         (1, "1 h", 600), (10, "10 h", 18)]:
        ax.plot(E, E / t_h, ls="--", lw=0.8, color="#999999", zorder=1)
        ax.text(Ex, Ex / t_h * 1.15, lab, fontsize=8, color="#666666", rotation=ang,
                rotation_mode="anchor", ha="left", va="bottom")
    for name, (e0, e1), (p0, p1), c, (lx, ly) in regions:
        ax.add_patch(Rectangle((e0, p0), e1 - e0, p1 - p0, fc=c, ec=c, alpha=0.28, lw=1.2, zorder=2))
        ax.add_patch(Rectangle((e0, p0), e1 - e0, p1 - p0, fc="none", ec=c, lw=1.2, zorder=3))
        ax.text(lx, ly, name, fontsize=8.5, ha="center", va="center", color=INK, zorder=4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 1000)
    ax.set_ylim(1, 1e5)
    ax.set_xlabel("Specific energy (Wh/kg)")
    ax.set_ylabel("Specific power (W/kg)")
    ax.grid(True, which="major", color=GRID, lw=0.6)
    ax.text(0.012, 1.6, "dashed lines: constant discharge time $t=E/P$", fontsize=8, color="#666666")
    save(fig, CH, "fig-16-1-ragone-plot")


# ----------------------------------------------------- 16.2 BESS single line
def _breaker(ax, x, y, s=0.32, horiz=True):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.1, zorder=5))


def _xfmr(ax, x, y, r=0.32, horiz=True, lab=None, lab_dy=0.55, fs=7.5, oltc=False):
    dx, dy = (0.42 * r * 2 / 2, 0) if horiz else (0, 0.42 * r * 2 / 2)
    for s in (-1, 1):
        ax.add_patch(Circle((x + s * dx, y + s * dy), r, fc="none", ec=INK, lw=1.1, zorder=5))
    if oltc:
        ax.annotate("", xy=(x + 0.55, y + 0.55), xytext=(x - 0.55, y - 0.55),
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=8), zorder=6)
    if lab:
        ax.text(x, y + lab_dy, lab, ha="center", va="bottom", fontsize=fs, color=INK)


def _fuse(ax, x, y, w=0.36, h=0.16):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.plot([x - w / 2, x + w / 2], [y, y], color=INK, lw=0.8, zorder=6)


def _disc(ax, x, y, L=0.4):
    ax.plot([x - L / 2, x - L / 2 + 0.05], [y, y], color=INK, lw=1.2, zorder=5)
    ax.add_patch(Rectangle((x - L / 2, y - 0.06), L, 0.12, fc="white", ec="none", zorder=4))
    ax.plot([x - L / 2, x + L / 2 - 0.02], [y, y + 0.22], color=INK, lw=1.2, zorder=5)
    ax.plot([x + L / 2, x + L / 2], [y, y], color=INK, lw=1.2, zorder=5)


def fig_16_2():
    fig, ax = schematic(6.8, 5.2, xlim=(-0.3, 19.9), ylim=(-0.2, 14.0))
    rows = [(11.3, "DC block 1"), (8.3, "DC block 2"), (3.8, "DC block 26")]
    xbus = 12.6  # 33 kV switchboard (vertical bus)
    comm = dict(color=COLORS[1], lw=0.9, ls=(0, (3, 2)))
    lab = dict(fontsize=7.5, color=INK)
    for k, (y, name) in enumerate(rows):
        for j in range(4):  # four containers, 2 x 2
            cx = 0.3 + (j % 2) * 1.0
            cy = y + 0.08 - (j // 2) * 0.66
            ax.add_patch(Rectangle((cx, cy), 0.85, 0.52, fc="#E8F1E4", ec=INK, lw=0.9, zorder=3))
            ax.plot([cx + 0.35] * 2, [cy + 0.12, cy + 0.40], color=INK, lw=1.1, zorder=4)
            ax.plot([cx + 0.5] * 2, [cy + 0.18, cy + 0.34], color=INK, lw=2.2, zorder=4)
            ax.plot([cx + 0.85, 2.6], [cy + 0.26] * 2, color=INK, lw=0.9)
        ax.text(0.3, y + 0.85, name, fontsize=8, fontweight="bold", color=INK)
        ax.plot([2.6, 2.6], [y - 0.7, y + 0.75], color=INK, lw=2.6)  # 1500 V DC bus
        ax.plot([2.6, 5.2], [y, y], color=INK, lw=1.1)
        _fuse(ax, 3.3, y)
        _disc(ax, 4.2, y)
        ax.add_patch(Rectangle((5.2, y - 0.5), 1.3, 1.0, fc="#EEF3F8", ec=INK, lw=1.0, zorder=3))
        ax.plot([5.2, 6.5], [y - 0.5, y + 0.5], color=INK, lw=0.7, zorder=4)
        ax.text(5.48, y + 0.22, "=", fontsize=9, ha="center", va="center")
        ax.text(6.22, y - 0.25, "~", fontsize=10, ha="center", va="center")
        ax.plot([6.5, 7.6], [y, y], color=INK, lw=1.1)
        _xfmr(ax, 8.0, y, r=0.32)
        ax.plot([8.4, xbus], [y, y], color=INK, lw=1.1)
        _breaker(ax, xbus - 0.55, y)
        # BMS hierarchy, dashed communication to the plant controller
        ax.text(0.3, y - 0.75, "BMS: cell →\nstring → block", fontsize=6.8, color=COLORS[1], va="top")
        ax.plot([0.05, 0.25], [y - 1.0] * 2, **comm)
    ax.plot([0.05, 0.05, 6.5], [rows[0][0] - 1.0, 0.85, 0.85], **comm)
    # component labels on block 1 (all blocks identical)
    y1 = rows[0][0]
    ax.text(3.0, y1 + 0.75, "1500 V DC bus", ha="left", va="bottom", **lab)
    ax.text(3.55, y1 - 0.4, "DC fuse,\ndisconnector", ha="center", va="top", **lab)
    ax.text(6.0, y1 - 0.6, "PCS 4 MVA\n690 V AC\nη 98.5 %", ha="center", va="top", **lab)
    ax.text(8.0, y1 - 0.45, "4 MVA\n0.69/33 kV\nDy11", ha="center", va="top", **lab)
    ax.text(10.1, y1 + 0.15, "33 kV cable ring", ha="center", va="bottom", **lab)
    ax.text(xbus, 12.8, "33 kV\nswitchboard", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.text(0.3, 6.25, "⋮   DC blocks 3 – 25 identical: 26 blocks × 4 MVA", fontsize=8.5, va="center")
    ax.text(0.3, 5.5, "each container: 12 strings × 416 LFP cells,\n1331 V nominal, ≈ 4.5 MWh",
            fontsize=7, va="center", style="italic", color="#333333")
    ax.plot([xbus, xbus], [3.0, 12.7], color=INK, lw=3)
    # main transformer branch to the point of interconnection
    ym = 9.8
    ax.plot([xbus, 18.7], [ym, ym], color=INK, lw=1.1)
    _breaker(ax, xbus + 0.6, ym)
    _xfmr(ax, 14.3, ym, r=0.45, oltc=True)
    ax.text(14.3, ym + 0.6, "main TX\n120 MVA\n33/132 kV\nYNd1, OLTC", ha="center", va="bottom", **lab)
    ax.add_patch(Circle((15.6, ym), 0.17, fc="none", ec=INK, lw=1.0, zorder=5))
    ax.text(15.6, ym + 0.3, "CT", ha="center", va="bottom", **lab)
    ax.plot([16.4, 16.4], [ym, ym - 0.45], color=INK, lw=1.0)
    _xfmr(ax, 16.4, ym - 0.75, r=0.16, horiz=False)
    ax.text(16.65, ym - 0.8, "VT", ha="left", va="center", **lab)
    ax.text(16.4, ym + 0.75, "POI", fontsize=8, ha="center", va="bottom", fontweight="bold")
    ax.plot([16.4, 16.4], [ym + 0.75, ym + 0.15], color=INK, lw=0.7)
    _breaker(ax, 17.6, ym)
    ax.text(17.6, ym + 0.3, "132 kV\nCB", ha="center", va="bottom", **lab)
    for i in range(3):
        ax.plot([18.7 + 0.14 * i] * 2, [ym - 0.55 + 0.14 * i, ym + 0.55 - 0.14 * i], color=INK, lw=1.4)
    ax.text(18.85, ym - 0.7, "grid\n132 kV", ha="center", va="top", fontsize=8)
    # auxiliary supply
    ya = 4.8
    ax.plot([xbus, 15.4], [ya, ya], color=INK, lw=1.1)
    _breaker(ax, xbus + 0.6, ya)
    _xfmr(ax, 14.3, ya, r=0.32)
    ax.text(14.3, ya + 0.5, "aux. TX 2 MVA\n33/0.4 kV", ha="center", va="bottom", **lab)
    ax.add_patch(Rectangle((15.4, ya - 0.6), 3.6, 1.2, fc="#F6F0E6", ec=INK, lw=0.9))
    ax.text(17.2, ya, "aux. loads 0.4 kV\nHVAC, fire, BMS", ha="center", va="center", **lab)
    # plant controller
    ax.add_patch(Rectangle((6.5, 0.25), 4.8, 1.2, fc="#FFF4D6", ec=INK, lw=1.0))
    ax.text(8.9, 0.85, "Plant controller (PPC / EMS)", ha="center", va="center", fontsize=8)
    ax.plot([16.4, 16.4, 19.6, 19.6, 11.3], [ym - 0.95, ym - 1.9, ym - 1.9, 0.85, 0.85], **comm)
    ax.text(19.4, 2.2, "POI P, Q, V\nmeasurements", fontsize=7.5, color=COLORS[1], ha="right", va="center")
    ax.text(0.25, 1.4, "BMS data", fontsize=7.5, color=COLORS[1], va="center")
    save(fig, CH, "fig-16-2-bess-single-line")


# ------------------------------------------------- 16.3 OCV curves and ECM
def _ocv_nmc(s):
    pts_s = [0, 5, 10, 20, 35, 50, 65, 80, 90, 100]
    pts_v = [3.00, 3.38, 3.50, 3.60, 3.67, 3.75, 3.85, 3.95, 4.06, 4.20]
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(pts_s, pts_v)(s)


def _ocv_lfp(s):
    pts_s = [0, 2, 5, 10, 20, 30, 60, 90, 95, 98, 100]
    pts_v = [2.50, 2.95, 3.12, 3.20, 3.25, 3.28, 3.305, 3.33, 3.37, 3.45, 3.60]
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(pts_s, pts_v)(s)


def fig_16_3():
    fig = plt.figure(figsize=(6.8, 3.6))
    ax = fig.add_axes([0.08, 0.13, 0.45, 0.82])
    s = np.linspace(0, 100, 401)
    ax.plot(s, _ocv_nmc(s), color=COLORS[1], label="NMC")
    h = 0.0125  # half of 25 mV hysteresis
    ax.plot(s, _ocv_lfp(s) + h, color=COLORS[2], lw=1.4, label="LFP charge")
    ax.plot(s, _ocv_lfp(s) - h, color=COLORS[2], lw=1.4, ls="--", label="LFP discharge")
    # 2 mV error band on plateau: +-2 mV around 3.305 V at 60 % -> +-4 %
    ax.axvspan(56, 64, ymin=0, ymax=1, color=COLORS[2], alpha=0.15, lw=0)
    ax.annotate("±2 mV error\n= ±4 % SoC\non LFP plateau", xy=(60, 3.30), xytext=(30, 2.68),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK,
                                                         mutation_scale=8))
    ax.annotate("≈ 8 mV per %", xy=(50, 3.75), xytext=(28, 4.12), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=8))
    ax.annotate("≈ 0.5 mV per %", xy=(75, 3.32), xytext=(66, 3.55), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=8))
    ax.set_xlim(0, 100)
    ax.set_ylim(2.5, 4.3)
    ax.set_xlabel("State of charge (%)")
    ax.set_ylabel("Open-circuit voltage (V)")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, color=GRID, lw=0.5)

    ax2 = fig.add_axes([0.56, 0.05, 0.43, 0.9])
    ax2.axis("off")
    d = schemdraw.Drawing(canvas=ax2)
    d.config(fontsize=8, unit=2.0, lw=1.1)
    src = d.add(elm.SourceV().up().label("OCV(SoC)", loc="bottom", ofst=0.15))
    d.add(elm.Line().up(0.5))
    d.add(elm.Resistor().right().label("$R_0$\n0.25 mΩ", ofst=0.1))
    # RC pair 1
    n1 = d.here
    d.push()
    d.add(elm.Line().up(0.8))
    d.add(elm.Resistor().right(2.2).label("$R_1$ 0.15 mΩ", ofst=0.1))
    d.add(elm.Line().down(0.8))
    n2 = d.here
    d.pop()
    d.add(elm.Line().down(0.8))
    d.add(elm.Capacitor().right(2.2).label("$C_1$ 20 kF", loc="bottom", ofst=0.1))
    d.add(elm.Line().up(0.8))
    d.add(elm.Line().right(0.4))
    d.push()
    d.add(elm.Line().up(0.8))
    d.add(elm.Resistor().right(2.2).label("$R_2$ 0.2 mΩ", ofst=0.1))
    d.add(elm.Line().down(0.8))
    d.pop()
    d.add(elm.Line().down(0.8))
    d.add(elm.Capacitor().right(2.2).label("$C_2$ 1.5 MF", loc="bottom", ofst=0.1))
    d.add(elm.Line().up(0.8))
    d.add(elm.Line().right(0.6))
    top = d.add(elm.Dot(open=True))
    d.move_from(src.start, dx=0, dy=0)
    d.add(elm.Line().at(src.start).tox(top.center))
    bot = d.add(elm.Dot(open=True))
    d.add(elm.Gap().up().at(bot.center).toy(top.center).label(("–", "$V$", "+"), fontsize=9))
    d.draw(show=False)
    ax2.text(0.62, 0.2, "τ$_1$ = R$_1$C$_1$ = 3 s\nτ$_2$ = R$_2$C$_2$ = 300 s",
             transform=ax2.transAxes, ha="center", va="center", fontsize=8)
    save(fig, CH, "fig-16-3-ocv-soc-and-ecm")


# --------------------------------------------------------- 16.4 Capacity fade
def _fade(N, n80, p, knee_at=None, knee_k=0.0):
    q = 100 - 20 * (N / n80) ** p
    if knee_at is not None:
        q = q - knee_k * np.clip(N - knee_at, 0, None) ** 2
    return q


def fig_16_4():
    fig, ax = new_fig(6.6, 4.2)
    N = np.linspace(0, 8000, 1601)
    curves = [
        ("LFP 25 °C", _fade(N, 6000, 0.85), COLORS[2], "-"),
        ("LFP 45 °C", _fade(N, 2500, 0.80), COLORS[2], "--"),
        ("NMC 25 °C", _fade(N, 2000, 0.75, knee_at=2400, knee_k=1.2e-5), COLORS[1], "-"),
        ("NMC 45 °C", _fade(N, 900, 0.70, knee_at=1000, knee_k=8e-5), COLORS[1], "--"),
    ]
    for lab, q, c, ls in curves:
        m = q >= 60
        ax.plot(N[m], q[m], color=c, ls=ls, label=lab)
    ax.axhline(80, color=INK, ls=":", lw=1.0)
    ax.text(2650, 80.4, "end of life, 80 % (EV and stationary)", ha="left", va="bottom", fontsize=8.5)
    ax.annotate("knee: fade\naccelerates", xy=(1250, 72), xytext=(1750, 69.5), fontsize=8.5,
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK, mutation_scale=8))
    for n80 in (900, 2000, 2500, 6000):
        ax.plot([n80], [80], "o", ms=3.5, color=INK, zorder=5)
    ax.set_xlim(0, 8000)
    ax.set_ylim(60, 100)
    ax.set_xlabel("Equivalent full cycles")
    ax.set_ylabel("Capacity retention (%)")
    ax.legend(loc="lower left", fontsize=8.5, ncol=2)
    ax.grid(True, color=GRID, lw=0.5)
    # inset: calendar fade at 50 % SoC, dQ = k sqrt(t), k(35 C) = 1.92 k(25 C)
    ins = ax.inset_axes([0.64, 0.74, 0.34, 0.23])
    t = np.linspace(0, 15, 300)
    k25 = 10 / np.sqrt(10)
    ins.plot(t, 100 - k25 * np.sqrt(t), color=COLORS[0], lw=1.4, label="25 °C")
    ins.plot(t, 100 - 1.92 * k25 * np.sqrt(t), color=COLORS[3], lw=1.4, label="35 °C")
    ins.set_xlim(0, 15)
    ins.set_ylim(75, 100)
    ins.set_xlabel("years at 50 % SoC (calendar fade)", fontsize=7, labelpad=1)
    ins.set_ylabel("retention (%)", fontsize=7, labelpad=1)
    ins.tick_params(labelsize=6.5, pad=1)
    ins.legend(fontsize=6.5, loc="lower left", handlelength=1.2)
    ins.set_facecolor("white")
    save(fig, CH, "fig-16-4-capacity-fade")


# ------------------------------------------------------ 16.5 Pumped hydro
def fig_16_5():
    fig = plt.figure(figsize=(6.8, 4.4))
    ax = fig.add_axes([0.09, 0.12, 0.60, 0.80])
    # terrain (x in km, elevation in m)
    tx = [-0.3, 0.0, 0.2, 1.2, 1.6, 2.2, 2.6, 3.0, 3.6, 4.2, 4.6, 6.0, 6.3]
    ty = [560, 640, 640, 640, 650, 640, 580, 420, 250, 150, 95, 95, 140]
    ax.fill_between(tx, ty, -20, color="#E9E1D3", zorder=1)
    ax.plot(tx, ty, color="#8C7B5E", lw=1.2, zorder=2)
    # upper reservoir: full level 600 m, 30 m drawdown
    ax.fill_between([0.0, 1.2], 600, 641, color="white", zorder=2.5)
    ax.add_patch(Polygon([[0.05, 600], [0.18, 570], [1.05, 570], [1.15, 600]], fc="#9CC9E8",
                         ec="none", zorder=3))
    ax.add_patch(Polygon([[0.0, 640], [0.05, 600], [0.18, 570], [1.05, 570], [1.15, 600], [1.2, 640]],
                         fc="none", ec="#8C7B5E", lw=1.0, zorder=3))
    ax.plot([0.05, 1.15], [600, 600], color=COLORS[0], lw=1.2, zorder=4)
    ax.text(0.0, 662, "upper reservoir, el. 600 m\n6 × 10$^6$ m$^3$ usable", ha="left", fontsize=7.5)
    ax.annotate("30 m drawdown", xy=(0.4, 585), xytext=(-0.2, 480), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK), zorder=6)
    ax.annotate("", xy=(0.4, 570), xytext=(0.4, 600),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=6), zorder=5)
    # lower reservoir
    ax.fill_between([4.6, 6.0], 80, 100, color="#9CC9E8", zorder=3)
    ax.plot([4.6, 6.0], [100, 100], color=COLORS[0], lw=1.2, zorder=4)
    ax.text(5.3, 108, "lower reservoir\nel. 100 m", ha="center", va="bottom", fontsize=7.5, zorder=5)
    # waterway: intake -> pressure tunnel -> penstock -> powerhouse -> tailrace
    wx = [1.05, 1.2, 2.55, 3.25, 3.55, 4.6]
    wy = [575, 560, 540, 95, 80, 88]
    ax.plot(wx[:3], wy[:3], color=COLORS[0], lw=3.0, zorder=4)
    ax.plot(wx[2:4], wy[2:4], color="#555555", lw=3.6, zorder=4)
    ax.plot(wx[3:], wy[3:], color=COLORS[0], lw=3.0, zorder=4)
    ax.plot([1.05, 1.05], [570, 590], color=INK, lw=1.5, zorder=5)
    ax.annotate("intake", xy=(1.1, 572), xytext=(1.15, 380), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK), zorder=6)
    ax.text(1.85, 522, "pressure tunnel 1.5 km", fontsize=7.5, ha="center", va="top", rotation=-2)
    ax.plot([2.45, 2.45], [541, 640], color=COLORS[0], lw=2.2, zorder=4)
    ax.text(2.55, 625, "surge shaft", ha="left", fontsize=7.5)
    ax.text(3.15, 215, "steel-lined\npenstock ⌀ 6 m", fontsize=7.5, ha="left", va="center")
    # powerhouse
    ax.add_patch(Rectangle((3.2, 62), 0.42, 45, fc="#F6D7B0", ec=INK, lw=1.0, zorder=5))
    ax.annotate("underground powerhouse, el. 80 m\n4 × 375 MW reversible Francis\npump-turbines + motor-generators",
                xy=(3.2, 85), xytext=(1.45, 120), fontsize=7.5, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK), zorder=6)
    ax.text(4.1, 62, "tailrace tunnel", fontsize=7.5, ha="center", va="top")
    # gross head
    ax.plot([1.15, 6.0], [600, 600], color="#999999", lw=0.6, ls="--", zorder=2.6)
    ax.annotate("", xy=(5.85, 600), xytext=(5.85, 100),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color=INK, mutation_scale=9), zorder=6)
    ax.text(5.75, 350, "gross head\n≈ 500 m", ha="right", va="center", fontsize=8, zorder=6)
    # flow directions, parallel to the penstock on its left
    ax.annotate("", xy=(2.62, 300), xytext=(2.38, 440),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLORS[0], mutation_scale=11), zorder=6)
    ax.annotate("", xy=(2.28, 420), xytext=(2.52, 280),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLORS[1], mutation_scale=11), zorder=6)
    ax.text(2.25, 445, "generating\n≈ 340 m$^3$/s", color=COLORS[0], fontsize=7.5, ha="right", va="center")
    ax.text(2.2, 300, "pumping", color=COLORS[1], fontsize=7.5, ha="right", va="center")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(0, 760)
    ax.set_xlabel("Horizontal distance (km)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title("vertical scale exaggerated", fontsize=8, loc="left", color="#666666")

    # electrical single-line diagram (side panel)
    ins = fig.add_axes([0.71, 0.12, 0.28, 0.80])
    ins.set_xlim(0, 4)
    ins.set_ylim(0, 11.4)
    ins.set_aspect("equal")
    ins.axis("off")
    ins.text(2.0, 11.2, "Electrical single line", ha="center", va="top", fontsize=8, fontweight="bold")
    x = 1.6
    ins.plot([0.6, 3.4], [10.0, 10.0], color=INK, lw=2.4)
    ins.text(3.45, 10.0, "400 kV", fontsize=7.5, va="center")
    ins.plot([x, x], [10.0, 1.4], color=INK, lw=1.0, zorder=1)
    for dy in (-0.27, 0.27):
        ins.add_patch(Circle((x, 8.9 + dy), 0.45, fc="none", ec=INK, lw=1.0, zorder=3))
    ins.add_patch(Rectangle((x - 0.47, 8.2), 0.94, 1.4, fc="white", ec="none", zorder=2))
    ins.text(x + 0.6, 8.9, "step-up\ntransformer", fontsize=7, va="center")
    # phase-reversal disconnector
    ins.add_patch(Rectangle((x - 0.1, 6.45), 0.2, 0.75, fc="white", ec="none", zorder=2))
    ins.plot([x, x - 0.35], [6.45, 7.1], color=INK, lw=1.1, zorder=3)
    ins.text(x + 0.35, 6.85, "phase-reversal\ndisconnector\n(pump mode)", fontsize=7, va="center")
    # generator circuit breaker
    ins.add_patch(Rectangle((x - 0.22, 4.9), 0.44, 0.44, fc="white", ec=INK, lw=1.0, zorder=3))
    ins.text(x + 0.35, 5.12, "generator CB", fontsize=7, va="center")
    # SFC branch
    ins.plot([x, 0.35, 0.35], [3.7, 3.7, 2.1], color=INK, lw=1.0)
    ins.add_patch(Rectangle((0.0, 1.0), 0.7, 1.1, fc="#EEF3F8", ec=INK, lw=1.0, zorder=3))
    ins.text(0.35, 1.55, "SFC", fontsize=7, ha="center", va="center", zorder=4)
    ins.text(0.0, 0.75, "static frequency\nconverter (start\nin pump mode)", fontsize=6.5, va="top")
    # motor-generator
    ins.add_patch(Circle((x, 1.4), 0.55, fc="white", ec=INK, lw=1.0, zorder=3))
    ins.text(x, 1.4, "M/G", fontsize=7, ha="center", va="center", zorder=4)
    ins.text(x + 0.7, 1.4, "375 MW\nmotor-\ngenerator", fontsize=7, va="center")
    save(fig, CH, "fig-16-5-pumped-hydro-layout")


# ------------------------------------------------------ 16.6 Hydrogen chain
def fig_16_6():
    fig, ax = schematic(6.8, 4.3, xlim=(0, 19.8), ylim=(0, 12.0))
    k = 0.06  # band thickness per kWh of energy per kg of hydrogen
    elec = "#9BC3E6"
    h2 = "#A8D8B9"
    heat = "#F2B8A0"

    def hband(x0, x1, yc, e, c):
        ax.add_patch(Rectangle((x0, yc - e * k / 2), x1 - x0, e * k, fc=c, ec="none", zorder=2))

    def vdown(xc, y0, y1, e, c):
        w = e * k
        ax.add_patch(Polygon([[xc - w / 2, y0], [xc + w / 2, y0], [xc + w / 2, y1 + 0.35],
                              [xc + w / 2 + 0.2, y1 + 0.35], [xc, y1], [xc - w / 2 - 0.2, y1 + 0.35],
                              [xc - w / 2, y1 + 0.35]], fc=c, ec="none", zorder=2))

    def harrow(x0, x1, yc, e, c):
        w = e * k
        ax.add_patch(Polygon([[x0, yc - w / 2], [x1 - 0.4, yc - w / 2], [x1 - 0.4, yc - w / 2 - 0.2],
                              [x1, yc], [x1 - 0.4, yc + w / 2 + 0.2], [x1 - 0.4, yc + w / 2],
                              [x0, yc + w / 2]], fc=c, ec="none", zorder=2))

    yc = 6.0
    box(ax, 0.1, 4.0, 1.9, 4.0, "AC grid\ninput\n54.5 kWh", fc="#DCEAF7", fontsize=8)
    hband(2.0, 2.6, yc, 52, elec)
    ax.text(2.3, yc + 1.65, "52", fontsize=7.5, ha="center", va="bottom")
    # electricity to the compressor (2.5 kWh)
    w = 2.5 * k
    xc = 8.6
    ax.add_patch(Polygon([[1.6, 8.0], [1.6, 10.2], [xc + w / 2, 10.2], [xc + w / 2, 7.4],
                          [xc - w / 2, 7.4], [xc - w / 2, 10.2 - w], [1.6 + w, 10.2 - w],
                          [1.6 + w, 8.0]], fc="#4F8FCB", ec="none", zorder=2))
    ax.text(5.0, 10.35, "2.5 kWh electricity to compressor", fontsize=7.5, ha="center", va="bottom")
    box(ax, 2.6, 3.9, 2.6, 4.2, "Rectifier +\nPEM\nelectrolyser\n52 kWh/kg\nη 64 % (LHV)\n30 bar out",
        fc="#EEF3F8", fontsize=7)
    vdown(3.9, 3.9, 1.0, 18.7, heat)
    ax.text(4.65, 1.7, "electrolyser heat\n18.7 kWh", fontsize=7.5, ha="left", va="center")
    hband(5.2, 7.4, yc, 33.3, h2)
    ax.text(6.3, yc + 1.1, "H$_2$, 1 kg", fontsize=8, ha="center", va="bottom")
    ax.text(6.3, yc, "LHV 33.3\nHHV 39.4\nkWh/kg", fontsize=7, ha="center", va="center")
    box(ax, 7.4, 4.6, 2.4, 2.8, "Compressor\n30 → 180 bar\n2.5 kWh/kg", fc="#EEF3F8", fontsize=7)
    vdown(xc, 4.6, 3.0, 2.5, heat)
    ax.text(xc + 0.3, 3.3, "compression\nheat 2.5 kWh", fontsize=7.5, ha="left", va="center")
    hband(9.8, 10.2, yc, 33.3, h2)
    box(ax, 10.2, 2.5, 2.5, 7.0, "Salt cavern\n500 000 m$^3$\n60–180 bar\nworking gas\n≈ 4000 t\n(≈ 132 GWh\nLHV)",
        fc="#E8F1E4", fontsize=7)
    yfc, ycc = 8.3, 3.7
    hband(12.7, 13.3, yfc, 33.3, h2)
    hband(12.7, 13.3, ycc, 33.3, h2)
    ax.text(13.0, 9.9, "either", fontsize=7.5, ha="center", style="italic")
    ax.text(13.0, 5.95, "or", fontsize=7.5, ha="center", style="italic")
    box(ax, 13.3, yfc - 1.25, 2.8, 2.5, "PEM fuel cell\nη 50 % (LHV)", fc="#EEF3F8", fontsize=7.5)
    box(ax, 13.3, ycc - 1.25, 2.8, 2.5, "H$_2$-fired\ncombined cycle\nη 60 % (LHV)", fc="#EEF3F8",
        fontsize=7.5)
    harrow(16.1, 17.7, yfc, 16.7, elec)
    harrow(16.1, 17.7, ycc, 20.0, elec)
    ax.text(16.9, yfc + 0.85, "16.7 kWh", fontsize=7.5, ha="center", va="bottom")
    ax.text(16.9, ycc + 0.95, "20.0 kWh", fontsize=7.5, ha="center", va="bottom")
    ax.text(17.85, yfc, "round\ntrip\n31 %", fontsize=8, ha="left", va="center", fontweight="bold")
    ax.text(17.85, ycc, "round\ntrip\n37 %", fontsize=8, ha="left", va="center", fontweight="bold")
    vdown(14.7, yfc - 1.25, 5.5, 16.6, heat)
    ax.text(15.35, 6.1, "conversion heat\n16.6 kWh", fontsize=7.5, ha="left", va="center")
    vdown(14.7, ycc - 1.25, 0.5, 13.3, heat)
    ax.text(15.3, 1.2, "conversion heat\n13.3 kWh", fontsize=7.5, ha="left", va="center")
    ax.text(0.1, 0.4, "band widths ∝ energy per kg H$_2$", fontsize=7.5, color="#555555")
    save(fig, CH, "fig-16-6-hydrogen-chain")


if __name__ == "__main__":
    fig_16_1()
    fig_16_2()
    fig_16_3()
    fig_16_4()
    fig_16_5()
    fig_16_6()
