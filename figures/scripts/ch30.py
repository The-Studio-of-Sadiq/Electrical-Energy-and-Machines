"""Figures for Chapter 30 — Electrical System Design.

Run from the repository root:  python figures/scripts/ch30.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon
from matplotlib.ticker import FixedLocator, NullFormatter

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID

GREY = "#8A8A8A"
RED = "#C0392B"


# ---------------------------------------------------------------- 30.1
def _darrow(ax, p0, p1, rad, text, tx, ty, color=COLORS[1], ha="center"):
    """Dashed curved feedback arrow with a label."""
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=10, color=color, lw=1.1, ls=(0, (4, 2.5))))
    ax.text(tx, ty, text, fontsize=7, color=color, ha=ha, va="center", style="italic")


def fig_design_flow():
    fig, ax = schematic(6.8, 4.8, xlim=(0, 17.4), ylim=(-0.5, 11.6))
    w, h = 3.15, 1.55
    fs = 7.0
    y1, yg, y2 = 8.1, 5.15, 1.45
    r1 = [(0.05, "Load schedule and\ndemand factors\n(30.1)"),
          (3.55, "Maximum demand\nand growth"),
          (7.0, "Transformer rating\nand impedance\n(30.2)"),
          (10.6, "Fault levels:\n$I''_k$, $i_p$ at each\nboard (30.4)"),
          (14.2, "Equipment ratings:\n$I_n$, $I_{cw}$, $I_{cu}$\n(30.4)")]
    r2 = [(0.1, "Cable sizing:\n$I_z$, derating,\nadiabatic (30.5)"),
          (3.55, "Voltage drop,\nrunning and\nstarting (30.6)"),
          (7.0, "Protection: $I_n$,\nsettings, selectivity,\narc flash (30.7)"),
          (10.6, "Earthing: system,\nPE, electrodes,\n$Z_s$ check (30.8)"),
          (14.2, "Documentation\nand verification\n(30.9, 30.10)")]
    for x, t in r1:
        box(ax, x, y1, w, h, t, fontsize=fs)
    for x, t in r2:
        box(ax, x, y2, w, h, t, fontsize=fs, fc="#EEF5EE" if "Documentation" in t else "#EEF3F8")
    gx = 7.0
    box(ax, gx, yg, w, h, "Essential loads →\ngenerator rating\n(30.3)", fontsize=fs, fc="#FFF4D6")
    # forward arrows row 1
    for (xa, _), (xb, _) in zip(r1[:-1], r1[1:]):
        arrow(ax, xa + w, y1 + h / 2, xb, y1 + h / 2)
    for (xa, _), (xb, _) in zip(r2[:-1], r2[1:]):
        arrow(ax, xa + w, y2 + h / 2, xb, y2 + h / 2)
    # demand -> generator, generator -> fault level
    ax.plot([5.0, 5.0], [y1, yg + h / 2], color=INK, lw=1.1)
    arrow(ax, 5.0, yg + h / 2, gx, yg + h / 2)
    ax.plot([gx + w, 12.05], [yg + h / 2, yg + h / 2], color=INK, lw=1.1)
    arrow(ax, 12.05, yg + h / 2, 12.05, y1)
    # wrap from equipment ratings to cable sizing
    ax.plot([15.75, 15.75, 1.6], [y1, 3.35, 3.35], color=INK, lw=1.1)
    arrow(ax, 1.6, 3.35, 1.6, y2 + h)
    # feedback loops (dashed)
    fb = dict(color=COLORS[1], lw=1.1, ls=(0, (4, 2.5)))
    ax.plot([5.1, 5.1, 2.3], [y2, 0.8, 0.8], **fb)
    arrow(ax, 2.3, 0.8, 2.3, y2, color=COLORS[1])
    ax.text(5.3, 0.8, "voltage drop too high: increase size", fontsize=7, color=COLORS[1],
            ha="left", va="center", style="italic")
    ax.plot([8.6, 8.6, 0.9], [y2, 0.0, 0.0], **fb)
    arrow(ax, 0.9, 0.0, 0.9, y2, color=COLORS[1])
    ax.text(8.75, 0.0, "adiabatic or $Z_s$ check fails:\nlarger cable, larger PE or other device",
            fontsize=7, color=COLORS[1], ha="left", va="center", style="italic")
    _darrow(ax, (12.05, y1 + h), (8.45, y1 + h), 0.5,
            "ratings too high: change impedance\nor split the bus", 10.25, 11.15)
    _darrow(ax, (gx + w - 0.4, yg), (gx + 0.4, yg), -0.75,
            "motor-start dip > 15–20 %: larger set or soft starter", gx + w / 2, 3.75)
    ax.text(5.15, 6.6, "essential\nloads", fontsize=6.5, color=GREY, va="center")
    save(fig, "30", "fig-30-1-design-flow")


# ---------------------------------------------------------------- 30.2
def _cb(ax, x, y, s=0.26, fc="white"):
    """Circuit-breaker square centred on (x, y)."""
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=INK, lw=1.1, zorder=3))


def _earth(ax, x, y, s=0.22):
    ax.plot([x, x], [y, y - 0.2], color=INK, lw=1.1)
    for i, f in enumerate([1.0, 0.65, 0.3]):
        ax.plot([x - s * f, x + s * f], [y - 0.2 - i * 0.1] * 2, color=INK, lw=1.1)


def fig_facility_single_line():
    fig, ax = schematic(6.8, 5.6, xlim=(-0.3, 14.3), ylim=(-0.2, 11.8))
    lw = 1.3
    t = dict(fontsize=6.8, color=INK)
    X = 3.0
    # utility
    ax.plot([X - 0.6, X + 0.6], [11.4, 11.4], color=INK, lw=3)
    ax.text(X + 0.75, 11.4, "11 kV utility supply, 250 MVA", va="center", **t)
    ax.plot([X, X], [11.4, 9.95], color=INK, lw=lw)
    # RMU with fuse-switch
    ax.add_patch(Rectangle((X - 0.55, 9.95), 1.1, 0.95, fc="#F2F2F2", ec=INK, lw=1.0, ls="--"))
    ax.add_patch(Rectangle((X - 0.1, 10.15), 0.2, 0.55, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.plot([X, X], [10.18, 10.67], color=INK, lw=0.8, zorder=4)
    ax.text(X + 0.75, 10.42, "11 kV ring main unit\nwith fuse-switch", va="center", **t)
    ax.plot([X, X], [9.95, 9.35], color=INK, lw=lw)
    # transformer
    ax.add_patch(Circle((X, 9.0), 0.4, fill=False, ec=INK, lw=lw))
    ax.add_patch(Circle((X, 8.45), 0.4, fill=False, ec=INK, lw=lw))
    ax.text(X + 0.75, 8.72, "1250 kVA Dyn11\n11/0.4 kV, $u_k$ = 6 %", va="center", **t)
    ax.plot([X, X], [8.05, 7.2], color=INK, lw=lw)
    # neutral to MET and foundation electrode
    ax.plot([X - 0.25, 1.0, 1.0], [8.3, 8.3, 7.05], color=COLORS[2], lw=1.1)
    ax.add_patch(Rectangle((0.45, 6.6), 1.1, 0.45, fc="#E5F3EC", ec=INK, lw=1.0))
    ax.text(1.0, 6.82, "MET", ha="center", va="center", fontsize=6.8)
    ax.plot([1.0, 1.0], [6.6, 6.2], color=COLORS[2], lw=1.1)
    _earth(ax, 1.0, 6.2)
    ax.text(1.0, 5.55, "foundation earth\nelectrode 1.15 Ω", fontsize=6.3, va="top", ha="center")
    ax.text(1.1, 8.38, "N", fontsize=6.3, color=COLORS[2], va="bottom")
    # incomer ACB
    _cb(ax, X, 6.95, s=0.34)
    ax.text(X + 0.75, 6.95, "ACB 2000 A frame, $I_r$ = 1800 A", va="center", **t)
    ax.plot([X, X], [6.78, 6.1], color=INK, lw=lw)
    # MSB busbar
    yb = 6.1
    ax.plot([1.9, 11.4], [yb, yb], color=INK, lw=4)
    ax.text(1.95, yb + 0.12, "MSB 400 V, busbars 2000 A, $I_{cw}$ = 50 kA 1 s", fontsize=7,
            va="bottom", fontweight="bold")
    ax.text(11.45, yb + 0.12, "$I''_k$ = 29.1 kA", fontsize=7, color=RED, ha="right",
            va="bottom", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=RED, lw=0.7))
    # outgoing feeders
    feeders = [(2.25, "compressor\nMCC\n4 × 110 kW\nVSDs"),
               (3.9, "PSB"),
               (5.6, "lighting and\nsmall power\nboards"),
               (7.3, "EV charger\nboard\n10 × 22 kW\ntype B RCDs"),
               (8.85, "forklift\ncharger\nboard"),
               (10.15, "cap")]
    yl = 3.0
    for x, name in feeders:
        ax.plot([x, x], [yb, 5.6], color=INK, lw=1.0)
        _cb(ax, x, 5.45)
        if name == "cap":
            ax.plot([x, x], [5.3, 4.45], color=INK, lw=1.0)
            # detuning reactor (coil) and capacitor
            th = np.linspace(0, 3 * np.pi, 60)
            ax.plot(x + 0.13 * np.sin(th), np.linspace(4.45, 3.75, 60), color=INK, lw=1.0)
            ax.plot([x, x], [3.75, 3.45], color=INK, lw=1.0)
            ax.plot([x - 0.28, x + 0.28], [3.45, 3.45], color=INK, lw=1.6)
            ax.plot([x - 0.28, x + 0.28], [3.3, 3.3], color=INK, lw=1.6)
            ax.text(x, 3.15, "125 kvar\ndetuned\nPFC bank", ha="center", va="top", fontsize=6.3)
        elif name == "PSB":
            ax.plot([x, x], [5.3, 1.75], color=INK, lw=1.0)
            ax.text(x + 0.18, 5.45, "400 A MCCB\n$I_r$ = 310 A", fontsize=6.2, va="center")
            ax.text(x + 0.15, 2.65, "120 m, 4c 185 mm²\nCu XLPE + 95 mm² PE", fontsize=6.2,
                    va="center")
            ax.plot([x - 0.75, x + 0.75], [1.75, 1.75], color=INK, lw=3)
            ax.text(x, 1.6, "packaging\nsub-board PSB", ha="center", va="top", fontsize=6.5)
            ax.text(x, 0.85, "$I''_k$ = 9.8 kA", fontsize=7, color=RED, ha="center", va="top",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=RED, lw=0.7))
        else:
            ax.plot([x, x], [5.3, 4.3], color=INK, lw=1.0)
            ax.text(x, 4.2, name, ha="center", va="top", fontsize=6.3,
                    bbox=dict(boxstyle="round,pad=0.25", fc="#EEF3F8", ec=INK, lw=0.8))
    # generator, ATS and ESB
    xg, xt = 12.9, 11.1
    ax.add_patch(Circle((xg, 9.3), 0.45, fc="#FFF4D6", ec=INK, lw=lw))
    ax.text(xg, 9.3, "G", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(xg, 9.95, "standby generator\n800 kVA, 400 V", ha="center", va="bottom", **t)
    ax.plot([xg, xg], [8.85, 7.3], color=INK, lw=lw)
    _cb(ax, xg, 7.15, s=0.34)
    ax.text(xg - 0.25, 7.15, "ACB\n1250 A", ha="right", va="center", fontsize=6.3)
    ax.plot([xg, xg, 12.3], [6.98, 4.0, 4.0], color=INK, lw=lw)
    ax.plot([xt, xt], [yb, 5.6], color=INK, lw=1.0)
    _cb(ax, xt, 5.45)
    ax.plot([xt, xt, 11.7], [5.3, 4.0, 4.0], color=INK, lw=1.0)
    ax.add_patch(Rectangle((11.4, 3.55), 1.2, 0.9, fc="#F7E6F0", ec=INK, lw=1.0, zorder=3))
    ax.text(12.0, 4.0, "ATS\n4-pole", ha="center", va="center", fontsize=6.5, zorder=4)
    ax.text(xt + 0.12, 4.75, "normal\nsupply", fontsize=6.2, ha="left", va="center")
    ax.text(xg + 0.12, 5.4, "standby", fontsize=6.2, ha="left", va="center")
    ax.plot([12.0, 12.0], [3.55, 2.6], color=INK, lw=lw)
    ax.plot([10.9, 13.6], [2.6, 2.6], color=INK, lw=3)
    ax.text(12.25, 2.45, "essential-services\nboard ESB\n(2 compressors, fans,\nlighting, IT, 75 kW pump)",
            ha="center", va="top", fontsize=6.3)
    # legend for symbols
    ax.text(5.6, 0.1, "□ circuit breaker    ━ busbar    MET main earthing terminal    "
            "ATS automatic transfer switch", fontsize=6.3, color=GREY, va="center")
    save(fig, "30", "fig-30-2-facility-single-line")


# ---------------------------------------------------------------- 30.3
def fig_generator_dip():
    Sst, Sst_soft, x = 597.0, 275.0, 0.20
    S = np.linspace(400, 1200, 300)
    dol = 100 * x * Sst / (S + x * Sst)
    soft = 100 * x * Sst_soft / (S + x * Sst_soft)
    fig, ax = new_fig(6.4, 4.0)
    ax.axvspan(780, 820, color=COLORS[2], alpha=0.18, lw=0)
    ax.text(800, 27.3, "selected\nset 800 kVA", ha="center", va="center", fontsize=8, color=COLORS[2])
    ax.plot(S, dol, color=COLORS[1], label="direct-on-line start, 597 kVA")
    ax.plot(S, soft, color=COLORS[0], ls="--", label="soft start, 3 × rated = 275 kVA")
    for s in (400, 600, 800, 1000):
        for curve, c in ((dol, COLORS[1]), (soft, COLORS[0])):
            v = np.interp(s, S, curve)
            ax.plot(s, v, "o", color=c, ms=4)
            ax.text(s + 12, v + 0.4, f"{v:.1f} %", fontsize=7.5, color=c, va="bottom")
    for y, lab in ((15, "typical limit 15 %"), (20, "typical limit 20 %")):
        ax.axhline(y, color=GREY, ls="--", lw=1.0)
        ax.text(1195, y + 0.3, lab, fontsize=7.5, color=GREY, ha="right", va="bottom")
    ax.set_xlim(400, 1200)
    ax.set_ylim(0, 30)
    ax.set_xlabel("Generator rating (kVA)")
    ax.set_ylabel("Estimated transient voltage dip (%)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.83), fontsize=8)
    top = ax.secondary_xaxis("top")
    top.set_xticks([400, 600, 800, 1000])
    top.set_xticklabels(["144 %", "96 %", "72 %", "58 %"], fontsize=8)
    top.set_xlabel("steady loading by the 576 kVA essential load", fontsize=8.5)
    save(fig, "30", "fig-30-3-generator-dip")


# ---------------------------------------------------------------- 30.4
def fig_voltage_profile():
    d = np.array([0, 120, 160])
    run = np.array([100, 97.74, 96.30])
    start = np.array([100, 96.56, 93.01])
    fig = plt.figure(figsize=(6.8, 3.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[3.1, 1], wspace=0.32)
    ax = fig.add_subplot(gs[0])
    ins = fig.add_subplot(gs[1])
    ax.axvspan(120, 160, color=GREY, alpha=0.10, lw=0)
    ax.text(60, 100.55, "feeder: 120 m, 185 mm² Cu XLPE", ha="center", fontsize=7.5)
    ax.text(140, 100.55, "motor circuit:\n40 m, 10 mm²", ha="center", fontsize=7.5, va="center")
    ax.plot(d, run, "-o", color=COLORS[0], ms=4.5, label="running (sub-board at 300 A)")
    ax.plot(d, start, "--o", color=COLORS[1], ms=4.5, label="22 kW motor starting (6.5 × $I_n$)")
    for x, y, c, dy, va in [(120, 97.74, COLORS[0], 0.25, "bottom"), (158, 96.30, COLORS[0], -0.3, "top"),
                            (118, 96.56, COLORS[1], -0.3, "top"), (158, 93.01, COLORS[1], -0.3, "top")]:
        ax.text(x - 2, y + dy, f"{y:.2f} %", fontsize=7.5, color=c, ha="right", va=va)
    ax.axhline(92, color=GREY, ls="--", lw=1.0)
    ax.text(2, 92.1, "8 % recommended limit (own transformer)", fontsize=7.5, color=GREY,
            va="bottom")
    ax.axhline(90, color=RED, ls="--", lw=1.0)
    ax.text(2, 90.1, "typical starting limit", fontsize=7.5, color=RED, va="bottom")
    ax.set_xlim(0, 160)
    ax.set_ylim(88, 101)
    ax.set_xticks([0, 40, 80, 120, 160])
    ax.set_xticklabels(["0\nMSB", "40", "80", "120\nPSB", "160\nmotor"])
    ax.set_xlabel("Cable distance from main switchboard (m)")
    ax.set_ylabel("Voltage (% of 400 V)")
    ax.legend(loc="lower left", fontsize=7.5, bbox_to_anchor=(0.0, -0.02))
    # side panel: transformer running drop offset by the tap
    vals = [100, 102.5, 100.1]
    ins.bar([0, 1, 2], vals, color=[GREY, COLORS[2], COLORS[0]], width=0.6, bottom=0)
    for k, v in enumerate(vals):
        ins.text(k, v + 0.08, f"{v:.1f}", ha="center", va="bottom", fontsize=7)
    ins.annotate("", xy=(2, 100.2), xytext=(2, 102.5),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.1, mutation_scale=9))
    ins.plot([1.3, 2.0], [102.5, 102.5], color=COLORS[1], lw=0.8, ls=":")
    ins.text(2.38, 101.35, "−2.4 %\nrunning\ndrop", fontsize=6.8, color=COLORS[1], ha="left",
             va="center")
    ins.set_xticks([0, 1, 2])
    ins.set_xticklabels(["MV\nnominal", "+2.5 %\ntap", "MSB,\nloaded"], fontsize=7)
    ins.set_ylim(98, 103.5)
    ins.set_xlim(-0.5, 2.5)
    ins.tick_params(axis="y", labelsize=7)
    ins.set_ylabel("LV voltage (%)", fontsize=8)
    ins.set_title("transformer", fontsize=8.5)
    save(fig, "30", "fig-30-4-voltage-profile")


# ---------------------------------------------------------------- 30.5
def _lt(I, Ir, t_at, I_at, pick):
    """Long-time I²t characteristic, infinite below pickup."""
    t = t_at * (I_at / I) ** 2
    return np.where(I > pick * Ir, t, np.nan)


def fig_time_current():
    I = np.logspace(2, 5, 2000)
    # ACB: Ir 1800 A, long-time ~100 s at 7.2 kA; Isd 7.2 kA ±10 %, 0.2-0.3 s, to 50 kA
    acb_lo = np.minimum(_lt(I, 1800, 80, 7200, 1.05), np.where(I >= 6480, 0.2, np.inf))
    acb_hi = np.minimum(_lt(I, 1800, 120, 7200, 1.2), np.where(I >= 7920, 0.3, np.inf))
    acb_lo[I > 50e3] = np.nan
    acb_hi[I > 50e3] = np.nan
    # MCCB: Ir 310 A, tr ~8 s at 6 Ir; Isd 1.86 kA ±10 %, 0.1-0.15 s; Ii 4 kA ±20 %, 0.01-0.02 s
    m_lo = np.minimum.reduce([_lt(I, 310, 6.4, 1860, 1.05), np.where(I >= 1674, 0.1, np.inf),
                              np.where(I >= 3200, 0.01, np.inf)])
    m_hi = np.minimum.reduce([_lt(I, 310, 9.6, 1860, 1.2), np.where(I >= 2046, 0.15, np.inf),
                              np.where(I >= 4800, 0.02, np.inf)])
    m_lo[I > 36e3] = np.nan
    m_hi[I > 36e3] = np.nan

    fig, ax = new_fig(6.6, 4.9)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.fill_between(I, acb_lo, acb_hi, color=COLORS[1], alpha=0.30, lw=0)
    ax.plot(I, acb_lo, color=COLORS[1], lw=1.2)
    ax.plot(I, acb_hi, color=COLORS[1], lw=1.2)
    ax.fill_between(I, m_lo, m_hi, color=COLORS[0], alpha=0.30, lw=0)
    ax.plot(I, m_lo, color=COLORS[0], lw=1.2)
    ax.plot(I, m_hi, color=COLORS[0], lw=1.2)
    # vertical ends of bands
    ax.plot([50e3, 50e3], [0.2, 0.3], color=COLORS[1], lw=1.2)
    ax.plot([36e3, 36e3], [0.01, 0.02], color=COLORS[0], lw=1.2)
    ax.axvspan(3200, 4800, ymin=0, ymax=0.08, color=COLORS[0], alpha=0.15, lw=0)
    ax.text(3920, 0.0125, "$I_i$ 4 kA\n±20 %", fontsize=6.5, ha="center", va="bottom",
            color=COLORS[0])
    # selective gap
    sel = (I > 1890) & (I < 29.1e3)
    ax.fill_between(I[sel], m_hi[sel], acb_lo[sel], color=COLORS[2], alpha=0.18, lw=0)
    ax.text(15000, 0.6, "selective", fontsize=8.5, color=COLORS[2], ha="center", fontweight="bold")
    # cable damage curve
    k2s2 = (143 * 185) ** 2
    Ic = np.logspace(np.log10(1.2e3), 5, 200)
    ax.plot(Ic, k2s2 / Ic ** 2, color=INK, ls="--", lw=1.2)
    ax.text(1.1e3, 520, "185 mm² cable damage\n$I^2t = 143^2 \\times 185^2$ A²s", fontsize=7,
            va="center", ha="right")
    # fault markers
    for If, lab, c in [(4.3e3, "4.3 kA, E/F at PSB", COLORS[3]),
                       (9.8e3, "9.8 kA, 3-ph at PSB", COLORS[3]),
                       (14.6e3, "14.6 kA, arc at MSB", RED),
                       (29.1e3, "29.1 kA, bolted MSB", RED)]:
        ax.axvline(If, color=c, lw=0.9, ls=":")
        ax.text(If * 1.04, 9000, lab, fontsize=6.5, color=c, rotation=90, va="top", ha="left")
    ax.text(115, 8500, "incomer ACB\n$I_r$ 1800 A, $I_{sd}$ 7.2 kA, 0.2 s", fontsize=7.5,
            color=COLORS[1], ha="left", va="top")
    ax.text(215, 2.0, "packaging MCCB\n$I_r$ 310 A, $I_{sd}$ 1.86 kA, 0.1 s,\n$I_i$ 4 kA",
            fontsize=7.5, color=COLORS[0], ha="left")
    ax.set_xlim(100, 1e5)
    ax.set_ylim(0.01, 1e4)
    ax.set_xticks([100, 1e3, 1e4, 1e5])
    ax.set_xticklabels(["100 A", "1 kA", "10 kA", "100 kA"])
    ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000, 1e4])
    ax.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1000", "10 000"])
    ax.grid(True, which="major", color=GRID, lw=0.6)
    ax.grid(True, which="minor", color=GRID, lw=0.3, alpha=0.6)
    ax.set_xlabel("Current at 400 V (A)")
    ax.set_ylabel("Time (s)")
    save(fig, "30", "fig-30-5-time-current-coordination")


# ---------------------------------------------------------------- 30.6
def fig_earth_electrode():
    rho, L, dd = 100.0, 3.0, 0.016
    R1 = rho / (2 * np.pi * L) * (np.log(8 * L / dd) - 1)
    n = np.array([1, 2, 4, 8, 12, 16, 24])
    F = np.array([1.0, 1.16, 1.36, 1.68, 1.80, 1.92, 2.16])
    Rn = F * R1 / n
    fig, ax = new_fig(6.4, 4.0)
    ax.set_yscale("log")
    ax.plot(n, R1 / n, ":", color=GREY, lw=1.3, label="ideal $R_{rod}/n$ (no interference)")
    ax.plot(n, Rn, "-o", color=COLORS[0], ms=5, label="3 m rods, spacing = rod length")
    for ni, r in zip(n, Rn):
        ax.text(ni + 0.35, r * 1.07, f"{r:.1f} Ω", fontsize=7.5, color=COLORS[0], va="bottom")
    ax.axhline(2.39, color=RED, ls="--", lw=1.2)
    ax.text(24.5, 2.5, "required: 2.39 Ω (430 V EPR at 180 A)", fontsize=8, color=RED,
            ha="right", va="bottom")
    ax.axhline(1.15, color=COLORS[2], lw=2.0)
    ax.text(24.5, 1.08, "60 m × 40 m foundation electrode: 1.15 Ω", fontsize=8, color=COLORS[2],
            ha="right", va="top")
    ax.annotate("curve flattens: overlapping\npotential zones (mutual\ninterference)",
                xy=(16, Rn[5]), xytext=(13.5, 13), fontsize=8, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
    ax.set_xlim(0, 25)
    ax.set_ylim(0.5, 40)
    ax.set_xticks([1, 2, 4, 8, 12, 16, 20, 24])
    ax.set_yticks([0.5, 1, 2, 5, 10, 20, 40])
    ax.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "40"])
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="major", axis="y", color=GRID, lw=0.6)
    ax.set_xlabel("Number of 3 m rods in parallel (100 Ω·m soil)")
    ax.set_ylabel("Earth resistance (Ω)")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "30", "fig-30-6-earth-electrode-resistance")


if __name__ == "__main__":
    fig_design_flow()
    fig_facility_single_line()
    fig_generator_dip()
    fig_voltage_profile()
    fig_time_current()
    fig_earth_electrode()
