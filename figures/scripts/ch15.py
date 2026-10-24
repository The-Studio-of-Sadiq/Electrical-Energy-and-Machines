"""Figures for Chapter 15 — Renewable Energy Systems.

Run from the repository root:  python figures/scripts/ch15.py
"""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy.optimize import minimize
from scipy.signal import argrelextrema

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, box, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

CH = "15"
BLUE, VERM, GREEN, PINK, ORANGE, SKY = COLORS[:6]

# ---------------------------------------------------------------- PV single-diode model
RSH = 400.0          # module shunt resistance (ohm)


def v_of_i(I, Isc, Voc, a, Rs):
    """Single-diode model solved for V(I); a = n*Ns*kT/q. Returns -inf-like value for I >= Iph."""
    Iph = Isc * (1 + Rs / RSH)
    I0 = (Iph - Voc / RSH) / np.expm1(Voc / a)
    I = np.asarray(I, dtype=float)
    ok = I < Iph - 1e-9
    x = np.full_like(I, 0.8 * Voc)
    for _ in range(100):           # Newton iteration on x = V + I*Rs
        f = Iph - I0 * np.expm1(x / a) - x / RSH - I
        d = -I0 / a * np.exp(np.minimum(x / a, 700)) - 1 / RSH
        x = np.where(ok, x - f / d, x)
    return np.where(ok, x - I * Rs, -1e3)


def iv_curve(Isc, Voc, a, Rs, n=3000):
    I = np.linspace(0, Isc * 0.99999, n)
    V = v_of_i(I, Isc, Voc, a, Rs)
    m = V >= 0
    return V[m][::-1], I[m][::-1]


def mpp(Isc, Voc, a, Rs):
    V, I = iv_curve(Isc, Voc, a, Rs, 8000)
    k = np.argmax(V * I)
    return V[k], I[k], V[k] * I[k]


def fit_module():
    """Fit ideality term a and series resistance so that the STC MPP is 41.9 V, 13.1 A."""
    def err(p):
        a, Rs = p
        if a <= 0.5 or Rs < 0:
            return 1e6
        Vm, Im, _ = mpp(14.0, 49.8, a, Rs)
        return (Vm - 41.9) ** 2 + 10 * (Im - 13.1) ** 2
    r = minimize(err, [2.2, 0.2], method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-8))
    return r.x


A_STC, RS = fit_module()


# ---------------------------------------------------------------- Figure 15.1
def fig_15_1():
    """I-V and P-V curves of a 550 W module."""
    cases = [  # label, G, Tc, Isc, Voc, colour
        ("1,000 W/m², 25 °C", 1000, 25, 14.0, 49.8, BLUE),
        ("1,000 W/m², 60 °C", 1000, 60, 14.2, 45.1, VERM),
        ("800 W/m², 60 °C", 800, 60, 11.4, 44.8, ORANGE),
        ("400 W/m², 25 °C", 400, 25, 5.6, 48.0, GREEN),
    ]
    fig, ax = new_fig(6.6, 4.8)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    res = []
    for lab, G, Tc, Isc, Voc, c in cases:
        a = A_STC * (273.15 + Tc) / 298.15
        V, I = iv_curve(Isc, Voc, a, RS)
        Vm_, Im_, Pm_ = mpp(Isc, Voc, a, RS)
        ax.plot(V, I, color=c, lw=1.8, label=f"{lab}: MPP {Pm_:.0f} W ({Vm_:.1f} V, {Im_:.1f} A)")
        ax2.plot(V, V * I, color=c, lw=1.2, ls="--")
        Vm, Im, Pm = mpp(Isc, Voc, a, RS)
        ax2.plot(Vm, Pm, "o", color=c, ms=5, zorder=6)
        res.append((lab, Vm, Im, Pm))
    for k, (lab, Vm, Im, Pm) in enumerate(res):
        ax2.text(Vm - 0.8, Pm + 8, f"{Pm:.0f} W", fontsize=7.6, ha="right", va="bottom", color=cases[k][5],
                 bbox=dict(fc="white", ec="none", pad=0.4))
    ax.set(xlim=(0, 55), ylim=(0, 15), xlabel="Module voltage (V)", ylabel="Current (A)")
    ax2.set_ylim(0, 600)
    ax2.set_ylabel("Power (W)")
    h, lb = ax.get_legend_handles_labels()
    ax2.legend(h, lb, loc="upper center", fontsize=7.4, title="I–V solid, P–V dashed (right axis)",
               title_fontsize=7.4, bbox_to_anchor=(0.5, -0.15), ncol=2)
    save(fig, CH, "fig-15-1-pv-module-iv-curves")
    return res


