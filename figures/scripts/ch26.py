"""Figures for Chapter 26 — Smart Grids.

Run from the repository root:  python figures/scripts/ch26.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from matplotlib.lines import Line2D

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

CH = "26"


def line(ax, xs, ys, color=INK, lw=1.3, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def zone(ax, x, y, w, h, title, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.25",
                                fc=fc, ec="#999999", lw=0.8, zorder=0))
    ax.text(x + w / 2, y + h - 0.25, title, ha="center", va="top", fontsize=8,
            fontweight="bold", color="#333333")


# ----------------------------------------------------------------------------
# Figure 26.1
# ----------------------------------------------------------------------------
def fig_26_1():
    """Architecture of an advanced metering infrastructure."""
    fig, ax = schematic(6.8, 4.6, xlim=(0, 17), ylim=(-0.3, 11.2))
    fs = 7.2
    zone(ax, 0.0, 2.75, 4.2, 8.4, "Home area\nnetwork", "#F4F8EE")
    zone(ax, 4.35, 2.75, 4.65, 8.4, "Neighbourhood\narea network", "#EEF3F8")
    zone(ax, 9.15, 2.75, 2.2, 8.4, "Wide-area\nbackhaul", "#F8F2EA")
    zone(ax, 11.5, 2.75, 5.5, 8.4, "Utility data\ncentre", "#F3EEF6")

    # home area
    ym = 5.9
    for i, t in enumerate(["in-home\ndisplay", "smart\nthermostat", "EV\ncharger"]):
        y = 7.7 - i * 1.75
        box(ax, 0.15, y, 1.75, 1.2, t, fc="white", fontsize=6.6)
        arrow(ax, 1.9, y + 0.6, 2.5, ym + 0.3 * (1 - i), both=True, color="#4c8a2a")
    box(ax, 2.5, ym - 0.9, 1.5, 1.8, "smart\nmeter", fc="#DCEFD0", fontsize=7.8)
    ax.text(2.1, 3.65, "HAN: Zigbee\nor Wi-SUN", fontsize=fs, ha="center", va="center",
            color="#3a6e1f")

    # neighbourhood network: RF mesh of meters
    pts = np.array([[4.9, 7.7], [5.6, 6.9], [5.0, 5.9], [5.9, 5.3], [5.1, 4.6], [6.5, 7.6],
                    [6.7, 6.2], [6.4, 4.3]])
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            if np.hypot(*(pts[a] - pts[b])) < 1.5:
                line(ax, pts[[a, b], 0], pts[[a, b], 1], color="#7fa7c9", lw=0.7)
    for p in pts:
        ax.add_patch(Circle(p, 0.2, fc="white", ec=COLORS[0], lw=1.0, zorder=3))
    line(ax, [4.0, 5.0], [ym, 5.9], color="#7fa7c9", lw=0.7)
    box(ax, 7.3, 5.0, 1.55, 1.9, "data\nconcen-\ntrator", fc="#D5E4F2", fontsize=fs)
    for p in (pts[5], pts[6], pts[7]):
        line(ax, [p[0], 7.3], [p[1], 5.95], color="#7fa7c9", lw=0.7)
    ax.text(6.65, 3.85, "≈ 2000 meters per\nconcentrator, at the\ndistribution substation",
            fontsize=6.8, ha="center", va="top")
    ax.text(6.65, 9.75, "RF mesh 50–300 kbit/s, or\nnarrowband PLC (G3-PLC,\nPRIME), 35–90 kHz,\n"
            "CENELEC A band", fontsize=6.6, ha="center", va="top", color="#1f4e79")

    # backhaul
    arrow(ax, 8.85, 5.95, 11.75, 5.95, both=True, color="#9a5a12")
    ax.text(10.25, 6.3, "cellular\nLTE or\nfibre", fontsize=fs, ha="center", va="bottom",
            color="#9a5a12")

    # utility data centre
    box(ax, 11.7, 5.1, 1.55, 1.7, "head-end\nsystem", fc="white", fontsize=6.8)
    arrow(ax, 13.25, 5.95, 13.85, 5.95, both=True)
    box(ax, 13.85, 4.85, 1.3, 2.2, "MDMS\n(VEE)", fc="#E5DAEE", fontsize=fs)
    outs = ["billing", "OMS", "GIS", "ADMS", "analytics"]
    for i, t in enumerate(outs):
        y = 8.85 - i * 1.15
        box(ax, 15.45, y - 0.42, 1.45, 0.8, t, fc="white", fontsize=6.8)
        line(ax, [15.15, 15.45], [5.95, y - 0.02], lw=0.8)
    ax.text(13.45, 4.3, "VEE: validation,\nestimation and editing", fontsize=6.6, ha="center",
            va="top")

    # two-way traffic
    ax.annotate("", xy=(16.8, 2.2), xytext=(0.3, 2.2),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=12))
    ax.text(8.5, 2.3, "reads up: interval data, events, last-gasp alarms",
            fontsize=7.5, ha="center", va="bottom", color=COLORS[0])
    ax.annotate("", xy=(0.3, 1.45), xytext=(16.8, 1.45),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.6, mutation_scale=12))
    ax.text(8.5, 1.35, "commands down: remote disconnect, tariff update, firmware",
            fontsize=7.5, ha="center", va="top", color=COLORS[1])
    ax.text(8.5, -0.2, "96 records/meter/day × 100 B ≈ 9.6 kB per meter per day;  "
            "1.2 million meters → 11.5 GB/day",
            fontsize=7.3, ha="center", va="bottom")
    save(fig, CH, "fig-26-1-ami-architecture")


# ----------------------------------------------------------------------------
# Figure 26.2
# ----------------------------------------------------------------------------
def breaker(ax, x, y, s=0.26, fc="white", ec=INK):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=ec, lw=1.2, zorder=4))


def xfmr(ax, x, yc, r=0.27):
    """Two-winding transformer centred at (x, yc), vertical; returns (ylow, yhigh)."""
    ax.add_patch(Circle((x, yc - 0.19), r, fill=False, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(Circle((x, yc + 0.19), r, fill=False, ec=INK, lw=1.2, zorder=3))
    return yc - 0.19 - r, yc + 0.19 + r


def fig_26_2():
    """Islanded mine microgrid single-line diagram."""
    fig, ax = schematic(6.8, 5.0, xlim=(0, 16.2), ylim=(-0.7, 11.1))
    COMM = COLORS[3]
    x0, x1, y0, y1 = 3.0, 12.6, 3.4, 7.2
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                fill=False, ec=INK, lw=3.2))
    ax.text((x0 + x1) / 2, 4.15, "11 kV ring bus", ha="center", va="center",
            fontsize=10, fontweight="bold", color="#666666")
    ycomm = 10.85

    # gensets (top)
    for x, name in ((4.7, "G1"), (7.9, "G2")):
        line(ax, [x, x], [y1, 9.1])
        breaker(ax, x, 7.6)
        lo, hi = xfmr(ax, x, 8.3)
        ax.add_patch(Circle((x, 9.5), 0.4, fc="white", ec=INK, lw=1.2, zorder=3))
        ax.text(x, 9.5, "G", ha="center", va="center", fontsize=9)
        ax.text(x, 6.95, f"{name}: 2 MW diesel\n0.4/11 kV step-up\n4 % droop", fontsize=7,
                va="top", ha="center")
        line(ax, [x, x], [9.9, ycomm], COMM, lw=0.9, ls="--")
    # battery (top)
    xb = 11.0
    line(ax, [xb, xb], [y1, 9.0])
    breaker(ax, xb, 7.6)
    xfmr(ax, xb, 8.3)
    box(ax, xb - 0.55, 9.0, 1.1, 0.6, "DC/AC", fc="white", fontsize=6.8)
    line(ax, [xb, xb], [9.6, 9.8])
    for k in range(3):
        yy = 9.85 + 0.17 * k
        line(ax, [xb - 0.3, xb + 0.3], [yy, yy], lw=1.6)
        line(ax, [xb - 0.15, xb + 0.15], [yy + 0.08, yy + 0.08], lw=1.0)
    ax.text(xb - 0.1, 6.95, "BESS 3 MW / 3 MWh\ngrid-forming\n2 % droop", fontsize=7,
            va="top", ha="center")
    line(ax, [xb, xb], [10.35, ycomm], COMM, lw=0.9, ls="--")

    # PV (bottom)
    xp = 11.4
    line(ax, [xp, xp], [y0, 1.1])
    breaker(ax, xp, 3.0)
    xfmr(ax, xp, 2.3)
    box(ax, xp - 0.55, 0.6, 1.1, 0.55, "DC/AC", fc="white", fontsize=6.8)
    ax.add_patch(Polygon([[xp - 0.5, -0.35], [xp + 0.5, -0.35], [xp + 0.3, 0.3], [xp - 0.7, 0.3]],
                         closed=True, fc="#FFE9A8", ec=INK, lw=1.0))
    line(ax, [xp, xp], [0.3, 0.6])
    ax.text(xp + 0.6, 1.4, "PV 6 MW\ngrid-following\ninverters", fontsize=7.5, va="center")
    # loads (bottom)
    for x, t in ((4.6, "crusher and\nconveyors\n2.5 MW"), (6.9, "ventilation\n1.5 MW"),
                 (9.1, "camp\n0.8 MW")):
        line(ax, [x, x], [y0, 2.2])
        breaker(ax, x, 3.0)
        ax.annotate("", xy=(x, 1.7), xytext=(x, 2.25),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=12))
        ax.text(x, 1.55, t, fontsize=7.5, ha="center", va="top")

    # PCC and utility
    yp = 5.3
    line(ax, [1.2, x0], [yp, yp])
    breaker(ax, 2.2, yp)
    line(ax, [0.05, 1.2], [yp, yp], ls="--", lw=1.3)
    ax.text(2.2, yp + 0.3, "PCC", fontsize=7.5, ha="center", va="bottom", fontweight="bold")
    ax.text(0.05, yp - 0.3, "33 kV utility\nline (absent\nwhen off-grid)", fontsize=7, va="top")
    line(ax, [1.55, 1.55], [ycomm, yp + 0.0], COMM, lw=0.9, ls="--")
    line(ax, [1.55, 2.07], [yp + 0.0, yp + 0.0], COMM, lw=0.0)

    # controller
    box(ax, 13.05, 3.6, 3.1, 3.3, "", fc="#F3EAF2", ec=COMM)
    ax.text(14.6, 6.65, "Microgrid\ncontroller", ha="center", va="top", fontsize=8,
            fontweight="bold")
    ax.text(14.6, 5.55, "primary:\nlocal droop\nsecondary: frequency\nrestoration\n"
            "tertiary: dispatch", fontsize=6.4, va="top", ha="center", linespacing=1.2)
    line(ax, [1.55, 14.6], [ycomm, ycomm], COMM, lw=0.9, ls="--")
    line(ax, [14.6, 14.6], [ycomm, 6.9], COMM, lw=0.9, ls="--")
    line(ax, [xp, xp], [-0.35, -0.6], COMM, lw=0.9, ls="--")
    line(ax, [xp, 14.6], [-0.6, -0.6], COMM, lw=0.9, ls="--")
    line(ax, [14.6, 14.6], [-0.6, 3.6], COMM, lw=0.9, ls="--")
    ax.text(8.0, ycomm + 0.08, "communication links (dashed)", fontsize=7, color=COMM,
            ha="center", va="bottom")
    save(fig, CH, "fig-26-2-mine-microgrid")


# ----------------------------------------------------------------------------
# Figure 26.3
# ----------------------------------------------------------------------------
def fig_26_3():
    """Frequency-power droop of two gensets and a battery sharing 2.5 MW."""
    f0 = 50.0
    Kg = 2.0 / 0.04 / f0      # MW per Hz for each genset: 1 MW/Hz
    Kb = 3.0 / 0.02 / f0      # 3 MW/Hz for the battery
    P = np.linspace(0, 3, 300)
    fig, ax = new_fig(6.4, 4.0)
    ax.plot(P, f0 - P / Kg, color=COLORS[1], lw=2, label="genset G1 or G2: 4 % on 2 MW (1 Hz/MW)")
    ax.plot(P, f0 - P / Kb, color=COLORS[0], lw=2, label="battery: 2 % on 3 MW (0.333 Hz/MW)")
    df = 2.5 / (2 * Kg + Kb)
    fss = f0 - df
    ax.plot(P, f0 + df - P / Kg, "--", color=COLORS[1], lw=1.4,
            label="after secondary control (setpoints raised 0.5 Hz)")
    ax.plot(P, f0 + df - P / Kb, "--", color=COLORS[0], lw=1.4)
    ax.axhline(fss, color="#666666", lw=1.0, ls="--")
    ax.axhline(f0, color="#999999", lw=0.6)
    pg, pb = Kg * df, Kb * df
    for p, c in ((pg, COLORS[1]), (pb, COLORS[0])):
        ax.plot([p], [fss], "o", color=c, ms=6, zorder=5)
        ax.plot([p], [f0], "s", color=c, ms=5, zorder=5, mfc="white")
        ax.plot([p, p], [48.5, fss], ":", color=c, lw=1)
    ax.text(pg + 0.04, 48.62, f"{pg:.1f} MW\neach genset", fontsize=8, color=COLORS[1])
    ax.text(pb + 0.04, 49.15, f"{pb:.1f} MW\nbattery", fontsize=8, color=COLORS[0])
    ax.text(2.95, 48.6, f"after primary control: {fss:.1f} Hz\n0.5 + 0.5 + 1.5 = 2.5 MW",
            fontsize=8.5, ha="right", va="bottom", linespacing=1.4)
    ax.text(0.9, f0 + 0.04, "same outputs restored to 50 Hz", fontsize=8, ha="left",
            va="bottom", color="#444444")
    ax.set_xlim(0, 3)
    ax.set_ylim(48.5, 50.5)
    ax.set_xlabel("Change in output power (MW)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend(loc="upper right", fontsize=7.8, bbox_to_anchor=(1.0, 1.02))
    save(fig, CH, "fig-26-3-droop-sharing")


# ----------------------------------------------------------------------------
# Figure 26.4
# ----------------------------------------------------------------------------
def fig_26_4():
    """FLISR sequence on two 11 kV feeders with a normally open tie."""
    C1, C2, DEAD = COLORS[0], COLORS[2], "#AAAAAA"
    xs = [0.9, 3.7, 6.5, 9.3, 12.1]     # CB1, S1, S2, S3, far end
    yf1, yf2 = 1.4, 0.0
    states = [
        dict(title="(a)  t < 0 s: normal state; tie T open",
             cb1=True, sw=[True, True, True], T=False, sec=[C1, C1, C1, C1], fault=False,
             fpi=[], off="0 customers off"),
        dict(title="(b)  t = 5 s: permanent fault between S1 and S2; CB1 locked out after reclose",
             cb1=False, sw=[True, True, True], T=False, sec=[DEAD] * 4, fault=True,
             fpi=[0, 1], off="3000 customers off"),
        dict(title="(c)  t = 40 s: S1 and S2 opened, CB1 reclosed; section 1 restored",
             cb1=True, sw=[False, False, True], T=False, sec=[C1, DEAD, DEAD, DEAD], fault=True,
             fpi=[0, 1], off="2250 customers off"),
        dict(title="(d)  t = 60 s: tie T closed; sections 3 and 4 fed from feeder 2",
             cb1=True, sw=[False, False, True], T=True, sec=[C1, DEAD, C2, C2], fault=True,
             fpi=[0, 1], off="750 customers off (section 2)"),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(6.8, 6.4))
    for ax, st in zip(axes, states):
        ax.set_xlim(0, 15.2)
        ax.set_ylim(-0.75, 2.35)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(0.0, 2.3, st["title"], fontsize=8.3, va="top", fontweight="bold")
        # feeder 1 sections
        for k in range(4):
            c = st["sec"][k]
            ax.plot([xs[k], xs[k + 1]], [yf1, yf1], color=c, lw=3.0 if c != DEAD else 2.0,
                    ls="-" if c != DEAD else (0, (3, 2)), solid_capstyle="butt", zorder=1)
            ax.text((xs[k] + xs[k + 1]) / 2, yf1 + 0.18, f"sec {k + 1}: 750", fontsize=7,
                    ha="center", va="bottom", color="#333333")
        # feeder 2
        ax.plot([xs[0], xs[-1]], [yf2, yf2], color=C2, lw=3.0, solid_capstyle="butt", zorder=1)
        ax.text((xs[0] + xs[-1]) / 2, yf2 - 0.18, "feeder 2 (own load not shown)", fontsize=7,
                ha="center", va="top", color="#2c6e4f")
        # tie connection
        tcol = C2 if st["T"] else DEAD
        ax.plot([xs[-1], xs[-1]], [yf1, yf2], color=tcol, lw=2.0 if st["T"] else 1.4,
                ls="-" if st["T"] else (0, (3, 2)), zorder=1)
        # breakers and switches
        def sw(x, y, closed, label, lab_dy=0.25, fs=7.5):
            s = 0.34
            ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=INK if closed else "white",
                                   ec=INK, lw=1.3, zorder=5))
            ax.text(x, y + lab_dy, label, fontsize=fs, ha="center",
                    va="bottom" if lab_dy > 0 else "top", fontweight="bold")
        sw(xs[0], yf1, st["cb1"], "", lab_dy=0.25)
        ax.text(xs[0] - 0.3, yf1, "CB1", fontsize=7.5, ha="right", va="center", fontweight="bold")
        sw(xs[0], yf2, True, "")
        ax.text(xs[0] - 0.3, yf2, "CB2", fontsize=7.5, ha="right", va="center", fontweight="bold")
        for k in range(3):
            sw(xs[k + 1], yf1, st["sw"][k], "", lab_dy=-0.25)
            ax.text(xs[k + 1], yf1 - 0.25, f"S{k + 1}", fontsize=7.5, ha="center", va="top",
                    fontweight="bold")
        sw(xs[-1], (yf1 + yf2) / 2, st["T"], "")
        ax.text(xs[-1] + 0.3, (yf1 + yf2) / 2, "T (NO)", fontsize=7.5, ha="left", va="center",
                fontweight="bold")
        # fault
        if st["fault"]:
            xf = (xs[1] + xs[2]) / 2 + 0.4
            ax.plot([xf - 0.15, xf + 0.1, xf - 0.05, xf + 0.2], [yf1 + 0.05, yf1 - 0.25,
                    yf1 - 0.3, yf1 - 0.6], color="#C00000", lw=1.8, zorder=6)
            ax.text(xf - 0.3, yf1 - 0.45, "fault", fontsize=7, color="#C00000", va="center", ha="right")
        # FPIs
        for k in st["fpi"]:
            x = xs[k] + 0.35
            ax.plot([x], [yf1 + 0.45], marker="v", ms=7, color=COLORS[4], mec=INK, mew=0.6,
                    zorder=6)
        ax.text(15.2, 2.3, st["off"], fontsize=8, ha="right", va="top",
                color="#C00000" if "0 customers" != st["off"][:11] else "#2c6e4f")
    handles = [Line2D([], [], color=C1, lw=3, label="energised from feeder 1"),
               Line2D([], [], color=C2, lw=3, label="energised from feeder 2"),
               Line2D([], [], color=DEAD, lw=2, ls=(0, (3, 2)), label="de-energised"),
               Line2D([], [], marker="s", ls="", color=INK, ms=7, label="closed"),
               Line2D([], [], marker="s", ls="", mfc="white", mec=INK, ms=7, label="open"),
               Line2D([], [], marker="v", ls="", color=COLORS[4], mec=INK, ms=7,
                      label="fault passage indicator lit")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=7.8, frameon=False,
               bbox_to_anchor=(0.5, -0.01))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.08, hspace=0.12)
    save(fig, CH, "fig-26-4-flisr-sequence")


# ----------------------------------------------------------------------------
# Figure 26.5
# ----------------------------------------------------------------------------
def fig_26_5():
    """Resilience trapezoid, base case and improved case."""
    t = np.linspace(0, 120, 2401)
    base = np.interp(t, [0, 10, 16, 40, 110, 120], [100, 100, 35, 35, 100, 100])
    imp = np.interp(t, [0, 10, 16, 24, 60, 120], [100, 100, 70, 70, 100, 100])
    fig, ax = new_fig(6.6, 4.0)
    ax.fill_between(t, base, 100, color=COLORS[1], alpha=0.10, lw=0)
    ax.fill_between(t, base, imp, where=imp > base, color=COLORS[2], alpha=0.25, lw=0)
    ax.plot(t, base, color=COLORS[1], lw=2.2, label="base case")
    ax.plot(t, imp, "--", color=COLORS[0], lw=2.2, label="with resilience measures")
    ax.text(47, 57, "avoided loss\nof load", fontsize=9.5, ha="center", va="center",
            color="#1d6b50", fontweight="bold")
    ax.text(30, 94, "loss remaining\nwith measures", fontsize=7.5, ha="center", va="center",
            color=COLORS[1])
    # phases of the base case
    for a in (10, 16, 40, 110):
        ax.axvline(a, color="#BBBBBB", lw=0.6, ymax=100 / 125)
    for x, y, name in ((13, 113, "disruption"), (28, 104, "degraded state"),
                       (75, 104, "restoration"), (115, 104, "post-\nrestoration")):
        ax.text(x, y, name, fontsize=7.8, ha="center", va="bottom", color="#333333")
    ax.annotate("hardening:\nsmaller drop", xy=(15, 72), xytext=(0.8, 55), fontsize=7.8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.7))
    ax.annotate("microgrids hold\ncritical loads", xy=(20, 69), xytext=(18, 14), fontsize=7.8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.7))
    ax.annotate("faster restoration\n(24 → 60 h)", xy=(46, 88), xytext=(60, 26), fontsize=7.8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.7))
    ax.text(9.0, 2, "event\nt = 10 h", fontsize=7.5, ha="right", va="bottom")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 125)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_xticks(np.arange(0, 121, 20))
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Load served (%)")
    ax.legend(loc="lower right", fontsize=8.5)
    save(fig, CH, "fig-26-5-resilience-trapezoid")


if __name__ == "__main__":
    fig_26_1()
    fig_26_2()
    fig_26_3()
    fig_26_4()
    fig_26_5()
