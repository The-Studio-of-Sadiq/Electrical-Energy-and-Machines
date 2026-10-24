"""Figures for Chapter 25 — Power Quality.

Run from the repository root:  python figures/scripts/ch25.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon
from scipy.interpolate import PchipInterpolator

from figstyle import new_fig, schematic, box, save, COLORS, INK

CH = "25"


# ----------------------------------------------------------------------------
# Single-line drawing helpers (matplotlib only)
# ----------------------------------------------------------------------------
def line(ax, xs, ys, color=INK, lw=1.3, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def transformer_v(ax, x, ytop, r=0.32, color=INK):
    """Two-winding transformer drawn vertically; returns y of bottom terminal."""
    ax.add_patch(Circle((x, ytop - r), r, fill=False, ec=color, lw=1.3))
    ax.add_patch(Circle((x, ytop - 1.6 * r), r, fill=False, ec=color, lw=1.3))
    return ytop - 2.6 * r


def breaker_v(ax, x, yc, s=0.22, color=INK, fc="white"):
    ax.add_patch(Rectangle((x - s / 2, yc - s / 2), s, s, fc=fc, ec=color, lw=1.2, zorder=3))


def switch_v(ax, x, ytop, h=0.45, color=INK):
    """Contactor/switch contact drawn vertically from ytop downward."""
    line(ax, [x, x], [ytop, ytop - 0.1], color)
    line(ax, [x, x + 0.18], [ytop - h + 0.1, ytop - 0.12], color)
    line(ax, [x, x], [ytop - h + 0.1, ytop - h], color)
    ax.plot([x], [ytop - h + 0.1], "o", ms=2.2, color=color)
    return ytop - h


def inductor_v(ax, x, ytop, n=3, r=0.09, color=INK):
    y = ytop
    for _ in range(n):
        ax.add_patch(Arc((x, y - r), 2 * r, 2 * r, theta1=-90, theta2=90, ec=color, lw=1.2))
        y -= 2 * r
    return y


def capacitor_v(ax, x, ytop, w=0.32, gap=0.09, lead=0.12, color=INK):
    line(ax, [x, x], [ytop, ytop - lead], color)
    line(ax, [x - w / 2, x + w / 2], [ytop - lead, ytop - lead], color, lw=1.6)
    line(ax, [x - w / 2, x + w / 2], [ytop - lead - gap, ytop - lead - gap], color, lw=1.6)
    line(ax, [x, x], [ytop - lead - gap, ytop - 2 * lead - gap], color)
    return ytop - 2 * lead - gap


def ground(ax, x, y, color=INK):
    for i, w in enumerate((0.26, 0.17, 0.08)):
        line(ax, [x - w / 2, x + w / 2], [y - 0.06 * i, y - 0.06 * i], color, lw=1.1)


def arrester_v(ax, x, ytop, color=INK):
    """Surge arrester: box with downward arrow, then earth."""
    line(ax, [x, x], [ytop, ytop - 0.15], color)
    ax.add_patch(Rectangle((x - 0.1, ytop - 0.55), 0.2, 0.4, fc="white", ec=color, lw=1.1))
    ax.annotate("", xy=(x, ytop - 0.5), xytext=(x, ytop - 0.2),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.8, mutation_scale=6))
    line(ax, [x, x], [ytop - 0.55, ytop - 0.7], color)
    ground(ax, x, ytop - 0.7, color)


def motor(ax, x, ytop, r=0.3, text="M"):
    ax.add_patch(Circle((x, ytop - r), r, fc="white", ec=INK, lw=1.2))
    ax.text(x, ytop - r, text, ha="center", va="center", fontsize=9)


# ----------------------------------------------------------------------------
# Figure 25.1
# ----------------------------------------------------------------------------
def fig_25_1():
    """Bus harmonic impedance with plain and detuned bank, drive spectrum overlaid."""
    Xs = 11.0 ** 2 / 250.0          # 0.484 ohm
    Xc = 11.0 ** 2 / 3.0            # 40.33 ohm
    XL = 0.07 * Xc                  # 7 % detuning reactor
    h = np.linspace(1, 25, 4000)
    Zs = h * Xs
    Zplain = np.abs(h * Xs * (Xc / h) / (h * Xs - Xc / h))
    xb = h * XL - Xc / h                         # detuned branch reactance
    Zdet = np.abs(h * Xs * xb / (h * Xs + xb))
    hr = np.sqrt(Xc / Xs)
    hp = np.sqrt(Xc / (Xs + XL))
    ht = 1 / np.sqrt(0.07)

    fig, ax = new_fig(6.6, 4.0)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    hb = np.array([5, 7, 11, 13, 17, 19])
    Ib = np.array([49.7, 19.9, 11.6, 8.3, 5.0, 4.1])
    ax2.bar(hb, Ib, width=0.55, color=COLORS[4], alpha=0.45, zorder=0, label="Drive current $I_h$")
    for x, v in zip(hb, Ib):
        ax2.text(x, v + 0.8, f"{v:g}", ha="center", va="bottom", fontsize=7.5, color="#8a5a00")
    ax2.set_ylim(0, 60)
    ax2.set_ylabel("Harmonic current $I_h$ (A)")
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)

    ax.plot(h, Zs, "--", color=INK, lw=1.4, label=r"Source alone, $hX_s$")
    Zp = np.where(Zplain > 45, np.nan, Zplain)
    ax.plot(h, Zp, "-", color=COLORS[0], lw=1.9, label="With plain 3 Mvar bank")
    ax.plot(h, np.where(Zdet > 45, np.nan, Zdet), ":", color=COLORS[1], lw=2.0,
            label="With bank detuned, $p$ = 7 %")
    ax.axvline(hr, color=COLORS[0], lw=0.6, alpha=0.6)
    ax.text(10.2, 37.5, f"parallel resonance\n$h_r$ = {hr:.2f} (456 Hz)", fontsize=8,
            color=COLORS[0], va="top")
    ax.text(1.3, 36.5, f"peak\n{hp:.2f}", fontsize=8, color=COLORS[1], va="center")
    ax.annotate(f"dip\n{ht:.2f}", xy=(ht, 0.25), xytext=(1.3, 6.0), fontsize=8,
                color=COLORS[1], va="center",
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.7, shrinkB=1))
    ax.text(12.6, 27.5, "Detuned bank (dotted): parallel peak\n"
            "below the 5th, series dip at $h_t$,\n"
            "inductive above $h$ ≈ 4, so $|Z_h| < hX_s$", fontsize=8, color=COLORS[1], va="top")
    for hh, amp in ((5, 1.43), (7, 2.43), (11, 2.21)):
        z = hh * Xs * (Xc / hh) / abs(hh * Xs - Xc / hh)
        ax.plot([hh], [z], "o", color=COLORS[0], ms=4.5, zorder=5)
    ax.text(12.6, 20.8, "Amplification by the plain bank:\n"
            "×1.43 at $h$ = 5, ×2.43 at 7, ×2.21 at 11",
            fontsize=8, color=COLORS[0], va="top", fontweight="bold")
    ax.set_xlim(1, 25)
    ax.set_ylim(0, 40)
    ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
    ax.set_xlabel("Harmonic order $h$")
    ax.set_ylabel(r"Bus impedance $|Z_h|$ ($\Omega$)")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=8)
    save(fig, CH, "fig-25-1-bus-harmonic-impedance")


# ----------------------------------------------------------------------------
# Figure 25.2
# ----------------------------------------------------------------------------
def fig_25_2():
    """Pst = 1 curve for rectangular voltage changes, 230 V lamp."""
    rp = np.array([1, 7, 39, 110, 1056, 1620, 4000])
    dp = np.array([2.72, 1.46, 0.91, 0.73, 0.30, 0.40, 0.90])
    f = PchipInterpolator(np.log10(rp), np.log10(dp))
    r_mid = np.logspace(0, np.log10(4000), 400)
    d_mid = 10 ** f(np.log10(r_mid))
    # below 1 change/min: flicker-time law Pst^3.2 proportional to n d^3.2  ->  d ~ r^(-1/3.2)
    r_lo = np.logspace(-2, 0, 60)
    d_lo = 2.72 * r_lo ** (-1 / 3.2)
    # above 4000/min: continue the last log-log slope
    s = np.log(0.9 / 0.4) / np.log(4000 / 1620)
    r_hi = np.logspace(np.log10(4000), 4, 40)
    d_hi = 0.9 * (r_hi / 4000) ** s
    r = np.concatenate([r_lo, r_mid[1:], r_hi[1:]])
    d = np.concatenate([d_lo, d_mid[1:], d_hi[1:]])

    fig, ax = new_fig(6.4, 3.9)
    ax.fill_between(r, d, 10, color=COLORS[1], alpha=0.10, lw=0)
    ax.plot(r, d, color=INK, lw=2)
    ax.plot(rp, dp, "o", color=INK, ms=3)
    ax.text(12, 4.2, "$P_{st}$ > 1 (irritating)", fontsize=9.5, color=COLORS[1])
    ax.text(0.04, 0.3, "$P_{st}$ < 1 (acceptable)", fontsize=9.5, color=INK)
    ax.annotate("minimum ≈ 0.30 % at 1056/min\n(8.8 Hz modulation)", xy=(1056, 0.30),
                xytext=(14, 0.17), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.7))
    # loads
    r_m = 4 / 60
    ax.plot([r_m], [3.0], "s", color=COLORS[0], ms=7)
    ax.text(0.014, 2.05, "large motor start\n4 per hour, 3 %", fontsize=8, va="top",
            color=COLORS[0])
    ax.plot([60], [1.0], "^", color=COLORS[3], ms=8)
    ax.text(60 * 1.35, 1.12, "spot welder\n60/min, 1 %", fontsize=8, color=COLORS[3])
    ax.add_patch(Rectangle((300, 0.5), 2700, 1.5, fc=COLORS[2], alpha=0.25, ec=COLORS[2], lw=1.2))
    ax.text(950, 2.2, "arc furnace\n300–3000/min,\n0.5–2 %", fontsize=8, color="#006b4f",
            ha="center", va="bottom")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 1e4)
    ax.set_ylim(0.1, 10)
    ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000, 10000])
    ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000", "10 000"])
    ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])
    ax.set_xlabel("Rectangular voltage changes per minute")
    ax.set_ylabel(r"Relative voltage change $\Delta V/V$ (%)")
    ax.grid(True, which="major", lw=0.5)
    save(fig, CH, "fig-25-2-pst-unity-curve")


# ----------------------------------------------------------------------------
# Figure 25.3
# ----------------------------------------------------------------------------
def fig_25_3():
    """IEEE 1159 magnitude-duration map with ITIC and SEMI F47."""
    fig, ax = new_fig(6.8, 4.6)
    regions = [
        (1e-6, 1e-2, 1.2, 2.0, "#CC79A7", "Transients", (1e-5, 1.62)),
        (1e-2, 1e3, 0.0, 0.1, "#999999", "Interruption", (2.0, 0.045)),
        (1e-2, 60, 0.1, 0.9, "#0072B2", "Sag (dip)", (0.18, 0.2)),
        (1e-2, 60, 1.1, 1.8, "#D55E00", "Swell", (0.4, 1.66)),
        (60, 1e3, 0.8, 0.9, "#56B4E9", "Under-\nvoltage", (250, 0.6)),
        (60, 1e3, 1.1, 1.2, "#E69F00", "Over-\nvoltage", (250, 1.37)),
    ]
    for x0, x1, y0, y1, c, name, (tx, ty) in regions:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, alpha=0.16, ec="none"))
        ax.text(tx, ty, name, fontsize=8.5, color=c if c != "#999999" else "#555555",
                ha="center", va="center", fontweight="bold")
    ax.axhspan(0.9, 1.1, xmin=0, xmax=1, color="#009E73", alpha=0.08)
    ax.text(3e-5, 1.0, "normal operating band 0.9–1.1 pu", fontsize=8, va="center", color="#006b4f")

    # ITIC
    lo_t = [1e-6, 0.02, 0.02, 0.5, 0.5, 10, 10, 1e3]
    lo_v = [0.0, 0.0, 0.70, 0.70, 0.80, 0.80, 0.90, 0.90]
    hi_t = [1e-3, 3e-3, 3e-3, 0.5, 0.5, 1e3]
    hi_v = [2.0, 1.4, 1.2, 1.2, 1.1, 1.1]
    ax.plot(lo_t, lo_v, color=INK, lw=2, label="ITIC tolerance curve")
    ax.plot(hi_t, hi_v, color=INK, lw=2)
    # SEMI F47
    ax.plot([0.02, 0.2, 0.2, 0.5, 0.5, 1.0, 1.0], [0.5, 0.5, 0.7, 0.7, 0.8, 0.8, 0.9], "--",
            color=COLORS[2], lw=2, label="SEMI F47 ride-through")
    ax.text(0.03, 0.44, "SEMI F47", color="#006b4f", fontsize=8)
    ax.text(1.5e-3, 0.76, "ITIC", fontsize=8.5, fontweight="bold")
    ax.text(5e-4, 2.0, "ITIC", fontsize=8.5, fontweight="bold", va="top", ha="right")
    # fab dip
    ax.plot([0.11], [0.62], "*", color="#B00000", ms=13, zorder=5)
    ax.annotate("fab dip\n0.62 pu, 110 ms", xy=(0.11, 0.62), xytext=(1.8, 0.33), fontsize=8,
                color="#B00000", arrowprops=dict(arrowstyle="-", color="#B00000", lw=0.8))
    ax.set_xscale("log")
    ax.set_xlim(1e-6, 1e3)
    ax.set_ylim(0, 2.0)
    ax.set_xticks([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
    ax.set_xticklabels(["1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "0.1 s", "1 s", "10 s",
                        "100 s", "1000 s"], fontsize=8.5)
    ax.axvline(60, color="#888888", lw=0.6, ls=":")
    ax.axvline(1e-2, color="#888888", lw=0.6, ls=":")
    ax.set_xlabel("Duration")
    ax.set_ylabel("RMS (or peak, for transients) voltage (pu)")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, CH, "fig-25-3-disturbance-map")


# ----------------------------------------------------------------------------
# Figure 25.4
# ----------------------------------------------------------------------------
def fig_25_4():
    """400 V automatic detuned PFC bank (single-line)."""
    fig, ax = schematic(6.8, 4.4, xlim=(0, 13.6), ylim=(0.6, 9.4))
    PINK = COLORS[3]
    # supply and transformer
    xT = 1.6
    line(ax, [xT, xT], [9.3, 8.95])
    ax.text(xT + 0.25, 9.2, "11 kV supply", fontsize=8.5, va="center")
    yb = transformer_v(ax, xT, 8.95)
    ax.text(xT + 0.5, 8.35, "1600 kVA\n11/0.4 kV Dyn11", fontsize=8, va="center")
    line(ax, [xT, xT], [yb, 7.07])
    breaker_v(ax, xT, 7.55)
    # CT on incomer
    ax.add_patch(Circle((xT, 7.25), 0.11, fill=False, ec=PINK, lw=1.2))
    line(ax, [xT + 0.11, 5.0], [7.25, 7.25], PINK, lw=0.9, ls="--")
    ax.text(xT + 0.2, 7.36, "CT", fontsize=7.5, ha="left", va="bottom", color=PINK)
    # busbar
    ax.add_patch(Rectangle((0.3, 6.95), 12.9, 0.12, fc=INK, ec=INK))
    ax.text(0.3, 7.2, "400 V", fontsize=8.5, fontweight="bold")
    # motor load
    xm = 0.85
    line(ax, [xm, xm], [6.95, 6.2])
    breaker_v(ax, xm, 6.55)
    motor(ax, xm, 6.2, r=0.34)
    ax.text(xm, 5.4, "motors\n600 kW\nPF 0.78", fontsize=8, ha="center", va="top")
    # drives
    xd = 2.5
    line(ax, [xd, xd], [6.95, 6.2])
    breaker_v(ax, xd, 6.55)
    box(ax, xd - 0.55, 5.35, 1.1, 0.85, "6-pulse\ndrives", fc="#FBE9DD", fontsize=8)
    ax.annotate("", xy=(xd + 0.85, 6.85), xytext=(xd + 0.85, 5.4),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.6, mutation_scale=12))
    ax.text(xd + 1.0, 5.6, "$I_5$", color=COLORS[1], fontsize=10)
    # controller
    box(ax, 5.0, 7.6, 2.4, 0.8, "PF controller\n(6 steps)", fc="#F3EAF2", fontsize=8)
    line(ax, [5.0, 5.0], [7.25, 7.6], PINK, lw=0.9, ls="--")
    # six steps
    xs = np.linspace(5.2, 12.6, 6)
    ycmd = 8.0
    line(ax, [7.4, xs[-1] + 0.3], [ycmd, ycmd], PINK, lw=0.8, ls="--")
    ax.text(9.6, ycmd + 0.1, "step switching commands", fontsize=7.5, color=PINK, va="bottom")
    for i, x in enumerate(xs):
        line(ax, [x, x], [6.95, 6.5])
        breaker_v(ax, x, 6.72, s=0.18)
        y = switch_v(ax, x, 6.5)
        line(ax, [x, x], [y, y - 0.15])
        y = inductor_v(ax, x, y - 0.15)
        line(ax, [x, x], [y, y - 0.15])
        y = y - 0.15
        ax.add_patch(Polygon([[x - 0.32, y - 0.85], [x + 0.32, y - 0.85], [x, y - 0.3]],
                             closed=True, fill=False, ec=INK, lw=1.0))
        line(ax, [x, x], [y, y - 0.3])
        ax.text(x, y - 0.68, "C", fontsize=7, ha="center", va="center")
        ax.text(x, y - 1.0, f"step {i + 1}", fontsize=7.5, ha="center", va="top")
        if i == 0:
            ax.text(x - 0.28, 6.25, "K", fontsize=7.5, ha="right", va="center")
            ax.text(x - 0.25, 5.65, "L", fontsize=7.5, ha="right", va="center")
            ax.text(x - 0.42, y - 0.6, "Δ", fontsize=7.5, ha="right", va="center")
        ytop = 7.6 if x < 7.4 else ycmd
        line(ax, [x + 0.3, x + 0.3], [ytop, 6.25], PINK, lw=0.8, ls="--")

    # data panel
    box(ax, 0.3, 0.7, 12.9, 2.0, "", fc="#EEF3F8")
    left = ("Each step: contactor K, 7 % reactor L,\n"
            "delta-connected capacitors rated 480 V\n"
            "Bank total per delta branch:\n"
            "   L = 0.375 mH,  C = 1889 µF")
    right = ("$X_C$ = 1.685 Ω,  $X_L$ = 0.07 $X_C$ = 0.118 Ω\n"
             "306 kvar effective (PF 0.78 → 0.96)\n"
             "Tuning $h_t$ = 1/√0.07 = 3.78  →  189 Hz\n"
             "Capacitor voltage 400 / 0.93 = 430 V")
    ax.text(0.55, 2.55, left, fontsize=8, va="top", linespacing=1.5)
    ax.text(7.0, 2.55, right, fontsize=8, va="top", linespacing=1.5)
    save(fig, CH, "fig-25-4-detuned-bank")


# ----------------------------------------------------------------------------
# Figure 25.5
# ----------------------------------------------------------------------------
def fig_25_5():
    """Location of power-quality mitigation devices in an MV/LV supply."""
    from matplotlib.lines import Line2D
    C_SRC, C_NET, C_LOAD = COLORS[1], COLORS[0], COLORS[2]
    fig, ax = schematic(6.8, 5.3, xlim=(0, 14), ylim=(0.1, 11.0))
    fs = 7.5

    # 33 kV source, arrester, transformer
    x0 = 1.0
    ax.add_patch(Circle((x0, 10.45), 0.38, fc="white", ec=INK, lw=1.2))
    ax.text(x0, 10.45, "~", ha="center", va="center", fontsize=13)
    ax.text(x0 + 0.55, 10.55, "33 kV source\n750 MVA", fontsize=8, va="center")
    line(ax, [x0, x0], [10.07, 9.45])
    line(ax, [x0, 3.0], [9.85, 9.85])
    arrester_v(ax, 3.0, 9.85, C_NET)
    ax.text(3.25, 9.45, "arrester", fontsize=fs, color=C_NET, va="center")
    yb = transformer_v(ax, x0, 9.45, r=0.3)
    ax.text(x0 + 0.45, 8.95, "33/11 kV", fontsize=8, va="center")
    line(ax, [x0, x0], [yb, 7.5])
    # PCC meter on the incomer
    ax.add_patch(Circle((x0, 8.0), 0.1, fill=False, ec=COLORS[3], lw=1.2))
    line(ax, [x0 + 0.1, 1.6], [8.0, 8.0], COLORS[3], lw=0.9)
    box(ax, 1.6, 7.72, 3.8, 0.58, "", fc="#F3EAF2", ec=COLORS[3])
    ax.text(3.5, 8.01, "PCC meter, IEC 61000-4-30\nClass A", fontsize=6.8, ha="center",
            va="center")

    # 11 kV bus
    yB = 7.4
    ax.add_patch(Rectangle((0.4, yB), 13.2, 0.12, fc=INK))
    ax.text(13.6, yB + 0.22, "11 kV bus", fontsize=8.5, ha="right", fontweight="bold")

    def feeder(x, ybus, ylow, brk=True):
        line(ax, [x, x], [ybus, ylow])
        if brk:
            breaker_v(ax, x, ybus - 0.25, s=0.2)

    # arrester on 11 kV
    xa = 4.6
    feeder(xa, yB, 6.95, brk=False)
    arrester_v(ax, xa, 6.95, C_NET)
    ax.text(xa, 6.0, "arrester", fontsize=fs, ha="center", va="top", color=C_NET)
    # furnace / drive
    xf = 6.0
    feeder(xf, yB, 6.7)
    box(ax, xf - 0.78, 5.85, 1.56, 0.85, "large drive\nor arc\nfurnace", fc="#FBE9DD", fontsize=6.8)
    # STATCOM
    xs_ = 7.6
    feeder(xs_, yB, 6.7)
    box(ax, xs_ - 0.68, 5.95, 1.36, 0.75, "STATCOM", fc="white", ec=C_NET, fontsize=7.2)
    ax.text(xs_, 5.85, "flicker,\nvar control", fontsize=6.8, ha="center", va="top", color=C_NET)
    # 5th tuned filter
    xt = 9.2
    feeder(xt, yB, 6.85)
    y = inductor_v(ax, xt, 6.85, color=C_NET)
    line(ax, [xt, xt], [y, y - 0.1], C_NET)
    y = capacitor_v(ax, xt, y - 0.1, color=C_NET)
    ground(ax, xt, y)
    ax.text(xt, y - 0.25, "5th tuned\nfilter 1.5 Mvar\n$h_t$ = 4.7", fontsize=6.8, ha="center",
            va="top", color=C_NET)
    # high-pass branch
    xh = 10.8
    feeder(xh, yB, 6.85)
    y = capacitor_v(ax, xh, 6.85, color=C_NET)
    line(ax, [xh - 0.22, xh + 0.22], [y, y], C_NET)
    yl = inductor_v(ax, xh - 0.22, y, color=C_NET)
    ax.add_patch(Rectangle((xh + 0.14, yl + 0.04), 0.16, y - yl - 0.08, fill=False, ec=C_NET, lw=1.1))
    line(ax, [xh + 0.22, xh + 0.22], [y, y - 0.04], C_NET)
    line(ax, [xh + 0.22, xh + 0.22], [yl + 0.04, yl], C_NET)
    line(ax, [xh - 0.22, xh + 0.22], [yl, yl], C_NET)
    line(ax, [xh, xh], [yl, yl - 0.1], C_NET)
    ground(ax, xh, yl - 0.1)
    ax.text(xh, yl - 0.35, "high-pass\nbranch\n(11th and up)", fontsize=6.8, ha="center", va="top",
            color=C_NET)
    # 11/0.4 kV transformer
    xT2 = 12.6
    feeder(xT2, yB, 6.85)
    yb2 = transformer_v(ax, xT2, 6.85, r=0.3)
    ax.text(xT2 + 0.42, 6.35, "11/0.4\nkV", fontsize=8, va="center")
    yL = 4.1
    line(ax, [xT2, xT2], [yb2, yL])

    # 400 V bus
    ax.add_patch(Rectangle((0.4, yL), 13.2, 0.12, fc=INK))
    ax.text(0.4, yL + 0.22, "400 V bus", fontsize=8.5, fontweight="bold")
    # SPD
    xp = 1.0
    feeder(xp, yL, 3.7, brk=False)
    arrester_v(ax, xp, 3.7, C_LOAD)
    ax.text(xp, 2.75, "SPD", fontsize=fs, ha="center", va="top", color=C_LOAD)
    # detuned PFC bank
    xc = 2.7
    feeder(xc, yL, 3.6)
    y = inductor_v(ax, xc, 3.6, color=C_NET)
    line(ax, [xc, xc], [y, y - 0.1], C_NET)
    y = capacitor_v(ax, xc, y - 0.1, color=C_NET)
    ground(ax, xc, y)
    ax.text(xc, y - 0.25, "detuned\nPFC bank\n$p$ = 7 %", fontsize=6.8, ha="center", va="top",
            color=C_NET)
    # active harmonic filter
    xh2 = 4.5
    feeder(xh2, yL, 3.5)
    box(ax, xh2 - 0.7, 2.6, 1.4, 0.9, "active\nharmonic\nfilter", fc="white", ec=C_NET, fontsize=6.8)
    # drives with line reactors
    xd = 6.4
    feeder(xd, yL, 3.6)
    y = inductor_v(ax, xd, 3.6, color=C_SRC)
    ax.text(xd + 0.22, 3.35, "line\nreactor", fontsize=6.8, va="center", color=C_SRC)
    line(ax, [xd, xd], [y, 2.85])
    box(ax, xd - 0.6, 2.05, 1.2, 0.8, "drives", fc="#FBE9DD", fontsize=7.2)
    # DVR + sensitive process
    xv = 8.6
    feeder(xv, yL, 3.55)
    box(ax, xv - 0.62, 2.8, 1.24, 0.75, "series\nDVR", fc="white", ec=C_LOAD, fontsize=6.8)
    line(ax, [xv, xv], [2.8, 2.4])
    box(ax, xv - 0.75, 1.5, 1.5, 0.9, "sensitive\nprocess", fc="#FFF6DD", fontsize=6.8)
    # UPS + IT load
    xu = 10.6
    feeder(xu, yL, 3.55)
    box(ax, xu - 0.62, 2.8, 1.24, 0.75, "online\nUPS", fc="white", ec=C_LOAD, fontsize=6.8)
    line(ax, [xu, xu], [2.8, 2.4])
    box(ax, xu - 0.75, 1.5, 1.5, 0.9, "IT load", fc="#FFF6DD", fontsize=6.8)

    handles = [Line2D([], [], color=C_SRC, lw=3, label="at the source (emission)"),
               Line2D([], [], color=C_NET, lw=3, label="in the network"),
               Line2D([], [], color=C_LOAD, lw=3, label="at the sensitive load (immunity)")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3, fontsize=7.5,
              frameon=False, handlelength=1.8, columnspacing=1.2)
    save(fig, CH, "fig-25-5-mitigation-locations")


if __name__ == "__main__":
    fig_25_1()
    fig_25_2()
    fig_25_3()
    fig_25_4()
    fig_25_5()