# ---------------------------------------------------------------- Figure 15.2
def string_pv(n_shaded, frac=0.3, n_sub=81, Vf=0.5):
    """P-V curve of a 27-module string (81 bypassed substrings) with n_shaded substrings at frac irradiance."""
    I = np.r_[np.linspace(0, 13.9, 30000), 14.0 - np.logspace(-1, -9, 4000)]
    a, Rs = A_STC / 3, RS / 3
    Vsub = np.maximum(v_of_i(I, 14.0, 49.8 / 3, a, Rs), -Vf)
    Vsh = np.maximum(v_of_i(I, frac * 14.0, 49.8 / 3 + a * np.log(frac), a, Rs), -Vf)
    V = (n_sub - n_shaded) * Vsub + n_shaded * Vsh
    o = np.argsort(V)
    return V[o], (V * I)[o]


def fig_15_2():
    """Partial shading of a 27-module string with bypass diodes."""
    fig, ax = new_fig(6.6, 4.2)
    out = {}
    for n, c, ls, lab in [(0, "#666666", "--", "unshaded string"),
                          (1, BLUE, "-", "one substring (⅓ of one module) at 30 %"),
                          (9, VERM, "-.", "three modules (9 substrings) at 30 %:\ntwo maxima")]:
        V, P = string_pv(n)
        m = V >= 0
        V, P = V[m], P[m] / 1000
        ax.plot(V, P, color=c, ls=ls, lw=1.6 if n else 1.3, label=lab)
        idx = argrelextrema(P, np.greater, order=150)[0]
        out[n] = [(V[i], P[i]) for i in idx]
    Vu, Pu = out[0][0]
    ax.plot(Vu, Pu, "o", color="#666666", ms=4.5)
    ax.text(Vu - 15, Pu + 0.2, f"{Pu:.2f} kW at {Vu:.0f} V", ha="right", va="bottom", fontsize=7.6, color="#444444")
    V1, P1 = max(out[1], key=lambda t: t[1])
    ax.plot(V1, P1, "o", color=BLUE, ms=5)
    ax.annotate(f"global maximum {P1:.2f} kW at {V1:.0f} V\n(bypass diode conducting)", xy=(V1, P1),
                xytext=(870, 8.15), fontsize=7.6, color=BLUE, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    loc9 = [t for t in out[9] if t[0] > 1150]
    glob9 = max(out[9], key=lambda t: t[1])
    ax.plot(*glob9, "o", color=VERM, ms=5)
    ax.annotate(f"{glob9[1]:.1f} kW at {glob9[0]:.0f} V", xy=glob9, xytext=(790, 14.7), fontsize=7.6, color=VERM,
                ha="center", arrowprops=dict(arrowstyle="-", color=VERM, lw=0.7))
    if loc9:
        Vl, Pl = loc9[0]
        ax.plot(Vl, Pl, "o", color=VERM, ms=5)
        ax.annotate(f"local maximum {Pl:.1f} kW at {Vl:.0f} V:\nMPPT may stick here", xy=(Vl, Pl),
                    xytext=(870, 6.55), fontsize=7.6, color=VERM, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.0, mutation_scale=10))
    ax.set(xlim=(0, 1400), ylim=(0, 15.5), xlabel="String voltage (V)", ylabel="String power (kW)")
    ax.legend(loc="upper left", fontsize=7.4, bbox_to_anchor=(0.0, 1.0))
    # inset: module with three substrings and bypass diodes
    ia = fig.add_axes([0.43, 0.15, 0.30, 0.25])
    ia.set_xlim(0, 10)
    ia.set_ylim(0, 6)
    ia.set_aspect("equal")
    ia.axis("off")
    for k in range(3):
        x0 = 0.6 + 3.1 * k
        shaded = k == 1
        ia.add_patch(Rectangle((x0, 3.0), 2.6, 2.2, fc="#9DA8B5" if shaded else "#CFE0F1", ec=INK, lw=0.9))
        for r in range(2):
            for cc in range(3):
                ia.add_patch(Rectangle((x0 + 0.15 + 0.82 * cc, 3.15 + 1.05 * r), 0.7, 0.9, fc="none",
                                       ec="#5A6B80", lw=0.4))
        xm = x0 + 1.3
        ia.plot([x0, x0, x0 + 0.2], [3.0, 1.6, 1.6], color=INK, lw=0.8)
        ia.plot([x0 + 2.6, x0 + 2.6, x0 + 2.4], [3.0, 1.6, 1.6], color=INK, lw=0.8)
        c = VERM if shaded else INK
        ia.add_patch(Polygon([[x0 + 0.95, 1.25], [x0 + 0.95, 1.95], [x0 + 1.55, 1.6]], fc=c, ec=c))
        ia.plot([x0 + 1.6, x0 + 1.6], [1.25, 1.95], color=c, lw=1.0)
        ia.plot([x0 + 0.2, x0 + 0.95], [1.6, 1.6], color=c, lw=0.8)
        ia.plot([x0 + 1.6, x0 + 2.4], [1.6, 1.6], color=c, lw=0.8)
    ia.text(5.0, 5.55, "module: 3 substrings, 3 bypass diodes", ha="center", va="bottom", fontsize=6.6)
    ia.text(5.0, 0.75, "shaded substring: its diode conducts", ha="center", va="top", fontsize=6.6, color=VERM)
    save(fig, CH, "fig-15-2-partial-shading-pv-curve")
    return out


