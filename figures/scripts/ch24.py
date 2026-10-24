"""Figures for Chapter 24 — High-Voltage Engineering.

Run from the repository root:  python figures/scripts/ch24.py
"""
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon, FancyBboxPatch
from matplotlib.ticker import FuncFormatter
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, fsolve
import schemdraw
import schemdraw.elements as elm

from figstyle import new_fig, save, COLORS, INK

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

CH = "24"


def _smoothstep(x, x0, x1):
    u = np.clip((x - x0) / (x1 - x0), 0, 1)
    return u * u * (3 - 2 * u)


def _draw(d):
    d.draw(show=False)


# ----------------------------------------------------------------------------
# Figure 24.1 — Paschen curves and long-gap saturation
# ----------------------------------------------------------------------------
def _paschen(pd, pdm, vmin, k_right, p0, p1):
    """Townsend-type curve with minimum vmin at pdm, bent smoothly (between p0 and p1 Pa m) onto
    k_right x the uniform-field air fit U = 24.4 dd + 6.53 sqrt(dd) kV (dd in cm at 20 C)."""
    pd = np.asarray(pd, dtype=float)
    arg = np.log(pd / pdm) + 1
    with np.errstate(divide="ignore", invalid="ignore"):
        vt = np.where(arg > 0.01, vmin * (pd / pdm) / arg, np.nan)
        x = pd / 1013.25
        ve = k_right * (24.4 * x + 6.53 * np.sqrt(x)) * 1e3
        w = _smoothstep(np.log10(pd), np.log10(p0), np.log10(p1))
        return vt * np.exp(w * np.log(ve / vt))


def paschen_air(pd):
    """Air: minimum about 330 V at 0.75 Pa m; right branch the empirical uniform-field fit."""
    return _paschen(pd, 0.75, 330.0, 1.0, 0.75, 5.0)


def paschen_sf6(pd):
    """SF6: minimum about 500 V near 0.35 Pa m; right branch 2.9 x air (89 kV/(cm bar))."""
    return _paschen(pd, 0.35, 500.0, 2.9, 0.35, 3.0)


def fig_24_1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.32))
    pd = np.logspace(-2, 3, 2000)
    va = paschen_air(pd)
    vs = paschen_sf6(pd)
    ax1.plot(pd, va, color=COLORS[0], label="air")
    ax1.plot(pd, vs, color=COLORS[1], ls="--", label="SF$_6$")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim(1e-2, 1e3)
    ax1.set_ylim(100, 1e6)
    ax1.grid(True, which="major", lw=0.5)
    i = np.nanargmin(va)
    ax1.plot([pd[i]], [va[i]], "o", color=COLORS[0], ms=4)
    ax1.annotate(f"air minimum ≈ {va[i]:.0f} V\nat {pd[i]:.2f} Pa·m", xy=(pd[i], va[i]), xytext=(1.8, 125),
                 fontsize=7.5, color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[0]))
    j = np.nanargmin(vs)
    ax1.plot([pd[j]], [vs[j]], "o", color=COLORS[1], ms=4)
    ax1.annotate(f"SF$_6$ min.\n≈ {vs[j]:.0f} V", xy=(pd[j], vs[j]), xytext=(0.012, 170),
                 fontsize=7.5, color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    v1 = paschen_air(1013.25)
    ax1.plot([1000], [v1], "s", color=INK, ms=4.5, zorder=5, clip_on=False)
    ax1.annotate(f"1 cm at 1 bar\n($pd$ ≈ 10$^3$ Pa·m):\nair {v1 / 1e3:.1f} kV", xy=(1000, v1), xytext=(8, 1.1e5),
                 fontsize=7.5,
                 arrowprops=dict(arrowstyle="-", lw=0.7))
    ax1.text(200, 1.5e3, "SF$_6$ ≈ 2.9 × air", fontsize=7.5, color=COLORS[1], ha="center")
    vv = paschen_air(10.13)
    ax1.plot([10.13], [vv], "^", color=INK, ms=4.5, zorder=5)
    ax1.annotate(f"0.1 mm void\nat 1 bar: ≈ 0.9 kV", xy=(10.13, vv), xytext=(14, 280), fontsize=7.5,
                 arrowprops=dict(arrowstyle="-", lw=0.7))
    ax1.set_xlabel("$pd$ (Pa·m)")
    ax1.set_ylabel("Breakdown voltage (V)")
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: {1e2: "100 V", 1e3: "1 kV", 1e4: "10 kV",
                                                              1e5: "100 kV", 1e6: "1 MV"}.get(v, "")))
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax1.legend(loc="upper left", fontsize=8)
    ax1.set_title("(a) Paschen curves, uniform field", fontsize=9.5, loc="left")

    d = np.linspace(0.05, 15, 400)
    u50 = 3400 / (1 + 8 / d)
    ax2.plot(d, u50 / 1e3, color=COLORS[0], label="positive switching impulse,\nrod–plane $U_{50}=3400/(1+8/d)$ kV")
    dl = np.linspace(0, 5, 10)
    ax2.plot(dl, 0.5 * dl, "--", color=COLORS[1], label="lightning impulse, rod–plane\n≈ 500 kV/m")
    for dd in (2, 5, 10):
        uu = 3400 / (1 + 8 / dd)
        ax2.plot([dd], [uu / 1e3], "o", color=COLORS[0], ms=4.5, zorder=5)
        ax2.text(dd + 0.25, uu / 1e3 - 0.08, f"{uu:.0f} kV", fontsize=7.5, va="top", color=COLORS[0])
    ax2.annotate("doubling 5 → 10 m\nadds only 44 %", xy=(10, 1.889), xytext=(9.0, 0.75), fontsize=7.5,
                 ha="center", arrowprops=dict(arrowstyle="-", lw=0.7))
    ax2.set_xlim(0, 15)
    ax2.set_ylim(0, 2.5)
    ax2.set_xlabel("Gap length $d$ (m)")
    ax2.set_ylabel("$U_{50}$ (MV)")
    ax2.grid(True, lw=0.5)
    ax2.legend(loc="upper left", fontsize=7.2)
    ax2.set_title("(b) Long rod–plane gaps (saturation)", fontsize=9.5, loc="left")
    save(fig, CH, "fig-24-1-paschen-curves")


