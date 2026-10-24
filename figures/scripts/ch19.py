"""Figures for Chapter 19 — Fault Analysis. Run from the repository root: python figures/scripts/ch19.py"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

CH = "19"


# ---------------------------------------------------------------- helpers
def resistor_h(ax, x0, x1, y, h=0.22, label="", above=True, fs=8.5, lead=None):
    """IEC impedance box between x0 and x1 at height y (leads included)."""
    w = (x1 - x0) * (0.5 if lead is None else lead)
    xm = (x0 + x1) / 2
    ax.plot([x0, xm - w / 2], [y, y], color=INK, lw=1.1)
    ax.plot([xm + w / 2, x1], [y, y], color=INK, lw=1.1)
    ax.add_patch(Rectangle((xm - w / 2, y - h / 2), w, h, fc="white", ec=INK, lw=1.1))
    if label:
        ax.text(xm, y + (h / 2 + 0.08 if above else -h / 2 - 0.08), label, ha="center",
                va="bottom" if above else "top", fontsize=fs)


def resistor_v(ax, x, y0, y1, w=0.22, label="", right=True, fs=8.5):
    ym = (y0 + y1) / 2
    h = abs(y1 - y0) * 0.5
    ax.plot([x, x], [y0, ym - np.sign(y1 - y0) * h / 2], color=INK, lw=1.1)
    ax.plot([x, x], [ym + np.sign(y1 - y0) * h / 2, y1], color=INK, lw=1.1)
    ax.add_patch(Rectangle((x - w / 2, ym - h / 2), w, h, fc="white", ec=INK, lw=1.1))
    if label:
        ax.text(x + (w / 2 + 0.08 if right else -w / 2 - 0.08), ym, label, ha="left" if right else "right",
                va="center", fontsize=fs)


def source(ax, x, y, r=0.25, label="", fs=8.5, side="left"):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    t = np.linspace(-0.6 * r, 0.6 * r, 50)
    ax.plot(x + t, y + 0.3 * r * np.sin(t / (0.6 * r) * np.pi), color=INK, lw=1.0, zorder=4)
    if label:
        dx = -r - 0.08 if side == "left" else r + 0.08
        ax.text(x + dx, y, label, ha="right" if side == "left" else "left", va="center", fontsize=fs)


def earth(ax, x, y, s=0.18):
    ax.plot([x, x], [y, y - s * 0.6], color=INK, lw=1.1)
    for k, f in enumerate([1.0, 0.65, 0.3]):
        yy = y - s * 0.6 - k * s * 0.3
        ax.plot([x - s * f, x + s * f], [yy, yy], color=INK, lw=1.1)


def fault_symbol(ax, x, y, s=0.35, color="#D55E00"):
    pts = np.array([[0, 0], [0.35, -0.35], [-0.05, -0.5], [0.3, -1.0]]) * s
    ax.plot(x + pts[:, 0], y + pts[:, 1], color=color, lw=2.0)
    ax.annotate("", xy=(x + pts[-1, 0], y + pts[-1, 1]),
                xytext=(x + pts[-2, 0], y + pts[-2, 1]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, mutation_scale=10))


def breaker(ax, x, y, s=0.16):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="white", ec=INK, lw=1.1, zorder=3))


# ---------------------------------------------------------------- 19.1
def fig_19_1():
    """Generator terminal fault current with full DC offset."""
    Xdpp, Xdp, Xd = 0.14, 0.22, 1.8
    Tdpp, Tdp, Ta, E, f = 0.03, 0.8, 0.15, 1.0, 50.0
    w = 2 * np.pi * f
    t = np.linspace(0, 1.5, 60001)

    def iac(t):
        return E * ((1 / Xdpp - 1 / Xdp) * np.exp(-t / Tdpp)
                    + (1 / Xdp - 1 / Xd) * np.exp(-t / Tdp) + 1 / Xd)

    Iac = iac(t)
    idc0 = np.sqrt(2) * iac(0.0)          # 10.1 pu for full offset
    idc = idc0 * np.exp(-t / Ta)
    i = idc - np.sqrt(2) * Iac * np.cos(w * t)
    up, lo = idc + np.sqrt(2) * Iac, idc - np.sqrt(2) * Iac

    fig, ax = new_fig(6.8, 4.2)
    ax.plot(t, i, color=COLORS[0], lw=0.5, label="phase current $i(t)$")
    ax.plot(t, up, "--", color=INK, lw=1.0, label="AC envelope (about the DC component)")
    ax.plot(t, lo, "--", color=INK, lw=1.0)
    ax.plot(t, idc, ":", color=COLORS[1], lw=2.0, label=r"DC component, $10.1\,e^{-t/0.15}$")
    ax.axhline(0, color=INK, lw=0.5)
    # RMS levels, drawn at their peak equivalents sqrt(2)*I and labelled outside the axes
    levels = [(1 / Xdpp, "$I''$ = 7.1 pu rms (subtransient)", ":"),
              (1 / Xdp, "$I'$ = 4.5 pu rms (transient)", ":"),
              (3.0, "3 pu rms: short-circuit support", "-."),
              (1 / Xd, "$I_k$ = 0.56 pu rms (steady state)", ":")]
    for I, txt, ls in levels:
        y = np.sqrt(2) * I
        col = COLORS[2] if ls == "-." else "#777777"
        ax.axhline(y, color=col, ls=ls, lw=1.2 if ls == "-." else 0.9)
        ax.text(1.52, y, txt, fontsize=7.5, va="center", ha="left",
                color=COLORS[2] if ls == "-." else INK, clip_on=False)
    ax.text(1.52, -3.2, "Levels are drawn at their peak\nvalues, $\\sqrt{2}\\times$ rms.\n"
            "Steady state assumes constant\nexcitation; the support level\nneeds excitation boost.",
            fontsize=7, va="top", ha="left", color="#555555", clip_on=False)
    ax.set_xlim(0, 1.5)
    ax.set_ylim(-12, 22)
    ax.set_xlabel("Time after fault inception (s)")
    ax.set_ylabel("Phase current (multiples of rated rms current)")
    ax.legend(loc="lower right", fontsize=8, frameon=True, facecolor="white", edgecolor="#cccccc")

    ins = ax.inset_axes([0.25, 0.58, 0.48, 0.39])
    m = t <= 0.2
    ins.plot(t[m] * 1e3, i[m], color=COLORS[0], lw=0.9)
    ins.plot(t[m] * 1e3, up[m], "--", color=INK, lw=0.8)
    ins.plot(t[m] * 1e3, lo[m], "--", color=INK, lw=0.8)
    ins.plot(t[m] * 1e3, idc[m], ":", color=COLORS[1], lw=1.6)
    ins.axhline(0, color=INK, lw=0.4)
    ins.set_xlim(0, 200)
    ins.set_ylim(-12, 22)
    ins.tick_params(labelsize=7)
    ins.set_xlabel("ms (zoom 0–0.2 s)", fontsize=7, labelpad=1)
    ins.set_facecolor("white")
    ins.text(12, 19.5, f"first peak {i[m].max():.1f}", fontsize=7)
    save(fig, CH, "fig-19-1-generator-fault-current")


# ---------------------------------------------------------------- 19.2
def fig_19_2():
    """Plant single-line diagram and reactance diagram."""
    fig, ax = schematic(6.8, 4.4, xlim=(0, 13.6), ylim=(0, 8.8))
    # ---- left: single-line diagram
    bus_y = 3.6
    ax.plot([0.6, 6.6], [bus_y, bus_y], color=INK, lw=4, solid_capstyle="butt")
    ax.text(1.65, bus_y + 0.18, "11 kV switchboard, 25 kA breakers", fontsize=8, va="bottom")
    # grid feeder (x=1.4)
    xg = 1.4
    source(ax, xg, 8.1, r=0.32)
    ax.text(xg + 0.45, 8.1, "132 kV grid\n4000 MVA", fontsize=8, va="center")
    ax.plot([xg, xg], [7.78, 7.1], color=INK, lw=1.1)
    ax.plot([xg - 0.15, xg + 0.15], [7.1, 7.1], color=INK, lw=2.5)  # 132 kV bus stub
    ax.plot([xg, xg], [7.1, 6.55], color=INK, lw=1.1)
    ax.add_patch(Circle((xg, 6.25), 0.3, fc="none", ec=INK, lw=1.1))
    ax.add_patch(Circle((xg, 5.8), 0.3, fc="none", ec=INK, lw=1.1))
    ax.text(xg + 0.45, 6.02, "40 MVA\n132/11 kV\n$z$ = 12 %", fontsize=8, va="center")
    ax.plot([xg, xg], [5.5, bus_y], color=INK, lw=1.1)
    breaker(ax, xg, 4.4)
    # generator (x=3.3)
    xG = 3.1
    ax.plot([xG, xG], [bus_y, 1.55], color=INK, lw=1.1)
    breaker(ax, xG, 2.8)
    ax.add_patch(Circle((xG, 1.2), 0.36, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(xG, 1.2, "G", ha="center", va="center", fontsize=10)
    ax.text(xG, 0.62, "12.5 MVA\n$X_d''$ = 0.14 pu", ha="center", va="top", fontsize=8)
    # motors (x=5.2)
    xM = 5.6
    ax.plot([xM, xM], [bus_y, 1.55], color=INK, lw=1.1)
    breaker(ax, xM, 2.8)
    ax.add_patch(Circle((xM, 1.2), 0.36, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(xM, 1.2, "M", ha="center", va="center", fontsize=10)
    ax.text(xM, 0.62, "15 MVA motors\n$X_M''$ = 0.17 pu", ha="center", va="top", fontsize=8)
    # fault on bus
    fault_symbol(ax, 1.95, bus_y - 0.05, s=0.75)
    ax.text(2.2, bus_y - 0.95, "F", fontsize=9, color="#D55E00", fontweight="bold")
    ax.text(3.3, 8.6, "(a) Single-line diagram", ha="center", fontsize=9.5, fontweight="bold")

    # ---- right: reactance diagram
    ax.plot([7.35, 7.35], [0.5, 8.2], color="#bbbbbb", lw=0.8)
    ax.text(10.6, 8.6, "(b) Reactance diagram, 100 MVA base", ha="center", fontsize=9.5, fontweight="bold")
    yref, yF = 1.0, 6.7
    xs = [8.3, 10.6, 12.9]
    ax.plot([xs[0], xs[-1]], [yref, yref], color=INK, lw=2.2)
    ax.text(10.6, yref - 0.2, "reference (neutral)", ha="center", va="top", fontsize=8)
    ax.plot([xs[0], xs[-1]], [yF, yF], color=INK, lw=2.2)
    ax.plot(xs[-1] + 0.05, yF, "o", color="#D55E00", ms=5)
    ax.text(10.6, yF + 0.25, "fault point F (bolted)", ha="center", fontsize=8, color="#D55E00")
    names = ["grid", "generator", "motors"]
    Xs = [None, 1.120, 1.133]
    Ik = [16.15, 4.69, 4.63]
    for k, x in enumerate(xs):
        ax.plot([x, x], [yref, 1.55], color=INK, lw=1.1)
        source(ax, x, 1.85, r=0.3)
        ax.text(x - 0.38, 1.85, "1.0", ha="right", va="center", fontsize=8)
        if k == 0:
            resistor_v(ax, x, 2.15, 3.55, label="j0.025", right=False)
            resistor_v(ax, x, 3.55, 5.0, label="j0.300", right=False)
            ax.plot([x, x], [5.0, yF], color=INK, lw=1.1)
        else:
            resistor_v(ax, x, 2.15, 4.6, label=f"j{Xs[k]:.3f}", right=False)
            ax.plot([x, x], [4.6, yF], color=INK, lw=1.1)
        arrow(ax, x + 0.22, 5.35, x + 0.22, 6.2, color=COLORS[0])
        ax.text(x + 0.3, 5.75, f"{Ik[k]:.2f} kA\n({names[k]})", fontsize=8, color=COLORS[0], va="center")
    ax.text(10.6, 7.6, r"$I_k''$ = 25.47 kA   (28.0 kA with $c$ = 1.1)", ha="center", fontsize=8.5,
            color=COLORS[1], fontweight="bold")
    save(fig, CH, "fig-19-2-plant-single-line")


# ---------------------------------------------------------------- 19.3
def star(ax, x, y, s=0.32, earthed=True, zn=False):
    for ang in (90, 210, 330):
        a = np.radians(ang)
        ax.plot([x, x + s * np.cos(a)], [y, y + s * np.sin(a)], color=INK, lw=1.3)
    if earthed:
        if zn:
            ax.plot([x, x], [y, y - 0.12], color=INK, lw=1.1)
            ax.add_patch(Rectangle((x - 0.07, y - 0.42), 0.14, 0.3, fc="white", ec=INK, lw=1.0))
            ax.text(x + 0.12, y - 0.27, "$Z_n$", fontsize=8, va="center")
            earth(ax, x, y - 0.42, s=0.13)
        else:
            ax.plot([x, x], [y, y - 0.25], color=INK, lw=1.1)
            earth(ax, x, y - 0.25, s=0.13)


def delta(ax, x, y, s=0.34):
    pts = np.array([[0, s * 0.62], [-s * 0.55, -s * 0.33], [s * 0.55, -s * 0.33]])
    ax.add_patch(Polygon(pts + [x, y], closed=True, fc="none", ec=INK, lw=1.3))


def switch(ax, x0, y0, x1, y1, closed):
    """Knife switch: pivot (filled) at (x0, y0), contact (open circle) at (x1, y1)."""
    if closed:
        ax.plot([x0, x1], [y0, y1], color=INK, lw=1.4, zorder=3)
    else:
        L = np.hypot(x1 - x0, y1 - y0)
        a = np.arctan2(y1 - y0, x1 - x0) + np.radians(30)
        ax.plot([x0, x0 + L * np.cos(a)], [y0, y0 + L * np.sin(a)], color=INK, lw=1.4, zorder=3)
    ax.plot(x0, y0, "o", ms=3.5, color=INK, zorder=4)
    ax.plot(x1, y1, "o", ms=3.8, mfc="white", mec=INK, zorder=4)


def fig_19_3():
    """Zero-sequence equivalents of two-winding transformers."""
    rows = [("YNyn", ("YN", "yn"), (True, False, True, False), False),
            ("YNd", ("YN", "d"), (True, False, False, True), False),
            ("Yd (star unearthed)", ("Y", "d"), (False, False, False, True), False),
            ("Dd", ("D", "d"), (False, True, False, True), False),
            ("YNyn, $Z_n$ in side-1 neutral", ("YNz", "yn"), (True, False, True, False), True)]
    # switch tuple: (series 1, shunt 1, series 2, shunt 2)
    fig, ax = schematic(6.8, 6.9, xlim=(0, 13.6), ylim=(-2.3, 12.2))
    ax.text(1.9, 11.75, "Winding connection", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(9.1, 11.75, "Zero-sequence equivalent circuit", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(1.25, 11.25, "side 1", ha="center", fontsize=7.5, color="#555555")
    ax.text(2.55, 11.25, "side 2", ha="center", fontsize=7.5, color="#555555")
    H = 2.4
    for k, (name, (w1, w2), sw, zn) in enumerate(rows):
        y0 = 11.0 - k * H     # top of row
        ax.text(0.1, y0 - 0.02, name, fontsize=8.5, va="top", ha="left", fontweight="bold")
        xa, xb, yy = 1.25, 2.55, y0 - 1.15
        for xc in (xa, xb):
            ax.add_patch(Circle((xc, yy), 0.55, fc="none", ec="#999999", lw=0.8))
        for xc, wd in ((xa, w1), (xb, w2)):
            if wd.lower().startswith("d"):
                delta(ax, xc, yy)
            else:
                star(ax, xc, yy, earthed="n" in wd.lower(), zn=wd.endswith("z"))
        # equivalent circuit
        yl, yr = y0 - 0.85, y0 - 2.05
        xP, xS = 4.8, 13.1
        s1, sh1, s2, sh2 = sw
        na, nb = 8.3, 11.0              # Z0 nodes
        ax.plot(xP, yl, "o", ms=4.5, mfc="white", mec=INK, zorder=5)
        ax.text(xP - 0.15, yl, "P", ha="right", va="center", fontsize=9)
        ax.plot(xS, yl, "o", ms=4.5, mfc="white", mec=INK, zorder=5)
        ax.text(xS + 0.15, yl, "S", ha="left", va="center", fontsize=9)
        if zn:
            resistor_h(ax, xP, 6.9, yl, label="$3Z_n$", lead=0.55)
        else:
            ax.plot([xP, 6.9], [yl, yl], color=INK, lw=1.1)
        switch(ax, 6.9, yl, 7.7, yl, s1)
        ax.plot([7.7, na], [yl, yl], color=INK, lw=1.1)
        resistor_h(ax, na, nb, yl, label="$Z_0$", lead=0.6)
        ax.plot([nb, 11.6], [yl, yl], color=INK, lw=1.1)
        switch(ax, 12.4, yl, 11.6, yl, s2)
        ax.plot([12.4, xS], [yl, yl], color=INK, lw=1.1)
        for xn, closed in ((na, sh1), (nb, sh2)):
            ax.plot(xn, yl, "o", ms=3.5, color=INK, zorder=5)
            ax.plot([xn, xn], [yl, yl - 0.32], color=INK, lw=1.1)
            ax.plot([xn, xn], [yr + 0.28, yr], color=INK, lw=1.1)
            switch(ax, xn, yr + 0.28, xn, yl - 0.32, closed)
        ax.plot([xP, xS], [yr, yr], color=INK, lw=2.0)
        ax.text(xS + 0.15, yr, "ref.", ha="left", va="center", fontsize=7.5)
        if k < len(rows) - 1:
            ax.plot([0.1, 13.5], [y0 - 2.32, y0 - 2.32], color="#dddddd", lw=0.8)
    ax.text(6.8, -1.45, "Two-switch convention: series switch closed for an earthed star (YN); shunt switch to\n"
            "reference closed for a delta; both open for an unearthed star.  Three-limb core with no delta:\n"
            "$Z_0$ is not infinite, about 0.3–1 pu through the tank flux path.",
            ha="center", va="center", fontsize=8, color="#333333")
    save(fig, CH, "fig-19-3-transformer-zero-sequence")



# ---------------------------------------------------------------- 19.4
def seq_box(ax, x, y, w, h, kind):
    """Sequence-network box with fault terminal F (top) and reference N (bottom)."""
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                fc="#EEF3F8", ec=INK, lw=1.0))
    xc = x + w / 2
    lab = {"1": "Positive", "2": "Negative", "0": "Zero"}[kind]
    ax.text(x + 0.1, y + h / 2, lab, fontsize=7.5, va="center", ha="left", color="#333333", rotation=90)
    # internal: N terminal (bottom) -> [source] -> Z -> F terminal (top)
    yb, yt = y, y + h
    if kind == "1":
        ax.plot([xc, xc], [yb, yb + 0.35], color=INK, lw=1.0)
        source(ax, xc, yb + 0.6, r=0.25)
        ax.text(xc + 0.3, yb + 0.6, "$V_f$", fontsize=8, va="center")
        resistor_v(ax, xc, yb + 0.85, yt, w=0.2, label="$Z_1$", fs=8)
    else:
        resistor_v(ax, xc, yb, yt, w=0.2, label=f"$Z_{kind}$", fs=8)
    ax.plot(xc, yt, "o", ms=3.5, color=INK, zorder=5)
    ax.plot(xc, yb, "o", ms=3.5, color=INK, zorder=5)
    ax.text(xc - 0.12, yt + 0.05, f"F$_{kind}$", fontsize=7.5, ha="right", va="bottom")
    ax.text(xc - 0.12, yb - 0.05, f"N$_{kind}$", fontsize=7.5, ha="right", va="top")
    return xc, yt, yb


def fig_19_4():
    """Sequence-network connections for SLG, LL and LLG faults."""
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 4.4))
    for a in axs:
        a.set_aspect("equal")
        a.axis("off")
        a.set_xlim(0, 4.2)
    C = COLORS[1]
    # (a) SLG: series loop  F1->N2? standard: N1-F1 -> F2..., boxes stacked
    a = axs[0]
    a.set_ylim(-0.4, 8.4)
    a.set_title("(a) Single line to ground", fontsize=9)
    w, h = 1.6, 1.9
    b1 = seq_box(a, 0.6, 5.6, w, h, "1")
    b2 = seq_box(a, 0.6, 3.1, w, h, "2")
    b0 = seq_box(a, 0.6, 0.6, w, h, "0")
    xc = b1[0]
    xr = 3.4
    # F1 -> right rail -> 3Zf -> down; chain: F1 to N2? Series: N1 to F2? Use loop: F1->3Zf->N0 ; F0->N2? simpler
    # Series loop: N1 – F2? We connect F1 to N2? no: standard picture: F1 -> F2 is wrong. Series: F1 → (3Zf) → N0 ;
    # F0 → N2 ; F2 → N1 closing loop. Use rails.
    a.plot([xc, xc, xr], [b1[1], 7.85, 7.85], color=INK, lw=1.1)
    resistor_v(a, xr, 7.85, 0.15, w=0.22, label="", right=True)
    a.text(xr + 0.18, 4.0, "$3Z_f$", fontsize=8.5, va="center")
    a.plot([xr, xc, xc], [0.15, 0.15, b0[2]], color=INK, lw=1.1)
    # F0 -> N2 and F2 -> N1 (short links between boxes)
    a.plot([xc, xc], [b0[1], b2[2]], color=INK, lw=1.1)
    a.plot([xc, xc], [b2[1], b1[2]], color=INK, lw=1.1)
    arrow(a, xr - 0.6, 7.85, xr - 0.15, 7.85, color=C)
    a.text(2.3, 8.0, "$I_1=I_2=I_0$", fontsize=8.5, color=C, ha="center", va="bottom")

    # (b) LL: positive and negative in parallel through Zf
    a = axs[1]
    a.set_ylim(-0.4, 8.4)
    a.set_title("(b) Line to line", fontsize=9)
    w, h = 1.5, 2.2
    b1 = seq_box(a, 0.1, 4.4, w, h, "1")
    b2 = seq_box(a, 2.45, 4.4, w, h, "2")
    yt = 7.5
    a.plot([b1[0], b1[0]], [b1[1], yt], color=INK, lw=1.1)
    a.plot([b2[0], b2[0]], [b2[1], yt], color=INK, lw=1.1)
    resistor_h(a, b1[0], b2[0], yt, label="$Z_f$")
    a.plot([b1[0], b1[0], b2[0], b2[0]], [b1[2], 3.9, 3.9, b2[2]], color=INK, lw=1.1)
    arrow(a, b1[0] - 0.0, 6.85, b1[0], 7.3, color=C)
    a.text(b1[0] + 0.1, 7.05, "$I_1$", fontsize=8.5, color=C, ha="left", va="center")
    arrow(a, b2[0], 6.85, b2[0], 7.3, color=C)
    a.text(b2[0] + 0.1, 7.05, "$I_2=-I_1$", fontsize=8.5, color=C, ha="left", va="center")
    seq_box(a, 1.3, 0.6, 1.5, 2.0, "0")
    a.text(2.05, 3.0, "not connected", ha="center", fontsize=7.5, color="#777777")

    # (c) LLG: all three in parallel, 3Zf with zero box
    a = axs[2]
    a.set_ylim(-0.4, 8.4)
    a.set_xlim(-0.1, 4.3)
    a.set_title("(c) Double line to ground", fontsize=9)
    w, h = 1.2, 2.4
    xs = [0.0, 1.45, 2.9]
    bb = [seq_box(a, xs[0], 2.6, w, h, "1"), seq_box(a, xs[1], 2.6, w, h, "2"), seq_box(a, xs[2], 2.6, w, h, "0")]
    ytop, ybot = 7.4, 1.4
    a.plot([bb[0][0], bb[2][0]], [ytop, ytop], color=INK, lw=1.1)
    a.plot([bb[0][0], bb[2][0]], [ybot, ybot], color=INK, lw=1.1)
    a.plot([bb[0][0]] * 2, [bb[0][1], ytop], color=INK, lw=1.1)
    a.plot([bb[1][0]] * 2, [bb[1][1], ytop], color=INK, lw=1.1)
    resistor_v(a, bb[2][0], ytop, bb[2][1], w=0.2)
    a.text(bb[2][0] + 0.16, (ytop + bb[2][1]) / 2, "$3Z_f$", fontsize=8, va="center")
    for b in bb:
        a.plot([b[0]] * 2, [b[2], ybot], color=INK, lw=1.1)
    for b, lab in zip(bb, ["$I_1$", "$I_2$", "$I_0$"]):
        arrow(a, b[0], b[1] + 0.2, b[0], b[1] + 0.75, color=C)
        a.text(b[0] + 0.08, b[1] + 0.5, lab, fontsize=8.5, color=C, ha="left", va="center")
    a.text(2.1, 0.7, "$I_1+I_2+I_0=0$", fontsize=8.5, color=C, ha="center")
    fig.subplots_adjust(wspace=0.05)
    save(fig, CH, "fig-19-4-sequence-connections")


# ---------------------------------------------------------------- 19.5
def fig_19_5():
    """IEC 60909 peak factor and DC decay."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    xr = np.logspace(0, 2, 400)
    kap = 1.02 + 0.98 * np.exp(-3 / xr)
    for lo, hi, lab, c in [(1, 5, "LV\ndistribution", "#E8F1F8"), (5, 15, "MV\ndistribution", "#FDF0E3"),
                           (15, 100, "near\ngenerators", "#E6F4EF")]:
        a1.axvspan(lo, hi, color=c, lw=0)
        xc = {1: 2.1, 5: 8.9, 15: 39}[lo]
        a1.text(xc, 1.04, lab, ha="center", va="bottom", fontsize=7, color="#444444")
    a1.semilogx(xr, kap, color=COLORS[0])
    for v in (3, 10, 20.3, 50):
        k = 1.02 + 0.98 * np.exp(-3 / v)
        a1.plot(v, k, "o", color=COLORS[1], ms=4.5, zorder=4)
        a1.annotate(f"{k:.2f}", (v, k), xytext=(-6, 6), textcoords="offset points", fontsize=8,
                    ha="right", va="bottom")
    a1.set_xlim(1, 100)
    a1.set_ylim(1.0, 2.0)
    a1.set_xlabel("$X/R$ at the fault")
    a1.set_ylabel(r"Peak factor $\kappa$")
    a1.set_title(r"(a) $\kappa = 1.02 + 0.98\,e^{-3R/X}$", fontsize=9.5)
    a1.set_xticks([1, 3, 10, 30, 100])
    a1.set_xticklabels(["1", "3", "10", "30", "100"])

    t = np.linspace(0, 150, 601)
    w = 2 * np.pi * 50
    for (X_R, c, extra) in [(40, COLORS[2], ""), (20.3, COLORS[1], ""),
                            (14.1, INK, ", IEC std"), (10, COLORS[0], "")]:
        tau = X_R / w * 1e3
        y = 100 * np.exp(-t / tau)
        a2.plot(t, y, color=c, lw=2.2 if X_R == 14.1 else 1.6, ls="--" if X_R == 14.1 else "-",
                label=f"X/R {X_R:g} (τ {tau:.0f} ms{extra})")
        v50 = 100 * np.exp(-50 / tau)
        a2.plot(50, v50, "o", color=c, ms=4)
        a2.text(53, v50, f"{v50:.0f} %", fontsize=7.5, va="center", color=c)
    a2.axvline(50, color="#777777", ls=":", lw=1.0)
    a2.text(52, 1.5, "contact\nseparation", fontsize=7.5, ha="left", va="bottom", color="#555555")
    a2.legend(loc="upper right", fontsize=7, handlelength=1.8)
    a2.set_xlim(0, 150)
    a2.set_ylim(0, 100)
    a2.set_xlabel("Time after fault inception (ms)")
    a2.set_ylabel("DC component (% of symmetrical peak)")
    a2.set_title("(b) Decay of the DC offset", fontsize=9.5)
    fig.tight_layout(w_pad=1.0)
    save(fig, CH, "fig-19-5-peak-factor-dc-decay")


