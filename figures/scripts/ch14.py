"""Figures for Chapter 14 — Conventional Generation.

Run from the repository root:  python figures/scripts/ch14.py
"""
import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy.interpolate import PchipInterpolator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, box, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

CH = "14"
BLUE, VERM, GREEN, PINK, ORANGE, SKY = COLORS[:6]
STEAM, WATER, CW, GAS, BLEED = VERM, BLUE, SKY, "#888888", ORANGE


# ---------------------------------------------------------------- drawing helpers
def path(ax, pts, color=INK, lw=1.3, arrow_end=True, ls="-", zorder=2):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="butt", zorder=zorder)
    if arrow_end:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        ax.annotate("", xy=(x1, y1), xytext=(x0 + 0.85 * (x1 - x0), y0 + 0.85 * (y1 - y0)),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9,
                                    shrinkA=0, shrinkB=0), zorder=zorder)


def mid_arrow(ax, x0, y0, x1, y1, color=INK, lw=1.3):
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    ax.annotate("", xy=(xm + 0.01 * (x1 - x0), ym + 0.01 * (y1 - y0)), xytext=(xm - 0.15 * (x1 - x0), ym - 0.15 * (y1 - y0)),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9, shrinkA=0, shrinkB=0))


def gen(ax, x, y, r=0.38, label=None, fs=8):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=5))
    t = np.linspace(-1, 1, 40)
    ax.plot(x + 0.55 * r * t, y + 0.25 * r * np.sin(np.pi * t), color=INK, lw=1.0, zorder=6)
    if label:
        ax.text(x, y - r - 0.1, label, ha="center", va="top", fontsize=fs)


def xfmr(ax, x, y, r=0.26, vertical=True, lw=1.1):
    d = 0.62 * r
    c = [(x, y + d), (x, y - d)] if vertical else [(x - d, y), (x + d, y)]
    for cx, cy in c:
        ax.add_patch(Circle((cx, cy), r, fc="none", ec=INK, lw=lw, zorder=5))
    return r + d


def cb(ax, x, y, s=0.3, fc=INK):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=fc, ec=INK, lw=1.0, zorder=6))


def busbar(ax, x0, x1, y, lw=3.0, color=INK):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, solid_capstyle="butt", zorder=4)


def line(ax, xs, ys, lw=1.1, color=INK, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def pump(ax, x, y, r=0.22, fc="white"):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=1.0, zorder=6))
    ax.add_patch(Polygon([[x - 0.6 * r, y - 0.5 * r], [x - 0.6 * r, y + 0.5 * r], [x + 0.75 * r, y]],
                         closed=True, fc=INK, ec=INK, zorder=7))


def heater(ax, x, y, label, r=0.24, fc="#FFF4E0"):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=1.0, zorder=6))
    ax.text(x, y, label, ha="center", va="center", fontsize=6.0, zorder=7)


def zigzag(ax, x0, x1, y0, y1, n=4, color=INK):
    xs = np.linspace(x0, x1, 2 * n + 1)
    ys = np.where(np.arange(2 * n + 1) % 2 == 0, y0, y1)
    ax.plot(xs, ys, color=color, lw=1.0, zorder=4)


def turbine(ax, x0, x1, yc, h0, h1, label, fc="#E7EEF6"):
    """Trapezoid: height h0 at inlet x0, h1 at exhaust x1."""
    ax.add_patch(Polygon([[x0, yc - h0 / 2], [x1, yc - h1 / 2], [x1, yc + h1 / 2], [x0, yc + h0 / 2]],
                         closed=True, fc=fc, ec=INK, lw=1.1, zorder=5))
    ax.text((x0 + x1) / 2, yc, label, ha="center", va="center", fontsize=7.5, zorder=6)


def lp_turbine(ax, x0, x1, yc, hm, he, label, fc="#E7EEF6"):
    """Double-flow LP turbine: inlet in the middle (height hm), exhausts at both ends (height he)."""
    xm = (x0 + x1) / 2
    ax.add_patch(Polygon([[x0, yc - he / 2], [xm, yc - hm / 2], [x1, yc - he / 2], [x1, yc + he / 2],
                          [xm, yc + hm / 2], [x0, yc + he / 2]], closed=True, fc=fc, ec=INK, lw=1.1, zorder=5))
    ax.text(xm, yc, label, ha="center", va="center", fontsize=7.5, zorder=6)


