"""Figures for Chapter 1 — Magnetic Circuit Fundamentals.

Run from the repository root:  python figures/scripts/ch01.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
from matplotlib.gridspec import GridSpec
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.interpolate import PchipInterpolator, RegularGridInterpolator

from figstyle import save, COLORS, INK, box, arrow

MU0 = 4e-7 * np.pi
IRON = "#C9D3DE"     # laminated iron fill
IRON_EC = "#5A6878"
FLUX = COLORS[0]

# Table 1.6 — 0.5 mm non-oriented steel (peak values)
T16_B = np.array([0.5, 0.8, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9])
T16_H = np.array([70, 100, 150, 250, 350, 600, 1500, 3500, 7000, 13000, 22000])


# ----------------------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------------------
def _flux_arrow(ax, x0, y0, x1, y1, color=FLUX, lw=1.4, ms=11):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, zorder=6))


def _reluctance(ax, xc, yc, w, h, label, vertical=True, fc="white"):
    """IEC-style rectangular reluctance symbol centred at (xc, yc)."""
    ax.add_patch(Rectangle((xc - w / 2, yc - h / 2), w, h, fc=fc, ec=INK, lw=1.3, zorder=4))


def _mmf_source(ax, xc, yc, r, up=True):
    """Circle source with + / - markings (MMF source)."""
    ax.add_patch(plt.Circle((xc, yc), r, fc="white", ec=INK, lw=1.3, zorder=4))
    ax.text(xc, yc + 0.45 * r, "+", ha="center", va="center", fontsize=10, zorder=5)
    ax.text(xc, yc - 0.48 * r, "−", ha="center", va="center", fontsize=11, zorder=5)


def solve_laplace(fixed, value, periodic_x=False):
    """Finite-difference Laplace solve on a uniform grid.

    fixed: bool array (ny, nx), True where the potential is prescribed (iron surfaces);
    value: prescribed potentials. Free edges are natural (zero normal derivative).
    """
    ny, nx = fixed.shape
    idx = -np.ones(fixed.shape, dtype=int)
    free = ~fixed
    idx[free] = np.arange(free.sum())
    n = free.sum()
    rows, cols, vals = [], [], []
    rhs = np.zeros(n)
    for j, i in zip(*np.nonzero(free)):
        k = idx[j, i]
        diag = 0.0
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jj, ii = j + dj, i + di
            if periodic_x:
                ii %= nx
            if not (0 <= jj < ny and 0 <= ii < nx):
                continue
            diag += 1.0
            if fixed[jj, ii]:
                rhs[k] += value[jj, ii]
            else:
                rows.append(k); cols.append(idx[jj, ii]); vals.append(-1.0)
        rows.append(k); cols.append(k); vals.append(diag)
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    V = value.astype(float).copy()
    V[free] = spsolve(A, rhs)
    return V


def trace_line(x0, y0, fx, fy, inside_stop, h, xlim, ylim, periodic=None, nmax=4000):
    """Trace a field line from (x0, y0) along +(fx, fy) until inside_stop(x, y) is True."""
    pts = [(x0, y0)]
    x, y = x0, y0
    for _ in range(nmax):
        def d(xx, yy):
            if periodic:
                xx = periodic[0] + (xx - periodic[0]) % (periodic[1] - periodic[0])
            gx, gy = fx((yy, xx)), fy((yy, xx))
            m = np.hypot(gx, gy) + 1e-30
            return gx / m, gy / m
        k1 = d(x, y)
        k2 = d(x + 0.5 * h * k1[0], y + 0.5 * h * k1[1])
        x, y = x + h * k2[0], y + h * k2[1]
        pts.append((x, y))
        if inside_stop(x, y) or not (xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]):
            break
    return np.array(pts)


# ----------------------------------------------------------------------------------------
# Figure 1.1 — gapped reactor and its reluctance circuit
# ----------------------------------------------------------------------------------------
def fig_1_1():
    fig = plt.figure(figsize=(6.8, 3.9))
    axa = fig.add_axes([0.0, 0.0, 0.47, 1.0])
    axb = fig.add_axes([0.50, 0.0, 0.50, 1.0])
    for ax in (axa, axb):
        ax.set_aspect("equal"); ax.axis("off")

    # (a) core, mm. Outer 160 x 210, limb 60 -> mean path 2(100 + 150) = 500 mm
    W, H, t = 160.0, 210.0, 60.0
    gdraw = 7.0                                   # gap drawn exaggerated (1.0 mm actual)
    ygap = H / 2
    ax = axa
    ax.set_xlim(-62, 205); ax.set_ylim(-30, 232)
    # yokes
    ax.add_patch(Rectangle((0, H - t), W, t, fc=IRON, ec=IRON_EC, lw=1.2))
    ax.add_patch(Rectangle((0, 0), W, t, fc=IRON, ec=IRON_EC, lw=1.2))
    # limbs, each split by a gap at mid-height
    for x in (0, W - t):
        ax.add_patch(Rectangle((x, t), t, ygap - gdraw / 2 - t, fc=IRON, ec=IRON_EC, lw=1.2))
        ax.add_patch(Rectangle((x, ygap + gdraw / 2), t, H - t - ygap - gdraw / 2, fc=IRON,
                               ec=IRON_EC, lw=1.2))
    # laminations hint (thin lines in the yokes)
    for yy in np.linspace(6, t - 6, 6):
        ax.plot([4, W - 4], [yy, yy], color="white", lw=0.5, zorder=1.5)
        ax.plot([4, W - 4], [H - t + yy, H - t + yy], color="white", lw=0.5, zorder=1.5)
    # gap labels
    ax.annotate("gap 1.0 mm\n(drawn enlarged)", xy=(W, ygap), xytext=(W + 6, ygap + 38),
                fontsize=8, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    # winding on left limb: 14 turns (drawn as conductor sections both sides of the limb)
    ywin = np.linspace(t + 8, H - t - 8, 14)
    ywin = ywin[np.abs(ywin - ygap) > 7]
    for yy in ywin:
        ax.add_patch(Rectangle((-12, yy - 3.2), 10, 6.4, fc="#E69F00", ec="#8A5A00", lw=0.6, zorder=3))
        ax.add_patch(Rectangle((t + 2, yy - 3.2), 10, 6.4, fc="#E69F00", ec="#8A5A00", lw=0.6, zorder=3))
        ax.plot(-7, yy, ".", color=INK, ms=2.5, zorder=4)            # current out of page
        ax.plot(t + 7, yy, "x", color=INK, ms=3.0, mew=0.7, zorder=4)  # current into page
    ax.text(-30, ygap + 2, "N = 14", rotation=90, ha="center", va="center", fontsize=8.5)
    # lead with current i entering at top-left
    ax.plot([-7, -7, -40], [ywin[-1] + 3, ywin[-1] + 22, ywin[-1] + 22], color="#8A5A00", lw=1.2)
    _flux_arrow(ax, -52, ywin[-1] + 22, -30, ywin[-1] + 22, color=INK, lw=1.2, ms=9)
    ax.text(-46, ywin[-1] + 29, "$i$", fontsize=10, ha="center")
    ax.plot([-7, -7, -40], [ywin[0] - 3, ywin[0] - 22, ywin[0] - 22], color="#8A5A00", lw=1.2)
    # mean path (dashed) through limb centres
    xs = [t / 2, W - t / 2, W - t / 2, t / 2, t / 2]
    ys = [t / 2, t / 2, H - t / 2, H - t / 2, t / 2]
    ax.plot(xs, ys, ls="--", color=INK, lw=0.9, zorder=2)
    ax.text(W / 2, t / 2 - 3, "mean path $l_c$ = 0.50 m", fontsize=8, ha="center", va="top")
    # flux arrows (clockwise for i entering at the top of the outer face: right-hand rule)
    _flux_arrow(ax, W / 2 - 20, H - t / 2, W / 2 + 20, H - t / 2)
    _flux_arrow(ax, W - t / 2, H - t - 12, W - t / 2, H - t - 42)
    _flux_arrow(ax, W / 2 + 20, t / 2 + 12, W / 2 - 20, t / 2 + 12)
    _flux_arrow(ax, t / 2, t + 12, t / 2, t + 42)
    ax.text(W / 2, H - t / 2 + 6, r"$\Phi$ = 6.30 mWb", color=FLUX, fontsize=9, ha="center",
            va="bottom", bbox=dict(fc=IRON, ec="none", pad=0.5))
    # dimensions
    ax.annotate("", xy=(0, H + 10), xytext=(W, H + 10),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(W / 2, H + 13, "160 mm", fontsize=8, ha="center", va="bottom")
    ax.annotate("", xy=(W + 30, 0), xytext=(W + 30, H),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(W + 34, 40, "210 mm", fontsize=8, rotation=90, va="center")
    ax.annotate("", xy=(W - t, -10), xytext=(W, -10),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(W - t / 2, -14, "60 mm", fontsize=8, ha="center", va="top")
    ax.text(0, -14, "stack depth 100 mm", fontsize=8, ha="left", va="top")
    ax.text(-60, 228, "(a)", fontsize=10, fontweight="bold", va="top")

    # (b) magnetic equivalent circuit
    ax = axb
    ax.set_xlim(0, 10); ax.set_ylim(0, 9.4)
    xl, xr, yb, yt = 2.4, 6.2, 3.6, 8.0
    ax.plot([xl, xl, xr, xr, xl], [yb, yt, yt, yb, yb], color=INK, lw=1.3, zorder=1)
    _mmf_source(ax, xl, (yb + yt) / 2, 0.55)
    ax.text(xl - 0.75, (yb + yt) / 2, "$Ni$\n1782 At", ha="right", va="center", fontsize=9)
    _reluctance(ax, (xl + xr) / 2, yt, 1.5, 0.55, "")
    ax.text((xl + xr) / 2, yt + 0.5, r"$\mathcal{R}_c$ = 1.745×10$^4$ A/Wb", ha="center",
            va="bottom", fontsize=9)
    ax.text((xl + xr) / 2, yt - 0.48, "drop 110 At", ha="center", va="top", fontsize=8.5,
            color=COLORS[1])
    _reluctance(ax, xr, (yb + yt) / 2, 0.55, 1.7, "")
    ax.text(xr + 0.45, (yb + yt) / 2 + 0.45, r"$\mathcal{R}_g$ = 2.653×10$^5$" + "\nA/Wb", ha="left",
            va="center", fontsize=9)
    ax.text(xr + 0.45, (yb + yt) / 2 - 0.65, "drop 1672 At", ha="left", va="top", fontsize=8.5,
            color=COLORS[1])
    _flux_arrow(ax, (xl + xr) / 2 - 0.7, yb, (xl + xr) / 2 + 0.7, yb, color=FLUX)
    ax.text((xl + xr) / 2, yb - 0.25, r"$\Phi$ = 6.30 mWb", ha="center", va="top", color=FLUX, fontsize=9)
    ax.text(0.1, 9.2, "(b)", fontsize=10, fontweight="bold", va="top")
    # energy shares
    box(ax, 0.6, 0.3, 8.8, 1.9,
        "Stored energy at 127 A peak: " r"$\frac{1}{2}Li^2$ = 5.62 J" "\n"
        "gaps 5.27 J (94 %),   iron 0.35 J (6 %)", fontsize=8.5, fc="#F4F6F9")
    save(fig, "01", "fig-1-1-gapped-reactor-and-reluctance-circuit")


# ----------------------------------------------------------------------------------------
# Figure 1.2 — E-I core, series-parallel network, flux sharing
# ----------------------------------------------------------------------------------------
def fig_1_2():
    # numbers of the worked example
    Ac, Ao = 2.0e-3, 1.0e-3
    Rcen = 0.060 / (MU0 * 3000 * Ac) + 0.5e-3 / (MU0 * Ac)
    Rout = 0.180 / (MU0 * 3000 * Ao)
    Rbad = Rout + 0.1e-3 / (MU0 * Ao)
    N = 200
    i = 2.0e-3 * (Rcen + Rout / 2) / N
    Rpar = Rout * Rbad / (Rout + Rbad)
    Phic = N * i / (Rcen + Rpar)
    B_left = Phic * Rout / (Rout + Rbad) / Ao
    B_right = Phic * Rbad / (Rout + Rbad) / Ao

    fig = plt.figure(figsize=(6.8, 4.9))
    axa = fig.add_axes([0.00, 0.30, 0.47, 0.70])
    axb = fig.add_axes([0.49, 0.30, 0.51, 0.70])
    axc = fig.add_axes([0.16, 0.07, 0.80, 0.17])

    # (a) geometry in mm: widths 20 | 20 | 40 | 20 | 20, window 60 high, yokes 20
    ax = axa
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-16, 138); ax.set_ylim(-34, 120)
    gc = 3.0   # centre gap drawn (0.5 mm)
    gb = 1.6   # butt gap drawn (0.1 mm)
    yj = 20.0  # E-I joint level (top of the I)
    ax.add_patch(Rectangle((0, 0), 120, 20, fc=IRON, ec=IRON_EC, lw=1.1))      # I
    ax.add_patch(Rectangle((0, 80), 120, 20, fc=IRON, ec=IRON_EC, lw=1.1))     # E back
    ax.add_patch(Rectangle((0, yj + gb), 20, 60 - gb, fc=IRON, ec=IRON_EC, lw=1.1))
    ax.add_patch(Rectangle((100, yj), 20, 60, fc=IRON, ec=IRON_EC, lw=1.1))
    ax.add_patch(Rectangle((40, yj + gc), 40, 60 - gc, fc=IRON, ec=IRON_EC, lw=1.1))
    for x0 in (22, 81):
        ax.add_patch(Rectangle((x0, 26), 17, 50, fc="#E69F00", ec="#8A5A00", lw=0.8, alpha=0.85))
    ax.text(30.5, 51, "×", ha="center", va="center", fontsize=13, color=INK)
    ax.text(89.5, 51, "•", ha="center", va="center", fontsize=15, color=INK)
    _flux_arrow(ax, 60, 34, 60, 70)
    _flux_arrow(ax, 52, 90, 22, 90)
    _flux_arrow(ax, 68, 90, 98, 90)
    _flux_arrow(ax, 10, 72, 10, 36)
    _flux_arrow(ax, 110, 72, 110, 36)
    _flux_arrow(ax, 22, 10, 52, 10)
    _flux_arrow(ax, 98, 10, 68, 10)
    ax.annotate("centre gap 0.5 mm", xy=(60, yj + gc / 2), xytext=(60, 30), fontsize=7.5,
                ha="center", va="bottom", arrowprops=dict(arrowstyle="-", lw=0.6), zorder=7,
                bbox=dict(fc=IRON, ec="none", pad=0.2))
    ax.annotate("0.1 mm butt gap\n(faulty joint)", xy=(1, yj + gb / 2), xytext=(-14, -24),
                fontsize=8, ha="left", va="center", color=COLORS[1],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9, mutation_scale=8))
    ax.text(136, -6, "N = 200 turns", ha="right", va="top", fontsize=8)
    ax.text(136, -16, "stack depth 50 mm", ha="right", va="top", fontsize=8)
    ax.text(10, 102, "20", ha="center", va="bottom", fontsize=7.5)
    ax.text(110, 102, "20", ha="center", va="bottom", fontsize=7.5)
    ax.annotate("", xy=(40, 104), xytext=(80, 104), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(60, 105, "40 mm", ha="center", va="bottom", fontsize=7.5)
    ax.annotate("", xy=(127, 20), xytext=(127, 80), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(130, 50, "60 mm", rotation=90, ha="left", va="center", fontsize=7.5)
    ax.text(-15, 119, "(a)", fontsize=10, fontweight="bold", va="top")

    # (b) reluctance network
    ax = axb
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.2, 11.6); ax.set_ylim(0.2, 10.0)
    xs, xl_, xr_ = 1.2, 5.0, 8.6
    yb, yt = 1.2, 8.6
    ym = (yb + yt) / 2
    ax.plot([xs, xs, xr_, xr_, xs], [yb, yt, yt, yb, yb], color=INK, lw=1.3)
    ax.plot([xl_, xl_], [yb, yt], color=INK, lw=1.3)
    for xx in (xl_,):
        ax.plot([xx], [yt], "o", ms=3.5, color=INK); ax.plot([xx], [yb], "o", ms=3.5, color=INK)
    _mmf_source(ax, xs, 3.0, 0.5)
    ax.text(xs - 0.65, 3.0, "$Ni$", ha="right", va="center", fontsize=9.5)
    _reluctance(ax, xs, 6.3, 0.5, 1.5, "")
    ax.text(xs - 0.4, 6.3, r"$\mathcal{R}_{cen}$" + "\n2.069×10$^5$", ha="right", va="center", fontsize=8.5)
    _reluctance(ax, xl_, ym, 0.5, 1.5, "", fc="#FBE3D3")
    ax.text(xl_ + 0.4, ym, "1.273×10$^5$", ha="left", va="center", fontsize=8.5)
    ax.text(xl_ + 0.4, ym - 1.3, "left (faulty)", ha="left", va="center", fontsize=8, color=COLORS[1])
    _reluctance(ax, xr_, ym, 0.5, 1.5, "")
    ax.text(xr_ + 0.4, ym, "4.775\n×10$^4$", ha="left", va="center", fontsize=8.5)
    ax.text(xr_ + 0.4, ym - 1.6, "right", ha="left", va="center", fontsize=8)
    _flux_arrow(ax, 2.2, yt, 3.6, yt)
    ax.text(2.9, yt + 0.25, r"$\Phi_c$", ha="center", va="bottom", color=FLUX, fontsize=9.5)
    _flux_arrow(ax, xl_, 7.7, xl_, 6.7)
    _flux_arrow(ax, xr_, 7.7, xr_, 6.7)
    ax.text(xl_ - 0.2, 7.2, "27 %", ha="right", va="center", color=FLUX, fontsize=8.5)
    ax.text(xr_ - 0.2, 7.2, "73 %", ha="right", va="center", color=FLUX, fontsize=8.5)
    ax.text(4.9, 0.55, "reluctances in A/Wb", ha="center", va="center", fontsize=8)
    ax.text(-2.1, 9.95, "(b)", fontsize=10, fontweight="bold", va="top")

    # (c) outer-limb flux densities
    ax = axc
    yy = np.array([1, 0])
    w = 0.38
    b1 = ax.barh(yy + w / 2, [1.0, 1.0], w, color=COLORS[5], label="balanced core")
    b2 = ax.barh(yy - w / 2, [B_left, B_right], w, color=COLORS[1], label="0.1 mm gap in left path")
    for bars in (b1, b2):
        for r in bars:
            ax.text(r.get_width() + 0.02, r.get_y() + r.get_height() / 2, f"{r.get_width():.2f} T",
                    ha="left", va="center", fontsize=8)
    ax.set_yticks(yy, ["left limb", "right limb"])
    ax.set_xlabel("outer-limb flux density $B$ (T)")
    ax.set_xlim(0, 1.8)
    ax.legend(fontsize=8, loc="center right", bbox_to_anchor=(1.0, 0.5))
    ax.text(-0.17, 1.12, "(c)", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
    save(fig, "01", "fig-1-2-ei-core-series-parallel")


# ----------------------------------------------------------------------------------------
# Figure 1.3 — fringing and Carter's coefficient (finite-difference field solutions)
# ----------------------------------------------------------------------------------------
def _fringing_field():
    h = 0.5
    x = np.arange(-70, 70 + h / 2, h)
    y = np.arange(-40, 40 + h / 2, h)
    X, Y = np.meshgrid(x, y)
    upper = (np.abs(X) <= 30 + 1e-9) & (Y >= 5 - 1e-9)
    lower = (np.abs(X) <= 30 + 1e-9) & (Y <= -5 + 1e-9)
    fixed = upper | lower
    val = np.where(upper, 1.0, 0.0)
    V = solve_laplace(fixed, val)
    return x, y, V, upper, lower


def _carter_field(g=0.6, pitch=15.0, bs=3.0, depth=5.0, h=0.05):
    x = np.arange(0, 2 * pitch, h)
    ytop = g + depth + 0.6
    y = np.arange(0, ytop + h / 2, h)
    X, Y = np.meshgrid(x, y)
    slot = np.zeros_like(X, dtype=bool)
    for xc in (pitch / 2, 1.5 * pitch):
        slot |= (np.abs(X - xc) < bs / 2 - 1e-9)
    stator = (Y >= g - 1e-9) & ~(slot & (Y < g + depth - 1e-9))
    rotor = Y <= 1e-9
    fixed = stator | rotor
    val = np.where(stator, 1.0, 0.0)
    V = solve_laplace(fixed, val, periodic_x=True)
    return x, y, V, stator


def fig_1_3():
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = GridSpec(3, 1, height_ratios=[1.7, 1.6, 1.25], hspace=0.32, figure=fig,
                  left=0.09, right=0.98, top=0.98, bottom=0.08)

    # (a) plain gap, 60 mm faces, g drawn as 10 mm
    x, y, V, upper, lower = _fringing_field()
    h = x[1] - x[0]
    Ey, Ex = np.gradient(V, h, h)
    fx = RegularGridInterpolator((y, x), Ex, bounds_error=False, fill_value=0.0)
    fy = RegularGridInterpolator((y, x), Ey, bounds_error=False, fill_value=0.0)
    ax = fig.add_subplot(gs[0])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-104, 66); ax.set_ylim(-25, 23)
    ax.add_patch(Rectangle((-30, 5), 60, 30, fc=IRON, ec=IRON_EC, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((-30, -35), 60, 30, fc=IRON, ec=IRON_EC, lw=1.2, zorder=3))
    # flux leaving the lower pole: equal-flux spacing along top face + sides (right half, mirrored)
    j0 = np.argmin(np.abs(y - (-5)))
    jface = j0 + 1
    i_face = np.where((x >= 0) & (x <= 30))[0]
    Bn_face = (V[jface, i_face] - V[j0, i_face]) / h
    s_face = x[i_face]
    i_side = np.argmin(np.abs(x - 30)) + 1
    j_side = np.where((y <= -5) & (y >= -40))[0][::-1]
    Bn_side = (V[j_side, i_side] - V[j_side, i_side - 1]) / h
    s_side = 30 + (-5 - y[j_side])
    s = np.concatenate([s_face, s_side[1:]])
    Bn = np.concatenate([Bn_face, Bn_side[1:]])
    cum = np.concatenate([[0], np.cumsum(0.5 * (Bn[1:] + Bn[:-1]) * np.diff(s))])
    nlines = 9
    face_flux = np.interp(30, s, cum)
    targets = (np.arange(nlines) + 0.5) / nlines * face_flux
    s_start = list(np.interp(targets, cum, s)) + [30 + d for d in (0.8, 2.5, 5.0, 8.5)]
    stop = lambda xx, yy: (abs(xx) <= 30) and (yy >= 5)
    for sgn in (1, -1):
        for ss in s_start:
            if ss <= 30:
                p0 = (sgn * ss, -5 + 0.3)
            else:
                p0 = (sgn * (30 + 0.3), -5 - (ss - 30))
            pts = trace_line(p0[0], p0[1], fx, fy, stop, 0.25, (-70, 70), (-40, 40))
            ax.plot(pts[:, 0], pts[:, 1], color=FLUX, lw=0.9, zorder=2)
    # effective-area outline (a+g)
    ax.add_patch(Rectangle((-35, -5), 70, 10, fill=False, ls="--", ec=COLORS[1], lw=1.2, zorder=4))
    ax.annotate("", xy=(-35, -19), xytext=(35, -19), arrowprops=dict(arrowstyle="<->", lw=0.7,
                color=COLORS[1]), zorder=5)
    ax.text(0, -19.6, "effective width $a+g$", ha="center", va="top", fontsize=8.5,
            color=COLORS[1], zorder=5, bbox=dict(fc=IRON, ec="none", pad=0.3))
    ax.annotate("", xy=(-30, 14), xytext=(30, 14), arrowprops=dict(arrowstyle="<->", lw=0.7), zorder=5)
    ax.text(0, 14.6, "pole face $a$ = 60 mm", ha="center", va="bottom", fontsize=8.5, zorder=5)
    ax.annotate("", xy=(-44, -5), xytext=(-44, 5), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(-46, 0, "$g$", ha="right", va="center", fontsize=9.5)
    ax.text(-102, -2, "$A_{eff}\\approx(a+g)(b+g)$\n$g$ drawn as 10 mm\n(1 mm in the reactor)",
            fontsize=8.5, ha="left", va="center")
    ax.text(-102, 22, "(a)", fontsize=10, fontweight="bold", va="top")

    # (b) slotted stator over smooth rotor (to scale)
    g = 0.6
    x, y, V, stator = _carter_field(g=g)
    h = x[1] - x[0]
    Bx = (V[1, :] - V[0, :]) / h               # normal B at rotor surface (arbitrary units)
    Bsmooth = 1.0 / g
    kC_num = Bsmooth / Bx.mean()
    Ey, Ex = np.gradient(V, h, h)
    fx = RegularGridInterpolator((y, x), Ex, bounds_error=False, fill_value=None)
    fy = RegularGridInterpolator((y, x), Ey, bounds_error=False, fill_value=None)
    ax = fig.add_subplot(gs[1])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(1.5, 13.5); ax.set_ylim(-0.7, 3.0)
    ax.add_patch(Rectangle((0, -1.0), 30, 1.0, fc=IRON, ec=IRON_EC, lw=1.0, zorder=3))
    teeth = [(0, 6.0), (9.0, 21.0), (24.0, 30.0)]
    for a_, b_ in teeth:
        ax.add_patch(Rectangle((a_, g), b_ - a_, 4.0, fc=IRON, ec=IRON_EC, lw=1.0, zorder=3))
    cum = np.concatenate([[0], np.cumsum(0.5 * (Bx[1:] + Bx[:-1]) * h)])
    nl = 64
    tg = (np.arange(nl) + 0.5) / nl * cum[-1]
    xs0 = np.interp(tg, cum, x[:len(cum)])
    def stop(xx, yy):
        xm = xx % 30
        in_slot = any(abs(xm - c) < 1.5 for c in (7.5, 22.5))
        return yy >= g and not (in_slot and yy < 4.6)
    for x0 in xs0:
        pts = trace_line(x0, 0.02, fx, fy, stop, 0.02, (-1, 31), (0, 5.0), periodic=(0, 30 - h))
        ax.plot(pts[:, 0], pts[:, 1], color=FLUX, lw=0.7, zorder=2)
    gp = kC_num * g
    ax.plot([1.5, 13.5], [gp, gp], ls="--", color=COLORS[1], lw=1.1, zorder=4)
    ax.annotate("$g' = k_C\\,g$ = %.2f mm\n(equivalent smooth gap)" % gp,
                xy=(12.0, gp), xytext=(11.3, 1.9), ha="center", va="center", fontsize=8,
                color=COLORS[1], zorder=6, bbox=dict(fc=IRON, ec="none", pad=0.4),
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.8))
    ax.annotate("", xy=(4.0, 0), xytext=(4.0, g), arrowprops=dict(arrowstyle="<->", lw=0.7,
                shrinkA=0, shrinkB=0), zorder=6)
    ax.text(4.25, 0.3, "$g$ = 0.6 mm", ha="left", va="center", fontsize=8, zorder=6,
            bbox=dict(fc="white", ec="none", pad=0.3))
    ax.annotate("", xy=(6.0, 2.75), xytext=(9.0, 2.75), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(7.5, 2.7, "slot opening 3 mm", ha="center", va="top", fontsize=8)
    ax.text(7.5, -0.35, "smooth rotor surface", ha="center", va="center", fontsize=8, zorder=5)
    ax.text(1.0, 2.95, "(b)", fontsize=10, fontweight="bold", va="top", ha="right")

    # B(x) at the rotor surface, scaled to an average of 0.80 T
    ax = fig.add_subplot(gs[2])
    B = Bx / Bx.mean() * 0.80
    ax.plot(x, B, color=FLUX)
    ax.axhline(0.80, ls="--", color=COLORS[1], lw=1.1)
    ax.text(29.5, 0.80 - 0.03, "average 0.80 T", ha="right", va="top", fontsize=8.5, color=COLORS[1])
    Bt = B.max()
    ax.axhline(Bt, ls=":", color=INK, lw=0.9)
    ax.text(15, Bt + 0.01, "under tooth: %.2f T" % Bt, ha="center", va="bottom", fontsize=8.5)
    imin = np.argmin(B[: len(B) // 2])
    ax.annotate("dip %.0f %% under\nslot opening" % (100 * (1 - B[imin] / Bt)), xy=(x[imin], B[imin]),
                xytext=(x[imin] + 2.6, B[imin] + 0.12), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7))
    ax.axvspan(1.5, 13.5, color="#EEF3F8", zorder=0)
    ax.annotate("", xy=(7.5, 0.2), xytext=(22.5, 0.2), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(18.5, 0.23, "slot pitch 15 mm", ha="center", va="bottom", fontsize=8)
    ax.text(1.7, 0.03, "region shown in (b)", ha="left", va="bottom", fontsize=7.5, color="#5A6878")
    ax.set_xlim(0, 30); ax.set_ylim(0, 1.05)
    ax.set_xlabel("position along the gap $x$ (mm)")
    ax.set_ylabel("gap $B$ (T)")
    ax.text(-2.6, 1.08, "", fontsize=10)
    save(fig, "01", "fig-1-3-fringing-and-carter")
    return kC_num, 1 - B[imin] / Bt


# ----------------------------------------------------------------------------------------
# Figure 1.4 — magnetisation curves and secant permeability
# ----------------------------------------------------------------------------------------
def _curve(Hpts, Bpts, H):
    """Monotone interpolation in log10(H)."""
    return PchipInterpolator(np.log10(Hpts), Bpts)(np.log10(H))


def fig_1_4():
    fig, (ax, axr) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw=dict(width_ratios=[1.45, 1]))
    H = np.logspace(1, 5, 600)
    mats = [
        ("grain-oriented (RD)", [3, 10, 30, 150, 1000, 1e4, 1e5],
         [0.3, 1.2, 1.5, 1.8, 1.9, 1.98, 2.05], COLORS[2], 2.03),
        ("non-oriented 0.5 mm\n(Table 1.6)", np.r_[10, 30, T16_H, 5e4, 1e5],
         np.r_[0.071, 0.214, T16_B, 2.03, 2.10], COLORS[0], 2.0),
        ("mild steel", [10, 100, 300, 1500, 8000, 3e4, 1e5],
         [0.02, 0.35, 1.0, 1.5, 1.8, 1.98, 2.12], INK, 2.1),
        ("amorphous ribbon", [1, 3, 10, 30, 100, 1000, 1e5],
         [0.15, 0.6, 1.3, 1.45, 1.52, 1.56, 1.68], COLORS[3], 1.56),
        ("MnZn ferrite (25 °C)", [3, 10, 30, 100, 300, 1000, 1e5],
         [0.008, 0.025, 0.08, 0.25, 0.40, 0.45, 0.47], COLORS[4], 0.45),
    ]
    ax.axvspan(350, 3500, color="#DDE7F2", lw=0, zorder=0)
    ax.text(1100, 0.12, "knee of\nNO steel\n1.3–1.6 T", ha="center", va="bottom", fontsize=7.5,
            color=COLORS[0])
    label_pos = {"grain-oriented (RD)": (22, 1.9), "non-oriented 0.5 mm\n(Table 1.6)": (11, 0.62),
                 "mild steel": (2500, 1.25), "amorphous ribbon": (12, 1.0),
                 "MnZn ferrite (25 °C)": (900, 0.6)}
    for name, Hp, Bp, c, Bs in mats:
        Bc = _curve(np.array(Hp, float), np.array(Bp, float), H)
        ax.plot(H, Bc, color=c, lw=1.6)
        xt, yt_ = label_pos[name]
        ax.text(xt, yt_, name, color=c, fontsize=7.8, ha="left", va="center")
    ax.plot(T16_H, T16_B, "o", ms=3.2, color=COLORS[0])
    for Bs, txt, c in [(2.03, "≈2.0 T (Si steels)", COLORS[0]), (2.15, "", INK),
                       (1.56, "1.56 T", COLORS[3]), (0.45, "0.45 T", COLORS[4])]:
        ax.axhline(Bs, ls="--", lw=0.7, color=c, alpha=0.8)
    ax.text(1.05e5, 2.03, "2.03", fontsize=7, va="top", ha="right", color=COLORS[0])
    ax.text(1.05e5, 2.155, "2.15 (mild)", fontsize=7, va="bottom", ha="right", color=INK)
    ax.text(11, 1.585, "$B_s$ 1.56", fontsize=7, va="bottom", ha="left", color=COLORS[3])
    ax.text(1.05e5, 0.47, "$B_s$ 0.45", fontsize=7, va="bottom", ha="right", color=COLORS[4])
    ax.set_xscale("log")
    ax.set_xlim(10, 1e5); ax.set_ylim(0, 2.3)
    ax.set_xlabel("$H$ (A/m)")
    ax.set_ylabel("$B$ (T)")
    ax.set_title("(a) normal magnetisation curves", loc="left", fontsize=10)

    mur = T16_B / (MU0 * T16_H)
    Bf = np.linspace(0.5, 1.9, 300)
    Hf = np.exp(PchipInterpolator(T16_B, np.log(T16_H))(Bf))
    axr.plot(Bf, Bf / (MU0 * Hf), color=COLORS[0])
    axr.plot(T16_B, mur, "o", ms=3.5, color=COLORS[0])
    k = np.argmax(mur)
    axr.annotate("peak ≈ %d\nat 0.8 T" % round(mur[k], -1), xy=(T16_B[k], mur[k]),
                 xytext=(0.6, 1500), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.7))
    axr.set_yscale("log")
    axr.set_ylim(50, 10000); axr.set_xlim(0.4, 2.0)
    axr.set_xlabel("$B$ (T)")
    axr.set_ylabel(r"secant $\mu_r = B/\mu_0H$")
    axr.set_title("(b) NO steel, Table 1.6", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.2)
    save(fig, "01", "fig-1-4-bh-curves-of-core-materials")


# ----------------------------------------------------------------------------------------
# Figure 1.5 — saturating reactor: load lines and inductances
# ----------------------------------------------------------------------------------------
def _reactor_model():
    N, lc, AFe, A, g = 14, 0.50, 5.7e-3, 6.0e-3, 2.0e-3
    Bt = np.r_[0.0, T16_B]
    Ht = np.r_[0.0, T16_H]
    Hof = lambda B: np.interp(B, Bt, Ht)           # piecewise-linear Table 1.6 (as in the text)
    NI = lambda B: Hof(B) * lc + B * AFe / (MU0 * A) * g
    Bgrid = np.linspace(0, 1.9, 19001)
    NIgrid = NI(Bgrid)
    i = NIgrid / N
    Bofi = lambda ii: np.interp(ii, i, Bgrid)
    return dict(N=N, lc=lc, AFe=AFe, A=A, g=g, Hof=Hof, NI=NI, Bofi=Bofi, Bt=Bt, Ht=Ht)


def fig_1_5():
    m = _reactor_model()
    N, lc, AFe, A, g = m["N"], m["lc"], m["AFe"], m["A"], m["g"]
    fig, (ax, axr) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    Hs = np.linspace(0, 4000, 800)
    ax.plot(Hs, np.interp(Hs, m["Ht"], m["Bt"]), color=INK, lw=1.8, label="Table 1.6 curve")
    for (ip, c) in [(127.3, COLORS[0]), (200, COLORS[4]), (254, COLORS[1])]:
        F = N * ip
        B0 = F * MU0 * A / (g * AFe)
        Hend = F / lc
        HH = np.linspace(0, min(Hend, 4000), 50)
        ax.plot(HH, B0 * (1 - HH / Hend), color=c, lw=1.2, ls="--")
        Bop = m["Bofi"](ip)
        ax.plot(m["Hof"](Bop), Bop, "o", color=c, ms=5, zorder=5)
        ax.text(m["Hof"](Bop) + (260 if ip < 150 else 60), Bop - (0.16 if ip < 150 else 0.06), "%.2f T" % Bop, color=c, fontsize=8, va="top")
        ax.text(60, B0, "$Ni$ = %d At (%d A)" % (round(F, -0), round(ip)), color=c, fontsize=7.8,
                va="center", ha="left", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.set_xlim(0, 4000); ax.set_ylim(0, 2.45)
    ax.set_xlabel("$H$ in the iron (A/m)")
    ax.set_ylabel("$B$ in the iron (T)")
    ax.set_title("(a) load lines of the gap", loc="left", fontsize=10)
    ax.text(3950, 0.35, "load line:\n$B = \\mu_0\\frac{A}{A_{Fe}}\\frac{Ni-Hl_c}{g}$",
            ha="right", va="bottom", fontsize=8.5)

    ip = np.linspace(1, 300, 900)
    B = m["Bofi"](ip)
    Ls = N * B * AFe / ip * 1e3
    dB = 1e-4
    Linc_pl = N ** 2 * AFe * dB / (m["NI"](B + dB) - m["NI"](B)) * 1e3
    # smooth (monotone cubic) version of the same table for the incremental slope
    Hs_ = PchipInterpolator(m["Bt"], m["Ht"])
    NIs = lambda BB: Hs_(BB) * lc + BB * AFe / (MU0 * A) * g
    Bg = np.linspace(0, 1.9, 19001)
    Bs_ = np.interp(ip, NIs(Bg) / N, Bg)
    Linc = N ** 2 * AFe * dB / (NIs(Bs_ + dB) - NIs(Bs_)) * 1e3
    axr.plot(ip, Ls, color=COLORS[0], label=r"secant $N\Phi/i$")
    axr.plot(ip, Linc, color=COLORS[1], label=r"incremental $N\,d\Phi/di$")
    axr.plot(ip, Linc_pl, color=COLORS[1], lw=0.8, ls=":",
             label="incremental, piecewise-\nlinear table (as in text)")
    axr.axhline(0.70, ls="--", color=INK, lw=0.9)
    axr.text(5, 0.715, "nameplate 0.70 mH", fontsize=8, va="bottom")
    axr.axvline(127.3, ls="--", color=INK, lw=0.9)
    axr.text(122, 0.02, "design peak\n127 A", fontsize=8, va="bottom", ha="right")
    for x0 in (127.3, 200, 254):
        yb = np.interp(x0, ip, Ls); yi = np.interp(x0, ip, Linc_pl)
        if x0 > 130:
            axr.plot(x0, yb, "o", ms=4, color=COLORS[0])
            axr.text(x0 + 4, yb + 0.02, "%.2f" % yb, fontsize=7.8, color=COLORS[0])
        axr.plot(x0, yi, "o", ms=4, color=COLORS[1])
        axr.text(x0 + 4, yi + 0.02, "%.2f" % yi, fontsize=7.8, color=COLORS[1])
    axr.set_xlim(0, 300); axr.set_ylim(0, 1.0)
    axr.set_xlabel("peak current $i$ (A)")
    axr.set_ylabel("inductance (mH)")
    axr.legend(fontsize=7.5, loc="upper right", bbox_to_anchor=(1.0, 1.02))
    axr.set_title("(b) inductance versus current", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.5)
    save(fig, "01", "fig-1-5-saturation-load-line-and-inductance")


if __name__ == "__main__":
    fig_1_1()
    fig_1_2()
    print("Carter (numerical) kC, dip:", fig_1_3())
    fig_1_4()
    fig_1_5()