# ----------------------------------------------------------------------------
# Figure 24.2 — partial discharge in a void
# ----------------------------------------------------------------------------
def fig_24_2():
    fig = plt.figure(figsize=(6.8, 5.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.15], height_ratios=[1, 1.05], wspace=0.08, hspace=0.12)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    axc = fig.add_subplot(gs[1, 0])
    axd = fig.add_subplot(gs[1, 1])

    # (a) cross-section
    ax = axa
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-1.0, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 4.0), 6, 0.45, fc="#B0B0B0", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((0, 0.0), 6, 0.45, fc="#B0B0B0", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((0, 0.45), 6, 3.55, fc="#FFF4D6", ec="none"))
    ax.text(3.0, 4.6, "HV electrode", ha="center", va="bottom", fontsize=8)
    ax.text(3.0, -0.1, "earthed electrode", ha="center", va="top", fontsize=8)
    # void (thickness exaggerated)
    vx0, vx1, vy0, vy1 = 2.0, 4.0, 2.05, 2.4
    ax.add_patch(FancyBboxPatch((vx0, vy0), vx1 - vx0, vy1 - vy0, boxstyle="round,pad=0,rounding_size=0.17",
                                fc="white", ec=COLORS[1], lw=1.3, zorder=3))
    # field lines: uniform in the solid, denser (x 2.3) inside the void
    for x in np.arange(0.4, 6.0, 0.5):
        ax.plot([x, x], [0.45, 4.0], color=COLORS[0], lw=0.7, zorder=2)
    for x in np.arange(vx0 + 0.12, vx1 - 0.05, 0.5 / 2.3):
        ax.plot([x, x], [vy0 + 0.02, vy1 - 0.02], color=COLORS[1], lw=0.9, zorder=4)
    ax.annotate("flat air void, 0.1 mm\n$E_{void}=\\varepsilon_r E_{ins}=2.3\\,E_{ins}$", xy=(4.0, 2.25),
                xytext=(4.25, 3.2), fontsize=7.5, color=COLORS[1],
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"),
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    ax.text(0.15, 1.0, "XLPE, 4 mm\n($\\varepsilon_r$ = 2.3)", fontsize=7.5, va="center",
            bbox=dict(boxstyle="round,pad=0.15", fc="#FFF4D6", ec="none"))
    ax.annotate("", xy=(6.15, 4.0), xytext=(6.15, 0.45),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax.text(-0.2, 5.4, "(a) Void in XLPE (not to scale)", fontsize=8.5, weight="bold")

    # (b) abc circuit
    ax = axb
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=2.0, fontsize=9, lw=1.2)
        elm.SourceSin().at((0, 0)).to((0, 3.6))
        elm.Line().at((0, 3.6)).to((4.6, 3.6))
        elm.Line().at((0, 0)).to((4.6, 0))
        elm.Capacitor().at((2.4, 3.6)).to((2.4, 0))                       # Cc
        elm.Capacitor().at((4.6, 3.6)).to((4.6, 1.8))                     # Cb
        elm.Capacitor().at((4.6, 1.8)).to((4.6, 0))                       # Ca
        elm.Line().at((4.6, 1.8)).to((5.8, 1.8))
        elm.Line().at((5.8, 1.8)).to((5.8, 1.55))
        elm.SparkGap().at((5.8, 1.55)).to((5.8, 0.25))
        elm.Line().at((5.8, 0.25)).to((5.8, 0))
        elm.Line().at((4.6, 0)).to((5.8, 0))
        elm.Dot().at((4.6, 1.8))
        elm.Dot().at((2.4, 3.6))
        elm.Dot().at((2.4, 0))
        elm.Dot().at((4.6, 0))
        elm.Ground().at((0, 0))
        _draw(d)
    ax.text(-0.55, 1.8, "$U$", ha="right", va="center", fontsize=10)
    ax.text(1.95, 1.8, "$C_c$", ha="right", va="center", fontsize=10)
    ax.text(4.15, 2.7, "$C_b$", ha="right", va="center", fontsize=10)
    ax.text(4.15, 0.9, "$C_a$", ha="right", va="center", fontsize=10)
    ax.text(6.15, 0.9, "spark\ngap", ha="left", va="center", fontsize=8)
    ax.text(3.9, -0.75, "$C_a$ void, $C_b$ solid in series,\n$C_c$ rest of the insulation", ha="center", va="top", fontsize=7.5)
    ax.text(-0.9, 4.6, "(b) abc equivalent circuit", fontsize=8.5, weight="bold")
    ax.set_xlim(-1.0, 7.2)
    ax.set_ylim(-1.3, 4.9)
    ax.set_aspect("equal")

    # (c) IEC 60270 measuring circuit
    ax = axc
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=2.0, fontsize=9, lw=1.2)
        elm.SourceSin().at((0, 0)).to((0, 3.4))
        elm.Line().at((0, 3.4)).to((0.5, 3.4))
        elm.Inductor2(loops=3).at((0.5, 3.4)).to((2.2, 3.4))             # filter impedance Z
        elm.Line().at((2.2, 3.4)).to((5.0, 3.4))
        elm.Capacitor().at((2.8, 3.4)).to((2.8, 0))                       # test object Ca
        elm.Capacitor().at((5.0, 3.4)).to((5.0, 1.6))                     # coupling capacitor Ck
        elm.Resistor().at((5.0, 1.6)).to((5.0, 0))                        # measuring impedance Zm
        elm.Line().at((0, 0)).to((5.0, 0))
        elm.Line().at((5.0, 1.6)).to((5.7, 1.6))
        elm.Dot().at((2.8, 3.4))
        elm.Dot().at((2.8, 0))
        elm.Dot().at((5.0, 1.6))
        elm.Ground().at((0, 0))
        _draw(d)
    ax.add_patch(FancyBboxPatch((5.7, 1.1), 1.55, 1.0, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc="#EEF3F8", ec=INK, lw=1.0, zorder=4))
    ax.text(6.475, 1.6, "PD\ninstrument", ha="center", va="center", fontsize=7.5, zorder=5)
    # calibrator injecting q0 across the test object
    ax.add_patch(FancyBboxPatch((1.15, 0.9), 1.0, 0.75, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc="#FDEBD6", ec=COLORS[1], lw=1.0, zorder=4))
    ax.text(1.65, 1.27, "$q_0$", ha="center", va="center", fontsize=9, color=COLORS[1], zorder=5)
    ax.plot([1.65, 1.65, 2.8], [1.65, 2.6, 2.6], color=COLORS[1], lw=1.0, ls="--")
    ax.plot([1.65, 1.65], [0.9, 0.0], color=COLORS[1], lw=1.0, ls="--")
    ax.plot([2.8], [2.6], "o", ms=3, color=COLORS[1])
    ax.text(1.65, 0.75, "calibrator\n$q_0$ = 100 pC", ha="center", va="top", fontsize=7, color=COLORS[1],
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
    ax.text(-0.55, 1.7, "HV\n~", ha="right", va="center", fontsize=8)
    ax.text(1.35, 3.85, "filter $Z$", ha="center", va="bottom", fontsize=8)
    ax.text(3.2, 1.7, "test\nobject\n$C_a$", ha="left", va="center", fontsize=8)
    ax.text(5.4, 2.5, "$C_k$", ha="left", va="center", fontsize=9)
    ax.text(5.4, 0.7, "$Z_m$", ha="left", va="center", fontsize=9)
    ax.text(-1.1, 4.5, "(c) IEC 60270 measuring circuit", fontsize=8.5, weight="bold")
    ax.set_xlim(-1.2, 7.4)
    ax.set_ylim(-1.0, 4.9)
    ax.set_aspect("equal")

    # (d) phase-resolved PD pattern
    ax = axd
    rng = np.random.default_rng(24)
    ph, q = [], []
    for c0 in (0.0, 180.0):
        n = 260
        p = c0 + 95 * rng.beta(2.0, 2.3, n) - 8
        qq = np.clip(rng.gamma(4.0, 5.0, n), 2, 48)
        ph.append(p % 360)
        q.append(qq)
    ph = np.concatenate(ph)
    q = np.concatenate(q)
    ax.scatter(ph, q, s=5, color=COLORS[0], alpha=0.6, lw=0)
    x = np.linspace(0, 360, 361)
    ax.plot(x, 25 + 20 * np.sin(np.radians(x)), color="#888888", lw=1.0, ls="--")
    ax.text(316, 48, "test voltage\n(scaled)", fontsize=7, color="#666666", ha="center", va="top")
    for x0 in (0, 180):
        ax.axvspan(x0, x0 + 90, color="#F2F2F2", zorder=0)
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 50)
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_xlabel("Phase of test voltage (°)")
    ax.set_ylabel("Apparent charge |q| (pC)")
    ax.set_title("(d) Phase-resolved pattern of void discharges", fontsize=8.5, weight="bold", loc="left")
    ax.text(45, 47, "|u| rising", fontsize=7, ha="center", va="top", color="#555555")
    ax.text(225, 47, "|u| rising", fontsize=7, ha="center", va="top", color="#555555")
    pos = axd.get_position()
    axd.set_position([pos.x0 + 0.06, pos.y0 + 0.04, pos.width - 0.06, pos.height - 0.06])
    save(fig, CH, "fig-24-2-pd-void-model")


