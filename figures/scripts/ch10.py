"""Figures for Chapter 10 — Drive-System Fundamentals. Run from the repository root: python figures/scripts/ch10.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

GREY = "#888888"


def fat_arrow(ax, x0, y0, x1, y1, both=True, color="#4A7DB5", lw=3.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle=("<|-|>" if both else "-|>") + ",head_length=0.45,head_width=0.35", mutation_scale=12,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- 10.1
def fig_10_1():
    fig, ax = schematic(6.8, 4.3, xlim=(0, 18.2), ylim=(0, 11.5))
    names = [("Supply", "grid 400 V\n50 Hz, DC line\nor battery"),
             ("Converter", "rectifier,\nDC link,\ninverter\nor chopper"),
             ("Motor", "induction,\nPM or DC"),
             ("Gearbox", "transmission,\nratio $n$"),
             ("Load", "conveyor\npulley, pump,\nhoist drum")]
    eff = ["", r"$\eta\approx0.97$", r"$\eta\approx0.95$", r"$\eta_g\approx0.96$", ""]
    w, h, gap = 2.7, 2.6, 1.05
    xs = [0.2 + i * (w + gap) for i in range(5)]
    y = 7.2
    for i, (x, (t, sub)) in enumerate(zip(xs, names)):
        box(ax, x, y, w, h, "", fc="#EEF3F8")
        ax.text(x + w / 2, y + h - 0.4, t, ha="center", va="center", fontsize=9.5, weight="bold", color=INK)
        ax.text(x + w / 2, y + (h - 0.7) / 2, sub, ha="center", va="center", fontsize=7.5, color=INK,
                linespacing=1.1)
        if eff[i]:
            ax.text(x + w / 2, y - 0.4, eff[i], ha="center", va="center", fontsize=9, color=COLORS[1])
        if i < 4:
            fat_arrow(ax, x + w + 0.05, y + h / 2, x + w + gap - 0.05, y + h / 2)
    ax.text(9.0, 10.85, "power flow (both directions: motoring and regenerative braking)",
            ha="center", fontsize=8.5, color="#4A7DB5")
    # motor shaft encoder
    mx = xs[2] + w / 2
    ax.add_patch(Rectangle((mx - 0.35, y - 1.45), 0.7, 0.55, fc="white", ec=INK, lw=1))
    ax.text(mx + 0.5, y - 1.18, "encoder", fontsize=7.5, va="center")
    ax.plot([mx, mx], [y - 0.9, y - 0.6], color=INK, lw=1)
    # current sensor at converter output
    cx = xs[1] + w + gap / 2
    ax.add_patch(Circle((cx, y + h / 2), 0.28, fc="none", ec=COLORS[2], lw=1.4, zorder=5))
    ax.text(cx, y + h + 0.1, "current\nsensors", ha="center", va="bottom", fontsize=7, color=COLORS[2])
    # controller
    box(ax, 4.2, 1.2, 6.4, 1.8, "", fc="#FFF4E0")
    ax.text(7.4, 2.35, "Controller", ha="center", fontsize=9.5, weight="bold")
    ax.text(7.4, 1.65, "current, speed and position loops", ha="center", fontsize=7.5)
    # reference
    arrow(ax, 0.6, 2.1, 4.2, 2.1)
    ax.text(0.6, 2.3, "speed set point\n$\\omega^{*}$", fontsize=8, va="bottom")
    # gate signals
    gx = xs[1] + w / 2
    arrow(ax, gx, 3.0, gx, y, color=COLORS[1])
    ax.text(gx - 0.15, 4.6, "gate\nsignals", ha="right", fontsize=7.5, color=COLORS[1])
    # current feedback
    ax.plot([cx, cx], [y + h / 2 - 0.28, 3.9], color=COLORS[2], lw=1.1, ls="--")
    arrow(ax, cx, 3.9, cx, 3.0, color=COLORS[2], linestyle="--")
    ax.text(cx + 0.12, 4.6, "current\nfeedback", fontsize=7.5, color=COLORS[2])
    # speed feedback
    ax.plot([mx, mx], [y - 1.45, 3.7], color=COLORS[0], lw=1.1, ls="--")
    ax.plot([mx, 9.8], [3.7, 3.7], color=COLORS[0], lw=1.1, ls="--")
    arrow(ax, 9.8, 3.7, 9.8, 3.0, color=COLORS[0], linestyle="--")
    ax.text(10.0, 4.0, "speed / position feedback", fontsize=7.5, color=COLORS[0])
    ax.text(9.0, 0.35, "chain efficiency at rated load  $0.97\\times0.95\\times0.96\\approx0.88$",
            ha="center", fontsize=8.5, color=COLORS[1])
    save(fig, "10", "fig-10-1-drive-system-blocks")


# ---------------------------------------------------------------- 10.2
def fig_10_2():
    t = [0, 2, 10, 12, 20]
    T = [180, 60, -100, 0]
    fig, ax = new_fig(6.4, 3.8)
    ax.axvspan(10, 12, color=COLORS[2], alpha=0.15, lw=0)
    ax.text(11, -82, "regen-\nerative", ha="center", va="center", fontsize=8.5, color="#00704F")
    ax.stairs(T, t, color=COLORS[0], lw=2.0, baseline=None)
    ax.plot([0, 0], [0, 180], color=COLORS[0], lw=2.0)
    ax.axhline(0, color=INK, lw=0.6)
    ax.axhline(200, color=COLORS[3], lw=1.2)
    ax.text(19.8, 203, "drive current limit (200 N m)", ha="right", va="bottom", fontsize=8.5, color=COLORS[3])
    ax.axhline(75.4, color=COLORS[1], ls="--", lw=1.3)
    ax.text(19.8, 71, r"$T_{rms}$ = 75.4 N m, equal weighting", ha="right", va="top", fontsize=8.5, color=COLORS[1])
    ax.axhline(86.5, color=COLORS[4], ls="-.", lw=1.3)
    ax.text(19.8, 90, r"$T_{rms}$ = 86.5 N m, standstill weight 0.4", ha="right", va="bottom", fontsize=8.5,
            color="#A86F00")
    ax.annotate("peak 180 N m", xy=(2, 180), xytext=(3.2, 150), fontsize=8.5,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    for x, lab in [(1, "accelerate"), (6, "run 60 N m"), (11, "brake"), (16, "standstill")]:
        yy = {1: 132, 6: 40, 11: -30, 16: 10}[x]
        ax.text(x, yy, lab, ha="center", va="center", fontsize=8.5, color=INK,
                rotation=90 if x == 1 else 0)
    ax.set_xlim(0, 20)
    ax.set_ylim(-120, 215)
    ax.set_xticks(range(0, 21, 2))
    ax.set_xlabel("time (s)")
    ax.set_ylabel("motor torque (N m)")
    save(fig, "10", "fig-10-2-duty-cycle-torque")


# ---------------------------------------------------------------- 10.3
def fig_10_3():
    fig, ax = new_fig(6.4, 4.2)
    n = np.linspace(0.001, 1.5, 600)
    # power hyperbolas
    for P in (0.5, 1.0):
        nn = np.linspace(P / 2.0, 1.5, 300)
        ax.plot(nn, P / nn, color="#BBBBBB", lw=0.9, zorder=1)
    ax.text(1.5, 0.5 / 1.5 + 0.03, "P = 0.5", fontsize=7.5, color=GREY, ha="right", va="bottom")
    ax.text(0.27, 1.92, "P = 0.5", fontsize=7.5, color=GREY, ha="left", va="center")
    # constant torque with breakaway
    nb = np.linspace(0, 1.5, 600)
    Tc = 1.0 + 0.3 * np.exp(-nb / 0.025)
    ax.plot(nb, Tc, color=COLORS[0])
    ax.text(0.07, 1.05, "constant torque\n(hoist, conveyor)", fontsize=7.5, color=COLORS[0],
            ha="left", va="bottom")
    ax.text(0.04, 1.29, "breakaway", fontsize=7.5, color=COLORS[0], va="bottom")
    # quadratic
    ax.plot(n, n ** 2, color=COLORS[1])
    ax.text(1.27, 1.86, "quadratic $T\\propto n^2$\n(fan, centrifugal pump)", fontsize=8, color=COLORS[1],
            ha="right", va="center")
    # constant power
    npow = np.linspace(0.5, 1.5, 300)
    ax.plot(npow, np.minimum(1 / npow, 2.0), color=COLORS[2])
    ax.plot([0, 0.5], [2.0, 2.0], color=COLORS[2], ls=":", lw=1.4)
    ax.text(0.66, 1.63, "constant power $T\\propto1/n$\n(winder, spindle)", fontsize=8, color=COLORS[2],
            ha="left", va="center")
    # linear
    ax.plot(n, n, color=COLORS[3])
    ax.text(1.45, 1.36, "linear $T\\propto n$\n(calender, eddy-\ncurrent brake)", fontsize=8, color=COLORS[3],
            ha="left", va="top")
    # pump with static head
    ns = np.linspace(0.5477, 1.5, 300)
    Ts = 0.3 + 0.7 * ns ** 2
    ok = Ts <= 2.0
    ax.plot(ns[ok], Ts[ok], color=COLORS[4], ls="--")
    ax.plot(0.5477, 0.51, "o", color=COLORS[4], ms=4)
    ax.annotate("pump with static head\n$T=0.3+0.7n^2$, flow begins at 0.55",
                xy=(0.5477, 0.51), xytext=(0.08, 0.66), fontsize=8, color="#A86F00",
                arrowprops=dict(arrowstyle="-|>", color="#A86F00", lw=0.8))
    ax.axvline(1.0, color=GREY, lw=0.6, ls=":")
    ax.axhline(1.0, color=GREY, lw=0.6, ls=":")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 2.0)
    ax.set_xlabel("speed (per unit of rated speed)")
    ax.set_ylabel("load torque (per unit of rated torque)")
    save(fig, "10", "fig-10-3-load-characteristics")


# ---------------------------------------------------------------- 10.4
def _hoist(ax, x, y, up, label_dir):
    """Rope drum at (x, y) with a load hanging below; up=True raises."""
    ax.add_patch(Circle((x, y), 0.32, fc="#DDDDDD", ec=INK, lw=1))
    ax.plot([x + 0.32, x + 0.32], [y, y - 1.3], color=INK, lw=1)
    ax.add_patch(Rectangle((x + 0.02, y - 1.85), 0.6, 0.55, fc="#B0B0B0", ec=INK, lw=1))
    ax.text(x + 0.32, y - 1.58, "m", ha="center", va="center", fontsize=7.5)
    dy = 0.6 if up else -0.6
    ax.annotate("", xy=(x + 0.95, y - 1.55 + dy), xytext=(x + 0.95, y - 1.55),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.3))
    ax.text(x + 1.1, y - 1.25, label_dir, fontsize=7, color=COLORS[0], va="center")


def _lift(ax, x, y, car_up, label):
    ax.add_patch(Circle((x, y), 0.3, fc="#DDDDDD", ec=INK, lw=1))
    ax.plot([x - 0.3, x - 0.3], [y, y - 1.0], color=INK, lw=1)
    ax.plot([x + 0.3, x + 0.3], [y, y - 0.7], color=INK, lw=1)
    ax.add_patch(Rectangle((x - 0.6, y - 1.6), 0.6, 0.6, fc="white", ec=INK, lw=1))
    ax.text(x - 0.3, y - 1.3, "car", ha="center", va="center", fontsize=6.5)
    ax.add_patch(Rectangle((x + 0.12, y - 1.25), 0.36, 0.55, fc="#B0B0B0", ec=INK, lw=1))
    ax.text(x + 0.3, y - 1.45, "cw", ha="center", va="top", fontsize=6.5)
    d = 0.55 if car_up else -0.55
    ax.annotate("", xy=(x - 0.85, y - 1.3 + d), xytext=(x - 0.85, y - 1.3),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.3))
    ax.text(x + 0.75, y - 0.9, label, fontsize=7, color=COLORS[0], va="center")


def _power(ax, x, y, into_motor):
    box(ax, x, y, 0.9, 0.5, "supply", fontsize=6.5, fc="#F4F4F4")
    ax.add_patch(Circle((x + 2.05, y + 0.25), 0.27, fc="white", ec=INK, lw=1))
    ax.text(x + 2.05, y + 0.25, "M", ha="center", va="center", fontsize=7.5)
    c = COLORS[2] if into_motor else COLORS[1]
    a, b = (x + 0.95, x + 1.75) if into_motor else (x + 1.75, x + 0.95)
    ax.annotate("", xy=(b, y + 0.25), xytext=(a, y + 0.25),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2, mutation_scale=12, shrinkA=0, shrinkB=0))


def fig_10_4():
    fig, ax = schematic(6.8, 6.4, xlim=(-7.4, 7.4), ylim=(-9.6, 6.6))
    ax.add_patch(Rectangle((0, 0), 7, 6.2, fc=COLORS[2], alpha=0.07, lw=0))
    ax.add_patch(Rectangle((-7, -6.2), 7, 6.2, fc=COLORS[2], alpha=0.07, lw=0))
    ax.add_patch(Rectangle((-7, 0), 7, 6.2, fc=COLORS[1], alpha=0.07, lw=0))
    ax.add_patch(Rectangle((0, -6.2), 7, 6.2, fc=COLORS[1], alpha=0.07, lw=0))
    ax.annotate("", xy=(7.2, 0), xytext=(-7.2, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.annotate("", xy=(0, 6.45), xytext=(0, -6.4), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(7.2, 0.2, "torque $T$", ha="right", va="bottom", fontsize=9)
    ax.text(0.15, 6.4, "speed $\\omega$", ha="left", va="top", fontsize=9)
    # quadrant titles
    ax.text(3.5, 5.7, "I  forward motoring\n$T>0,\\ \\omega>0,\\ P>0$", ha="center", va="top", fontsize=8.5)
    ax.text(-3.5, 5.7, "II  forward braking\n$T<0,\\ \\omega>0,\\ P<0$", ha="center", va="top", fontsize=8.5)
    ax.text(-3.5, -0.4, "III  reverse motoring\n$T<0,\\ \\omega<0,\\ P>0$", ha="center", va="top", fontsize=8.5)
    ax.text(3.5, -0.4, "IV  reverse braking\n$T>0,\\ \\omega<0,\\ P<0$", ha="center", va="top", fontsize=8.5)
    # sketches
    _hoist(ax, 1.4, 3.6, True, "hoist raising\nload")
    _lift(ax, -4.6, 3.6, True, "lift: light car\nrising, heavier\ncounterweight\nfalling;\nor vehicle\ndecelerating")
    _lift(ax, -4.6, -2.5, False, "lift: light car\ndriven down\nagainst heavier\ncounterweight")
    _hoist(ax, 1.4, -2.5, False, "hoist lowering\nheavy load,\ntorque still\nupward")
    # power-flow icons
    _power(ax, 3.9, 1.5, True)
    _power(ax, -3.1, 0.5, False)
    _power(ax, -3.1, -5.6, True)
    _power(ax, 3.9, -5.6, False)
    ax.text(4.95, 2.15, "power to motor", ha="center", fontsize=6.8, color=COLORS[2])
    ax.text(-2.05, 1.15, "power from motor", ha="center", fontsize=6.8, color=COLORS[1])
    ax.text(-2.05, -4.95, "power to motor", ha="center", fontsize=6.8, color=COLORS[2])
    ax.text(4.95, -4.95, "power from motor", ha="center", fontsize=6.8, color=COLORS[1])
    ax.text(7.0, -6.1, "forward = up (hoisting / car rising)", ha="right", va="bottom", fontsize=6.8,
            color=GREY)
    # converter strip
    ax.text(-7.2, -7.0, "Converter coverage", fontsize=9, weight="bold", va="center")

    def quads(x0, y0, cols):
        # mini-plane: order II I / III IV
        pos = {"II": (0, 1), "I": (1, 1), "III": (0, 0), "IV": (1, 0)}
        for q, (cx, cy) in pos.items():
            ax.add_patch(Rectangle((x0 + cx * 0.75, y0 + cy * 0.55), 0.75, 0.55, fc=cols[q], ec=INK, lw=0.8))
            ax.text(x0 + cx * 0.75 + 0.375, y0 + cy * 0.55 + 0.275, q, ha="center", va="center", fontsize=6.8)

    g, o = "#9FD8C4", "#F2B48C"
    quads(-7.2, -8.6, {"I": g, "III": g, "II": o, "IV": o})
    ax.text(-5.5, -8.05, "diode rectifier + inverter\n+ brake chopper: motoring in\nI and III; braking energy of\nII and IV burnt in resistor",
            fontsize=7.5, va="center")
    quads(1.6, -8.6, {"I": g, "III": g, "II": g, "IV": g})
    ax.text(3.3, -8.05, "active front end:\nall four quadrants, braking\nenergy regenerated to the grid",
            fontsize=7.5, va="center")
    ax.add_patch(Rectangle((-7.2, -9.45), 0.4, 0.3, fc=g, ec=INK, lw=0.6))
    ax.text(-6.7, -9.3, "motoring or regenerating", fontsize=7, va="center")
    ax.add_patch(Rectangle((-1.0, -9.45), 0.4, 0.3, fc=o, ec=INK, lw=0.6))
    ax.text(-0.5, -9.3, "braking into resistor", fontsize=7, va="center")
    save(fig, "10", "fig-10-4-four-quadrant-plane")


# ---------------------------------------------------------------- 10.5
def motor_curve():
    """Catalogue-shaped DOL curve (per unit): modified Kloss formula with a stator-resistance
    term q (breakdown 2.6 pu at slip 0.1, 1.0 pu at slip 0.01) plus a deep-bar term s**3.2 that
    lifts the low-speed torque to 2.0 pu at standstill with a pull-up minimum of 1.6 pu near 500 rpm."""
    Tb, sb, q = 2.6, 0.10, 1.53

    def T(n):
        s = np.clip((1500.0 - np.asarray(n, float)) / 1500.0, 1e-9, 1.0)
        return 2 * Tb * (1 + q) / (s / sb + sb / s + 2 * q) + s ** 3.2
    return T


def load_curve(n):
    return 0.78 + 0.22 * np.clip(1 - n / 100, 0, 1) ** 2


def fig_10_5():
    Tm = motor_curve()
    n = np.linspace(0, 1500, 3001)
    fig, ax = new_fig(6.4, 4.0)
    TL = load_curve(n)
    m = Tm(n)
    ax.fill_between(n, TL, m, where=m > TL, color=COLORS[2], alpha=0.18, lw=0)
    ax.plot(n, m, color=COLORS[0], label="motor, direct-on-line")
    ax.plot(n, TL, color=COLORS[1], label="conveyor load")
    ax.plot([0, 1485], [1.26, 1.26], color=COLORS[3], ls="--", lw=1.4)
    ax.text(30, 1.30, "VFD start: motor torque held at 1.26 pu from 0 to rated speed", fontsize=8,
            color=COLORS[3], va="bottom")
    ax.text(700, 1.0, "accelerating torque\n$T_m-T_L$", ha="center", va="center", fontsize=9, color="#00704F")
    # operating point
    from scipy.optimize import brentq
    nop = brentq(lambda x: Tm(x) - 0.78, 1460, 1499)
    ax.plot(nop, 0.78, "o", color=INK, ms=5, zorder=5)
    ax.annotate(f"stable operating point\n{nop:.0f} rpm, 0.78 pu", xy=(nop, 0.78), xytext=(1080, 0.35),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    ax.annotate("locked rotor 2.0", xy=(0, 2.0), xytext=(40, 2.45), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("pull-up 1.6", xy=(500, 1.6), xytext=(420, 2.05), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("breakdown 2.6", xy=(1350, 2.6), xytext=(950, 2.8), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.set_xlim(0, 1520)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel("motor speed (rpm)")
    ax.set_ylabel("torque (per unit of rated torque)")
    ax.legend(loc="lower left", bbox_to_anchor=(0.08, 0.02), fontsize=8.5)
    save(fig, "10", "fig-10-5-motor-load-acceleration")


# ---------------------------------------------------------------- 10.6
RHO_G = 9810.0
Q_D = 0.25


def eta_pump(qeq):
    """Pump efficiency vs full-speed-equivalent flow (fitted: 0.82 at 0.25, 0.74 at 0.175 m3/s)."""
    beta = -12.65
    alpha = 3.28 - 0.25 * beta
    return alpha * qeq + beta * qeq ** 2


def fig_10_6():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.8), gridspec_kw=dict(wspace=0.42))
    Q = np.linspace(0, 0.30, 400)
    a1.plot(Q, 50 - 160 * Q ** 2, color=COLORS[0], label="pump, 100 % speed")
    a1.plot(Q, 32.15 - 160 * Q ** 2, color=COLORS[0], ls="--", label="pump, 80.2 % speed")
    a1.plot(Q, 15 + 400 * Q ** 2, color=COLORS[1], label="system")
    Kt = (45.1 - 15) / 0.175 ** 2
    Qt = Q[Q <= 0.21]
    a1.plot(Qt, 15 + Kt * Qt ** 2, color=COLORS[1], ls=":", lw=1.6, label="system, valve throttled")
    for (q, h, lab, dx, dy) in [(0.25, 40, "design\n(0.25, 40 m)", -0.015, -11),
                                (0.175, 45.1, "A (0.175, 45.1 m)", -0.14, -4.5),
                                (0.175, 27.25, "B (0.175, 27.25 m)", 0.006, -16.5)]:
        a1.plot(q, h, "o", color=INK, ms=4.5, zorder=5)
        a1.annotate(lab, xy=(q, h), xytext=(q + dx, h + dy), fontsize=7.5,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.annotate("", xy=(0.175, 28.2), xytext=(0.175, 44.2),
                arrowprops=dict(arrowstyle="<->", color=COLORS[3], lw=1))
    a1.text(0.18, 36, "valve\nloss", fontsize=7.5, color=COLORS[3])
    a1.set_xlim(0, 0.30)
    a1.set_ylim(0, 55)
    a1.set_xlabel("flow $Q$ (m$^3$/s)")
    a1.set_ylabel("head $H$ (m)")
    a1.legend(fontsize=6.5, loc="lower left", handlelength=1.6)
    a1.set_title("(a) operating points", fontsize=10)

    pct = np.linspace(40, 100, 200)
    q = pct / 100 * Q_D
    # throttling: full speed
    Hthr = 50 - 160 * q ** 2
    Pthr = RHO_G * q * Hthr / eta_pump(q) / 0.955 / 1e3
    # speed control
    Hsys = 15 + 400 * q ** 2
    k = np.sqrt((Hsys + 160 * q ** 2) / 50)
    Pspd = RHO_G * q * Hsys / eta_pump(q / k) / (0.95 * 0.97) / 1e3
    a2.plot(pct, Pthr, color=COLORS[1], label="throttle valve")
    a2.plot(pct, Pspd, color=COLORS[0], label="speed control (VFD)")
    a2.fill_between(pct, Pspd, Pthr, where=Pthr > Pspd, color=COLORS[2], alpha=0.15, lw=0)
    p70t = np.interp(70, pct, Pthr)
    p70s = np.interp(70, pct, Pspd)
    a2.plot([70, 70], [p70s, p70t], "o", color=INK, ms=4)
    a2.axvline(70, color=GREY, lw=0.6, ls=":")
    a2.text(68, p70t + 3, f"{p70t:.0f} kW", ha="right", fontsize=8, color=COLORS[1])
    a2.text(72, p70s - 9, f"{p70s:.0f} kW", ha="left", fontsize=8, color=COLORS[0])
    a2.text(77, (p70t + p70s) / 2 + 2, "saving\n46 kW", fontsize=8, color="#00704F")
    a2.set_xlim(40, 100)
    a2.set_ylim(0, 140)
    a2.set_xlabel("flow (% of design)")
    a2.set_ylabel("electrical input power (kW)")
    a2.legend(fontsize=7.5, loc="upper left")
    a2.set_title("(b) input power", fontsize=10)
    save(fig, "10", "fig-10-6-pump-throttle-vs-speed")


if __name__ == "__main__":
    fig_10_1()
    fig_10_2()
    fig_10_3()
    fig_10_4()
    fig_10_5()
    fig_10_6()
