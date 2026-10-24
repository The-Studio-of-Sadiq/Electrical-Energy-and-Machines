"""Figures for Chapter 3 — Energy Conversion Principles.

Run from the repository root:  python figures/scripts/ch03.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

from figstyle import save, COLORS, INK

MU0 = 4e-7 * np.pi


# ----------------------------------------------------------------------------------------
# Figure 3.1 — energy and co-energy of the saturating plunger magnet
# ----------------------------------------------------------------------------------------
def plunger(i, x):
    N, A, lam_s = 500, 4e-4, 0.32
    L = MU0 * N ** 2 * A / x
    return lam_s * np.tanh(L * i / lam_s), L


def fig_3_1():
    lam_s = 0.32
    i = np.linspace(0, 10, 600)
    lam2, L2 = plunger(i, 2.0e-3)
    lam18, L18 = plunger(i, 1.8e-3)
    i0 = 5.0
    l0, _ = plunger(i0, 2.0e-3)
    Wc = lam_s ** 2 / L2 * np.log(np.cosh(L2 * i0 / lam_s))
    W = l0 * i0 - Wc

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.8, 3.6), sharey=True)
    m = i <= i0
    ax.fill_between(i[m], 0, lam2[m], color=COLORS[5], alpha=0.35, lw=0)
    ax.fill_betweenx(lam2[m], 0, i[m], color=COLORS[4], alpha=0.35, lw=0)
    ax.plot(i, lam2, color=COLORS[0], label="$x$ = 2.0 mm")
    ax.plot(i, L2 * i, ":", color=INK, lw=1.2, label="linear, $L$ = 62.8 mH")
    ax.plot([0, i0, i0], [l0, l0, 0], "--", color=INK, lw=0.9)
    ax.plot(i0, l0, "o", color=COLORS[0], ms=5)
    ax.text(0.45, 0.215, "$W$ = %.2f J" % W, fontsize=8.5, ha="left", va="center")
    ax.text(3.65, 0.07, "$W'$ =\n%.2f J" % Wc, fontsize=8.5, ha="center", va="center")
    ax.text(i0 + 0.15, l0 + 0.012, r"$\lambda i$ = %.2f J at 5 A" % (l0 * i0), fontsize=8, va="bottom")
    ax.set_xlim(0, 10); ax.set_ylim(0, 0.35)
    ax.set_xlabel("current $i$ (A)")
    ax.set_ylabel(r"flux linkage $\lambda$ (Wb-turn)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("(a) energy and co-energy", loc="left", fontsize=10)

    bx.fill_between(i[m], lam2[m], lam18[m], color=COLORS[1], alpha=0.35, lw=0)
    bx.plot(i, lam18, color=COLORS[1], label="$x$ = 1.8 mm ($L$ = 69.8 mH)")
    bx.plot(i, lam2, color=COLORS[0], label="$x$ = 2.0 mm ($L$ = 62.8 mH)")
    bx.axvline(i0, ls="--", color=INK, lw=0.9)
    bx.annotate(r"$\Delta W' = F\,dx$" + "\nat constant current", xy=(3.4, 0.205), xytext=(6.0, 0.14),
                fontsize=8.5, arrowprops=dict(arrowstyle="-", lw=0.7))
    bx.set_xlim(0, 10)
    bx.set_xlabel("current $i$ (A)")
    bx.legend(fontsize=8, loc="lower right")
    bx.set_title("(b) armature moves 0.2 mm", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.2)
    save(fig, "03", "fig-3-1-energy-and-coenergy")


# ----------------------------------------------------------------------------------------
# Figure 3.2 — SRM energy-conversion loop
# ----------------------------------------------------------------------------------------
def lam_aligned(i):
    i = np.asarray(i, float)
    return np.where(i <= 12, 0.025 * i, 0.30 + 0.15 * (1 - np.exp(-(i - 12) / 6.0)))


def i_aligned(lam):
    lam = np.asarray(lam, float)
    return np.where(lam <= 0.30, lam / 0.025, 12 - 6.0 * np.log(1 - (np.minimum(lam, 0.4499) - 0.30) / 0.15))


def fig_3_2():
    IA, lamB, target = 30.0, 0.38, 5.0
    lamA = 0.0025 * IA
    dI = IA - i_aligned(lamB)

    def i_ret(lam, n):
        return i_aligned(lam) + dI * (lam / lamB) ** n

    def area(n):
        right = lamB * IA - 0.5 * IA * lamA          # under the O-A-B boundary (integral of i dλ)
        left = quad(lambda l: float(i_ret(l, n)), 0, lamB, limit=200)[0]
        return right - left

    hug = lamB * IA - 0.5 * IA * lamA - quad(lambda l: float(i_aligned(l)), 0, lamB)[0]
    print("area if the return path followed the aligned curve: %.2f J" % hug)
    n = brentq(lambda nn: area(nn) - target, 0.05, 20)
    W = area(n)

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ii = np.linspace(0, 40, 400)
    ax.plot(ii, 0.0025 * ii, color=COLORS[2], lw=1.4, label="unaligned (2.5 mH)")
    ax.plot(ii, lam_aligned(ii), color=COLORS[3], lw=1.4, label="aligned (25 mH, saturating)")
    lam = np.linspace(0, lamB, 300)
    xr = i_ret(lam, n)
    # loop polygon O -> A -> B -> back to O along the return path
    px = np.r_[0, IA, IA, xr[::-1]]
    py = np.r_[0, lamA, lamB, lam[::-1]]
    ax.fill(px, py, color=COLORS[0], alpha=0.18, lw=0)
    ax.plot(px, py, color=COLORS[0], lw=2.0)
    for (x0, y0, x1, y1) in [(12, 0.03, 18, 0.045), (IA, 0.20, IA, 0.26)]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=13))
    k = 150
    ax.annotate("", xy=(xr[k - 12], lam[k - 12]), xytext=(xr[k], lam[k]),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=13))
    for lab, (x, y), off in [("O", (0, 0), (-1.2, 0.01)), ("A", (IA, lamA), (-1.6, -0.035)),
                             ("B", (IA, lamB), (0.6, 0.01))]:
        ax.plot(x, y, "o", color=COLORS[0], ms=4.5)
        ax.text(x + off[0], y + off[1], lab, fontsize=10, fontweight="bold", color=COLORS[0])
    ax.text(19.5, 0.215, "$W$ = %.1f J per stroke" % W, ha="center", va="center", fontsize=9.5,
            color="#0A4F7A")
    ax.text(31, 0.23, "A→B: rotor moves\ntowards alignment\nat ≈ constant 30 A", fontsize=8, va="center")
    ax.text(15.5, 0.33, "B→O: switch-off;\nflux and current\nfall together", fontsize=8, va="center",
            ha="center")
    ax.text(35, 0.075, "O→A: switch-on,\ncurrent rises along\nthe unaligned curve", fontsize=8,
            va="top", ha="center")
    ax.text(39.5, 0.49, "anticlockwise loop = motoring\n24 strokes per revolution (3 phases × 8 rotor poles)",
            fontsize=8, ha="right", va="top")
    ax.set_xlim(-1.5, 40); ax.set_ylim(0, 0.5)
    ax.set_xlabel("phase current $i$ (A)")
    ax.set_ylabel(r"flux linkage $\lambda$ (Wb-turn)")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "03", "fig-3-2-srm-energy-conversion-loop")
    return n, W


# ----------------------------------------------------------------------------------------
# Figure 3.3 — rotating MMF
# ----------------------------------------------------------------------------------------
def fig_3_3():
    th = np.linspace(0, 360, 721)
    r = np.radians(th)
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = GridSpec(3, 2, width_ratios=[3.1, 1.0], hspace=0.22, wspace=0.08, figure=fig,
                  left=0.1, right=0.99, top=0.95, bottom=0.1)
    cols = [COLORS[0], COLORS[1], COLORS[2]]
    for row, wt in enumerate((0, 30, 60)):
        ax = fig.add_subplot(gs[row, 0])
        w = np.radians(wt)
        tot = np.zeros_like(r)
        for k, name in enumerate("abc"):
            ik = np.cos(w - k * 2 * np.pi / 3)
            Fk = ik * np.cos(r - k * 2 * np.pi / 3)
            tot += Fk
            ax.plot(th, Fk, color=cols[k], lw=1.0, label="$F_%s$" % name)
        ax.plot(th, tot, color=INK, lw=2.4, label="sum")
        ax.axhline(0, color=INK, lw=0.5)
        ax.axvline(wt, ls=":", color=INK, lw=0.9)
        ax.annotate("", xy=(wt + 28, 1.5), xytext=(wt, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
        ax.text(wt + 32, 1.5, "crest at %d°" % wt, fontsize=8, va="center")
        ax.text(352, -1.45, r"$\omega t$ = %d°" % wt, fontsize=9, ha="right", va="bottom",
                bbox=dict(fc="white", ec="none", pad=0.5))
        ax.set_xlim(0, 360); ax.set_ylim(-1.7, 1.75)
        ax.set_xticks(np.arange(0, 361, 60))
        ax.set_yticks([-1.5, 0, 1.5])
        if row < 2:
            ax.tick_params(labelbottom=False)
        if row == 1:
            ax.set_ylabel("MMF (per unit of one phase peak)")
        if row == 0:
            handles, labels = ax.get_legend_handles_labels()
    ax.set_xlabel(r"electrical angle around the gap $\theta$ (degrees)")
    lax = fig.add_subplot(gs[0, 1]); lax.axis("off")
    lax.legend(handles, ["$F_a$ (phase a)", "$F_b$ (phase b)", "$F_c$ (phase c)", "sum, amplitude 1.5"],
               fontsize=8, loc="center left")

    # stator axes and the rotating resultant
    ax = fig.add_subplot(gs[1:, 1])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-2.15, 1.4)
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, ec="#AAAAAA", lw=1.0))
    for k, name in enumerate("abc"):
        a = np.radians(120 * k)
        ax.plot([0, 1.12 * np.cos(a)], [0, 1.12 * np.sin(a)], color=cols[k], lw=1.0, ls="--")
        ax.text(1.22 * np.cos(a), 1.22 * np.sin(a), name, color=cols[k], fontsize=10,
                ha="center", va="center", fontweight="bold")
    for wt, alpha in ((0, 0.35), (30, 0.65), (60, 1.0)):
        a = np.radians(wt)
        ax.annotate("", xy=(0.85 * np.cos(a), 0.85 * np.sin(a)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8, alpha=alpha))
    th_ = np.radians(np.linspace(8, 80, 40))
    ax.plot(1.0 * np.cos(th_), 1.0 * np.sin(th_), color=INK, lw=1.0)
    ax.annotate("", xy=(np.cos(np.radians(86)), np.sin(np.radians(86))),
                xytext=(np.cos(np.radians(80)), np.sin(np.radians(80))),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0))
    ax.text(0, -1.72, "stator axes a, b, c;\nresultant MMF of\n1.5 × phase peak, drawn\nat $\\omega t$ = 0°, 30°, 60°",
            ha="center", va="center", fontsize=8)
    save(fig, "03", "fig-3-3-rotating-mmf")


# ----------------------------------------------------------------------------------------
# Figure 3.4 — core-loss data
# ----------------------------------------------------------------------------------------
def fig_3_4():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw=dict(width_ratios=[1.1, 1]))
    B = np.linspace(0.5, 1.8, 200)
    grades = [("M800-65A (8.0 W/kg)", 8.0, 1.5, 2.0, COLORS[1], 1.8),
              ("M400-50A (4.0 W/kg)", 4.0, 1.5, 2.0, COLORS[0], 1.8),
              ("M235-35A (2.35 W/kg)", 2.35, 1.5, 2.0, COLORS[2], 1.8)]
    for name, p0, B0, alpha, c, Bmax in grades:
        b = B[B <= Bmax]
        ax.plot(b, p0 * (b / B0) ** alpha, color=c, label=name)
        ax.plot(B0, p0, "o", color=c, ms=4)
    # grain-oriented: fitted through 0.75 W/kg at 1.5 T and 1.11 W/kg at 1.7 T
    a_go = np.log(1.11 / 0.75) / np.log(1.7 / 1.5)
    ax.plot(B, 0.75 * (B / 1.5) ** a_go, color=COLORS[3], label="GO M111-30P (slope %.1f)" % a_go)
    ax.plot([1.5, 1.7], [0.75, 1.11], "o", color=COLORS[3], ms=4)
    b = B[B <= 1.45]
    ax.plot(b, 0.15 * (b / 1.3) ** 2, color=COLORS[4], label="amorphous (0.15 W/kg at 1.3 T)")
    ax.plot(1.3, 0.15, "o", color=COLORS[4], ms=4)
    ax.legend(fontsize=7.3, loc="upper left", handlelength=1.4)
    ax.text(1.75, 0.03, "markers: catalogue values;\nlines: power laws through them", fontsize=7.3,
            ha="right", va="bottom", color="#555555")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.5, 1.8); ax.set_ylim(0.02, 60)
    ax.set_xticks([0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8])
    ax.set_xticklabels(["0.5", "0.6", "0.8", "1.0", "1.2", "1.5", "1.8"])
    ax.minorticks_off()
    ax.set_yticks([0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50])
    ax.set_yticklabels(["0.02", "0.05", "0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50"])
    ax.set_xlabel("peak flux density $\\hat B$ (T)")
    ax.set_ylabel("specific core loss at 50 Hz (W/kg)")
    ax.set_title("(a) loss versus flux density", loc="left", fontsize=10)

    f = np.linspace(0, 400, 200)
    kh, ke = 0.055, 5.0e-4
    rho, dens, d, Bp = 0.48e-6, 7650.0, 0.5e-3, 1.5
    kc = np.pi ** 2 * d ** 2 * Bp ** 2 / (6 * rho * dens)        # classical eddy: p_c/f = kc f
    tot = kh + ke * f
    cls = kh + kc * f
    bx.fill_between(f, 0, kh, color="#DDDDDD", lw=0)
    bx.fill_between(f, kh, cls, color=COLORS[5], alpha=0.35, lw=0)
    bx.fill_between(f, cls, tot, color=COLORS[1], alpha=0.25, lw=0)
    bx.plot(f, tot, color=INK, lw=1.8, label=r"measured fit $0.055 + 5.0\times10^{-4} f$")
    bx.plot(f, cls, "--", color=COLORS[0], lw=1.3,
            label=r"hysteresis + classical eddy ($%.2f\times10^{-4} f$)" % (kc * 1e4))
    bx.plot([50, 60], [0.080, 0.085], "o", color=INK, ms=5, zorder=5)
    bx.annotate("50 Hz: 0.080\n60 Hz: 0.085", xy=(55, 0.083), xytext=(70, 0.135), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.7))
    bx.text(250, 0.03, "hysteresis 0.055 J/kg", fontsize=8, ha="center", va="center")
    bx.text(330, 0.100, "classical\neddy", fontsize=8, ha="center", va="center", color="#1F5C80")
    bx.text(310, 0.188, "excess", fontsize=8.5, ha="center", va="center", color="#8A3A00")
    bx.set_xlim(0, 400); bx.set_ylim(0, 0.30)
    bx.set_xlabel("frequency $f$ (Hz)")
    bx.set_ylabel("loss per cycle $p/f$ (J/kg)")
    bx.legend(fontsize=7.3, loc="upper left")
    bx.set_title("(b) M400-50A at 1.5 T", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.2)
    save(fig, "03", "fig-3-4-core-loss-data")


# ----------------------------------------------------------------------------------------
# Figure 3.5 — efficiency versus load
# ----------------------------------------------------------------------------------------
def fig_3_5():
    Pr, P0, Pv = 75.0, 1.2, 2.0
    x = np.linspace(0.02, 1.25, 500)
    eta = 100 * Pr * x / (Pr * x + P0 + Pv * x ** 2)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(x, np.full_like(x, P0), color=COLORS[2], lw=1.3, label="constant loss 1.2 kW")
    ax2.plot(x, Pv * x ** 2, color=COLORS[1], lw=1.3, label=r"variable loss $2.0x^2$ kW")
    ax2.plot(x, P0 + Pv * x ** 2, color=COLORS[3], lw=1.3, ls="--", label="total loss")
    ax2.set_ylim(0, 5)
    ax2.set_ylabel("losses (kW)")
    ax.plot(x, eta, color=COLORS[0], lw=2.4, label="efficiency")
    xm = np.sqrt(P0 / Pv)
    ax.axvline(xm, ls="--", color=INK, lw=0.9)
    for lvl, nm in ((94.0, "IE2 94.0 %"), (95.0, "IE3 95.0 %"), (96.0, "IE4 96.0 %")):
        ax.axhline(lvl, ls=":", color="#777777", lw=1.0)
        ax.text(0.03, lvl + 0.07, nm, fontsize=7.8, color="#555555", va="bottom")
    for xk in (0.25, 0.5, xm, 1.0, 1.25):
        ek = 100 * Pr * xk / (Pr * xk + P0 + Pv * xk ** 2)
        ax.plot(xk, ek, "o", color=COLORS[0], ms=4.5, zorder=5)
        ax.text(xk + (0.02 if xk < 1.2 else -0.02), ek - 0.25, "%.1f" % ek, fontsize=7.8,
                ha="left" if xk < 1.2 else "right", va="top", color=COLORS[0])
    ax.text(xm + 0.015, 89.2, "$x$ = %.3f:\nvariable = constant\nloss (1.2 kW each)" % xm, fontsize=8,
            va="center")
    ax.set_xlim(0, 1.25); ax.set_ylim(85, 97)
    ax.set_xlabel("load fraction $x$ (output / 75 kW)")
    ax.set_ylabel("efficiency (%)", color=COLORS[0])
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.8, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    save(fig, "03", "fig-3-5-efficiency-versus-load")


# ----------------------------------------------------------------------------------------
# Figure 3.6 — thermal transient of the EV motor
# ----------------------------------------------------------------------------------------
def fig_3_6():
    Tcool, Tlim = 65.0, 180.0
    Rth = 115 / 4000.0
    Cth = 25 * 500.0
    tau = Rth * Cth
    t = np.linspace(0, 400, 2001)
    single = lambda P, T0: Tcool + P * Rth + (T0 - Tcool - P * Rth) * np.exp(-t / tau)
    T1 = single(4000, Tcool)
    T2 = single(12000, 135.0)
    T3 = single(12000, Tcool)
    # two-node model: copper (8 kg x 385 J/kgK, 20 s to the iron) + iron/rest, same total R and C
    Cc = 8 * 385.0
    Rci = 20.0 / Cc
    Ci = Cth - Cc
    Ria = Rth - Rci
    fr = 0.85                         # share of the 12 kW dissipated in the copper
    P0 = 70 / (fr * Rci + Ria)        # steady state that gives a 70 K winding rise
    y0 = [70.0, P0 * Ria]

    def rhs(_, y):
        q = (y[0] - y[1]) / Rci
        return [(fr * 12000 - q) / Cc, (q + (1 - fr) * 12000 - y[1] / Ria) / Ci]
    sol = solve_ivp(rhs, (0, 400), y0, t_eval=t, max_step=0.2)
    T4 = Tcool + sol.y[0]

    def t_hit(T):
        k = np.argmax(T >= Tlim)
        return t[k] if T[k] >= Tlim else np.nan

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.axhline(Tlim, ls="--", color=COLORS[1], lw=1.0)
    ax.text(398, Tlim + 1.5, "180 °C Class H limit", ha="right", va="bottom", fontsize=8, color=COLORS[1])
    ax.axhline(Tcool, ls="--", color="#777777", lw=1.0)
    ax.text(398, Tcool + 1.5, "65 °C coolant", ha="right", va="bottom", fontsize=8, color="#555555")
    m2 = T2 <= Tlim + 15
    m3 = T3 <= Tlim + 15
    m4 = T4 <= Tlim + 15
    ax.plot(t, T1, color=COLORS[0], label="1: 4.0 kW continuous, from cold (single node)")
    ax.plot(t[m2], T2[m2], color=COLORS[3], label="2: 12 kW peak from 135 °C (single node)")
    ax.plot(t[m3], T3[m3], color=COLORS[2], label="3: 12 kW peak from cold (single node)")
    ax.plot(t[m4], T4[m4], "--", color=INK, label="4: 12 kW from 135 °C, copper hot spot (two node)")
    for T, c in ((T2, COLORS[3]), (T3, COLORS[2]), (T4, INK)):
        th_ = t_hit(T)
        ax.plot(th_, Tlim, "o", color=c, ms=5, zorder=5)
        ax.text(th_ + 3, Tlim - 3, "%.0f s" % th_, color=c, fontsize=8, ha="left", va="top")
    ax.text(400, T1[-1] - 3, "%.0f °C\nat 400 s" % T1[-1], fontsize=8, ha="right", va="top", color=COLORS[0])
    ax.text(150, 128, r"single node: $\tau$ = $R_{th}C_{th}$ = %.0f s" % tau, fontsize=8.5, color=COLORS[0])
    ax.annotate(r"copper $\tau\approx$ 20 s", xy=(16, 166), xytext=(48, 148), fontsize=8.5, color=INK,
                ha="left", va="center", arrowprops=dict(arrowstyle="-", lw=0.7))
    ax.set_xlim(0, 400); ax.set_ylim(60, 200)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("winding temperature (°C)")
    ax.legend(fontsize=7.6, loc="lower right", bbox_to_anchor=(1.0, 0.06))
    save(fig, "03", "fig-3-6-thermal-transient-ev-motor")
    return t_hit(T2), t_hit(T3), t_hit(T4), T1[-1]


if __name__ == "__main__":
    fig_3_1()
    print("SRM return-path exponent and area:", fig_3_2())
    fig_3_3()
    fig_3_4()
    fig_3_5()
    print("thermal times:", fig_3_6())
