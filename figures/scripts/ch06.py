"""Figures for Chapter 6 — Induction Machines.

Run from the repository root:  python figures/scripts/ch06.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle, Ellipse, FancyArrowPatch  # noqa: E402
from scipy.interpolate import PchipInterpolator  # noqa: E402

from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

BLUE, ORANGE, GREEN, PINK, YELLOW, SKY = COLORS[:6]
STEEL = "#B9BEC4"
STEEL2 = "#D5D9DD"
ALU = "#9EA7B0"
COPPER = "#E3A869"
PHASE = {"A": BLUE, "B": ORANGE, "C": GREEN}

# 37 kW, 400 V, 50 Hz, 4-pole motor of Sections 6.4-6.6 (per phase, star)
V1 = 400 / np.sqrt(3)
R1, X1, R2, X2, XM = 0.070, 0.28, 0.060, 0.32, 11.0
NS = 1500.0
WS = 2 * np.pi * 50 / 2


def _farrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ms=10, z=4):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms, color=color,
                                 lw=lw, shrinkA=0, shrinkB=0, zorder=z))


def _pol(r, deg):
    a = np.radians(deg)
    return r * np.cos(a), r * np.sin(a)


def motor(s, r2=R2, x2=X2, v=V1):
    """Stator current (complex, A) and electromagnetic torque (N m) from the equivalent circuit."""
    s = np.asarray(s, dtype=float)
    Zr = r2 / s + 1j * x2
    Zp = 1j * XM * Zr / (1j * XM + Zr)
    I1 = v / (R1 + 1j * X1 + Zp)
    I2 = I1 * Zp / Zr
    T = 3 * np.abs(I2) ** 2 * r2 / s / WS
    return I1, T


# ---------------------------------------------------------------------------
# Figure 6.1
# ---------------------------------------------------------------------------
def _cross_section(ax):
    Ro, Rb, Rr, Rsh = 190, 120, 114, 30           # gap 0.6 mm drawn as 6 mm
    ax.add_patch(Circle((0, 0), Ro, fc=STEEL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), Rb, fc="white", ec=INK, lw=0.8))
    # 48 stator slots, 4 poles, q = 4: A+ C- B+ A- C+ B- per pair of poles
    seq = ["A+", "C-", "B+", "A-", "C+", "B-"]
    for k in range(48):
        ang = 7.5 * k + 3.75
        ph = seq[(k // 4) % 6]
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        hw, r0, r1 = 4.2, Rb, Rb + 26
        pts = [(r0 * c - hw * s, r0 * s + hw * c), (r1 * c - hw * s, r1 * s + hw * c),
               (r1 * c + hw * s, r1 * s - hw * c), (r0 * c + hw * s, r0 * s - hw * c)]
        ax.add_patch(Polygon(pts, closed=True, fc=PHASE[ph[0]], ec=INK, lw=0.4, alpha=0.9))
    # rotor with 40 closed bars
    ax.add_patch(Circle((0, 0), Rr, fc=STEEL2, ec=INK, lw=0.8))
    for k in range(40):
        x, y = _pol(Rr - 9, 9 * k)
        ax.add_patch(Circle((x, y), 4.2, fc=ALU, ec=INK, lw=0.4))
    ax.add_patch(Circle((0, 0), Rsh, fc="#888888", ec=INK, lw=0.6))
    # four-pole flux: loops between adjacent pole axes (0, 90, 180, 270 deg)
    for a0 in (0, 90, 180, 270):
        for da, rr, ry in [(10, 70, 170), (25, 88, 160)]:
            a_n, a_s = a0 + da, a0 + 90 - da
            pts = [_pol(r, a_n) for r in np.linspace(ry, rr, 8)]
            pts += [_pol(rr, a) for a in np.linspace(a_n, a_s, 30)]
            pts += [_pol(r, a_s) for r in np.linspace(rr, ry, 8)]
            pts += [_pol(ry, a) for a in np.linspace(a_s, a_n, 30)]
            pts = np.array(pts)
            ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=0.7, ls=(0, (3, 2)), zorder=5)
    for a, lab in zip((0, 90, 180, 270), ("N", "S", "N", "S")):
        x, y = _pol(Ro + 14, a)
        ax.text(x, y, lab, ha="center", va="center", fontsize=9, fontweight="bold")
    fs = 8
    kw = dict(fontsize=fs, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("stator core", xy=_pol(170, 125), xytext=(-255, 205), ha="left", **kw)
    ax.annotate("stator winding\n(48 slots)", xy=_pol(Rb + 14, 52), xytext=(150, 215), ha="left", **kw)
    ax.annotate("air gap\n(0.6 mm, enlarged)", xy=_pol(117, 205), xytext=(-260, -215), ha="left", **kw)
    ax.annotate("rotor bar\n(40 slots)", xy=_pol(Rr - 9, 297), xytext=(110, -225), ha="left", **kw)
    ax.annotate("shaft", xy=(0, -20), xytext=(-50, -245), ha="center", **kw)
    for ph, c, yy in [("phase A", BLUE, -130), ("phase B", ORANGE, -150), ("phase C", GREEN, -170)]:
        ax.add_patch(Rectangle((205, yy - 5), 12, 10, fc=c, ec=INK, lw=0.4))
        ax.text(222, yy, ph, fontsize=7.5, va="center")
    ax.text(205, -110, "flux (dashed)", fontsize=7.5, va="center")
    ax.set_xlim(-265, 300)
    ax.set_ylim(-265, 250)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a) Four-pole cage motor, 380 mm o.d., 240 mm bore", fontsize=9)


def _cage(ax):
    L, a, b = 3.0, 0.32, 1.0                       # length, ring half-width (perspective), radius
    nbar = 14
    skew = 7.5 * 2.5                               # one stator slot pitch (7.5 deg), drawn x2.5 for visibility
    for k in range(nbar):
        t0 = np.radians(360 / nbar * k + 6)
        t1 = t0 + np.radians(skew)
        x0, y0 = a * np.cos(t0), b * np.sin(t0)
        x1, y1 = L + a * np.cos(t1), b * np.sin(t1)
        if np.cos(t0) > 0:
            ax.plot([x0, x1], [y0, y1], color=INK, lw=3.4, zorder=3, solid_capstyle="butt")
            ax.plot([x0, x1], [y0, y1], color=ALU, lw=2.4, zorder=3, solid_capstyle="butt")
        else:
            ax.plot([x0, x1], [y0, y1], color="#AAAAAA", lw=0.8, ls=(0, (3, 2)), zorder=1)
    for x0 in (0, L):
        ax.add_patch(Ellipse((x0, 0), 2 * a + 0.12, 2 * b + 0.12, fill=False, ec=ALU, lw=6, zorder=4))
        ax.add_patch(Ellipse((x0, 0), 2 * a + 0.12, 2 * b + 0.12, fill=False, ec=INK, lw=0.6, zorder=5))
    kw = dict(fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("end ring", xy=(L + 0.05, 1.05), xytext=(L + 0.55, 1.35), **kw)
    ax.annotate("end ring", xy=(-0.05, -1.05), xytext=(-0.65, -1.45), **kw)
    ax.annotate("skewed aluminium bar", xy=(1.5, 0.98), xytext=(0.15, 1.45), **kw)
    ax.text(L / 2, -1.45, "skew = one stator slot pitch\n(drawn enlarged)", fontsize=7, ha="center", va="top")
    ax.set_xlim(-0.8, L + 1.5)
    ax.set_ylim(-1.95, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(b) Squirrel cage", fontsize=9)


def _wound(ax):
    # rotor body and shaft (side view)
    ax.add_patch(Rectangle((0, -0.9), 2.2, 1.8, fc=STEEL2, ec=INK, lw=0.8))
    for k in range(9):
        ax.plot([0.15 + 0.24 * k] * 2, [-0.9, 0.9], color="#999999", lw=0.4)
    ax.add_patch(Rectangle((-0.6, -0.15), 4.6, 0.3, fc="#888888", ec=INK, lw=0.6, zorder=0))
    xs = [2.7, 3.1, 3.5]
    for k, x in enumerate(xs):
        ax.add_patch(Rectangle((x - 0.08, -0.45), 0.16, 0.9, fc=COPPER, ec=INK, lw=0.6, zorder=2))
        ax.add_patch(Rectangle((x - 0.07, 0.47), 0.14, 0.25, fc="#444444", ec=INK, lw=0.5, zorder=2))
        # rotor winding leads along the shaft
        ax.plot([2.2, x], [0.25 - 0.12 * k, 0.25 - 0.12 * k], color=COPPER, lw=0.8, zorder=1)
    # brushes to star-connected resistors
    ytop = 1.15
    rx = [4.6, 5.1, 5.6]
    for x, xr in zip(xs, rx):
        ax.plot([x, x, xr, xr], [0.72, ytop + 0.05 * (xr - 4.6) * 0, ytop, 0.95], color=INK, lw=0.8)
        # resistor zigzag (vertical) with variable arrow
        zz = np.linspace(0.95, 0.15, 9)
        xz = xr + np.array([0, 0.08, -0.08, 0.08, -0.08, 0.08, -0.08, 0.08, 0])
        ax.plot(xz, zz, color=INK, lw=0.9)
        _farrow(ax, xr - 0.22, 0.20, xr + 0.22, 0.85, color=INK, lw=0.7, ms=6)
        ax.plot([xr, xr], [0.15, -0.15], color=INK, lw=0.8)
    ax.plot([rx[0], rx[-1]], [-0.15, -0.15], color=INK, lw=0.8)
    ax.plot(5.1, -0.15, "o", color=INK, ms=3)
    kw = dict(fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("slip rings", xy=(3.1, -0.45), xytext=(2.6, -1.25), **kw)
    ax.annotate("brush", xy=(2.7, 0.62), xytext=(1.8, 1.35), **kw)
    ax.annotate("external resistance\n(star-connected)", xy=(5.1, -0.15), xytext=(4.3, -1.25), **kw)
    ax.text(1.1, -1.1, "wound rotor", fontsize=8, ha="center", va="top")
    ax.set_xlim(-0.7, 6.4)
    ax.set_ylim(-1.75, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(c) Wound rotor with slip rings", fontsize=9)


def fig_6_1():
    """Cage induction motor cross-section, squirrel cage and wound rotor."""
    fig = plt.figure(figsize=(6.8, 4.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1.0])
    ax_a = fig.add_subplot(gs[:, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 1])
    _cross_section(ax_a)
    _cage(ax_b)
    _wound(ax_c)
    fig.tight_layout(w_pad=0.2, h_pad=0.4)
    return save(fig, "06", "fig-6-1-cage-and-wound-rotor")


# ---------------------------------------------------------------------------
# Figure 6.2
# ---------------------------------------------------------------------------
def _ind_circuit(ax):
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=9.5, lw=1.1)
        yt, yb = 3.4, 0.0
        d.add(elm.SourceSin().endpoints((0, yb), (0, yt)).label("$V_1$\n230.9 V", loc="top"))
        d.add(elm.Line().endpoints((0, yt), (1.0, yt)))
        d.add(elm.Resistor().endpoints((1.0, yt), (3.0, yt)).label("$R_1$", loc="top").label("0.070 Ω", loc="bot"))
        d.add(elm.Inductor2(loops=3).endpoints((3.0, yt), (5.0, yt)).label("$jX_1$", loc="top")
              .label("j0.28 Ω", loc="bot"))
        d.add(elm.Line().endpoints((5.0, yt), (8.4, yt)))
        for x in (5.8, 7.3):
            d.add(elm.Dot().at((x, yt)))
            d.add(elm.Dot().at((x, yb)))
        d.add(elm.Line().endpoints((5.8, yt), (5.8, yt - 0.7)))
        d.add(elm.Inductor2(loops=3).endpoints((5.8, yt - 0.7), (5.8, yb)).label("$jX_m$\nj11.0 Ω", loc="top"))
        d.add(elm.Resistor().endpoints((7.3, yt), (7.3, yb)).label("$R_c$", loc="bot").linestyle("--"))
        d.add(elm.Inductor2(loops=3).endpoints((8.4, yt), (10.4, yt)).label("$jX_2$", loc="top")
              .label("j0.32 Ω", loc="bot"))
        d.add(elm.Resistor().endpoints((10.4, yt), (12.4, yt)).label("$R_2$", loc="top").label("0.060 Ω", loc="bot"))
        d.add(elm.Line().endpoints((12.4, yt), (13.6, yt)))
        d.add(elm.ResistorVar().endpoints((13.6, yt), (13.6, yb)).label(r"$R_2\,\dfrac{1-s}{s}$", loc="bot")
              .label("mechanical\nload", loc="top"))
        d.add(elm.Line().endpoints((13.6, yb), (0, yb)))
        d.draw(show=False)
    # current reference arrows on the wires
    for (x0, y0, x1, y1, lab, dx, dy) in [(0.25, yt, 0.85, yt, "$I_1$", 0.0, 0.18),
                                         (5.8, yt - 0.05, 5.8, yt - 0.62, "$I_m$", -0.12, 0.0),
                                         (12.7, yt, 13.3, yt, "$I_2$", 0.0, 0.18)]:
        _farrow(ax, x0, y0, x1, y1, color=INK, lw=1.2, ms=9, z=6)
        ax.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, lab, ha="right" if dx < 0 else "center",
                va="center" if dx < 0 else "bottom", fontsize=9.5)
    ax.set_aspect("equal")
    ax.axis("off")


def _sankey(ax):
    P = dict(inp=40.24, cu1=0.86, core=0.70, ag=38.68, cu2=0.63, mech=38.06, fw=0.30, out=37.76)
    H = 1.0 / P["inp"]           # height per kW of the main stream
    K = 5.0                      # loss branches drawn 5x wider
    x = [0.0, 1.8, 3.4, 5.0, 6.8, 8.8, 10.3]
    y_top = 0.5
    # main stream: piecewise rectangles whose height steps down at each loss tap (top edge fixed)
    stream = [(x[0], x[1], P["inp"]), (x[1], x[2], P["inp"] - P["cu1"]), (x[2], x[4], P["ag"]),
              (x[4], x[5], P["mech"]), (x[5], x[6], P["out"])]
    outline = [(x[0], y_top)]
    for x0, x1, p in stream:
        outline.append((x0, y_top - p * H) if x0 == x[0] else (x0, y_top - p * H))
    pts = [(x[0], y_top), (x[6], y_top)]
    for x0, x1, p in reversed(stream):
        pts += [(x1, y_top - p * H), (x0, y_top - p * H)]
    ax.add_patch(Polygon(pts, closed=True, fc="#CFE0F0", ec=BLUE, lw=0.8))
    ax.plot([x[0], x[6]], [y_top, y_top], color=BLUE, lw=1.0)
    ax.add_patch(Polygon([(x[6], y_top + 0.08), (x[6] + 0.6, y_top - P["out"] * H / 2),
                          (x[6], y_top - P["out"] * H - 0.08)], closed=True, fc="#CFE0F0", ec=BLUE, lw=1.0))
    # loss branches
    losses = [(x[1] - 0.25, P["cu1"], "stator copper\n0.86 kW"), (x[2] - 0.25, P["core"], "core\n0.70 kW"),
              (x[4] - 0.25, P["cu2"], "rotor copper\n$sP_{ag}$ = 0.63 kW"),
              (x[5] - 0.25, P["fw"], "friction and\nwindage 0.30 kW")]
    ybot = y_top - P["inp"] * H
    for xc, p, lab in losses:
        w = K * p * H
        ax.add_patch(Rectangle((xc - w / 2, ybot - 0.45), w, 0.45 + 0.02, fc=ORANGE, ec="none", alpha=0.8))
        ax.add_patch(Polygon([(xc - w / 2 - 0.08, ybot - 0.45), (xc + w / 2 + 0.08, ybot - 0.45),
                              (xc, ybot - 0.65)], closed=True, fc=ORANGE, ec="none", alpha=0.8))
        ax.text(xc, ybot - 0.72, lab, ha="center", va="top", fontsize=8)
    # stage labels
    labs = [(x[0] + 0.05, "input\n40.24 kW"), (5.1, "air-gap power\n$P_{ag}$ = 38.68 kW"),
            (7.8, "mechanical\n38.06 kW"), (x[6] - 0.05, "output\n37.76 kW")]
    for xx, t in labs:
        ax.text(xx, y_top + 0.08, t, ha="left" if xx < 1 else ("right" if xx > 10 else "center"),
                va="bottom", fontsize=8.5)
    for xx in (x[3] - 0.95 + 0.0, x[4] + 0.95):
        pass
    ax.plot([5.1] * 2, [y_top, y_top - P["ag"] * H], color=INK, lw=0.6, ls=":")
    ax.plot([7.8] * 2, [y_top, y_top - P["mech"] * H], color=INK, lw=0.6, ls=":")
    ax.text(6.0, 0.0, "s = 0.0162, 1476 rpm, η = 93.8 %", ha="center", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(-0.2, 11.2)
    ax.set_ylim(-1.95, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-0.1, -1.93, "loss branches drawn 5× wider than the main stream", fontsize=7, ha="left", va="bottom",
            color="#555555")


def fig_6_2():
    """Per-phase equivalent circuit and power flow of the 37 kW motor."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 5.0), gridspec_kw=dict(height_ratios=[1.05, 1.0]))
    _ind_circuit(a1)
    a1.set_title("(a) Per-phase equivalent circuit (values for the 37 kW, 400 V motor)", fontsize=9.5, loc="left", pad=10)
    _sankey(a2)
    a2.set_title("(b) Power flow at s = 0.0162", fontsize=9.5, loc="left")
    fig.tight_layout(h_pad=0.6)
    return save(fig, "06", "fig-6-2-equivalent-circuit-and-power-flow")


