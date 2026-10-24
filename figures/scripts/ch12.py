"""Figures for Chapter 12 — AC Motor Drives. Run from the repository root: python figures/scripts/ch12.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle, Ellipse, Arc, Polygon  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")
GREY = "#888888"

# ------------------------------------------------------------------ motor and drive data
VDC = 540.0
# 37 kW, 400 V, 50 Hz, four-pole induction motor (Section 12.3), per-phase star equivalent at 50 Hz
R1, R2, X1, X2, XM = 0.080, 0.070, 0.35, 0.35, 11.0
PP_IM = 2


def im_torque(f, vph, s):
    """Electromagnetic torque (N m) from the equivalent circuit at frequency f, phase voltage vph, slip s."""
    k = f / 50.0
    z2 = R2 / s + 1j * X2 * k
    zm = 1j * XM * k
    z = R1 + 1j * X1 * k + zm * z2 / (zm + z2)
    i1 = vph / z
    i2 = i1 * zm / (zm + z2)
    pag = 3 * np.abs(i2) ** 2 * R2 / s
    return pag / (2 * np.pi * f / PP_IM)


# IPM traction motor (Section 12.8)
PSI, LD, LQ, PP_PM, IMAX, RS = 0.065, 0.20e-3, 0.50e-3, 4, 400.0, 0.010
VLIM = 0.95 * 400 / np.sqrt(3)


def pm_torque(i_d, i_q):
    return 1.5 * PP_PM * (PSI * i_q + (LD - LQ) * i_d * i_q)


def pm_volt(we, i_d, i_q):
    vd = RS * i_d - we * LQ * i_q
    vq = RS * i_q + we * (LD * i_d + PSI)
    return np.hypot(vd, vq)


def _hop(ax, x, y, r=0.2, color=INK, lw=1.0, horizontal=True):
    """Small semicircular hop where a horizontal wire crosses a vertical one at (x, y)."""
    ax.add_patch(Rectangle((x - r, y - 0.06), 2 * r, 0.12, fc="white", ec="none", zorder=5))
    t = np.linspace(0, np.pi, 30)
    ax.plot(x - r * np.cos(t), y + r * np.sin(t), color=color, lw=lw, zorder=6)


# ---------------------------------------------------------------- 12.1
def _sw(d, x, ytop, name, diode=True):
    d.add(elm.IgbtN().theta(0).anchor("collector").at((x, ytop)))
    d.add(elm.Label().at((x - 0.8, ytop - 0.45)).label(name, halign="right", fontsize=7.5))
    if diode:
        d.add(elm.Line().at((x, ytop)).to((x + 0.7, ytop)))
        d.add(elm.Line().at((x, ytop - 1.4)).to((x + 0.7, ytop - 1.4)))
        d.add(elm.Diode().up().at((x + 0.7, ytop - 1.4)).to((x + 0.7, ytop)))


def _wave_inset(ax, rect, kind, title):
    ia = ax.inset_axes(rect, transform=ax.transData)
    th = np.linspace(0, 2 * 2 * np.pi, 2000)
    if kind == "rect":
        deg = np.degrees(th) % 360

        def half(dd):
            return np.exp(-((dd - 65) / 17) ** 2) + np.exp(-((dd - 115) / 17) ** 2)
        y = np.where(deg < 180, half(deg), -half(deg - 180))
        ia.plot(th, y, color=COLORS[0], lw=1)
        ia.set_ylim(-1.4, 1.4)
    elif kind == "dc":
        y = 540 + 10 * np.cos(6 * th)
        ia.plot(th, y, color=COLORS[1], lw=1)
        ia.set_ylim(0, 640)

    elif kind == "pwm":
        t = th / (2 * np.pi)
        car = 2 * np.abs(2 * ((t * 15) % 1) - 1) - 1
        sa = np.where(0.9 * np.sin(th) > car, 1, 0)
        sb = np.where(0.9 * np.sin(th - 2 * np.pi / 3) > car, 1, 0)
        ia.plot(th, 540 * (sa - sb), color=COLORS[2], lw=0.6)
        ia.set_ylim(-700, 700)
    else:
        y = np.sin(th - 0.5) + 0.06 * (2 * np.abs(2 * ((th / (2 * np.pi) * 15) % 1) - 1) - 1)
        ia.plot(th, y, color=COLORS[3], lw=1)
        ia.set_ylim(-1.4, 1.4)
    ia.axhline(0, color=GREY, lw=0.4)
    ia.set_xticks([])
    ia.set_yticks([])
    for sp in ia.spines.values():
        sp.set_visible(True)
        sp.set_color("#BBBBBB")
        sp.set_linewidth(0.6)
    ia.set_title(title, fontsize=6.6, pad=2)
    return ia


def fig_12_1():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=2, fontsize=7.5, lw=1.0)
    top, bot = 6.0, 0.0
    ph_y = [4.0, 3.0, 2.0]
    legs_r = [3.4, 4.6, 5.8]
    # supply and line reactors
    for k, y in enumerate(ph_y):
        d.add(elm.Inductor2(loops=3).right().at((0.8, y)).to((2.0, y)))
    # rectifier legs (diodes at the rails, plain wire in the middle)
    for x in legs_r:
        d.add(elm.Diode().up().at((x, top - 1.4)).to((x, top)))
        d.add(elm.Diode().up().at((x, bot)).to((x, bot + 1.4)))
        d.add(elm.Line().at((x, bot + 1.4)).to((x, top - 1.4)))
    # DC link: choke in positive rail, capacitor, voltage sensor
    d.add(elm.Line().at((legs_r[0], top)).to((6.6, top)))
    d.add(elm.Inductor2(loops=3).right().at((6.6, top)).to((8.0, top)).label("DC choke", loc="bottom", fontsize=7))
    d.add(elm.Line().at((8.0, top)).to((19.0, top)))
    d.add(elm.Line().at((legs_r[0], bot)).to((19.0, bot)))
    d.add(elm.Capacitor().down().at((8.8, top)).to((8.8, bot)).label("$C$\n4.7 mF", loc="top", fontsize=7))
    d.add(elm.Dot().at((8.8, top)))
    d.add(elm.Dot().at((8.8, bot)))
    d.add(elm.MeterV().down().at((10.3, top)).to((10.3, bot)))
    d.add(elm.Dot().at((10.3, top)))
    d.add(elm.Dot().at((10.3, bot)))
    # brake chopper
    d.add(elm.Resistor().down().at((12.3, top)).to((12.3, 2.8)).label("$R_{br}$\n(ext.)", loc="bottom", fontsize=7))
    d.add(elm.Line().at((12.3, 2.8)).to((12.3, 1.4)))
    _sw(d, 12.3, 1.4, "S7", diode=False)
    d.add(elm.Dot().at((12.3, top)))
    d.add(elm.Dot().at((12.3, bot)))
    # inverter
    legs_i = [14.2, 16.6, 19.0]
    names = [("S1", "S4"), ("S3", "S6"), ("S5", "S2")]
    for x, (nu, nl) in zip(legs_i, names):
        _sw(d, x, top, nu)
        _sw(d, x, bot + 1.4, nl)
        d.add(elm.Line().at((x, top - 1.4)).to((x, bot + 1.4)))
    d.draw(show=False)
    # ---- wires with hops drawn in matplotlib
    lw = 1.0
    for k, (y, xl) in enumerate(zip(ph_y, legs_r)):
        ax.plot([-0.4, 0.8], [y, y], color=INK, lw=lw)
        xs = [2.0] + [xx for xx in legs_r[:k]] + [xl]
        ax.plot([2.0, xl], [y, y], color=INK, lw=lw)
        for xx in legs_r[:k]:
            _hop(ax, xx, y, r=0.18)
        ax.plot(xl, y, "o", color=INK, ms=3)
        ax.text(-0.5, y, "abc"[k], ha="right", va="center", fontsize=8)
    out_y = [3.6, 3.0, 2.4]
    for k, (y, xl) in enumerate(zip(out_y, legs_i)):
        ax.plot([xl, 22.0], [y, y], color=INK, lw=lw)
        for xx in legs_i[k + 1:]:
            _hop(ax, xx, y, r=0.18)
        ax.plot(xl, y, "o", color=INK, ms=3)
    # current sensors on phases a and b
    for y in out_y[:2]:
        ax.add_patch(Circle((20.5, y), 0.22, fc="none", ec=COLORS[2], lw=1.2, zorder=7))
    ax.annotate("current sensors", xy=(20.55, 2.75), xytext=(21.0, 0.7), fontsize=6.4, color=COLORS[2],
                ha="left", va="center", arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    # cable
    ax.add_patch(Ellipse((21.7, 3.0), 1.2, 2.0, fc="none", ec=GREY, lw=0.9, ls="--"))
    ax.text(21.7, 4.1, "shielded\ncable\n≤ 100 m", fontsize=6.4, ha="center", va="bottom", color=GREY)
    # motor
    mx, my = 23.6, 3.0
    for y in out_y:
        ax.plot([22.0, mx - 0.85], [y, my + (y - my) * 0.5], color=INK, lw=lw)
    ax.add_patch(Circle((mx, my), 0.9, fc="white", ec=INK, lw=1.3, zorder=4))
    ax.text(mx, my, "M\n3~", ha="center", va="center", fontsize=8, zorder=5, linespacing=0.9)
    ax.text(mx + 0.3, my + 1.05, "induction\nmotor\n37 kW", fontsize=6.4, ha="left", va="bottom")
    ax.plot([mx + 0.9, mx + 1.5], [my, my], color=INK, lw=2.2)
    ax.add_patch(Rectangle((mx + 1.5, my - 0.3), 0.45, 0.6, fc="white", ec=INK, lw=0.9))
    ax.text(mx + 1.72, my - 0.45, "encoder\n(optional)", fontsize=6.2, ha="center", va="top")
    # supply label and stage labels
    ax.text(-1.0, 1.4, "400 V\n50 Hz", fontsize=7, ha="center", va="top")
    ax.text(1.4, 4.45, "line reactor\n3 %", fontsize=6.6, ha="center", va="bottom")
    ax.text(4.6, 6.35, "6-diode bridge", fontsize=7, ha="center", va="bottom")
    ax.text(10.3, 6.35, "$V_{dc}$\nsensor", fontsize=6.6, ha="center", va="bottom")
    ax.text(12.5, 6.35, "brake\nchopper", fontsize=6.6, ha="center", va="bottom")
    ax.text(16.9, 6.35, "two-level IGBT inverter", fontsize=7, ha="center", va="bottom")
    ax.text(7.0, -0.35, "DC link ≈ 540 V", fontsize=7, ha="center", va="top")
    # control block and gate signals
    cy = -3.4
    box(ax, 11.0, cy, 9.4, 1.7, "controller\nPWM, current and speed loops,\nprotection", fontsize=6.6,
        fc="#FFF4E0")
    for x in [12.3, 14.2, 16.6, 19.0]:
        ax.annotate("", xy=(x - 0.6, -0.15), xytext=(x - 0.6, cy + 1.7),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9, ls="--", shrinkA=0, shrinkB=0))
    ax.text(15.4, -1.0, "gate signals", fontsize=6.6, color=COLORS[1], ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=0.5))
    sig = dict(color=COLORS[0], lw=0.8, ls=":")
    ax.plot([10.3, 10.3, 11.0], [-0.1, cy + 0.75, cy + 0.75], **sig)
    ax.plot([20.5, 20.5, 20.4], [out_y[1] - 0.22, cy + 0.75, cy + 0.75], **sig)
    ax.plot([mx + 1.72, mx + 1.72, 20.4], [my - 1.1, cy + 0.4, cy + 0.4], **sig)
    ax.text(20.6, cy + 0.85, "$i_a, i_b$", fontsize=6.6, color=COLORS[0], va="bottom")
    ax.text(21.3, cy + 0.3, "speed", fontsize=6.6, color=COLORS[0], va="top")
    ax.text(10.2, cy + 0.85, "$V_{dc}$", fontsize=6.6, color=COLORS[0], va="bottom", ha="right")
    # waveform sketches
    _wave_inset(ax, [-0.6, 7.6, 3.6, 1.6], "rect", "rectifier input current")
    _wave_inset(ax, [6.6, 7.6, 3.6, 1.6], "dc", "DC-link voltage ≈ 540 V")
    _wave_inset(ax, [14.4, 7.6, 3.6, 1.6], "pwm", "inverter line voltage")
    _wave_inset(ax, [20.4, 7.6, 3.6, 1.6], "cur", "motor current")
    ax.set_xlim(-1.6, 25.6)
    ax.set_ylim(-3.6, 9.9)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "12", "fig-12-1-vfd-power-circuit")


# ---------------------------------------------------------------- 12.2
def fig_12_2():
    f, fc, m = 50.0, 1000.0, 0.9
    t = np.linspace(0, 0.02, 40001)
    w = 2 * np.pi * f
    car = 2 * np.abs(2 * ((t * fc + 0.25) % 1) - 1) - 1      # triangle, +-1
    ra = m * np.sin(w * t)
    rb = m * np.sin(w * t - 2 * np.pi / 3)
    rc = m * np.sin(w * t + 2 * np.pi / 3)
    va0 = np.where(ra > car, 1, -1) * VDC / 2
    vb0 = np.where(rb > car, 1, -1) * VDC / 2
    vc0 = np.where(rc > car, 1, -1) * VDC / 2
    vab = va0 - vb0
    van = va0 - (va0 + vb0 + vc0) / 3
    # motor phase current: fundamental 90 A peak at pf 0.88 plus ripple through the leakage inductance
    phi = np.arccos(0.88)
    l_sigma = (X1 + X2) / (2 * np.pi * 50)
    van1 = m * VDC / 2 * np.sin(w * t)
    dt = t[1] - t[0]
    rip = np.cumsum(van - van1) * dt / l_sigma
    rip -= np.polyval(np.polyfit(t, rip, 1), t)
    # the carrier is drawn at 1 kHz for clarity; the ripple is scaled to a typical 4 kHz carrier
    ia = 90 * np.sin(w * t - phi) + rip * 1000 / 4000
    tm = t * 1e3
    fig, axs = plt.subplots(3, 1, figsize=(6.6, 5.0), sharex=True, gridspec_kw=dict(hspace=0.22))
    a0, a1, a2 = axs
    a0.plot(tm, car, color=GREY, lw=0.7, label="carrier, 1 kHz")
    a0.plot(tm, ra, color=COLORS[0], label="reference $a$ ($m$ = 0.9)")
    a0.plot(tm, rb, color=COLORS[1], label="reference $b$")
    a0.set_ylim(-1.15, 1.6)
    a0.set_yticks([-1, 0, 1])
    a0.set_ylabel("per unit")
    a0.legend(loc="upper center", ncol=3, fontsize=7.5, bbox_to_anchor=(0.5, 1.04))
    a1.plot(tm, va0, color=COLORS[0], lw=0.7)
    a1.plot(tm, m * VDC / 2 * np.sin(w * t), color=INK, ls="--", lw=1.4)
    a1.set_ylim(-340, 400)
    a1.set_yticks([-270, 0, 270])
    a1.set_ylabel("$v_{a0}$ (V)")
    a1.text(20.0, 300, "leg voltage ±270 V;  dashed: average $243\\sin\\omega t$", fontsize=7.5, ha="right",
            va="bottom")
    a2.plot(tm, vab, color=COLORS[2], lw=0.6, label="$v_{ab}$ pulses ±540 V")
    v1 = np.sqrt(3) * m * VDC / 2
    a2.plot(tm, v1 * np.sin(w * t + np.pi / 6), color=INK, ls="--", lw=1.4,
            label=f"fundamental, {v1:.0f} V peak ({v1 / np.sqrt(2):.1f} V rms)")
    a2.set_ylim(-700, 1050)
    a2.set_yticks([-540, 0, 540])
    a2.set_ylabel("$v_{ab}$ (V)")
    a2r = a2.twinx()
    a2r.spines["right"].set_visible(True)
    a2r.plot(tm, ia, color=COLORS[1], lw=1.3, label="phase current $i_a$ (90 A peak)")
    a2r.set_ylim(-700 * 90 / 540, 1050 * 90 / 540)
    a2r.set_yticks([-90, 0, 90])
    a2r.set_ylabel("$i_a$ (A)", color=COLORS[1])
    a2r.tick_params(axis="y", colors=COLORS[1])
    h1, l1 = a2.get_legend_handles_labels()
    h2, l2 = a2r.get_legend_handles_labels()
    a2.legend(h1 + h2, l1 + l2, loc="upper center", ncol=3, fontsize=7, bbox_to_anchor=(0.5, 1.05))
    a2.set_xlabel("time (ms)")
    a2.set_xlim(0, 20)
    a2.set_xticks(range(0, 21, 2))
    save(fig, "12", "fig-12-2-sine-triangle-pwm")


# ---------------------------------------------------------------- 12.3
def v_boost(f):
    """Boosted V/f characteristic (line V): 20 V at 0 Hz, 47 V at 5 Hz, meets 8 V/Hz at 15 Hz."""
    f = np.asarray(f, float)
    a, b = 4.7667, 0.12667
    vb = 20 + a * f + b * f ** 2
    return np.where(f < 15, vb, np.minimum(8 * f, 400))


def fig_12_3():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1, 1.35], wspace=0.3))
    f = np.linspace(0, 75, 400)
    a1.plot(f, np.minimum(8 * f, 400), color=COLORS[0], label="linear V/f (8 V/Hz)")
    fb = np.linspace(0, 15, 100)
    a1.plot(fb, v_boost(fb), color=COLORS[1], label="with low-speed boost")
    a1.plot(5, 47, "o", color=COLORS[1], ms=4)
    a1.annotate("(5 Hz, 47 V)", xy=(5, 47), xytext=(10, 20), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.axvline(50, color=GREY, ls=":", lw=0.8)
    a1.text(52, 200, "field\nweakening", fontsize=7.5, va="center")
    a1.set_xlim(0, 75)
    a1.set_ylim(0, 450)
    a1.set_xlabel("frequency (Hz)")
    a1.set_ylabel("line voltage (V)")
    a1.legend(loc="upper left", fontsize=7)
    a1.set_title("(a) voltage-frequency characteristic", fontsize=9.5)
    vph = 400 / np.sqrt(3)
    for k, fr in enumerate([5, 10, 25, 50, 75]):
        v = vph * min(fr, 50) / 50
        ns = 60 * fr / PP_IM
        s = np.linspace(1.0, 1e-4, 1500)
        T = im_torque(fr, v, s)
        n = ns * (1 - s)
        a2.plot(n, T, color=COLORS[k])
        i = T.argmax()
        if fr in (5, 10):
            a2.annotate(f"{fr} Hz, {T[i]:.0f} N m", xy=(n[i], T[i]), xytext=(15, 660 if fr == 5 else 590),
                        ha="left", va="center", fontsize=7, color=COLORS[k],
                        arrowprops=dict(arrowstyle="-", color=COLORS[k], lw=0.6))
        elif fr == 25:
            a2.text(n[i] + 60, T[i] + 5, f"{fr} Hz\n{T[i]:.0f} N m", ha="left", va="bottom", fontsize=7,
                    color=COLORS[k])
        else:
            a2.text(n[i], T[i] + 10, f"{fr} Hz\n{T[i]:.0f} N m", ha="center", va="bottom", fontsize=7,
                    color=COLORS[k])
    a2.axhline(240, color=INK, lw=0.8, ls="--")
    a2.text(2240, 246, "rated torque 240 N m", fontsize=7, ha="right", va="bottom")
    for fr, nop in [(25, 720), (50, 1471)]:
        a2.plot(nop, 240, "o", color=INK, ms=4, zorder=5)
    a2.annotate("720 rpm\n(sync. 750)", xy=(720, 240), xytext=(430, 130), fontsize=7,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a2.annotate("1471 rpm\n(sync. 1500)", xy=(1471, 240), xytext=(1100, 130), fontsize=7,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))

    a2.set_xlim(0, 2250)
    a2.set_ylim(0, 720)
    a2.set_xlabel("speed (rpm)")
    a2.set_ylabel("torque (N m)")
    a2.set_title("(b) torque-speed curves, pure V/f", fontsize=9.5)
    save(fig, "12", "fig-12-3-vf-control")


# ---------------------------------------------------------------- 12.4
def _vec(ax, x1, y1, color, lw=2.0, x0=0.0, y0=0.0, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=12))


def fig_12_4():
    fig = plt.figure(figsize=(6.8, 4.0))
    ax = fig.add_axes([0.0, 0.0, 0.64, 1.0])
    ax2 = fig.add_axes([0.66, 0.1, 0.33, 0.8])
    th = np.radians(40)
    # phase axes b, c (phase a coincides with alpha)
    for ang, lab in [(120, "b"), (240, "c")]:
        r = np.radians(ang)
        ax.plot([0, 74 * np.cos(r)], [0, 74 * np.sin(r)], color="#CCCCCC", lw=0.9, ls="--")
        ax.text(79 * np.cos(r), 79 * np.sin(r), lab, color=GREY, fontsize=8, ha="center", va="center")
    _vec(ax, 112, 0, INK, lw=1.0, x0=-50)
    _vec(ax, 0, 108, INK, lw=1.0, y0=-50)
    ax.text(112, -4, r"$\alpha$ (phase a)", fontsize=9, ha="right", va="top")
    ax.text(-3, 108, r"$\beta$", fontsize=11, ha="right", va="top")
    # d and q axes
    ax.plot([-30 * np.cos(th), 104 * np.cos(th)], [-30 * np.sin(th), 104 * np.sin(th)], color=COLORS[2], lw=1.1)
    ax.text(108 * np.cos(th), 108 * np.sin(th), "$d$", color=COLORS[2], fontsize=11, ha="center", va="center")
    tq = th + np.pi / 2
    ax.plot([-30 * np.cos(tq), 104 * np.cos(tq)], [-30 * np.sin(tq), 104 * np.sin(tq)], color=COLORS[2], lw=1.1)
    ax.text(108 * np.cos(tq), 108 * np.sin(tq), "$q$", color=COLORS[2], fontsize=11, ha="center", va="center")
    # rotor flux (own scale) on the d-axis
    Lpsi = 60
    _vec(ax, Lpsi * np.cos(th), Lpsi * np.sin(th), COLORS[1], lw=2.4)
    ax.text(Lpsi * np.cos(th) - 6, Lpsi * np.sin(th) + 2, r"$\psi_r$ = 0.971 Wb", color=COLORS[1], fontsize=8.5,
            ha="right", va="bottom")
    # stator current and its components
    gam = th + np.radians(72)
    Is, i_d, i_q = 89.9, 27.7, 85.5
    ix, iy = Is * np.cos(gam), Is * np.sin(gam)
    dx, dy = i_d * np.cos(th), i_d * np.sin(th)
    qx, qy = i_q * np.cos(tq), i_q * np.sin(tq)
    ax.plot([ix, dx], [iy, dy], color=COLORS[0], ls="--", lw=0.9)
    ax.plot([ix, qx], [iy, qy], color=COLORS[0], ls="--", lw=0.9)
    _vec(ax, dx, dy, COLORS[0], lw=1.5)
    _vec(ax, qx, qy, COLORS[0], lw=1.5)
    _vec(ax, ix, iy, COLORS[0], lw=2.4)
    ax.text(ix + 2, iy + 3, r"$\vec i_s$ = 89.9 A", color=COLORS[0], fontsize=9, ha="center", va="bottom")
    ax.text(dx + 5, dy - 1, "$i_d$ = 27.7 A", color=COLORS[0], fontsize=8, va="top")
    ax.text(qx - 4, qy - 2, "$i_q$ = 85.5 A", color=COLORS[0], fontsize=8, ha="right", va="top")
    # angles
    ax.add_patch(Arc((0, 0), 30, 30, theta1=0, theta2=40, color=INK, lw=0.8))
    ax.text(17, 2, r"$\theta$ = 40°", fontsize=7.5, va="bottom")
    ax.add_patch(Arc((0, 0), 40, 40, theta1=40, theta2=112, color=COLORS[0], lw=0.8))
    ax.text(22 * np.cos(np.radians(70)), 22 * np.sin(np.radians(70)), "72°", fontsize=7.5, color=COLORS[0],
            ha="left", va="bottom")
    # rotation of the d-q frame
    ax.add_patch(Arc((0, 0), 2 * 92, 2 * 92, theta1=25, theta2=36, color=COLORS[2], lw=1.3))
    a_end = np.radians(36)
    ax.annotate("", xy=(92 * np.cos(a_end), 92 * np.sin(a_end)),
                xytext=(92 * np.cos(a_end - 0.02), 92 * np.sin(a_end - 0.02)),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=1.2, mutation_scale=10))
    ax.text(88, 50, "$\\omega_e$: d–q frame\nrotates with $\\psi_r$",
            color=COLORS[2], fontsize=7.5, ha="left", va="center")
    # rotor axis and slip
    thr = np.radians(30)
    ax.plot([0, 70 * np.cos(thr)], [0, 70 * np.sin(thr)], color=COLORS[3], lw=1.2, ls=(0, (4, 2)))
    ax.add_patch(Arc((0, 0), 2 * 50, 2 * 50, theta1=30, theta2=40, color=COLORS[3], lw=1.2))
    ax.text(72 * np.cos(thr) + 1, 72 * np.sin(thr) - 1, "rotor axis", color=COLORS[3], fontsize=7.5, va="top")
    ax.annotate("flux ahead of rotor:\nslip $\\omega_{sl}$ = 5.97 rad/s",
                xy=(50 * np.cos(np.radians(33)), 50 * np.sin(np.radians(33))), xytext=(56, -22), fontsize=7.5,
                color=COLORS[3], ha="left", va="center", arrowprops=dict(arrowstyle="-", color=COLORS[3], lw=0.6))
    ax.text(128, -78, "grey dashed: phase axes b, c\ncurrents to scale (A);\n$\\psi_r$ to its own scale", fontsize=7, color=GREY, ha="right",
            va="bottom")
    ax.set_xlim(-110, 130)
    ax.set_ylim(-82, 118)
    ax.set_aspect("equal")
    ax.axis("off")
    # inset: inverter voltage vectors
    Vv = 2 * VDC / 3
    hexa = [(Vv * np.cos(np.radians(60 * k)), Vv * np.sin(np.radians(60 * k))) for k in range(6)]
    ax2.add_patch(Polygon(hexa, closed=True, fc="#EEF3F8", ec=INK, lw=1))
    ax2.add_patch(Circle((0, 0), VDC / np.sqrt(3), fc="none", ec=COLORS[1], lw=1.2, ls="--"))
    for k, (x, y) in enumerate(hexa):
        _vec(ax2, x, y, COLORS[0], lw=1.2)
        ax2.text(1.15 * x, 1.15 * y, f"$V_{k + 1}$", fontsize=8.5, ha="center", va="center")
    ax2.plot(0, 0, "o", color=INK, ms=3)
    ax2.text(18, -14, "$V_0, V_7$", fontsize=7, ha="left", va="top")
    a30 = np.radians(-30)
    ax2.annotate("", xy=(VDC / np.sqrt(3) * np.cos(a30), VDC / np.sqrt(3) * np.sin(a30)), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9))
    ax2.text(120, -120, "312 V", fontsize=7.5, color=COLORS[1], ha="center", va="top")
    ax2.text(0, -440, "$|V_k| = 2V_{dc}/3$ = 360 V\nlinear limit (circle):\n$V_{dc}/\\sqrt{3}$ = 312 V",
             fontsize=7.2, ha="center", va="top")
    ax2.set_title("inverter voltage vectors\n($V_{dc}$ = 540 V)", fontsize=8.5)
    ax2.set_xlim(-430, 430)
    ax2.set_ylim(-640, 430)
    ax2.set_aspect("equal")
    ax2.axis("off")
    save(fig, "12", "fig-12-4-space-vector-dq")


# ---------------------------------------------------------------- 12.5
def _sum(ax, x, y, r=0.3, minus=()):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.plot([x - r * 0.55, x + r * 0.55], [y, y], color=INK, lw=0.8, zorder=4)
    ax.plot([x, x], [y - r * 0.55, y + r * 0.55], color=INK, lw=0.8, zorder=4)
    for dx, dy in minus:
        ax.text(x + dx, y + dy, "−", fontsize=8.5, ha="center", va="center", zorder=4)


def _ln(ax, pts, color=INK, arrow_end=True, ls="-", lw=1.0):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls)
    if arrow_end:
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9, shrinkA=0, shrinkB=0))


def _vhop(ax, x, y, r=0.22):
    """Vertical wire at x hopping over a horizontal wire at y."""
    ax.add_patch(Rectangle((x - 0.07, y - r), 0.14, 2 * r, fc="white", ec="none", zorder=5))
    t = np.linspace(-np.pi / 2, np.pi / 2, 30)
    ax.plot(x + r * np.cos(t), y + r * np.sin(t), color=INK, lw=1.0, zorder=6)


def fig_12_5():
    fig, ax = schematic(6.8, 4.9, xlim=(0, 25.7), ylim=(0.4, 18.4))
    fs = 6.4
    pi_fc, pl_fc = "#FFF4E0", "#EEF3F8"
    bh = 1.5

    def blk(x0, x1, y, text, fc=pl_fc, h=bh, size=fs):
        box(ax, x0, y - h / 2, x1 - x0, h, text, fc=fc, fontsize=size)

    yq, yd = 15.6, 12.0
    xsq, xsd = 12.6, 11.6         # q and d current summing junctions
    # ---- speed loop and q-axis reference
    ax.text(0.1, yq + 0.15, r"$\omega^{*}$", fontsize=9.5, va="bottom")
    _ln(ax, [(0.1, yq), (1.1, yq)])
    _sum(ax, 1.4, yq, minus=[(-0.45, -0.5)])
    blk(1.9, 4.1, yq, "speed PI", fc=pi_fc)
    _ln(ax, [(1.7, yq), (1.9, yq)])
    ax.text(3.0, yq + bh / 2 + 0.1, "bandwidth\n50 Hz", fontsize=6.2, ha="center", va="bottom", color=GREY)
    _ln(ax, [(4.1, yq), (4.9, yq)])
    ax.text(4.5, yq + 0.1, "$T^{*}$", fontsize=8.5, ha="center", va="bottom")
    blk(4.9, 8.5, yq, "$\\div\\ \\dfrac{1.5\\,p_p L_m \\psi_r^{*}}{L_r}$", size=fs + 0.8, h=1.9)
    _ln(ax, [(8.5, yq), (9.0, yq)])
    blk(9.0, 10.2, yq, "")
    ax.plot([9.15, 9.4, 9.8, 10.05], [yq - 0.4, yq - 0.4, yq + 0.4, yq + 0.4], color=INK, lw=1)
    ax.text(9.6, yq + bh / 2 + 0.1, "current\nlimit", fontsize=6.2, ha="center", va="bottom")
    _ln(ax, [(10.2, yq), (xsq - 0.3, yq)])
    ax.text(11.3, yq + 0.1, "$i_q^{*}$", fontsize=8.5, ha="center", va="bottom")
    _sum(ax, xsq, yq, minus=[(0.45, -0.5)])
    blk(13.2, 14.6, yq, "PI $i_q$", fc=pi_fc)
    _ln(ax, [(xsq + 0.3, yq), (13.2, yq)])
    ax.text(13.9, yq + bh / 2 + 0.1, "current loops\n1 kHz bandwidth", fontsize=6.2, ha="center", va="bottom",
            color=GREY)
    _sum(ax, 15.3, yq)
    _ln(ax, [(14.6, yq), (15.0, yq)])
    _ln(ax, [(15.6, yq), (16.6, yq)])
    ax.text(16.1, yq + 0.1, "$v_q^{*}$", fontsize=8, ha="center", va="bottom")
    # ---- flux and d-axis reference
    ax.text(2.4, yd + 0.15, "$\\psi_r^{*}$ = 0.971 Wb", fontsize=7, va="bottom")
    ax.text(2.4, yd - 0.2, "(reduced in field weakening)", fontsize=6.0, va="top", color=GREY)
    _ln(ax, [(2.4, yd), (8.5, yd)])
    blk(8.5, 9.8, yd, "$1/L_m$", size=fs + 1.0)
    _ln(ax, [(9.8, yd), (xsd - 0.3, yd)])
    ax.text(10.55, yd + 0.1, "$i_d^{*}$", fontsize=8.5, ha="center", va="bottom")
    ax.text(10.55, yd - 0.15, "27.7 A", fontsize=6.4, ha="center", va="top")
    _sum(ax, xsd, yd, minus=[(0.45, -0.5)])
    blk(13.2, 14.6, yd, "PI $i_d$", fc=pi_fc)
    _ln(ax, [(xsd + 0.3, yd), (13.2, yd)])
    _sum(ax, 15.3, yd)
    _ln(ax, [(14.6, yd), (15.0, yd)])
    _ln(ax, [(15.6, yd), (16.6, yd)])
    ax.text(16.1, yd + 0.1, "$v_d^{*}$", fontsize=8, ha="center", va="bottom")
    # decoupling feed-forward
    ym = (yq + yd) / 2
    blk(14.3, 16.3, ym, "decoupling\nterms", size=6.0, h=1.2)
    _ln(ax, [(15.3, ym + 0.6), (15.3, yq - 0.3)])
    _ln(ax, [(15.3, ym - 0.6), (15.3, yd + 0.3)])
    # ---- inverse Park, SVPWM, inverter, motor
    hp = yq - yd + 1.6
    blk(16.6, 18.4, ym, "inverse\nPark\n($\\theta$)", h=hp, size=6.0)
    _ln(ax, [(18.4, 14.4), (19.2, 14.4)])
    _ln(ax, [(18.4, 13.2), (19.2, 13.2)])
    ax.text(18.8, 14.5, "$v_\\alpha^{*}$", fontsize=7.5, ha="center", va="bottom")
    ax.text(18.8, 13.1, "$v_\\beta^{*}$", fontsize=7.5, ha="center", va="top")
    blk(19.2, 21.0, 13.8, "SVPWM", h=2.4, size=6.0)
    _ln(ax, [(21.0, 13.8), (21.4, 13.8)])
    blk(21.4, 23.2, 13.8, "inverter\n$V_{dc}$\n540 V", h=2.4, size=6.0)
    mx, my = 24.6, 13.8
    _ln(ax, [(23.2, 13.8), (mx - 0.9, 13.8)], lw=1.6)
    ax.add_patch(Circle((mx, my), 0.9, fc="white", ec=INK, lw=1.2, zorder=3))
    ax.text(mx, my, "IM\n37 kW", ha="center", va="center", fontsize=6.4, zorder=4)
    ax.plot([mx, mx], [my - 0.9, 11.6], color=INK, lw=2.0)
    box(ax, mx - 0.6, 10.8, 1.2, 0.8, "enc.", fontsize=6.2)
    # ---- current feedback: sensors -> Clarke -> Park -> id, iq
    yc = 8.6
    ax.plot(23.5, 13.8, "o", color=INK, ms=3)
    _ln(ax, [(23.5, 13.8), (23.5, yc), (22.6, yc)])
    ax.text(23.35, 10.2, "$i_a, i_b$", fontsize=7.5, va="center", ha="right")
    blk(20.6, 22.6, yc, "Clarke", h=1.3)
    _ln(ax, [(20.6, yc), (18.4, yc)])
    blk(16.6, 18.4, yc, "Park\n($\\theta$)", h=1.5, size=6.0)
    _ln(ax, [(16.6, yc + 0.35), (xsq, yc + 0.35), (xsq, yq - 0.3)])
    _ln(ax, [(16.6, yc - 0.35), (xsd, yc - 0.35), (xsd, yd - 0.3)])
    _vhop(ax, xsq, yd)
    ax.text(14.5, yc + 0.45, "$i_q$", fontsize=8, va="bottom")
    ax.text(14.5, yc - 0.45, "$i_d$", fontsize=8, va="top")
    # ---- flux angle: encoder -> x pp -> + slip -> integrator -> theta
    yt = 5.0
    _ln(ax, [(mx, 10.8), (mx, yt), (23.2, yt)])
    ax.text(mx + 0.15, 7.4, "$\\omega_r$", fontsize=8.5, va="center")
    blk(21.6, 23.2, yt, "$\\times p_p$", size=fs + 1.2)
    _ln(ax, [(21.6, yt), (21.0, yt)])
    _sum(ax, 20.7, yt)
    blk(18.6, 19.9, yt, "$\\int dt$", size=fs + 1.2)
    _ln(ax, [(20.4, yt), (19.9, yt)])
    ax.text(20.15, yt + 0.1, "$\\omega_e$", fontsize=7.5, ha="center", va="bottom")
    ax.plot([18.6, 17.5], [yt, yt], color=INK, lw=1.0)
    ax.text(18.05, yt + 0.1, "$\\theta$", fontsize=8.5, ha="center", va="bottom")
    _ln(ax, [(17.5, yt), (17.5, yc - 0.75)])
    ax.plot(17.5, 6.6, "o", color=INK, ms=3)
    _ln(ax, [(17.5, 6.6), (19.5, 6.6), (19.5, 10.4), (17.5, 10.4), (17.5, ym - hp / 2)])
    _vhop(ax, 19.5, yc)
    # slip calculator
    blk(14.2, 23.7, 2.8, "slip calc.:  $\\omega_{sl} = L_m i_q^{*} / (\\tau_r \\psi_r^{*})$,  "
        "$\\tau_r$ = 0.516 s", h=1.3, size=fs + 0.3)
    _ln(ax, [(20.7, 3.45), (20.7, yt - 0.3)])
    ax.text(20.85, 3.9, "$\\omega_{sl}$", fontsize=7.5, va="center")
    _ln(ax, [(12.9, 2.8), (14.2, 2.8)])
    ax.text(12.8, 2.8, "$i_q^{*}$, $\\psi_r^{*}$", fontsize=7.5, ha="right", va="center")
    # ---- speed feedback to the speed summing junction
    ys = 1.1
    _ln(ax, [(mx, yt), (mx, ys), (1.4, ys), (1.4, yq - 0.3)])
    ax.text(7.0, ys + 0.1, "measured rotor speed $\\omega$ (encoder)", fontsize=7, va="bottom")
    save(fig, "12", "fig-12-5-foc-block-diagram")


# ---------------------------------------------------------------- 12.6
def pm_capability(rpm):
    we = rpm * 2 * np.pi / 60 * PP_PM
    ids = np.linspace(-400, 0, 401)
    iqs = np.linspace(0, 400, 401)
    ID, IQ = np.meshgrid(ids, iqs)
    ok = (np.hypot(ID, IQ) <= IMAX) & (pm_volt(we, ID, IQ) <= VLIM)
    TT = np.where(ok, pm_torque(ID, IQ), 0.0)
    return TT.max()


def fig_12_6():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.5), gridspec_kw=dict(width_ratios=[1, 1.05], wspace=0.4))
    # (a) current plane
    t = np.linspace(np.pi / 2, np.pi, 200)
    a1.plot(IMAX * np.cos(t), IMAX * np.sin(t), color=INK, lw=1.4, label="current limit 400 A")
    # MTPA trajectory
    mt = []
    for I in np.linspace(1, IMAX, 120):
        r = minimize_scalar(lambda b: -pm_torque(-I * np.sin(b), I * np.cos(b)), bounds=(0, 1.2), method="bounded")
        mt.append((-I * np.sin(r.x), I * np.cos(r.x)))
    mt = np.array([(0, 0)] + mt)
    a1.plot(mt[:, 0], mt[:, 1], color=COLORS[1], lw=1.8, label="MTPA")
    # voltage-limit contours (stator resistance included)
    ids = np.linspace(-450, 50, 501)
    iqs = np.linspace(0, 450, 451)
    ID, IQ = np.meshgrid(ids, iqs)
    for k, (rpm, ls) in enumerate([(3170, "-"), (4500, "--"), (6340, "-.")]):
        we = rpm * 2 * np.pi / 60 * PP_PM
        cs = a1.contour(ID, IQ, pm_volt(we, ID, IQ), levels=[VLIM], colors=[COLORS[0]], linestyles=[ls],
                        linewidths=1.2)
    for lab, yy in [("3170 rpm", 300), ("4500 rpm", 186), ("6340 rpm", 82)]:
        a1.text(45, yy, lab, fontsize=6.4, color=COLORS[0], ha="right", va="bottom",
                bbox=dict(fc="white", ec="none", pad=0.3))

    # constant-torque contours
    for Tc in (100, 170, 263):
        idv = np.linspace(-450, 50, 400)
        iqv = Tc / (1.5 * PP_PM * (PSI + (LD - LQ) * idv))
        a1.plot(idv, iqv, color=COLORS[2], lw=0.8, ls=":")
        xl = {100: -300, 170: -110, 263: -330}[Tc]
        a1.text(xl, Tc / (1.5 * PP_PM * (PSI + (LD - LQ) * xl)), f"{Tc} N m", fontsize=6.4, color=COLORS[2],
                ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.3))
    a1.plot(-234, 325, "o", color=INK, ms=4, zorder=5)
    a1.annotate("MTPA point\n(−234, 325) A", xy=(-234, 325), xytext=(-340, 418), fontsize=6.6, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.text(-120, 120, "MTPA", fontsize=7, color=COLORS[1], ha="center", rotation=-52)
    a1.text(-395, 300, "400 A", fontsize=6.6, color=INK, ha="left")
    a1.plot(-366, 162, "o", color=INK, ms=4, zorder=5)
    a1.annotate("(−366, 162) A", xy=(-366, 162), xytext=(-440, 40), fontsize=6.6,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    a1.plot(-325, 0, "x", color=COLORS[0], ms=6, mew=1.5)
    a1.text(-300, 10, "centre (−325, 0)", fontsize=6.4, ha="left", va="bottom", color=COLORS[0])
    a1.set_xlim(-450, 50)
    a1.set_ylim(0, 450)
    a1.set_aspect("equal")
    a1.set_xlabel("$i_d$ (A)")
    a1.set_ylabel("$i_q$ (A)")
    a1.set_title("(a) current plane (blue: voltage limits)", fontsize=9)

    # (b) capability
    rpm = np.concatenate([np.linspace(0, 3000, 7), np.linspace(3050, 12000, 90)])
    T = np.array([min(pm_capability(r), 263.2) for r in rpm])
    P = T * rpm * 2 * np.pi / 60 / 1e3
    a2.plot(rpm, T, color=COLORS[0], label="torque")
    a2.set_xlim(0, 12500)
    a2.set_ylim(0, 300)
    a2.set_xlabel("speed (rpm)")
    a2.set_ylabel("torque (N m)", color=COLORS[0])
    a2.tick_params(axis="y", colors=COLORS[0])
    a2r = a2.twinx()
    a2r.spines["right"].set_visible(True)
    a2r.plot(rpm, P, color=COLORS[1], label="power")
    a2r.set_ylim(0, 130)
    a2r.set_ylabel("power (kW)", color=COLORS[1])
    a2r.tick_params(axis="y", colors=COLORS[1])
    for x in (3170, 6340):
        a2.axvline(x, color=GREY, lw=0.6, ls=":")
    a2.axvline(12000, color=INK, lw=0.9, ls="--")
    a2.text(11900, 290, "max speed\n12 000 rpm", fontsize=6.8, ha="right", va="top")
    a2.plot(3170, 263, "o", color=COLORS[0], ms=4)
    a2.plot(6340, 170, "o", color=COLORS[0], ms=4)
    a2.text(3300, 268, "263 N m", fontsize=7, color=COLORS[0], va="bottom")
    a2.text(6450, 175, "170 N m", fontsize=7, color=COLORS[0], va="bottom")
    a2r.plot(3170, 87, "o", color=COLORS[1], ms=4)
    a2r.plot(6340, 113, "o", color=COLORS[1], ms=4)
    a2r.text(3300, 82, "87 kW", fontsize=7, color=COLORS[1], va="top")
    a2r.text(6450, 116, "113 kW", fontsize=7, color=COLORS[1], va="bottom")
    a2.text(3170, 8, "base\n3170", fontsize=6.6, ha="center", va="bottom", color=GREY)
    a2.text(6340, 8, "6340", fontsize=6.6, ha="center", va="bottom", color=GREY)
    a2.axvspan(8480, 12500, color=COLORS[3], alpha=0.08, lw=0)
    a2.set_xticks([0, 3000, 6000, 9000, 12000])
    a2.text(8650, 192, "open-circuit\nback-EMF\n566 V (line\npeak) at\n12 000 rpm;\nexceeds $V_{dc}$\n= 400 V above\n≈ 8500 rpm",
            fontsize=6.0, va="center", color="#8A3F6E")
    a2.set_title("(b) torque and power capability", fontsize=9.5)
    save(fig, "12", "fig-12-6-pmsm-mtpa-field-weakening")


if __name__ == "__main__":
    fig_12_1()
    fig_12_2()
    fig_12_3()
    fig_12_4()
    fig_12_5()
    fig_12_6()
