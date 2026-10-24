"""Figures for Chapter 22 — Distribution Systems.\n\nRun from the repository root:  python figures/scripts/ch22.py\n"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch

from figstyle import new_fig, schematic, save, COLORS, INK

CH = "22"


# ----------------------------------------------------------------------------
# Single-line drawing helpers (matplotlib only)
# ----------------------------------------------------------------------------
def line(ax, xs, ys, color=INK, lw=1.2, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def bus(ax, xs, ys, color=INK):
    ax.plot(xs, ys, color=color, lw=3.2, solid_capstyle="butt")


def breaker(ax, x, y, s=0.26, fc="white", color=INK):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=color, lw=1.1, zorder=4))


def xfmr_h(ax, x, y, r=0.26, oltc=False, color=INK):
    """Two-winding transformer drawn horizontally, centred at (x, y)."""
    ax.add_patch(Circle((x - 0.3 * r * 1.0 - 0.15 * r, y), r, fill=False, ec=color, lw=1.2, zorder=3))
    ax.add_patch(Circle((x + 0.3 * r * 1.0 + 0.15 * r, y), r, fill=False, ec=color, lw=1.2, zorder=3))
    if oltc:
        ax.annotate("", xy=(x + 1.3 * r, y + 1.1 * r), xytext=(x - 1.3 * r, y - 1.1 * r),
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color=color, mutation_scale=7))
    return x - 1.45 * r, x + 1.45 * r


def xfmr_v(ax, x, y, r=0.24, color=INK):
    """Two-winding transformer drawn vertically, centred at (x, y)."""
    ax.add_patch(Circle((x, y + 0.45 * r), r, fill=False, ec=color, lw=1.1, zorder=3))
    ax.add_patch(Circle((x, y - 0.45 * r), r, fill=False, ec=color, lw=1.1, zorder=3))
    return y + 1.45 * r, y - 1.45 * r


def fuse_h(ax, x, y, w=0.36, h=0.14, color=INK):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=color, lw=1.0, zorder=4))
    line(ax, [x - w / 2, x + w / 2], [y, y], color, lw=0.8, zorder=5)


def fuse_v(ax, x, y, w=0.14, h=0.36, color=INK):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=color, lw=1.0, zorder=4))
    line(ax, [x, x], [y - h / 2, y + h / 2], color, lw=0.8, zorder=5)


def open_switch_h(ax, x, y, w=0.4, color=INK):
    """Open switch (gap with lifted blade) on a horizontal line centred at x."""
    ax.add_patch(Rectangle((x - w / 2 - 0.02, y - 0.12), w + 0.04, 0.24, fc="white", ec="none", zorder=4))
    line(ax, [x - w / 2, x + w / 2 - 0.05], [y, y + 0.22], color, zorder=5)
    ax.plot([x - w / 2, x + w / 2], [y, y], "o", ms=2.5, color=color, zorder=5)


def open_switch_v(ax, x, y, h=0.4, color=INK):
    ax.add_patch(Rectangle((x - 0.12, y - h / 2 - 0.02), 0.24, h + 0.04, fc="white", ec="none", zorder=4))
    line(ax, [x, x + 0.22], [y - h / 2, y + h / 2 - 0.05], color, zorder=5)
    ax.plot([x, x], [y - h / 2, y + h / 2], "o", ms=2.5, color=color, zorder=5)


def relay(ax, x, y, text="51", fs=6.5):
    ax.add_patch(Circle((x, y), 0.17, fc="white", ec=COLORS[0], lw=0.9, zorder=4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=COLORS[0], zorder=5)


def house(ax, x, y, w=0.42, h=0.3, color=INK, fc="white"):
    """Small house symbol with bottom-centre at (x, y)."""
    ax.add_patch(Polygon([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x, y + h + 0.22),
                          (x - w / 2, y + h)], closed=True, fc=fc, ec=color, lw=0.9, zorder=3))


def load_arrow(ax, x, y, dy=-0.35, color=INK):
    ax.annotate("", xy=(x, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color=color, mutation_scale=8))


def rmu(ax, x, y, s=0.42, label=None, fs=7):
    ax.add_patch(FancyBboxPatch((x - s / 2, y - s / 2), s, s, boxstyle="round,pad=0.01,rounding_size=0.05",
                                fc="#EEF3F8", ec=INK, lw=1.0, zorder=4))
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, zorder=5)


# ----------------------------------------------------------------------------
# Figure 22.1 — distribution chain
# ----------------------------------------------------------------------------
def fig_22_1():
    fig, ax = schematic(6.9, 5.0, xlim=(-0.3, 17.6), ylim=(-0.6, 12.4))
    fs = 7.5

    # --- grid substation: 132 kV busbar and two 90 MVA transformers --------
    bus(ax, [0.4, 0.4], [6.3, 11.3])
    ax.text(0.4, 11.55, "132 kV", ha="center", fontsize=fs, weight="bold")
    bus(ax, [3.0, 3.0], [6.3, 11.3])
    ax.text(3.0, 11.55, "33 kV", ha="center", fontsize=fs, weight="bold")
    for y in (10.1, 7.5):
        line(ax, [0.4, 3.0], [y, y])
        breaker(ax, 0.9, y)
        xfmr_h(ax, 1.7, y)
        breaker(ax, 2.5, y)
    ax.text(1.7, 8.8, "2 × 90 MVA\n132/33 kV", ha="center", va="center", fontsize=fs)
    ax.text(1.7, 5.75, "Grid substation", ha="center", fontsize=fs, style="italic")

    # --- 33 kV ring to three primary substations --------------------------
    ring = dict(color=COLORS[0], lw=1.3)
    # ring path: from 33 kV bus top and bottom out to x=5.6, closing on the right
    line(ax, [3.0, 5.7], [10.9, 10.9], **ring)
    line(ax, [3.0, 5.7], [6.7, 6.7], **ring)
    line(ax, [5.7, 5.7], [6.7, 10.9], **ring)
    breaker(ax, 3.4, 10.9)
    breaker(ax, 3.4, 6.7)
    ax.text(4.35, 11.1, "33 kV ring", ha="center", va="bottom", fontsize=fs, color=COLORS[0])
    # primary A and C as small boxes on the ring
    for (x, y, lab) in ((4.55, 10.9, "Primary\nA"), (4.55, 6.7, "Primary\nC")):
        rmu(ax, x, y, s=0.5)
        ax.text(x, y - 0.42 if y < 8 else y - 0.42, lab, ha="center", va="top", fontsize=6.8)
    # primary B tapped from right side of ring (detailed)
    ax.plot([5.7], [8.8], "o", ms=3, color=COLORS[0])
    line(ax, [5.7, 6.1], [8.8, 8.8])
    line(ax, [6.1, 6.1], [7.7, 9.9])
    for y in (9.9, 7.7):
        line(ax, [6.1, 8.3], [y, y])
        breaker(ax, 6.5, y)
        xfmr_h(ax, 7.3, y, oltc=True)
    ax.text(6.95, 7.3, "2 × 20 MVA\n33/11 kV Dyn11\nOLTC ±10 %\n(17 taps)", ha="center", va="top",
            fontsize=6.3)
    ax.text(7.2, 5.55, "Primary substation B", ha="center", fontsize=fs, style="italic")

    # --- 11 kV split busbar with bus-section breaker -----------------------
    bus(ax, [8.3, 8.3], [8.95, 11.0])
    bus(ax, [8.3, 8.3], [6.2, 8.25])
    line(ax, [8.3, 8.3], [8.25, 8.95], lw=1.2)
    breaker(ax, 8.3, 8.6)
    ax.text(8.1, 8.6, "bus\nsection", ha="right", va="center", fontsize=6.3)
    ax.text(8.3, 11.25, "11 kV", ha="center", fontsize=fs, weight="bold")
    feeders = [10.6, 9.95, 9.3, 7.85, 7.2, 6.55]
    for i, y in enumerate(feeders):
        line(ax, [8.3, 9.6], [y, y])
        breaker(ax, 8.75, y)
        relay(ax, 9.2, y + 0.27, fs=5.5)
        line(ax, [9.2, 9.2], [y + 0.1, y], lw=0.6, color=COLORS[0])
    for y in feeders[1:5]:
        ax.annotate("", xy=(10.1, y), xytext=(9.6, y),
                    arrowprops=dict(arrowstyle="-|>", lw=1.0, color=INK, mutation_scale=7))
    ax.text(10.2, 8.6, "6 × 11 kV\nfeeders,\nbreakers\nwith relays", ha="left", va="center", fontsize=6.6)

    # --- open ring through four RMUs, NOP ----------------------------------
    ring2 = dict(color=COLORS[1], lw=1.3)
    yt, yb = feeders[0], feeders[-1]
    line(ax, [9.6, 16.9], [yt, yt], **ring2)
    line(ax, [9.6, 16.9], [yb, yb], **ring2)
    line(ax, [16.9, 16.9], [yb, yt], **ring2)
    rmus = [(11.8, yt, "RMU 1"), (14.6, yt, "RMU 2"), (14.6, yb, "RMU 3"), (11.8, yb, "RMU 4")]
    for x, y, lab in rmus:
        rmu(ax, x, y, s=0.42)
        ax.text(x + 0.3, y + (-0.12 if y == yt else 0.12), lab, ha="left", va="top" if y == yt else "bottom",
                fontsize=6.5)
    open_switch_v(ax, 16.9, (yt + yb) / 2, h=0.5)
    ax.text(16.7, (yt + yb) / 2, "NOP", ha="right", va="center", fontsize=fs, weight="bold",
            color=COLORS[1])
    ax.text(13.2, 9.75, "11 kV open ring (cable)", ha="center", va="center", fontsize=6.8,
            color=COLORS[1])
    # secondary transformers: upward on top row, downward on bottom row
    for x, y, _ in rmus:
        if y == yt:
            line(ax, [x, x], [y + 0.21, y + 0.62])
            t, b = xfmr_v(ax, x, y + 0.95, r=0.2)
            load_arrow(ax, x, t, dy=0.35)
        else:
            line(ax, [x, x], [y - 0.21, y - 0.62])
            t, b = xfmr_v(ax, x, y - 0.95, r=0.2)
            if x > 12.5:
                load_arrow(ax, x, b, dy=-0.35)
    ax.text(11.45, yt + 1.05, "500 kVA\n11/0.4 kV Dyn11", ha="right", va="center", fontsize=6.3)
    ax.text(14.95, yb - 0.95, "500 kVA", ha="left", va="center", fontsize=6.3)
    ax.text(14.2, 8.25, "each secondary\nsubstation supplies\n≈100–250 customers", ha="center",
            va="center", fontsize=6.8, style="italic")

    # --- LV board under RMU 4 with four radial feeders ---------------------
    x4 = 11.8
    bot = yb - 0.95 - 1.45 * 0.2
    ybus = 4.4
    line(ax, [x4, x4], [bot, ybus])
    bus(ax, [8.9, 13.7], [ybus, ybus])
    ax.text(12.0, ybus + 0.15, "400/230 V LV board", ha="left", va="bottom", fontsize=6.8, weight="bold")
    xs_f = [9.2, 10.6, 12.0, 13.4]
    yh = [3.3, 2.3, 1.3, 0.3]
    for i, xf in enumerate(xs_f):
        line(ax, [xf, xf], [ybus, yh[-1] + 0.05])
        fuse_v(ax, xf, ybus - 0.4)
        for yy in yh:
            line(ax, [xf, xf + 0.35], [yy, yy], lw=0.8)
            house(ax, xf + 0.6, yy - 0.12, w=0.42, h=0.26)
    ax.text(9.0, 2.0, "4 × 400 V radial\ncable feeders\n300 mm² Al XLPE", ha="right", va="center", fontsize=6.8)
    # PV roof and EV charger on one house (feeder 4, top house)
    xh, yr = xs_f[3] + 0.6, yh[0] - 0.12
    ax.add_patch(Polygon([(xh - 0.21, yr + 0.26), (xh, yr + 0.48), (xh + 0.05, yr + 0.43),
                          (xh - 0.16, yr + 0.21)], closed=True, fc=COLORS[4], ec=INK, lw=0.6, zorder=5))
    ax.add_patch(Rectangle((xh + 0.35, yr), 0.17, 0.26, fc=COLORS[2], ec=INK, lw=0.6, zorder=5))
    line(ax, [xh + 0.21, xh + 0.35], [yr + 0.1, yr + 0.1], lw=0.6)
    ax.text(xh + 0.65, yr + 0.35, "rooftop PV\n+ EV charger", ha="left", va="center", fontsize=6.3)

    # --- voltage-level ribbons ---------------------------------------------
    for x0, x1, lab, yy in ((-0.1, 5.9, "Subtransmission 132 kV and 33 kV", 5.15),
                            (5.9, 8.6, "33/11 kV", 5.15)):
        ax.annotate("", xy=(x1, yy), xytext=(x0, yy),
                    arrowprops=dict(arrowstyle="<->", lw=0.8, color="#777777"))
        ax.text((x0 + x1) / 2, yy - 0.15, lab, ha="center", va="top", fontsize=6.8, color="#555555")
    ax.text(0.0, 2.6, "Levels, source to customer:\n"
            "132/33 kV grid substation\n"
            "33/11 kV primary substations\n"
            "11 kV primary feeders (3–8 MVA)\n"
            "11/0.4 kV secondary substations\n"
            "400/230 V LV mains to customers",
            ha="left", va="center", fontsize=6.8, color="#444444", linespacing=1.35)
    save(fig, CH, "fig-22-1-distribution-chain")


# ----------------------------------------------------------------------------
# Figure 22.2 — radial, open ring, closed ring, secondary network
# ----------------------------------------------------------------------------
def _panel_title(ax, letter, title, use):
    ax.text(0.0, 6.05, f"({letter}) {title}", fontsize=9, weight="bold", va="bottom")
    ax.text(0.0, -0.15, use, fontsize=8, style="italic", va="top", color="#444444")


def _ring(ax, closed, fault=False):
    """Loop of six RMUs fed from bus sections A and B."""
    bus(ax, [0.3, 1.5], [5.2, 5.2])
    bus(ax, [1.9, 3.1], [5.2, 5.2])
    line(ax, [1.5, 1.9], [5.2, 5.2])
    breaker(ax, 1.7, 5.2, s=0.22)
    ax.text(0.9, 5.4, "A", ha="center", fontsize=8)
    ax.text(2.5, 5.4, "B", ha="center", fontsize=8)
    # two feeder breakers down from each section
    xa, xb = 0.9, 2.5
    for x in (xa, xb):
        line(ax, [x, x], [5.2, 4.2])
        breaker(ax, x, 4.75)
    # loop: left leg down from A, bottom across, right leg up to B
    pts = {1: (xa, 3.4), 2: (xa, 1.9), 3: (xa + 1.0, 0.8), 4: (xb + 2.0, 0.8), 5: (xb + 2.4, 2.4),
           6: (xb + 1.4, 4.2)}
    path = [(xa, 4.2), pts[1], pts[2], (xa, 0.8), pts[3], pts[4], (xb + 2.4, 0.8), pts[5],
            (xb + 2.4, 4.2), pts[6], (xb, 4.2)]
    xs, ys = zip(*path)
    line(ax, xs, ys, lw=1.3)
    for k, (x, y) in pts.items():
        rmu(ax, x, y, s=0.44, label=str(k), fs=7.5)
        # load tap
        if y in (0.8,):
            line(ax, [x, x], [y - 0.22, y - 0.5], lw=0.9)
            load_arrow(ax, x, y - 0.5, dy=-0.25)
        elif x == xa:
            line(ax, [x - 0.22, x - 0.5], [y, y], lw=0.9)
            ax.annotate("", xy=(x - 0.75, y), xytext=(x - 0.5, y),
                        arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=7))
        elif y == 4.2:
            line(ax, [x, x], [y + 0.22, y + 0.5], lw=0.9)
            load_arrow(ax, x, y + 0.5, dy=0.25)
        else:
            line(ax, [x + 0.22, x + 0.5], [y, y], lw=0.9)
            ax.annotate("", xy=(x + 0.75, y), xytext=(x + 0.5, y),
                        arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=7))
    return pts, xa, xb


def fig_22_2():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 5.6))
    for ax in axs.flat:
        ax.set_xlim(-0.3, 5.9)
        ax.set_ylim(-0.75, 6.4)
        ax.set_aspect("equal")
        ax.axis("off")

    # (a) radial
    ax = axs[0, 0]
    bus(ax, [0.2, 1.4], [5.2, 5.2])
    line(ax, [0.8, 0.8], [5.2, 3.5])
    breaker(ax, 0.8, 4.75)
    line(ax, [0.8, 5.6], [3.5, 3.5], lw=1.5)
    # recloser on main
    ax.add_patch(Rectangle((2.35, 3.32), 0.36, 0.36, fc=COLORS[4], ec=INK, lw=1.0, zorder=4))
    ax.text(2.53, 3.82, "recloser", ha="center", va="bottom", fontsize=7)
    for x in (1.4, 3.2, 4.8, 5.6):
        line(ax, [x, x], [3.5, 3.2], lw=0.9)
        load_arrow(ax, x, 3.2, dy=-0.3)
    # laterals with fuses
    for x in (2.0, 3.9):
        line(ax, [x, x], [3.5, 0.9], lw=1.0)
        fuse_v(ax, x, 3.0)
        for y in (2.2, 1.3):
            line(ax, [x, x + 0.35], [y, y], lw=0.9)
            ax.annotate("", xy=(x + 0.6, y), xytext=(x + 0.35, y),
                        arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, mutation_scale=7))
        ax.text(x + 0.15, 2.95, "fuse", ha="left", va="center", fontsize=7)
    ax.text(3.1, 0.6, "laterals", ha="center", fontsize=7)
    ax.text(3.6, 3.62, "main", ha="center", va="bottom", fontsize=7)
    ax.text(1.0, 4.75, "CB", ha="left", va="center", fontsize=7)
    _panel_title(ax, "a", "Radial", "Rural overhead feeders")

    # (b) open ring with NOP and fault
    ax = axs[0, 1]
    pts, xa, xb = _ring(ax, closed=False)
    # NOP between RMU 3 and RMU 4 on the bottom run
    xn = (pts[3][0] + pts[4][0]) / 2
    open_switch_h(ax, xn, 0.8, w=0.38)
    ax.text(xn, 0.55, "NOP", ha="center", va="top", fontsize=8, weight="bold", color=COLORS[1])
    # fault between RMU 1 and RMU 2
    yf = (pts[1][1] + pts[2][1]) / 2
    ax.plot([xa], [yf], marker="X", ms=9, color=COLORS[1], zorder=6)
    ax.text(xa + 0.2, yf, "fault", ha="left", va="center", fontsize=7.5, color=COLORS[1])
    # restoration path: from B round the ring through closed NOP to RMU 2
    rp = [(xb + 0.15, 3.95), (xb + 1.3, 3.95), (xb + 2.15, 3.95), (xb + 2.15, 1.05),
          (xa + 0.25, 1.05), (xa + 0.25, 1.75)]
    xs, ys = zip(*rp)
    ax.plot(xs, ys, color=COLORS[2], lw=1.4, ls=(0, (4, 2)), zorder=2)
    ax.annotate("", xy=rp[-1], xytext=(xa + 0.25, 1.3),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=COLORS[2], mutation_scale=10))
    ax.text(3.0, 2.4, "restoration:\nisolate 1–2,\nclose NOP,\nfeed 2–3 from B",
            ha="center", va="center", fontsize=7, color=COLORS[2])
    _panel_title(ax, "b", "Open ring", "Urban cable networks (RMUs)")

    # (c) closed ring with directional relays
    ax = axs[1, 0]
    pts, xa, xb = _ring(ax, closed=True)
    for x in (xa, xb):
        ax.add_patch(Circle((x + 0.42, 4.75), 0.2, fc="white", ec=COLORS[0], lw=1.0, zorder=4))
        ax.text(x + 0.42, 4.75, "67", ha="center", va="center", fontsize=6.5, color=COLORS[0], zorder=5)
        line(ax, [x + 0.13, x + 0.22], [4.75, 4.75], lw=0.7, color=COLORS[0])
    ax.text(3.0, 2.4, "all switches closed;\ndirectional (67) or\nunit protection\nat both ends",
            ha="center", va="center", fontsize=7, color=COLORS[0])
    _panel_title(ax, "c", "Closed ring", "Subtransmission, critical industry")

    # (d) secondary network
    ax = axs[1, 1]
    bus(ax, [0.2, 5.6], [5.2, 5.2])
    ax.text(5.65, 5.2, "MV", ha="left", va="center", fontsize=7)
    xs_f = [0.9, 2.9, 4.9]
    grid_nodes = [(0.9, 1.9), (2.9, 1.9), (4.9, 1.9), (0.9, 0.5), (2.9, 0.5), (4.9, 0.5)]
    for i, x in enumerate(xs_f):
        line(ax, [x, x], [5.2, 4.6])
        breaker(ax, x, 4.95, s=0.2)
        t, b = xfmr_v(ax, x, 4.05, r=0.2)
        line(ax, [x, x], [t, 4.6])
        line(ax, [x, x], [b, 2.95])
        ax.add_patch(Rectangle((x - 0.2, 2.75), 0.4, 0.3, fc=COLORS[5], ec=INK, lw=0.9, zorder=4))
        ax.text(x, 2.9, "NP", ha="center", va="center", fontsize=6.5, zorder=5)
        line(ax, [x, x], [2.75, 1.9])
        ax.text(x + 0.3, 4.05, f"F{i + 1}", ha="left", va="center", fontsize=7)
    # meshed LV grid
    gl = dict(lw=1.5, color=COLORS[3])
    line(ax, [0.9, 4.9], [1.9, 1.9], **gl)
    line(ax, [0.9, 4.9], [0.5, 0.5], **gl)
    for x in xs_f:
        line(ax, [x, x], [1.9, 0.5], **gl)
    for (x, y) in grid_nodes:
        ax.plot([x], [y], "o", ms=4.5, color=COLORS[3], zorder=5)
    ax.text(5.15, 1.2, "meshed\nLV grid", ha="left", va="center", fontsize=7, color=COLORS[3])
    ax.text(3.9, 2.35, "network protectors\n(reverse power)", ha="center", va="center", fontsize=6.5)
    _panel_title(ax, "d", "Secondary network", "Downtown cores")

    fig.subplots_adjust(wspace=0.08, hspace=0.12, left=0.01, right=0.99, top=0.98, bottom=0.02)
    save(fig, CH, "fig-22-2-radial-ring-network")


# ----------------------------------------------------------------------------
# Figure 22.3 — transformer efficiency
# ----------------------------------------------------------------------------
def fig_22_3():
    Sr, pf = 1000.0, 0.95
    k = np.linspace(0.005, 1.2, 600)
    units = [("Low-loss: $P_0$ = 0.70 kW, $P_k$ = 9.0 kW", 0.70, 9.0, "-", COLORS[0]),
             ("1990s unit: $P_0$ = 1.70 kW, $P_k$ = 10.5 kW", 1.70, 10.5, "--", COLORS[1])]
    cycle = [(0.9, 6), (0.5, 10), (0.2, 8)]
    fig, ax = new_fig(6.4, 4.0)
    for kk, h in cycle:
        ax.axvspan(kk - 0.03, kk + 0.03, color="#E8E8E8", zorder=0)
        ax.text(kk, 97.56, f"{h} h/day", ha="center", va="bottom", fontsize=8, color="#444444")
    for lab, P0, Pk, ls, c in units:
        P = k * Sr * pf
        eta = 100 * P / (P + P0 + k ** 2 * Pk)
        ax.plot(k, eta, ls=ls, color=c, label=lab)
        km = np.sqrt(P0 / Pk)
        em = 100 * km * Sr * pf / (km * Sr * pf + 2 * P0)
        ax.plot([km], [em], "o", color=c, ms=5)
        # all-day efficiency
        Eout = Sr * pf * sum(kk * h for kk, h in cycle)
        Eloss = 24 * P0 + Pk * sum(kk ** 2 * h for kk, h in cycle)
        eday = 100 * Eout / (Eout + Eloss)
        if P0 < 1:
            ax.annotate(f"max {em:.2f} % at k = {km:.2f}", xy=(km, em), xytext=(0.36, 99.56),
                        fontsize=8, color=c, arrowprops=dict(arrowstyle="-", color=c, lw=0.7))
            ax.text(0.47, 98.33, f"low-loss unit  {eday:.2f} %", fontsize=8.5, color=c)
        else:
            ax.annotate(f"max {em:.2f} % at k = {km:.2f}", xy=(km, em), xytext=(0.5, 98.82),
                        fontsize=8, color=c, arrowprops=dict(arrowstyle="-", color=c, lw=0.7))
            ax.text(0.47, 98.21, f"1990s unit      {eday:.2f} %", fontsize=8.5, color=c)
    ax.set_xlim(0, 1.2)
    ax.set_ylim(97.5, 99.65)
    ax.set_xlabel("Per-unit load $k$")
    ax.set_ylabel("Efficiency (%)")
    ax.grid(True, lw=0.5)
    ax.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.07))
    ax.text(0.47, 98.45, "All-day efficiency over the shaded cycle:", fontsize=8.5, color=INK)
    ax.text(1.19, 99.6, "1000 kVA, 11/0.4 kV, PF 0.95", fontsize=8, color="#444444", ha="right", va="top")
    save(fig, CH, "fig-22-3-transformer-efficiency")


# ----------------------------------------------------------------------------
# Figure 22.4 — feeder voltage profile
# ----------------------------------------------------------------------------
def fig_22_4():
    l = 8.0
    P, pf, V = 3.0e6, 0.9, 11e3
    R, X = 0.273 * l, 0.35 * l
    Q = P * np.tan(np.arccos(pf))
    d = (R * P + X * Q) / V ** 2          # 0.0878
    I = P / (np.sqrt(3) * V * pf)
    loss_l = 3 * I ** 2 * R / 1e3
    loss_u = loss_l / 3
    s = np.linspace(0, l, 200)
    v_l = 1 - d * s / l
    v_u = 1 - d * (s / l - s ** 2 / (2 * l ** 2))
    fig, ax = new_fig(6.4, 3.8)
    ax.plot(s, v_l, "--", color=COLORS[1], label="load lumped at the end")
    ax.plot(s, v_u, "-", color=COLORS[0], label="load uniformly distributed")
    ax.axhline(0.94, ls=":", color=INK, lw=1.2)
    ax.text(0.15, 0.9415, "design limit for MV feeder, 0.94 pu", fontsize=8, va="bottom")
    ax.text(l - 0.1, v_l[-1] - 0.002, f"{v_l[-1]:.3f} pu\n({100 * d:.2f} % drop)", ha="right", va="top",
            fontsize=8, color=COLORS[1])
    ax.text(l - 0.1, v_u[-1] + 0.003, f"{v_u[-1]:.3f} pu ({100 * d / 2:.2f} % drop)", ha="right",
            va="bottom", fontsize=8, color=COLORS[0])
    ax.text(0.25, 0.912, f"Losses at 3 MW, PF 0.9 lagging:\nlumped  {loss_l:.1f} kW\nuniform  {loss_u:.1f} kW",
            fontsize=8, va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#BBBBBB", lw=0.7))
    ax.set_xlim(0, l)
    ax.set_ylim(0.90, 1.02)
    ax.set_xlabel("Distance from substation $s$ (km)")
    ax.set_ylabel("Voltage (pu)")
    ax.grid(True, lw=0.5)
    ax.legend(loc="upper right", fontsize=8)
    save(fig, CH, "fig-22-4-feeder-voltage-profile")


# ----------------------------------------------------------------------------
# Figure 22.5 — voltage band from substation to last customer
# ----------------------------------------------------------------------------
def fig_22_5():
    # schematic x: 0 busbar; 0.3–4.3 feeder (8 km); 4.3–5.3 transformer; 5.3–8.3 LV (300 m); 8.3 customer
    xf0, xf1, xt1, xl1 = 0.3, 4.3, 5.3, 8.3
    u = np.linspace(0, 1, 100)

    def profile(vbus, dfeed, vafter_tap, vafter_tr, dlv, shape_lv):
        x = [np.array([0, xf0])]
        v = [np.array([vbus, vbus])]
        x.append(xf0 + u * (xf1 - xf0))
        v.append(vbus - dfeed * (2 * u - u ** 2))          # distributed load (or generation)
        vend = vbus - dfeed
        x.append(np.array([xf1, xf1 + 0.15, xt1]))
        v.append(np.array([vend, vafter_tap, vafter_tr]))
        x.append(xt1 + u * (xl1 - xt1))
        v.append(vafter_tr - dlv * shape_lv(u))
        x.append(np.array([xl1, xl1 + 0.4]))
        v.append(np.array([vafter_tr - dlv, vafter_tr - dlv]))
        return np.concatenate(x), np.concatenate(v)

    xp, vp = profile(1.03, 0.044, 0.986 * 1.025, 0.99, 0.05, lambda u: 2 * u - u ** 2)
    xn, vn = profile(1.01, -0.005, 1.015 * 1.025, 1.04, -0.035, lambda u: u ** 1.5)

    fig, ax = new_fig(6.6, 4.0)
    ax.axhspan(0.90, 1.10, color="#E6F2E6", zorder=0)
    ax.text(0.1, 1.103, "EN 50160 band 0.90–1.10 pu", fontsize=8, color="#2E7D32", va="bottom")
    ax.axhline(1.0, color="#999999", lw=0.6)
    ax.plot(xp, vp, color=COLORS[0], label="evening peak (OLTC with LDC)")
    ax.plot(xn, vn, color=COLORS[1], ls="--", label="noon minimum load, rooftop PV exporting")
    for xs in (xf0, xf1, xt1, xl1):
        ax.axvline(xs, color="#BBBBBB", lw=0.7, zorder=0)
    pts = [(0.15, 1.03, "1.03", "bottom", COLORS[0]), (xt1 + 0.12, 0.993, "0.99", "bottom", COLORS[0]),
           (xl1 + 0.2, 0.94, "0.94", "top", COLORS[0]),
           (0.15, 1.01, "1.01", "top", COLORS[1]), (xt1, 1.04, "1.04", "bottom", COLORS[1]),
           (xl1 + 0.2, 1.075, "1.075", "bottom", COLORS[1])]
    for x, y, t, va, c in pts:
        ax.text(x, y + (0.003 if va == "bottom" else -0.003), t, ha="center", va=va, fontsize=7.5, color=c)
    ax.text((xf0 + xf1) / 2, 0.955, "feeder drop 4.4 %", ha="center", fontsize=7.5, color=COLORS[0])
    ax.text((xt1 + xl1) / 2 + 0.2, 0.932, "LV drop 5 %", ha="center", fontsize=7.5, color=COLORS[0])
    ax.text((xt1 + xl1) / 2 - 0.3, 1.067, "LV rise 3.5 %", ha="center", fontsize=7.5, color=COLORS[1])
    ax.text((xf1 + xt1) / 2 + 0.1, 0.962, "transformer\ndrop 2 %", ha="center", fontsize=7, color=COLORS[0])
    ax.text(xf1 - 0.08, 0.983, "0.986", ha="right", va="top", fontsize=7.5, color=COLORS[0])
    ax.annotate("+2.5 % off-circuit tap (to 1.01)", xy=(xf1 + 0.08, 0.999), xytext=(xf1 - 0.25, 1.024),
                ha="right", va="center", fontsize=7.5, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.7))
    ax.set_xlim(0, xl1 + 0.4)
    ax.set_ylim(0.88, 1.12)
    ax.set_xticks([xf0 / 2, (xf0 + xf1) / 2, (xf1 + xt1) / 2, (xt1 + xl1) / 2, xl1 + 0.2])
    ax.set_xticklabels(["11 kV\nbusbar", "11 kV feeder\n(0–8 km)", "11/0.4 kV\ntransformer",
                        "LV main\n(0–300 m)", "last\ncustomer"], fontsize=8)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Voltage (pu)")
    ax.legend(loc="lower left", fontsize=8, bbox_to_anchor=(0.0, 0.0))
    save(fig, CH, "fig-22-5-voltage-band-profile")


# ----------------------------------------------------------------------------
# Figure 22.6 — planning load forecast
# ----------------------------------------------------------------------------
def fig_22_6():
    yr = np.linspace(2025, 2045, 801)
    tau = (yr - 2025) / 20
    low = 18 * 1.01 ** (yr - 2025)
    central = 18 + 13 * tau ** 1.5
    step = np.clip((yr - 2031.5) / 0.5, 0, 1) * 6
    high = 18 + 14 * tau ** 1.5 + step
    firm, inst = 26.0, 40.0
    fig, ax = new_fig(6.4, 3.9)
    ax.plot(yr, low, color=COLORS[2], label="low: 1 %/yr")
    ax.plot(yr, central, color=COLORS[0], label="central: EV and heat-pump growth")
    ax.plot(yr, high, color=COLORS[1], label="high: central + 6 MVA data centre (2032)")
    ax.axhline(firm, color=INK, lw=1.3)
    ax.axhline(inst, color=INK, lw=1.0, ls="--")
    ax.text(2025.2, firm + 0.3, "N−1 firm capacity 26 MVA\n(1.3 × 20 MVA cyclic rating)", fontsize=8, va="bottom")
    ax.text(2025.2, inst - 0.3, "installed 2 × 20 MVA = 40 MVA", fontsize=8, va="top")
    for curve, c in ((central, COLORS[0]), (high, COLORS[1])):
        i = np.argmax(curve >= firm)
        y0 = yr[i]
        ax.plot([y0], [firm], "o", color=c, ms=6, zorder=5)
        ax.annotate(f"crosses firm\ncapacity ≈ {y0:.0f}", xy=(y0, firm), xytext=(y0 + (0.6 if c == COLORS[0] else -1.2), 20.2),
                    fontsize=8, color=c, ha="left" if c == COLORS[0] else "right",
                    arrowprops=dict(arrowstyle="-", color=c, lw=0.7))
    for curve, c in ((low, COLORS[2]), (central, COLORS[0]), (high, COLORS[1])):
        ax.text(2045.2, curve[-1], f"{curve[-1]:.0f}", va="center", fontsize=8, color=c)
    ax.set_xlim(2025, 2045)
    ax.set_ylim(10, 42)
    ax.set_xticks(range(2025, 2046, 5))
    ax.set_xlabel("Year")
    ax.set_ylabel("Peak demand (MVA)")
    ax.grid(True, lw=0.5)
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.9))
    save(fig, CH, "fig-22-6-planning-load-forecast")


if __name__ == "__main__":
    fig_22_1()
    fig_22_2()
    fig_22_3()
    fig_22_4()
    fig_22_5()
    fig_22_6()