# ---------------------------------------------------------------- Figure 14.1
def fig_14_1():
    """660 MW ultra-supercritical steam unit: water-steam cycle, flue gas and electrical connection."""
    fig, ax = schematic(6.8, 5.2, xlim=(0, 17), ylim=(0, 13.0))
    fs = 7.0
    # boiler
    bx0, bx1, by0, by1 = 0.3, 2.5, 4.6, 11.5
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fc="#FBEFE6", ec=INK, lw=1.2, zorder=1))
    ax.text((bx0 + bx1) / 2, 8.25, "Boiler", ha="center", va="center", fontsize=7.6, fontweight="bold")
    zigzag(ax, 0.55, 1.35, 10.0, 11.1, n=3, color=STEAM)
    ax.text(0.95, 9.75, "RH", ha="center", va="top", fontsize=fs)
    zigzag(ax, 1.5, 2.3, 10.0, 11.1, n=3, color=STEAM)
    ax.text(1.9, 9.75, "SH", ha="center", va="top", fontsize=fs)
    zigzag(ax, 1.5, 2.3, 7.0, 7.7, n=3, color=WATER)
    ax.text(1.9, 6.9, "ECO", ha="center", va="top", fontsize=fs)
    ax.text(0.85, 6.0, "Furnace", ha="center", va="center", fontsize=fs, rotation=90)
    for k in range(3):   # flame
        xf = 0.75 + 0.18 * k
        ax.add_patch(Polygon([[xf - 0.08, 5.0], [xf + 0.08, 5.0], [xf, 5.45 + 0.1 * (k % 2)]], fc=ORANGE, ec="none"))
    # turbines on one shaft
    yc = 9.9
    ax.plot([3.1, 11.4], [yc, yc], color=INK, lw=1.0, zorder=3)
    turbine(ax, 3.2, 4.4, yc, 0.7, 1.2, "HP")
    turbine(ax, 4.8, 6.2, yc, 0.9, 1.5, "IP")
    lp_turbine(ax, 6.65, 8.65, yc, 0.7, 1.7, "LP-A")
    lp_turbine(ax, 8.95, 10.95, yc, 0.7, 1.7, "LP-B")
    ax.add_patch(Rectangle((11.4, 9.35), 1.35, 1.1, fc="#E3F2EA", ec=INK, lw=1.1, zorder=5))
    ax.text(12.07, 9.9, "G", ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=6)
    ax.text(12.07, 9.25, "776 MVA\n22 kV", ha="center", va="top", fontsize=6.6)
    # main steam and reheat
    path(ax, [(1.9, 11.1), (1.9, 11.9), (3.0, 11.9), (3.0, yc), (3.2, yc)], color=STEAM, lw=1.6)
    ax.text(3.1, 11.8, "main steam\n27 MPa\n600 °C", ha="left", va="top", fontsize=6.4, color=STEAM)
    path(ax, [(0.95, 11.1), (0.95, 12.55), (4.65, 12.55), (4.65, yc), (4.8, yc)], color=STEAM, lw=1.6)
    ax.text(4.75, 12.6, "hot reheat 5 MPa, 620 °C", ha="left", va="bottom", fontsize=fs, color=STEAM)
    path(ax, [(4.2, 9.35), (4.2, 8.75), (bx1, 8.75)], color=STEAM, lw=1.3, arrow_end=True)
    line(ax, [bx1, 0.95, 0.95], [8.75, 8.75, 10.0], color=STEAM, lw=1.0, ls=":")
    ax.text(4.3, 8.5, "cold reheat", ha="left", va="center", fontsize=6.6, color=STEAM)
    # crossover IP -> LP
    path(ax, [(6.0, 10.55), (6.0, 11.3), (9.95, 11.3), (9.95, 10.25)], color=STEAM, lw=1.3)
    path(ax, [(7.65, 11.3), (7.65, 10.25)], color=STEAM, lw=1.3)
    ax.text(8.8, 11.38, "crossover", ha="center", va="bottom", fontsize=fs, color=STEAM)
    # condenser under LP-B, LP-A exhaust ducted across
    cx0, cx1, cy0, cy1 = 9.2, 12.3, 6.5, 7.7
    ax.add_patch(Polygon([[9.15, 9.15], [10.75, 9.15], [10.9, cy1], [9.35, cy1]], fc="#DDE6EE", ec=INK,
                         lw=0.9, zorder=2))
    ax.add_patch(Polygon([[8.15, 9.2], [8.6, 9.2], [9.6, 8.1], [9.6, 7.7], [9.2, 7.7], [8.15, 8.9]],
                         fc="#DDE6EE", ec=INK, lw=0.9, zorder=2))
    ax.add_patch(Rectangle((cx0, cy0), cx1 - cx0, cy1 - cy0, fc="#CFE3F3", ec=INK, lw=1.1, zorder=3))
    ax.text((cx0 + cx1) / 2 + 0.1, (cy0 + cy1) / 2, "Condenser\n5 kPa (32.9 °C)", ha="center", va="center",
            fontsize=fs, zorder=4)
    # cooling tower
    tx = np.linspace(-1, 1, 50)
    prof = 0.75 + 0.55 * tx ** 2
    ty = 2.4 + (tx + 1) / 2 * 3.6
    tc = 14.9
    ax.add_patch(Polygon(np.r_[np.c_[tc - (prof[::-1] * 1.2 + 0.1), ty[::-1]], np.c_[tc + prof * 1.2 + 0.1, ty]],
                         closed=True, fc="#F2F2F2", ec=INK, lw=1.1, zorder=2))
    ax.text(tc, 4.6, "Natural-\ndraught\ncooling\ntower", ha="center", va="center", fontsize=fs)
    for k in range(3):
        ax.plot(tc - 0.5 + 0.5 * k + 0.12 * np.sin(np.linspace(0, 6, 30)), np.linspace(6.15, 6.9, 30),
                color="#AAAAAA", lw=0.9)
    path(ax, [(cx1, 7.35), (tc, 7.35), (tc, 5.7)], color=CW, lw=1.5)
    ax.text(12.4, 7.42, "CW out 30 °C", ha="left", va="bottom", fontsize=6.6, color="#2E7FB0")
    path(ax, [(tc - 1.25, 2.6), (12.75, 2.6), (12.75, 6.85), (cx1, 6.85)], color=CW, lw=1.5)
    pump(ax, 12.75, 4.3)
    ax.text(12.5, 3.3, "CW in\n20 °C", ha="right", va="center", fontsize=6.6, color="#2E7FB0")
    # feedwater train (right to left at y = yw)
    yw = 3.75
    pump(ax, 10.3, 5.3)
    ax.text(10.6, 5.3, "CP", ha="left", va="center", fontsize=6.4)
    line(ax, [10.3, 10.3], [cy0, 5.52], color=WATER, lw=1.3)
    path(ax, [(10.3, 5.08), (10.3, yw), (8.55, yw)], color=WATER, lw=1.3)
    hx = {"H1": 8.3, "H2": 7.7, "H3": 7.1, "H4": 6.45, "H6": 4.15, "H7": 3.55, "H8": 2.95}
    xda, xbfp = 5.6, 4.85
    line(ax, [hx["H8"], hx["H1"]], [yw, yw], color=WATER, lw=1.3)
    for k, x in hx.items():
        heater(ax, x, yw, k)
    ax.add_patch(Rectangle((xda - 0.38, yw + 0.35), 0.76, 0.45, fc="#FFF4E0", ec=INK, lw=1.0, zorder=6))
    ax.text(xda, yw + 0.575, "DA", ha="center", va="center", fontsize=6.0, zorder=7)
    line(ax, [xda, xda], [yw, yw + 0.35], color=WATER, lw=1.3)
    pump(ax, xbfp, yw, fc="#FFF4E0")
    ax.text(xbfp, yw - 0.32, "BFP", ha="center", va="top", fontsize=6.4)
    path(ax, [(hx["H8"] - 0.24, yw), (2.1, yw), (2.1, by0)], color=WATER, lw=1.4)
    line(ax, [2.1, 2.1], [by0, 7.0], color=WATER, lw=1.0, ls=":")
    ax.text(5.0, 3.2, "H1–H4 LP heaters, DA deaerator, H6–H8 HP heaters", ha="center", va="top",
            fontsize=6.4, color=WATER)
    # bleed lines
    bl = dict(color=BLEED, lw=0.9, ls=(0, (3, 2)), zorder=1)
    for k in ("H1", "H2", "H3"):
        ax.plot([hx[k], hx[k]], [yc - 0.55, yw + 0.24], **bl)
    ax.plot([6.1, 6.45, 6.45], [yc - 0.5, yc - 0.85, yw + 0.24], **bl)        # IP exhaust -> H4
    ax.plot([xda, xda], [yc - 0.5, yw + 0.8], **bl)                            # IP -> DA
    ax.plot([5.0, 4.15, 4.15], [yc - 0.42, yc - 1.2, yw + 0.24], **bl)          # IP -> H6
    ax.plot([3.55, 3.55], [yc - 0.38, yw + 0.24], **bl)                         # HP -> H7
    ax.plot([2.95, 2.95], [8.75, yw + 0.24], **bl)                              # cold reheat -> H8
    ax.text(7.7, 6.4, "bleed\nsteam", ha="center", va="center", fontsize=6.6, color="#B07000",
            bbox=dict(fc="white", ec="none", pad=0.5))
    # flue-gas path
    yg = 1.15
    path(ax, [(0.75, by0), (0.75, yg + 0.45)], color=GAS, lw=2.0)
    items = [(0.3, 1.25, "SCR"), (1.55, 2.6, "Air\nheater"), (2.9, 4.4, "ESP")]
    for x0, x1, lab in items:
        ax.add_patch(Rectangle((x0, yg - 0.45), x1 - x0, 0.9, fc="#EEEEEE", ec=INK, lw=1.0, zorder=3))
        ax.text((x0 + x1) / 2, yg, lab, ha="center", va="center", fontsize=6.6, zorder=4)
    for xa, xb in ((1.25, 1.55), (2.6, 2.9), (4.4, 4.8), (5.32, 5.6)):
        path(ax, [(xa, yg), (xb, yg)], color=GAS, lw=2.0)
    ax.add_patch(Circle((5.05, yg), 0.27, fc="white", ec=INK, lw=1.0, zorder=4))
    ax.text(5.05, yg, "ID", ha="center", va="center", fontsize=6.2, zorder=5)
    ax.add_patch(Rectangle((5.6, yg - 0.6), 1.35, 1.35, fc="#EEEEEE", ec=INK, lw=1.0, zorder=3))
    ax.text(6.27, yg + 0.07, "FGD\nabsorber", ha="center", va="center", fontsize=6.0, zorder=4)
    path(ax, [(6.95, yg), (7.37, yg)], color=GAS, lw=2.0)
    ax.add_patch(Polygon([[7.35, 0.3], [7.85, 0.3], [7.75, 2.7], [7.45, 2.7]], fc="#DDDDDD", ec=INK, lw=1.0))
    ax.text(7.95, 2.45, "stack", ha="left", va="center", fontsize=6.6)
    ax.text(0.3, 0.25, "flue gas", ha="left", va="bottom", fontsize=6.6, color="#666666")
    # electrical side
    ye = yc
    line(ax, [12.75, 13.35], [ye, ye], lw=2.6)
    ax.text(13.05, ye + 0.12, "IPB", ha="center", va="bottom", fontsize=6.4)
    cb(ax, 13.55, ye, s=0.32)
    ax.text(13.55, ye + 0.25, "GCB", ha="center", va="bottom", fontsize=6.4)
    line(ax, [13.7, 14.45], [ye, ye], lw=1.4)
    ax.add_patch(Circle((14.1, ye), 0.06, fc=INK, zorder=7))
    xfmr(ax, 14.75, ye, r=0.27, vertical=False)
    ax.text(14.75, ye + 0.38, "GSU\n22/400 kV", ha="center", va="bottom", fontsize=6.4)
    path(ax, [(15.07, ye), (16.4, ye)], color=INK, lw=1.4)
    ax.text(16.45, ye, "400 kV", ha="left", va="center", fontsize=6.8)
    line(ax, [14.1, 14.1], [ye, 9.25], lw=1.2)
    xfmr(ax, 14.1, 8.85, r=0.22)
    line(ax, [14.1, 14.1], [8.45, 8.15], lw=1.2)
    busbar(ax, 13.5, 14.7, 8.15, lw=2.4)
    ax.text(14.5, 8.85, "UAT\n22/11 kV", ha="left", va="center", fontsize=6.4)
    ax.text(14.8, 8.15, "11 kV unit board", ha="left", va="center", fontsize=6.4)
    # legend
    lx, ly = 9.0, 2.2
    for k, (lab, c, ls_, lw_) in enumerate([("steam", STEAM, "-", 1.6), ("water", WATER, "-", 1.4),
                                           ("bleed steam", BLEED, (0, (3, 2)), 1.0),
                                           ("cooling water", CW, "-", 1.5), ("flue gas", GAS, "-", 2.0)]):
        yy = ly - 0.42 * k
        ax.plot([lx, lx + 0.6], [yy, yy], color=c, ls=ls_, lw=lw_)
        ax.text(lx + 0.75, yy, lab, ha="left", va="center", fontsize=6.6)
    save(fig, CH, "fig-14-1-steam-plant-schematic")


