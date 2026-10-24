"""Figures for Chapter 2 — Electromagnetic Induction.

Run from the repository root:  python figures/scripts/ch02.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon

from figstyle import save, COLORS, INK, box, arrow

IRON = "#C9D3DE"
IRON_EC = "#5A6878"
CU = "#E69F00"
CU_EC = "#8A5A00"


def _arr(ax, x0, y0, x1, y1, color=INK, lw=1.3, ms=11, ls="-", z=6):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, zorder=z))


# ----------------------------------------------------------------------------------------
# Figure 2.1 — transformer EMF and speed EMF
# ----------------------------------------------------------------------------------------
def fig_2_1():
    fig = plt.figure(figsize=(6.8, 3.4))
    axa = fig.add_axes([0.0, 0.19, 0.54, 0.81])
    axb = fig.add_axes([0.56, 0.19, 0.44, 0.81])
    for ax in (axa, axb):
        ax.set_aspect("equal"); ax.axis("off")

    # (a) core with primary and 1-turn search loop
    ax = axa
    ax.set_xlim(-3.0, 7.6); ax.set_ylim(-0.4, 7.0)
    ax.add_patch(Rectangle((0, 0), 4.4, 4.0, fc=IRON, ec=IRON_EC, lw=1.2))
    ax.add_patch(Rectangle((1.0, 1.0), 2.4, 2.0, fc="white", ec=IRON_EC, lw=1.2))
    for yy in np.linspace(0.15, 0.85, 4):
        ax.plot([0.15, 4.25], [yy, yy], color="white", lw=0.5)
        ax.plot([0.15, 4.25], [4 - yy, 4 - yy], color="white", lw=0.5)
    for yy in np.linspace(1.15, 2.85, 7):
        ax.add_patch(Rectangle((-0.12, yy - 0.09), 1.24, 0.18, fc=CU, ec=CU_EC, lw=0.6, zorder=3))
    ax.plot([-0.12, -1.4, -1.4], [2.85, 2.85, 2.35], color=INK, lw=1.1)
    ax.plot([-0.12, -1.4, -1.4], [1.15, 1.15, 1.65], color=INK, lw=1.1)
    ax.add_patch(Circle((-1.4, 2.0), 0.35, fc="white", ec=INK, lw=1.2, zorder=4))
    tt = np.linspace(-0.22, 0.22, 40)
    ax.plot(-1.4 + tt, 2.0 + 0.12 * np.sin(tt / 0.22 * np.pi), color=INK, lw=1.0, zorder=5)
    ax.text(-1.85, 2.0, "50 Hz\nsupply", ha="right", va="center", fontsize=8.5)
    ax.text(-0.6, 3.15, "primary", ha="center", va="bottom", fontsize=8)
    # one-turn search loop on the right limb, leads to a voltmeter
    ax.add_patch(Rectangle((3.3, 1.92), 1.22, 0.16, fc="#D55E00", ec="#7A3400", lw=0.6, zorder=3))
    red = "#D55E00"
    ax.plot([4.52, 4.95, 4.95, 5.75, 5.75], [2.08, 2.08, 2.75, 2.75, 2.36], color=red, lw=1.1)
    ax.plot([4.52, 4.95, 4.95, 5.75, 5.75], [1.92, 1.92, 1.25, 1.25, 1.64], color=red, lw=1.1)
    ax.add_patch(Circle((5.75, 2.0), 0.36, fc="white", ec=INK, lw=1.2, zorder=4))
    ax.text(5.75, 2.0, "V", ha="center", va="center", fontsize=10, zorder=5)
    ax.text(6.2, 2.0, "10.0 V\nrms", ha="left", va="center", fontsize=8.5)
    ax.text(5.35, 1.1, "1-turn search loop", ha="center", va="top", fontsize=8)
    for (x0, y0, x1, y1) in [(1.5, 3.5, 2.9, 3.5), (3.9, 3.0, 3.9, 2.4), (2.9, 0.5, 1.5, 0.5)]:
        _arr(ax, x0, y0, x1, y1, color=COLORS[0], lw=1.4)
    ax.text(2.2, 3.62, r"$\Phi(t)$", color=COLORS[0], ha="center", va="bottom", fontsize=9.5,
            bbox=dict(fc=IRON, ec="none", pad=0.2))
    # inset: Phi(t), placed above the core
    ins = ax.inset_axes([1.0, 4.85, 4.6, 1.9], transform=ax.transData)
    t = np.linspace(0, 40, 400)
    ins.plot(t, 45 * np.sin(2 * np.pi * 50 * t / 1000), color=COLORS[0], lw=1.2)
    ins.axhline(0, color=INK, lw=0.5)
    ins.set_xlim(0, 40); ins.set_ylim(-55, 55)
    ins.set_yticks([-45, 0, 45]); ins.set_xticks([0, 20, 40])
    ins.tick_params(labelsize=7, length=2)
    ins.set_xlabel("t (ms)", fontsize=7, labelpad=1)
    ins.set_ylabel(r"$\Phi$ (mWb)", fontsize=7, labelpad=1)

    # (b) conductor moving through a uniform field into the page
    ax = axb
    ax.set_xlim(-0.3, 6.0); ax.set_ylim(-0.4, 5.6)
    ax.add_patch(Rectangle((0, 0.2), 5.6, 4.4, fc="#F2F5F9", ec="none"))
    xc = 2.3
    keep_clear = [(xc - 1.15, xc + 0.4, 0.4, 4.3), (xc + 0.25, xc + 2.1, 1.9, 2.8),
                  (xc + 0.2, xc + 1.6, 2.7, 3.9), (2.85, 5.6, 0.25, 1.75)]
    for xx in np.arange(0.3, 5.6, 0.55):
        for yy in np.arange(0.45, 4.6, 0.55):
            if any(a <= xx <= b and c <= yy <= d for a, b, c, d in keep_clear[:1]):
                continue
            ax.text(xx, yy, "×", ha="center", va="center", fontsize=8, color="#7A8796")
    ax.text(5.6, 4.72, r"$\mathbf{B}$ = 0.9 T into the page", ha="right", va="bottom", fontsize=8.5)
    ax.add_patch(Rectangle((xc - 0.1, 0.6), 0.2, 3.4, fc=CU, ec=CU_EC, lw=0.8, zorder=4))
    ax.text(xc - 0.25, 3.9, "+", ha="right", va="center", fontsize=14, color=COLORS[1], zorder=5)
    ax.text(xc - 0.25, 0.75, "−", ha="right", va="center", fontsize=14, color=COLORS[1], zorder=5)
    ax.annotate("", xy=(xc - 0.75, 4.0), xytext=(xc - 0.75, 0.6),
                arrowprops=dict(arrowstyle="<->", lw=0.7, color=INK))
    ax.text(xc - 0.85, 2.3, "$l$ = 0.15 m", rotation=90, ha="right", va="center", fontsize=8.5)
    _arr(ax, xc + 0.25, 2.1, xc + 1.8, 2.1, color=COLORS[2], lw=1.6)
    ax.text(xc + 1.0, 2.22, r"$\mathbf{v}$ = 50.3 m/s", ha="center", va="bottom", fontsize=8.5,
            color=COLORS[2], zorder=7, bbox=dict(fc="#F2F5F9", ec="none", pad=0.4))
    _arr(ax, xc + 0.35, 2.95, xc + 0.35, 3.85, color=COLORS[3], lw=1.6)
    ax.text(xc + 0.5, 3.4, r"$\mathbf{v}\times\mathbf{B}$", ha="left", va="center", fontsize=9,
            color=COLORS[3], zorder=7, bbox=dict(fc="#F2F5F9", ec="none", pad=0.4))
    ax.text(4.2, 1.0, "$e = Blv$\n= 0.9 × 0.15 × 50.3\n= 6.79 V (peak)", ha="center", va="center",
            fontsize=8.5, bbox=dict(fc="white", ec=INK, lw=0.6, pad=3), zorder=7)

    # captions under both panels, aligned
    fig.text(0.27, 0.15, "(a) transformer EMF", ha="center", va="top", fontsize=9.5, fontweight="bold")
    fig.text(0.27, 0.07, r"$d\lambda/dt$ from $di/dt$:  $E = 4.44\,fN\Phi_m$, $\Phi_m$ = 45 mWb",
             ha="center", va="top", fontsize=8.5)
    fig.text(0.78, 0.15, "(b) speed EMF", ha="center", va="top", fontsize=9.5, fontweight="bold")
    fig.text(0.78, 0.07, r"$d\lambda/dt$ from $d\theta/dt$:  $e = Blv$", ha="center", va="top",
             fontsize=8.5)
    save(fig, "02", "fig-2-1-transformer-and-speed-emf")


# ----------------------------------------------------------------------------------------
# Figure 2.2 — contactor lambda-i curves
# ----------------------------------------------------------------------------------------
def fig_2_2():
    Lc, Lo = 14.0, 1.32
    lam_m = np.sqrt(2) * 230 / (2 * np.pi * 50)
    i1 = 1.1 / Lc

    def lam_closed(i):
        i = np.asarray(i, float)
        return np.where(i <= i1, Lc * i, 1.1 + 0.2 * np.tanh(Lc * (i - i1) / 0.2))

    i = np.linspace(0, 0.8, 800)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    lc_ = lam_closed(i)
    lo_ = Lo * i
    # shaded area between the curves up to lambda_m
    lam = np.linspace(0, lam_m, 300)
    i_closed = lam / Lc
    i_open = lam / Lo
    ax.fill_betweenx(lam, i_closed, i_open, color=COLORS[5], alpha=0.25, lw=0)
    ax.plot(i, lc_, color=COLORS[0], label="armature closed")
    ax.plot(i, lo_, color=COLORS[1], label="armature open")
    ax.axhline(lam_m, ls="--", color=INK, lw=0.9)
    ax.text(0.79, lam_m + 0.02, r"$\lambda_m$ = %.2f Wb-turn, set by 230 V, 50 Hz" % lam_m,
            ha="right", va="bottom", fontsize=8.5)
    # operating points
    ic = lam_m / Lc
    ax.plot(ic, lam_m, "o", color=COLORS[0], ms=6, zorder=5)
    ax.annotate("closed: 0.074 A peak\n(0.052 A rms)", xy=(ic, lam_m), xytext=(0.10, 1.25),
                fontsize=8.5, color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[0]))
    # open: the coil resistance takes part of the voltage (Z = 441 ohm, X = 415 ohm)
    io = np.sqrt(2) * 0.52
    lo_op = Lo * io
    ax.plot(io, lo_op, "o", color=COLORS[1], ms=6, zorder=5)
    ax.plot(lam_m / Lo, lam_m, "o", mfc="white", mec=COLORS[1], ms=5, zorder=5)
    ax.annotate("0.79 A if $R$\nis neglected", xy=(lam_m / Lo, lam_m), xytext=(0.66, 1.18),
                fontsize=7.5, color=COLORS[1], ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[1]))
    ax.annotate("open: 0.74 A peak (0.52 A rms)\nat $\\lambda$ = %.2f Wb-turn, because\n150 Ω takes part of the voltage" % lo_op,
                xy=(io, lo_op), xytext=(0.45, 0.42), fontsize=8.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    ax.text(0.035, 0.30, "slope\n14.0 H", fontsize=8.5, color=COLORS[0], ha="left")
    ax.text(0.30, 0.30, "slope 1.32 H", fontsize=8.5, color=COLORS[1], rotation=0, ha="left")
    ax.text(0.30, 0.72, "energy available for\nmechanical work during\nclosing (Chapter 3)",
            fontsize=8, ha="center", va="center", color="#1F5C80")
    ax.set_xlim(0, 0.8); ax.set_ylim(0, 1.4)
    ax.set_xlabel("coil current $i$ (A)")
    ax.set_ylabel(r"flux linkage $\lambda$ (Wb-turn)")
    ax.legend(loc="lower right", fontsize=8.5)
    save(fig, "02", "fig-2-2-contactor-lambda-i-curves")


# ----------------------------------------------------------------------------------------
# Figure 2.3 — coupling-field energy balance
# ----------------------------------------------------------------------------------------
def fig_2_3():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    ax.set_xlim(0, 17); ax.set_ylim(-0.4, 9.2)
    ax.set_aspect("equal"); ax.axis("off")
    yb, yt = 2.0, 4.6
    ym = (yb + yt) / 2
    LOSS = COLORS[1]
    # electrical side: source, series R, shunt core-loss resistance
    ax.add_patch(Circle((0.9, ym), 0.55, fc="white", ec=INK, lw=1.2, zorder=4))
    ax.text(0.9, ym, "$v$", ha="center", va="center", fontsize=11, zorder=5)
    ax.plot([0.9, 0.9, 1.8], [ym + 0.55, yt, yt], color=INK, lw=1.2)
    ax.plot([0.9, 0.9], [ym - 0.55, yb], color=INK, lw=1.2)
    ax.add_patch(Rectangle((1.8, yt - 0.3), 1.6, 0.6, fc="#FBE3D3", ec=INK, lw=1.2, zorder=3))
    ax.text(2.6, yt - 0.45, "winding $R$\n(copper loss)", ha="center", va="top", fontsize=8)
    ax.plot([3.4, 6.0], [yt, yt], color=INK, lw=1.2)
    ax.plot([0.9, 6.0], [yb, yb], color=INK, lw=1.2)
    ax.plot([4.5, 4.5], [yt, yb + 2.05], color=INK, lw=1.2)
    ax.add_patch(Rectangle((4.2, yb + 0.55), 0.6, 1.5, fc="#FBE3D3", ec=INK, lw=1.2, zorder=3))
    ax.plot([4.5, 4.5], [yb, yb + 0.55], color=INK, lw=1.2)
    ax.text(4.5, yb - 0.2, "core-loss\nresistance", ha="center", va="top", fontsize=8)
    _arr(ax, 1.15, yt + 0.25, 1.65, yt + 0.25, lw=1.0, ms=8)
    ax.text(1.4, yt + 0.35, "$i$", fontsize=9, ha="center", va="bottom")
    ax.text(5.55, ym, "$e$", fontsize=10, ha="center", va="center")
    ax.text(5.55, yt - 0.35, "+", fontsize=10, ha="center", va="center")
    ax.text(5.55, yb + 0.35, "−", fontsize=11, ha="center", va="center")
    # coupling field
    box(ax, 6.0, 1.3, 4.0, 4.0, "", fc="#E3EEF8")
    ax.text(8.0, 3.3, "lossless\nmagnetic\ncoupling field\n\nstored energy\n$W_{fld}(\\lambda,\\theta)$",
            ha="center", va="center", fontsize=8.5)
    # shaft (behind the boxes) and mechanical blocks
    ax.plot([10.0, 16.8], [3.3, 3.3], color="#555555", lw=3.0, solid_capstyle="butt", zorder=0.5)
    box(ax, 11.0, 2.45, 1.7, 1.7, "friction\nand\nwindage", fc="#FBE3D3", fontsize=8)
    box(ax, 13.1, 2.45, 1.5, 1.7, "inertia\n$J$", fc="#EEF3F8", fontsize=8.5)
    box(ax, 15.0, 2.45, 1.7, 1.7, "load\ntorque\n$T_L$", fc="#EEF3F8", fontsize=8.5)
    ax.text(10.5, 3.5, r"$T,\ \omega$", fontsize=9, ha="center", va="bottom")
    ax.text(13.85, 4.3, r"$J\omega\,d\omega/dt$", ha="center", va="bottom", fontsize=8.5)
    # losses leaving as heat
    for xh, y0, lab in [(2.6, yt + 0.35, "$Ri^2$"), (4.5, yt + 0.1, "core\nloss"), (11.85, 4.25, r"$b\omega^2$")]:
        _arr(ax, xh, y0, xh, 6.0, color=LOSS, lw=1.2, ms=9)
        ax.text(xh + 0.15, 5.35, lab, ha="left", va="center", fontsize=8, color=LOSS)
    ax.text(3.6, 6.25, "heat", ha="center", va="bottom", fontsize=8, color=LOSS)
    # field storage
    _arr(ax, 8.0, 6.3, 8.0, 5.4, lw=1.0, ms=8)
    ax.text(8.2, 5.85, r"$dW_{fld}/dt$", ha="left", va="center", fontsize=8.5)
    # power flow: solid = motor, dashed = generator (reversed)
    ym_, yg_ = 7.75, 7.1
    pw = [(0.2, 1.7, "$vi$"), (5.0, 6.4, "$ei$"), (10.0, 11.5, r"$T\omega$"), (15.0, 16.6, r"$T_L\omega$")]
    for x0, x1, lab in pw:
        _arr(ax, x0, ym_, x1, ym_, color=COLORS[0], lw=1.8)
        ax.text((x0 + x1) / 2, ym_ + 0.15, lab, ha="center", va="bottom", fontsize=10, color=COLORS[0])
        _arr(ax, x1, yg_, x0, yg_, color=INK, lw=1.0, ls="--", ms=9)
    ax.text(3.35, ym_, "motor", ha="center", va="center", fontsize=8, color=COLORS[0])
    ax.text(3.35, yg_, "generator", ha="center", va="center", fontsize=8, color=INK)
    ax.text(2.9, 9.1, "electrical port", ha="center", va="top", fontsize=9, fontweight="bold")
    ax.text(13.8, 9.1, "mechanical port", ha="center", va="top", fontsize=9, fontweight="bold")
    ax.text(8.5, 0.15,
            "1 MW pump motor at rated load:  input 1047 kW  →  losses ≈ 47 kW  →  shaft 1000 kW",
            ha="center", va="center", fontsize=8.5, bbox=dict(fc="#F4F6F9", ec=INK, lw=0.6, pad=4))
    save(fig, "02", "fig-2-3-coupling-field-energy-balance")


# ----------------------------------------------------------------------------------------
# Figure 2.4 — inductances and torque versus angle
# ----------------------------------------------------------------------------------------
def fig_2_4():
    th = np.linspace(0, 360, 1441)
    r = np.radians(th)
    L = 0.175 + 0.075 * np.cos(2 * r)
    M = 0.8 * np.cos(r)
    is_, if_ = 10.0, 20.0
    Trel = -0.075 * is_ ** 2 * np.sin(2 * r)
    Tal = -0.8 * is_ * if_ * np.sin(r)
    T = Trel + Tal
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 4.8), sharex=True,
                                   gridspec_kw=dict(height_ratios=[1, 1.25]))
    ax1.plot(th, L, color=COLORS[0], label=r"$L(\theta) = 0.175 + 0.075\cos2\theta$")
    ax1.plot(th, M, color=COLORS[1], label=r"$M(\theta) = 0.8\cos\theta$")
    ax1.axhline(0, color=INK, lw=0.6)
    ax1.set_ylabel("inductance (H)")
    ax1.set_ylim(-1.0, 1.0)
    ax1.legend(fontsize=8.5, loc="lower left", ncol=2, bbox_to_anchor=(0, -0.02))
    ax1.set_title("(a) stator self-inductance and stator–rotor mutual inductance", loc="left", fontsize=10)
    ax1.text(128, 0.04, "$L_q$ = 0.10 H", fontsize=8, ha="center", va="top", color=COLORS[0])
    ax1.text(180, 0.30, "$L_d$ = 0.25 H", fontsize=8, ha="center", color=COLORS[0])

    ax2.plot(th, Trel, ":", color=COLORS[2], lw=1.8, label=r"reluctance $-7.5\sin2\theta$")
    ax2.plot(th, Tal, "--", color=COLORS[1], lw=1.5, label=r"alignment $-160\sin\theta$")
    ax2.plot(th, T, color=INK, lw=1.9, label="total")
    ax2.axhline(0, color=INK, lw=0.6)
    k = np.argmin(T)
    ax2.plot(th[k], T[k], "o", color=INK, ms=5)
    ax2.annotate("minimum −%.1f N·m at %.0f°" % (abs(T[k]), th[k]), xy=(th[k], T[k]), xytext=(100, -172),
                 fontsize=8.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.7))
    ax2.plot(0, 0, "s", color=COLORS[2], ms=6, clip_on=False, zorder=5)
    ax2.annotate("stable equilibrium\n$\\theta$ = 0", xy=(0, 0), xytext=(14, 60), fontsize=8.5,
                 arrowprops=dict(arrowstyle="-", lw=0.7))
    ax2.set_ylim(-180, 180)
    ax2.set_yticks([-180, -90, 0, 90, 180])
    ax2.set_ylabel("torque (N·m)")
    ax2.set_xlabel(r"rotor angle $\theta$ (electrical degrees)")
    ax2.set_xlim(0, 360); ax2.set_xticks(np.arange(0, 361, 45))
    ax2.legend(fontsize=8.5, loc="lower right")
    ax2.set_title(r"(b) torque, $i_s$ = 10 A, $i_f$ = 20 A", loc="left", fontsize=10)
    fig.tight_layout(h_pad=0.8)
    save(fig, "02", "fig-2-4-inductances-and-torque-vs-angle")


# ----------------------------------------------------------------------------------------
# Figure 2.5 — residual voltage after disconnection
# ----------------------------------------------------------------------------------------
def residual_model(t):
    J, P, n_r = 30.0, 1e6, 1490.0
    w0 = 2 * np.pi * n_r / 60
    T0 = P / w0
    a = T0 / (J * w0)                       # 1.37 1/s
    speed = 1 / (1 + a * t)
    flux = np.exp(-t / 1.0)
    v = speed * flux
    f0 = 50 * n_r / 1500                    # rotor electrical frequency at 1490 rpm
    freq = f0 * speed
    slip = 2 * np.pi * (50 * t - f0 * np.log(1 + a * t) / a)    # phase lag behind supply (rad)
    return speed, flux, v, freq, slip, a


def fig_2_5():
    t = np.linspace(0, 0.6, 601)
    speed, flux, v, freq, slip, a = residual_model(t)
    fig = plt.figure(figsize=(6.8, 3.7))
    ax = fig.add_axes([0.08, 0.14, 0.40, 0.74])
    ax.plot(t, speed, color=COLORS[2], label=r"speed $1/(1+%.2f\,t)$" % a)
    ax.plot(t, flux, color=COLORS[3], ls="--", label=r"flux $e^{-t/1.0\,\mathrm{s}}$")
    ax.plot(t, v, color=COLORS[0], lw=2.2, label="residual voltage")
    pos = {0.05: (0.045, 0.86, "right", "top"), 0.1: (0.095, 0.77, "right", "top"),
           0.2: (0.205, 0.665, "left", "bottom"), 0.5: (0.5, 0.33, "center", "top")}
    for tk in (0.05, 0.1, 0.2, 0.5):
        vk = np.interp(tk, t, v)
        ax.plot(tk, vk, "o", ms=4, color=COLORS[0], zorder=5)
        x_, y_, ha, va = pos[tk]
        ax.text(x_, y_, "%.2f" % vk, fontsize=7.5, color=COLORS[0], ha=ha, va=va)
    axf = ax.twinx()
    axf.spines["right"].set_visible(True)
    axf.plot(t, freq, color=COLORS[4], lw=1.2, ls="-.")
    axf.set_ylim(25, 50)
    axf.set_ylabel("frequency (Hz)", color=COLORS[4])
    axf.tick_params(axis="y", colors=COLORS[4])
    for tk in (0.05, 0.1):
        axf.plot(tk, np.interp(tk, t, freq), "s", ms=3.5, color=COLORS[4], zorder=5)
    f05, f10 = np.interp(0.05, t, freq), np.interp(0.1, t, freq)
    ax.text(0.59, 1.06, "frequency: %.1f Hz at 50 ms,\n%.1f Hz at 100 ms (squares)" % (f05, f10),
            ha="right", va="top", fontsize=7.5, color="#A06A00")
    ax.set_xlim(0, 0.6); ax.set_ylim(0, 1.1)
    ax.set_xlabel("time after disconnection (s)")
    ax.set_ylabel("per unit")
    h1, l1 = ax.get_legend_handles_labels()
    h1.append(plt.Line2D([], [], color=COLORS[4], lw=1.2, ls="-.")); l1.append("frequency (right axis)")
    ax.legend(h1, l1, fontsize=7.5, loc="lower left")
    fig.text(0.08, 0.95, "(a) magnitude and frequency", fontsize=10, va="bottom")

    # (b) phasor plane, supply phasor 1∠0 along +x
    axp = fig.add_axes([0.575, 0.04, 0.425, 0.88])
    axp.set_aspect("equal")
    axp.set_xlim(-1.05, 2.4); axp.set_ylim(-1.45, 1.65)
    axp.axis("off")
    axp.add_patch(Circle((1.0, 0.0), 1.33, fc=COLORS[2], alpha=0.12, ec=COLORS[2], lw=1.0, ls="--"))
    axp.text(1.0, 1.37, "acceptance: |ΔV| ≤ 1.33 pu (ANSI C50.41)", fontsize=7.5, color="#00704F",
             ha="center", va="bottom")
    axp.plot([-1.0, 2.35], [0, 0], color="#AAAAAA", lw=0.5)
    axp.plot([0, 0], [-1.1, 1.1], color="#AAAAAA", lw=0.5)
    axp.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.8, color=INK))
    axp.text(1.05, 0.06, "supply 1∠0°", fontsize=7.8, ha="left", va="bottom")
    ts = np.linspace(0, 0.2, 401)
    _, _, vs, _, ss, _ = residual_model(ts)
    z = vs * np.exp(-1j * ss)
    axp.plot(z.real, z.imag, color=COLORS[0], lw=1.0)
    off = {0.05: (0.05, -0.12), 0.10: (-0.30, -0.14), 0.15: (-0.30, 0.06), 0.20: (0.06, -0.08)}
    for tk in (0.05, 0.10, 0.15, 0.20):
        _, _, vk, _, sk, _ = residual_model(np.array([tk]))
        zk = vk[0] * np.exp(-1j * sk[0])
        axp.annotate("", xy=(zk.real, zk.imag), xytext=(0, 0),
                     arrowprops=dict(arrowstyle="-|>", lw=1.0, color=COLORS[0]))
        axp.text(zk.real + off[tk][0], zk.imag + off[tk][1], "%d ms" % round(tk * 1000), fontsize=7.5,
                 color=COLORS[0])
    for tk, c, tx, ty in ((0.05, "#00704F", 1.25, -0.42), (0.10, COLORS[1], -1.0, -1.15)):
        _, _, vk, _, sk, _ = residual_model(np.array([tk]))
        zk = vk[0] * np.exp(-1j * sk[0])
        axp.plot([zk.real, 1.0], [zk.imag, 0.0], color=c, lw=1.4)
        d = abs(1 - zk)
        lab = "%.2f pu, inside" % d if tk == 0.05 else "%.1f pu, outside" % d
        axp.text(tx, ty, "ΔV(%d ms) = %s" % (round(tk * 1000), lab), fontsize=7.5, color=c,
                 ha="left", va="center")
    axp.text(-0.6, -0.3, "lag grows\nclockwise", fontsize=7, color=COLORS[0], ha="center")
    fig.text(0.575, 0.95, "(b) residual-voltage phasor relative to the supply", fontsize=10, va="bottom")
    save(fig, "02", "fig-2-5-residual-voltage-after-disconnection")


if __name__ == "__main__":
    fig_2_1()
    fig_2_2()
    fig_2_3()
    fig_2_4()
    fig_2_5()
