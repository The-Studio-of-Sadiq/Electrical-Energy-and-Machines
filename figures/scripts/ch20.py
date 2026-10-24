"""Figures for Chapter 20 — Power-System Stability. Run from the repository root: python figures/scripts/ch20.py"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from figstyle import new_fig, box, save, COLORS, INK

CH = "20"

# 600 MVA unit of Sections 20.2-20.3 (machine base)
H, F0 = 4.0, 50.0
WS = 2 * np.pi * F0
PM = 0.85
P1, P2_MID, P3 = 1.15 / 0.70, 1.15 / 1.85, 1.15 / 0.95     # pre-, during-(mid-line), post-fault
D0 = np.arcsin(PM / P1)
DMAX = np.pi - np.arcsin(PM / P3)


def crit_angle(p2):
    c = (PM * (DMAX - D0) + P3 * np.cos(DMAX) - p2 * np.cos(D0)) / (P3 - p2)
    return np.arccos(c)


# ---------------------------------------------------------------- 20.1
def fig_20_1():
    """Classification tree and typical time windows."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.0, 0.40, 1.0, 0.60])
    ax.set_xlim(0, 13.6)
    ax.set_ylim(1.0, 6.2)
    ax.axis("off")
    box(ax, 4.6, 5.25, 4.4, 0.75, "Power-system stability", fc="#DCE8F3", fontsize=10)
    branches = [
        ("Rotor-angle\nstability", [("Small-\ndisturbance", "short term"), ("Transient", "short term")]),
        ("Voltage\nstability", [("Large-\ndisturbance", "short or\nlong term"), ("Small-\ndisturbance", "short or\nlong term")]),
        ("Frequency\nstability", [("Short\nterm", ""), ("Long\nterm", "")]),
        ("Resonance\nstability", [("Torsional", ""), ("Electrical", "")]),
        ("Converter-driven\nstability", [("Fast\ninteraction", ""), ("Slow\ninteraction", "")]),
    ]
    colw = 13.6 / 5
    new = "#FDF0E3"
    for k, (name, kids) in enumerate(branches):
        xc = colw * (k + 0.5)
        fc = new if k >= 3 else "#EEF3F8"
        box(ax, xc - 1.22, 3.65, 2.44, 0.85, name, fc=fc, fontsize=8.5)
        ax.plot([6.8, 6.8], [5.25, 4.85], color=INK, lw=1.0)
        ax.plot([colw * 0.5, colw * 4.5], [4.85, 4.85], color=INK, lw=1.0)
        ax.plot([xc, xc], [4.85, 4.5], color=INK, lw=1.0)
        ax.plot([xc, xc], [3.65, 3.3], color=INK, lw=1.0)
        ax.plot([xc - 0.67, xc + 0.67], [3.3, 3.3], color=INK, lw=1.0)
        for j, (kid, note) in enumerate(kids):
            xk = xc + (j - 0.5) * 1.34
            ax.plot([xk, xk], [3.3, 3.1], color=INK, lw=1.0)
            box(ax, xk - 0.64, 2.2, 1.28, 0.9, kid, fc="white", fontsize=7)
            if note:
                ax.text(xk, 2.1, note, ha="center", va="top", fontsize=7, color="#555555", style="italic")
    ax.text(0.15, 1.15, "Shaded orange: categories added in 2021 for inverter-dominated systems.",
            fontsize=7.5, color="#555555")

    # time axis
    tx = fig.add_axes([0.24, 0.07, 0.72, 0.30])
    bars = [("Converter-driven, fast", 1e-3, 0.1, COLORS[3]),
            ("Converter-driven, slow", 0.1, 10, COLORS[3]),
            ("Resonance (torsional, electrical)", 1e-3, 5, COLORS[4]),
            ("Frequency, long term", 30, 600, COLORS[2]),
            ("Frequency, short term", 0.5, 30, COLORS[2]),
            ("Voltage, long term", 30, 600, COLORS[1]),
            ("Voltage, short term", 0.5, 10, COLORS[1]),
            ("Rotor angle, small-disturbance", 1, 30, COLORS[0]),
            ("Rotor angle, transient", 0.5, 10, COLORS[0])]
    for i, (lab, a, b, c) in enumerate(bars):
        tx.barh(i, np.log10(b) - np.log10(a), left=np.log10(a), height=0.62, color=c, alpha=0.85)
    tx.set_yticks(range(len(bars)))
    tx.set_yticklabels([b[0] for b in bars], fontsize=7.5)
    ticks = [1e-3, 1e-2, 0.1, 1, 10, 60, 600]
    tx.set_xticks(np.log10(ticks))
    tx.set_xticklabels(["1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"], fontsize=8)
    tx.set_xlim(-3, np.log10(600))
    tx.set_ylim(-0.6, len(bars) - 0.4)
    tx.grid(axis="x", color="#e5e5e5")
    tx.set_axisbelow(True)
    tx.set_xlabel("Typical time window (logarithmic)", fontsize=8.5)
    save(fig, CH, "fig-20-1-stability-classification")