# ----------------------------------------------------------------------------
# Figure 24.3 — impulse waveshapes and back-flashover
# ----------------------------------------------------------------------------
def _double_exp_params(tp, th):
    """tau1 (tail), tau2 (front) of u = A(exp(-t/tau1) - exp(-t/tau2)) with time to peak tp and time
    to half-value th, both from the true origin."""
    def eqs(v):
        t1, t2 = np.exp(v)
        tpk = np.log(t1 / t2) * t1 * t2 / (t1 - t2)
        up = np.exp(-tpk / t1) - np.exp(-tpk / t2)
        uh = np.exp(-th / t1) - np.exp(-th / t2)
        return [tpk - tp, uh - 0.5 * up]
    t1, t2 = np.exp(fsolve(eqs, [np.log(th * 1.4), np.log(tp / 4)]))
    tpk = np.log(t1 / t2) * t1 * t2 / (t1 - t2)
    A = 1 / (np.exp(-tpk / t1) - np.exp(-tpk / t2))
    return t1, t2, A


def fig_24_3():
    fig = plt.figure(figsize=(6.8, 3.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1.1, 0.95], wspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])

    # lightning impulse
    t = np.linspace(0, 100, 20001)
    u = 1.037 * (np.exp(-t / 68.2) - np.exp(-t / 0.405))
    ipk = np.argmax(u)
    t30 = np.interp(0.3, u[:ipk], t[:ipk])
    t90 = np.interp(0.9, u[:ipk], t[:ipk])
    T1 = 1.67 * (t90 - t30)
    O1 = t30 - 0.3 * T1
    t50 = np.interp(0.5, u[ipk:][::-1], t[ipk:][::-1])
    T2 = t50 - O1
    ax1.plot(t, u, color=COLORS[0])
    ax1.axhline(0.5, color="#AAAAAA", lw=0.6, ls=":")
    ax1.plot([t50], [0.5], "o", color=COLORS[0], ms=4)
    ax1.annotate("", xy=(t50, 0.42), xytext=(O1, 0.42),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax1.text(t50 / 2 + 8, 0.40, f"$T_2$ = {T2:.1f} µs", ha="center", va="top", fontsize=8)
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 1.05)
    ax1.set_xlabel("Time (µs)")
    ax1.set_ylabel("Voltage (per unit of peak)")
    ax1.set_title("(a) Lightning 1.2/50 µs", fontsize=8.5, loc="left")
    ax1.text(98, 1.02, "$u = 1.037(e^{-t/68.2}-e^{-t/0.405})$, t in µs", fontsize=6.5, ha="right", va="top")
    # front zoom
    ins = ax1.inset_axes([0.45, 0.47, 0.52, 0.33])
    tz = t[t <= 4]
    ins.plot(tz, u[t <= 4], color=COLORS[0])
    ins.plot([O1, O1 + T1], [0, 1.0], "--", color=COLORS[1], lw=1.0)
    ins.plot([t30, t90], [0.3, 0.9], "o", color=COLORS[1], ms=3.5)
    ins.annotate("", xy=(O1 + T1, 0.08), xytext=(O1, 0.08),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
    ins.text(O1 + T1 + 0.15, 0.2, f"$T_1$ = {T1:.2f} µs", fontsize=6.5, va="center")
    ins.text(t30 + 0.3, 0.33, "30 %", fontsize=6.5, va="center")
    ins.text(t90 + 0.12, 0.86, "90 %", fontsize=6.5, va="top")
    ins.set_xlim(0, 4)
    ins.set_ylim(0, 1.05)
    ins.tick_params(labelsize=6.5)
    ins.set_xticks([0, 1, 2, 3, 4])
    ins.set_yticks([0, 0.5, 1])
    for sp in ("top", "right"):
        ins.spines[sp].set_visible(True)
    ins.set_title("front (µs)", fontsize=6.5, pad=1)

    # switching impulse 250/2500 us
    tau1, tau2, A = _double_exp_params(250.0, 2500.0)
    ts = np.linspace(0, 5000, 5001)
    us = A * (np.exp(-ts / tau1) - np.exp(-ts / tau2))
    ax2.plot(ts, us, color=COLORS[1])
    ip = np.argmax(us)
    th = np.interp(0.5, us[ip:][::-1], ts[ip:][::-1])
    ax2.plot([ts[ip]], [us[ip]], "o", color=COLORS[1], ms=4)
    ax2.plot([th], [0.5], "o", color=COLORS[1], ms=4)
    ax2.axhline(0.5, color="#AAAAAA", lw=0.6, ls=":")
    ax2.annotate(f"$T_p$ = {ts[ip]:.0f} µs", xy=(ts[ip], 1.0), xytext=(700, 0.93), fontsize=8,
                 arrowprops=dict(arrowstyle="-", lw=0.7))
    ax2.annotate("", xy=(th, 0.42), xytext=(0, 0.42),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax2.text(th / 2 + 300, 0.40, f"$T_2$ = {th:.0f} µs", ha="center", va="top", fontsize=8)
    ax2.set_xlim(0, 5000)
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks([0, 1000, 2000, 3000, 4000, 5000])
    ax2.set_xticklabels(["0", "1000", "2000", "3000", "4000", "5000"], fontsize=8)
    ax2.set_xlabel("Time (µs)")
    ax2.set_title("(b) Switching 250/2500 µs", fontsize=8.5, loc="left")

    # tower sketch
    ax = ax3
    ax.set_xlim(-7, 11)
    ax.set_ylim(-19, 38)
    ax.axis("off")
    ax.set_title("(c) Back-flashover", fontsize=8.5, loc="left")
    ax.add_patch(Polygon([(-2.6, 0), (2.6, 0), (0.9, 30), (-0.9, 30)], closed=True, fc="#EEEEEE", ec=INK, lw=1.0))
    for yy in np.arange(0, 30, 4):
        y2 = min(yy + 4, 30)
        w0 = 2.6 - 1.7 * yy / 30
        w1 = 2.6 - 1.7 * y2 / 30
        ax.plot([-w0, w1], [yy, y2], color="#999999", lw=0.6)
        ax.plot([w0, -w1], [yy, y2], color="#999999", lw=0.6)
    ax.plot([0, 0], [30, 32], color=INK, lw=1.0)
    ax.plot([-7, 11], [32, 32], color=INK, lw=0.8)              # shield wire
    ax.text(10.8, 32.7, "shield wire", fontsize=6.8, ha="right", va="bottom")
    ax.plot([1.2, 7.0], [24, 24], color=INK, lw=1.4)            # cross-arm
    ax.plot([6.5, 6.5], [24, 18.8], color=COLORS[0], lw=2.0)    # insulator string
    for yy in np.linspace(23.2, 19.6, 6):
        ax.plot([5.8, 7.2], [yy, yy], color=COLORS[0], lw=1.0)
    ax.plot([6.5], [18.2], "o", ms=6, color=INK)                # phase conductor
    ax.text(7.6, 17.6, "phase", fontsize=6.8, va="top")
    ax.text(7.6, 22.0, "insulator", fontsize=6.8, va="center", color=COLORS[0])
    # stroke
    ax.plot([-4.0, -1.4, -2.8, 0.0], [38, 35.5, 34.6, 32.2], color=COLORS[4], lw=1.8)
    ax.text(-6.8, 37.6, "50 kA", fontsize=7.5, color="#8a6200", va="top")
    # footing resistance
    zz = np.array([0.0, -0.8, -1.3, -1.8, -2.3, -2.8, -3.3, -3.8, -4.6])
    xs = np.array([0, 0, 0.6, -0.6, 0.6, -0.6, 0.6, 0, 0])
    ax.plot(xs, zz, color=INK, lw=1.0)
    for k, w in enumerate((1.4, 0.9, 0.4)):
        ax.plot([-w / 2, w / 2], [-4.6 - 0.8 * k, -4.6 - 0.8 * k], color=INK, lw=1.0)
    ax.text(1.0, -2.3, "$R_f$ = 20 Ω", fontsize=7, va="center")
    # height
    ax.annotate("", xy=(-4.6, 30), xytext=(-4.6, 0),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
    ax.text(-5.0, 15, "30 m", fontsize=6.8, rotation=90, ha="right", va="center")
    # flashover arrow, tower to phase
    ax.annotate("", xy=(6.1, 18.6), xytext=(1.6, 21.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLORS[1], connectionstyle="arc3,rad=0.3",
                                mutation_scale=10))
    ax.text(-6.8, -8.5, "tower top ≈ 50 kA × 20 Ω = 1 MV", fontsize=6.8, va="center")
    ax.text(-6.8, -13.0, "insulator: (1 − 0.25) × 1 MV\n= 750 kV > CFO 700 kV:", fontsize=6.8,
            va="center", color=COLORS[1])
    ax.text(-6.8, -17.3, "back-flashover tower → phase", fontsize=6.8, va="center", color=COLORS[1])
    save(fig, CH, "fig-24-3-impulse-waveshapes")


# ----------------------------------------------------------------------------
# Figure 24.4 — arrester V-I and insulation coordination
# ----------------------------------------------------------------------------
def fig_24_4():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 4.0), gridspec_kw=dict(width_ratios=[1, 1.05], wspace=0.25))
    Ipts = np.array([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 4e4, 6e4])
    Vpts = np.array([112, 136, 168, 190, 205, 220, 238, 260, 290, 330, 350])
    f = PchipInterpolator(np.log10(Ipts), Vpts)
    I = np.logspace(-4, np.log10(6e4), 400)
    ax1.plot(I, f(np.log10(I)), color=COLORS[0])
    pts = [(1e-3, 136, "136 kV at 1 mA\n($U_c$ = 96 kV RMS)", (2e-4, 205)),
           (1e3, 260, "260 kV at 1 kA", (3e-3, 280)),
           (1e4, 290, "$U_{pl}$ = 290 kV at 10 kA", (3e-3, 306)),
           (4e4, 330, "330 kV at 40 kA", (3e-3, 332))]
    for x, y, lab, (tx, ty) in pts:
        ax1.plot([x], [y], "o", color=COLORS[0], ms=4, zorder=5)
        ax1.annotate(lab, xy=(x, y), xytext=(tx, ty), fontsize=7.2, ha="left", va="center",
                     arrowprops=dict(arrowstyle="-", lw=0.6, color="#777777"))
    ax1.axhline(124, color=COLORS[1], ls="--", lw=1.0)
    ax1.text(1.0, 117, "minimum $U_c$ as a peak:\n1.05 × 145√2/√3 = 124 kV", fontsize=7.2, color=COLORS[1],
             va="top")
    ax1.set_xscale("log")
    ax1.set_xlim(1e-4, 1e5)
    ax1.set_ylim(0, 350)
    ax1.set_xlabel("Arrester current (A)")
    ax1.set_ylabel("Voltage (kV peak)")
    ax1.set_title("(a) ZnO arrester, $U_r$ = 120 kV", fontsize=9, loc="left")
    ax1.grid(True, lw=0.5)
    ax1.set_xticks([1e-4, 1e-2, 1, 1e2, 1e4])
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, _: {1e-4: "$10^{-4}$", 1e-2: "$10^{-2}$", 1: "1",
                                                              1e2: "$10^{2}$", 1e4: "$10^{4}$"}.get(v, "")))

    rows = [("system peak phase voltage, 145√2/√3", 118, "#9E9E9E", "solid"),
            ("TOV peak (earth-fault factor 1.4, 1 s)", 166, "#9E9E9E", "solid"),
            ("arrester protective level $U_{pl}$ (10 kA)", 290, COLORS[0], "solid"),
            ("at transformer, 15 m from arrester", 390, COLORS[1], "solid"),
            ("at transformer, 41 m (separation limit)", 565, COLORS[1], "dashed"),
            ("required withstand LIWL/1.15", 565, COLORS[2], "solid"),
            ("LIWL (BIL)", 650, COLORS[2], "solid")]
    n = len(rows)
    for i, (lab, v, c, st) in enumerate(rows):
        y = n - 1 - i
        if st == "dashed":
            ax2.barh(y, v, height=0.42, fc="white", ec=c, ls="--", lw=1.2)
        else:
            ax2.barh(y, v, height=0.42, color=c, alpha=0.8)
        ax2.text(4, y + 0.27, lab, fontsize=7.2, va="bottom")
        ax2.text(v + 8, y, f"{v}", va="center", fontsize=7.5)
    for i, ratio in ((5, 565 / 390), (6, 650 / 390)):
        y = n - 1 - i
        v = rows[i][1]
        ax2.annotate("", xy=(v, y), xytext=(390, y),
                     arrowprops=dict(arrowstyle="-|>", lw=1.1, color=INK, mutation_scale=8, shrinkA=0, shrinkB=0))
        ax2.plot([390, 390], [y - 0.21, y + 0.21], color=INK, lw=1.1)
        ax2.text(v + 82, y, f"×{ratio:.2f}", va="center", fontsize=8, weight="bold")
    ax2.axvline(390, color=COLORS[1], lw=0.7, ls=":")
    ax2.set_yticks([])
    ax2.spines["left"].set_visible(False)
    ax2.set_xlim(0, 820)
    ax2.set_ylim(-0.5, n - 0.2)
    ax2.set_xlabel("Voltage (kV peak)")
    ax2.set_title("(b) Coordination of a 132 kV transformer", fontsize=9, loc="left")
    ax2.grid(True, axis="x", lw=0.5)
    save(fig, CH, "fig-24-4-arrester-coordination")


