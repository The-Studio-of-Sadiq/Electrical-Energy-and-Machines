"""Figures for Chapter 23 — Power-System Protection.\n\nRun from the repository root:  python figures/scripts/ch23.py\n"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon, Wedge
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter

from figstyle import new_fig, schematic, save, COLORS, INK

CH = "23"


def line(ax, xs, ys, color=INK, lw=1.3, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def breaker(ax, x, y, s=0.32):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.2, zorder=5))


def ct(ax, x, y, color, r=0.16):
    ax.add_patch(Circle((x, y), r, fc="none", ec=color, lw=1.4, zorder=6))


def si(M, tms=1.0):
    return tms * 0.14 / (M ** 0.02 - 1)


def log_axes(ax):
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(True, which="major", lw=0.6)
    ax.grid(True, which="minor", lw=0.3, color="#EEEEEE")


def plain(v, _):
    return f"{v:g}"


# ----------------------------------------------------------------------------
# Figure 23.1 — overlapping zones of protection
# ----------------------------------------------------------------------------
def fig_23_1():
    fig, ax = schematic(6.9, 3.6, xlim=(0.0, 20.2), ylim=(0.2, 8.0))
    y0, yl1, yl2 = 4.0, 5.7, 2.3
    zc = {1: COLORS[0], 2: COLORS[1], 3: COLORS[2], 4: COLORS[3], 5: COLORS[4], "3b": COLORS[2],
          6: COLORS[5], 7: COLORS[0]}

    # generator
    ax.add_patch(Circle((1.1, y0), 0.45, fc="white", ec=INK, lw=1.3, zorder=4))
    ax.text(1.1, y0, "G", ha="center", va="center", fontsize=10, zorder=5)
    line(ax, [1.55, 3.35], [y0, y0])
    breaker(ax, 2.4, y0)
    # step-up transformer
    for xc in (3.65, 4.15):
        ax.add_patch(Circle((xc, y0), 0.33, fill=False, ec=INK, lw=1.3, zorder=4))
    line(ax, [4.48, 6.8], [y0, y0])
    breaker(ax, 5.6, y0)
    # 132 kV double busbar
    for xb in (6.8, 7.1):
        ax.plot([xb, xb], [1.7, 6.3], color=INK, lw=3.0, solid_capstyle="butt")
    ax.text(6.6, 1.75, "132 kV\ndouble\nbus", ha="right", va="bottom", fontsize=7)
    # two 60 km lines
    for yl in (yl1, yl2):
        line(ax, [6.8, 14.0], [yl, yl])
        ax.plot([6.8, 7.1], [yl, yl], "o", ms=3, color=INK, zorder=6)
        breaker(ax, 8.0, yl)
        breaker(ax, 13.0, yl)
        ax.text(10.5, yl + 0.12, "132 kV line, 60 km", ha="center", va="bottom", fontsize=7.5)
    # remote 132 kV bus, transformer and 33 kV bus
    ax.plot([14.0, 14.0], [1.7, 6.3], color=INK, lw=3.0, solid_capstyle="butt")
    line(ax, [14.0, 15.45], [y0, y0])
    breaker(ax, 14.6, y0)
    for xc in (15.75, 16.25):
        ax.add_patch(Circle((xc, y0), 0.33, fill=False, ec=INK, lw=1.3, zorder=4))
    line(ax, [16.58, 18.4], [y0, y0])
    breaker(ax, 17.4, y0)
    ax.plot([18.4, 18.4], [3.0, 5.0], color=INK, lw=3.0, solid_capstyle="butt")
    for yy in (3.2, 4.8):
        ax.annotate("", xy=(19.9, yy), xytext=(18.4, yy),
                    arrowprops=dict(arrowstyle="-|>", lw=1.2, color=INK, mutation_scale=9))
    ax.text(18.4, 5.05, "33 kV", ha="center", va="bottom", fontsize=7.5)

    # zones: (x0, x1, y0, y1, key, label, label position)
    zones = [
        (0.35, 2.8, 2.75, 5.25, 1, "Zone 1\n87G", "b"),
        (2.0, 6.0, 3.0, 5.0, 2, "Zone 2\n87T", "b"),
        (5.2, 8.4, 1.15, 6.85, 3, "Zone 3\n87B", "b"),
        (7.6, 13.4, 5.2, 6.45, 4, "Zone 4: 21 + 87L", "t"),
        (7.6, 13.4, 1.55, 2.8, 5, "Zone 5: 21 + 87L", "b"),
        (12.6, 15.0, 1.15, 6.85, "3b", "87B\n(remote bus)", "b"),
        (14.2, 17.8, 3.0, 5.0, 6, "Zone 6\n87T", "b"),
        (17.0, 19.4, 2.45, 5.55, 7, "Zone 7\n87B", "t"),
    ]
    for x0, x1, yb, yt, key, lab, pos in zones:
        c = zc[key]
        ax.add_patch(FancyBboxPatch((x0, yb), x1 - x0, yt - yb, boxstyle="round,pad=0,rounding_size=0.25",
                                    fc="none", ec=c, lw=1.3, ls=(0, (4, 2.5)), zorder=3))
        if pos == "t":
            ax.text((x0 + x1) / 2, yt + 0.08, lab, ha="center", va="bottom", fontsize=7.2, color=c)
        else:
            ax.text((x0 + x1) / 2, yb - 0.08, lab, ha="center", va="top", fontsize=7.2, color=c)

    # CTs on the far side of each breaker relative to the zone they feed
    cts = [(2.8, y0, 1), (2.0, y0, 2), (6.0, y0, 2), (5.2, y0, 3),
           (8.4, yl1, 3), (8.4, yl2, 3), (7.6, yl1, 4), (7.6, yl2, 5),
           (13.4, yl1, 4), (13.4, yl2, 5), (12.6, yl1, "3b"), (12.6, yl2, "3b"),
           (15.0, y0, "3b"), (14.2, y0, 6), (17.8, y0, 6), (17.0, y0, 7)]
    for x, y, key in cts:
        ct(ax, x, y, zc[key])

    # equipment labels
    ax.text(1.1, y0 - 0.52, "200 MVA", ha="center", va="top", fontsize=7)
    ax.text(3.95, 5.1, "200 MVA\n15.75/132 kV", ha="center", va="bottom", fontsize=7)
    ax.text(16.0, 5.1, "60 MVA\n132/33 kV", ha="center", va="bottom", fontsize=7)

    # fault in overlap near a 132 kV breaker
    xf = 8.2
    ax.plot([xf], [yl1], marker=(8, 2, 0), ms=12, color=COLORS[1], mew=1.6, zorder=8)
    ax.annotate("F lies in zones 3 and 4:\nbusbar and line\nprotection both trip",
                xy=(xf, yl1), xytext=(10.75, 4.0), fontsize=7.5, color=COLORS[1], ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.8))
    # legend for symbols
    breaker(ax, 0.6, 1.15, s=0.26)
    ax.text(0.9, 1.15, "circuit breaker", va="center", fontsize=7)
    ct(ax, 0.6, 0.6, INK, r=0.13)
    ax.text(0.9, 0.6, "CT (colour = zone it feeds)", va="center", fontsize=7)
    save(fig, CH, "fig-23-1-protection-zones")


# ----------------------------------------------------------------------------
# Figure 23.2 — IEC IDMT curves
# ----------------------------------------------------------------------------
def fig_23_2():
    M = np.logspace(np.log10(1.02), np.log10(30), 600)
    tms = 0.1
    t_si = tms * 0.14 / (M ** 0.02 - 1)
    t_vi = tms * 13.5 / (M - 1)
    t_ei = tms * 80 / (M ** 2 - 1)
    fig, ax = new_fig(6.4, 4.2)
    log_axes(ax)
    ax.plot(M, t_si, "-", color=COLORS[0], label="standard inverse  $0.014/(M^{0.02}-1)$")
    ax.plot(M, t_vi, "--", color=COLORS[1], label="very inverse  $1.35/(M-1)$")
    ax.plot(M, t_ei, ":", color=COLORS[2], lw=2.2, label="extremely inverse  $8/(M^2-1)$")
    # definite-time + instantaneous
    ax.plot([1.5, 1.5, 15, 15, 30], [100, 0.5, 0.5, 0.03, 0.03], color=INK, lw=1.4,
            label="definite time 0.5 s ($M\\geq1.5$) + instantaneous 0.03 s ($M\\geq15$)")
    # worked example points
    for t, c in ((si(10, tms), COLORS[0]), (tms * 13.5 / 9, COLORS[1]), (tms * 80 / 99, COLORS[2])):
        ax.plot([10], [t], "o", color=c, ms=5, zorder=5)
    ax.annotate("M = 10: SI 0.297 s,\nVI 0.150 s, EI 0.081 s", xy=(10, si(10, tms)), xytext=(17, 1.6),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    for t, c, ha in ((si(2, tms), COLORS[0], "right"), (1.35, COLORS[1], "left"), (80 / 3 * tms, COLORS[2], "left")):
        ax.plot([2], [t], "s", color=c, ms=4, zorder=5)
    ax.text(1.93, 0.93, "1.00 s", ha="right", va="top", fontsize=7.5, color=COLORS[0])
    ax.text(2.07, 1.27, "1.35 s", ha="left", va="top", fontsize=7.5, color=COLORS[1])
    ax.text(2.08, 2.67, "2.67 s", ha="left", va="center", fontsize=7.5, color=COLORS[2])
    ax.text(1.95, 0.25, "M = 2", ha="center", fontsize=7.5, color="#555555")
    ax.set_xlim(1, 30)
    ax.set_ylim(0.01, 100)
    ax.xaxis.set_major_formatter(FuncFormatter(plain))
    ax.xaxis.set_minor_formatter(FuncFormatter(lambda v, _: f"{v:g}" if v in (2, 3, 5, 20, 30) else ""))
    ax.yaxis.set_major_formatter(FuncFormatter(plain))
    ax.set_xlabel("Multiple of setting $M = I/I_s$")
    ax.set_ylabel("Operating time $t$ (s)")
    ax.legend(loc="upper right", fontsize=7.5, handlelength=2.6)
    ax.text(1.05, 0.013, "IEC 60255-151, TMS = 0.1", fontsize=8, color="#444444")
    save(fig, CH, "fig-23-2-idmt-curves")


# ----------------------------------------------------------------------------
# Figure 23.3 — biased differential characteristic
# ----------------------------------------------------------------------------
def fig_23_3():
    b = np.linspace(0, 10, 1001)
    b1 = 0.25 / 0.30 + 0.0      # knee where slope 1 starts: 0.25 = 0.3*b -> b = 0.833
    thr = np.where(b <= b1, 0.25, np.where(b <= 2.0, 0.25 + 0.30 * (b - b1), 0.6 + 0.70 * (b - 2.0)))
    thr[(b > b1) & (b <= 2.0)] = 0.25 + 0.35 * (b[(b > b1) & (b <= 2.0)] - b1) / (2.0 - b1)
    fig, ax = new_fig(6.4, 4.0)
    ax.fill_between(b, thr, 6.5, color="#FBE3D6", zorder=0)
    ax.fill_between(b, 0, thr, color="#E3EEF8", zorder=0)
    ax.plot(b, thr, color=INK, lw=2.0)
    ax.text(1.0, 4.6, "TRIP", fontsize=13, weight="bold", color=COLORS[1])
    ax.text(4.3, 1.5, "RESTRAIN", fontsize=13, weight="bold", color=COLORS[0])
    ax.text(0.05, 0.21, "pickup 0.25 pu", fontsize=8, va="top")
    ax.annotate("slope 30 %", xy=(1.45, 0.43), xytext=(2.6, 0.62), fontsize=8, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    ax.text(5.6, 3.45, "slope 70 %", fontsize=8, rotation=38, ha="center")
    # internal fault trajectory along Idiff = 2 Ibias
    bi = np.array([0.5, 1.0, 1.6, 2.2, 2.6, 3.0])
    ax.plot(bi, 2 * bi, "o-", color=COLORS[1], ms=4.5, lw=1.4, label="internal fault ($I_{diff}=2I_{bias}$)")
    ax.annotate("internal fault\n(3, 6)", xy=(3.0, 6.0), xytext=(3.4, 5.3), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    # external fault with CT saturation
    be = np.array([2.0, 3.5, 5.0, 7.0, 8.0, 8.0, 8.0, 8.0])
    de = np.array([0.05, 0.08, 0.12, 0.15, 0.2, 1.0, 2.0, 3.0])
    ax.plot(be, de, "s-", color=COLORS[0], ms=4, lw=1.4, label="external fault, 8 pu through current, one CT saturating")
    ax.text(7.85, 2.4, "one CT saturates:\nrises to (8, 3.0),\nstill below the\n70 % slope", fontsize=8, color=COLORS[0],
            va="center", ha="right")
    ax.text(5.0, 0.22, "external fault, through current rising to 8 pu", fontsize=8, color=COLORS[0],
            ha="center", va="bottom")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_xlabel("Bias (restraint) current $I_{bias}$ (pu)")
    ax.set_ylabel("Differential current $I_{diff}$ (pu)")
    ax.text(9.9, 6.12, "unrestrained high-set differential at $I_{diff}$ = 8 pu (above this range)",
            ha="right", va="bottom", fontsize=7.5, color="#444444")
    save(fig, CH, "fig-23-3-biased-differential")


# ----------------------------------------------------------------------------
# Figure 23.4 — mho distance zones
# ----------------------------------------------------------------------------
def fig_23_4():
    zl = 10 + 40j
    ang = np.angle(zl)
    fig, ax = new_fig(6.4, 4.6)
    # load area
    rl = 104.8
    th = np.radians(np.linspace(-30, 30, 100))
    rr = 200
    poly = np.concatenate([np.c_[rl * np.cos(th), rl * np.sin(th)], np.c_[rr * np.cos(th[::-1]), rr * np.sin(th[::-1])]])
    ax.add_patch(Polygon(poly, closed=True, fc="#FBE3D6", ec="none", zorder=0))
    ax.text(110, 6, "load\narea", ha="center", va="center", fontsize=8.5, color=COLORS[1])
    # blinders along +-30 deg
    for sgn in (1, -1):
        r = np.array([45, 160])
        ax.plot(r * np.cos(np.radians(30)), sgn * r * np.sin(np.radians(30)), color=COLORS[1], lw=1.1, ls="-.")
    ax.annotate("load-encroachment\nblinders (±30°)", xy=(95, 95 * np.tan(np.radians(30))), xytext=(56, 66),
                fontsize=7.5, color=COLORS[1], ha="left", arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    # mho circles
    for D, lab, c in ((33.0, "Zone 1  33.0 Ω", COLORS[0]), (49.5, "Zone 2  49.5 Ω", COLORS[2]),
                      (82.5, "Zone 3  82.5 Ω", COLORS[3])):
        cen = D / 2 * np.exp(1j * ang)
        ax.add_patch(Circle((cen.real, cen.imag), D / 2, fill=False, ec=c, lw=1.6, zorder=3))
    for (tx, ty, px, py, lab, c) in ((-57, -11, -11.5, 12, "Zone 1  33.0 Ω", COLORS[0]),
                                      (-57, 2, -18.4, 20, "Zone 2  49.5 Ω", COLORS[2]),
                                      (-57, 15, -30.4, 30, "Zone 3  82.5 Ω", COLORS[3])):
        ax.annotate(lab, xy=(px, py), xytext=(tx, ty), fontsize=8, color=c, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color=c))
    # line impedance and adjacent line
    ax.annotate("", xy=(10, 40), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=2.0, color=INK,
                                                                mutation_scale=12), zorder=5)
    ax.plot([10, 20], [40, 80], color=INK, lw=1.3, ls="--", zorder=5)
    ax.annotate("$Z_L$ = 10 + j40 Ω\n= 41.2 Ω ∠76°", xy=(5.0, 20), xytext=(-5, 60), fontsize=8, va="center", ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    ax.text(21, 80, "adjacent line", fontsize=8, va="center")
    ax.plot([10], [40], "o", ms=4, color=INK, zorder=6)
    # fault at 60 km with 8 ohm fault resistance
    ax.plot([6, 14], [24, 24], color=COLORS[1], lw=1.0, zorder=6)
    ax.plot([14], [24], "X", ms=8, color=COLORS[1], zorder=7)
    ax.annotate("fault at 60 km\n+ 8 Ω fault resistance\n(14, 24)", xy=(14, 24), xytext=(36, 4),
                fontsize=7.5, color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    # power swing: equal EMFs, ZS small, ZR large -> straight locus through electrical centre at 40 ohm
    zs = 8.2 * np.exp(1j * ang)
    zr = 47.1 * np.exp(1j * ang)
    zt = zs + zl + zr
    d = np.radians(np.linspace(25, 330, 400))
    z = zt / (1 - np.exp(-1j * d)) - zs
    mask = (z.real > -60) & (z.real < 120) & (z.imag > -20) & (z.imag < 100)
    ax.plot(z.real[mask], z.imag[mask], color=COLORS[4], lw=1.6, ls="--", zorder=4)
    for dd in (60, 120, 180, 240):
        zz = zt / (1 - np.exp(-1j * np.radians(dd))) - zs
        ax.plot([zz.real], [zz.imag], "o", ms=3.5, color=COLORS[4], zorder=6)
        ax.text(zz.real + (9 if dd == 180 else 0), zz.imag + 3.0, f"δ = {dd}°", fontsize=7, ha="center", va="bottom",
                color="#8a6200")
    zz = zt / (1 - np.exp(-1j * np.radians(90))) - zs
    ax.annotate("", xy=(zz.real - 8, zz.imag + 2.0), xytext=(zz.real + 4, zz.imag - 1.0),
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=COLORS[4], mutation_scale=12))
    ax.text(-57, 45, "power-swing locus", fontsize=8, color="#8a6200", ha="left", va="top")
    ax.axhline(0, color="#888888", lw=0.7)
    ax.axvline(0, color="#888888", lw=0.7)
    ax.set_xlim(-60, 120)
    ax.set_ylim(-20, 100)
    ax.set_aspect("equal")
    ax.set_xlabel("R (Ω, primary)")
    ax.set_ylabel("X (Ω, primary)")
    ax.grid(True, lw=0.4)
    ax.text(118, 96, "100 km, 132 kV line\nmho characteristics\nalong 76°", fontsize=8, ha="right", va="top")
    ax.text(105, -12, "$Z_{load,min}$ = 104.8 Ω", fontsize=7.5, color=COLORS[1], ha="center")
    save(fig, CH, "fig-23-4-distance-zones")


# ----------------------------------------------------------------------------
# Figure 23.5 — current zero and TRV
# ----------------------------------------------------------------------------
def fig_23_5():
    f = 50.0
    w = 2 * np.pi * f
    tau = 0.045
    # asymmetrical fault current: i = Ip [sin(w(t - t0) - th) + sin(th) e^{-(t - t0)/tau}] with th = 90 deg
    t0 = -0.040                                         # fault inception (s)
    Ip = np.sqrt(2) * 40.0

    def i_f(t):
        tt = t - t0
        return Ip * (-np.cos(w * tt) + np.exp(-tt / tau))

    # find the current zero closest to -0 after a major loop; shift so that it lies at t = 0
    ts = np.linspace(-0.035, 0.0, 20001)
    vals = i_f(ts)
    zc = ts[np.where(np.diff(np.sign(vals)) != 0)[0]]
    tz = zc[-1]
    shift = -tz

    t = np.linspace(-0.025, 0.0, 3000)
    i = i_f(t - shift)
    tsep = -0.018                                        # contact separation
    ua = np.where(t > tsep, 1.0 * np.sign(i), 0.0)       # arc voltage, kV (rectangular)

    # TRV after current zero: u = Up [cos(w t) - e^{-a t} cos(w0 t)]
    Up = 1.3 * 145 * np.sqrt(2 / 3)                      # 153.9 kV
    tp = 260e-6
    w0 = np.pi / tp
    tr = np.linspace(0, 0.002, 4000)

    def trv(a):
        return Up * (np.cos(w * tr) - np.exp(-a * tr) * np.cos(w0 * tr))

    # choose the damping so that the amplitude factor is exactly 1.4 (peak 1.4 Up)
    from scipy.optimize import brentq
    a = brentq(lambda aa: trv(aa).max() - 1.4 * Up, 100.0, 20000.0)
    u = trv(a)
    upk = u.max()

    fig = plt.figure(figsize=(6.6, 5.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.4], hspace=0.10)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    tm = t * 1e3
    ax1.plot(tm, i, color=COLORS[0], label="fault current $i$")
    ax1.plot([0, 2], [0, 0], color=COLORS[0])
    ax1.axhline(0, color="#999999", lw=0.6)
    ax1.set_ylabel("Current (kA)")
    ax1.set_ylim(-60, 115)
    ax1b = ax1.twinx()
    ax1b.spines["right"].set_visible(True)
    ax1b.plot(tm, ua, color=COLORS[1], lw=1.2, label="arc voltage $u_a$")
    ax1b.plot([0, 2], [0, 0], color=COLORS[1], lw=1.2)
    ax1b.set_ylim(-1.6, 3.0)
    ax1b.set_ylabel("Arc voltage (kV)", color=COLORS[1])
    ax1b.tick_params(axis="y", colors=COLORS[1])
    ax1.axvline(tsep * 1e3, color="#888888", lw=0.8, ls=":")
    ax1.text(tsep * 1e3 + 0.25, 108, "contacts separate", fontsize=7.5, va="top")
    ax1.text(-24.6, -22, "asymmetrical fault\ncurrent, τ = 45 ms", fontsize=7.5, va="top", color=COLORS[0])
    ax1.annotate("current zero:\ninterruption", xy=(0, 0), xytext=(-4.2, -22), fontsize=7.5, ha="center",
                 va="top", arrowprops=dict(arrowstyle="-", lw=0.7))
    ax1.text(-17.7, -44, "arc voltage ≈ 1 kV, rectangular", fontsize=7.5, color=COLORS[1], va="top")
    plt.setp(ax1.get_xticklabels(), visible=False)

    # bottom: contact voltage
    ax2.plot(tm, np.where(t > tsep, ua, 0.0), color=COLORS[2])
    ax2.plot(tr * 1e3, u, color=COLORS[2], label="voltage across contacts")
    ax2.axhline(Up, color="#777777", lw=0.8, ls="--")
    ax2.text(-24.5, Up + 6, f"recovery voltage peak 1.3 × 145 × 0.816 = {Up:.0f} kV", fontsize=7.5, va="bottom")
    ax2.axhline(upk, color="#777777", lw=0.8, ls=":")
    ax2.text(-24.5, upk + 6, f"TRV peak 1.3 × 1.4 × 145 × 0.816 = {upk:.0f} kV", fontsize=7.5, va="bottom")
    ax2.axvline(0, color="#888888", lw=0.6)
    ax2.text(-24.5, 10, "≈ 0 while the arc burns", fontsize=7.5, color=COLORS[2])
    ax2.annotate("TRV", xy=(0.25, 200), xytext=(-2.5, 200), fontsize=7.5, color=COLORS[2], ha="right",
                 va="center", arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[2]))
    ax2.set_xlim(-25, 2.2)
    ax2.set_ylim(-20, 290)
    ax2.set_xlabel("Time from current zero (ms)")
    ax2.set_ylabel("Contact voltage (kV)")

    # inset: 0 to 600 us
    ins = ax2.inset_axes([0.36, 0.13, 0.50, 0.33])
    tu = tr[tr <= 600e-6] * 1e6
    uu = u[tr <= 600e-6]
    ins.plot(tu, uu, color=COLORS[2], lw=1.6, label="TRV")
    ok = 320 * (1 - np.exp(-tu / 140)) + 0.25 * tu
    bad = 120 * (1 - np.exp(-tu / 60)) + 0.10 * tu
    ins.plot(tu, ok, "--", color=COLORS[0], lw=1.3)
    ins.plot(tu, bad, "--", color=COLORS[1], lw=1.3)
    k = np.argmax(uu > bad)
    ins.plot([tu[k]], [uu[k]], "x", color=COLORS[1], ms=8, mew=2)
    ins.text(445, 395, "recovery faster:\ninterruption\nsucceeds", fontsize=6.6, color=COLORS[0],
             ha="center", va="top")
    ins.set_title("zoom: contact voltage (kV) vs time after current zero (µs)", fontsize=7, pad=2)
    ins.text(230, 100, "slower: crosses\nTRV, reignition", fontsize=6.6, color=COLORS[1],
             va="top")
    ins.set_xlim(0, 600)
    ins.set_ylim(0, 450)
    ins.set_xticks([0, 200, 400, 600])
    ins.set_yticks([0, 200, 400])
    ins.tick_params(labelsize=7)
    ins.set_facecolor("white")
    for sp in ("top", "right"):
        ins.spines[sp].set_visible(True)
    save(fig, CH, "fig-23-5-current-zero-trv")


# ----------------------------------------------------------------------------
# Figure 23.6 — coordination curves
# ----------------------------------------------------------------------------
def fuse_100k_tc(I):
    """Approximate total-clearing curve of a 100 A K-type expulsion fuse link.\n\n    Smooth (PCHIP) interpolation in log-log space through representative points of published\n    100K total-clearing curves; valid from about 230 A to 10 kA.\n    """
    from scipy.interpolate import PchipInterpolator
    pts_I = np.array([230, 300, 400, 600, 1000, 1500, 2000, 3000, 5000, 10000])
    pts_t = np.array([300, 60, 14, 3.0, 0.62, 0.20, 0.090, 0.040, 0.020, 0.0135])
    f = PchipInterpolator(np.log(pts_I), np.log(pts_t))
    I = np.asarray(I, dtype=float)
    out = np.full_like(I, np.nan)
    m = (I >= pts_I[0]) & (I <= pts_I[-1])
    out[m] = np.exp(f(np.log(I[m])))
    return out


def fig_23_6():
    I = np.logspace(2, 4, 800)
    tB = np.where(I > 1.03 * 200, si(I / 200, 0.10), np.nan)
    tA = np.where(I > 1.03 * 600, si(I / 600, 0.16), np.nan)
    tF = fuse_100k_tc(I)
    # 20 MVA 33/11 kV transformer through-fault (thermal) damage curve, I^2 t = 1250 pu^2 s
    Ir = 20e6 / (np.sqrt(3) * 11e3)
    Ipu = I / Ir
    tD = np.where(Ipu >= 2.0, 1250 / Ipu ** 2, np.nan)

    fig, ax = new_fig(6.4, 4.6)
    log_axes(ax)
    ax.plot(I, tF, color=COLORS[2], label="100 A K-type fuse, total clearing (approx.)")
    ax.plot(I, tB, color=COLORS[0], label="relay B: SI, $I_s$ = 200 A, TMS 0.10")
    ax.plot(I, tA, color=COLORS[1], label="relay A: SI, $I_s$ = 600 A, TMS 0.16")
    ax.plot(I, tD, "--", color=INK, lw=1.2, label="20 MVA transformer through-fault damage")
    for x, lab in ((2000, "2 kA"), (5000, "5 kA (max fault at B)"), (8000, "8 kA (busbar)")):
        ax.axvline(x, color="#777777", lw=0.9, ls="--")
        ax.text(x / 1.04, 1.6, lab, fontsize=7.5, va="bottom", ha="right", rotation=90)
    for x in (2000, 5000):
        for tms, Is, c in ((0.10, 200, COLORS[0]), (0.16, 600, COLORS[1])):
            tt = si(x / Is, tms)
            ax.plot([x], [tt], "o", color=c, ms=4, zorder=5)
            if c == COLORS[1]:
                ax.text(x * 1.05, tt * 1.12, f"{tt:.3f} s", fontsize=7.2, ha="left", va="bottom", color=c)
            else:
                ax.text(x / 1.05, tt / 1.12, f"{tt:.3f} s", fontsize=7.2, ha="right", va="top", color=c)
    tt = si(8000 / 600, 0.16)
    ax.plot([8000], [tt], "o", color=COLORS[1], ms=4, zorder=5)
    ax.text(8000 * 1.05, tt * 1.1, f"{tt:.3f} s", fontsize=7.2, ha="left", va="bottom", color=COLORS[1])
    tf2 = fuse_100k_tc(np.array([2000.0]))[0]
    ax.plot([2000], [tf2], "o", color=COLORS[2], ms=4, zorder=5)
    ax.text(2000 / 1.06, tf2, f"{tf2:.3f} s", fontsize=7.2, ha="right", va="center", color=COLORS[2])
    # fuse-to-B margin at 2 kA (maximum fault at the lateral)
    tb2 = si(10, 0.10)
    ax.annotate("", xy=(2000 * 1.1, tb2), xytext=(2000 * 1.1, tf2),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color=INK, mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(2000 * 1.16, 0.165, f"{round(tb2, 3) - round(tf2, 3):.2f} s\nfuse–B", fontsize=7.2, va="center")
    # grading margin at 5 kA
    tb5, ta5 = si(25, 0.10), si(5000 / 600, 0.16)
    ax.annotate("", xy=(5000 * 1.05, ta5), xytext=(5000 * 1.05, tb5),
                arrowprops=dict(arrowstyle="<|-|>", lw=1.0, color=INK, mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(5000 * 1.09, 0.33, f"{round(ta5, 3) - round(tb5, 3):.3f} s\nA–B", fontsize=7.0, va="center")
    # fuse / relay B crossing
    d = np.log(tF) - np.log(tB)
    k = np.where(np.isfinite(d[:-1]) & (np.sign(d[:-1]) != np.sign(d[1:])))[0]
    if len(k):
        xc = I[k[-1]]
        ax.annotate(f"fuse and B cross at ≈{xc / 1000:.1f} kA:" + "\n" + "below this B is faster",
                    xy=(xc, si(xc / 200, 0.10)), xytext=(330, 0.16), fontsize=7.2, color="#444444",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="#444444"))
    ax.set_xlim(100, 10000)
    ax.set_ylim(0.01, 100)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_major_formatter(FuncFormatter(plain))
    ax.set_xlabel("Current at 11 kV (A)")
    ax.set_ylabel("Time (s)")
    ax.legend(loc="lower left", fontsize=7.5, frameon=True, facecolor="white", edgecolor="#CCCCCC")
    save(fig, CH, "fig-23-6-coordination-curves")


if __name__ == "__main__":
    fig_23_1()
    fig_23_2()
    fig_23_3()
    fig_23_4()
    fig_23_5()
    fig_23_6()