# ---------------------------------------------------------------- 20.2
def fig_20_2():
    """Equal-area criterion for the 600 MVA unit."""
    d = np.linspace(0, np.pi, 721)
    dg = np.degrees(d)
    dcr_bus, dcr_mid = crit_angle(0.0), crit_angle(P2_MID)
    fig, ax = new_fig(6.4, 4.0)
    # areas, bus fault
    m1 = (d >= D0) & (d <= dcr_bus)
    ax.fill_between(dg[m1], 0, PM, color=COLORS[1], alpha=0.25, lw=0)
    m2 = (d >= dcr_bus) & (d <= DMAX)
    ax.fill_between(dg[m2], PM, P3 * np.sin(d[m2]), color=COLORS[2], alpha=0.25, lw=0)
    ax.plot(dg, P1 * np.sin(d), color=COLORS[0], label=r"pre-fault, $1.643\sin\delta$")
    ax.plot(dg, P3 * np.sin(d), "--", color=COLORS[2], label=r"post-fault (one line out), $1.211\sin\delta$")
    ax.plot(dg, P2_MID * np.sin(d), ":", color=COLORS[3], lw=2.0, label=r"during mid-line fault, $0.622\sin\delta$")
    ax.plot(dg, 0 * d, color=COLORS[1], lw=2.6, label="during bus fault, 0", solid_capstyle="butt")
    ax.axhline(PM, color=INK, lw=1.1)
    ax.text(2, PM + 0.03, "$P_m$ = 0.85 pu", fontsize=8.5, va="bottom")
    for ang, lab, y, ha in [(D0, r"$\delta_0$ = %.1f°", 1.78, "right"),
                            (dcr_bus, r"$\delta_{cr}$ = %.1f° (bus fault)", 1.78, "left"),
                            (dcr_mid, r"$\delta_{cr}$ = %.1f° (mid-line fault)", 0.04, "left"),
                            (DMAX, r"$\delta_{max}$ = %.1f°", 1.78, "left")]:
        a = np.degrees(ang)
        ax.axvline(a, color="#777777", ls=(0, (4, 3)), lw=0.9)
        ax.text(a + (1.5 if ha == "left" else -1.5), y, lab % a, fontsize=7.5,
                va="top" if y > 1 else "bottom", ha=ha, bbox=dict(fc="white", ec="none", pad=0.5))
    ax.text(43, 0.38, "$A_1$", fontsize=11, ha="center", color=COLORS[1])
    ax.text(95, 0.99, "$A_2$", fontsize=11, ha="center", color=COLORS[2])
    ax.text(160, 1.05, "$A_1 = A_2$ for the\nbus fault cleared\nat $\\delta_{cr}$ = 55.6°", fontsize=7.5,
            ha="center", color="#333333")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1.8)
    ax.set_xticks(range(0, 181, 30))
    ax.set_xlabel("Rotor angle δ (degrees)")
    ax.set_ylabel("Electrical power (pu, 600 MVA base)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=7.5)
    save(fig, CH, "fig-20-2-equal-area-criterion")


# ---------------------------------------------------------------- 20.3
def swing(tc, pd=0.0, T=2.0):
    def rhs(t, x, p):
        return [x[1], WS / (2 * H) * (PM - p * np.sin(x[0]))]
    kw = dict(max_step=1e-3, rtol=1e-9, atol=1e-12)
    s1 = solve_ivp(rhs, (0, tc), [D0, 0], args=(pd,), **kw)
    s2 = solve_ivp(rhs, (tc, T), s1.y[:, -1], args=(P3,), **kw)
    return np.r_[s1.t, s2.t[1:]], np.degrees(np.r_[s1.y[0], s2.y[0][1:]])


def fig_20_3():
    """Swing curves for bus-fault clearing at 0.10, 0.15 and 0.20 s."""
    tcr = np.sqrt(4 * H * (crit_angle(0.0) - D0) / (WS * PM))
    fig, ax = new_fig(6.4, 3.9)
    for tc, c in [(0.10, COLORS[2]), (0.15, COLORS[0]), (0.20, COLORS[1])]:
        t, d = swing(tc)
        if d.max() > 180:
            k = np.argmax(d > 205)
            t, d = t[:k], d[:k]
            t180 = np.interp(180, d[d < 205], t[d < 205])
            ax.annotate(f"cleared {tc:.2f} s: passes 180° at {t180:.2f} s,\nloses synchronism",
                        (t180, 180), xytext=(0.66, 168), fontsize=8, color=c, va="center",
                        arrowprops=dict(arrowstyle="-", color=c, lw=0.8))
        else:
            first = t < 1.0
            imax = np.argmax(np.where(first, d, -1e9))
            ax.plot(t[imax], d[imax], "o", color=c, ms=4)
            ax.text(t[imax] + 0.02, d[imax] + 4, f"{d[imax]:.1f}° at {t[imax]:.2f} s", fontsize=7.5, color=c,
                    ha="left", va="bottom")
            win = (t > 0.6) & (t < 1.6)
            imin = np.argmin(np.where(win, d, 1e9))
            ax.plot(t[imin], d[imin], "o", color=c, ms=4)
            ax.text(t[imin] + 0.04, d[imin], f"{d[imin]:.1f}° at {t[imin]:.2f} s", fontsize=7.5, color=c,
                    ha="left", va="center", bbox=dict(fc="white", ec="none", pad=0.5))
        ax.plot(t, d, color=c, label=f"cleared at {tc:.2f} s ({np.interp(tc, t, d):.1f}° at clearing)")
        ax.axvline(tc, color=c, ls="--", lw=0.8)
    ax.axhline(np.degrees(DMAX), color="#777777", ls="--", lw=0.9)
    ax.text(1.98, np.degrees(DMAX) + 2, r"$\delta_{max}$ = 135.4°", fontsize=8, ha="right", va="bottom")
    ax.text(1.98, 200 - 4, f"critical clearing time {tcr:.3f} s", fontsize=8.5, ha="right", va="top",
            bbox=dict(fc="white", ec="#cccccc"))
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_xlim(0, 2.0)
    ax.set_ylim(-10, 200)
    ax.set_xlabel("Time after fault inception (s)")
    ax.set_ylabel("Rotor angle δ (degrees)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=7.5)
    save(fig, CH, "fig-20-3-swing-curves")


# ---------------------------------------------------------------- 20.4
def pv_curve(X, pf, E=1.0):
    t = np.tan(np.arccos(pf))
    V = np.linspace(0.05, E, 4000)
    a = X ** 2 * (1 + t ** 2)
    b = 2 * V ** 2 * X * t
    c = V ** 4 - E ** 2 * V ** 2
    P = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return P * 100, V          # MW on 100 MVA base


def fig_20_4():
    """PV nose curves for the industrial area."""
    fig, ax = new_fig(6.4, 4.0)
    ax.axhspan(0.95, 1.05, color="#E6F4EF", lw=0)
    ax.text(258, 1.0, "normal voltage range 0.95–1.05 pu", fontsize=7.5, va="center", ha="right", color="#2d7a5f")
    cases = [(0.20, 1.0, COLORS[0], "-"), (0.20, 0.95, COLORS[0], "--"),
             (0.30, 1.0, COLORS[1], "-"), (0.30, 0.95, COLORS[1], "--")]
    for X, pf, c, ls in cases:
        P, V = pv_curve(X, pf)
        ax.plot(P, V, color=c, ls=ls, label=f"X = {X:.2f} pu, " + ("unity pf" if pf == 1 else "0.95 lagging"))
        i = np.argmax(P)
        ax.plot(P[i], V[i], "o", color=c, ms=4)
        ax.text(P[i] + 3, V[i], f"{P[i]:.0f} MW\n{V[i]:.3f} pu", fontsize=7, color=c, va="center")
    ax.axvline(130, color=INK, lw=0.9, ls=":")
    ax.text(129, 0.03, "130 MW load", rotation=90, fontsize=7.5, ha="right", va="bottom")
    for X, pf, c in [(0.20, 1.0, COLORS[0]), (0.20, 0.95, COLORS[0]), (0.30, 1.0, COLORS[1])]:
        P, V = pv_curve(X, pf)
        up = V > V[np.argmax(P)]
        v130 = np.interp(130, P[up][::-1], V[up][::-1])
        ax.plot(130, v130, "s", color=c, ms=4.5, mfc="white", mew=1.4)
        ax.text(127, v130, f"{v130:.3f}", fontsize=7.5, ha="right", va="center", color=c,
                bbox=dict(fc="white", ec="none", pad=0.4))
    # margin arrow on X=0.30 unity
    ax.annotate("", xy=(166.7, 0.70), xytext=(130, 0.70),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.1, mutation_scale=9))
    ax.text(146, 0.685, "margin 22 %", fontsize=7.5, ha="center", color=COLORS[1], va="top")
    ax.set_xlim(0, 260)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Load power P (MW)")
    ax.set_ylabel("Load-bus voltage (pu)")
    ax.legend(loc="lower right", fontsize=7.5, frameon=True, facecolor="white", edgecolor="#cccccc")
    save(fig, CH, "fig-20-4-pv-nose-curves")


# ---------------------------------------------------------------- 20.5
def freq_run(Ek, ffr=0.0, delay=0.2, ramp=0.5, dP=1.8, D=0.7, R=3.0, Tg=6.0):
    trig = [None]

    def ffr_power(t, df):
        if not ffr:
            return 0.0
        if trig[0] is None and df <= -0.2:
            trig[0] = t
        if trig[0] is None:
            return 0.0
        return ffr * min(1.0, max(0.0, (t - trig[0] - delay) / ramp))

    t = np.linspace(0, 30, 30001)
    x = np.zeros(2)
    out = np.zeros_like(t)
    dt = t[1] - t[0]
    for k in range(1, len(t)):             # explicit RK2 with the event-triggered FFR
        def f(tt, xx):
            pf = ffr_power(tt, xx[0])
            return np.array([F0 / (2 * Ek) * (-dP - D * xx[0] + xx[1] + pf), (-R * xx[0] - xx[1]) / Tg])
        k1 = f(t[k - 1], x)
        k2 = f(t[k - 1] + dt, x + dt * k1)
        x = x + dt / 2 * (k1 + k2)
        out[k] = x[0]
    return t, F0 + out


def fig_20_5():
    """Frequency after loss of 1.8 GW in a 35 GW system."""
    fig, ax = new_fig(6.4, 4.3)
    for y, lab in [(49.8, "49.8 Hz\nFFR trigger"), (49.5, "49.5 Hz\nstatutory limit"),
                   (48.8, "48.8 Hz first\nstage of load\nshedding")]:
        ax.axhline(y, color="#888888", ls="--", lw=0.8)
        ax.text(30.4, y, lab, fontsize=7.5, ha="left", va="center", color="#555555", clip_on=False)
    runs = [(200, 0, COLORS[0], "200 GW·s"), (130, 0, COLORS[2], "130 GW·s"),
            (80, 0, COLORS[1], "80 GW·s"), (80, 0.6, COLORS[3], "80 GW·s + 0.6 GW FFR")]
    for Ek, ffr, c, lab in runs:
        t, f = freq_run(Ek, ffr)
        i = np.argmin(f)
        rocof = 1.8 * F0 / (2 * Ek)
        ax.plot(t, f, color=c, ls="--" if ffr else "-",
                label=f"{lab}: RoCoF {rocof + 1e-9:.3f} Hz/s, nadir {f[i]:.2f} Hz at {t[i]:.1f} s")
        ax.plot(t[i], f[i], "o", color=c, ms=4)
        if not ffr:
            tt = np.array([0, 0.75 / rocof])
            ax.plot(tt, 50 - rocof * tt, color=c, lw=1.0, ls=":")
    ax.text(8, 48.93, "dotted lines: tangents at the initial RoCoF", fontsize=7.5, color="#555555",
            ha="left", va="center")
    ax.annotate("settles at 49.51 Hz (no FFR)", (27, 49.51), xytext=(19.5, 49.33), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color="#555555", lw=0.7))
    ax.annotate("settles at 49.68 Hz (with FFR)", (27, 49.677), xytext=(18.5, 49.92), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color="#555555", lw=0.7))
    ax.set_xlim(0, 30)
    ax.set_ylim(48.7, 50.1)
    ax.set_xlabel("Time after loss of generation (s)")
    ax.set_ylabel("System frequency (Hz)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1, fontsize=7.5)
    save(fig, CH, "fig-20-5-frequency-response")


# ---------------------------------------------------------------- 20.6
def fig_20_6():
    """Time scales of the response to a disturbance."""
    fig, ax = new_fig(6.8, 4.4)
    lo = 1e-3
    bars = [("Electromagnetic transients, fault current", 1e-3, 0.02, 0),
            ("Protection and breaker operation", 0.02, 0.15, 0),
            ("Inverter fault ride-through", lo, 0.5, 0),
            ("Rotor-angle first swing", 0.1, 3, 1),
            ("AVR and PSS action", 0.1, 10, 1),
            ("Inertial response", lo, 10, 1),
            ("Governor primary response", 2, 30, 1),
            ("Tap changers, over-excitation limiters", 30, 600, 2),
            ("Secondary frequency control (AGC)", 30, 900, 2),
            ("Operator actions, thermal limits", 600, 3600, 2)]
    cols = [COLORS[3], COLORS[0], COLORS[2]]
    bands = [(1e-3, 0.1, "EMT simulation domain"), (0.1, 60, "RMS (phasor) simulation domain"),
             (60, 3600, "quasi-steady-state domain")]
    bfc = ["#F7E9F1", "#E8F1F8", "#E6F4EF"]
    n = len(bars)
    for (a, b, lab), fc in zip(bands, bfc):
        ax.axvspan(np.log10(a), np.log10(b), color=fc, lw=0)
        ax.text((np.log10(a) + np.log10(b)) / 2, n - 0.15, lab, ha="center", va="bottom", fontsize=7.5,
                color="#444444")
    for i, (lab, a, b, g) in enumerate(bars):
        y = n - 1 - i
        ax.barh(y, np.log10(b) - np.log10(a), left=np.log10(a), height=0.6, color=cols[g])
        xa = np.log10(a)
        if xa > np.log10(5):
            ax.text(xa - 0.08, y, lab, ha="right", va="center", fontsize=7.5)
        else:
            ax.text(np.log10(b) + 0.08, y, lab, ha="left", va="center", fontsize=7.5)
    ticks = [1e-3, 1e-2, 0.1, 1, 10, 60, 600, 3600]
    ax.set_xticks(np.log10(ticks))
    ax.set_xticklabels(["1 ms", "10 ms", "100 ms", "1 s", "10 s", "1 min", "10 min", "1 h"])
    ax.set_xlim(-3, np.log10(3600))
    ax.set_ylim(-0.6, n + 0.45)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Time after the disturbance (logarithmic)")
    ax.text(-2.97, -0.5, "bars starting at 1 ms begin at fault inception", fontsize=7, color="#666666",
            va="bottom")
    save(fig, CH, "fig-20-6-disturbance-time-scales")


if __name__ == "__main__":
    fig_20_1()
    fig_20_2()
    fig_20_3()
    fig_20_4()
    fig_20_5()
    fig_20_6()