# ---------------------------------------------------------------- Figure 14.2
def brayton(T1, rp=20.0, T3=1600.0, eta_c=0.88, eta_t=0.90, g=1.4):
    """Air-standard Brayton cycle of the §14.2 worked example: (net work per kg, efficiency)."""
    r = rp ** ((g - 1) / g)
    T2 = T1 + T1 * (r - 1) / eta_c
    T4 = T3 - eta_t * T3 * (1 - 1 / r)
    w = (T3 - T4) - (T2 - T1)
    return w, w / (T3 - T2)


def fig_14_2():
    """Gas-turbine output and heat rate relative to ISO versus inlet temperature."""
    fig, ax = new_fig(6.4, 3.9)
    T = np.linspace(-10, 45, 300)
    # rating curves through the manufacturer-style points of the text
    out = PchipInterpolator([-10, -5, 0, 15, 25, 35, 40, 45],
                            [1.125, 1.10, 1.075, 1.0, 0.93, 0.86, 0.82, 0.785])(T)
    hr = PchipInterpolator([-10, 0, 15, 25, 35, 40, 45], [0.985, 0.99, 1.0, 1.012, 1.03, 1.04, 1.05])(T)
    cap = 1.10
    out_c = np.minimum(out, cap)
    Tcap = T[np.argmin(np.abs(out - cap))]  # ≈ −5 °C
    ax.plot(T, out_c, color=BLUE, label="Output (left axis)")
    ax.plot(T[T < Tcap], out[T < Tcap], color=BLUE, lw=0.9, ls=":")
    ax.text(-9.5, cap - 0.008, "flat-rated below −5 °C:\ngenerator or compressor\nlimit 1.10", fontsize=7.8,
            color=BLUE, va="top")
    # air-standard model check (worked example, §14.2)
    w0, e0 = brayton(288.15)
    Tm = np.array([15, 25, 35, 40, 45])
    om = [brayton(273.15 + t)[0] / w0 * 288.15 / (273.15 + t) for t in Tm]
    ax.plot(Tm, om, "o", mfc="white", mec=BLUE, ms=4.5, label="Air-standard model (§14.2)")
    ax.set(xlim=(-10, 45), ylim=(0.75, 1.15), xlabel="Compressor inlet temperature (°C)",
           ylabel="Output relative to ISO rating")
    ax.axvline(15, color="#777777", lw=0.9, ls="--")
    ax.text(15.6, 0.765, "ISO 3977-2\nrating point (15 °C)", fontsize=7.8, va="bottom")
    # evaporative cooling recovery at 35 °C
    o35 = float(np.interp(35, T, out))
    ax.annotate("", xy=(35, o35 + 0.065), xytext=(35, o35),
                arrowprops=dict(arrowstyle="simple,head_width=0.9,head_length=0.7,tail_width=0.45",
                                fc="#9BD3B5", ec=GREEN, lw=0.8))
    ax.text(35.9, o35 + 0.05, "evaporative cooling\nrecovers ≈ 5–8 %", fontsize=7.8, color="#1E6B47",
            va="center")
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(T, hr, color=VERM, ls="--", label="Heat rate (right axis)")
    ax2.set_ylim(0.97, 1.06)
    ax2.set_ylabel("Heat rate relative to ISO")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=8, bbox_to_anchor=(0.0, 0.1))
    save(fig, CH, "fig-14-2-gas-turbine-ambient-correction")


