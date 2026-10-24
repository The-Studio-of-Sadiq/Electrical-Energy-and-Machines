"""Figures for Chapter 5 — DC Machines.

Run from the repository root:  python figures/scripts/ch05.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle, FancyArrowPatch  # noqa: E402
from scipy.interpolate import PchipInterpolator  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

from figstyle import new_fig, save, COLORS, INK  # noqa: E402

BLUE, ORANGE, GREEN, PINK, YELLOW, SKY = COLORS[:6]
STEEL = "#B9BEC4"
STEEL2 = "#D5D9DD"
COPPER = "#E3A869"


def _farrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, ms=10, z=4):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms, color=color,
                                 lw=lw, shrinkA=0, shrinkB=0, zorder=z))


def _pol(r, deg):
    a = np.radians(deg)
    return r * np.cos(a), r * np.sin(a)


# ---------------------------------------------------------------------------
# Figure 5.1
# ---------------------------------------------------------------------------
def _pole_polygon(ang, r_face, r_shoe, half_arc, half_body, r_root):
    """Pole (shoe + body) centred on angle ang (deg); radii in mm."""
    pts = []
    # shoe face arc
    for a in np.linspace(ang - half_arc, ang + half_arc, 30):
        pts.append(_pol(r_face, a))
    # shoe outer edge to body (body has constant width half_body in mm)
    def body_pt(r, side):
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        return (r * c - side * half_body * s, r * s + side * half_body * c)
    pts.append(_pol(r_shoe, ang + half_arc))
    pts.append(body_pt(r_shoe, +1))
    pts.append(body_pt(r_root, +1))
    pts.append(body_pt(r_root, -1))
    pts.append(body_pt(r_shoe, -1))
    pts.append(_pol(r_shoe, ang - half_arc))
    return Polygon(pts, closed=True)


def fig_5_1():
    """Four-pole DC machine cross-section with interpoles and compensating winding."""
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_aspect("equal")
    ax.axis("off")
    R_out, R_yoke = 400, 340          # frame
    R_arm = 225                       # armature radius (450 mm diameter)
    gap = 10                          # 3 mm gap drawn as 10 mm for clarity
    R_face = R_arm + gap
    # yoke
    ax.add_patch(Wedge((0, 0), R_out, 0, 360, width=R_out - R_yoke, fc=STEEL, ec=INK, lw=1.0))
    # main poles and field coils
    poles = [(0, "N"), (90, "S"), (180, "N"), (270, "S")]
    for ang, name in poles:
        p = _pole_polygon(ang, R_face, R_face + 28, 31, 62, R_yoke + 2)
        p.set(fc=STEEL, ec=INK, lw=1.0)
        ax.add_patch(p)
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        for side in (+1, -1):
            # field coil cross-section beside the pole body
            r0, r1 = R_face + 40, R_yoke - 6
            off0, off1 = 64, 98
            pts = [(r0 * c - side * off0 * s, r0 * s + side * off0 * c),
                   (r1 * c - side * off0 * s, r1 * s + side * off0 * c),
                   (r1 * c - side * off1 * s, r1 * s + side * off1 * c),
                   (r0 * c - side * off1 * s, r0 * s + side * off1 * c)]
            ax.add_patch(Polygon(pts, closed=True, fc=COPPER, ec=INK, lw=0.6))
        x, y = _pol(R_face + 62, ang)
        ax.text(x, y, name, ha="center", va="center", fontsize=12, fontweight="bold", color=INK)
        # compensating conductors in the pole face (current opposite to the armature beneath)
        for da in (-22, -11, 0, 11, 22):
            x, y = _pol(R_face + 13, ang + da)
            ax.add_patch(Circle((x, y), 6.5, fc="white", ec=INK, lw=0.7, zorder=3))
            if name == "N":     # armature under N carries dots -> compensating carries crosses
                ax.plot([x - 4, x + 4], [y - 4, y + 4], color=INK, lw=0.7, zorder=4)
                ax.plot([x - 4, x + 4], [y + 4, y - 4], color=INK, lw=0.7, zorder=4)
            else:
                ax.plot(x, y, "o", color=INK, ms=1.6, zorder=4)
    # interpoles
    for ang in (45, 135, 225, 315):
        p = _pole_polygon(ang, R_face, R_face + 8, 6.5, 24, R_yoke + 2)
        p.set(fc=STEEL, ec=INK, lw=0.9)
        ax.add_patch(p)
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        for side in (+1, -1):
            r0, r1 = R_face + 30, R_yoke - 20
            pts = [(r0 * c - side * 26 * s, r0 * s + side * 26 * c), (r1 * c - side * 26 * s, r1 * s + side * 26 * c),
                   (r1 * c - side * 44 * s, r1 * s + side * 44 * c), (r0 * c - side * 44 * s, r0 * s + side * 44 * c)]
            ax.add_patch(Polygon(pts, closed=True, fc="#F0C9A0", ec=INK, lw=0.5))
    # armature with 36 slots
    ax.add_patch(Circle((0, 0), R_arm, fc=STEEL2, ec=INK, lw=1.0))
    for k in range(36):
        ang = 10 * k
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        hw = 7
        r0, r1 = R_arm - 34, R_arm
        pts = [(r0 * c - hw * s, r0 * s + hw * c), (r1 * c - hw * s, r1 * s + hw * c),
               (r1 * c + hw * s, r1 * s - hw * c), (r0 * c + hw * s, r0 * s - hw * c)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.5))
        x, y = _pol(R_arm - 16, ang)
        ax.add_patch(Circle((x, y), 6, fc="white", ec=INK, lw=0.6, zorder=3))
        a = ang % 360
        under_N = (a < 45 or a > 315) or (135 < a < 225)
        if under_N:
            ax.plot(x, y, "o", color=INK, ms=1.6, zorder=4)
        else:
            ax.plot([x - 3.6, x + 3.6], [y - 3.6, y + 3.6], color=INK, lw=0.6, zorder=4)
            ax.plot([x - 3.6, x + 3.6], [y + 3.6, y - 3.6], color=INK, lw=0.6, zorder=4)
    # commutator (shown projected) with brushes on the interpolar axes
    ax.add_patch(Circle((0, 0), 112, fc="white", ec=INK, lw=0.8, ls="--"))
    ax.add_patch(Circle((0, 0), 92, fc=COPPER, ec=INK, lw=0.8))
    for k in range(36):
        x0, y0 = _pol(62, 5 + 10 * k)
        x1, y1 = _pol(92, 5 + 10 * k)
        ax.plot([x0, x1], [y0, y1], color=INK, lw=0.4)
    ax.add_patch(Circle((0, 0), 62, fc="white", ec=INK, lw=0.6))
    ax.add_patch(Circle((0, 0), 38, fc="#888888", ec=INK, lw=0.6))
    for ang, sgn in zip((45, 135, 225, 315), ("+", "−", "+", "−")):
        c, s = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        r0, r1, hw = 92, 112, 9
        pts = [(r0 * c - hw * s, r0 * s + hw * c), (r1 * c - hw * s, r1 * s + hw * c),
               (r1 * c + hw * s, r1 * s - hw * c), (r0 * c + hw * s, r0 * s - hw * c)]
        ax.add_patch(Polygon(pts, closed=True, fc="#444444", ec=INK, lw=0.5, zorder=3))
        x, y = _pol(124, ang)
        ax.text(x, y, sgn, ha="center", va="center", fontsize=9, fontweight="bold")
    # main flux paths (dashed): N pole -> gap -> armature -> gap -> S pole -> yoke -> N pole
    def loop(a_n, a_s, r_arm_path, r_yoke_path):
        pts = []
        sgn = np.sign(a_s - a_n)
        for r in np.linspace(R_yoke - 5, R_face - 5, 10):
            pts.append(_pol(r, a_n))
        for r in np.linspace(R_face - 5, r_arm_path, 6):
            pts.append(_pol(r, a_n))
        for a in np.linspace(a_n, a_s, 40):
            pts.append(_pol(r_arm_path, a))
        for r in np.linspace(r_arm_path, R_yoke - 5, 10):
            pts.append(_pol(r, a_s))
        for r in np.linspace(R_yoke - 5, r_yoke_path, 4):
            pts.append(_pol(r, a_s))
        for a in np.linspace(a_s, a_n, 40):
            pts.append(_pol(r_yoke_path, a))
        for r in np.linspace(r_yoke_path, R_yoke - 5, 4):
            pts.append(_pol(r, a_n))
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], color=BLUE, lw=1.0, ls=(0, (4, 2.5)), zorder=5)
        # arrows: inward on the N-pole leg, along the armature, outward on the S leg
        xa, ya = _pol(R_face + 18, a_n)
        xb, yb = _pol(R_face - 22, a_n)
        _farrow(ax, xa, ya, xb, yb, color=BLUE, lw=1.0, ms=8, z=6)
        am = (a_n + a_s) / 2
        xa, ya = _pol(r_arm_path, am - 3 * sgn)
        xb, yb = _pol(r_arm_path, am + 3 * sgn)
        _farrow(ax, xa, ya, xb, yb, color=BLUE, lw=1.0, ms=8, z=6)
        xa, ya = _pol(r_yoke_path, am + 3 * sgn)
        xb, yb = _pol(r_yoke_path, am - 3 * sgn)
        _farrow(ax, xa, ya, xb, yb, color=BLUE, lw=1.0, ms=8, z=6)

    for a_n, a_s in [(0, 90), (0, -90), (180, 90), (180, 270)]:
        d = 1 if a_s > a_n else -1
        loop(a_n + 7 * d, a_s - 7 * d, 160, 370)
    # labels
    fs = 8.5
    lab = dict(fontsize=fs, ha="left", va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("yoke", xy=_pol(385, 62), xytext=(330, 430), **lab)
    ax.annotate("main pole", xy=_pol(R_face + 70, 96), xytext=(-120, 450), ha="right", va="center", fontsize=fs,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("field winding", xy=_pol(R_face + 70, 112), xytext=(-330, 430), ha="right", va="center",
                fontsize=fs, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("interpole", xy=_pol(R_face + 60, 135), xytext=(-450, 300), ha="right", va="center", fontsize=fs,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("compensating\nwinding", xy=_pol(R_face + 13, 191), xytext=(-460, -80), ha="right", va="center",
                fontsize=fs, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("air gap\n(3 mm, enlarged)", xy=_pol(R_arm + 5, 205), xytext=(-460, -250), ha="right",
                va="center", fontsize=fs, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("armature\n(36 slots)", xy=_pol(170, 240), xytext=(-330, -440), ha="right", va="center",
                fontsize=fs, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("commutator\n(projected)", xy=_pol(80, 290), xytext=(90, -470), **lab)
    ax.annotate("brush", xy=_pol(105, 315), xytext=(360, -440), **lab)
    ax.annotate("main flux", xy=_pol(370, 20), xytext=(440, 140), color=BLUE, fontsize=fs, ha="left",
                va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    ax.annotate("armature conductor\n(• under N, × under S)", xy=_pol(R_arm - 16, 350), xytext=(440, -150),
                **lab)
    ax.set_xlim(-640, 660)
    ax.set_ylim(-580, 480)
    ax.text(0, -578, "frame 800 mm o.d., armature 450 mm dia.; brushes on the geometric neutral axes",
            fontsize=7.5, ha="center", va="bottom")
    return save(fig, "05", "fig-5-1-dc-machine-cross-section")


# ---------------------------------------------------------------------------
# Figure 5.2
# ---------------------------------------------------------------------------
def _developed(ax, n, span, yc, pole_centres, coil_seg, seg_x, brushes, coil_path, path_colors, title):
    """Generic developed winding: n slots, coils of slot span `span`, commutator pitch yc."""
    y_top, y_bot = 4.5, 2.1
    y_seg0, y_seg1 = 1.05, 1.45
    pitch = n / 4.0
    # pole faces (shaded behind the active conductors)
    for k, xc in enumerate(pole_centres):
        for shift in (0, -n, n):
            x0 = xc - 0.35 * pitch + shift
            ax.add_patch(Rectangle((x0, y_bot - 0.1), 0.7 * pitch, y_top - y_bot + 0.2,
                                   fc="#D9534F" if k % 2 == 0 else "#5B8DD6", alpha=0.13, ec="none", zorder=0))
        ax.text(xc, y_top + 0.78, "N" if k % 2 == 0 else "S", ha="center", va="center", fontsize=11,
                fontweight="bold", color="#B03030" if k % 2 == 0 else "#2E5FA8")
    for j in range(n):
        c = path_colors[coil_path[j]]
        lw = 1.25 if coil_path[j] >= 0 else 0.9
        x_t = j
        x_b = j + span + 0.3
        s0 = coil_seg[j]
        xs0 = seg_x(s0)
        xs1 = seg_x(s0 + yc)
        # unwrap segment positions so that leads are short
        while xs0 - x_t > n / 2:
            xs0 -= n
        while x_t - xs0 > n / 2:
            xs0 += n
        while xs1 - x_b > n / 2:
            xs1 -= n
        while x_b - xs1 > n / 2:
            xs1 += n
        apex = (x_t + x_b) / 2
        xs = [xs0, x_t, x_t, apex, x_b, x_b, xs1]
        ys = [y_seg1, y_bot, y_top, y_top + 0.45, y_top, y_bot, y_seg1]
        for shift in (0, -n, n):
            xx = [v + shift for v in xs]
            ax.plot(xx[:4], ys[:4], color=c, lw=lw, zorder=3, solid_capstyle="round")
            ax.plot(xx[3:5], ys[3:5], color=c, lw=lw, zorder=3)
            ax.plot(xx[4:6], ys[4:6], color=c, lw=lw, ls=(0, (3, 1.5)), zorder=3)
            ax.plot(xx[5:], ys[5:], color=c, lw=lw, zorder=3)
    # slot numbers
    for j in range(n):
        ax.text(j + 0.15, y_bot - 0.28, str(j + 1), ha="center", va="center", fontsize=6.5, color="#555555", clip_on=True)
    # commutator segments
    for k in range(n):
        x = seg_x(k)
        for shift in (0, -n, n):
            ax.add_patch(Rectangle((x - 0.42 + shift, y_seg0), 0.84, y_seg1 - y_seg0, fc=COPPER, ec=INK, lw=0.6,
                                   zorder=2))
            ax.text(x + shift, (y_seg0 + y_seg1) / 2, str(k + 1), ha="center", va="center", fontsize=6.5, zorder=4,
                    clip_on=True)
    # brushes
    for xb, sgn in brushes:
        ax.add_patch(Rectangle((xb - 0.7, 0.35), 1.4, 0.55, fc="#444444", ec=INK, lw=0.6, zorder=2))
        ax.text(xb, 0.62, sgn, ha="center", va="center", color="white", fontsize=10, fontweight="bold", zorder=3)
    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(-0.75, 6.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=9.5, loc="left")


def fig_5_2():
    """Developed simplex lap (16 slots) and simplex wave (15 slots) windings, 4 poles."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 6.0))
    pc = [BLUE, ORANGE, GREEN, PINK]
    grey = "#9A9A9A"
    # ----- lap: 16 slots, coil span 4 slots (full pitch), coil ends on adjacent segments (yc = 1)
    n, span = 16, 4
    seg_x = lambda k: (k % n) + 1.65                         # noqa: E731
    coil_seg = [j for j in range(n)]
    poles = [2.15 + 4 * m for m in range(4)]
    brushes = [(2.15 + 4 * m, "+" if m % 2 == 0 else "−") for m in range(4)]
    # coil j joins segments j and j+1; brushes short segments 4m,4m+1 -> coil 4m commutating
    coil_path = [-1 if j % 4 == 0 else j // 4 for j in range(n)]
    colors = {-1: grey, 0: pc[0], 1: pc[1], 2: pc[2], 3: pc[3]}
    _developed(a1, n, span, 1, poles, coil_seg, seg_x, brushes, coil_path, colors,
               "(a) Simplex lap: 16 slots, 16 segments, coil pitch 4 slots, commutator pitch 1, a = 4")
    # dimensions
    kw = dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=7)
    a1.annotate("", xy=(poles[0], 5.55), xytext=(poles[1], 5.55), arrowprops=kw)
    a1.text((poles[0] + poles[1]) / 2, 5.62, "pole pitch (4 slots)", ha="center", va="bottom", fontsize=7.5)
    a1.annotate("", xy=(5, 2.6), xytext=(9.3, 2.6), arrowprops=kw)
    a1.text(7.15, 2.68, "coil pitch", ha="center", va="bottom", fontsize=7.5,
            bbox=dict(fc="white", ec="none", pad=0.5))
    a1.text(-0.65, -0.45, "4 parallel paths (colours); grey coils are short-circuited by the brushes (commutating)",
            fontsize=7.5, ha="left")
    # ----- wave: 15 slots, coil span 3 slots, commutator pitch 7
    n, span, yc = 15, 3, 7
    seg_x = lambda k: (k % n) + 0.15                         # noqa: E731
    coil_seg = [(j - 2) % n for j in range(n)]
    poles = [0.15 + 3.75 * m for m in range(4)]
    b1, b2 = 0, 4
    brushes = [(seg_x(b1), "+"), (seg_x(b2), "−")]
    # trace the two paths through the chain of segments k -> k+7
    coil_from = {coil_seg[j]: j for j in range(n)}
    coil_path = [0] * n
    k = b1
    while k != b2:
        j = coil_from[k]
        coil_path[j] = 0
        k = (k + yc) % n
    for j in range(n):
        pass
    path_a = set()
    k = b1
    while k != b2:
        path_a.add(coil_from[k])
        k = (k + yc) % n
    coil_path = [0 if j in path_a else 1 for j in range(n)]
    colors = {0: pc[0], 1: pc[1]}
    _developed(a2, n, span, yc, poles, coil_seg, seg_x, brushes, coil_path, colors,
               "(b) Simplex wave: 15 slots, 15 segments, coil pitch 3 slots, commutator pitch 7, a = 2")
    a2.annotate("", xy=(seg_x(7), 0.75), xytext=(seg_x(14), 0.75), arrowprops=kw)
    a2.text((seg_x(7) + seg_x(14)) / 2, 0.68, "commutator pitch $y_c$ = 7 (coil in slots 10 and 13)",
            ha="center", va="top", fontsize=7.5)
    a2.annotate("", xy=(poles[1], 5.55), xytext=(poles[2], 5.55), arrowprops=kw)
    a2.text((poles[1] + poles[2]) / 2, 5.62, "pole pitch (3.75 slots)", ha="center", va="bottom", fontsize=7.5)
    a2.text(-0.65, -0.45, f"2 parallel paths: {len(path_a)} coils (blue) and {n - len(path_a)} coils (orange) "
            "between the two brushes", fontsize=7.5, ha="left")
    fig.text(0.5, 0.005, "Top-layer coil sides solid, bottom-layer sides dashed; numbers are slots and segments.",
             ha="center", fontsize=7.5)
    fig.tight_layout(rect=(0, 0.02, 1, 1), h_pad=0.6)
    return save(fig, "05", "fig-5-2-lap-and-wave-windings")


