"""Figures for Chapter 29 — Electrical Safety.

Run from the repository root:  python figures/scripts/ch29.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch, Arc
from matplotlib.lines import Line2D
from scipy.interpolate import PchipInterpolator
import schemdraw
import schemdraw.elements as elm

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID

schemdraw.use("matplotlib")
GREY = "#8A8A8A"
RED, ORANGE, PURPLE, GREEN, BLUE = "#C0392B", COLORS[4], "#7B3FA0", COLORS[2], COLORS[0]


# ---------------------------------------------------------------- 29.1
def _loglog_curve(I_pts, t_pts, t):
    """Smooth curve I(t) through points, interpolated in log-log space."""
    f = PchipInterpolator(np.log10(t_pts), np.log10(I_pts))
    return 10 ** f(np.log10(t))


def fig_iec60479_zones():
    """Time-current zones for 50/60 Hz AC, left hand to feet (after IEC 60479-1)."""
    t = np.logspace(1, 4, 400)                          # ms
    # curve b: 200 mA at 10 ms, 10 mA at 2000 ms, vertical at 10 mA beyond
    b = np.where(t <= 2000, 200 * (t / 10) ** (np.log(10 / 200) / np.log(200)), 10)
    tk = np.array([10, 200, 500, 1000, 3000, 10000])
    c1 = _loglog_curve([500, 400, 120, 50, 43, 40], tk, t)
    c2 = _loglog_curve([800, 600, 190, 80, 66, 60], tk, t)      # ~5 % fibrillation
    c3 = _loglog_curve([1500, 1100, 350, 150, 110, 100], tk, t)  # ~50 % fibrillation

    fig, ax = new_fig(6.4, 4.4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.fill_betweenx(t, b, c1, color=COLORS[4], alpha=0.12, lw=0)
    ax.fill_betweenx(t, c1, 1e4, color=RED, alpha=0.10, lw=0)
    ax.axvline(0.5, color=INK, lw=1.4)
    ax.plot(b, t, color=INK, lw=1.4)
    ax.plot(c1, t, color=RED, lw=1.6)
    ax.plot(c2, t, color=RED, lw=1.0, ls="--")
    ax.plot(c3, t, color=RED, lw=1.0, ls=":")
    for x, y, s, c in [(0.5, 7000, "a", INK), (11, 7000, "b", INK), (34, 7000, "c1", RED),
                       (62, 7000, "c2", RED), (102, 7000, "c3", RED)]:
        ax.text(x * 1.08, y, s, fontsize=8.5, color=c, ha="left", va="center", style="italic")
    ax.text(0.2, 300, "AC-1\nperception\npossible", fontsize=8, ha="center")
    ax.text(2.2, 300, "AC-2\nno harmful\neffects", fontsize=8, ha="center")
    ax.text(150, 150, "AC-3", fontsize=9, ha="center", fontweight="bold")
    ax.text(2500, 1000, "AC-4", fontsize=9, ha="center", fontweight="bold", color=RED)
    for x, s in [(640, "AC-4.1"), (1120, "AC-4.2"), (2600, "AC-4.3")]:
        ax.text(x, 14, s, fontsize=7, rotation=90, ha="center", va="bottom", color=RED)
    ax.text(5500, 600, "fibrillation\nprobability\nc1–c2: < 5 %\nc2–c3: < 50 %\n> c3: > 50 %",
            fontsize=7, ha="center", va="top", color=RED)
    # RCD line and overlay points
    ax.axhline(40, color=BLUE, ls="--", lw=1.1)
    ax.text(0.12, 43, "RCD at 5 × rated residual current: trips within 40 ms", fontsize=7.5,
            color=BLUE, va="bottom")
    ax.plot(230, 25, "o", color=GREEN, ms=7, mec="white", zorder=5)
    ax.annotate("230 mA, 25 ms\nRCD trips: safe", xy=(230, 25), xytext=(20, 17), fontsize=7.5,
                color=GREEN, ha="right", va="center",
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.9))
    ax.plot(230, 1000, "X", color=RED, ms=8, mec="white", zorder=5)
    ax.annotate("230 mA, 1 s\nno RCD: AC-4", xy=(230, 1000), xytext=(600, 2600), fontsize=7.5,
                color=RED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9))
    ax.set_xlim(0.1, 10000)
    ax.set_ylim(10, 10000)
    ax.set_xticks([0.1, 1, 10, 100, 1000, 10000])
    ax.set_xticklabels(["0.1", "1", "10", "100", "1000", "10 000"])
    ax.set_yticks([10, 100, 1000, 10000])
    ax.set_yticklabels(["10", "100", "1000", "10 000"])
    ax.grid(True, which="major", color=GRID, lw=0.6)
    ax.set_xlabel("Body current, left hand to feet (mA r.m.s.)")
    ax.set_ylabel("Duration of current flow (ms)")
    save(fig, "29", "fig-29-1-iec60479-zones")


# ---------------------------------------------------------------- 29.2
def fig_incident_energy():
    """Lee-method incident energy at 455 mm against arcing time, with PPE thresholds."""
    V, Ibf, D = 0.4, 34.8, 455.0
    K = 2.142e6 * V * Ibf / D ** 2 / 4.184           # cal/cm² per second
    t = np.linspace(0, 1.0, 100)
    E = K * t
    fig, ax = new_fig(6.4, 4.0)
    ax.plot(t, E, color=BLUE, lw=2.0, label="Lee method, 34.8 kA, 400 V, D = 455 mm")
    levels = [(1.2, "burn threshold 1.2", GREY), (4, "PPE cat 1 (4)", COLORS[2]),
              (8, "cat 2 (8)", COLORS[4]), (25, "cat 3 (25)", COLORS[1]), (40, "cat 4 (40)", RED)]
    for y, s, c in levels:
        ax.axhline(y, color=c, ls="--", lw=1.0)
        ax.text(1.0, y + 0.3, s, color=c, fontsize=7.5, ha="right", va="bottom")
    pts = [(0.05, "arc-flash relay", (0.02, 13.5)), (0.2, "reduced short-time delay", (0.30, 5.9)),
           (0.5, "original setting", (0.58, 12.5))]
    for tt, lab, xy in pts:
        e = K * tt
        ax.plot(tt, e, "o", color=BLUE, ms=6, zorder=5)
        ax.annotate(f"{lab}\n{tt:g} s: {e:.1f} cal/cm²", xy=(tt, e), xytext=xy, fontsize=7.5,
                    va="center", arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 42)
    ax.set_xlabel("Arcing time (s)")
    ax.set_ylabel("Incident energy (cal/cm²)")
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 1.02))
    # inset: arc-flash boundary
    ins = ax.inset_axes([0.10, 0.50, 0.30, 0.30])
    ins.set_facecolor("white")
    db = np.sqrt(2.142e6 * V * Ibf * t / 5.0) / 1000
    ins.plot(t, db, color=PURPLE, lw=1.4)
    for tt in (0.05, 0.2, 0.5):
        d = np.sqrt(2.142e6 * V * Ibf * tt / 5.0) / 1000
        ins.plot(tt, d, "o", color=PURPLE, ms=4)
        ins.text(tt + 0.03, d - 0.05, f"{d:.2f} m", fontsize=6.5, va="top", color=PURPLE)
    ins.set_xlim(0, 1.0)
    ins.set_ylim(0, 2.6)
    ins.tick_params(labelsize=6.5)
    ins.set_xlabel("arcing time (s)", fontsize=6.5, labelpad=1)
    ins.set_title("arc-flash boundary (m)", fontsize=7)
    save(fig, "29", "fig-29-2-incident-energy-time")


# ---------------------------------------------------------------- 29.3
def _earth(ax, x, y, s=0.22, lw=1.2, color=INK):
    """Earth symbol hanging below (x, y)."""
    ax.plot([x, x], [y, y - 0.25], color=color, lw=lw)
    for i, w in enumerate([1.0, 0.65, 0.3]):
        yy = y - 0.25 - i * 0.11
        ax.plot([x - s * w, x + s * w], [yy, yy], color=color, lw=lw)


def _panel(ax, kind, title):
    ax.set_xlim(0, 10)
    ax.set_ylim(0.4, 6.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.1, 6.25, title, fontsize=9, fontweight="bold", va="top")
    yL = {"L1": 5.2, "L2": 4.85, "L3": 4.5, "N": 4.15, "PE": 3.75}
    # star-connected secondary
    cx, cy = 1.05, 4.55
    for name, ang in [("L1", 60), ("L2", 0), ("L3", -60)]:
        a = np.radians(ang)
        ex, ey = cx + 0.45 * np.cos(a), cy + 0.45 * np.sin(a)
        ax.plot([cx, ex], [cy, ey], color=INK, lw=1.4)
        ax.plot([ex, 1.9, 1.9], [ey, ey, yL[name]], color=INK, lw=1.0)
    ax.plot(cx, cy, "o", color=INK, ms=3)
    ax.plot([cx, cx, 1.9], [cy, yL["N"] - 0.0, yL["N"]], color=INK, lw=1.0)
    ax.add_patch(Circle((cx, cy), 0.62, fill=False, ec=GREY, lw=0.8, ls=":"))
    ax.text(cx, cy + 0.75, "source", fontsize=7, ha="center", color=GREY)
    xs, xe = 1.9, 8.0
    split = 5.4                                       # service position for TN-C-S
    for name in ("L1", "L2", "L3"):
        ax.plot([xs, xe], [yL[name]] * 2, color=INK, lw=1.0)
        ax.text(xe + 0.08, yL[name], name, fontsize=7, va="center")
    # installation boundary
    ax.add_patch(Rectangle((5.0, 1.15), 4.85, 4.45, fill=False, ec=GREY, ls="--", lw=0.8))
    ax.text(5.1, 5.57, "installation", fontsize=6.5, color=GREY, ha="left", va="top")
    # enclosure (exposed conductive part) with load
    ex0, ey0, ew, eh = 6.35, 2.2, 1.95, 0.9
    ax.add_patch(Rectangle((ex0, ey0), ew, eh, fc="#E4E4E4", ec=INK, lw=1.2))
    ax.text(ex0 + ew / 2, ey0 + eh / 2, "metal\nenclosure", fontsize=6.5, ha="center",
            va="center")
    # load taps from L1 and N
    ax.plot([7.0, 7.0], [yL["L1"], ey0 + eh], color=INK, lw=0.9)
    ax.plot(7.0, yL["L1"], "o", color=INK, ms=2.5)
    ax.plot([7.5, 7.5], [yL["N"], ey0 + eh], color=COLORS[0], lw=0.9)
    ax.plot(7.5, yL["N"], "o", color=COLORS[0], ms=2.5)
    pe_col = COLORS[2]
    if kind == "TN-S":
        ax.plot([xs, xe], [yL["N"]] * 2, color=COLORS[0], lw=1.0)
        ax.text(xe + 0.08, yL["N"], "N", fontsize=7, va="center", color=COLORS[0])
        ax.plot([cx, cx], [yL["N"], yL["PE"]], color=pe_col, lw=1.0)
        ax.plot([cx, 8.5, 8.5, ex0 + ew], [yL["PE"], yL["PE"], ey0 + eh / 2, ey0 + eh / 2],
                color=pe_col, lw=1.2)
        ax.text(4.0, yL["PE"] - 0.08, "PE", fontsize=7, va="top", color=pe_col)
        _earth(ax, cx, yL["PE"] - 0.0 - 0.6)
        ax.plot([cx, cx], [yL["PE"], yL["PE"] - 0.6], color=INK, lw=1.0)
        ax.text(cx + 0.15, yL["PE"] - 1.2, "source earth", fontsize=6.5, va="top")
    elif kind == "TN-C-S":
        ax.plot([xs, split], [yL["N"]] * 2, color="#7A5C00", lw=1.6)
        ax.text(3.2, yL["N"] - 0.08, "PEN", fontsize=7, va="top", color="#7A5C00")
        ax.plot([split, xe], [yL["N"]] * 2, color=COLORS[0], lw=1.0)
        ax.text(xe + 0.08, yL["N"], "N", fontsize=7, va="center", color=COLORS[0])
        ax.plot(split, yL["N"], "o", color=INK, ms=3.5)
        ax.plot([split, split, 8.5, 8.5, ex0 + ew],
                [yL["N"], yL["PE"], yL["PE"], ey0 + eh / 2, ey0 + eh / 2], color=pe_col, lw=1.2)
        ax.text(6.2, yL["PE"] + 0.06, "PE", fontsize=7, va="bottom", color=pe_col)
        ax.plot([split, split], [yL["PE"], 2.3], color=INK, lw=1.0)
        _earth(ax, split, 2.3)
        ax.text(split + 0.35, 1.75, "PEN re-earthed\nat split", fontsize=6.3, ha="left", va="center")
        ax.plot([cx, cx], [yL["N"], 3.0], color=INK, lw=1.0)
        _earth(ax, cx, 3.0)
        ax.text(cx + 0.15, 2.45, "source earth", fontsize=6.5, va="top")
    else:
        ax.plot([xs, xe], [yL["N"]] * 2, color=COLORS[0], lw=1.0)
        ax.text(xe + 0.08, yL["N"], "N", fontsize=7, va="center", color=COLORS[0])
        # local earth of enclosure (TT and IT)
        ax.plot([ex0 + ew, 8.6, 8.6], [ey0 + eh / 2, ey0 + eh / 2, 2.0], color=pe_col, lw=1.2)
        _earth(ax, 8.6, 2.0)
        ax.text(8.8, 1.75, "$R_A$", fontsize=8, va="center")
        if kind == "TT":
            ax.plot([cx, cx], [yL["N"], 2.0], color=INK, lw=1.0)
            _earth(ax, cx, 2.0)
            ax.text(cx + 0.3, 1.75, "$R_B$", fontsize=8, va="center")
            ax.annotate("", xy=(cx + 0.35, 1.1), xytext=(8.25, 1.1),
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.1, ls="--"))
            ax.text(4.6, 0.95, "fault current returns through soil", fontsize=6.8, ha="center",
                    va="top", color=COLORS[1])
            ax.text(3.6, yL["PE"] - 0.05, "no PE between\nsource and installation",
                    fontsize=6.5, ha="center", va="top", color=GREY)
        else:  # IT
            # high impedance Z from star point to earth
            ax.plot([cx, cx], [yL["N"], 3.55], color=INK, lw=1.0)
            ax.add_patch(Rectangle((cx - 0.13, 2.85), 0.26, 0.7, fc="white", ec=INK, lw=1.1))
            ax.text(cx - 0.25, 3.2, "Z", fontsize=8, ha="right", va="center")
            ax.plot([cx, cx], [2.85, 2.0], color=INK, lw=1.0)
            _earth(ax, cx, 2.0)
            # IMD between N and earth
            ax.plot([3.2, 3.2], [yL["N"], 3.5], color=INK, lw=1.0)
            ax.plot(3.2, yL["N"], "o", color=INK, ms=2.5)
            ax.add_patch(Rectangle((2.75, 2.8), 0.9, 0.7, fc="#FFF4D6", ec=INK, lw=1.1))
            ax.text(3.2, 3.15, "IMD", fontsize=7, ha="center", va="center")
            ax.plot([3.2, 3.2, cx], [2.8, 2.3, 2.3], color=INK, lw=1.0)
            ax.plot(cx, 2.3, "o", color=INK, ms=2.5)
            ax.text(cx + 0.25, 1.55, "isolated or high-\nimpedance earthed", fontsize=6.3,
                    va="top")


def fig_earthing_systems():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.35), gridspec_kw=dict(wspace=0.04, hspace=0.02))
    specs = [("TN-S", "TN-S — industry"),
             ("TN-C-S", "TN-C-S — public LV supply"),
             ("TT", "TT — rural and outdoor supplies"),
             ("IT", "IT — hospitals, mines and ships")]
    for ax, (k, ttl) in zip(axs.flat, specs):
        _panel(ax, k, ttl)
    handles = [Line2D([], [], color=INK, lw=1.0, label="line"),
               Line2D([], [], color=COLORS[0], lw=1.0, label="neutral N"),
               Line2D([], [], color=COLORS[2], lw=1.2, label="protective conductor PE"),
               Line2D([], [], color="#7A5C00", lw=1.6, label="combined PEN")]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=7.5, bbox_to_anchor=(0.5, 0.0))
    save(fig, "29", "fig-29-3-earthing-systems")


# ---------------------------------------------------------------- 29.4
def fig_tn_fault_loop():
    """Earth-fault loop of a TN-S final circuit with touch voltage across R2."""
    fig, ax = plt.subplots(figsize=(6.8, 4.9))
    ax.set_aspect("equal")
    ax.axis("off")
    u = 3.0
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(unit=u, fontsize=9)
        src = elm.SourceSin().at((0, 0)).up()
        ze = elm.ResistorIEC().right()
        org = elm.Dot()
        elm.Breaker().right()
        r1 = elm.ResistorIEC().right()
        elm.Line().down(0.6)
        flt = elm.SparkGap().down(1.2)
        case = elm.Dot()
        elm.Line().down().toy(0)
        r2 = elm.ResistorIEC().left()
        met = elm.Dot()
        elm.Line().left().tox(0)
        d.draw()
    t = dict(fontsize=8.5, color=INK)
    ax.text(-0.7, u / 2, "$U_0$ = 230 V\ntransformer\nphase winding", ha="right", va="center", **t)
    ax.text(ze.center[0], u + 0.4, "$Z_e$ = 0.35 Ω\n(external loop)", ha="center", va="bottom", **t)
    ax.text(org.center[0], u - 0.25, "consumer\norigin", ha="center", va="top", fontsize=7.5)
    ax.text(1.5 * u, u + 0.55, "32 A MCB", ha="center", va="bottom", **t)
    ax.text(r1.center[0], u + 0.4, "$R_1$ = 0.267 Ω\n30 m, 2.5 mm², 70 °C", ha="center",
            va="bottom", fontsize=8, color=INK)
    ax.text(r2.center[0] - 0.3, 0.35, "$R_2$ = 0.436 Ω\n30 m, 1.5 mm² PE", ha="center",
            va="bottom", fontsize=8, color=INK)
    ax.text(met.center[0] - 0.15, 0.12, "MET", ha="right", va="bottom", fontsize=8)
    # fault-current arrows around the loop
    fc = COLORS[1]
    akw = dict(arrowprops=dict(arrowstyle="-|>", color=fc, lw=1.6, mutation_scale=12))
    ax.annotate("", xy=(1.0, u + 0.25), xytext=(0.2, u + 0.25), **akw)
    ax.annotate("", xy=(2 * u + 1.2, u + 0.25), xytext=(2 * u + 0.4, u + 0.25), **akw)
    ax.annotate("", xy=(1.6, -0.3), xytext=(2.6, -0.3), **akw)
    ax.text(1.5 * u, u / 2 - 0.05, "fault current $I_f$ = 218 A\n$Z_s$ = 0.35 + 0.267 + 0.436 = 1.053 Ω",
            ha="center", va="center", fontsize=9, color=fc)
    # appliance enclosure around the fault and the case node
    cx, cy = case.center
    ax.add_patch(FancyBboxPatch((cx - 0.5, -0.4), 1.15, 2.95,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="#E8E8E8", ec=INK, lw=1.0, zorder=0))
    ax.text(cx + 0.8, 0.5, "appliance\nmetal case", fontsize=8, ha="left", va="center")
    ax.text(cx + 0.8, flt.center[1] - 0.1, "fault:\nline to case", fontsize=8, ha="left",
            va="center", color=fc)
    # touch voltage across R2
    x0, x1 = met.center[0], cx
    ax.annotate("", xy=(x1, -0.75), xytext=(x0, -0.75),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[3], lw=1.3))
    ax.text((x0 + x1) / 2, -0.85, "touch voltage\n$U_t = I_f R_2$ = 95 V", fontsize=8.5,
            ha="center", va="top", color=COLORS[3])
    # bonded pipe at MET potential and person
    mx = met.center[0]
    ax.plot([mx, mx], [0, -2.0], color=COLORS[2], lw=1.3)
    ax.add_patch(Rectangle((mx - 0.14, -3.1), 0.28, 1.1, fc="#B0C4DE", ec=INK, lw=0.8))
    ax.text(mx, -3.2, "bonded\nmetal pipe", fontsize=7.5, ha="center", va="top")
    hx, hy = cx + 1.6, -1.95
    ax.add_patch(Circle((hx, hy), 0.22, fc="white", ec=INK, lw=1.1))
    ax.plot([hx, hx], [hy - 0.22, hy - 1.0], color=INK, lw=1.4)
    ax.plot([hx - 0.3, hx, hx + 0.3], [hy - 1.55, hy - 1.0, hy - 1.55], color=INK, lw=1.4)
    ax.plot([hx, cx + 0.3], [hy - 0.45, -0.4], color=INK, lw=1.4)         # hand on case
    ax.plot([hx, mx + 0.14], [hy - 0.45, -2.45], color=INK, lw=1.4)       # hand on pipe
    ax.text(hx + 0.35, hy - 0.2, "person", fontsize=7.5, ha="left", va="center")
    # inset table
    tx, ty = -3.0, -1.55
    cols = [(0.0, ["32 A MCB", "type B", "type C"]),
            (2.0, ["instant trip above", "5 × 32 = 160 A", "10 × 32 = 320 A"]),
            (4.95, ["at $I_f$ = 218 A", "trips: meets 0.4 s", "fails: thermal only"])]
    ax.add_patch(FancyBboxPatch((tx - 0.15, ty - 1.45), 8.0, 1.6,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc="#F6F6F6", ec=GREY, lw=0.8))
    for dx, items in cols:
        for k, s in enumerate(items):
            col = INK if k != 2 or dx < 4 else RED
            if k == 1 and dx > 4:
                col = GREEN
            ax.text(tx + dx, ty - 0.05 - k * 0.47, s, fontsize=7.8, ha="left", va="top", color=col,
                    fontweight="normal")
    ax.set_xlim(-3.3, 3 * u + 2.4)
    ax.set_ylim(-3.95, u + 1.4)
    save(fig, "29", "fig-29-4-tn-fault-loop")


# ---------------------------------------------------------------- 29.5
def _diamond(ax, x, y, w, h, text, fs=8.3):
    ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)],
                         closed=True, fc="#FFF4D6", ec=INK, lw=1.0))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


def _ppe_icon(ax, x, y, s=0.32):
    """Simple hood-and-visor icon."""
    ax.add_patch(Polygon([(x - s, y - s), (x - s, y + 0.4 * s), (x - 0.5 * s, y + s),
                          (x + 0.5 * s, y + s), (x + s, y + 0.4 * s), (x + s, y - s)],
                         closed=True, fc=COLORS[4], ec=INK, lw=0.9))
    ax.add_patch(Rectangle((x - 0.6 * s, y - 0.2 * s), 1.2 * s, 0.55 * s, fc="#2F4F6F", ec=INK,
                           lw=0.8))


def fig_isolation_sequence():
    fig, ax = schematic(6.8, 7.2, xlim=(0, 10), ylim=(0, 10.6))
    X, W, H = 4.6, 4.8, 0.62
    steps = [
        ("q", "Work requested:\ncan it be done de-energised?"),
        ("b", "1  Identify all sources from up-to-date\nsingle-line diagram"),
        ("b", "2  Disconnect: open isolators,\nwithdraw breakers"),
        ("b", "3  Lock and tag: personal lock per worker"),
        ("b", "4  Release stored energy: discharge\ncapacitors, wait time from nameplate"),
        ("b", "5  Test before touch: live–dead–live\nwith CAT-rated detector"),
        ("q", "Voltage absent on\nall conductors?"),
        ("b", "6  Earth and short-circuit where required"),
        ("b", "7  Barriers to adjacent live parts"),
        ("e", "Electrically safe work condition established:\nwork may start"),
    ]
    ys = np.linspace(10.0, 0.55, len(steps))
    for i, ((kind, txt), y) in enumerate(zip(steps, ys)):
        if kind == "q":
            _diamond(ax, X, y, W * 0.78, 0.98, txt)
        elif kind == "e":
            box(ax, X - W / 2, y - H / 2, W, H, txt, fc="#DFF0E3", fontsize=8.3)
        else:
            box(ax, X - W / 2, y - H / 2, W, H, txt, fontsize=8.3)
        if i < len(steps) - 1:
            top = y - (0.49 if kind == "q" else H / 2)
            nxt = ys[i + 1] + (0.49 if steps[i + 1][0] == "q" else H / 2)
            arrow(ax, X, top, X, nxt)
    # yes labels
    ax.text(X + 0.12, (ys[0] + ys[1]) / 2 + 0.05, "yes", fontsize=8, va="center", color=GREEN)
    ax.text(X + 0.12, (ys[6] + ys[7]) / 2 + 0.05, "yes", fontsize=8, va="center", color=GREEN)
    # no branch from start
    xr = X + W * 0.39
    arrow(ax, xr, ys[0], 7.45, ys[0])
    ax.text((xr + 7.45) / 2, ys[0] + 0.06, "no", fontsize=8, color=RED, ha="center", va="bottom")
    box(ax, 7.45, ys[0] - 0.45, 2.45, 0.9, "Justify energised work:\npermit, risk\nassessment, PPE",
        fc="#FBE3E0", fontsize=7.5)
    # no branch from test decision: loop back to step 1
    xl = X - W * 0.39
    xloop = 1.05
    ax.plot([xl, xloop, xloop], [ys[6], ys[6], ys[1]], color=RED, lw=1.1)
    arrow(ax, xloop, ys[1], X - W / 2, ys[1], color=RED)
    ax.text((xl + xloop) / 2 + 0.1, ys[6] + 0.06, "no", fontsize=8, color=RED, ha="center",
            va="bottom")
    ax.text(xloop - 0.12, (ys[1] + ys[6]) / 2, "missed source:\nback to step 1", fontsize=7,
            color=RED, rotation=90, ha="right", va="center")
    # side note of sources
    ax.text(X + W / 2 + 0.2, ys[1], "mains, generator, UPS,\nPV, batteries, capacitors,\nback-feed",
            fontsize=7, va="center", color=GREY)
    # PPE bracket beside steps 2-5
    xb = X + W / 2 + 0.25
    ax.plot([xb, xb + 0.15, xb + 0.15, xb], [ys[2] + H / 2, ys[2] + H / 2, ys[5] - H / 2,
                                             ys[5] - H / 2], color=COLORS[4], lw=1.6)
    _ppe_icon(ax, xb + 0.75, (ys[2] + ys[5]) / 2 + 0.35)
    ax.text(xb + 0.4, (ys[2] + ys[5]) / 2 - 0.15, "treat as live:\nshock and arc-flash\nPPE until "
            "step 5\nis passed", fontsize=7, va="top", ha="left")
    save(fig, "29", "fig-29-5-isolation-sequence")


# ---------------------------------------------------------------- 29.6
def _stadium(ax, half, r, **kw):
    """Boundary at distance r in front of an exposed segment x in [-half, half] on y = 0."""
    th = np.linspace(np.pi, 1.5 * np.pi, 40)
    left = np.c_[-half + r * np.cos(th), r * np.sin(th)]
    th2 = np.linspace(1.5 * np.pi, 2 * np.pi, 40)
    right = np.c_[half + r * np.cos(th2), r * np.sin(th2)]
    pts = np.vstack([left, right])
    ax.plot(pts[:, 0], pts[:, 1], **kw)


def fig_approach_boundaries():
    fig, ax = schematic(6.8, 3.9, xlim=(-2.6, 5.6), ylim=(-2.35, 0.95))
    # switchboard
    ax.add_patch(Rectangle((-1.5, 0), 3.0, 0.55, fc="#D9D9D9", ec=INK, lw=1.2))
    ax.text(0, 0.62, "400 V main switchboard, 3 m wide, door open (plan view)", fontsize=7.5,
            ha="center", va="bottom")
    half = 0.5
    ax.add_patch(Rectangle((-half, 0.0), 2 * half, 0.18, fc=COLORS[1], ec=INK, lw=0.8))
    ax.text(0, 0.24, "exposed busbars", fontsize=6.8, ha="center", va="bottom")
    bnds = [(1.73, PURPLE, "--", 1.6, "arc-flash boundary 1.73 m (0.5 s clearing)"),
            (1.0, ORANGE, "--", 1.6, "limited approach 1.0 m"),
            (0.55, PURPLE, ":", 1.8, "arc-flash boundary 0.55 m (arc-flash relay)"),
            (0.3, RED, "--", 1.6, "restricted approach 0.3 m")]
    for r, c, ls, lw, lab in bnds:
        _stadium(ax, half, r, color=c, ls=ls, lw=lw)
    # worker at working distance
    wy = -0.455
    ax.add_patch(Circle((0.15, wy - 0.13), 0.12, fc="#F2D7B6", ec=INK, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((-0.12, wy - 0.42), 0.54, 0.2, fc=COLORS[0], ec=INK, lw=0.9, zorder=3))
    ax.annotate("", xy=(-0.25, 0), xytext=(-0.25, wy),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=8))
    ax.annotate("working distance\n455 mm", xy=(-0.27, wy / 2), xytext=(-2.55, 0.3), fontsize=7,
                ha="left", va="center", arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    # labels along the right
    ax.text(half + 0.3 * 0.71 + 0.05, -0.3 * 0.71 - 0.02, "0.3", color=RED, fontsize=7)
    ax.text(half + 0.55 * 0.71 + 0.05, -0.55 * 0.71 - 0.02, "0.55", color=PURPLE, fontsize=7)
    ax.text(half + 1.0 * 0.71 + 0.05, -1.0 * 0.71 - 0.02, "1.0", color=ORANGE, fontsize=7)
    ax.text(half + 1.73 * 0.71 + 0.05, -1.73 * 0.71 - 0.02, "1.73 m", color=PURPLE, fontsize=7)
    # scale bar
    sx, sy = -2.4, -2.15
    for i in range(2):
        ax.add_patch(Rectangle((sx + i, sy), 1, 0.07, fc=INK if i == 0 else "white", ec=INK, lw=0.8))
    for i, s in enumerate(["0", "1", "2 m"]):
        ax.text(sx + i, sy + 0.11, s, fontsize=7, ha="center", va="bottom")
    # legend
    lx, ly = 2.55, 0.55
    entries = [(RED, "--", "restricted approach 0.3 m",
                "qualified persons only, with shock\nPPE, insulated tools and a plan"),
               (ORANGE, "--", "limited approach 1.0 m",
                "unqualified persons stop here unless\nescorted by a qualified person"),
               (PURPLE, "--", "arc-flash boundary 1.73 m (t = 0.5 s)",
                "arc-rated PPE ≥ incident energy\n(17.2 cal/cm² at 455 mm) inside"),
               (PURPLE, ":", "arc-flash boundary 0.55 m (t = 0.05 s)",
                "with arc-flash relay: 1.7 cal/cm²")]
    for i, (c, ls, head, body) in enumerate(entries):
        y = ly - i * 0.72
        ax.plot([lx, lx + 0.4], [y - 0.05, y - 0.05], color=c, ls=ls, lw=1.8)
        ax.text(lx + 0.5, y, head, fontsize=7.5, va="center", color=c, fontweight="bold")
        ax.text(lx + 0.5, y - 0.12, body, fontsize=6.8, va="top")
    save(fig, "29", "fig-29-6-approach-boundaries")


if __name__ == "__main__":
    fig_iec60479_zones()
    fig_incident_energy()
    fig_earthing_systems()
    fig_tn_fault_loop()
    fig_isolation_sequence()
    fig_approach_boundaries()
