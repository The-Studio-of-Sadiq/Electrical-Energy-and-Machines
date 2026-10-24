"""Figures for Chapter 27 — Grid Integration of Renewable Energy.

Run from the repository root:  python figures/scripts/ch27.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

CH = "27"


def line(ax, xs, ys, color=INK, lw=1.2, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def coil_h(ax, x0, x1, y, n=4, color=INK):
    """Horizontal inductor between x0 and x1 at height y."""
    r = (x1 - x0) / (2 * n)
    for k in range(n):
        ax.add_patch(Arc((x0 + r * (2 * k + 1), y), 2 * r, 2 * r, theta1=0, theta2=180,
                         ec=color, lw=1.2))


# ----------------------------------------------------------------------------
# Figure 27.1
# ----------------------------------------------------------------------------
def fig_27_1():
    """Control structure of a grid-following inverter."""
    fig, ax = schematic(6.8, 4.75, xlim=(0, 17), ylim=(0.6, 12.4))
    fs = 7
    SIG = "#1f4e79"
    PLLc = COLORS[3]
    yP = 10.8
    # ---- power stage
    box(ax, 0.1, 10.1, 1.8, 1.4, "PV array\nor battery", fc="#FFF3D6", fontsize=fs)
    line(ax, [1.9, 3.3], [11.2, 11.2])
    line(ax, [1.9, 3.3], [10.4, 10.4])
    xc = 2.6
    line(ax, [xc, xc], [11.2, 10.88])
    line(ax, [xc - 0.25, xc + 0.25], [10.88, 10.88], lw=1.6)
    line(ax, [xc - 0.25, xc + 0.25], [10.72, 10.72], lw=1.6)
    line(ax, [xc, xc], [10.72, 10.4])
    ax.text(xc, 10.25, "$C_{dc}$\n1100 V", fontsize=6.5, ha="center", va="top")
    box(ax, 3.3, 10.1, 1.8, 1.4, "two-level\nVSC", fc="#E3ECF6", fontsize=fs)
    line(ax, [5.1, 5.6], [yP, yP])
    coil_h(ax, 5.6, 6.8, yP)
    ax.text(6.2, yP + 0.45, "$L_1$ 0.10 pu", fontsize=fs, ha="center", va="bottom")
    line(ax, [6.8, 7.6], [yP, yP])
    line(ax, [7.2, 7.2], [yP, yP - 0.35])
    line(ax, [6.95, 7.45], [yP - 0.35, yP - 0.35], lw=1.6)
    line(ax, [6.95, 7.45], [yP - 0.5, yP - 0.5], lw=1.6)
    line(ax, [7.2, 7.2], [yP - 0.5, yP - 0.75])
    ax.text(7.2, yP - 0.85, "$C_f$ 0.05 pu", fontsize=fs, ha="center", va="top")
    coil_h(ax, 7.6, 8.8, yP)
    ax.text(8.2, yP + 0.45, "$L_2$ 0.05 pu", fontsize=fs, ha="center", va="bottom")
    ax.text(7.2, 12.2, "LCL filter", fontsize=fs, ha="center", va="top", style="italic")
    line(ax, [8.8, 10.2], [yP, yP])
    ax.add_patch(Circle((10.45, yP), 0.3, fill=False, ec=INK, lw=1.2))
    ax.add_patch(Circle((10.85, yP), 0.3, fill=False, ec=INK, lw=1.2))
    ax.text(10.65, yP + 0.45, "0.69/33 kV", fontsize=fs, ha="center", va="bottom")
    line(ax, [11.15, 11.9], [yP, yP])
    ax.add_patch(Circle((12.25, yP), 0.35, fc="white", ec=INK, lw=1.2))
    ax.text(12.25, yP, "~", fontsize=11, ha="center", va="center")
    ax.text(12.25, yP - 0.5, "grid", fontsize=fs, ha="center", va="top")
    # measurement points
    xi, xv = 9.25, 9.65
    ax.add_patch(Circle((xi, yP), 0.13, fill=False, ec=SIG, lw=1.1))
    ax.plot([xv], [yP], "o", color=SIG, ms=3.5)
    line(ax, [xi, xi], [yP - 0.13, 3.1], SIG, lw=0.9)
    line(ax, [xv, xv], [yP, 3.7], SIG, lw=0.9)
    ax.text(xi - 0.1, 9.4, "$i_{abc}$", fontsize=7.5, ha="right", color=SIG)
    ax.text(xv + 0.1, 9.4, "$v_{abc}$", fontsize=7.5, ha="left", color=SIG)

    # ---- plant controller and outer loops
    box(ax, 13.1, 10.1, 3.8, 1.4, "plant controller at the\npoint of connection", fc="#EFE6F3",
        fontsize=fs)
    box(ax, 13.1, 7.0, 2.9, 1.2, "DC-voltage or\nMPPT controller", fc="white", fontsize=fs)
    box(ax, 13.1, 5.2, 2.9, 1.2, "Q or volt-var\ncontroller", fc="white", fontsize=fs)
    arrow(ax, 14.5, 10.1, 14.5, 8.2, color=SIG)
    ax.text(14.6, 9.1, "$P^*$", fontsize=8, color=SIG, va="center")
    line(ax, [16.5, 16.5], [10.1, 5.8], SIG, lw=1.1)
    arrow(ax, 16.5, 5.8, 16.0, 5.8, color=SIG)
    ax.text(16.6, 8.0, "$Q^*$", fontsize=8, color=SIG, va="center")

    # ---- current limiter
    box(ax, 10.3, 4.9, 2.3, 3.6, "", fc="white")
    cx, cy, R = 11.45, 7.15, 0.75
    ax.add_patch(Circle((cx, cy), R, fill=False, ec=COLORS[1], lw=1.3))
    line(ax, [cx - 1.0, cx + 1.0], [cy, cy], "#888888", lw=0.6)
    line(ax, [cx, cx], [cy - 1.0, cy + 1.0], "#888888", lw=0.6)
    ax.text(cx + 1.0, cy + 0.08, "$i_d$", fontsize=6.5, ha="right", va="bottom", color="#666666")
    ax.text(cx + 0.08, cy + 0.95, "$i_q$", fontsize=6.5, ha="left", va="top", color="#666666")
    ax.text(cx, 5.55, "current limiter\n$|i^*|$ ≤ 1.1 pu", fontsize=fs, ha="center",
            va="center")
    arrow(ax, 13.1, 7.6, 12.6, 7.6, color=SIG)
    ax.text(12.85, 7.75, "$i_d^*$", fontsize=7.5, ha="center", va="bottom", color=SIG)
    arrow(ax, 13.1, 5.8, 12.6, 5.8, color=SIG)
    ax.text(12.85, 5.95, "$i_q^*$", fontsize=7.5, ha="center", va="bottom", color=SIG)

    # ---- inner current loop
    box(ax, 6.2, 4.9, 2.7, 3.6, "dq current PI\ncontrollers\n(bandwidth\n≈ 500 Hz)\n"
        "+ decoupling\nterms $\\omega L i$", fc="#E3ECF6", fontsize=fs)
    arrow(ax, 10.3, 6.7, 8.9, 6.7, color=SIG)
    ax.text(9.75, 6.6, "$i_{dq}^*$", fontsize=7, ha="left", va="top", color=SIG)
    box(ax, 3.4, 6.1, 2.0, 1.2, "dq → abc", fc="white", fontsize=fs)
    arrow(ax, 6.2, 6.7, 5.4, 6.7, color=SIG)
    ax.text(5.8, 6.8, "$v_{dq}^*$", fontsize=7, ha="center", va="bottom", color=SIG)
    box(ax, 3.4, 8.2, 2.0, 1.0, "PWM 4 kHz", fc="white", fontsize=fs)
    arrow(ax, 4.4, 7.3, 4.4, 8.2, color=SIG)
    arrow(ax, 4.4, 9.2, 4.4, 10.1, color=SIG)
    ax.text(4.55, 9.65, "gate\nsignals", fontsize=6.5, va="center", color=SIG)

    # current transform (feedback)
    box(ax, 6.2, 2.6, 2.7, 1.0, "$i_{abc}$ → $i_{dq}$", fc="white", fontsize=fs)
    arrow(ax, xi, 3.1, 8.9, 3.1, color=SIG)
    arrow(ax, 7.55, 3.6, 7.55, 4.9, color=SIG)
    ax.text(7.65, 4.25, "$i_{dq}$", fontsize=7.5, va="center", color=SIG)

    # ---- PLL
    ax.add_patch(Rectangle((10.3, 0.75), 6.6, 3.65, fc="#F7EEF5", ec=PLLc, lw=1.0, ls="--"))
    ax.text(16.8, 4.3, "SRF-PLL, bandwidth 20 Hz", fontsize=fs, ha="right", va="top",
            color=PLLc, fontweight="bold")
    box(ax, 10.6, 1.9, 1.6, 1.0, "abc → dq", fc="white", fontsize=fs)
    box(ax, 12.9, 1.9, 1.3, 1.0, "PI", fc="white", fontsize=fs)
    box(ax, 14.9, 1.9, 1.3, 1.0, "$\\int$", fc="white", fontsize=9)
    line(ax, [xv, 11.4], [3.7, 3.7], SIG, lw=0.9)
    arrow(ax, 11.4, 3.7, 11.4, 2.9, color=SIG)
    arrow(ax, 12.2, 2.4, 12.9, 2.4, color=PLLc)
    ax.text(12.55, 2.5, "$v_q$", fontsize=7, ha="center", va="bottom", color=PLLc)
    arrow(ax, 14.2, 2.4, 14.9, 2.4, color=PLLc)
    ax.text(14.55, 2.5, "$\\omega$", fontsize=8, ha="center", va="bottom", color=PLLc)
    ax.text(13.55, 1.75, "drives $v_q$ → 0", fontsize=6.5, ha="center", va="top", color=PLLc)
    line(ax, [16.2, 16.6], [2.4, 2.4], PLLc, lw=1.1)
    line(ax, [16.6, 16.6], [2.4, 1.1], PLLc, lw=1.1)
    line(ax, [16.6, 11.4], [1.1, 1.1], PLLc, lw=1.1)
    arrow(ax, 11.4, 1.1, 11.4, 1.9, color=PLLc)
    ax.text(16.7, 1.75, "$\\theta$", fontsize=8.5, color=PLLc, va="center")
    # theta distribution to the dq transforms
    line(ax, [11.4, 2.9], [1.1, 1.1], PLLc, lw=1.1)
    line(ax, [2.9, 2.9], [1.1, 6.7], PLLc, lw=1.1)
    arrow(ax, 2.9, 6.7, 3.4, 6.7, color=PLLc)
    arrow(ax, 7.55, 1.1, 7.55, 2.6, color=PLLc)
    ax.text(3.0, 4.0, "$\\theta$", fontsize=8.5, color=PLLc)
    ax.text(7.65, 1.75, "$\\theta$", fontsize=8.5, color=PLLc, va="center")
    save(fig, CH, "fig-27-1-grid-following-control")


# ----------------------------------------------------------------------------
# Figure 27.2
# ----------------------------------------------------------------------------
def fig_27_2():
    """P-Q capability of an inverter plant against a grid-code requirement."""
    fig, ax = new_fig(5.6, 5.0)
    th = np.linspace(0, 2 * np.pi, 721)
    S1 = np.sqrt(1 + 0.33 ** 2)
    S09 = 0.9 * S1
    # battery requirement (hatched)
    ax.add_patch(Rectangle((-0.33, -1.0), 0.66, 2.0, fill=False, hatch="////", ec=COLORS[0],
                           lw=0.0, alpha=0.55))
    ax.add_patch(Rectangle((-0.33, -1.0), 0.66, 2.0, fill=False, ec=COLORS[0], lw=1.0, ls=":"))
    # PV requirement (shaded)
    pv = Polygon([[0, 0], [0.33, 0.2], [0.33, 1.0], [-0.33, 1.0], [-0.33, 0.2]], closed=True,
                 fc=COLORS[4], alpha=0.45, ec=COLORS[4], lw=1.2)
    ax.add_patch(pv)
    ax.plot(S1 * np.sin(th), S1 * np.cos(th), color=INK, lw=2,
            label=f"inverter current limit at 1.0 pu voltage ($S$ = {S1:.3f} pu)")
    ax.plot(S09 * np.sin(th), S09 * np.cos(th), "--", color=INK, lw=1.3,
            label=f"same current at 0.9 pu voltage ($S$ = {S09:.3f} pu)")
    ax.axhline(1.0, color=COLORS[1], lw=1.3)
    ax.text(0.58, 1.02, "export limit 1.0 pu", color=COLORS[1], fontsize=8, ha="right",
            va="bottom")
    ax.plot([0.33, -0.33], [1.0, 1.0], "o", color=COLORS[1], ms=6, zorder=5)
    ax.annotate("PF 0.95 lagging\n(injecting vars)", xy=(0.33, 1.0), xytext=(0.36, 0.52),
                fontsize=7.8, arrowprops=dict(arrowstyle="-", lw=0.7))
    ax.annotate("PF 0.95 leading\n(absorbing vars)", xy=(-0.33, 1.0), xytext=(-0.59, 0.52),
                fontsize=7.8, arrowprops=dict(arrowstyle="-", lw=0.7))
    ax.text(0.0, 0.55, "required:\nPV plant", ha="center", va="center", fontsize=8.5,
            fontweight="bold", color="#8a5a00")
    ax.text(0.0, -0.5, "required:\nbattery plant\n(hatched, all\nfour quadrants)", ha="center",
            va="center", fontsize=8, color=COLORS[0], fontweight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))
    ax.text(0.40, 0.2, "±0.33 pu down\nto P = 0.2 pu", fontsize=7.5, va="center")
    ax.axhline(0, color="#999999", lw=0.6)
    ax.axvline(0, color="#999999", lw=0.6)
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("Reactive power $Q$ (pu)   ← absorbing | injecting →")
    ax.set_ylabel("Active power $P$ (pu)   ← charging | exporting →")
    ax.legend(loc="upper center", fontsize=7.5, bbox_to_anchor=(0.5, -0.12), frameon=False)
    save(fig, CH, "fig-27-2-pq-capability")


# ----------------------------------------------------------------------------
# Figure 27.3
# ----------------------------------------------------------------------------
def fig_27_3():
    """LVRT envelope, fault trajectory and reactive/active current response."""
    t = np.linspace(-0.2, 3.0, 3201)
    # envelope
    env_t = [0.0, 0.15, 1.5, 3.0]
    env_v = [0.0, 0.0, 0.85, 0.85]
    # voltage trajectory
    v = np.ones_like(t)
    v[(t >= 0) & (t < 0.1)] = 0.25
    m = t >= 0.1
    v[m] = 0.92 - (0.92 - 0.65) * np.exp(-(t[m] - 0.1) / 0.1)
    # current response: k = 2, deadband 0.1 pu, reactive limit 1.0 pu, total limit 1.1 pu
    k, imax_q, imax = 2.0, 1.0, 1.1
    dv = 1.0 - v
    iq_ref = np.where((dv > 0.1) & (t >= 0), np.minimum(k * (dv - 0.1) + 0.0, imax_q), 0.0)
    iq_ref[(t >= 0) & (t < 0.1)] = min(k * 0.75, imax_q)
    dt = t[1] - t[0]
    tau = 0.010                     # ~30 ms to 95 %
    iq = np.zeros_like(t)
    for i in range(1, len(t)):
        iq[i] = iq[i - 1] + dt / tau * (iq_ref[i] - iq[i - 1])
    id_ = np.ones_like(t)
    f = (t >= 0) & (t < 0.1)
    id_[f] = np.sqrt(np.maximum(imax ** 2 - iq[f] ** 2, 0)) * 0.9
    r = t >= 0.1
    id_[r] = np.minimum(1.0, 0.4 + (0.9 - 0.4) * (t[r] - 0.1) / 0.5)
    id_[(t >= 0) & (t < 0.1)] = np.minimum(id_[(t >= 0) & (t < 0.1)], 0.4)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.12))
    a1.fill_between(env_t, env_v, 1.2, color=COLORS[2], alpha=0.10, lw=0)
    a1.fill_between(env_t, 0, env_v, color=COLORS[1], alpha=0.08, lw=0)
    a1.plot(env_t, env_v, color=INK, lw=2, label="ride-through envelope")
    a1.plot([0.15, 3.0], [0.0, 0.85], "--", color=INK, lw=1.2,
            label="alternative recovery ramp to 3 s")
    a1.plot([1.5, 3.0], [0.90, 0.90], color="#777777", lw=1.0)
    a1.text(2.95, 0.95, "0.90 pu: continuous operation", fontsize=7.5, ha="right",
            va="bottom", color="#555555")
    a1.plot(t, v, ":", color=COLORS[0], lw=2.2, label="fault: dip to 0.25 pu, cleared at 0.1 s")
    a1.text(2.2, 0.45, "disconnection\npermitted", fontsize=8.5, ha="center", color=COLORS[1])
    a1.text(0.75, 1.03, "remain connected", fontsize=8.5, ha="center", color="#1d6b50")
    a1.annotate("0 pu for 150 ms", xy=(0.075, 0.0), xytext=(0.55, 0.05), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    a1.set_ylim(0, 1.2)
    a1.set_ylabel("Voltage at point\nof connection (pu)")
    a1.legend(loc="lower right", fontsize=7.5, bbox_to_anchor=(1.0, 0.04))

    a2.plot(t, iq, color=COLORS[3], lw=2, label="reactive current $i_q$")
    a2.plot(t, id_, "--", color=COLORS[0], lw=1.8, label="active current $i_d$")
    a2.axhline(imax, color="#777777", lw=0.8, ls=":")
    a2.text(2.95, imax + 0.01, "current limit 1.1 pu", fontsize=7.5, ha="right", va="bottom",
            color="#555555")
    a2.annotate("$k\\,\\Delta v$ = 2 × 0.75 = 1.5 pu demanded,\nlimited to 1.0 pu within 30 ms",
                xy=(0.06, 1.0), xytext=(1.0, 0.33), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.7))
    a2.annotate("$i_d$ reduced during the fault,\nback to 0.9 pu by 0.6 s", xy=(0.6, 0.9),
                xytext=(1.0, 0.66),
                fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.7))
    a2.set_ylim(0, 1.2)
    a2.set_xlim(-0.2, 3.0)
    a2.set_xlabel("Time (s)")
    a2.set_ylabel("Current (pu)")
    a2.legend(loc="lower right", fontsize=7.5)
    for a in (a1, a2):
        a.axvline(0, color="#BBBBBB", lw=0.6)
        a.axvline(0.1, color="#BBBBBB", lw=0.6)
    save(fig, CH, "fig-27-3-frt-curve")


# ----------------------------------------------------------------------------
# Figure 27.4
# ----------------------------------------------------------------------------
def simulate_frequency(Ek, ffr=0.0, dP=1.8, f0=50.0, load=30.0, D_pct=2.0, droop_gw_hz=3.9,
                       T_gov=2.0, ramp=0.30, t_end=30.0, dt=0.002):
    """Aggregate swing equation with load damping, rate-limited governor response and
    optional fast frequency response (step at 0.5 s).  Returns t, f."""
    M = 2 * Ek / f0                 # GW.s per Hz
    D = D_pct / 100 * load          # GW per Hz
    n = int(t_end / dt) + 1
    t = np.arange(n) * dt
    f = np.empty(n)
    df, Pg = 0.0, 0.0
    for i in range(n):
        f[i] = f0 + df
        Pf = ffr if t[i] >= 0.5 else 0.0
        tgt = min(-df * droop_gw_hz, dP) - Pf   # FFR is part of the total response
        dPg = np.clip((tgt - Pg) / T_gov, -ramp, ramp)
        Pg += dPg * dt
        df += (Pg + Pf - dP - D * df) / M * dt
    return t, f


def fig_27_4():
    """System frequency after a 1.8 GW loss for three inertia levels, with and without FFR."""
    fig, ax = new_fig(6.4, 4.2)
    cols = {150: COLORS[0], 100: COLORS[2], 60: COLORS[1]}
    for Ek in (150, 100, 60):
        t, f = simulate_frequency(Ek)
        i = f.argmin()
        rocof = 1.8 * 50 / (2 * Ek)
        ax.plot(t, f, color=cols[Ek], lw=2, label=f"$E_k$ = {Ek} GW·s (ROCOF {rocof:.2f} Hz/s)")
        ax.plot([t[i]], [f[i]], "o", color=cols[Ek], ms=4)
        ax.text(t[i] + 0.4, f[i] - 0.02, f"{f[i]:.2f} Hz", fontsize=7.5, color=cols[Ek],
                va="top")
        tt = np.linspace(0, 1.2 / rocof * 0.7, 10)
        ax.plot(tt, 50 - rocof * tt, ":", color=cols[Ek], lw=1.2)
    t, f = simulate_frequency(60, ffr=1.0)
    i = f.argmin()
    ax.plot(t, f, "--", color=COLORS[1], lw=1.8, label="$E_k$ = 60 GW·s + 1 GW FFR at 0.5 s")
    ax.text(t[i] + 0.5, f[i] - 0.03, f"{f[i]:.2f} Hz", fontsize=7.5, color=COLORS[1],
            va="top")
    ax.axhline(49.2, color="#555555", lw=1.0, ls="--")
    ax.axhline(48.8, color="#B00000", lw=1.0, ls="--")
    ax.text(29.8, 49.21, "49.2 Hz: limit for largest infeed loss", fontsize=7.5, ha="right",
            va="bottom", color="#444444")
    ax.text(29.8, 48.79, "48.8 Hz: under-frequency load shedding", fontsize=7.5, ha="right",
            va="top", color="#B00000")
    ax.text(0.4, 48.6, "dotted: tangents at $t$ = 0 (initial ROCOF)", fontsize=7.5)
    ax.set_xlim(0, 30)
    ax.set_ylim(48.5, 50.1)
    ax.set_xlabel("Time after loss of infeed (s)")
    ax.set_ylabel("System frequency (Hz)")
    ax.legend(loc="upper right", fontsize=7.6, bbox_to_anchor=(1.0, 1.0))
    save(fig, CH, "fig-27-4-frequency-after-infeed-loss")


# ----------------------------------------------------------------------------
# Figure 27.5
# ----------------------------------------------------------------------------
def fig_27_5():
    """IEEE 1547-2018 Category B volt-var and volt-watt characteristics."""
    v = np.linspace(0.85, 1.15, 601)
    q = np.interp(v, [0.85, 0.92, 0.98, 1.02, 1.08, 1.15], [0.44, 0.44, 0, 0, -0.44, -0.44])
    p = np.interp(v, [0.85, 1.06, 1.10, 1.15], [1.0, 1.0, 0.2, 0.2])
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True,
                                 gridspec_kw=dict(hspace=0.28))
    a1.axhline(0, color="#999999", lw=0.6)
    a1.axvspan(0.98, 1.02, color="#DDDDDD", alpha=0.5, lw=0)
    a1.plot(v, q, color=COLORS[0], lw=2.2)
    a1.text(1.0, 0.25, "dead-\nband", ha="center", fontsize=7.5, color="#555555")
    for x, y, txt, ha, dy, va in ((0.92, 0.44, "(0.92, +0.44)", "right", -0.05, "top"),
                                  (0.98, 0.0, "(0.98, 0)", "right", 0.05, "bottom"),
                                  (1.02, 0.0, "(1.02, 0)", "left", 0.05, "bottom"),
                                  (1.08, -0.44, "(1.08, −0.44)", "left", 0.05, "bottom")):
        a1.plot([x], [y], "o", color=COLORS[0], ms=4)
        dx = 0.004 if ha == "left" else -0.004
        a1.text(x + dx, y + dy, txt, fontsize=7.5, ha=ha, va=va)
    qop = float(np.interp(1.06, v, q))
    qtxt = f"{qop:.2f}".replace("-", "−")
    a1.plot([1.06], [qop], "s", color=COLORS[1], ms=7, zorder=5)
    a1.annotate(f"LV example, 1.06 pu:\nQ = {qtxt} pu (absorbing)", xy=(1.06, qop),
                xytext=(1.075, -0.06), fontsize=7.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.7))
    a1.text(0.855, 0.08, "injecting vars\n(raises voltage)", fontsize=7.5, color="#444444")
    a1.text(0.855, -0.38, "absorbing vars\n(lowers voltage)", fontsize=7.5, color="#444444")
    a1.set_ylim(-0.5, 0.5)
    a1.set_ylabel("Reactive power $Q$\n(pu of rated $S$)")
    a1.set_title("Volt-var (Category B default)", fontsize=9.5, loc="left")

    a2.plot(v, p, color=COLORS[2], lw=2.2)
    for x, y, txt in ((1.06, 1.0, "(1.06, 1.0)"), (1.10, 0.2, "(1.10, 0.2)")):
        a2.plot([x], [y], "o", color=COLORS[2], ms=4)
        a2.text(x + 0.004, y + 0.04, txt, fontsize=7.5)
    a2.plot([1.06], [1.0], "s", color=COLORS[1], ms=7, zorder=5)
    a2.annotate("LV example at 1.06 pu:\ncurtailment about to start", xy=(1.06, 1.0),
                xytext=(0.93, 0.55), fontsize=7.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.7))
    a2.set_ylim(0, 1.15)
    a2.set_ylabel("Active power limit\n(pu of rated $P$)")
    a2.set_title("Volt-watt (Category B default)", fontsize=9.5, loc="left")
    a2.set_xlim(0.85, 1.15)
    a2.set_xlabel("Voltage at DER terminals (pu)")
    for a in (a1, a2):
        a.grid(True, lw=0.4)
    save(fig, CH, "fig-27-5-volt-var-curve")


# ----------------------------------------------------------------------------
# Figure 27.6
# ----------------------------------------------------------------------------
def fig_27_6():
    """Ramp-rate control of a 100 MW PV plant by a battery during a cloud passage."""
    t = np.linspace(0, 12, 2401)
    pv = np.interp(t, [0, 1, 8, 9, 12], [100, 30, 30, 100, 100])
    plant_dn = np.maximum(100 - 10 * t, pv)
    plant = np.where(t < 8, plant_dn, np.minimum(pv, 30 + 10 * (t - 8)))
    batt = np.where(t < 8, plant - pv, 0.0)
    batt = np.maximum(batt, 0)
    E = np.trapezoid(batt, t) / 60 if hasattr(np, "trapezoid") else np.trapz(batt, t) / 60
    curt = np.where(t >= 8, pv - plant, 0.0)
    Ec = (np.trapezoid(curt, t) if hasattr(np, "trapezoid") else np.trapz(curt, t)) / 60

    fig, ax = new_fig(6.4, 4.0)
    ax.fill_between(t, 0, batt, color=COLORS[0], alpha=0.18, lw=0)
    ax.fill_between(t, plant, pv, where=t >= 8, color=COLORS[4], alpha=0.35, lw=0,
                    hatch="///", edgecolor="#b07a00")
    ax.plot(t, pv, color=COLORS[4], lw=1.3, label="PV array output")
    ax.plot(t, plant, color=INK, lw=2.6, label="plant output at point of connection")
    ax.plot(t, batt, "--", color=COLORS[0], lw=1.8, label="battery power (+ = discharging)")
    ax.axhline(0, color="#999999", lw=0.6)
    ax.text(2.6, 18, f"battery energy\n{E:.1f} MWh", fontsize=8.5, color=COLORS[0], ha="center")
    ax.text(1.12, 61, "60 MW", fontsize=8, color=COLORS[0], va="bottom")
    ax.text(10.5, 82, f"PV curtailed\n{Ec:.1f} MWh\n(to 12 min)", fontsize=8.5, color="#8a5a00",
            ha="center", va="center")
    ax.text(4.6, 61.5, "−10 MW/min", fontsize=8, rotation=-29, ha="center", va="bottom")
    ax.text(10.2, 55, "+10 MW/min", fontsize=8, rotation=29, ha="center", va="bottom")
    ax.set_xlim(0, 12)
    ax.set_ylim(-20, 110)
    ax.set_xticks(range(0, 13))
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Power (MW)")
    ax.legend(loc="lower right", fontsize=7.8, ncol=1, bbox_to_anchor=(1.0, 0.17))
    save(fig, CH, "fig-27-6-ramp-rate-control")


if __name__ == "__main__":
    fig_27_1()
    fig_27_2()
    fig_27_3()
    fig_27_4()
    fig_27_5()
    fig_27_6()