# ----------------------------------------------------------------------------
# Figure 24.5 — ground potential rise, touch and step voltages
# ----------------------------------------------------------------------------
def _grid_model(rho=100.0, L=60.0, n=11, depth=0.5, a=0.005, seg=3.0):
    """Segment (method-of-moments) model of a square earth grid in uniform soil.
    Returns segment arrays and leakage currents for 1 V grid potential."""
    xs = np.linspace(0, L, n)
    segs = []
    ns = int(round(L / seg))
    for c in xs:                      # conductors along x at y = c - L/2
        for k in range(ns):
            segs.append((k * seg, c - L / 2, (k + 1) * seg, c - L / 2))
    for c in xs:                      # conductors along y at x = c
        for k in range(ns):
            segs.append((c, -L / 2 + k * seg, c, -L / 2 + (k + 1) * seg))
    S = np.array(segs)

    def pot(px, py, pz, S, I):
        """Potential at points from uniform line currents I in segments S (with image)."""
        V = np.zeros_like(px, dtype=float)
        for (x1, y1, x2, y2), Ii in zip(S, I):
            ln = np.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
            for zs in (-depth, depth):
                dx, dy, dz = px - x1, py - y1, pz - zs
                s = dx * ux + dy * uy
                d2 = np.maximum(dx ** 2 + dy ** 2 + dz ** 2 - s ** 2, a ** 2)
                r1 = np.sqrt(s ** 2 + d2)
                r2 = np.sqrt((s - ln) ** 2 + d2)
                V += rho * Ii / (4 * np.pi * ln) * np.log((s + r1) / (s - ln + r2))
        return V

    mx = 0.5 * (S[:, 0] + S[:, 2])
    my = 0.5 * (S[:, 1] + S[:, 3])
    N = len(S)
    A = np.zeros((N, N))
    for j in range(N):
        e = np.zeros(N)
        e[j] = 1.0
        A[:, j] = pot(mx, my, np.full(N, -depth + a), S[j:j + 1], e[j:j + 1])
    I = np.linalg.solve(A, np.ones(N))
    return S, I, pot