# ---------------------------------------------------------------- Figure 15.3
RHO, AREA, PR = 1.225, np.pi * 118.0 ** 2, 15.0


def power_curve(v):
    v = np.asarray(v, dtype=float)
    return np.where((v >= 3) & (v < 11), PR * (v ** 3 - 27) / (1331 - 27),
                    np.where((v >= 11) & (v <= 25), PR, 0.0))


def rayleigh(v, mean):
    s = mean / np.sqrt(np.pi / 2)
    return v / s ** 2 * np.exp(-v ** 2 / (2 * s ** 2))


def fig_15_3():
    """15 MW power curve with Rayleigh distribution (mean 9.5 m/s)."""
    v = np.linspace(0, 30, 3001)
    P = power_curve(v)
    f = rayleigh(v, 9.5)
    cf = np.trapezoid(P * f, v) / PR
    fig, ax = new_fig(6.6, 4.6)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.fill_between(v, 0, f, color=SKY, alpha=0.30, lw=0, label="Rayleigh pdf, mean 9.5 m/s (right)")
    ax2.plot(v, f, color=SKY, lw=1.0)
    e = P * f / PR
    ax2.fill_between(v, 0, e, color=ORANGE, alpha=0.35, lw=0,
                     label=f"energy contribution P·f / P$_{{rated}}$ (right;\narea = capacity factor {cf:.2f})")
    ax2.plot(v, e, color=ORANGE, lw=1.0)
    ax2.set_ylim(0, 0.10)
    ax2.set_ylabel("Probability density (per m/s)")
    ax.plot(v, P, color=BLUE, lw=2.0, label="idealised power curve (left)")
    vb = np.linspace(0, 12, 200)
    Pb = 16 / 27 * 0.5 * RHO * AREA * vb ** 3 / 1e6
    ax.plot(vb[Pb <= 16], Pb[Pb <= 16], color=INK, ls=":", lw=1.4, label="Betz limit, 236 m rotor (left)")
    ax.set(xlim=(0, 30), ylim=(0, 16), xlabel="Hub-height wind speed (m/s)", ylabel="Power (MW)")
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    for vv, lab in ((3, "cut-in\n3 m/s"), (11, "rated\n11 m/s"), (25, "cut-out\n25 m/s")):
        ax.axvline(vv, color="#999999", lw=0.8, ls="--")
        ax.text(vv + 0.3, 15.7 if vv != 3 else 12.0, lab, fontsize=7.6, va="top")
    vp = v[np.argmax(f)]
    ax2.annotate(f"peak {f.max():.3f} at {vp:.1f} m/s", xy=(vp, f.max()), xytext=(13.5, 0.088), fontsize=7.6,
                 color="#2E7FB0", arrowprops=dict(arrowstyle="-", color="#2E7FB0", lw=0.7))
    ax.text(26.0, 9.0, f"gross capacity\nfactor {cf * 100:.0f} %", fontsize=8.5, ha="center", va="center",
            bbox=dict(fc="white", ec="#999999", lw=0.6, pad=3))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", fontsize=7.4, bbox_to_anchor=(0.5, -0.16), ncol=2)
    save(fig, CH, "fig-15-3-wind-power-curve-and-distribution")
    return cf, cf * PR * 8.76