# ---------------------------------------------------------------- 19.6
def fig_19_6():
    """One-ended impedance and two-ended travelling-wave fault location."""
    fig = plt.figure(figsize=(6.8, 5.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], height_ratios=[1, 1.25], hspace=0.38, wspace=0.28)
    # top-left: line schematic
    a = fig.add_subplot(gs[0, 0])
    a.set_xlim(-8, 68)
    a.set_ylim(-4.2, 5)
    a.axis("off")
    a.plot([0, 60], [2, 2], color=INK, lw=1.6)
    for x, n in ((0, "A"), (60, "B")):
        a.plot([x, x], [0.6, 3.4], color=INK, lw=4)
        a.text(x, 3.8, n, ha="center", fontsize=10, fontweight="bold")
        a.text(x, 0.1, f"{x} km", ha="center", va="top", fontsize=8)
    a.plot([25, 25], [2, 0.9], color=INK, lw=1.1)
    a.add_patch(Rectangle((24.0, -0.6), 2.0, 1.5, fc="white", ec=INK, lw=1.1))
    a.text(27, 0.35, "$R_f$ = 5 Ω", fontsize=8, va="center")
    earth(a, 25, -0.6, s=1.2)
    a.text(27, -1.1, "fault at 25 km", fontsize=8, va="center", color="#D55E00")
    a.annotate("", xy=(21, 2.55), xytext=(9, 2.55), arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.3))
    a.text(13.5, 2.75, "$I_A$", color=COLORS[0], fontsize=9)
    a.annotate("", xy=(29, 2.55), xytext=(48, 2.55), arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.3))
    a.text(40, 2.75, "$I_B$", color=COLORS[1], fontsize=9)
    a.text(30, -3.4, "132 kV, $z_1$ = 0.12 + j0.40 Ω/km;  $I_f/I_A$ = 1.5∠−10°",
           ha="center", fontsize=7.8)
    a.set_title("(a) Line and fault", fontsize=9.5, loc="left")

    # top-right: impedance plane
    b = fig.add_subplot(gs[0, 1])
    ang = np.arctan2(0.40, 0.12)


    b.plot([0, 3.6], [0, 12], color=INK, lw=1.4)
    b.text(1.6, 2.4, "line impedance\nlocus, 73.3°", fontsize=7.5)
    Zt = 3.0 + 10.0j
    Zr = 7.5 * np.exp(-1j * np.radians(10))
    Za = Zt + Zr
    b.plot(Zt.real, Zt.imag, "o", color=COLORS[2], ms=5)
    b.text(Zt.real + 0.3, Zt.imag + 0.6, "true 3.0 + j10.0", fontsize=7.5, color=COLORS[2])
    b.annotate("", xy=(Za.real, Za.imag), xytext=(Zt.real, Zt.imag),
               arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.2))
    b.text(7.0, 9.55, "+7.5∠−10° Ω", fontsize=7.5, va="bottom", color=COLORS[1])
    b.plot(Za.real, Za.imag, "s", color=COLORS[1], ms=5)
    b.text(Za.real, Za.imag - 0.5, "apparent\n10.39 + j8.70", fontsize=7.5, color=COLORS[1],
           ha="center", va="top")
    xl = Za.imag / np.tan(ang)
    b.plot([xl, Za.real], [Za.imag, Za.imag], "--", color=COLORS[3], lw=1.1)
    b.plot(xl, Za.imag, "o", color=COLORS[3], ms=4)
    b.text(4.0, 6.7, "reactance method:\n21.7 km (error 3.3 km)", fontsize=7, color=COLORS[3],
           ha="left", va="top")
    b.set_xlim(0, 12)
    b.set_ylim(0, 12)
    b.set_aspect("equal")
    b.set_xlabel("R (Ω)", fontsize=8.5)
    b.set_ylabel("X (Ω)", fontsize=8.5)
    b.tick_params(labelsize=7.5)
    b.set_title("(b) One-ended impedance", fontsize=9.5, loc="left")

    # bottom: lattice diagram
    c = fig.add_subplot(gs[1, :])
    v = 2.95e5 * 1e-6  # km per microsecond
    xf, Lk = 25.0, 60.0
    tA, tB = xf / v, (Lk - xf) / v


    c.plot([xf, 0], [0, tA], color=COLORS[0], lw=1.8)
    c.plot([xf, Lk], [0, tB], color=COLORS[1], lw=1.8)
    # reflections (faint): wave reflects at A, returns to fault, reflects back
    t1 = tA
    c.plot([0, xf], [t1, t1 + tA], color=COLORS[0], lw=0.9, alpha=0.35)
    c.plot([xf, 0], [t1 + tA, t1 + 2 * tA], color=COLORS[0], lw=0.9, alpha=0.35)
    c.plot([Lk, xf], [tB, 2 * tB], color=COLORS[1], lw=0.9, alpha=0.35)
    c.plot([xf, Lk], [2 * tB, 3 * tB], color=COLORS[1], lw=0.9, alpha=0.35)
    c.plot([xf, Lk], [2 * tA, 2 * tA + tB], color=COLORS[0], lw=0.9, alpha=0.35, ls="--")
    c.axvline(0, color=INK, lw=3)
    c.axvline(Lk, color=INK, lw=3)
    c.axvline(xf, color="#D55E00", lw=0.8, ls=":")
    c.plot(xf, 0, marker=(5, 1, 0), color="#D55E00", ms=11)
    for t_, x_, ha, dx in ((tA, 0, "left", 1.2), (tB, Lk, "right", -1.2)):
        c.plot(x_, t_, "o", color=INK, ms=5, zorder=5)
        c.annotate(f"$t$ = {t_:.1f} µs", (x_, t_), xytext=(x_ + dx * 2.2, t_ + 2), fontsize=8.5,
                   ha=ha, va="center")
    # GPS clocks
    for x_ in (1.6, Lk - 1.6):
        c.plot(x_, 28, "o", ms=17, mfc="white", mec=INK, mew=1.0, zorder=6)
        c.plot([x_, x_], [28, 20], color=INK, lw=1.0, zorder=7)
        c.plot([x_, x_ + 0.6], [28, 28], color=INK, lw=1.0, zorder=7)
        c.text(x_ + (1.4 if x_ < 30 else -1.4), 28, "GPS clock", fontsize=7.5, va="center",
               ha="left" if x_ < 30 else "right")
    c.set_xlim(0, 60)
    c.set_ylim(250, 0)
    c.set_xlabel("Distance from A (km)")
    c.set_ylabel("Time (µs)")
    c.text(42, 175, r"$d_A=\dfrac{\ell+v(t_A-t_B)}{2}=\dfrac{60+0.295(84.7-118.6)}{2}=25.0$ km",
           fontsize=8.5, ha="center", bbox=dict(fc="white", ec="#cccccc"))
    c.text(13, 225, "faint lines: reflections\nbetween fault and terminals", fontsize=7.5, color="#666666",
           ha="center")
    c.set_title("(c) Two-ended travelling-wave timing, $v$ = 2.95×10$^5$ km/s", fontsize=9.5, loc="left")
    save(fig, CH, "fig-19-6-fault-location-methods")


if __name__ == "__main__":
    fig_19_1()
    fig_19_2()
    fig_19_3()
    fig_19_4()
    fig_19_5()
    fig_19_6()