# ---------------------------------------------------------------------------
# OCC used for Figures 5.3 and 5.4 (220 V shunt generator at 1000 rpm)
# ---------------------------------------------------------------------------
def occ(i_f, speed=1000.0):
    """OCC of the 220 V shunt generator: residual 8 V, slope 160 V/A in the linear part,
    saturating smoothly (fitted to 168 V at 1.0 A, 205 V at 1.4 A, 240 V at 2.2 A, 255 V at 3.0 A)."""
    i_f = np.asarray(i_f, dtype=float)
    u = 160.0 * i_f
    e = 8.0 + u / (1 + (np.abs(u) / 226.81) ** 3.727) ** (1 / 3.727) + 7.625 * i_f
    return e * speed / 1000.0


def docc(i_f, h=1e-5):
    return (occ(i_f + h) - occ(i_f - h)) / (2 * h)


def fig_5_3():
    """OCC, field-resistance lines and voltage build-up of a shunt generator."""
    fig, ax = new_fig(6.4, 4.2)
    i = np.linspace(0, 3, 600)
    ax.plot(i, occ(i), color=BLUE, lw=2.0, label="OCC, 1000 rpm")
    ax.plot(i, occ(i, 800), color=BLUE, lw=1.5, ls="--", label="OCC, 800 rpm")
    # field-resistance lines
    R_op, R_cr, R_hi = 100, 160, 200
    f = lambda x: occ(x) - R_op * x                       # noqa: E731
    i_op = brentq(f, 1.5, 3.0)
    v_op = R_op * i_op
    ax.plot(i, R_op * i, color=GREEN, lw=1.3)
    ax.plot(i, R_cr * i, color=ORANGE, lw=1.3)
    ax.plot(i, R_hi * i, color=PINK, lw=1.3)
    ax.text(2.97, 282, "100 Ω", color=GREEN, fontsize=9, ha="right", va="top")
    ax.text(1.86, 286, "160 Ω: critical\n(slope of linear part)", color=ORANGE, fontsize=9, ha="left", va="center")
    ax.text(1.27, 262, "200 Ω: no build-up", color=PINK, fontsize=9, ha="right", va="center")
    i_lo = brentq(lambda x: occ(x) - R_hi * x, 0.01, 1.0)
    ax.plot(i_lo, R_hi * i_lo, "o", color=PINK, ms=4)
    # staircase build-up on the 100 ohm line
    x, v = 0.0, float(occ(0))
    xs, vs = [x], [v]
    for _ in range(40):
        x = v / R_op
        xs.append(x); vs.append(v)
        v = float(occ(x))
        xs.append(x); vs.append(v)
        if abs(v - R_op * x) < 1.0:
            break
    ax.plot(xs, vs, color=INK, lw=0.8)
    for k in range(1, min(len(xs) - 1, 14), 2):
        _farrow(ax, xs[k], vs[k], xs[k + 1], vs[k + 1], color=INK, lw=0.8, ms=7)
    ax.plot(i_op, v_op, "o", color=INK, ms=6, zorder=5)
    ax.annotate(f"operating point\n{i_op:.2f} A, {v_op:.0f} V", xy=(i_op, v_op), xytext=(2.25, 140),
                fontsize=9, ha="left", arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("residual 8 V", xy=(0, 8), xytext=(0.25, 22), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("voltage build-up", xy=(1.0, 128), xytext=(1.45, 100), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 300)
    ax.set_xlabel("Field current $I_f$ (A)")
    ax.set_ylabel("Generated EMF $E_a$ (V)")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(True, lw=0.5)
    return save(fig, "05", "fig-5-3-occ-and-self-excitation")


# ---------------------------------------------------------------------------
# Figure 5.4
# ---------------------------------------------------------------------------
def _vt(V0, Rf, ra, kd, I, c=0.0, shunt=True):
    """Terminal voltage (V) at load current I (pu) from the OCC.

    Field current = V/Rf (shunt) or V0/Rf (separate), plus c*I from a series field, minus kd*I^2
    equivalent demagnetising armature reaction; armature-circuit drop ra*V0*I.
    Returns the highest stable solution, or nan if none exists.
    """
    vv = np.linspace(0.5, 1.6 * V0, 800)
    if shunt:
        g = occ(vv / Rf + c * I - kd * I ** 2) - ra * V0 * I - vv
    else:
        g = occ(V0 / Rf + c * I - kd * I ** 2) - ra * V0 * I - vv
    idx = np.where(np.diff(np.sign(g)))[0]
    if not len(idx):
        return np.nan
    j = idx[-1]
    return vv[j] - g[j] * (vv[j + 1] - vv[j]) / (g[j + 1] - g[j])


def _shunt_curve(V0, Rf, ra, kd, n=600):
    """Parametrise the shunt characteristic by terminal voltage so that the turn-back is traced."""
    Vs = np.linspace(V0, 0.0, n)
    Is = []
    for V in Vs:
        h = lambda I: occ(V / Rf - kd * I ** 2) - ra * V0 * I - V      # noqa: E731
        Is.append(brentq(h, 0.0, 10.0) if h(0.0) > 0 else 0.0)
    return np.array(Is), Vs / V0


def _fit_generator():
    """Choose Rf, ra and kd: shunt 0.88 pu at 1 pu, separately excited 0.93 pu, shunt turn-back 1.5 pu."""
    from scipy.optimize import least_squares
    xg = np.linspace(0, 5, 20001)

    def no_load(Rf):
        return float(xg[np.where(np.diff(np.sign(occ(xg) - Rf * xg)))[0][-1]] * Rf)

    def res(p):
        Rf, ra, kd = p
        V0 = no_load(Rf)
        sh = _vt(V0, Rf, ra, kd, 1.0) / V0
        se = _vt(V0, Rf, ra, kd, 1.0, shunt=False) / V0
        Is, _ = _shunt_curve(V0, Rf, ra, kd, n=200)
        return [sh - 0.88, se - 0.93, (Is.max() - 1.5) / 10]

    r = least_squares(res, [130.0, 0.05, 0.1], bounds=([100, 0.0, 0.0], [158, 0.2, 1.0]))
    Rf, ra, kd = r.x
    return no_load(Rf), Rf, ra, kd


def fig_5_4():
    """External characteristics computed from the OCC with armature-circuit drop and armature reaction."""
    # Parameters returned by _fit_generator() (fixed here so the script runs quickly):
    # shunt-field circuit 127.4 ohm (no-load 228 V), armature-circuit drop 0.0562 pu at rated
    # current, equivalent demagnetising armature reaction 0.066 A of field current per pu^2.
    V0, Rf, ra, kd = 228.1336, 127.3956, 0.0562136, 0.0660057
    I = np.linspace(0, 1.5, 151)
    I_sh, v_sh = _shunt_curve(V0, Rf, ra, kd)

    def compound(c, Iarr):
        return np.array([_vt(V0, Rf, ra, kd, Ii, c) for Ii in Iarr]) / V0

    def c_for(target):
        return brentq(lambda c: np.nan_to_num(compound(c, [1.0])[0], nan=0.0) - target, -3, 3)

    curves = {}
    for name, tgt in [("over-compound", 1.08), ("flat compound", 1.00), ("under-compound", 0.96)]:
        curves[name] = compound(c_for(tgt), I)
    # differential compound (welding-generator type): strongly saturated separately excited field
    # (4.47 A) opposed by a series field of 3.53 A per pu current, same per-unit armature drop.
    # The two field settings were chosen for 0.5 pu at rated current and 0.05 pu at 1.2 pu.
    If0, c_d = 4.47368, -3.53208
    Vd0 = float(occ(If0))
    Id = np.linspace(0, 1.5, 1501)
    v_d = (occ(If0 + c_d * Id - kd * Id ** 2) - ra * Vd0 * Id) / Vd0
    keep = v_d >= 0
    Id = np.append(Id[keep], np.interp(0.0, -v_d, Id))
    v_d = np.append(v_d[keep], 0.0)
    v_se = np.array([_vt(V0, Rf, ra, kd, Ii, shunt=False) for Ii in I]) / V0

    # series generator: V = occ(cs*I) - rs*V0*I with maximum 1.0 pu at 1.0 pu current
    def tan_int(x):
        return float(occ(x) - x * docc(x))
    cs = brentq(lambda x: tan_int(x) - V0, 1.0, 5.0)
    rs = cs * float(docc(cs)) / V0
    v_s = (occ(cs * I) - rs * V0 * I) / V0
    print(f"  5.4: Rf = {Rf:.1f} ohm, ra = {ra:.3f} pu, kd = {kd:.3f} A/pu^2, V0 = {V0:.0f} V")

    fig, ax = new_fig(6.8, 4.0)
    ax.plot(I, curves["over-compound"], color=ORANGE, label="over-compound")
    ax.plot(I, curves["flat compound"], color=GREEN, label="flat compound")
    ax.plot(I, curves["under-compound"], color=YELLOW, label="under-compound")
    ax.plot(I, v_se, color=INK, label="separately excited")
    ax.plot(I_sh, v_sh, color=BLUE, label="shunt")
    ax.plot(Id, v_d, color=PINK, label="differential compound")
    ax.plot(I, v_s, color=SKY, label="series")
    ax.axvline(1.0, color="#777777", ls=":", lw=1.0)
    ax.text(0.99, 1.17, "rated current", fontsize=8, color="#555555", ha="right", va="top")
    k = np.argmax(I_sh)
    ax.annotate("shunt turns back\n(voltage collapse)", xy=(I_sh[k], v_sh[k]), xytext=(1.08, 0.64),
                fontsize=8, color=BLUE, arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    ax.set_xlim(0, 1.55)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("Load current (pu of rated)")
    ax.set_ylabel("Terminal voltage (pu of no-load)")
    ax.legend(loc="center left", fontsize=8.5, bbox_to_anchor=(1.01, 0.5))
    ax.grid(True, lw=0.5)
    print(f"  5.4: sep-ex at 1 pu = {v_se[100]:.3f}, shunt max current = {I_sh.max():.2f} pu, "
          f"diff-comp at 1.2 pu = {np.interp(1.2, Id, v_d):.3f}, flat/over/under at 1.5 = "
          f"{curves['flat compound'][-1]:.3f}/{curves['over-compound'][-1]:.3f}/{curves['under-compound'][-1]:.3f}")
    return save(fig, "05", "fig-5-4-generator-external-characteristics")


# ---------------------------------------------------------------------------
# Figure 5.5
# ---------------------------------------------------------------------------
def fig_5_5():
    """Speed against torque for shunt, cumulative-compound and series motors (per unit)."""
    T = np.linspace(0, 2.5, 500)
    r = 0.0654                                   # armature-circuit resistance, pu (1.07 pu no-load speed)
    w_sh = (1 - r * T) / (1 - r)
    # cumulative compound: flux = (1-k) + k*I, T = flux*I, speed = (1 - r I)/((1-r) flux)
    k = 1 - 1 / (1.2 * (1 - r))
    I_c = (-(1 - k) + np.sqrt((1 - k) ** 2 + 4 * k * T)) / (2 * k)
    phi = (1 - k) + k * I_c
    w_c = (1 - r * I_c) / ((1 - r) * phi)
    # series (unsaturated): flux = I, T = I^2, speed = (1 - rs I)/((1 - rs) I)
    rs = 0.08
    Ts = np.linspace(0.12, 2.5, 500)
    Is = np.sqrt(Ts)
    w_s = (1 - rs * Is) / ((1 - rs) * Is)
    fig, ax = new_fig(6.4, 4.2)
    ax.axhspan(1.5, 2.6, color=PINK, alpha=0.10, lw=0)
    ax.text(1.55, 2.30, "series motor overspeed region:\nnever run uncoupled", fontsize=8.5, color=PINK,
            ha="left", va="center")
    ax.plot(T, w_sh, color=BLUE, label="separately excited / shunt")
    ax.plot(T, w_c, color=GREEN, label="cumulative compound")
    ax.plot(Ts, w_s, color=ORANGE, label="series")
    # fan load T = 1.6 n^2
    n = np.linspace(0, 1.25, 200)
    ax.plot(1.6 * n ** 2, n, color=INK, ls="--", lw=1.2, label=r"fan load $T\propto n^2$")
    for wv, c in [(w_sh, BLUE), (w_c, GREEN)]:
        j = np.argmin(abs(1.6 * wv ** 2 - T))
        ax.plot(T[j], wv[j], "o", color=c, ms=5)
    j = np.argmin(abs(1.6 * w_s ** 2 - Ts))
    ax.plot(Ts[j], w_s[j], "o", color=ORANGE, ms=5)
    ax.plot(1, 1, "s", color=INK, ms=6, zorder=5)
    ax.annotate("rated point (1, 1)", xy=(1, 1), xytext=(1.45, 0.35), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel("Torque (pu)")
    ax.set_ylabel("Speed (pu)")
    ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.0, 0.82))
    ax.grid(True, lw=0.5)
    print(f"  5.5: shunt at 2.5 pu = {w_sh[-1]:.3f}, compound at 2.5 = {w_c[-1]:.3f}, series at 2.5 = {w_s[-1]:.3f},"
          f" series speed 2.5 pu at T = {np.interp(-2.5, -w_s, Ts):.3f}")
    return save(fig, "05", "fig-5-5-motor-speed-torque")


# ---------------------------------------------------------------------------
# Figure 5.6
# ---------------------------------------------------------------------------
def fig_5_6():
    """(a) Mill-motor capability; (b) four-position resistor start of the 220 V shunt motor."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    # (a) 440 V, 150 kW, Ra = 0.04, Ia = 370 A, base 600 rpm
    Va, Ra, Ia = 440.0, 0.04, 370.0
    E = Va - Ia * Ra
    kphi0 = E / (600 * np.pi / 30)
    n = np.linspace(1, 1200, 600)
    w = n * np.pi / 30
    kphi = np.where(n <= 600, kphi0, E / w)
    T = kphi * Ia
    P = T * w / 1000
    a1.plot(n, T, color=BLUE, lw=2, label="torque")
    a1.set_xlim(0, 1200)
    a1.set_ylim(0, 3000)
    a1.set_xlabel("Speed (rpm)")
    a1.set_ylabel("Torque (N·m)", color=BLUE)
    a1.axvline(600, color="#888888", ls=":", lw=1)
    t1000 = kphi0 * 600 / 1000 * Ia
    a1.plot(1000, t1000, "o", color=BLUE, ms=5)
    a1.annotate(f"1000 rpm,\n{t1000:.0f} N·m", xy=(1000, t1000), xytext=(760, 750), fontsize=8,
                color=BLUE, arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    a1.text(200, 2380, "armature\nvoltage\ncontrol\n(0–440 V,\nfull field)", ha="center", va="top", fontsize=7.5)
    a1.text(900, 2700, "field weakening\n(flux 100 % → 50 %)", ha="center", fontsize=7.5)
    a1.text(300, 2504 + 60, "2504 N·m", ha="center", fontsize=7.5, color=BLUE, va="bottom")
    a1b = a1.twinx()
    a1b.spines["right"].set_visible(True)
    a1b.plot(n, P, color=ORANGE, lw=1.8, ls="--", label="power")
    a1b.set_ylim(0, 200)
    a1b.set_ylabel("Developed power (kW)", color=ORANGE)
    a1b.text(1190, 157.3 + 4, "157 kW", color=ORANGE, fontsize=7.5, ha="right", va="bottom")
    a1.set_title("(a) 150 kW, 440 V mill motor", fontsize=9.5)
    h1, l1 = a1.get_legend_handles_labels()
    h2, l2 = a1b.get_legend_handles_labels()
    a1.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=8)

    # (b) 220 V shunt motor: Ra = 0.25, E = 219.25 V per 1000 rpm, load = full-load torque (58 A)
    V, Ra = 220.0, 0.25
    ke = 219.25 / 1000                             # V per rpm
    I_load = 58.0
    I1 = 116.0
    R1 = V / I1
    ratio = (R1 / Ra) ** (1 / 3)
    Rs = [R1, R1 / ratio, R1 / ratio ** 2, Ra]
    I2 = I1 / ratio
    J = 0.6                                        # kg m^2, assumed
    kphi = ke * 30 / np.pi                         # V s/rad
    dt = 1e-4
    t, nn = 0.0, 0.0
    step = 0
    ts, Is, ns, sw = [], [], [], []
    while t < 3.0:
        R = Rs[step]
        i = (V - ke * nn) / R
        if step < 3 and i <= I2:
            step += 1
            sw.append((t, nn))
            R = Rs[step]
            i = (V - ke * nn) / R
        Tm = kphi * (i - I_load)
        nn += Tm / J * dt * 30 / np.pi
        ts.append(t); Is.append(i); ns.append(nn)
        t += dt
    ts, Is, ns = map(np.array, (ts, Is, ns))
    a2.plot(ts, Is, color=BLUE, lw=1.6, label="armature current")
    a2.set_xlim(0, 3)
    a2.set_ylim(0, 130)
    a2.set_xlabel("Time (s)")
    a2.set_ylabel("Armature current (A)", color=BLUE)
    a2.axhline(I1, color=BLUE, ls=":", lw=0.8)
    a2.axhline(I2, color=BLUE, ls=":", lw=0.8)
    a2.text(2.95, I1 + 2, f"{I1:.0f} A", color=BLUE, fontsize=7.5, ha="right", va="bottom")
    a2.text(0.03, I2 + 2, f"{I2:.0f} A", color=BLUE, fontsize=7.5, ha="left", va="bottom")
    a2b = a2.twinx()
    a2b.spines["right"].set_visible(True)
    a2b.plot(ts, ns, color=ORANGE, lw=1.6, ls="--", label="speed")
    a2b.set_ylim(0, 1300)
    a2b.set_ylabel("Speed (rpm)", color=ORANGE)
    for (tt, nv) in sw:
        a2b.plot(tt, nv, "o", color=ORANGE, ms=4)
        a2b.text(tt + 0.04, nv - 55, f"{nv:.0f}", color=ORANGE, fontsize=7.5, va="top",
                 bbox=dict(fc="white", ec="none", pad=0.3))
    a2b.text(2.95, ns[-1] + 25, f"{ns[-1]:.0f} rpm", color=ORANGE, fontsize=7.5, ha="right", va="bottom")
    a2.text(2.95, 55, "58 A (full load)", color=BLUE, fontsize=7.5, ha="right", va="top")
    a2.set_title("(b) Four-position starter, 220 V shunt motor", fontsize=9.5)
    h1, l1 = a2.get_legend_handles_labels()
    h2, l2 = a2b.get_legend_handles_labels()
    a2.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.08))
    a2.text(2.95, 3, f"J = {J} kg·m² (assumed),\nload at full-load torque", fontsize=7, ha="right", va="bottom")
    fig.tight_layout(w_pad=1.2)
    print("  5.6: switching speeds", [round(v) for _, v in sw], "final", round(ns[-1], 1), "I2", round(I2, 1))
    return save(fig, "05", "fig-5-6-capability-and-starting")


if __name__ == "__main__":
    fig_5_1()
    fig_5_2()
    fig_5_3()
    fig_5_4()
    fig_5_5()
    fig_5_6()
