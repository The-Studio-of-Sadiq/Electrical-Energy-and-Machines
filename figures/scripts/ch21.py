"""Figures for Chapter 21 — Transmission Lines. Run from the repository root: python figures/scripts/ch21.py"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch
from scipy.interpolate import PchipInterpolator

from figstyle import new_fig, save, COLORS, INK

CH = "21"

# ---------------------------------------------------------------- reference 400 kV line
F = 50.0
W = 2 * np.pi * F
EPS0 = 8.854e-12
GMD = (11 * 11 * 22) ** (1 / 3)
GMR_S, R_COND, D_SUB = 0.01285, 0.03177 / 2, 0.45
L_PH = 2e-7 * np.log(GMD / np.sqrt(GMR_S * D_SUB))           # H/m
C_PH = 2 * np.pi * EPS0 / np.log(GMD / np.sqrt(R_COND * D_SUB))  # F/m
R_PH = 0.0349e-3                                              # ohm/m
Z_SER = R_PH + 1j * W * L_PH
Y_SH = 1j * W * C_PH
ZC = np.sqrt(Z_SER / Y_SH)
GAMMA = np.sqrt(Z_SER * Y_SH)
VLL = 400e3
SIL = VLL ** 2 / abs(ZC) / 1e6                                 # MW, about 516


def abcd(length_km):
    x = length_km * 1e3
    g = GAMMA * x
    return np.cosh(g), ZC * np.sinh(g), np.sinh(g) / ZC


# ---------------------------------------------------------------- 21.1
def lattice(ax, pts, lw=1.2):
    pts = np.asarray(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=lw)


def fig_21_1():
    """400 kV single-circuit horizontal tower."""
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-30, 44)
    ax.set_ylim(-5.5, 40)
    ya, yc = 30.5, 27.0          # crossarm, conductor attachment
    ys = 35.0                    # shield wires
    # ground
    ax.plot([-28, 28], [0, 0], color="#8B6F47", lw=2)
    for x in np.arange(-27, 28, 2.0):
        ax.plot([x, x - 0.8], [0, -0.8], color="#8B6F47", lw=0.6)
    # body: legs and waist
    legL = [(-5, 0), (-2.2, 18), (-1.6, ya - 1.6)]
    legR = [(5, 0), (2.2, 18), (1.6, ya - 1.6)]
    lattice(ax, legL)
    lattice(ax, legR)
    ys_lvls = [0, 4.5, 9, 13.5, 18, 22, 26, ya - 1.6]
    for y0, y1 in zip(ys_lvls[:-1], ys_lvls[1:]):
        xl0, xl1 = np.interp(y0, [0, 18, ya - 1.6], [-5, -2.2, -1.6]), np.interp(y1, [0, 18, ya - 1.6], [-5, -2.2, -1.6])
        ax.plot([xl0, -xl1], [y0, y1], color=INK, lw=0.6)
        ax.plot([-xl0, xl1], [y0, y1], color=INK, lw=0.6)
        ax.plot([xl1, -xl1], [y1, y1], color=INK, lw=0.6)
    # crossarm (top and bottom chords) to +/-12.5 m
    ax.plot([-12.5, 12.5], [ya, ya], color=INK, lw=1.2)
    ax.plot([-12.5, -1.6, 1.6, 12.5], [ya - 0.3, ya - 1.6, ya - 1.6, ya - 0.3], color=INK, lw=1.2)
    for x in np.arange(-12, 12.1, 1.5):
        yb = np.interp(abs(x), [1.6, 12.5], [ya - 1.6, ya - 0.3])
        ax.plot([x, x + 0.75 * np.sign(-x if x else 1)], [yb, ya], color=INK, lw=0.5)
    # earth-wire peaks over the outer phases
    for s in (-1, 1):
        lattice(ax, [(s * 9.6, ya), (s * 11, ys + 1.0), (s * 12.4, ya)])
        ax.plot([s * 10.3, s * 11.7], [ya + 2.7, ya + 2.7], color=INK, lw=0.5)
        ax.plot(s * 11, ys, "o", ms=5, color="#555555", zorder=5)
    # phases with I-strings (3.5 m)
    for x, lab in ((-11, "a"), (0, "b"), (11, "c")):
        ax.plot([x, x], [ya, yc], color="#7a5c2e", lw=3.0, solid_capstyle="butt")
        for yy in np.linspace(ya - 0.4, yc + 0.4, 7):
            ax.plot([x - 0.45, x + 0.45], [yy, yy], color="#7a5c2e", lw=1.0)
        ax.plot([x - 0.25, x + 0.25], [yc, yc], "o", ms=3.8, color=COLORS[0], zorder=5)
        ax.text(x + 1.0, yc - 0.6, lab, ha="left", va="top", fontsize=11, fontweight="bold", color=COLORS[0],
                bbox=dict(fc="white", ec="none", pad=0.6), zorder=6)
        # mid-span position (sagged)
        ax.plot([x - 0.25, x + 0.25], [15, 15], "o", ms=3.8, mfc="white", mec=COLORS[0], zorder=5)
    ax.plot([-14, 14], [15, 15], ls=":", color=COLORS[0], lw=0.9)
    ax.text(-14.3, 15, "mid-span\n(after sag)", ha="right", va="center", fontsize=7.5, color=COLORS[0])
    # dimensions
    def dim_v(x, y0, y1, txt, side="right", ym=None):
        ax.annotate("", xy=(x, y1), xytext=(x, y0),
                    arrowprops=dict(arrowstyle="<|-|>", color="#444444", lw=0.8, mutation_scale=7))
        ax.text(x + (0.5 if side == "right" else -0.5), (y0 + y1) / 2 if ym is None else ym, txt, fontsize=7.5,
                ha="left" if side == "right" else "right", va="center", color="#333333")
    dim_v(18.0, 0, yc, "27 m\n(attach-\nment)")
    dim_v(14.5, 0, 15, "15 m\nground\nclearance")
    dim_v(-17.5, 0, ys, "35 m\n(shield\nwires)", side="left", ym=7)
    ax.annotate("", xy=(0, yc + 0.9), xytext=(-11, yc + 0.9),
                arrowprops=dict(arrowstyle="<|-|>", color="#444444", lw=0.8, mutation_scale=7))
    ax.annotate("", xy=(11, yc + 0.9), xytext=(0, yc + 0.9),
                arrowprops=dict(arrowstyle="<|-|>", color="#444444", lw=0.8, mutation_scale=7))
    ax.text(-5.5, yc + 1.05, "11 m", ha="center", va="bottom", fontsize=7.5)
    ax.text(5.5, yc + 1.05, "11 m", ha="center", va="bottom", fontsize=7.5)
    ax.text(-13.2, ya + 1.5, "shield wire", ha="right", fontsize=7.5, color="#555555")
    ax.text(-13.0, 27.8, "I-string\n≈ 3.5 m", ha="right", va="center", fontsize=7.5, color="#7a5c2e")
    ax.annotate("", xy=(26, -3.0), xytext=(-26, -3.0),
                arrowprops=dict(arrowstyle="<|-|>", color="#444444", lw=0.8, mutation_scale=7))
    ax.text(0, -3.3, "right-of-way ≈ 46–52 m", ha="center", va="top", fontsize=8)
    ax.text(25.0, 5.5, f"GMD = (11·11·22)$^{{1/3}}$\n      = {GMD:.2f} m\n\ntwin ACSR Moose\nper phase",
            fontsize=8, va="center", ha="left")

    # inset: twin bundle
    ins = ax.inset_axes([25.0, 11.5, 18.8, 21.0], transform=ax.transData)
    ins.set_aspect("equal")
    ins.set_xlim(-340, 340)
    ins.set_ylim(-260, 492)
    ins.axis("off")
    ins.add_patch(FancyBboxPatch((-330, -250), 660, 735, boxstyle="round,pad=0,rounding_size=20",
                                 fc="#F7F9FB", ec="#999999", lw=0.8))
    for x in (-225, 225):
        ins.add_patch(Circle((x, 0), 31.77 / 2 * 2.6, fc="#cfd8e3", ec=INK, lw=0.9))
    ins.plot([-225, 225], [0, 0], color="#888888", lw=2.0)    # spacer
    ins.annotate("", xy=(225, -62), xytext=(-225, -62),
                 arrowprops=dict(arrowstyle="<|-|>", color="#444444", lw=0.7, mutation_scale=6))
    ins.text(0, -80, "d = 450 mm", ha="center", va="top", fontsize=7)
    ins.text(0, 470, "twin bundle (enlarged)", ha="center", va="top", fontsize=7, fontweight="bold")
    ins.text(0, 395, "ACSR Moose, Ø 31.77 mm\n(drawn ×2.6)\nsub-conductor GMR 12.85 mm\n"
             "bundle GMR $\\sqrt{12.85\\times450}$\n= 76.0 mm", ha="center", va="top", fontsize=6.8)
    ax.plot([11.7, 25.0], [yc, 20.0], color="#999999", lw=0.7, ls="--")
    save(fig, CH, "fig-21-1-400kv-tower-geometry")


# ---------------------------------------------------------------- 21.2
def model_errors(lengths):
    eA, eB, eC = [], [], []
    for l in lengths:
        A, B, C = abcd(l)
        Z, Y = Z_SER * l * 1e3, Y_SH * l * 1e3
        Cn = Y * (1 + Y * Z / 4)
        eA.append((1 / abs(A) - 1) * 100)                 # short model |A| = 1, relative to exact (omitted Ferranti rise)
        eB.append((abs(Z) - abs(B)) / abs(B) * 100)
        eC.append(abs((abs(Cn) - abs(C)) / abs(C)) * 100)
    return map(np.array, (eA, eB, eC))


def fig_21_2():
    """Errors of the short and nominal-pi models."""
    l = np.linspace(1, 800, 800)
    eA, eB, eC = model_errors(l)
    beta = np.degrees(GAMMA.imag) * 1e3            # deg/km
    fig, ax = new_fig(6.4, 4.0)
    for x0, x1, lab, fc in [(0, 80, "short", "#E8F1F8"), (80, 250, "medium", "#FDF0E3"),
                            (250, 800, "long", "#E6F4EF")]:
        ax.axvspan(x0, x1, color=fc, lw=0)
        ax.text((x0 + x1) / 2, 52.3, lab, ha="center", fontsize=8.5, color="#444444")
    ax.plot(l, eA, color=COLORS[0], label="short model: error in |A| (1/|A| − 1, omitted Ferranti rise)")
    ax.plot(l, eB, color=COLORS[1], label="nominal π: error in |B|")
    ax.plot(l, eC, color=COLORS[2], label="nominal π: error in |C| (magnitude)")
    tab = [80, 150, 250, 400, 600, 800]
    a2, b2, c2 = model_errors(tab)
    for arr, c in ((a2, COLORS[0]), (b2, COLORS[1]), (c2, COLORS[2])):
        ax.plot(tab, arr, "o", color=c, ms=3.5)
    for x, y in zip(tab[3:], a2[3:]):
        ax.text(x - 8, y + 0.6, f"{y:.1f}", fontsize=7, color=COLORS[0], ha="right", va="bottom")
    for x, y in zip(tab[3:], b2[3:]):
        ax.text(x - 8, y + 0.6, f"{y:.1f}", fontsize=7, color=COLORS[1], ha="right", va="bottom")
    for x, y in zip(tab[4:], c2[4:]):
        ax.text(x + 8, y - 0.4, f"{y:.1f}", fontsize=7, color=COLORS[2], ha="left", va="top")
    ax.axhline(1, color=INK, ls="--", lw=0.9)
    ax.text(795, 1.3, "1 % tolerance", ha="right", fontsize=7.5)
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 55)
    ax.set_xlabel("Line length (km)")
    ax.set_ylabel("Model error versus exact solution (%)")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.88), fontsize=7.5, frameon=True,
              facecolor="white", edgecolor="#cccccc")
    sec = ax.secondary_xaxis("top", functions=(lambda x: x * beta, lambda d: d / beta))
    sec.set_xlabel(f"Electrical length βℓ (degrees, {beta * 100:.2f}° per 100 km)", fontsize=8.5)
    sec.set_xticks([0, 10, 20, 30, 40, 48.6])
    sec.set_xticklabels(["0", "10", "20", "30", "40", "48.6"])
    save(fig, CH, "fig-21-2-line-model-errors")


# ---------------------------------------------------------------- 21.3
def vr_curve(A, B, pf, Ps):
    """Receiving-end voltage (pu, upper branch) for constant-power loads, sending end fixed at 1 pu."""
    Vb = VLL / np.sqrt(3)
    t = np.tan(np.arccos(pf))
    out = []
    vs = np.linspace(0.2, 1.3, 22001) * Vb
    for P in Ps:
        S = P * 1e6 / 3 * (1 + 1j * t)
        f = np.abs(A * vs + B * np.conj(S / vs)) - Vb
        idx = np.where(np.diff(np.sign(f)))[0]
        out.append(vs[idx[-1]] / Vb if len(idx) else np.nan)
    return np.array(out)


def fig_21_3():
    """400 km line: receiving-end voltage and reactive requirement."""
    A, B, C = abcd(400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.7))
    a1.axhspan(0.95, 1.05, color="#E6F4EF", lw=0)
    x = np.linspace(0, 1.3, 261)
    for pf, c, lab in [(1.0, COLORS[0], "unity pf"), (0.95, COLORS[1], "0.95 lagging")]:
        v = vr_curve(A, B, pf, x * SIL)
        a1.plot(x, v, color=c, label=lab)
        k = np.where(~np.isnan(v))[0][-1]
        a1.plot(x[k], v[k], "x", color=c, ms=6)
        for xp in (0.0, 0.5, 1.0):
            vv = vr_curve(A, B, pf, [xp * SIL])[0]
            if not np.isnan(vv) and not (pf != 1 and xp == 0):
                a1.plot(xp, vv, "o", color=c, ms=4)
                a1.text(xp + (0.03 if pf == 1 else -0.03), vv + (0.012 if pf == 1 else -0.012), f"{vv:.3f}", fontsize=7.5, color=c,
                        va="bottom" if pf == 1 else "top", ha="left" if pf == 1 else "right")
    a1.text(0.02, 0.62, "×: nose (no operating\npoint beyond)", fontsize=7, color="#555555")
    a1.text(1.28, 1.0, "0.95–1.05 pu", fontsize=7, ha="right", va="center", color="#2d7a5f")
    a1.set_xlim(0, 1.3)
    a1.set_ylim(0.6, 1.15)
    a1.set_xlabel("Receiving-end power P / SIL")
    a1.set_ylabel("Receiving-end voltage (pu)")
    a1.set_title("(a) Sending end fixed at 1.0 pu", fontsize=9.5)
    a1.legend(loc="lower left", bbox_to_anchor=(0.0, 0.12), fontsize=7.5)

    # (b) both ends at 1.0 pu, lossless line
    bl = np.degrees(GAMMA.imag) * 400e3
    th = np.radians(bl)
    p = np.linspace(0, 2.0, 401)
    d = np.arcsin(np.clip(p * np.sin(th), -1, 1))
    q_sup = -SIL * (np.cos(d) - np.cos(th)) / np.sin(th)      # MVAr supplied by receiving bus
    a2.axhline(0, color=INK, lw=0.5)
    a2.plot(p, q_sup, color=COLORS[0], label="lossless line")
    # lossy check (exact ABCD)
    Vb = VLL / np.sqrt(3)
    q_l = []
    for pp in p:
        ds = np.radians(np.linspace(0, 89, 8901))
        VS = Vb * np.exp(1j * ds)
        SR = 3 * Vb * np.conj((VS - A * Vb) / B) / 1e6
        i = np.argmin(abs(SR.real - pp * SIL))
        q_l.append(-SR[i].imag)
    a2.plot(p, q_l, "--", color="#888888", lw=1.1, label="with conductor resistance")
    for pp in (0, 1.0, 1.5):
        dd = np.arcsin(pp * np.sin(th))
        qq = -SIL * (np.cos(dd) - np.cos(th)) / np.sin(th)
        a2.plot(pp, qq, "o", color=COLORS[0], ms=4)
        a2.text(pp + 0.05, qq - 8, f"{round(qq) + 0:+d} MVAr" if abs(qq) > 0.5 else "0 MVAr", fontsize=7.5, color=COLORS[0], va="top")
    a2.set_xlim(0, 2.0)
    a2.set_ylim(-150, 450)
    a2.set_xlabel("Transferred power P / SIL")
    a2.set_ylabel("Reactive power supplied at receiving end (MVAr)")
    a2.set_title("(b) Both ends held at 1.0 pu", fontsize=9.5)
    a2.legend(loc="upper left", fontsize=7.5)
    tw = a2.twinx()
    tw.spines["right"].set_visible(True)
    tw.plot(p, np.degrees(d), color=COLORS[2], lw=1.2, ls="-.")
    for pp in (1.0, 1.5, 2.0):
        dd = np.degrees(np.arcsin(pp * np.sin(th)))
        tw.plot(pp, dd, "s", color=COLORS[2], ms=3.5)
        tw.text(pp - 0.04, dd + 1.5, f"{dd:.1f}°", fontsize=7.5, color=COLORS[2], ha="right", va="bottom")
    tw.set_ylim(0, 75)
    tw.set_ylabel("Angle across line δ (deg), dash-dot", color=COLORS[2], fontsize=8.5)
    tw.tick_params(axis="y", colors=COLORS[2])
    fig.tight_layout(w_pad=0.8)
    save(fig, CH, "fig-21-3-receiving-end-voltage")


# ---------------------------------------------------------------- 21.4
def fig_21_4():
    """St. Clair loadability curve."""
    pts_l = np.array([80, 160, 320, 480, 640, 800])
    pts_v = np.array([3.0, 2.0, 1.3, 1.0, 0.8, 0.65])
    f = PchipInterpolator(np.log(pts_l), np.log(pts_v))
    l = np.linspace(80, 800, 400)
    fig, ax = new_fig(6.4, 4.0)
    for x0, x1, lab, fc in [(0, 80, "thermal\nlimit", "#FDECEA"), (80, 300, "voltage-drop\nlimit", "#FDF0E3"),
                            (300, 800, "stability limit", "#E6F4EF")]:
        ax.axvspan(x0, x1, color=fc, lw=0)
        ax.text((x0 + x1) / 2, 3.3, lab, ha="center", va="center", fontsize=8.5, color="#444444")
    ax.plot(l, np.exp(f(np.log(l))), color=COLORS[0], lw=2.2, label="St. Clair curve (loadability)")
    ax.plot([0, 80], [3.0, 3.0], color=COLORS[0], lw=1.4, ls=":")
    ax.plot(pts_l, pts_v, "o", color=COLORS[0], ms=4)
    for x, y in zip(pts_l, pts_v):
        ax.text(x - 8, y - 0.07, f"{y:.2f}".rstrip("0") if y < 1 else f"{y:.1f}", fontsize=7.5,
                color=COLORS[0], ha="right", va="top")
    beta = 6.07 / 100
    lr = np.linspace(55, 800, 400)
    ax.plot(lr, np.sin(np.radians(30)) / np.sin(np.radians(beta * lr)), "--", color=COLORS[1], lw=1.4,
            label="lossless line alone at δ = 30°: sin 30° / sin βℓ")
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 3.5)
    ax.set_xlabel("Line length (km)")
    ax.set_ylabel("Loadability (multiple of SIL)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), fontsize=7.5, frameon=True,
              facecolor="white", edgecolor="#cccccc")
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.set_ylim(0, 3.5 * 516)
    ax2.set_ylabel("MW for a 400 kV twin-bundle line (SIL 516 MW)", fontsize=8.5)
    save(fig, CH, "fig-21-4-st-clair-loadability")


# ---------------------------------------------------------------- 21.5
def emax_per_kv(n, gmd, r=R_COND, d=D_SUB):
    """Maximum surface gradient (kV/cm rms) per kV line-to-line."""
    if n == 1:
        req, Rb = r, np.inf
    else:
        Rb = d / (2 * np.sin(np.pi / n))
        req = (n * r * Rb ** (n - 1)) ** (1 / n)
    C = 2 * np.pi * EPS0 / np.log(gmd / req)
    q = C * 1e3 / np.sqrt(3)
    eav = q / (2 * np.pi * EPS0 * n * r) / 1e5
    return eav * (1 + (n - 1) * r / Rb if n > 1 else 1)


def peek(m, delta, r_cm=R_COND * 100):
    return 21.1 * m * delta * (1 + 0.3 / np.sqrt(delta * r_cm))


def fig_21_5():
    """Maximum surface gradient versus voltage."""
    V = np.linspace(200, 800, 2)
    gmd765 = (15 * 15 * 30) ** (1 / 3)
    fig, ax = new_fig(6.4, 4.0)
    lo, hi = peek(0.82, 1.0), peek(0.90, 1.0)
    lo_a, hi_a = peek(0.82, 0.89), peek(0.90, 0.89)
    ax.axhspan(lo, hi, color="#FDECEA", lw=0)
    ax.text(795, (lo + hi) / 2, f"Peek visual onset, m 0.82–0.9: {lo:.1f}–{hi:.1f}", fontsize=7.5, ha="right",
            va="center", color="#9c3d2e")
    ax.axhspan(lo_a, hi_a, fc="none", ec="#9c3d2e", ls="--", lw=0.8, hatch="////", alpha=0.35)
    ax.text(795, (lo_a + hi_a) / 2, f"at 1000 m (δ = 0.89): {lo_a:.1f}–{hi_a:.1f}", fontsize=7.5, ha="right",
            va="center", color="#9c3d2e")
    ax.axhline(17, color=INK, ls="--", lw=0.9)
    ax.text(795, 16.6, "typical design limit 17 kV/cm", fontsize=7.5, ha="right", va="top")
    lines = [(1, GMD, COLORS[1], "single Moose, GMD 13.86 m", "-"),
             (2, GMD, COLORS[0], "twin Moose, 450 mm, GMD 13.86 m", "-"),
             (4, gmd765, COLORS[2], f"quad Moose, 450 mm, GMD {gmd765:.1f} m (765 kV, indicative)", "-.")]
    for n, g, c, lab, ls in lines:
        k = emax_per_kv(n, g)
        ax.plot(V, k * V, color=c, ls=ls, label=lab)
        for v in ((400, 420) if n < 4 else (800,)):
            ax.plot(v, k * v, "o", color=c, ms=3.5)
        if n < 4:
            ax.text(395, k * 400 + (0.5 if n == 1 else 0.5), f"{k * 400:.1f}", fontsize=7, color=c,
                    ha="right", va="bottom")
            ax.text(425, k * 420 - 0.4, f"{k * 420:.1f}", fontsize=7, color=c, ha="left", va="top")
        else:
            ax.text(790, k * 800 - 0.7, f"{k * 800:.1f} kV/cm at 800 kV", fontsize=7, color=c, ha="right", va="top")
    for v in (420, 800):
        ax.axvline(v, color="#999999", ls=":", lw=0.9)
    ax.text(422, 1.0, "420 kV", fontsize=7.5, color="#555555")
    ax.text(797, 1.0, "800 kV", fontsize=7.5, color="#555555", ha="right")
    ax.set_xlim(200, 800)
    ax.set_ylim(0, 35)
    ax.set_xlabel("Line-to-line voltage (kV rms)")
    ax.set_ylabel("Maximum surface gradient (kV/cm rms)")
    ax.legend(loc="upper left", fontsize=7.5, frameon=True, facecolor="white", edgecolor="#cccccc")
    save(fig, CH, "fig-21-5-corona-surface-gradient")


# ---------------------------------------------------------------- 21.6
def converter(ax, x, y, s=0.9, label=None):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.plot([x - s / 2, x + s / 2], [y - s / 2, y + s / 2], color=INK, lw=0.8, zorder=4)
    ax.text(x - s * 0.22, y + s * 0.2, "~", ha="center", va="center", fontsize=8, zorder=5)
    ax.text(x + s * 0.22, y - s * 0.22, "=", ha="center", va="center", fontsize=8, zorder=5)
    if label:
        ax.text(x, y - s / 2 - 0.15, label, ha="center", va="top", fontsize=6.5)


def acbus(ax, x, y, h=1.1):
    ax.plot([x, x], [y - h / 2, y + h / 2], color=INK, lw=2.5)


def electrode(ax, x, y):
    ax.plot([x, x], [y, y - 0.35], color=INK, lw=0.9)
    for k, w in enumerate([0.35, 0.22, 0.09]):
        ax.plot([x - w, x + w], [y - 0.35 - k * 0.12] * 2, color=INK, lw=0.9)


def fig_21_6():
    """HVDC configurations and AC/DC break-even distance."""
    fig = plt.figure(figsize=(6.8, 4.6))
    a = fig.add_axes([0.0, 0.0, 0.47, 1.0])
    a.set_xlim(0, 8)
    a.set_ylim(0, 12.4)
    a.set_aspect("equal")
    a.axis("off")
    # (1) monopole, earth return
    y = 11.0
    a.text(0.1, 12.2, "Monopole, earth return", fontsize=8, fontweight="bold", va="top")
    acbus(a, 0.5, y)
    acbus(a, 7.5, y)
    a.plot([0.5, 1.3], [y, y], color=INK, lw=1)
    a.plot([6.7, 7.5], [y, y], color=INK, lw=1)
    converter(a, 1.8, y)
    converter(a, 6.2, y)
    a.plot([2.25, 5.75], [y + 0.25, y + 0.25], color=COLORS[1], lw=1.6)
    a.text(4.0, y + 0.35, "pole conductor", ha="center", fontsize=6.8, color=COLORS[1])
    for xc in (1.8, 6.2):
        a.plot([xc, xc], [y - 0.45, y - 0.7], color=INK, lw=0.9)
        electrode(a, xc, y - 0.7)
    a.text(4.0, y - 1.5, "return current through earth / sea electrodes", ha="center", fontsize=6.5,
           color="#555555")
    # (2) bipole
    y = 7.4
    a.text(0.1, 9.05, "Bipole", fontsize=8, fontweight="bold", va="top")
    acbus(a, 0.5, y, 2.0)
    acbus(a, 7.5, y, 2.0)
    for dy, lab, c in ((0.6, "+500 kV", COLORS[1]), (-0.6, "−500 kV", COLORS[0])):
        a.plot([0.5, 1.3], [y + dy, y + dy], color=INK, lw=1)
        a.plot([6.7, 7.5], [y + dy, y + dy], color=INK, lw=1)
        converter(a, 1.8, y + dy, s=0.75)
        converter(a, 6.2, y + dy, s=0.75)
        yy = y + dy + np.sign(dy) * 0.2
        a.plot([2.18, 5.82], [yy, yy], color=c, lw=1.6)
        a.text(4.0, yy + np.sign(dy) * 0.12, lab, ha="center", va="bottom" if dy > 0 else "top",
               fontsize=6.8, color=c)
    for xc in (1.8, 6.2):
        a.plot([xc, xc], [y + 0.22, y - 0.22], color=INK, lw=0.9)
        a.plot([xc, xc - 0.7], [y, y], color=INK, lw=0.9) if False else None
    a.plot([1.8, 2.5], [y, y], color=INK, lw=0.9)
    a.plot([6.2, 5.5], [y, y], color=INK, lw=0.9)
    electrode(a, 2.5, y)
    electrode(a, 5.5, y)
    a.text(4.0, y - 0.05, "neutral earthed\nat electrodes", ha="center", va="center", fontsize=6.3, color="#555555")
    # (3) back-to-back
    y = 4.6
    a.text(0.1, 5.75, "Back-to-back (no line)", fontsize=8, fontweight="bold", va="top")
    a.add_patch(Rectangle((2.5, y - 0.8), 3.0, 1.6, fc="#F3F3F3", ec="#888888", lw=0.8, ls="--"))
    acbus(a, 1.2, y)
    acbus(a, 6.8, y)
    a.plot([1.2, 3.1], [y, y], color=INK, lw=1)
    a.plot([4.9, 6.8], [y, y], color=INK, lw=1)
    converter(a, 3.4, y, s=0.75)
    converter(a, 4.6, y, s=0.75)
    a.plot([3.78, 4.22], [y, y], color=COLORS[1], lw=1.6)
    a.text(4.0, y - 0.95, "one building", ha="center", va="top", fontsize=6.5, color="#555555")
    a.text(1.2, y + 0.7, "AC 1", ha="center", fontsize=6.5)
    a.text(6.8, y + 0.7, "AC 2", ha="center", fontsize=6.5)
    # (4) multi-terminal VSC
    a.text(0.1, 2.75, "Multi-terminal VSC", fontsize=8, fontweight="bold", va="top")
    nodes = [(1.8, 1.0), (6.2, 1.0), (4.0, 2.2)]
    hub = (4.0, 1.0)
    for (xc, yc) in nodes:
        converter(a, xc, yc, s=0.7)
    a.plot([2.15, 5.85], [1.0, 1.0], color=COLORS[1], lw=1.6)
    a.plot([4.0, 4.0], [1.0, 1.85], color=COLORS[1], lw=1.6)
    a.plot(*hub, "o", color=COLORS[1], ms=4)
    a.text(4.0, 0.75, "DC network", ha="center", va="top", fontsize=6.5, color=COLORS[1])
    for (xc, yc), (dx, dy) in zip(nodes, [(-0.85, 0), (0.85, 0), (0.85, 0)]):
        a.plot([xc + np.sign(dx) * 0.35, xc + dx], [yc, yc], color=INK, lw=1)
        acbus(a, xc + dx, yc, 0.7)

    # cost plot
    b = fig.add_axes([0.56, 0.13, 0.42, 0.78])
    L = np.linspace(0, 1500, 1501)
    ac = 1.0 + 0.008 * L + 0.7 * np.floor(L / 350)          # compensation / intermediate substations
    dc = 3.9 + 0.0043 * L
    acc = 0.5 + 0.06 * L                                   # cables
    dcc = 3.5 + 0.0225 * L
    b.plot(L, ac, color=COLORS[0], label="AC overhead")
    b.plot(L, dc, color=COLORS[1], label="DC overhead")
    b.plot(L, acc, "--", color=COLORS[0], lw=1.3, label="AC cable")
    b.plot(L, dcc, "--", color=COLORS[1], lw=1.3, label="DC cable")
    i = np.argmax(ac >= dc)
    j = np.argmax(acc >= dcc)
    for k, lab in ((i, f"≈ {round(L[i], -2):.0f} km\n(overhead)"), (j, f"≈ {L[j]:.0f} km\n(cable)")):
        b.plot(L[k], dc[k] if k == i else dcc[k], "o", color=INK, ms=5, zorder=5)
        b.axvline(L[k], color="#999999", ls=":", lw=0.9)
        b.text(L[k] + 25, 0.6, lab, fontsize=7.5, va="bottom")
    b.text(950, 15.8, "steps: intermediate\nsubstations and\ncompensation", fontsize=7,
           color=COLORS[0], ha="center", va="top")
    b.annotate("intercept: two\nconverter stations", (0, dc[0]), xytext=(900, 3.0), fontsize=7, color=COLORS[1],
               va="center", arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.8, mutation_scale=7))
    b.set_xlim(0, 1500)
    b.set_ylim(0, 20)
    b.set_xlabel("Transmission distance (km)")
    b.set_ylabel("Total cost (relative units)")
    b.set_title("Break-even distance (schematic)", fontsize=9)
    b.legend(loc="upper left", fontsize=7.5, frameon=True, facecolor="white", edgecolor="#cccccc")
    save(fig, CH, "fig-21-6-hvdc-configurations-breakeven")


if __name__ == "__main__":
    fig_21_1()
    fig_21_2()
    fig_21_3()
    fig_21_4()
    fig_21_5()
    fig_21_6()