def fig_24_5():
    IG = 5000.0
    GPR = 3870.0                      # text: 5 kA x 0.774 ohm (Sverak)
    NG = 20                           # text: 60 m x 60 m grid with 2400 m of conductor = 20 x 20 conductors
    S, I1, pot = _grid_model(n=NG)
    Rg_model = 1 / I1.sum()
    D = 60.0 / (NG - 1)               # mesh spacing, 3.16 m
    yc = -30.0 + D / 2                # cut through the centres of the edge row of meshes
    x = np.linspace(-60, 100, 1601)
    v = pot(x, np.full_like(x, yc), np.zeros_like(x), S, I1) * GPR      # scaled to the text's GPR
    # touch voltage at the corner mesh centre (D/2, yc)
    vc = pot(np.array([D / 2]), np.array([yc]), np.array([0.0]), S, I1)[0] * GPR
    touch_corner = GPR - vc
    # step voltage just outside the perimeter (1 m step)
    xo = np.linspace(60, 70, 101)
    vo = pot(xo, np.full_like(xo, yc), np.zeros_like(xo), S, I1) * GPR
    vo1 = pot(xo + 1, np.full_like(xo, yc), np.zeros_like(xo), S, I1) * GPR
    step = np.max(vo - vo1)
    # unbonded fence 2 m outside the grid, continuing 150 m away along the road: average post potential
    fy = np.arange(-32, 120, 3.0)
    fence_v = pot(np.full_like(fy, 62.0), fy, np.zeros_like(fy), S, I1).mean() * GPR
    v_stand = pot(np.array([60.5]), np.array([yc]), np.array([0.0]), S, I1)[0] * GPR
    touch_fence = v_stand - fence_v

    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1], hspace=0.06)
    ax = fig.add_subplot(gs[0])
    axs = fig.add_subplot(gs[1], sharex=ax)
    ax.plot(x, v / 1e3, color=COLORS[0], lw=1.8)
    ax.axhline(GPR / 1e3, color=COLORS[1], ls="--", lw=1.0)
    ax.text(-58, GPR / 1e3 + 0.06, f"GPR = 5 kA × 0.774 Ω = {GPR / 1e3:.2f} kV (grid and everything bonded to it)",
            fontsize=7.5, color=COLORS[1], va="bottom")
    ax.axvspan(0, 60, color="#F3F3F3", zorder=0)
    # corner-mesh touch
    ax.annotate("", xy=(D / 2, GPR / 1e3), xytext=(D / 2, vc / 1e3),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax.text(4.5, 2.25, f"mesh (touch)\nvoltage, corner\nmesh: {touch_corner:.0f} V\n(tolerable 681 V)",
            fontsize=7.2, va="center")
    ax.annotate("", xy=(62.5, fence_v / 1e3), xytext=(62.5, v_stand / 1e3),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color=COLORS[3], mutation_scale=7, shrinkA=0, shrinkB=0))
    ax.plot([58, 100], [fence_v / 1e3] * 2, color=COLORS[3], lw=0.8, ls=":")
    ax.annotate(f"unbonded fence 2 m outside, running\noff site: touch ≈ {touch_fence:.0f} V from inside",
                xy=(62.5, 2.3), xytext=(22, 1.3), fontsize=7.2, color=COLORS[3], va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[3]))
    ax.annotate(f"step (1 m) just outside: up to {step:.0f} V\n(tolerable 2231 V)", xy=(61.5, 2.9),
                xytext=(22, 0.55), fontsize=7.2, color=COLORS[2], va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[2]))
    ax.text(99, 3.78, "telecom cable to\nremote earth: transferred\n≈ GPR = 3.87 kV", fontsize=7.2,
            color="#B07800", va="top", ha="right")
    ax.set_ylim(0, 4.4)
    ax.set_ylabel("Surface potential (kV)")
    ax.grid(True, lw=0.4)
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.text(-58, 3.55, f"profile through the edge row\nof meshes; uniform-soil model\n($R_g$ = {Rg_model:.2f} Ω) scaled to\nthe GPR of 3.87 kV", ha="left", va="top", fontsize=6.8, color="#555555")

    # cross-section
    axs.set_ylim(-3.2, 3.0)
    axs.add_patch(Rectangle((-60, -3.2), 160, 3.2, fc="#EAD9BF", ec="none", zorder=0))
    axs.add_patch(Rectangle((-5, -0.25), 70, 0.25, fc="#9E9E9E", ec="none", zorder=1))
    axs.axhline(0, color=INK, lw=0.8)
    for xg in np.linspace(0, 60, NG):
        axs.plot([xg], [-0.9], "o", ms=3.0, color=COLORS[1], zorder=3)
    axs.plot([0, 60], [-0.9, -0.9], color=COLORS[1], lw=0.6, zorder=2)
    axs.text(-58, -1.2, "grid at 0.5 m depth: 20 × 20 conductors,\n3.16 m spacing, 2400 m (60 m × 60 m)", ha="left",
             va="top", fontsize=7.2, color=COLORS[1])
    axs.text(-58, -2.6, "soil ρ = 100 Ω·m", fontsize=7.5)
    axs.text(-4, 0.1, "crushed rock 0.1 m, 3000 Ω·m (depths exaggerated)", fontsize=6.8, va="bottom", ha="right")
    axs.annotate("5 kA", xy=(30, -0.95), xytext=(30, -2.6), fontsize=7.5, ha="center", va="center",
                 arrowprops=dict(arrowstyle="-|>", lw=1.2, color=COLORS[1], mutation_scale=9))

    def person(xp, yb=0.0, h=2.0, w=1.6, color=INK, arm_to=None):
        axs.add_patch(Circle((xp, yb + h * 0.9), 0.0, fc="none"))
        axs.plot([xp], [yb + h * 0.92], "o", ms=5, color=color)
        axs.plot([xp, xp], [yb + h * 0.35, yb + h * 0.85], color=color, lw=1.4)
        axs.plot([xp - w / 2, xp, xp + w / 2], [yb, yb + h * 0.35, yb], color=color, lw=1.4)
        if arm_to is not None:
            axs.plot([xp, arm_to[0]], [yb + h * 0.7, arm_to[1]], color=color, lw=1.4)

    # earthed structure at the grid corner and person at corner mesh centre
    axs.add_patch(Rectangle((-0.9, 0), 0.9, 2.5, fc="#BBBBBB", ec=INK, lw=0.8))
    axs.plot([-0.45, -0.45, 0], [0, -0.9, -0.9], color=INK, lw=0.8)
    person(D / 2 + 0.3, arm_to=(0.0, 1.5))
    axs.text(D / 2 + 0.6, 2.3, "touch", fontsize=7, ha="left")
    # fence 2 m outside, unbonded
    axs.plot([62, 62], [0, 2.4], color=COLORS[3], lw=2.0)
    axs.plot([62, 62], [0, -0.6], color=COLORS[3], lw=1.2)
    person(60.4, arm_to=(62, 1.5), color=COLORS[3])
    axs.text(62.4, 2.45, "fence", fontsize=7, color=COLORS[3])
    # step outside
    person(70, w=2.2, color=COLORS[2])
    axs.text(70, 2.3, "step", fontsize=7, ha="center", color=COLORS[2])
    # telecom cable to remote earth
    axs.plot([45, 45, 100], [0, -2.2, -2.2], color=COLORS[4], lw=1.4)
    axs.text(99, -2.35, "telecom cable → remote earth", fontsize=7, ha="right", va="top", color="#8a6200")
    person(43, color=COLORS[4], arm_to=(45, 0.6))
    axs.add_patch(Rectangle((44.6, 0), 0.8, 0.7, fc=COLORS[4], ec=INK, lw=0.6))
    axs.set_xlim(-60, 100)
    axs.set_yticks([])
    axs.spines["left"].set_visible(False)
    axs.set_xlabel("Distance (m), grid from 0 to 60 m")
    print(f"  24.5 model: Rg = {Rg_model:.3f} ohm, corner-mesh touch = {touch_corner:.0f} V, "
          f"step = {step:.0f} V, fence touch = {touch_fence:.0f} V, centre V = {v[np.argmin(abs(x - 30))]:.0f} V")
    save(fig, CH, "fig-24-5-gpr-touch-step")