# ---------------------------------------------------------------------------
# Figure 6.3
# ---------------------------------------------------------------------------
def fig_6_3():
    """Torque and stator current against speed, constant-parameter circuit, s = 2 ... -1."""
    n = np.linspace(-1500, 3000, 2251)
    n = n[np.abs(n - NS) > 0.5]
    s = (NS - n) / NS
    I1, T = motor(s)
    _, T_ext = motor(s, r2=R2 + 0.537)
    fig, ax = new_fig(6.6, 4.4)
    ax.axvspan(-1500, 0, color=PINK, alpha=0.08, lw=0)
    ax.axvspan(0, NS, color=GREEN, alpha=0.06, lw=0)
    ax.axvspan(NS, 3000, color=BLUE, alpha=0.06, lw=0)
    ax.text(-750, 760, "braking (s > 1)", ha="center", fontsize=8.5, color=PINK)
    ax.text(750, 760, "motoring (0 < s < 1)", ha="center", fontsize=8.5, color=GREEN)
    ax.text(2250, 760, "generating (s < 0)", ha="center", fontsize=8.5, color=BLUE)
    ax.axhline(0, color=INK, lw=0.6)
    ax.plot(n, np.where(np.abs(T) <= 800, T, np.nan), color=BLUE, lw=2.0, label="torque")
    ax.plot(n, np.where(np.abs(T_ext) <= 800, T_ext, np.nan), color=BLUE, lw=1.3, ls="--",
            label="torque, + 0.537 Ω rotor resistance")
    ax.set_xlim(-1500, 3000)
    ax.set_ylim(-800, 800)
    ax.set_xlabel("Speed (rpm)")
    ax.set_ylabel("Torque (N·m)", color=BLUE)
    # key points
    s_m = 0.1005
    _, Tm = motor(s_m)
    ax.plot(NS * (1 - s_m), Tm, "o", color=BLUE, ms=5)
    ax.annotate(f"$T_{{max}}$ = {float(Tm):.0f} N·m\n{NS * (1 - s_m):.0f} rpm (s = 0.100)", xy=(NS * (1 - s_m), Tm),
                xytext=(1720, 640), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    _, Tr = motor(0.0162)
    ax.plot(1476, Tr, "s", color=INK, ms=5, zorder=6)
    ax.annotate(f"s = 0.0162, 1476 rpm:\n{float(Tr):.0f} N·m, 64 A", xy=(1476, Tr), xytext=(1750, 130), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    _, Ts = motor(1.0)
    ax.plot(0, Ts, "o", color=BLUE, ms=5)
    ax.annotate(f"start: {float(Ts):.0f} N·m", xy=(0, Ts), xytext=(-1000, 235), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    sg = np.linspace(-0.9, -0.01, 5000)
    _, Tg = motor(sg)
    kg = np.argmin(Tg)
    ax.annotate(f"generating pull-out\n{Tg[kg]:.0f} N·m at {NS * (1 - sg[kg]):.0f} rpm\n(off scale)",
                xy=(NS * (1 - sg[kg]), -790), xytext=(2990, -785), fontsize=7.5, ha="right", va="bottom",
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.5),
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(n, np.abs(I1), color=ORANGE, lw=1.6, label="stator current")
    ax2.set_ylim(0, 450)
    ax2.set_ylabel("Stator current (A)", color=ORANGE)
    ax2.annotate(f"{abs(motor(1.0)[0]):.0f} A at standstill", xy=(0, abs(motor(1.0)[0])), xytext=(-1400, 345),
                 fontsize=8, color=ORANGE, arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    ax2.annotate(f"{abs(motor(1e-6)[0]):.0f} A\nat $n_s$", xy=(NS, abs(motor(1e-6)[0])), xytext=(1150, 60),
                 fontsize=8, color=ORANGE, ha="right", arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    # top axis: slip
    axt = ax.secondary_xaxis("top", functions=(lambda x: (NS - x) / NS, lambda s_: NS * (1 - s_)))
    axt.set_xticks([2, 1.5, 1, 0.5, 0, -0.5, -1])
    axt.set_xlabel("Slip s")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=8, bbox_to_anchor=(0.0, 0.02))
    return save(fig, "06", "fig-6-3-torque-speed-curve")


# ---------------------------------------------------------------------------
# Figure 6.4
# ---------------------------------------------------------------------------
def _kloss_var(s, tmax, sm0, k):
    """Breakdown-torque form with slip-dependent rotor resistance: s_m(s) = sm0 (1 + k s)."""
    sm = sm0 * (1 + k * s)
    return 2 * tmax / (s / sm + sm / s)


def _class_curves():
    s = np.linspace(1e-4, 1, 2000)
    out = {}
    # NEMA A / IEC NE: LRT 180 %, peak 300 % at s = 0.15
    out["A"] = _kloss_var(s, 300, 0.1177, 1.83)
    # NEMA D: LRT 290 %, monotonic, rated torque at s = 0.08
    out["D"] = _kloss_var(s, 294.8, 0.3857, 2.109)

    def blend(peak, s_pk, sm0, k, low_pts):
        hi = s <= s_pk + 0.03
        sk = np.linspace(1e-4, s_pk + 0.03, 40)
        tk = _kloss_var(sk, peak, sm0, k)
        ps, pt = zip(*sorted(low_pts))
        xs = np.concatenate([sk, ps])
        ys = np.concatenate([tk, pt])
        f = PchipInterpolator(xs, ys)
        return np.where(hi, _kloss_var(s, peak, sm0, k), f(s))

    # NEMA B / IEC N: LRT 180 %, pull-up 140 %, peak 250 % at s = 0.18, rated slip 2 %
    out["B"] = blend(250, 0.18, 0.0857, 6.17, [(0.32, 205), (0.45, 158), (0.60, 141), (0.75, 147), (0.9, 165),
                                               (1.0, 180)])
    # NEMA C / IEC H: LRT 240 %, pull-up about 185 %, peak 200 % at s = 0.25, rated slip 2.5 %
    sm_c = 0.25
    # s_m(0.025) for 100 % torque at 200 % peak: s/sm = 0.2679 -> sm(0.025) = 0.0933
    k_c = (sm_c / 0.0933 - 1) / (0.25 - 0.025 * sm_c / 0.0933)
    sm0_c = sm_c / (1 + 0.25 * k_c)
    out["C"] = blend(200, 0.25, sm0_c, k_c, [(0.36, 193), (0.5, 186), (0.65, 190), (0.8, 208), (0.9, 224),
                                             (1.0, 240)])
    return s, out


def fig_6_4():
    """Design-class torque-speed curves with rotor-slot inset."""
    s, cur = _class_curves()
    sp = 100 * (1 - s)
    fig, ax = new_fig(6.6, 4.4)
    styles = [("A", "NEMA A / IEC NE", BLUE), ("B", "NEMA B / IEC N", GREEN), ("C", "NEMA C / IEC H", ORANGE),
              ("D", "NEMA D", PINK)]
    for key, lab, c in styles:
        ax.plot(sp, cur[key], color=c, lw=1.9, label=lab)
    ax.axhline(100, color="#777777", ls=":", lw=1.0)
    ax.text(52, 103, "rated torque", fontsize=8, color="#555555", va="bottom")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 320)
    ax.set_xlabel("Speed (% of synchronous)")
    ax.set_ylabel("Torque (% of rated)")
    ax.legend(loc="lower left", fontsize=8.5, bbox_to_anchor=(0.50, 0.03))
    ax.grid(True, lw=0.5)
    # inset: rotor slots to scale (25 mm deep)
    ins = ax.inset_axes([0.02, 0.02, 0.46, 0.27])
    ins.set_aspect("equal")
    ins.axis("off")
    ins.set_xlim(-2, 66)
    ins.set_ylim(-28, 8)
    gap_x = 17
    for k, (lab, c) in enumerate([("A", BLUE), ("B", GREEN), ("C", ORANGE), ("D", PINK)]):
        x0 = 6 + k * gap_x
        # slot outline 25 mm deep, opening at the rotor surface (y = 0)
        ins.plot([x0 - 9, x0 + 9], [0, 0], color=INK, lw=0.8)
        ins.add_patch(Rectangle((x0 - 9, -27), 18, 27, fc=STEEL2, ec="none", zorder=0))
        if lab == "A":
            ins.add_patch(Circle((x0, -6.5), 5.5, fc=ALU, ec=c, lw=1.2))
        elif lab == "B":
            ins.add_patch(Rectangle((x0 - 2.0, -25), 4.0, 24, fc=ALU, ec=c, lw=1.2))
        elif lab == "C":
            ins.add_patch(Circle((x0, -4.0), 2.6, fc=ALU, ec=c, lw=1.2))
            ins.add_patch(Rectangle((x0 - 0.5, -11), 1.0, 4.4, fc="white", ec=INK, lw=0.5))
            ins.add_patch(Rectangle((x0 - 3.8, -25), 7.6, 14, fc=ALU, ec=c, lw=1.2))
        else:
            ins.add_patch(Circle((x0, -4.5), 3.0, fc="#C9A66B", ec=c, lw=1.2))
        ins.text(x0, 1.5, lab, ha="center", va="bottom", fontsize=8.5, color=c, fontweight="bold")
    ins.annotate("", xy=(-1, 0), xytext=(-1, -25), arrowprops=dict(arrowstyle="<|-|>", lw=0.6, color=INK,
                                                                   mutation_scale=6))
    ins.text(-1.8, -12.5, "25 mm", rotation=90, fontsize=7, ha="right", va="center")
    ins.text(64, -26, "rotor bars to scale", fontsize=7, ha="right", va="bottom", color="#444444")
    return save(fig, "06", "fig-6-4-design-classes-and-rotor-bars")


# ---------------------------------------------------------------------------
# Figure 6.5
# ---------------------------------------------------------------------------
def _deep_bar(s):
    """Rotor parameters varying linearly with slip from running (s = 0) to standstill (s = 1) values."""
    return R2 + (0.156 - R2) * s, X2 + (0.224 - X2) * s


def fig_6_5():
    """Starting methods for the 37 kW motor: line current and torque against speed, pump load."""
    n = np.linspace(0, 1490, 1000)
    s = (NS - n) / NS
    r2, x2 = _deep_bar(s)
    I, T = motor(s, r2, x2)
    I = np.abs(I)
    TL = 244 * (n / 1476) ** 2
    # star-delta: one third until 1300 rpm, then delta (open transition)
    n_sd = 1300
    sd = n < n_sd
    # autotransformer 65 % tap until 1400 rpm
    n_at = 1400
    at = n < n_at
    # soft starter: 60 % voltage ramped to 100 % at 1200 rpm
    v_ss = np.clip(0.6 + 0.4 * n / 1200, 0, 1)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.4), sharex=True)
    a1.plot(n, I, color=INK, lw=1.8, label="direct-on-line")
    a1.plot(n[sd], I[sd] / 3, color=BLUE, lw=1.6, label="star–delta")
    k = np.argmin(abs(n - n_sd))
    a1.plot([n_sd, n_sd], [I[k] / 3, 350], color=BLUE, lw=1.2, ls="--")
    a1.plot([n_sd, n_sd + 15], [350, I[k]], color=BLUE, lw=1.2, ls="--")
    a1.text(n_sd - 15, 355, "transition\ntransient ≈ 350 A", fontsize=7.5, color=BLUE, ha="right", va="bottom")
    a1.plot(n[at], 0.65 ** 2 * I[at], color=GREEN, lw=1.6, label="autotransformer 65 %")
    a1.plot(n, v_ss * I, color=ORANGE, lw=1.6, label="soft starter (60 % → 100 %)")
    a1.text(15, I[0] + 5, f"{I[0]:.0f} A", fontsize=7.5, va="bottom")
    a1.text(15, I[0] / 3 - 5, f"{I[0] / 3:.0f} A", fontsize=7.5, va="top", color=BLUE)
    a1.text(15, 0.4225 * I[0] + 4, f"{0.4225 * I[0]:.0f} A", fontsize=7.5, va="bottom", color=GREEN)
    a1.text(15, 0.6 * I[0] + 4, f"{0.6 * I[0]:.0f} A", fontsize=7.5, va="bottom", color=ORANGE)
    a1.set_ylim(0, 450)
    a1.set_ylabel("Line current (A)")
    a1.legend(loc="lower left", fontsize=8, ncol=2)
    a1.grid(True, lw=0.5)
    a1.set_title("(a) Line current", fontsize=9.5, loc="left")
    a2.fill_between(n, TL, T, where=T > TL, color=INK, alpha=0.07, lw=0)
    a2.plot(n, T, color=INK, lw=1.8, label="direct-on-line")
    a2.plot(n[sd], T[sd] / 3, color=BLUE, lw=1.6, label="star–delta (1/3)")
    a2.plot(n[at], 0.4225 * T[at], color=GREEN, lw=1.6, label="autotransformer (0.42)")
    a2.plot(n, v_ss ** 2 * T, color=ORANGE, lw=1.6, label="soft starter")
    a2.plot(n, TL, color=PINK, lw=1.8, ls="--", label="pump load ∝ $n^2$")
    a2.text(15, T[0] + 8, f"{T[0]:.0f} N·m", fontsize=7.5, va="bottom")
    kmax = np.argmax(T)
    a2.annotate(f"peak {T[kmax]:.0f} N·m", xy=(n[kmax], T[kmax]), xytext=(900, 760), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    a2.text(650, 118, "accelerating torque (DOL)", fontsize=7.5, ha="center", va="center", color="#555555")
    a2.text(1478, 18, "load 244 N·m at 1476 rpm", fontsize=7.5, color=PINK, ha="right", va="bottom")
    a2.set_ylim(0, 800)
    a2.set_xlim(0, 1500)
    a2.set_ylabel("Torque (N·m)")
    a2.set_xlabel("Speed (rpm)")
    a2.legend(loc="upper left", fontsize=8, ncol=2)
    a2.grid(True, lw=0.5)
    a2.set_title("(b) Motor torque and load torque", fontsize=9.5, loc="left")
    fig.tight_layout(h_pad=0.8)
    print(f"  6.5: DOL start {I[0]:.0f} A, {T[0]:.0f} N m, peak {T[kmax]:.0f} N m at {n[kmax]:.0f} rpm")
    return save(fig, "06", "fig-6-5-starting-methods-current-torque")


# ---------------------------------------------------------------------------
# Figure 6.6
# ---------------------------------------------------------------------------
def _sp_circuit(ax):
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=9, lw=1.1)
        yt, yb = 5.0, 0.0
        d.add(elm.SourceSin().endpoints((0, yb), (0, yt)).label("230 V\n50 Hz", loc="top"))
        d.add(elm.Line().endpoints((0, yt), (6.6, yt)))
        d.add(elm.Line().endpoints((0, yb), (6.6, yb)))
        # main winding
        d.add(elm.Dot().at((2.4, yt)))
        d.add(elm.Dot().at((2.4, yb)))
        d.add(elm.Resistor().endpoints((2.4, yt), (2.4, 2.5)).label("2.0 Ω", loc="bot"))
        d.add(elm.Inductor2(loops=3).endpoints((2.4, 2.5), (2.4, yb)).label("j3.5 Ω", loc="bot"))
        # auxiliary branch: start capacitor + centrifugal switch, run capacitor dashed in parallel
        d.add(elm.Line().endpoints((6.6, yt), (6.6, 4.4)))
        d.add(elm.Line().endpoints((5.7, 4.4), (7.5, 4.4)))
        d.add(elm.Capacitor().endpoints((5.7, 4.4), (5.7, 3.3)).label("150 µF\nstart", loc="top"))
        d.add(elm.Switch(action="open").endpoints((5.7, 3.3), (5.7, 2.3)).label("centrifugal\nswitch", loc="top"))
        d.add(elm.Capacitor().endpoints((7.5, 4.4), (7.5, 2.3)).label("20 µF\nrun", loc="bot").linestyle("--"))
        d.add(elm.Line().endpoints((5.7, 2.3), (7.5, 2.3)))
        d.add(elm.Line().endpoints((6.6, 2.3), (6.6, 2.1)))
        d.add(elm.Inductor2(loops=3).endpoints((6.6, 2.1), (6.6, yb)).label("auxiliary\nwinding", loc="bot"))
        d.add(elm.Dot().at((6.6, yb)))
        d.draw(show=False)
    ax.text(1.75, 1.25, "main\nwinding", ha="right", va="center", fontsize=9)
    for x0, y0, x1, y1, lab in [(2.4, 4.95, 2.4, 4.45, "$I_m$"), (6.6, 4.95, 6.6, 4.5, "$I_a$")]:
        _farrow(ax, x0, y0, x1, y1, color=INK, lw=1.1, ms=8, z=6)
        ax.text(x0 - 0.12, (y0 + y1) / 2, lab, ha="right", va="center", fontsize=9.5)
    ax.set_aspect("equal")
    ax.axis("off")


def fig_6_6():
    """Single-phase motor: forward/backward torque, capacitor-start circuit and phasors."""
    Tmf, sm = 8.690, 0.12876           # fitted: resultant peak 7.5 N m, 5.0 N m at 1420 rpm
    n = np.linspace(-1499, 1499, 3000)
    s = (NS - n) / NS

    def tk(sl):
        return 2 * Tmf / (sl / sm + sm / sl)

    Tf = tk(s)
    Tb = -tk(2 - s)
    fig = plt.figure(figsize=(6.8, 5.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], width_ratios=[1.45, 1.0])
    a1 = fig.add_subplot(gs[0, :])
    a1.axhline(0, color=INK, lw=0.6)
    a1.axvline(0, color=INK, lw=0.6)
    a1.plot(n, Tf, color=BLUE, lw=1.4, ls="--", label="forward field")
    a1.plot(n, Tb, color=ORANGE, lw=1.4, ls="--", label="backward field")
    a1.plot(n, Tf + Tb, color=INK, lw=2.0, label="resultant")
    Tr = Tf + Tb
    k = np.argmax(Tr)
    a1.plot(n[k], Tr[k], "o", color=INK, ms=4)
    a1.annotate(f"{Tr[k]:.1f} N·m at {n[k]:.0f} rpm", xy=(n[k], Tr[k]), xytext=(380, 8.6), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    tr = tk((NS - 1420) / NS) - tk(2 - (NS - 1420) / NS)
    a1.plot(1420, tr, "s", color=INK, ms=4)
    a1.annotate(f"rated {tr:.1f} N·m, 1420 rpm", xy=(1420, tr), xytext=(1440, 2.0), fontsize=8, ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    a1.annotate("zero torque\nat standstill", xy=(0, 0), xytext=(-620, 4.2), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    a1.set_xlim(-1500, 1500)
    a1.set_ylim(-10, 10)
    a1.set_xlabel("Speed (rpm)")
    a1.set_ylabel("Torque (N·m)")
    a1.legend(loc="lower right", fontsize=8)
    a1.grid(True, lw=0.5)
    a1.set_title("(a) Double-revolving-field torque, 0.75 kW, 4-pole, 50 Hz", fontsize=9.5, loc="left")
    a2 = fig.add_subplot(gs[1, 0])
    _sp_circuit(a2)
    a2.set_title("(b) Capacitor-start (run capacitor dashed: CSCR)", fontsize=9.5, loc="left")
    # phasors at standstill: main Z = 2 + j3.5; auxiliary R = 9, X = 17 ohm (assumed) with 150 uF
    a3 = fig.add_subplot(gs[1, 1])
    Xc = 1 / (2 * np.pi * 50 * 150e-6)
    Im = 230 / (2.0 + 3.5j)
    Ia = 230 / (9.0 + 1j * (17.0 - Xc))
    sc = 1.0 / max(abs(Im), abs(Ia))
    _farrow(a3, 0, 0, 1.0, 0, color=INK, lw=1.6)
    a3.text(1.02, 0.0, "$V$", fontsize=9.5, va="center")
    for I_, c, lab in [(Im, BLUE, "$I_m$"), (Ia, ORANGE, "$I_a$")]:
        z = I_ * sc * 0.95
        _farrow(a3, 0, 0, z.real, z.imag, color=c, lw=1.5)
        a3.text(z.real + 0.03, z.imag + (0.07 if z.imag > 0 else -0.04), lab, color=c, fontsize=9.5,
                va="center")
    am, aa = np.degrees(np.angle(Im)), np.degrees(np.angle(Ia))
    th = np.linspace(np.radians(am), 0, 30)
    a3.plot(0.42 * np.cos(th), 0.42 * np.sin(th), color=BLUE, lw=0.8)
    a3.text(0.40, -0.25, f"{-am:.0f}°", color=BLUE, fontsize=8)
    th = np.linspace(0, np.radians(aa), 30)
    a3.plot(0.26 * np.cos(th), 0.26 * np.sin(th), color=ORANGE, lw=0.8)
    a3.text(0.28, 0.05, f"{aa:.0f}°", color=ORANGE, fontsize=8, va="bottom")
    th = np.linspace(np.radians(am), np.radians(aa), 40)
    a3.plot(0.16 * np.cos(th), 0.16 * np.sin(th), color=INK, lw=0.8)
    a3.text(-0.03, -0.02, f"{aa - am:.0f}°", fontsize=8, ha="right", va="center")
    a3.set_xlim(-0.35, 1.2)
    a3.set_ylim(-1.14, 0.75)
    a3.set_aspect("equal")
    a3.axis("off")
    a3.set_title("(c) Currents at standstill", fontsize=9.5, loc="left")
    a3.text(0.42, -1.13, "auxiliary winding 9 + j17 Ω assumed", fontsize=7, ha="center", va="bottom",
            color="#555555")
    fig.tight_layout(h_pad=0.6)
    print(f"  6.6: Im lags {-am:.1f} deg, Ia leads {aa:.1f} deg, peak {Tr[k]:.2f} at {n[k]:.0f}, rated {tr:.2f}")
    return save(fig, "06", "fig-6-6-single-phase-motors")


if __name__ == "__main__":
    fig_6_1()
    fig_6_2()
    fig_6_3()
    fig_6_4()
    fig_6_5()
    fig_6_6()