# ---------------------------------------------------------------- Figure 14.3
def flow_arrow(ax, x0, y0, x1, y1, text, color, width, ha="center", va="bottom", dx=0, dy=0.1, fs=7.4):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=f"simple,head_width={1.6 * width},head_length={1.1 * width},"
                                           f"tail_width={width}", fc=color, ec="none", alpha=0.85),
                zorder=8)
    if text:
        ax.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, text, ha=ha, va=va, fontsize=fs, color=INK, zorder=9)


def fig_14_3():
    """1-on-1 combined-cycle unit, energy flows per 100 units of fuel, HRSG T-Q inset."""
    fig, ax = schematic(6.8, 5.3, xlim=(0, 17), ylim=(0, 13.2))
    ys = 8.0
    # 400 kV busbar
    busbar(ax, 0.5, 16.5, 12.6, lw=3.2)
    ax.text(16.5, 12.75, "400 kV", ha="right", va="bottom", fontsize=7.6)
    # gas turbine
    gen(ax, 1.0, ys, r=0.45)
    ax.text(1.0, ys - 0.55, "G1", ha="center", va="top", fontsize=7.6, fontweight="bold")
    ax.plot([1.45, 6.4], [ys, ys], color=INK, lw=1.0, zorder=3)
    ax.add_patch(Polygon([[1.9, ys - 0.85], [3.3, ys - 0.4], [3.3, ys + 0.4], [1.9, ys + 0.85]], fc="#E7EEF6",
                         ec=INK, lw=1.1, zorder=5))
    ax.text(2.6, ys, "C", ha="center", va="center", fontsize=8, zorder=6)
    ax.add_patch(Polygon([[4.9, ys - 0.4], [6.3, ys - 0.85], [6.3, ys + 0.85], [4.9, ys + 0.4]], fc="#F6E3D8",
                         ec=INK, lw=1.1, zorder=5))
    ax.text(5.6, ys, "T", ha="center", va="center", fontsize=8, zorder=6)
    ax.add_patch(Rectangle((3.6, ys + 0.75), 1.0, 0.7, fc="#FBD9C4", ec=INK, lw=1.0, zorder=5))
    ax.text(4.1, ys + 1.1, "CC", ha="center", va="center", fontsize=7, zorder=6)
    line(ax, [3.3, 3.75, 3.75], [ys + 0.3, ys + 0.3, ys + 0.75], lw=1.0)
    line(ax, [4.45, 4.45, 4.9], [ys + 0.75, ys + 0.3, ys + 0.3], lw=1.0)
    ax.text(3.6, ys - 0.95, "gas turbine", ha="center", va="top", fontsize=7.2)
    flow_arrow(ax, 4.1, 10.9, 4.1, ys + 1.48, "fuel 100", ORANGE, 0.55, ha="left", dx=0.3, dy=0)
    # GT generator to bus
    flow_arrow(ax, 1.0, ys + 0.5, 1.0, 10.7, "", "#7FB5DC", 0.5)
    ax.text(1.35, 9.35, "40", ha="left", va="center", fontsize=8.5, fontweight="bold", color=BLUE)
    xfmr(ax, 1.0, 11.3, r=0.25)
    line(ax, [1.0, 1.0], [11.6, 12.6], lw=1.2)
    ax.text(1.35, 11.3, "GSU 1", ha="left", va="center", fontsize=7)
    # exhaust to HRSG
    flow_arrow(ax, 6.35, ys, 7.3, ys, "", "#BBBBBB", 0.6)
    ax.text(6.75, ys + 0.45, "exhaust\n620 °C\n60", ha="center", va="bottom", fontsize=7.0)
    hx0, hx1, hy0, hy1 = 7.3, 12.5, 7.0, 9.0
    ax.add_patch(Rectangle((hx0, hy0), hx1 - hx0, hy1 - hy0, fc="#F4F4F4", ec=INK, lw=1.2, zorder=2))
    secs = [(7.5, 9.2, "HP", "17 MPa", VERM), (9.4, 10.9, "IP", "3 MPa", ORANGE), (11.0, 12.3, "LP", "0.4 MPa", BLUE)]
    for x0, x1, nm, p, c in secs:
        zigzag(ax, x0, x1, hy0 + 0.3, hy1 - 0.3, n=4, color=c)
        xm = (x0 + x1) / 2
        ax.add_patch(Rectangle((xm - 0.45, hy1 + 0.35), 0.9, 0.42, fc="white", ec=INK, lw=1.0, zorder=5))
        line(ax, [xm, xm], [hy1, hy1 + 0.35], lw=0.9)
        ax.text(xm, hy1 + 0.9, f"{nm} drum\n{p}", ha="center", va="bottom", fontsize=6.8)
    ax.text((hx0 + hx1) / 2, hy0 - 0.12, "triple-pressure reheat HRSG", ha="center", va="top", fontsize=7.2)
    # stack
    ax.add_patch(Polygon([[12.5, hy0], [13.1, hy0], [13.0, 10.6], [12.6, 10.6]], fc="#DDDDDD", ec=INK, lw=1.0))
    flow_arrow(ax, 12.8, 10.65, 12.8, 11.9, "", "#BBBBBB", 0.35)
    ax.text(12.45, 11.35, "stack 85 °C\nloss 6", ha="right", va="center", fontsize=7.2)
    # steam turbine
    yst = 4.3
    line(ax, [9.0, 9.0], [hy0, yst + 0.55], lw=1.6, color=VERM)
    ax.annotate("", xy=(9.0, yst + 0.55), xytext=(9.0, yst + 1.2),
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.4, mutation_scale=10))
    ax.text(8.85, 5.95, "steam", ha="right", va="center", fontsize=7.2, color=VERM)
    ax.plot([8.6, 14.0], [yst, yst], color=INK, lw=1.0, zorder=3)
    turbine(ax, 8.7, 9.7, yst, 0.6, 0.9, "HP")
    turbine(ax, 9.95, 11.0, yst, 0.75, 1.1, "IP")
    lp_turbine(ax, 11.25, 12.85, yst, 0.6, 1.4, "LP")
    gen(ax, 14.4, yst, r=0.45)
    ax.text(14.4, yst - 0.55, "G2", ha="center", va="top", fontsize=7.6, fontweight="bold")
    ax.text(10.8, yst + 0.85, "steam turbine", ha="center", va="bottom", fontsize=7.2)
    flow_arrow(ax, 14.4, yst + 0.5, 14.4, 10.7, "", "#7FB5DC", 0.38)
    ax.text(14.75, 7.6, "19", ha="left", va="center", fontsize=8.5, fontweight="bold", color=BLUE)
    xfmr(ax, 14.4, 11.3, r=0.25)
    line(ax, [14.4, 14.4], [11.6, 12.6], lw=1.2)
    ax.text(14.75, 11.3, "GSU 2", ha="left", va="center", fontsize=7)
    # condenser and other losses
    ax.add_patch(Rectangle((11.0, 2.0), 2.1, 0.8, fc="#CFE3F3", ec=INK, lw=1.0))
    ax.text(12.05, 2.4, "condenser", ha="center", va="center", fontsize=7)
    line(ax, [12.05, 12.05], [yst - 0.7, 2.8], lw=1.0)
    flow_arrow(ax, 13.1, 2.4, 15.6, 2.4, "condenser 32", SKY, 0.6, dy=0.3)
    flow_arrow(ax, 9.2, yst - 0.5, 9.2, 2.6, "", "#CCCCCC", 0.22)
    ax.text(9.45, 2.75, "other\nlosses 3", ha="left", va="center", fontsize=7.2)
    # T-Q inset of the HRSG
    ia = fig.add_axes([0.08, 0.06, 0.40, 0.33])
    Qt = 54.0
    Q = np.linspace(0, Qt, 200)
    Tg = 85 + (620 - 85) * Q / Qt
    wq = [0, 8, 11, 17, 20, 27.76, 38, 54]
    wt = [40, 144, 144, 234, 234, 352, 352, 585]
    ia.plot(Q, Tg, color=GAS, lw=1.6, label="gas")
    ia.plot(wq, wt, color=BLUE, lw=1.4, label="water/steam")
    ia.annotate("", xy=(27.76, 352), xytext=(27.76, 360),
                arrowprops=dict(arrowstyle="<->", color=VERM, lw=0.9, mutation_scale=6, shrinkA=0, shrinkB=0))
    ia.annotate("pinch 8 K", xy=(27.76, 356), xytext=(30.5, 250), fontsize=7, color=VERM,
                arrowprops=dict(arrowstyle="-", color=VERM, lw=0.7))
    for qa, qb, Ts, lab in ((8, 11, 144, "LP"), (17, 20, 234, "IP"), (27.76, 38, 352, "HP")):
        ia.text((qa + qb) / 2, Ts + 12, lab, ha="center", va="bottom", fontsize=6.5, color=BLUE)
    ia.text(53, 625, "620 °C", ha="right", va="bottom", fontsize=6.5)
    ia.annotate("85 °C", xy=(0.3, 85), xytext=(5, 15), fontsize=6.5,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ia.set_xlim(0, 54)
    ia.set_ylim(0, 700)
    ia.set_xlabel("Heat transferred (units of fuel)", fontsize=7)
    ia.set_ylabel("T (°C)", fontsize=7)
    ia.tick_params(labelsize=6.5)
    ia.legend(fontsize=6.5, loc="upper left")
    ia.set_title("HRSG temperature–heat diagram (illustrative)", fontsize=7.2, loc="left")
    save(fig, CH, "fig-14-3-combined-cycle-energy-flow")


# ---------------------------------------------------------------- Figure 14.4
def fig_14_4():
    """Hydro turbine application ranges with lines of constant power."""
    fig, ax = new_fig(6.4, 4.6)
    regions = [  # name, Q range, H range, colour, label position
        ("Pelton", (0.1, 60), (200, 1800), VERM, (0.35, 900)),
        ("Francis", (1, 1000), (20, 700), BLUE, (8, 300)),
        ("Kaplan", (2, 1000), (2, 70), GREEN, (8, 10)),
        ("Bulb / pit", (50, 1000), (2, 25), PINK, (230, 3.2)),
        ("Cross-flow", (0.05, 10), (2, 200), ORANGE, (0.3, 20)),
    ]
    ax.set(xscale="log", yscale="log", xlim=(0.1, 1000), ylim=(1, 2000))
    for name, (q0, q1), (h0, h1), c, (lx, ly) in regions:
        ax.add_patch(Rectangle((q0, h0), q1 - q0, h1 - h0, fc=c, alpha=0.07, ec="none"))
        ax.add_patch(Rectangle((q0, h0), q1 - q0, h1 - h0, fc="none", ec=c, lw=1.6))
        ax.text(lx, ly, name, ha="center", va="center", fontsize=9, color=c, fontweight="bold")
    q = np.logspace(-1, 3, 200)
    fig.canvas.draw()
    p0 = ax.transData.transform((1, 1000))
    p1 = ax.transData.transform((10, 100))
    ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
    for P in (1, 10, 100, 1000):
        H = P * 1000 / (8.5 * q)
        ax.plot(q, H, color="#555555", lw=0.9, ls="--")
        Hl = 450.0 if P < 1000 else 300.0
        ql = P * 1000 / (8.5 * Hl)
        ax.text(ql, Hl, f"{P:,} MW", fontsize=7.6, color="#333333", rotation=ang, ha="center", va="center",
                rotation_mode="anchor", bbox=dict(fc="white", ec="none", pad=0.4))
    Pw = 9.81 * 120 * 172.8 * 0.93 * 0.985 / 1000
    ax.plot(120, 172.8, "o", color=INK, ms=6, zorder=6)
    ax.annotate(f"worked example\nQ = 120 m³/s, H = 172.8 m\nP = {Pw:.0f} MW", xy=(120, 172.8), xytext=(140, 900),
                fontsize=7.8, ha="center", arrowprops=dict(arrowstyle="-", color=INK, lw=0.8),
                bbox=dict(fc="white", ec="#999999", pad=2.5, lw=0.6))
    ax.set(xscale="log", yscale="log", xlim=(0.1, 1000), ylim=(1, 2000),
           xlabel="Flow per unit Q (m³/s)", ylabel="Net head H (m)")
    ax.text(0.11, 1.15, "dashed: P = 8.5 Q H kW", fontsize=7.6, color="#333333")
    save(fig, CH, "fig-14-4-hydro-turbine-selection")


# ---------------------------------------------------------------- Figure 14.5
def fig_14_5():
    """Capability curve of a 776 MVA, 0.85 pf, 22 kV turbo-generator."""
    S, pf, Xd = 776.0, 0.85, 2.0
    Pr, Qr = S * pf, S * np.sqrt(1 - pf ** 2)
    qc = -S / Xd                                    # field-limit centre (-V^2/Xd)
    Rf = np.hypot(Qr - qc, Pr)                      # field-limit radius (Eq_max V / Xd)
    Pmin = 260.0
    uel = lambda P: -250 + (-180 + 250) / 640 * P  # noqa: E731
    fig, ax = new_fig(6.4, 5.0)
    th = np.linspace(0, np.pi, 400)
    ax.plot(S * np.cos(th), S * np.sin(th), color=BLUE, lw=1.2, label="stator-current limit (776 MVA)")
    ax.plot(qc + Rf * np.cos(th), Rf * np.sin(th), color=VERM, lw=1.2, label="field-current limit")
    ax.plot([-450, 700], [Pr, Pr], color=INK, lw=1.2, label="turbine maximum (660 MW)")
    ax.plot([-450, 700], [Pmin, Pmin], color=INK, lw=1.0, ls="--", label="minimum stable load (260 MW)")
    Pu = np.linspace(0, Pr, 50)
    ax.plot(uel(Pu), Pu, color=GREEN, lw=1.4, label="under-excitation / end-region limit")
    # permitted region
    P = np.linspace(0, Pr, 300)
    qmax = np.minimum(np.sqrt(S ** 2 - P ** 2), qc + np.sqrt(Rf ** 2 - P ** 2))
    qmin = uel(P)
    ax.fill_betweenx(P, qmin, qmax, where=P >= Pmin, color=BLUE, alpha=0.22, lw=0)
    ax.fill_betweenx(P, qmin, qmax, where=P <= Pmin, color=BLUE, alpha=0.08, lw=0)
    ax.text(150, 460, "continuous\noperating region", ha="center", va="center", fontsize=8.5)
    ax.text(150, 130, "start-up and\nshutdown only", ha="center", va="center", fontsize=8, color="#555555")
    ax.plot(Qr, Pr, "o", color=INK, ms=6, zorder=6)
    ax.annotate(f"rated point\nP = {Pr:.0f} MW, Q = {Qr:.0f} Mvar\n(pf 0.85 lagging)", xy=(Qr, Pr),
                xytext=(560, 715), fontsize=7.8, ha="center", arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.plot(qc, 0, "x", color=VERM, ms=6, clip_on=False, zorder=6)
    ax.text(qc + 10, 15, f"field-limit centre\n−V²/X$_d$ = {qc:.0f} Mvar", fontsize=7.4, color=VERM, va="bottom")
    ax.axvline(0, color="#999999", lw=0.7)
    ax.set(xlim=(-450, 700), ylim=(0, 820),
           xlabel="Reactive power Q (Mvar)      ← leading (absorbing)  |  lagging (supplying) →",
           ylabel="Active power P (MW)")
    ax.legend(loc="upper center", fontsize=7.4, bbox_to_anchor=(0.5, -0.16), ncol=2)
    save(fig, CH, "fig-14-5-generator-capability-curve")
    return Rf, Rf / (S / Xd) / Xd * Xd


# ---------------------------------------------------------------- Figure 14.6
def motor(ax, x, y, r=0.22, label=None, fs=5.9):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.text(x, y, "M", ha="center", va="center", fontsize=6.2, zorder=6)
    if label:
        ax.text(x, y - r - 0.08, label, ha="center", va="top", fontsize=fs)


def hop(ax, x, y, r=0.16, color=INK, lw=1.1):
    """Horizontal line at y crossing a vertical line at x: draw a semicircular hop."""
    t = np.linspace(np.pi, 0, 20)
    ax.plot(x + r * np.cos(t), y + r * np.sin(t), color=color, lw=lw, zorder=4)
    ax.plot([x - r, x + r], [y, y], color="white", lw=lw + 1.5, zorder=3)


def fig_14_6():
    """Auxiliary power single-line diagram of a 660 MW unit."""
    fig, ax = schematic(6.8, 5.6, xlim=(0, 17), ylim=(0.3, 14.2))
    fs = 6.4
    yb = 8.8                                           # 11 kV boards
    # generator chain (horizontal, top left)
    yg = 12.9
    gen(ax, 0.75, yg, r=0.42)
    ax.text(0.75, yg - 0.5, "G\n776 MVA\n22 kV", ha="center", va="top", fontsize=fs)
    line(ax, [1.17, 2.9], [yg, yg], lw=2.2)
    cb(ax, 1.8, yg, s=0.32)
    ax.text(1.8, yg + 0.25, "GCB", ha="center", va="bottom", fontsize=fs)
    ax.add_patch(Circle((2.6, yg), 0.07, fc=INK, zorder=7))
    xfmr(ax, 3.3, yg, r=0.3, vertical=False)
    ax.text(3.3, yg + 0.4, "GSU\n22/400 kV\n800 MVA", ha="center", va="bottom", fontsize=fs)
    line(ax, [3.67, 4.4], [yg, yg], lw=1.2)
    ax.plot([4.4, 4.4], [yg - 0.7, yg + 0.7], color=INK, lw=3.2, solid_capstyle="butt")
    ax.text(4.55, yg + 0.55, "400 kV", ha="left", va="center", fontsize=fs)
    # UAT
    line(ax, [2.6, 2.6], [yg, 11.95], lw=1.2)
    xfmr(ax, 2.6, 11.55, r=0.26)
    ax.text(2.95, 11.55, "UAT 22/11 kV\n50 MVA", ha="left", va="center", fontsize=fs)
    yu = 10.25
    line(ax, [2.6, 2.6], [11.15, yu], lw=1.2)
    # station transformer
    ax.plot([11.2, 13.8], [13.6, 13.6], color=INK, lw=3.2, solid_capstyle="butt")
    ax.text(13.9, 13.6, "132 kV grid", ha="left", va="center", fontsize=fs)
    line(ax, [12.5, 12.5], [13.6, 12.35], lw=1.2)
    xfmr(ax, 12.5, 11.95, r=0.26)
    ax.text(12.85, 11.95, "ST 132/11 kV\n50 MVA", ha="left", va="center", fontsize=fs)
    ys_ = 10.85
    line(ax, [12.5, 12.5], [11.55, ys_], lw=1.2)
    # boards: A, C, B, D
    boards = {"A": (0.3, 4.5, "Unit board A"), "C": (5.0, 7.9, "Station board C"),
              "B": (8.4, 12.6, "Unit board B"), "D": (13.1, 16.0, "Station board D")}
    inc = {"A": 2.8, "C": 7.75, "B": 11.0, "D": 15.85}
    for k, (x0, x1, lab) in boards.items():
        busbar(ax, x0, x1, yb, lw=3.4)
        ax.text(x0, yb + 0.12, lab, ha="left", va="bottom", fontsize=fs, fontweight="bold")
    # UAT secondary to A and B, ST secondary to C and D
    line(ax, [2.6, inc["B"]], [yu, yu], lw=1.2)
    for k in ("A", "B"):
        line(ax, [inc[k], inc[k]], [yu, yb], lw=1.2)
        cb(ax, inc[k], yb + 0.75, s=0.26)
    line(ax, [inc["C"], inc["D"]], [ys_, ys_], lw=1.2)
    for k in ("C", "D"):
        line(ax, [inc[k], inc[k]], [ys_, yb], lw=1.2)
        cb(ax, inc[k], yb + 0.75, s=0.26)
    hop(ax, inc["C"], yu)
    # bus ties (normally open)
    for (k1, k2) in (("A", "C"), ("B", "D")):
        xa, xb = boards[k1][1], boards[k2][0]
        line(ax, [xa, xb], [yb, yb], lw=1.1)
        cb(ax, (xa + xb) / 2, yb, s=0.26, fc="white")
    ax.text(5.6, 11.3, "All boards 11 kV. Bus ties A–C and B–D\nnormally open (white); auto-transfer\n"
            "closes them on loss of the UAT supply", ha="left", va="bottom", fontsize=fs, style="italic",
            bbox=dict(fc="#FFF6E0", ec="#C9A24A", lw=0.6, pad=2))
    # loads (labels rotated so that 0.66-unit spacing stays legible)
    fl = fs - 0.3
    ym = 6.83

    def drop(x, y_end):
        line(ax, [x, x], [yb, y_end], lw=1.0)
        cb(ax, x, yb - 0.4, s=0.22)

    def vlabel(x, y, text):
        ax.text(x, y, text, ha="center", va="top", fontsize=fl, rotation=90)

    def mload(x, text):
        drop(x, ym + 0.22)
        motor(ax, x, ym)
        vlabel(x, ym - 0.32, text)

    def tx_bus(x, text, y_bus=6.75):
        drop(x, 7.85)
        xfmr(ax, x, 7.55, r=0.2)
        line(ax, [x, x], [7.23, y_bus], lw=1.0)
        ax.plot([x - 0.28, x + 0.28], [y_bus, y_bus], color=INK, lw=2.2, solid_capstyle="butt")
        vlabel(x, y_bus - 0.12, text)

    for side, x0 in (("A", 0.3), ("B", 8.4)):
        xs = x0 + 0.45 + 0.66 * np.arange(6)
        if side == "A":          # boiler feed pump A with variable-frequency drive
            drop(xs[0], 7.8)
            ax.add_patch(Rectangle((xs[0] - 0.22, 7.35), 0.44, 0.44, fc="white", ec=INK, lw=0.9, zorder=5))
            ax.plot([xs[0] - 0.22, xs[0] + 0.22], [7.35, 7.79], color=INK, lw=0.7, zorder=6)
            ax.text(xs[0] - 0.11, 7.66, "~", fontsize=5.5, ha="center", va="center", zorder=6)
            ax.text(xs[0] + 0.11, 7.47, "~", fontsize=5.5, ha="center", va="center", zorder=6)
            line(ax, [xs[0], xs[0]], [7.35, ym + 0.22], lw=1.0)
            motor(ax, xs[0], ym)
            vlabel(xs[0], ym - 0.32, "BFP A 10 MW (VFD)")
        else:
            mload(xs[0], "BFP B 10 MW")
        for x, lab in zip(xs[1:5], ["ID fan 4 MW", "FD fan 2 MW", "CW pump 3 MW", "Mills 3 × 0.8 MW"]):
            mload(x, lab)
        tx_bus(xs[5], "LV tx → MCC")
    # station board C: third CW pump, FGD board, essential supply
    xc = 5.0 + np.array([0.45, 1.25, 2.3])
    mload(xc[0], "CW pump 3 MW")
    tx_bus(xc[1], "11/0.69 kV → FGD")
    drop(xc[2], 7.85)
    xfmr(ax, xc[2], 7.55, r=0.2)
    ax.text(xc[2] + 0.27, 7.55, "LV tx", ha="left", va="center", fontsize=fl)
    # station board D
    xd = 13.1 + np.array([0.6, 1.4])
    tx_bus(xd[0], "LV tx → MCC")
    mload(xd[1], "other station loads")
    # essential 415 V board
    ye = 3.6
    line(ax, [xc[2], xc[2]], [7.23, ye], lw=1.0)
    cb(ax, xc[2], 4.3, s=0.22)
    busbar(ax, 3.9, 8.1, ye, lw=3.0, color=VERM)
    ax.text(3.8, ye, "Essential\n415 V board", ha="right", va="center", fontsize=fs, fontweight="bold",
            color=VERM)
    xe = 4.6                                            # emergency diesel generator
    line(ax, [xe, xe], [ye, 2.7], lw=1.0)
    cb(ax, xe, 3.2, s=0.22)
    gen(ax, xe, 2.3, r=0.38)
    ax.text(xe, 1.8, "EDG\n2 MW", ha="center", va="top", fontsize=fs)
    xu = 6.0                                            # UPS
    line(ax, [xu, xu], [ye, 2.75], lw=1.0)
    ax.add_patch(Rectangle((xu - 0.4, 1.95), 0.8, 0.8, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.text(xu, 2.35, "UPS", ha="center", va="center", fontsize=fs, zorder=6)
    line(ax, [xu, xu], [1.95, 1.5], lw=1.0)
    ax.text(xu, 1.42, "I&C, DCS", ha="center", va="top", fontsize=fs)
    xb = 7.5                                            # battery charger, 220 V DC
    line(ax, [xb, xb], [ye, 2.75], lw=1.0)
    ax.add_patch(Rectangle((xb - 0.4, 1.95), 0.8, 0.8, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.plot([xb - 0.4, xb + 0.4], [1.95, 2.75], color=INK, lw=0.8, zorder=6)
    ax.text(xb - 0.18, 2.55, "~", ha="center", va="center", fontsize=6, zorder=6)
    ax.text(xb + 0.18, 2.13, "=", ha="center", va="center", fontsize=6, zorder=6)
    ax.text(xb + 0.5, 2.35, "charger", ha="left", va="center", fontsize=fl)
    line(ax, [xb, xb], [1.95, 1.4], lw=1.0)
    ax.plot([xb - 0.7, xb + 0.7], [1.4, 1.4], color=INK, lw=2.2, solid_capstyle="butt")
    ax.text(xb + 0.8, 1.4, "220 V DC", ha="left", va="center", fontsize=fs)
    for k in range(3):   # battery cells
        xx = xb - 0.3 + 0.3 * k
        ax.plot([xx, xx], [0.65, 1.05], color=INK, lw=1.4)
        ax.plot([xx + 0.12, xx + 0.12], [0.75, 0.95], color=INK, lw=2.4)
    line(ax, [xb, xb], [1.4, 1.05], lw=1.0)
    ax.text(xb + 0.6, 0.85, "battery", ha="left", va="center", fontsize=fs)
    ax.text(10.0, 2.7, "LV tx = 2.5 MVA, 11/0.415 kV transformer\n"
            "Essential loads: turning gear, lube-oil pumps,\nemergency lighting, controls",
            ha="left", va="center", fontsize=fs, color="#555555")
    save(fig, CH, "fig-14-6-auxiliary-power-single-line")


if __name__ == "__main__":
    fig_14_1()
    fig_14_2()
    fig_14_3()
    fig_14_4()
    print(fig_14_5())
    fig_14_6()