# ----------------------------------------------------------------------------
# Figure 24.6 — Cockcroft-Walton multiplier and Marx generator
# ----------------------------------------------------------------------------
def fig_24_6():
    fig = plt.figure(figsize=(6.8, 5.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.25], height_ratios=[1.6, 1], wspace=0.05, hspace=0.05)
    axa = fig.add_subplot(gs[:, 0])
    axb = fig.add_subplot(gs[0, 1])
    axc = fig.add_subplot(gs[1, 1])
    for ax in (axa, axb, axc):
        ax.axis("off")

    # (a) Cockcroft-Walton, 5 stages
    ax = axa
    n, H = 5, 1.3
    xl, xr, xs = 1.6, 3.6, 5.4           # smoothing column, oscillating column, transformer
    yT = -2.6 * H                        # earth rail below the transformer
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=1.3, fontsize=8, lw=1.1)
        # smoothing column: earth (y = 0) -> L1 ... L5 at y = 2kH
        for k in range(n):
            elm.Capacitor().at((xl, 2 * k * H)).to((xl, 2 * (k + 1) * H))
        # oscillating column: transformer terminal T (y = -H) -> O1 (H) -> O2 (3H) ... O5 (9H)
        elm.Capacitor().at((xr, -H)).to((xr, H))
        for k in range(n - 1):
            elm.Capacitor().at((xr, (2 * k + 1) * H)).to((xr, (2 * k + 3) * H))
        # diodes zig-zag: L_k -> O_(k+1) -> L_(k+1)
        for k in range(n):
            elm.Diode().at((xl, 2 * k * H)).to((xr, (2 * k + 1) * H))
            elm.Diode().at((xr, (2 * k + 1) * H)).to((xl, 2 * (k + 1) * H))
        # transformer secondary between earth (bottom of the smoothing column) and T
        elm.Line().at((xr, -H)).to((xs, -H))
        elm.SourceSin().at((xs, yT)).to((xs, -H))
        elm.Line().at((xs, yT)).to((xl, yT))
        elm.Line().at((xl, yT)).to((xl, 0))
        elm.Ground().at((xl, yT))
        # load
        elm.Line().at((xl, 2 * n * H)).to((0.0, 2 * n * H))
        elm.Resistor().at((0.0, 2 * n * H)).to((0.0, 0))
        elm.Line().at((0.0, 0)).to((xl, 0))
        for k in range(n + 1):
            elm.Dot().at((xl, 2 * k * H))
        for k in range(n):
            elm.Dot().at((xr, (2 * k + 1) * H))
        elm.Dot().at((xr, -H))
        _draw(d)
    ax.text(xs + 0.5, (yT - H) / 2, "100 kV\npeak,\n50 Hz", fontsize=7.5, va="center")
    ax.text(-0.45, n * H, "load\n2 mA", fontsize=7, va="center", ha="right")
    ax.text(-1.5, 2 * n * H + 0.35, "output $2nU_m$ = 1000 kV (ideal)\nripple 6.0 kV p-p, drop 38 kV",
            fontsize=7.5, va="bottom", ha="left")
    ax.text(xl - 0.4, yT - 0.75, "smoothing\ncolumn", ha="center", va="top", fontsize=6.8)
    ax.text(xr + 0.5, yT - 0.75, "oscillating\ncolumn", ha="center", va="top", fontsize=6.8)
    ax.text(xr + 0.5, 6 * H, "$C$ = 0.1 µF\neach (10)", fontsize=7, va="center")
    ax.text(-1.5, 2 * n * H + 2.0, "(a) Cockcroft–Walton, 5 stages", fontsize=8.5, weight="bold")
    ax.set_xlim(-1.6, 7.4)
    ax.set_ylim(yT - 2.2, 2 * n * H + 2.5)
    ax.set_aspect("equal")

    # (b) Marx generator, 4 stages stacked in a column
    ax = axb
    xa, xc, H = 2.0, 4.6, 2.0            # low side (left), high side (right) of each stage capacitor
    yg = -2.0                            # earth rail
    yt = 3 * H
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=1.4, fontsize=8, lw=1.1)
        for k in range(4):
            y = k * H
            elm.Capacitor().at((xa, y)).to((xc, y))
            if k < 3:
                elm.Resistor().at((xa, y)).to((xa, y + H))
                elm.Resistor().at((xc, y)).to((xc, y + H))
                elm.SparkGap().at((xc, y)).to((xa, y + H))
            elm.Dot().at((xa, y))
            elm.Dot().at((xc, y))
        # low side of stage 1 to earth; high side charged from U0 through Rc
        elm.Line().at((xa, 0)).to((xa, yg))
        elm.Resistor().at((xc, 0)).to((xc, -0.9))
        elm.SourceV().at((xc, yg)).to((xc, -0.9))
        # output: G4 from the top high side, Rt to earth, Rf to the load and divider
        elm.SparkGap().at((xc, yt)).to((xc + 1.2, yt + 1.0))
        elm.Line().at((xc + 1.2, yt + 1.0)).to((xc + 1.6, yt + 1.0))
        elm.Resistor().at((xc + 1.6, yt + 1.0)).to((xc + 3.4, yt + 1.0))         # Rf
        elm.Resistor().at((xc + 1.6, yg)).to((xc + 1.6, yt + 1.0))               # Rt
        elm.Capacitor().at((xc + 3.4, yg)).to((xc + 3.4, yt + 1.0))              # Cb
        elm.Line().at((xc + 3.4, yt + 1.0)).to((xc + 4.4, yt + 1.0))
        elm.Capacitor().at((xc + 4.4, 0.6)).to((xc + 4.4, yt + 1.0))             # divider HV arm
        elm.Capacitor().at((xc + 4.4, yg)).to((xc + 4.4, 0.6))                   # divider LV arm
        elm.Line().at((xc + 4.4, 0.6)).to((xc + 5.1, 0.6))
        elm.Line().at((xa, yg)).to((xc + 4.4, yg))
        elm.Ground().at((xc + 3.4, yg))
        elm.Dot().at((xc + 1.6, yt + 1.0))
        elm.Dot().at((xc + 3.4, yt + 1.0))
        elm.Dot().at((xc, yg))
        elm.Dot().at((xc + 1.6, yg))
        elm.Dot().at((xc + 3.4, yg))
        _draw(d)
    for k in range(4):
        ax.text(2.65, k * H + 0.1, f"$C_{{{k + 1}}}$", ha="center", va="bottom", fontsize=7.5)
    for k in range(3):
        ax.text(3.8, k * H + H / 2 - 0.3, f"G{k + 1}", ha="left", va="center", fontsize=7, color=COLORS[1])
    ax.text(xc + 0.35, yt + 0.85, "G4", fontsize=7, color=COLORS[1], ha="right", va="bottom")
    ax.text(1.0, -0.6, "G1\ntriggered", fontsize=6.5, color=COLORS[1], ha="center", va="center")
    ax.text(xa - 0.3, H / 2, "$R_c$", ha="right", va="center", fontsize=7.5)
    ax.text(xc - 0.45, yg + 0.55, "$U_0$", ha="right", va="center", fontsize=8)
    ax.text(xc + 2.5, yt + 1.35, "$R_f$ = 220 Ω", ha="center", va="bottom", fontsize=7.5)
    ax.text(xc + 1.85, 1.2, "$R_t$\n3.2 kΩ", ha="left", va="center", fontsize=7.5)
    ax.text(xc + 3.1, 3.3, "$C_b$\n2 nF", ha="right", va="center", fontsize=7.5)
    ax.text(xc + 5.15, 0.6, "to\nscope", ha="left", va="center", fontsize=7)
    ax.text(xc + 4.7, 3.6, "divider", ha="left", va="center", fontsize=7)
    ax.text(2.2, yt + 2.0, "(b) Marx generator, 4 stages", fontsize=8.5, weight="bold")
    ax.set_xlim(0.2, 11.2)
    ax.set_ylim(yg - 1.0, yt + 2.4)
    ax.set_aspect("equal")

    # (c) single-stage equivalent
    ax = axc
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=1.4, fontsize=8, lw=1.1)
        elm.Capacitor().at((0, 0)).to((0, 2.0))
        elm.Line().at((0, 2.0)).to((0.4, 2.0))
        elm.Switch().at((0.4, 2.0)).to((1.8, 2.0))
        elm.Line().at((1.8, 2.0)).to((2.4, 2.0))
        elm.Resistor().at((2.4, 2.0)).to((2.4, 0))          # Rt
        elm.Resistor().at((2.4, 2.0)).to((4.4, 2.0))        # Rf
        elm.Capacitor().at((4.4, 2.0)).to((4.4, 0))         # Cb
        elm.Line().at((0, 0)).to((4.4, 0))
        elm.Line().at((4.4, 2.0)).to((5.0, 2.0))
        elm.Dot(open=True).at((5.0, 2.0))
        elm.Dot().at((2.4, 2.0))
        elm.Dot().at((2.4, 0))
        elm.Ground().at((2.4, 0))
        _draw(d)
    ax.text(-0.45, 1.0, "$C_s$ = 20 nF\ncharged\nto $nU_0$", ha="right", va="center", fontsize=7.5)
    ax.text(2.7, 1.0, "$R_t$", ha="left", va="center", fontsize=7.5)
    ax.text(3.4, 2.3, "$R_f$", ha="center", va="bottom", fontsize=7.5)
    ax.text(4.75, 1.0, "$C_b$", ha="left", va="center", fontsize=7.5)
    ax.text(5.15, 2.0, "$u(t)$", ha="left", va="center", fontsize=7.5)
    ax.text(6.3, 1.55, "$T_1 \\approx 3R_f\\,\\dfrac{C_sC_b}{C_s+C_b}$ = 1.2 µs", fontsize=7.5, va="center")
    ax.text(6.3, 0.35, "$T_2 \\approx 0.7\\,R_t\\,(C_s+C_b)$ = 50 µs", fontsize=7.5, va="center")
    ax.text(-2.4, 3.0, "(c) Single-stage equivalent", fontsize=8.5, weight="bold")
    ax.set_xlim(-2.5, 12.6)
    ax.set_ylim(-1.0, 3.4)
    ax.set_aspect("equal")
    save(fig, CH, "fig-24-6-cw-and-marx")


if __name__ == "__main__":
    fig_24_1()
    fig_24_2()
    fig_24_3()
    fig_24_4()
    fig_24_5()
    fig_24_6()