# ---------------------------------------------------------------- Figure 15.4
def fig_15_4():
    """The four wind-turbine generator types."""
    fig, ax = schematic(6.8, 5.7, xlim=(0, 17), ylim=(0, 14.3))
    fs = 7.0
    rows = [12.6, 9.0, 5.4, 1.8]   # centre lines
    def rotor(x, y):
        ax.add_patch(Circle((x, y), 0.14, fc=INK, zorder=6))
        for ang in (90, 210, 330):
            t = np.radians(ang)
            ax.add_patch(Polygon([[x, y], [x + 0.62 * np.cos(t) - 0.1 * np.sin(t), y + 0.62 * np.sin(t) + 0.1 * np.cos(t)],
                                  [x + 0.62 * np.cos(t), y + 0.62 * np.sin(t)]], fc="#BBBBBB", ec=INK, lw=0.7, zorder=5))
    def bx(x, y, w, txt, fc="#EEF3F8", h=1.0, ls="-", fsz=fs):
        from matplotlib.patches import FancyBboxPatch
        ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc,
                                    ec=INK, lw=1.0, ls=ls, zorder=4))
        ax.text(x + w / 2, y, txt, ha="center", va="center", fontsize=fsz, zorder=5)
    def ln(xs, ys, **kw):
        ax.plot(xs, ys, color=INK, lw=1.1, zorder=3, **kw)
    def tx(x, y):
        for dx in (-0.2, 0.2):
            ax.add_patch(Circle((x + dx, y), 0.32, fc="none", ec=INK, lw=1.0, zorder=5))
        ax.text(x, y - 0.45, "0.69/33 kV", ha="center", va="top", fontsize=6.2)
    def grid(x, y):
        ax.plot([x, x], [y - 0.55, y + 0.55], color=INK, lw=3.0)
        ax.text(x + 0.15, y, "grid", ha="left", va="center", fontsize=fs)
    def cap(x, y):
        ln([x, x], [y, y - 0.55])
        ax.plot([x - 0.22, x + 0.22], [y - 0.55, y - 0.55], color=INK, lw=1.3)
        ax.plot([x - 0.22, x + 0.22], [y - 0.7, y - 0.7], color=INK, lw=1.3)
        ln([x, x], [y - 0.7, y - 0.95])
        ax.plot([x - 0.15, x + 0.15], [y - 0.95, y - 0.95], color=INK, lw=1.0)
        ax.text(x + 0.3, y - 0.62, "capacitor\nbank", ha="left", va="center", fontsize=6.2)
    titles = [("Type 1", "fixed speed\n(≈ 1 % slip)"), ("Type 2", "limited\nvariable speed\n(≈ +10 %)"),
              ("Type 3", "variable speed\n(≈ ±30 %)"), ("Type 4", "full variable\nspeed")]
    for (t1, t2), y in zip(titles, rows):
        ax.text(0.1, y + 0.25, t1, ha="left", va="bottom", fontsize=8.5, fontweight="bold")
        ax.text(0.1, y + 0.15, t2, ha="left", va="top", fontsize=6.1, color="#444444")
        rotor(2.95, y)
    xtx, xg = 14.1, 15.6
    # Type 1
    y = rows[0]
    ln([2.65, 15.6], [y, y])
    bx(3.55, y, 1.45, "gearbox", fsz=6.6)
    bx(5.3, y, 1.6, "SCIG", fc="#E3F2EA")
    bx(7.4, y, 1.6, "soft\nstarter", fc="#FDF3D9")
    cap(10.2, y)
    tx(xtx, y)
    grid(xg, y)
    # Type 2
    y = rows[1]
    ln([2.65, 15.6], [y, y])
    bx(3.55, y, 1.45, "gearbox", fsz=6.6)
    bx(5.3, y, 1.6, "WRIG", fc="#E3F2EA")
    ln([6.1, 6.1], [y - 0.5, y - 1.0])
    bx(5.0, y - 1.45, 2.2, "rotor resistor +\nPE switch", fc="#FDF3D9", h=0.8, fsz=6.4)
    cap(10.2, y)
    tx(xtx, y)
    grid(xg, y)
    # Type 3
    y = rows[2]
    ln([2.65, 15.6], [y, y])
    bx(3.55, y, 1.45, "gearbox", fsz=6.6)
    bx(5.3, y, 1.6, "DFIG", fc="#E3F2EA")
    ax.text(9.4, y + 0.12, "stator direct", ha="center", va="bottom", fontsize=6.4)
    yr = y - 1.55
    ln([6.1, 6.1, 7.6], [y - 0.5, yr, yr])
    bx(7.6, yr, 1.25, "AC/DC", fc="#F6E3D8", h=0.75)
    ln([8.85, 9.25], [yr, yr])
    ax.plot([9.05, 9.05], [yr - 0.3, yr + 0.3], color=INK, lw=0)
    bx(9.25, yr, 1.25, "DC/AC", fc="#F6E3D8", h=0.75)
    ln([10.5, 12.6, 12.6], [yr, yr, y])
    ax.add_patch(Circle((12.6, y), 0.07, fc=INK, zorder=6))
    ax.text(9.05, yr + 0.45, "back-to-back converter, ≈ 30 % rating", ha="center", va="bottom", fontsize=6.4)
    ln([6.1, 5.75], [yr + 0.4, yr + 0.4])
    bx(4.6, yr + 0.4, 1.15, "crowbar", fc="#FDF3D9", h=0.5, fsz=6.0)
    tx(xtx, y)
    grid(xg, y)
    # Type 4
    y = rows[3]
    ln([2.65, 15.6], [y, y])
    bx(3.6, y, 1.3, "gearbox\n(optional)", ls="--", fsz=6.4)
    bx(5.3, y, 1.6, "PMSG", fc="#E3F2EA")
    bx(7.4, y, 1.25, "AC/DC", fc="#F6E3D8")
    ax.plot([8.65, 8.65], [y, y], color=INK)
    xdc = 9.25
    ln([xdc, xdc], [y - 0.55, y + 0.55])
    ln([xdc + 0.25, xdc + 0.25], [y - 0.55, y + 0.55])
    ax.add_patch(Rectangle((xdc - 0.15, y - 0.15), 0.55, 0.3, fc="white", ec="none", zorder=4))
    ln([xdc + 0.12, xdc + 0.12], [y - 0.55, y - 0.9])
    bx(xdc - 0.75, y - 1.25, 1.75, "DC-link chopper", fc="#FDF3D9", h=0.5, fsz=6.0)
    bx(10.0, y, 1.25, "DC/AC", fc="#F6E3D8")
    ax.text(9.6, y + 0.62, "full-rating back-to-back converter with DC link", ha="center", va="bottom",
            fontsize=6.4)
    ax.text(4.25, y - 0.62, "or direct drive", ha="center", va="top", fontsize=6.2, style="italic")
    tx(xtx, y)
    grid(xg, y)
    for y in rows[:3]:
        ax.plot([0.1, 16.9], [y - 2.05, y - 2.05], color="#CCCCCC", lw=0.6)
    save(fig, CH, "fig-15-4-wind-generator-types")


