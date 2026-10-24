"""Figures for Chapter 28 — Energy Efficiency and Management.

Run from the repository root:  python figures/scripts/ch28.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FixedLocator, NullFormatter

from figstyle import new_fig, save, COLORS, INK, GRID

GREY = "#8A8A8A"


# ---------------------------------------------------------------- 28.1
def fig_load_profile_duration():
    """Weekday load profile (15-min steps) and annual load duration curve."""
    t = np.arange(0, 24, 0.25)              # start of each 15-min interval, h
    p = np.empty_like(t)
    rng = np.random.default_rng(28)
    for i, h in enumerate(t):
        if h < 6:
            base = 1150
        elif h < 7:
            base = 1150 + (h - 6 + 0.25) * 450          # ramp to ~1600 kW
        elif h < 22:
            # production plateau 1600-1900 kW with a lunch dip
            base = 1750 + 120 * np.sin((h - 7) / 15 * np.pi) - (80 if 12 <= h < 13 else 0)
        elif h < 23:
            base = 1600 - (h - 22 + 0.25) * 450
        else:
            base = 1150
        p[i] = base + rng.normal(0, 25)
    p[(t >= 15) & (t < 15.5)] = 2400                      # coincident peak
    p = np.clip(p, None, 2400)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(wspace=0.32))
    tt = np.append(t, 24)
    a1.stairs(p, tt, color=COLORS[0], lw=1.4, baseline=None)
    a1.axhline(2100, color=COLORS[1], ls="--", lw=1.2)
    a1.text(0.3, 2140, "demand limit target 2100 kW", color=COLORS[1], fontsize=8, va="bottom")
    a1.axhline(1500, color=INK, ls=":", lw=1.2)
    a1.text(0.3, 1430, "monthly average 1500 kW", color=INK, fontsize=8, va="top")
    a1.annotate("compressors plus\ndefrost coincide", xy=(14.9, 2400), xytext=(13.6, 2470),
                fontsize=8, va="center", ha="right", arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    a1.text(1.0, 950, "refrigeration\nbase load", fontsize=8, color=GREY, va="top")
    a1.set_xlim(0, 24)
    a1.set_ylim(0, 2600)
    a1.set_xticks(range(0, 25, 4))
    a1.set_xlabel("Time of day (h)")
    a1.set_ylabel("Demand (kW)")
    a1.set_title("Weekday profile", fontsize=10)

    # Load duration curve: monotone interpolation in (hours, kW)
    hk = np.array([0, 40, 300, 2000, 4400, 7000, 8760])
    pk = np.array([2400, 2100, 1950, 1800, 1500, 1180, 1100])
    from scipy.interpolate import PchipInterpolator
    hh = np.linspace(0, 8760, 2000)
    ldc = PchipInterpolator(hk, pk)(hh)
    a2.plot(hh, ldc, color=COLORS[0])
    hz = np.linspace(0, 40, 200)
    lz = PchipInterpolator(hk, pk)(hz)
    a2.fill_between(hz, 2100, lz, color=COLORS[1], alpha=0.6, lw=0)
    a2.axhline(2100, color=COLORS[1], ls="--", lw=1.2)
    a2.annotate("above target about 40 h/yr;\nworst event: about 450 kWh\nto be shaved",
                xy=(25, 2250), xytext=(1100, 2580), fontsize=7.5, va="top",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    for h, v in [(2000, 1800), (4400, 1500)]:
        a2.plot(h, v, "o", color=COLORS[0], ms=3.5)
        a2.text(h + 150, v + 40, f"{v} kW at {h} h", fontsize=7.5, va="bottom")
    a2.text(8600, 1150, "base\n1100 kW", fontsize=7.5, ha="right", va="bottom")
    a2.set_xlim(0, 8760)
    a2.set_ylim(0, 2600)
    a2.set_xticks([0, 2000, 4000, 6000, 8760])
    a2.set_xlabel("Hours per year demand is exceeded")
    a2.set_ylabel("Demand (kW)")
    a2.set_title("Annual load duration curve", fontsize=10)
    save(fig, "28", "fig-28-1-load-profile-duration")


# ---------------------------------------------------------------- 28.2
def fig_battery_peak_shaving():
    """Worst afternoon: site demand, grid import with battery, battery power."""
    t = np.linspace(12, 20, 961)              # 30 s resolution, hours
    # site demand: 1800 kW base with a trapezoidal event: ramp 14:15-14:45,
    # plateau 2400 kW 14:45-16:00, ramp down to 16:30 (450 kWh above 2100 kW)
    base = np.interp(t, [12, 14.25, 16.5, 17.0, 20], [1800, 1800, 1800, 1800, 1650])
    trap = np.interp(t, [14.25, 14.75, 16.0, 16.5], [0, 600, 600, 0], left=0, right=0)
    d = base + trap
    target = 2100
    grid = np.minimum(d, target)
    batt = d - grid
    e_kwh = np.trapezoid(batt, t)

    fig, ax = new_fig(6.4, 3.9)
    ax.axhline(0, color=INK, lw=0.6)
    ax.fill_between(t, grid, d, where=d > target, color=COLORS[1], alpha=0.35, lw=0)
    ax.plot(t, d, color=GREY, lw=4.5, alpha=0.55, label="site demand without battery")
    ax.plot(t, grid, color=COLORS[0], lw=1.8, label="grid import with battery")
    ax.plot(t, batt, color=COLORS[2], lw=1.6, label="battery power (+ discharge)")
    ax.axhline(target, color=COLORS[1], ls="--", lw=1.1)
    ax.text(19.9, target + 40, "target 2100 kW", color=COLORS[1], fontsize=8, ha="right", va="bottom")
    ax.text(15.38, 2250, f"{e_kwh:.0f} kWh\ndelivered", fontsize=8.5, ha="center", va="center")
    ax.annotate("300 kW", xy=(15.4, 300), xytext=(16.6, 520), fontsize=8, color=COLORS[2],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=0.9))
    # recharge off-peak, off the right edge
    ax.annotate("recharge about −100 kW\nfrom 22:00 (off-peak)", xy=(20, -100), xytext=(16.9, -210),
                fontsize=8, color=COLORS[2], va="center",
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=0.9))
    ax.set_xlim(12, 20)
    ax.set_ylim(-400, 2600)
    ax.set_xticks(range(12, 21))
    ax.set_xticklabels([f"{h}:00" for h in range(12, 21)])
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Power (kW)")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.55), fontsize=8)
    save(fig, "28", "fig-28-2-battery-peak-shaving")


# ---------------------------------------------------------------- 28.3
def fig_throttle_vs_vsd():
    """Input power of the pump set against flow: throttle, VSD (friction), VSD (40 % static)."""
    eta_m, eta_d, Pd = 0.95, 0.97, 80.0
    q = np.linspace(0.4, 1.0, 200)
    # throttle: pump-curve shaft power fractions 1.00, 0.93, 0.85 at 100, 80, 60 % (text);
    # 40 % point 0.76 (64 kW) from the figure plan; quadratic through them
    qp = np.array([1.0, 0.8, 0.6, 0.4])
    pthr_pts = np.array([84.2, 78.3, 71.6, 64.0])
    c = np.polyfit(qp, pthr_pts, 2)
    pthr = np.polyval(c, q)
    p100 = Pd / (eta_m * eta_d)                  # 86.8 kW
    pvsd = p100 * q ** 3
    hs = 0.4                                     # static head fraction
    pst = p100 * q * (hs + (1 - hs) * q ** 2)    # P ∝ Q·H with H = Hs + k Q², constant pump efficiency

    fig, ax = new_fig(6.4, 3.9)
    ax.plot(q * 100, pthr, color=COLORS[1], label="throttle valve")
    ax.plot(qp * 100, pthr_pts, "o", color=COLORS[1], ms=4)
    ax.plot(q * 100, pst, ":", color=COLORS[2], lw=2.0, label="VSD, 40 % static head")
    ax.plot(q * 100, pvsd, "--", color=COLORS[0], label="VSD, friction-only system")
    ax.plot(qp * 100, p100 * qp ** 3, "o", color=COLORS[0], ms=4)
    for qq, txt in [(0.8, "33.9 kW"), (0.6, "52.8 kW")]:
        top = np.polyval(c, qq)
        bot = p100 * qq ** 3
        ax.annotate("", xy=(qq * 100, bot + 0.8), xytext=(qq * 100, top - 0.8),
                    arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, mutation_scale=9))
        ax.text(qq * 100 - 1.0, (top + bot) / 2 + 4, f"saving\n{txt}", fontsize=8, va="center",
                ha="right")
    for qq in [0.8, 0.6, 0.4]:
        ax.text(qq * 100 + 1.0, p100 * qq ** 3 - 1.5, f"{p100*qq**3:.1f} kW", fontsize=7.5,
                ha="left", va="top", color=COLORS[0])
    ax.annotate("at 100 % the drive adds\n3 % loss: 86.8 vs 84.2 kW", xy=(100, 86.8),
                xytext=(76, 96), fontsize=7.5, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    ax.set_xlim(38, 102)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Flow (% of design)")
    ax.set_ylabel("Electrical input power (kW)")
    ax.legend(loc="lower right", fontsize=8)
    save(fig, "28", "fig-28-3-throttle-vs-vsd")


# ---------------------------------------------------------------- 28.4
def fig_ie_classes():
    """IE1-IE4 minimum efficiency against rated output (Table 28.6)."""
    P = np.array([0.75, 1.1, 7.5, 11, 75, 200, 1000])
    data = {
        "IE1": [72.1, 75.0, 86.0, 87.6, 93.1, 94.0],
        "IE2": [79.6, 81.4, 88.7, 89.8, 94.7, 95.1],
        "IE3": [82.5, 84.1, 90.4, 91.4, 95.6, 96.0],
        "IE4": [85.7, 87.2, 91.9, 92.6, 96.4, 96.7],
    }
    from scipy.interpolate import PchipInterpolator
    x = np.logspace(np.log10(0.75), 3, 400)
    fig, ax = new_fig(6.4, 3.9)
    curves = {}
    cols = {"IE1": GREY, "IE2": COLORS[1], "IE3": COLORS[2], "IE4": COLORS[0]}
    for k, v in data.items():
        y = np.array(v + [v[-1]])
        f = PchipInterpolator(np.log10(P), y)
        curves[k] = f(np.log10(x))
        ax.plot(x, curves[k], color=cols[k], lw=1.7)
        ax.plot(P[:-1], v, "o", color=cols[k], ms=3.2)
        ax.text(1050, {"IE4": 97.5, "IE3": 96.2, "IE2": 94.9, "IE1": 93.6}[k], k, color=cols[k], fontsize=9, va="center", fontweight="bold")
    ax.fill_between(x, curves["IE2"], curves["IE4"], color=COLORS[0], alpha=0.12, lw=0)
    ax.annotate("IE2 → IE4:\nabout one third less loss", xy=(3, 87.0), xytext=(5.0, 78.0),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    ax.plot([75, 75], [94.7, 96.4], "o", color=INK, ms=5, mfc="white", mew=1.4, zorder=5)
    ax.annotate("75 kW fan example\n94.7 % (IE2), 96.4 % (IE4)", xy=(75, 94.7), xytext=(110, 85.5),
                fontsize=8, arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    ax.set_xscale("log")
    ax.set_xlim(0.75, 1000)
    ax.set_ylim(70, 100)
    ticks = [0.75, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.set_xticklabels([str(t) for t in ticks])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="major", color=GRID, lw=0.6)
    ax.set_xlabel("Rated output (kW)")
    ax.set_ylabel("Minimum nominal efficiency (%)")
    save(fig, "28", "fig-28-4-ie-efficiency-classes")


# ---------------------------------------------------------------- 28.5
def fig_cusum():
    """CUSUM of actual minus expected energy (Table 28.7)."""
    prod = np.array([950, 1020, 980, 1100, 1000, 1050])
    actual = np.array([520, 510, 480, 520, 470, 480])
    expected = 180 + 0.35 * prod
    diff = actual - expected
    cus = np.concatenate([[0], np.cumsum(diff)])
    m = np.arange(0, 7)
    slope, icpt = np.polyfit(m[3:], cus[3:], 1)
    pct = -slope / expected[2:].mean() * 100

    fig, ax = new_fig(6.4, 3.9)
    ax.axhline(0, color=INK, lw=0.6)
    ax.plot(m, cus, "-o", color=COLORS[0], ms=5, label="CUSUM (actual − expected)")
    for mi, ci in zip(m, cus):
        ax.text(mi + 0.08, ci + 6, f"{ci:+.1f}" if mi else "0", fontsize=7.5, va="bottom")
    xf = np.linspace(2.6, 6.2, 50)
    ax.plot(xf, slope * xf + icpt, ":", color=COLORS[1], lw=2.0,
            label=f"fit months 3–6: {slope:.0f} MWh/month")
    ax.axvline(1, color=GREY, ls="--", lw=1.1)
    ax.text(1.07, -40, "retrofit\ncommissioned", fontsize=8, color=GREY, va="top")
    ax.annotate(f"slope ≈ {slope:.0f} MWh/month:\nsaving about {pct:.0f}–12 %\nof expected energy",
                xy=(3.4, slope * 3.4 + icpt), xytext=(1.25, -125), fontsize=8, ha="left",
                va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    ax.set_xlim(-0.2, 6.6)
    ax.set_ylim(-250, 25)
    ax.set_xlabel("Month")
    ax.set_ylabel("CUSUM (MWh)")
    ax.legend(loc="upper right", fontsize=8)

    ins = ax.inset_axes([0.08, 0.07, 0.30, 0.20])
    ins.bar(m[1:], diff, color=[COLORS[1] if v > 0 else COLORS[0] for v in diff], width=0.6)
    ins.axhline(0, color=INK, lw=0.6)
    ins.set_xticks(m[1:])
    ins.tick_params(labelsize=7)
    ins.set_ylim(-75, 15)
    ins.set_title("monthly difference (MWh)", fontsize=7.5)
    save(fig, "28", "fig-28-5-cusum")


# ---------------------------------------------------------------- 28.6
def fig_transformer_efficiency():
    """Efficiency against per-unit load for the 1990s and Tier 2 1000 kVA units."""
    S = 1000.0
    x = np.linspace(0.02, 1.2, 500)
    units = [("1990s CRGO: $P_0$ = 1.70 kW, $P_k$ = 13.0 kW", 1.70, 13.0, COLORS[1]),
             ("Ecodesign Tier 2: $P_0$ = 0.693 kW, $P_k$ = 7.6 kW", 0.693, 7.6, COLORS[0])]
    fig, ax = new_fig(6.4, 3.9)
    ax.axvspan(0.3, 0.6, color=GREY, alpha=0.15, lw=0)
    ax.text(0.45, 97.58, "typical operating\nband", fontsize=8, ha="center", va="bottom", color=INK)
    for lab, P0, Pk, col in units:
        eta = 100 * x * S / (x * S + P0 + x ** 2 * Pk)
        ax.plot(x, eta, color=col, label=lab)
        xo = np.sqrt(P0 / Pk)
        eo = 100 * xo * S / (xo * S + 2 * P0)
        ax.plot(xo, eo, "o", color=col, ms=5)
        ax.annotate(f"$x_{{opt}}$ = {xo:.2f}\n{eo:.2f} %", xy=(xo, eo), xytext=(xo + 0.02, eo - 0.12),
                    fontsize=8, color=col, va="top")
    ax.set_xlim(0, 1.2)
    ax.set_ylim(97.5, 99.8)
    ax.set_xlabel("Load (per unit of 1000 kVA), unity power factor")
    ax.set_ylabel("Efficiency (%)")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "28", "fig-28-6-transformer-efficiency")


if __name__ == "__main__":
    fig_load_profile_duration()
    fig_battery_peak_shaving()
    fig_throttle_vs_vsd()
    fig_ie_classes()
    fig_cusum()
    fig_transformer_efficiency()
