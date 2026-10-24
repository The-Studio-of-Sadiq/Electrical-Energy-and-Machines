"""Figures for Chapter 11 — DC Motor Drives. Run from the repository root: python figures/scripts/ch11.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle, Polygon  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")
GREY = "#888888"

# Motor data used throughout the chapter (Sections 11.1, 11.4, 11.5)
VA_R, IA_R, N_R, RA = 440.0, 370.0, 1000.0, 0.050
KPHI = (VA_R - IA_R * RA) / (N_R * 2 * np.pi / 60)     # 4.025 V s/rad
T_R = KPHI * IA_R                                       # 1489 N m


# ---------------------------------------------------------------- 11.1
def fig_11_1():
    n = np.linspace(0, 2000, 2001)
    nb, nc = 1000.0, 1800.0
    va = np.where(n <= nb, (IA_R * RA + KPHI * n * 2 * np.pi / 60 * 1.0) / VA_R, 1.0)
    va = np.minimum(va, 1.0)
    phi = np.where(n <= nb, 1.0, nb / np.maximum(n, 1))
    # commutation limit: reactance voltage ~ Ia*n, so Ia*n <= const; 0.8 pu current at 1800 rpm
    nk = 0.8 * nc  # 1440 rpm, where the limit starts to bite
    ia = np.where(n <= nk, 1.0, nk / np.maximum(n, 1))
    t_ideal = phi  # torque at rated current
    torque = phi * ia
    power = torque * n / nb
    p_ideal = t_ideal * n / nb
    fig, ax = new_fig(6.4, 3.9)
    ax.axvspan(0, nb, color=COLORS[0], alpha=0.05, lw=0)
    ax.axvspan(nb, nk, color=COLORS[2], alpha=0.07, lw=0)
    ax.axvspan(nk, 2000, color=COLORS[1], alpha=0.05, lw=0)
    ax.axvline(nb, color=GREY, ls="--", lw=1)
    ax.axvline(nc, color=GREY, ls=":", lw=0.9)
    m = n <= nk
    ax.plot(n[m], torque[m], color=COLORS[1], lw=3.2, label="torque $T$")
    ax.plot(n[~m], t_ideal[~m], color=COLORS[1], lw=1.0, ls=":")
    ax.plot(n[~m], torque[~m], color=COLORS[1], lw=2.4, ls="--")
    ax.plot(n, phi, color=COLORS[2], lw=1.4, ls=(0, (4, 2)), label=r"field flux $\Phi$")
    ax.plot(n, va, color=COLORS[0], lw=1.6, label="armature voltage $V_a$")
    ax.plot(n[m], power[m], color=COLORS[3], lw=1.6, ls="-.", label="power $P$")
    ax.plot(n[~m], p_ideal[~m], color=COLORS[3], lw=1.0, ls=":")
    ax.plot(n[~m], power[~m], color=COLORS[3], lw=1.6, ls="--")
    ax.text(500, 1.13, "armature control,\nconstant torque", ha="center", va="center", fontsize=9)
    ax.text(1220, 1.13, "field control,\nconstant power", ha="center", va="center", fontsize=9)
    ax.text(1720, 1.13, "commutation\nlimit", ha="center", va="center", fontsize=9)
    i18 = int(nc)
    ax.plot([nc, nc], [torque[i18], power[i18]], "o", color=INK, ms=4, zorder=5)
    ax.text(nc - 20, torque[i18] - 0.03, "0.445 (80 % of\nrated $I_a$)", fontsize=7.5, color=COLORS[1], ha="right", va="top")
    ax.text(nc + 15, power[i18] + 0.02, "0.80", fontsize=7.5, color=COLORS[3], va="bottom")
    ax.plot(nc, phi[i18], "o", color=GREY, ms=3, zorder=5)
    ax.text(nc + 15, phi[i18] + 0.02, "0.556\n(rated $I_a$)", fontsize=7, color=GREY, va="bottom")
    ax.text(1010, 0.40, "base speed\n1000 rpm", fontsize=8, color=GREY, va="bottom")
    ax.annotate("0.04 ($I_aR_a$ drop)", xy=(0, 0.042), xytext=(140, 0.015), fontsize=7.5, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel("speed (rpm)")
    ax.set_ylabel("per unit of rated value")
    ax.legend(loc="lower right", bbox_to_anchor=(0.88, 0.02), fontsize=8)
    save(fig, "11", "fig-11-1-dc-capability")


# ---------------------------------------------------------------- 11.2
def fig_11_2():
    T = np.linspace(0, 1.5 * T_R, 200)
    fig, ax = new_fig(6.4, 4.0)
    for k, Va in enumerate([440, 330, 220, 110, 60.7]):
        n0 = Va / KPHI * 60 / (2 * np.pi)
        n = n0 - RA * T / KPHI ** 2 * 60 / (2 * np.pi)
        ax.plot(T, n, color=COLORS[k])
        ax.text(1.5 * T_R + 25, n[-1], f"{Va:g} V", va="center", fontsize=8.5, color=COLORS[k])
        ax.text(20, n0 + 8, f"{n0:.0f} rpm", fontsize=7.5, color=COLORS[k], va="bottom")
    ax.plot(T_R, 1000, "o", color=INK, ms=5, zorder=5)
    ax.annotate("rated point\n1000 rpm, 1489 N m", xy=(T_R, 1000), xytext=(T_R - 330, 870), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8), ha="right")
    for y in (1000, 100):
        ax.axhline(y, color=INK, ls=(0, (5, 3)), lw=0.9, xmax=1.5 * T_R / 2400)
    ax.text(200, 990, "closed-loop speed held (1000 rpm)", fontsize=7.5, va="top")
    ax.text(200, 92, "closed-loop speed held (100 rpm)", fontsize=7.5, va="top")
    ax.axvline(1.5 * T_R, color=COLORS[1], ls="--", lw=1)
    ax.text(1.5 * T_R - 15, 588, "current limit", rotation=90, ha="right", va="center", fontsize=7.5,
            color=COLORS[1])
    ax.plot([0, T_R], [522, 522], color=GREY, lw=0.6, ls=":")
    ax.annotate("", xy=(T_R, 522 - 43.9), xytext=(T_R, 522),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(T_R - 25, 532, "43.9 rpm per rated torque", fontsize=7.5, color=GREY, va="bottom", ha="right")
    ax.set_xlim(0, 2400)
    ax.set_ylim(0, 1100)
    ax.set_xlabel("torque (N m)")
    ax.set_ylabel("speed (rpm)")
    sec = ax.secondary_xaxis("top", functions=(lambda x: x / T_R, lambda x: x * T_R))
    sec.set_xlabel("torque (per unit)", fontsize=9)
    sec.set_xticks([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    save(fig, "11", "fig-11-2-armature-control-family")


# ---------------------------------------------------------------- 11.3
def _sw(d, x, ytop, name, dname=None, diode=True):
    """IGBT with collector at (x, ytop), emitter 1.4 below; antiparallel diode to the right."""
    q = d.add(elm.IgbtN().theta(0).anchor("collector").at((x, ytop)))
    d.add(elm.Label().at((x - 0.85, ytop - 0.45)).label(name, halign="right", fontsize=8.5))
    if diode:
        d.add(elm.Line().at((x, ytop)).to((x + 0.8, ytop)))
        d.add(elm.Line().at((x, ytop - 1.4)).to((x + 0.8, ytop - 1.4)))
        d.add(elm.Diode().at((x + 0.8, ytop - 1.4)).to((x + 0.8, ytop)))
        if dname:
            d.add(elm.Label().at((x + 1.15, ytop - 0.7)).label(dname, halign="left", fontsize=8.5))
    return q


def _qplane(ax, x0, y0, shade, size=0.7):
    """Small Va-Ia plane centred at (x0, y0); shade = list of quadrant numbers."""
    pos = {1: (0, 0), 2: (-1, 0), 3: (-1, -1), 4: (0, -1)}
    for qn, (cx, cy) in pos.items():
        fc = "#9FD8C4" if qn in shade else "#F4F4F4"
        ax.add_patch(Rectangle((x0 + cx * size, y0 + cy * size), size, size, fc=fc, ec="none"))
        ax.text(x0 + (cx + 0.5) * size, y0 + (cy + 0.5) * size, ["I", "II", "III", "IV"][qn - 1],
                ha="center", va="center", fontsize=7)
    ax.annotate("", xy=(x0 + size * 1.3, y0), xytext=(x0 - size * 1.2, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8))
    ax.annotate("", xy=(x0, y0 + size * 1.3), xytext=(x0, y0 - size * 1.2),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8))
    ax.text(x0 + size * 1.35, y0, "$I_a$", fontsize=8, va="center")
    ax.text(x0, y0 + size * 1.35, "$V_a$", fontsize=8, ha="center", va="bottom")


def _armature_down(d, x, ymid, ybot, rlab="$R_a$ 0.08 Ω", llab="$L_a$ + 10 mH"):
    """Armature branch from (x, ymid) to the right then down through E to the bottom rail."""
    d.add(elm.Line().at((x, ymid)).to((x + 1.0, ymid)))
    d.add(elm.Resistor().at((x + 1.0, ymid)).to((x + 2.4, ymid)).label(rlab, fontsize=8))
    d.add(elm.Inductor2(loops=3).at((x + 2.4, ymid)).to((x + 4.0, ymid)).label(llab, loc="bottom", fontsize=8))
    d.add(elm.Line().at((x + 4.0, ymid)).to((x + 4.6, ymid)))
    d.add(elm.SourceV().up().at((x + 4.6, ybot)).to((x + 4.6, ymid)).label("$E$", loc="bottom", fontsize=9))
    d.add(elm.Line().at((x + 4.6, ybot)).to((x, ybot)))


def _ia_arrow(ax, x, y):
    ax.annotate("", xy=(x + 0.55, y - 0.28), xytext=(x, y - 0.28),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.1, mutation_scale=9))
    ax.text(x + 0.27, y - 0.38, "$I_a$", ha="center", va="top", fontsize=8.5, color=COLORS[1])


def fig_11_3():
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=2, fontsize=8.5, lw=1.1)
    H = 6.0
    # ---- (a) one-quadrant chopper, origin (0, 9)
    ox, oy = 0.0, 9.0
    d.add(elm.SourceV().at((ox, oy)).to((ox, oy + H)).label("$V_{dc}$\n750 V", loc="top", fontsize=8.5))
    d.add(elm.Line().at((ox, oy + H)).to((ox + 2.5, oy + H)))
    d.add(elm.Line().at((ox, oy)).to((ox + 2.5, oy)))
    _sw(d, ox + 2.5, oy + H, "S1", diode=False)
    d.add(elm.Line().at((ox + 2.5, oy + H - 1.4)).to((ox + 2.5, oy + 3)))
    d.add(elm.Diode().at((ox + 2.5, oy)).to((ox + 2.5, oy + 3)).label("D1", loc="bottom", fontsize=8.5))
    d.add(elm.Dot().at((ox + 2.5, oy + 3)))
    _armature_down(d, ox + 2.5, oy + 3, oy)
    # ---- (b) two-quadrant chopper, origin (11.4, 9)
    ox = 11.4
    d.add(elm.SourceV().at((ox, oy)).to((ox, oy + H)).label("$V_{dc}$", loc="top", fontsize=8.5))
    xl = ox + 5.4
    d.add(elm.Line().at((ox, oy + H)).to((xl, oy + H)))
    d.add(elm.Line().at((ox, oy)).to((xl, oy)))
    d.add(elm.Capacitor().at((ox + 1.3, oy + H)).to((ox + 1.3, oy)).label("$C$", loc="bottom", fontsize=8.5))
    d.add(elm.Resistor().at((ox + 3.2, oy + H)).to((ox + 3.2, oy + 2.6)).label("$R_{br}$", loc="bottom",
                                                                                 fontsize=8.5))
    d.add(elm.Line().at((ox + 3.2, oy + 2.6)).to((ox + 3.2, oy + 1.4)))
    _sw(d, ox + 3.2, oy + 1.4, "S5", diode=False)
    _sw(d, xl, oy + H, "S1", "D1")
    _sw(d, xl, oy + 1.4, "S2", "D2")
    d.add(elm.Line().at((xl, oy + H - 1.4)).to((xl, oy + 1.4)))
    d.add(elm.Dot().at((xl, oy + 3)))
    d.add(elm.Line().at((xl, oy + 3)).to((xl + 1.0, oy + 3)))
    _armature_down(d, xl + 1.0, oy + 3, oy, rlab="$R_a$", llab="$L_a$")
    d.add(elm.Line().at((xl + 1.0, oy)).to((xl, oy)))
    # ---- (c) four-quadrant H-bridge, origin (0, 0)
    ox, oy = 0.0, 0.0
    d.add(elm.SourceV().at((ox, oy)).to((ox, oy + H)).label("$V_{dc}$", loc="top", fontsize=8.5))
    d.add(elm.Capacitor().at((ox + 1.3, oy + H)).to((ox + 1.3, oy)).label("$C$", loc="bottom", fontsize=8.5))
    xa, xb = ox + 3.4, ox + 11.4
    d.add(elm.Line().at((ox, oy + H)).to((xb, oy + H)))
    d.add(elm.Line().at((ox, oy)).to((xb, oy)))
    _sw(d, xa, oy + H, "S1", "D1")
    _sw(d, xa, oy + 1.4, "S2", "D2")
    _sw(d, xb, oy + H, "S3", "D3")
    _sw(d, xb, oy + 1.4, "S4", "D4")
    for x in (xa, xb):
        d.add(elm.Line().at((x, oy + H - 1.4)).to((x, oy + 1.4)))
        d.add(elm.Dot().at((x, oy + 3)))
    d.add(elm.Line().at((xa, oy + 3)).to((xa + 1.4, oy + 3)))
    d.add(elm.Resistor().at((xa + 1.4, oy + 3)).to((xa + 2.8, oy + 3)).label("$R_a$", fontsize=8.5))
    d.add(elm.Inductor2(loops=3).at((xa + 2.8, oy + 3)).to((xa + 4.4, oy + 3)).label("$L_a$", loc="bottom",
                                                                                    fontsize=8.5))
    d.add(elm.SourceV().right().at((xa + 4.4, oy + 3)).to((xa + 6.0, oy + 3)).reverse().label("$E$", fontsize=9))
    d.add(elm.Line().at((xa + 6.0, oy + 3)).to((xb, oy + 3)))
    d.draw(show=False)
    # annotations in drawing coordinates
    _ia_arrow(ax, 2.85, 12.0)
    _ia_arrow(ax, xl + 0.2, 12.0)
    _ia_arrow(ax, xa + 0.3, 3.0)
    _qplane(ax, 9.7, 13.4, [1])
    _qplane(ax, 25.4, 13.4, [1, 2])
    _qplane(ax, 16.6, 3.2, [1, 2, 3, 4])
    ax.text(-0.6, 16.6, "(a) one-quadrant chopper", fontsize=9.5, weight="bold")
    ax.text(10.8, 16.6, "(b) two-quadrant (current-reversible) chopper", fontsize=9.5, weight="bold")
    ax.text(-0.6, 7.3, "(c) four-quadrant H-bridge", fontsize=9.5, weight="bold")
    ax.text(15.2, 7.9, "(b): S1–D2 buck, quadrant I (motoring); S2–D1 boost,\nquadrant II (regeneration); "
            "S5 + $R_{br}$ optional braking resistor",
            fontsize=7.5, va="top")
    ax.text(18.6, 3.2, "(c): S1 + S4 give $+V_a$, S2 + S3 give $-V_a$;\ncurrent of either sign flows in the\n"
            "switches or their diodes: all four\nquadrants",
            fontsize=7.5, va="center")
    ax.set_xlim(-1.0, 27.4)
    ax.set_ylim(-0.6, 17.2)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "11", "fig-11-3-chopper-quadrants")


# ---------------------------------------------------------------- 11.4
def _sum(ax, x, y, r=0.32, signs=None):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.plot([x - r * 0.55, x + r * 0.55], [y, y], color=INK, lw=0.8, zorder=4)
    ax.plot([x, x], [y - r * 0.55, y + r * 0.55], color=INK, lw=0.8, zorder=4)
    for (dx, dy, s) in (signs or []):
        ax.text(x + dx, y + dy, s, fontsize=8, ha="center", va="center", zorder=4)


def _line(ax, pts, color=INK, arrow_end=True, ls="-", lw=1.0):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys, color=color, lw=lw, ls=ls)
    if arrow_end:
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9, shrinkA=0, shrinkB=0))


def fig_11_4():
    fig, ax = schematic(6.8, 4.9, xlim=(0, 22), ylim=(0.2, 15.8))
    bh = 1.6
    fs = 6.5
    pi_fc, pl_fc = "#FFF4E0", "#EEF3F8"

    def blk(x0, x1, y, text, fc=pl_fc, size=fs):
        box(ax, x0, y - bh / 2, x1 - x0, bh, text, fc=fc, fontsize=size)

    # ---------- row 1: speed and current controllers, left to right
    y1 = 13.6
    ax.text(0.1, y1 + 0.15, r"$\omega^{*}$", fontsize=9.5, va="bottom")
    _line(ax, [(0.1, y1), (0.6, y1)])
    blk(0.6, 2.0, y1, "ramp")
    _sum(ax, 2.6, y1, signs=[(-0.45, -0.5, "−")])
    _line(ax, [(2.0, y1), (2.28, y1)])
    blk(3.2, 6.6, y1, "PI speed\n$K_p$ = 254 A s/rad\n$T_i$ = 29 ms", fc=pi_fc)
    _line(ax, [(2.92, y1), (3.2, y1)])
    blk(7.1, 8.7, y1, "")
    ax.plot([7.3, 7.65, 8.15, 8.5], [y1 - 0.1, y1 - 0.1, y1 + 0.5, y1 + 0.5], color=INK, lw=1)
    ax.text(7.9, y1 - 0.5, "±555 A", ha="center", va="center", fontsize=6.3)
    ax.text(7.9, y1 + bh / 2 + 0.1, "current limit\n(1.5 pu)", ha="center", va="bottom", fontsize=6.5)
    _line(ax, [(6.6, y1), (7.1, y1)])
    _sum(ax, 9.75, y1, signs=[(-0.45, -0.5, "−")])
    _line(ax, [(8.7, y1), (9.43, y1)])
    ax.text(9.05, y1 + 0.1, "$I_a^{*}$", fontsize=8.5, ha="center", va="bottom")
    blk(10.2, 13.4, y1, "PI current\n$K_p$ = 0.47 V/A\n$T_i$ = 25.6 ms", fc=pi_fc)
    _line(ax, [(10.07, y1), (10.2, y1)])
    blk(13.8, 18.3, y1, "thyristor converter\ngain 1, delay 1.67 ms\n$\\alpha$ = 15° to 150°")
    _line(ax, [(13.4, y1), (13.8, y1)])
    ax.text(18.75, y1 + 0.1, "$V_a$", fontsize=9, ha="center", va="bottom")
    # ---------- row 2: motor model, right to left
    y2 = 8.6
    _line(ax, [(18.3, y1), (19.2, y1), (19.2, y2 + 0.32)])
    _sum(ax, 19.2, y2, signs=[(0.45, -0.5, "−")])
    blk(15.4, 18.5, y2, "armature\n$1/(R_a+L_a s)$", size=fs + 0.5)
    ax.text(16.95, y2 + bh / 2 + 0.1, "$R_a$ = 0.0977 Ω\n$L_a$ = 2.5 mH", fontsize=6.3, ha="center", va="bottom")
    _line(ax, [(18.88, y2), (18.5, y2)])
    blk(12.6, 14.2, y2, "$k\\Phi$\n4.025", size=fs + 0.5)
    _line(ax, [(15.4, y2), (14.2, y2)])
    ax.plot(14.8, y2, "o", color=INK, ms=3.5)
    ax.text(14.85, y2 - 0.15, "$I_a$", fontsize=8.5, ha="left", va="top")
    _sum(ax, 11.6, y2, signs=[(-0.45, -0.5, "−")])
    _line(ax, [(12.6, y2), (11.92, y2)])
    ax.text(12.25, y2 - 0.15, "$T_e$", fontsize=8.5, ha="center", va="top")
    _line(ax, [(11.6, y2 - 1.5), (11.6, y2 - 0.32)])
    ax.text(11.75, y2 - 1.45, "$T_L$", fontsize=8.5, va="bottom")
    blk(7.6, 10.8, y2, "mechanics\n$1/(Js)$\n$J$ = 15 kg m$^2$", size=fs + 0.3)
    _line(ax, [(11.28, y2), (10.8, y2)])
    _line(ax, [(7.6, y2), (2.6, y2)], arrow_end=False)
    ax.plot(6.2, y2, "o", color=INK, ms=3.5)
    ax.text(6.9, y2 + 0.1, r"$\omega$", fontsize=10, ha="center", va="bottom")
    # speed feedback: omega -> filter 2 ms -> sum 1
    blk(1.75, 3.45, 11.0, "filter\n2 ms")
    ax.plot([2.6, 2.6], [y2, 11.0 - bh / 2], color=INK, lw=1.0)
    _line(ax, [(2.6, 11.0 + bh / 2), (2.6, y1 - 0.32)])
    ax.text(2.45, 9.3, "encoder", fontsize=6.8, ha="right", va="center")
    # current feedback: Ia -> filter 1 ms -> sum 2
    ax.plot([14.8, 14.8, 12.6], [y2, 11.0, 11.0], color=INK, lw=1.0)
    blk(10.9, 12.6, 11.0, "filter\n1 ms")
    ax.plot([10.9, 9.75], [11.0, 11.0], color=INK, lw=1.0)
    _line(ax, [(9.75, 11.0), (9.75, y1 - 0.32)])
    # back-EMF path: omega -> k Phi -> sum 3
    ye = 5.7
    ax.plot([6.2, 6.2, 12.6], [y2, ye, ye], color=INK, lw=1.0)
    blk(12.6, 14.2, ye, "$k\\Phi$", size=fs + 2)
    _line(ax, [(14.2, ye), (19.2, ye), (19.2, y2 - 0.32)])
    ax.text(16.8, ye + 0.1, "back-EMF $E=k\\Phi\\,\\omega$", fontsize=7, ha="center", va="bottom")
    # ---------- row 3: field (EMF) control, left to right
    y3 = 2.0
    ax.text(0.1, y3 + 0.4, "$E^{*}$ = 418 V", fontsize=7.2, va="bottom")
    _line(ax, [(0.1, y3), (2.48, y3)])
    _sum(ax, 2.8, y3, signs=[(-0.45, -0.5, "−")])
    _line(ax, [(2.8, y3 - 1.5), (2.8, y3 - 0.32)])
    ax.text(2.95, y3 - 1.45, "measured EMF $V_a-R_aI_a$", fontsize=6.6, va="bottom")
    blk(3.6, 6.4, y3, "PI field\ncontroller", fc=pi_fc)
    _line(ax, [(3.12, y3), (3.6, y3)])
    blk(7.0, 9.8, y3, "field\nconverter")
    _line(ax, [(6.4, y3), (7.0, y3)])
    blk(10.4, 13.2, y3, "field winding\n$\\tau_f$ = 1.5 s")
    _line(ax, [(9.8, y3), (10.4, y3)])
    # flux output: dashed, multiplies into both k Phi gains
    fl = dict(color=COLORS[2], ls="--", lw=1.1)
    ax.plot([13.2, 16.2, 16.2, 13.4], [y3, y3, 7.0, 7.0], **fl)
    _line(ax, [(13.4, 7.0), (13.4, y2 - bh / 2)], color=COLORS[2], ls="--", lw=1.1)
    ax.plot([16.2, 13.4], [3.8, 3.8], **fl)
    _line(ax, [(13.4, 3.8), (13.4, ye - bh / 2)], color=COLORS[2], ls="--", lw=1.1)
    ax.text(16.4, y3 + 0.1, "flux $k\\Phi$ sets both\n$k\\Phi$ gains", fontsize=7, color=COLORS[2], va="bottom")
    ax.text(21.9, 15.3, "speed and current loops", ha="right", fontsize=7.5, color=GREY)
    ax.text(21.9, 10.0, "motor", ha="right", fontsize=7.5, color=GREY)
    ax.text(21.9, 0.4, "field-weakening (EMF) loop", ha="right", fontsize=7.5, color=GREY)
    save(fig, "11", "fig-11-4-cascade-control")


# ---------------------------------------------------------------- 11.5
def _breaker(ax, x, y, s=0.36):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.1, zorder=3))


def _fuse(ax, x, y, w=0.6, h=0.26):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=INK, lw=1, zorder=3))
    ax.plot([x - w / 2, x + w / 2], [y, y], color=INK, lw=0.8, zorder=4)


def _coil(ax, x, y, n=3, r=0.18):
    t = np.linspace(0, np.pi, 30)
    ax.add_patch(Rectangle((x - n * r, y - 0.02), 2 * n * r, 0.04, fc="white", ec="white", zorder=3))
    for k in range(n):
        cx = x + (2 * k + 1 - n) * r
        ax.plot(cx - r * np.cos(t), y + r * np.sin(t), color=INK, lw=1.2, zorder=4)


def _thy(ax, x, y, s=0.3, up=True, color=INK):
    """Thyristor symbol: triangle pointing in the conduction direction (up or down)."""
    sgn = 1 if up else -1
    ax.add_patch(Polygon([(x - s, y - sgn * s * 0.55), (x + s, y - sgn * s * 0.55), (x, y + sgn * s * 0.55)],
                         closed=True, fc=color, ec=color, zorder=4))
    ax.plot([x - s, x + s], [y + sgn * s * 0.55] * 2, color=color, lw=1.2, zorder=4)
    ax.plot([x, x], [y - sgn * s * 1.3, y + sgn * s * 1.3], color=color, lw=1.0, zorder=3)
    ax.plot([x + s * 0.2, x + s * 0.9], [y + sgn * s * 0.55, y + sgn * s * 1.15], color=color, lw=0.9, zorder=4)


def fig_11_5():
    fig, ax = schematic(6.8, 5.0, xlim=(0, 23.6), ylim=(0, 17.35))
    lwp = 1.5
    sig = dict(color=COLORS[0], lw=0.9, ls=":")
    lab = dict(fontsize=6.8, ha="center", va="top")
    yb = 14.2   # main power path
    # supply, breaker, reactor, fuses
    ax.text(0.2, yb + 0.35, "400 V 50 Hz", fontsize=7.5, va="bottom")
    ax.plot([0.2, 7.6], [yb, yb], color=INK, lw=lwp)
    for dx in (0.75, 0.95, 1.15):
        ax.plot([dx - 0.1, dx + 0.1], [yb - 0.18, yb + 0.18], color=INK, lw=0.8)
    _breaker(ax, 2.4, yb)
    ax.text(2.4, yb - 0.4, "circuit\nbreaker", **lab)
    _coil(ax, 4.4, yb)
    ax.text(4.4, yb - 0.4, "line\nreactor\n4 %", **lab)
    _fuse(ax, 6.4, yb)
    ax.text(6.4, yb - 0.4, "semi-\ncond.\nfuses", **lab)
    # dual bridge
    ax.plot([7.6, 7.6], [yb + 1.2, yb - 1.2], color=INK, lw=lwp)
    for yy, name, up in [(yb + 1.2, "forward bridge", True), (yb - 1.2, "reverse bridge", False)]:
        ax.plot([7.6, 8.0], [yy, yy], color=INK, lw=lwp)
        box(ax, 8.0, yy - 0.7, 4.0, 1.4, "", fc="#EEF3F8")
        _thy(ax, 8.55, yy, up=up)
        ax.text(10.4, yy, name.replace(" ", "\n"), fontsize=6.8, ha="center", va="center")
        ax.plot([12.0, 12.4], [yy, yy], color=INK, lw=lwp)
    ax.plot([12.4, 12.4], [yb + 1.2, yb - 1.2], color=INK, lw=lwp)
    ax.text(10.0, yb + 2.05, "dual (antiparallel) six-pulse thyristor bridges", fontsize=7, ha="center", va="bottom")
    # DC contactor, Hall sensor, Va tap, motor
    ax.plot([12.4, 13.3], [yb, yb], color=INK, lw=lwp)
    ax.plot([13.3, 13.75], [yb, yb + 0.35], color=INK, lw=lwp)
    ax.plot([13.8, 17.8, 17.8], [yb, yb, 11.6], color=INK, lw=lwp)
    ax.text(13.55, yb - 0.4, "DC\ncontactor", **lab)
    ax.add_patch(Circle((14.6, yb), 0.3, fc="none", ec=COLORS[2], lw=1.4, zorder=4))
    ax.text(14.6, yb + 0.4, "Hall $I_a$", fontsize=6.8, ha="center", va="bottom", color=COLORS[2])
    ax.plot(15.7, yb, "o", color=INK, ms=3)
    ax.text(15.8, yb + 0.3, "$V_a$ meas.", fontsize=6.8, va="bottom", color=COLORS[0])
    mx, my = 17.8, 10.8
    ax.add_patch(Circle((mx, my), 0.8, fc="white", ec=INK, lw=1.4, zorder=3))
    ax.text(mx, my, "M", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(mx, my - 1.0, "DC motor 150 kW\n440 V, 370 A, 1000 rpm", fontsize=6.8, ha="center", va="top")
    # shaft and encoder
    ax.plot([mx + 0.8, mx + 2.0], [my, my], color=INK, lw=2.6)
    ax.add_patch(Rectangle((mx + 2.0, my - 0.4), 0.6, 0.8, fc="white", ec=INK, lw=1))
    ax.text(mx + 2.8, my, "encoder\n2048 lines", fontsize=6.8, va="center")
    # blower
    ax.add_patch(Circle((20.7, 13.4), 0.45, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.text(20.7, 13.4, "B", ha="center", va="center", fontsize=8)
    ax.plot([20.25, mx + 0.6], [13.15, my + 0.55], color=INK, lw=0.8, ls=(0, (2, 2)))
    ax.text(21.25, 13.4, "blower +\nairflow\nswitch", fontsize=6.8, va="center")
    # field branch
    yf = 4.4
    ax.text(9.3, yf + 0.3, "1-phase\nsupply", fontsize=6.8, va="bottom")
    ax.plot([9.3, 11.0], [yf, yf], color=INK, lw=1.2)
    _fuse(ax, 10.3, yf)
    ax.text(10.3, yf - 0.4, "fuse", **lab)
    box(ax, 11.0, yf - 0.7, 4.0, 1.4, "", fc="#EEF3F8")
    _thy(ax, 11.5, yf)
    ax.text(13.45, yf, "1-phase fully\ncontrolled\nbridge", fontsize=6.6, ha="center", va="center")
    ax.plot([15.0, 18.6], [yf, yf], color=INK, lw=1.2)
    ax.add_patch(Rectangle((15.5, yf - 0.32), 0.9, 0.64, fc="white", ec=COLORS[3], lw=1.1, zorder=3))
    ax.text(15.95, yf, "$I_f$", fontsize=7.5, ha="center", va="center", color=COLORS[3], zorder=4)
    ax.text(15.95, yf - 0.4, "field-\ncurrent\nrelay", fontsize=6.6, ha="center", va="top", color=COLORS[3])
    _coil(ax, mx + 0.1, yf, n=4)
    ax.text(mx + 0.4, yf - 0.4, "field winding\n(on motor)\n310 V, 8 A", **lab)
    # controller
    cx0, cy0, cw, ch = 0.4, 3.0, 8.6, 5.0
    box(ax, cx0, cy0, cw, ch, "", fc="#FFF4E0")
    ax.text(cx0 + cw / 2, cy0 + ch - 0.5, "Digital controller", fontsize=9, ha="center", weight="bold")
    ax.text(cx0 + cw / 2, cy0 + ch - 1.1,
            "ramp, speed and current loops,\nEMF / field loop, firing-angle\ngeneration (PLL synchronised\nto the supply), protection logic",
            fontsize=6.8, ha="center", va="top")
    # firing pulses up to the bridges, across to the field bridge
    fir = dict(arrowstyle="-|>", color=COLORS[1], lw=1.0, ls="--", shrinkA=0, shrinkB=0)
    ax.plot([8.6, 8.6], [cy0 + ch, 11.2], color=COLORS[1], lw=1.0, ls="--")
    ax.annotate("", xy=(8.6, yb - 1.9), xytext=(8.6, 11.2), arrowprops=fir)
    ax.text(8.45, 10.0, "firing pulses\n(both bridges)", fontsize=6.6, color=COLORS[1], ha="right", va="center")
    ax.plot([cx0 + cw, 13.2], [3.25, 3.25], color=COLORS[1], lw=1.0, ls="--")
    ax.annotate("", xy=(13.2, yf - 0.7), xytext=(13.2, 3.25), arrowprops=fir)
    ax.text(9.2, 3.15, "firing (field bridge)", fontsize=6.6, color=COLORS[1], va="top")
    # supply synchronisation
    ax.plot([1.6, 1.6], [yb, cy0 + ch + 0.3], **sig)
    ax.annotate("", xy=(1.6, cy0 + ch), xytext=(1.6, cy0 + ch + 0.3),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(1.75, 10.0, "supply\nvoltage\n(sync)", fontsize=6.6, color=COLORS[0], va="center")
    # measured signals into the controller
    ins = [(mx + 2.3, my - 0.4, 6.4, "encoder"), (14.6, yb - 0.3, 7.4, "$I_a$"),
           (15.7, yb, 6.9, "$V_a$"), (15.95, yf + 0.32, 5.9, "$I_f$")]
    for sx, sy, yy, name in ins:
        ax.plot([sx, sx, cx0 + cw + 0.35], [sy, yy, yy], **sig)
        ax.annotate("", xy=(cx0 + cw, yy), xytext=(cx0 + cw + 0.35, yy),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=0.9, shrinkA=0, shrinkB=0))
        ax.text(sx - 0.12, yy + 0.05, name, fontsize=6.6, color=COLORS[0], va="bottom", ha="right")
    # protection list
    ax.text(9.8, 1.2, "Protection: overcurrent · field failure · overspeed · blower failure ·\n"
            "motor thermistor · supply phase loss · commutation failure",
            fontsize=6.8, va="center")
    save(fig, "11", "fig-11-5-dc-drive-architecture")


if __name__ == "__main__":
    fig_11_1()
    fig_11_2()
    fig_11_3()
    fig_11_4()
    fig_11_5()