# ---------------------------------------------------------------- Figure 15.5
FDC_P = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
FDC_Q = [30, 18, 13, 9, 6.8, 5.4, 4.4, 3.6, 3.0, 2.5, 2.0, 1.7, 1.2]


def run_of_river(Qd, Qenv=0.5, H=60.0, eta=0.85, pmin=0.25):
    p = np.linspace(0, 100, 100001)
    Q = np.interp(p, FDC_P, FDC_Q)
    t = np.minimum(Q - Qenv, Qd)
    t = np.where(t >= pmin * Qd, t, 0.0)
    E = np.trapezoid(9.81 * eta * H * t / 1000, p) / 100 * 8.76     # GWh/yr
    Pr = 9.81 * eta * H * Qd / 1000
    return p, Q, t, E, E / (Pr * 8.76)


def fig_15_5():
    """Flow-duration curve with environmental flow, design flow and turbined flow."""
    Qd, Qenv = 6.8, 0.5
    p, Q, t, E, cf = run_of_river(Qd)
    fig, ax = new_fig(6.4, 4.0)
    ax.fill_between(p, 0, np.minimum(Q, Qenv), color="#7FBF7F", alpha=0.6, lw=0, label="environmental flow 0.5 m³/s")
    ax.fill_between(p, Qenv, Qenv + t, where=t > 0, color=BLUE, alpha=0.35, lw=0,
                    label=f"turbined flow (≤ Q$_d$ = 6.8 m³/s): {E:.1f} GWh/yr, CF {cf * 100:.0f} %")
    ax.fill_between(p, Qenv + t, Q, where=Q > Qenv + t, color="#DDDDDD", alpha=0.6, lw=0,
                    label="spilled (flood flow and flow below turbine minimum)")
    ax.plot(p, Q, color=INK, lw=1.8)
    ax.plot(FDC_P, FDC_Q, "o", color=INK, ms=3)
    ax.axhline(Qenv + Qd, color=BLUE, lw=1.0, ls="--")
    ax.text(99, Qenv + Qd + 0.3, "environmental + design flow = 0.5 + 6.8 m³/s", ha="right", va="bottom",
            fontsize=7.6, color=BLUE)
    ax.plot(30, 6.8, "s", color=VERM, ms=6, zorder=6)
    ax.annotate("design flow Q$_{30}$ = 6.8 m³/s", xy=(30, 6.8), xytext=(31, 12.5), fontsize=8, color=VERM,
                arrowprops=dict(arrowstyle="-", color=VERM, lw=0.8))
    pend = p[np.nonzero(t)[0][-1]]
    ax.axvline(pend, color="#777777", lw=0.8, ls=":")
    ax.annotate(f"turbine stops at {pend:.0f} %:\nturbined flow < 1.7 m³/s\n(25 % of design)", xy=(pend, 2.4),
                xytext=(67, 12.5), fontsize=7.6, arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.text(9, 21, "spilled\nflood flow", fontsize=8, ha="left", va="center", color="#555555")
    ax.set(xlim=(0, 100), ylim=(0, 30), xlabel="Percentage of time flow is equalled or exceeded (%)",
           ylabel="Flow (m³/s)")
    ax.legend(loc="upper right", fontsize=7.4, bbox_to_anchor=(1.0, 1.0))
    save(fig, CH, "fig-15-5-flow-duration-curve")
    return {qd: run_of_river(qd)[3:] for qd in (4.4, 5.4, 6.8, 9.0, 13.0)}


# ---------------------------------------------------------------- Figure 15.6
def clear_sky(t):
    return 0.95 * np.clip(np.cos(np.pi * (t - 12.5) / 13.0), 0, None) ** 1.25


def cloud_index(rng, t, slow, p_on=0.035, p_off=0.06):
    """One-minute clear-sky index: two-state (clear/shadow) Markov chain modulated by slow cloud cover."""
    n = len(t)
    k = np.ones(n)
    state = 0
    z = 0.0
    for i in range(1, n):
        c = slow[i]
        if state == 0 and rng.random() < p_on * c:
            state = 1
        elif state == 1 and rng.random() < p_off:
            state = 0
        z = 0.8 * z + 0.2 * rng.standard_normal()          # smooth AR(1) texture
        k[i] = (0.27 + 0.05 * z) if state else (1.0 + c * (0.05 + 0.03 * z))
    # cloud-edge enhancement just after a shadow ends
    edge = np.r_[0, np.diff(k) > 0.4]
    k = np.where(edge, k + 0.08, k)
    return k


def fig_15_6():
    """One PV plant versus the aggregate of twenty plants on a partly cloudy day."""
    rng = np.random.default_rng(7)
    t = np.arange(6 * 60, 19 * 60 + 1) / 60.0
    cs = clear_sky(t)
    # slowly varying regional cloud cover (shared by all plants), 0 before 09:30 and after 15:30
    cover = np.clip(np.sin(np.pi * (t - 9.5) / 6.0), 0, None) ** 0.7
    cover *= 0.85 + 0.15 * np.sin(2 * np.pi * (t - 9.5) / 2.3)
    plants = []
    for j in range(20):
        local = cover * (0.85 + 0.3 * rng.random())
        plants.append(np.minimum(cs * cloud_index(rng, t, np.clip(local, 0, 1)), 1.05))
    plants = np.array(plants)
    single = plants[0]
    agg = plants.mean(axis=0)
    win = (t >= 10) & (t <= 15)
    sd1 = np.std(np.diff(single)[win[1:]])
    sda = np.std(np.diff(agg)[win[1:]])
    fig, ax = new_fig(6.6, 4.3)
    ax.plot(t, cs, color="#AAAAAA", lw=1.0, label="clear-sky envelope")
    ax.plot(t, single, color=BLUE, lw=0.6, label="single 5 MW plant (1-min data)")
    ax.plot(t, agg, color=VERM, lw=2.2, label="aggregate of 20 plants over 100 km")
    d = np.diff(single)
    i = np.argmax(np.where(win[1:], -d, 0))
    ax.annotate("", xy=(t[i + 1] + 0.05, single[i + 1]), xytext=(t[i] + 0.05, single[i]),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=10))
    ax.annotate(f"ramp of {single[i] - single[i + 1]:.2f}\nin one minute", xy=(t[i] + 0.05, (single[i] + single[i + 1]) / 2),
                xytext=(t[i] + 1.0, 0.08), fontsize=7.6,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    ax.text(15.6, 1.0, f"1-min ramp standard deviation\n(10:00–15:00)\nsingle plant: {sd1:.2f}\naggregate: {sda:.2f}",
            fontsize=7.6, va="top", bbox=dict(fc="white", ec="#999999", lw=0.6, pad=3))
    ax.set(xlim=(6, 19), ylim=(0, 1.1), xlabel="Time of day", ylabel="Output (fraction of rated)")
    ax.set_xticks(range(6, 20, 2), [f"{h:02d}:00" for h in range(6, 20, 2)])
    ax.legend(loc="upper center", fontsize=7.4, bbox_to_anchor=(0.5, -0.15), ncol=3)
    save(fig, CH, "fig-15-6-pv-aggregation-smoothing")
    return sd1, sda, single[win].min(), single[win].max(), agg[win].min(), agg[win].max()


if __name__ == "__main__":
    print("module fit a, Rs:", A_STC, RS)
    print(fig_15_1())
    print(fig_15_2())
    print(fig_15_3())
    fig_15_4()
    print(fig_15_5())
    print(fig_15_6())
