"""Figures for Chapter 7 — Synchronous Machines.

Run from the repository root:  python figures/scripts/ch07.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle, Polygon, Arc
from matplotlib.transforms import Affine2D
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

from figstyle import new_fig, save, COLORS, INK

BLUE, ORANGE, GREEN, PINK, YELLOW = COLORS[0], COLORS[1], COLORS[2], COLORS[3], COLORS[4]
STEEL = "#D9DEE4"
STEEL_DARK = "#B9C1CA"


def _rot_rect(ax, r_in, r_out, width, ang_deg, **kw):
    """Rectangle spanning radius r_in..r_out, centred on angle ang (deg)."""
    rect = Rectangle((r_in, -width / 2), r_out - r_in, width, **kw)
    rect.set_transform(Affine2D().rotate_deg(ang_deg) + ax.transData)
    ax.add_patch(rect)
    return rect


def _pol(r, a_deg):
    a = np.radians(a_deg)
    return r * np.cos(a), r * np.sin(a)


# ---------------------------------------------------------------------------
def fig_7_1():
    """Cylindrical and salient-pole rotor cross-sections."""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.8, 3.9))
    for ax in (axa, axb):
        ax.set_aspect("equal")
        ax.axis("off")

    # ---------------- (a) two-pole cylindrical rotor ----------------
    ax = axa
    Rso, Rb, Rr = 1.0, 0.60, 0.525          # stator outer (schematic), bore 1.2 m, rotor 1.05 m
    ax.add_patch(Circle((0, 0), Rso, fc=STEEL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), Rb, fc="white", ec=INK, lw=1.0))
    # 48 armature slots
    for k in range(48):
        a = k * 7.5 + 3.75
        _rot_rect(ax, Rb, Rb + 0.085, 0.032, a, fc=BLUE, ec="none")
    # rotor body
    ax.add_patch(Circle((0, 0), Rr, fc=STEEL_DARK, ec=INK, lw=1.0))
    # field slots on 2/3 of circumference: pole faces (unslotted) centred on 0 and 180 deg
    for side, centre in ((+1, 90), (-1, 270)):
        for k in range(8):
            a = centre - 52.5 + 15 * k
            _rot_rect(ax, Rr - 0.13, Rr, 0.045, a, fc=ORANGE, ec="none")
            x, y = _pol(Rr - 0.065, a)
            # current direction: dot on upper half, cross on lower half
            sym = "•" if side > 0 else "×"
            ax.text(x, y, sym, ha="center", va="center", fontsize=6, color="white")
    ax.add_patch(Circle((0, 0), 0.07, fc="#888888", ec=INK, lw=0.6))  # shaft
    ax.text(Rr - 0.17, 0, "N", ha="right", va="center", fontsize=12, weight="bold", color=INK)
    ax.text(-Rr + 0.17, 0, "S", ha="left", va="center", fontsize=12, weight="bold", color=INK)
    # axes
    ax.plot([-1.12, 1.12], [0, 0], ls="-.", lw=0.9, color=PINK)
    ax.plot([0, 0], [-1.12, 1.12], ls="-.", lw=0.9, color=GREEN)
    ax.text(1.13, 0.03, "d", color=PINK, fontsize=10, ha="left", va="bottom")
    ax.text(0.03, 1.13, "q", color=GREEN, fontsize=10, ha="left", va="bottom")
    # labels
    kw = dict(fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    x, y = _pol(Rb + 0.05, 131.25)
    ax.annotate("armature winding\n(48 slots)", xy=(x, y), xytext=(-1.25, 1.12), ha="left", va="center", **kw)
    x, y = _pol(Rr - 0.06, 52.5 - 15 * 0 + 0)
    ax.annotate("field winding", xy=_pol(Rr - 0.07, 232.5), xytext=(-1.25, -1.05), ha="left", va="center", **kw)
    ax.annotate("unslotted\npole face", xy=_pol(Rr - 0.01, -20), xytext=(0.62, -1.12), ha="left", va="center", **kw)
    ax.annotate("air gap 75 mm", xy=_pol(0.5625, 60), xytext=(0.55, 1.12), ha="left", va="center", **kw)
    ax.text(0, -1.3, "retaining rings hold the end windings\nat each rotor end (outside this section)",
            ha="center", va="top", fontsize=7.5, color="#555555", style="italic")
    ax.text(0, 1.38, "(a) two-pole cylindrical rotor\nbore 1.2 m, rotor 1.05 m",
            ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-1.3, 1.45)
    ax.set_ylim(-1.55, 1.7)

    # ---------------- (b) 12-pole salient-pole rotor ----------------
    ax = axb
    Rb, Rso = 3.0, 3.45
    g0, gt = 0.08, 0.24                 # 20 mm and 60 mm drawn x4
    half_arc = 10.5                     # pole-arc half angle (deg), pole pitch 30 deg
    ax.add_patch(Circle((0, 0), Rso, fc=STEEL, ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), Rb, fc="white", ec=INK, lw=1.0))
    for k in range(108):
        _rot_rect(ax, Rb, Rb + 0.16, 0.06, k * 360 / 108 + 1.67, fc=BLUE, ec="none")
    # spider: hub, arms, rim
    ax.add_patch(Circle((0, 0), 2.25, fc=STEEL_DARK, ec=INK, lw=0.9))
    ax.add_patch(Circle((0, 0), 1.95, fc="white", ec=INK, lw=0.9))
    for k in range(6):
        _rot_rect(ax, 0.45, 2.0, 0.22, k * 60 + 15, fc=STEEL_DARK, ec=INK, lw=0.6)
    ax.add_patch(Circle((0, 0), 0.5, fc=STEEL_DARK, ec=INK, lw=0.9))
    ax.add_patch(Circle((0, 0), 0.2, fc="#888888", ec=INK, lw=0.6))
    for k in range(12):
        c = 90 + 30 * k
        # pole body
        _rot_rect(ax, 2.25, 2.66, 0.62, c, fc=STEEL_DARK, ec=INK, lw=0.6)
        # field coil either side of the body
        for s in (+1, -1):
            a_off = np.degrees(np.arctan2(s * 0.43, 2.47))
            _rot_rect(ax, 2.30, 2.62, 0.20, c + a_off * 1.0, fc=ORANGE, ec=INK, lw=0.4)
        # pole shoe: inner chord at r=2.64, outer surface with growing gap
        phi = np.linspace(-half_arc, half_arc, 41)
        g = g0 + (gt - g0) * (phi / half_arc) ** 2
        outer = [_pol(Rb - gi, c + p) for gi, p in zip(g, phi)]
        inner = [_pol(2.64, c + p) for p in phi[::-1] * 0.95]
        ax.add_patch(Polygon(outer + inner, closed=True, fc=STEEL_DARK, ec=INK, lw=0.6))
        # five damper bars
        for p in np.linspace(-7.5, 7.5, 5):
            gi = g0 + (gt - g0) * (p / half_arc) ** 2
            ax.add_patch(Circle(_pol(Rb - gi - 0.09, c + p), 0.035, fc=YELLOW, ec=INK, lw=0.3))
        ax.text(*_pol(2.47, c), "N" if k % 2 == 0 else "S", ha="center", va="center",
                fontsize=6.5, weight="bold", color=INK)
    # axes for one pole pair (pole at 90 deg and the next at 120 deg)
    for ang, col, lab in ((90, PINK, "d"), (105, GREEN, "q")):
        x0, y0 = _pol(0.55, ang)
        x1, y1 = _pol(3.75, ang)
        ax.plot([x0, x1], [y0, y1], ls="-.", lw=0.9, color=col)
        ax.text(x1, y1 + 0.05, lab, color=col, fontsize=10, ha="center", va="bottom")
    kw = dict(fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("armature\nwinding", xy=_pol(3.1, 30), xytext=(3.75, 2.9), ha="left", va="center", **kw)
    ax.annotate("field coil", xy=_pol(2.46, 30 + 9.5), xytext=(3.75, 1.4), ha="left", va="center", **kw)
    ax.annotate("damper bars", xy=_pol(2.83, 0), xytext=(3.75, -0.6), ha="left", va="center", **kw)
    ax.annotate("spider", xy=_pol(1.2, -45), xytext=(3.75, -2.2), ha="left", va="center", **kw)
    ax.annotate("rim", xy=_pol(2.1, -40), xytext=(3.75, -3.2), ha="left", va="center", **kw)
    ax.text(0, -3.75, "air gap 20 mm at pole centre, 60 mm at tips\n(drawn 4× enlarged)",
            ha="center", va="top", fontsize=7.5, color="#555555", style="italic")
    ax.text(0, 4.35, "(b) 12-pole salient-pole rotor\nbore 6 m", ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-3.6, 5.6)
    ax.set_ylim(-4.6, 5.0)
    fig.subplots_adjust(wspace=0.05, left=0.01, right=0.99)
    save(fig, "07", "fig-7-1-rotor-cross-sections")


# ---------------------------------------------------------------------------
def _phasor(ax, x0, y0, x1, y1, color, lw=1.8):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=11,
                                shrinkA=0, shrinkB=0))


def fig_7_2():
    """Cylindrical-rotor generator phasor diagrams at 0.8 lag, unity, 0.8 lead."""
    Xs = 1.65
    cases = [("(a) 0.8 lagging\nover-excited", -np.degrees(np.arccos(0.8))),
             ("(b) unity pf", 0.0),
             ("(c) 0.8 leading\nunder-excited", np.degrees(np.arccos(0.8)))]
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 3.0))
    for ax, (title, phi) in zip(axs, cases):
        V = 1.0 + 0j
        I = np.exp(1j * np.radians(phi))
        jXI = 1j * Xs * I
        Ef = V + jXI
        d = np.degrees(np.angle(Ef))
        _phasor(ax, 0, 0, V.real, V.imag, INK)
        _phasor(ax, 0, 0, I.real, I.imag, ORANGE)
        _phasor(ax, V.real, V.imag, Ef.real, Ef.imag, GREEN)
        _phasor(ax, 0, 0, Ef.real, Ef.imag, BLUE, lw=2.2)
        # labels
        ax.text(0.72, -0.05, r"$\mathbf{V}=1.0$", ha="center", va="top", fontsize=8.5)
        ilab = r"$\mathbf{I}=1.0$"
        if phi < 0:
            ax.text(I.real + 0.05, I.imag - 0.02, ilab, ha="left", va="top", fontsize=8.5, color=ORANGE)
        elif phi == 0:
            ax.text(0.72, -0.24, ilab + " (in phase)", ha="center", va="top", fontsize=8.5, color=ORANGE)
        else:
            ax.text(I.real + 0.04, I.imag - 0.06, ilab, ha="left", va="top", fontsize=8.5, color=ORANGE)
        mid = (V + Ef) / 2
        if phi < 0:
            ax.text(mid.real + 0.16, mid.imag - 0.05, r"$jX_s\mathbf{I}$" + "\n1.65",
                    ha="left", va="center", fontsize=8.5, color=GREEN)
        elif phi == 0:
            ax.text(mid.real + 0.08, mid.imag, r"$jX_s\mathbf{I}$" + "\n1.65",
                    ha="left", va="center", fontsize=8.5, color=GREEN)
        else:
            ax.text(mid.real + 0.12, mid.imag + 0.12, r"$jX_s\mathbf{I}$" + "\n1.65",
                    ha="left", va="bottom", fontsize=8.5, color=GREEN)
        mE = Ef * 0.6
        ax.text(mE.real - 0.08, mE.imag + 0.04,
                r"$\mathbf{E}_f$" + f"={abs(Ef):.2f}", ha="right", va="bottom", fontsize=8.5, color=BLUE)
        # delta arc
        r = 0.42
        ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=0, theta2=d, color=BLUE, lw=1.0))
        if phi > 0:
            ax.text(-0.06, 0.28, rf"$\delta$={d:.1f}°", fontsize=8, color=BLUE, ha="right", va="center")
        else:
            ax.text(*_pol(r + 0.05, d / 2), rf"$\delta$={d:.1f}°", fontsize=8, color=BLUE,
                    ha="left", va="center")
        # phi arc
        if phi != 0:
            r2 = 0.26
            ax.add_patch(Arc((0, 0), 2 * r2, 2 * r2, theta1=min(0, phi), theta2=max(0, phi), color=ORANGE, lw=1.0))
            ax.text(*_pol(r2 + 0.03, phi * 0.5), r"$\varphi$", fontsize=9,
                    color=ORANGE, ha="left", va="center")
        ax.set_xlim(-0.6, 2.15)
        ax.set_ylim(-0.75, 1.75)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.axhline(0, color="#BBBBBB", lw=0.5, zorder=0)
        ax.set_title(title, fontsize=9.5)
    fig.text(0.5, 0.01, r"Same scale in all panels; $X_s$ = 1.65 pu, $|\mathbf{I}|$ = 1.0 pu, $R_a$ neglected",
             ha="center", va="bottom", fontsize=8, color="#555555")
    fig.subplots_adjust(left=0.01, right=0.99, wspace=0.08, bottom=0.07, top=0.86)
    save(fig, "07", "fig-7-2-cylindrical-phasor-diagrams")


# ---------------------------------------------------------------------------
def _occ():
    """Smooth saturating OCC (kV line) fitted to the test points of the text:
    air-gap slope 11 kV/170 A, 11 kV at 200 A, 13 kV at 300 A, about 13.9 kV at 478-500 A."""
    a, vs, n = 11 / 170, 14.142, 3.413
    return lambda i: a * np.asarray(i) / (1 + (a * np.asarray(i) / vs) ** n) ** (1 / n)


# ---------------------------------------------------------------------------
def fig_7_3():
    """OCC, SCC and air-gap line of the 20 MVA, 11 kV generator."""
    occ = _occ()
    If = np.linspace(0, 500, 501)
    fig, ax = new_fig(6.4, 3.9)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax.plot(If, occ(If), color=BLUE, label="OCC (line voltage)")
    ag = 11 / 170 * If
    m = ag <= 15
    ax.plot(If[m], ag[m], ls="--", color=BLUE, lw=1.2, label="air-gap line")
    Isc = 1050 / 330 * If
    ax2.plot(If, Isc, color=ORANGE, label="SCC (armature current)")
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 15)
    ax2.set_ylim(0, 1600)
    ax.set_xlabel("Field current $I_f$ (A)")
    ax.set_ylabel("Open-circuit line voltage (kV)", color=BLUE)
    ax2.set_ylabel("Short-circuit armature current (A)", color=ORANGE)
    # markers
    ax.plot([200, 200], [0, 11], color="#666666", lw=0.8, ls=":")
    ax.plot([0, 200], [11, 11], color="#666666", lw=0.8, ls=":")
    ax.plot(200, 11, "o", color=BLUE, ms=5)
    ax2.plot([330, 330], [0, 1050], color="#666666", lw=0.8, ls=":")
    ax2.plot([330, 500], [1050, 1050], color="#666666", lw=0.8, ls=":")
    ax2.plot(330, 1050, "o", color=ORANGE, ms=5)
    ax.text(203, 0.4, "200 A", fontsize=8, ha="left")
    ax.text(333, 0.4, "330 A", fontsize=8, ha="left")
    ax.text(5, 11.15, "rated 11 kV", fontsize=8, va="bottom")
    ax2.text(495, 1065, "rated 1050 A", fontsize=8, va="bottom", ha="right")
    ax.annotate("SCR = 200/330 = 0.61", xy=(265, 2.3), ha="center", fontsize=9,
                bbox=dict(fc="white", ec="#999999", lw=0.6, boxstyle="round,pad=0.3"))
    ax.annotate("", xy=(330, 1.6), xytext=(200, 1.6),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=8))
    ax.text(178, 12.6, "air-gap line", fontsize=8, color=BLUE, ha="right")
    ax.text(420, 13.95, "OCC", fontsize=8.5, color=BLUE, ha="center", va="bottom")
    ax2.text(430, 1290, "SCC", fontsize=8.5, color=ORANGE, ha="left", va="center")
    save(fig, "07", "fig-7-3-occ-scc")


# ---------------------------------------------------------------------------
def fig_7_4():
    """Salient-pole power-angle curves."""
    Ef, Xd, Xq, V = 1.680, 1.0, 0.65, 1.0
    a = Ef * V / Xd
    b = V ** 2 / 2 * (1 / Xq - 1 / Xd)
    d = np.linspace(0, 180, 1801)
    r = np.radians(d)
    P1, P2 = a * np.sin(r), b * np.sin(2 * r)
    P = P1 + P2
    k = P.argmax()
    dmax, Pmax = d[k], P[k]
    Pf = lambda x: a * np.sin(np.radians(x)) + b * np.sin(np.radians(2 * x)) - 0.9
    d1 = brentq(Pf, 1, dmax)
    d2 = brentq(Pf, dmax, 179)
    fig, ax = new_fig(6.4, 3.8)
    ax.axvspan(dmax, 180, color="#F3E1D6", zorder=0)
    ax.text(150, 1.9, "steady-state\nunstable", ha="center", va="top", fontsize=8.5, color=ORANGE)
    ax.axhline(0, color="#999999", lw=0.6)
    ax.plot(d, P1, ls="--", color=BLUE, lw=1.4)
    ax.plot(d, P2, ls=":", color=GREEN, lw=1.6)
    ax.plot(d, P, color=INK, lw=2.0)
    ax.axhline(0.9, color=PINK, lw=1.0)
    ax.text(178, 0.93, "$P$ = 0.9 pu", color=PINK, ha="right", va="bottom", fontsize=8.5)
    ax.plot(d1, 0.9, "o", color=INK, ms=6, zorder=5)
    ax.plot(d2, 0.9, "o", mfc="white", mec=INK, ms=6, zorder=5)
    ax.annotate(f"stable, $\\delta$ = {d1:.1f}°", xy=(d1, 0.9), xytext=(d1 + 3, 0.55),
                fontsize=8.5, arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.annotate(f"unstable, $\\delta$ = {d2:.0f}°", xy=(d2, 0.9), xytext=(d2 - 18, 0.45),
                fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.plot(dmax, Pmax, "s", color=INK, ms=5)
    ax.annotate(f"pull-out {Pmax:.3f} pu at {dmax:.1f}°", xy=(dmax, Pmax), xytext=(10, 1.88),
                fontsize=8.5, arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.text(143, 1.12, r"$1.680\,\sin\delta$", color=BLUE, fontsize=9, ha="left")
    ax.text(28, 0.30, r"$0.269\,\sin2\delta$", color=GREEN, fontsize=9, ha="left")
    ax.text(116, 1.36, "total", color=INK, fontsize=9, ha="left")
    ax.set_xlim(0, 180)
    ax.set_ylim(-0.4, 2.0)
    ax.set_xticks(np.arange(0, 181, 30))
    ax.set_xlabel(r"Load angle $\delta$ (electrical degrees)")
    ax.set_ylabel("Active power $P$ (pu)")
    save(fig, "07", "fig-7-4-power-angle-curves")


# ---------------------------------------------------------------------------
def fig_7_5():
    """V-curves of a synchronous motor, Xs = 1.2 pu."""
    Xs, V = 1.2, 1.0
    fig, ax = new_fig(6.4, 4.0)
    cols = [BLUE, GREEN, ORANGE]
    for P, c in zip((0.0, 0.4, 0.8), cols):
        Elim = max(P * Xs / V, 0.4)
        E = np.linspace(Elim, 2.3, 600)
        # motor: Ef = V - jXs I, I = P + jIq (Iq > 0 leading)
        s = np.sqrt(np.clip(E ** 2 - (Xs * P) ** 2, 0, None))
        Iq = (s - V) / Xs
        I = np.hypot(P, Iq)
        ax.plot(E, I, color=c, lw=1.8)
        ax.text(2.31, I[-1] + {0.0: -0.035, 0.4: 0.02, 0.8: 0.0}[P], f"$P$ = {P:.1f}", color=c,
                fontsize=8.5, va="center", ha="left")
    # unity-pf locus
    Pp = np.linspace(0, 0.9, 100)
    ax.plot(np.sqrt(1 + (Xs * Pp) ** 2), Pp, ls="--", color="#555555", lw=1.1)
    ax.text(1.43, 0.86, "unity-pf\nlocus", fontsize=8, color="#555555", ha="left", va="bottom")
    # stability-limit locus (delta = 90 deg): Ef = P Xs, Iq = -V/Xs
    Ps = np.linspace(0.0, 0.9, 100)
    Es = Ps * Xs
    m = Es >= 0.4
    ax.plot(Es[m], np.hypot(Ps[m], V / Xs), ls=":", color=PINK, lw=1.8)
    ax.text(0.42, 1.17, "stability limit\n($\\delta$ = 90°)", fontsize=8, color=PINK, ha="left", va="bottom")
    for P in (0.4, 0.8):
        ax.plot(P * Xs, np.hypot(P, V / Xs), "o", color=PINK, ms=3.5)
    # check points from text
    ax.plot([1.0, 1.97], [1.0, 1.0], "o", mfc="white", mec=ORANGE, ms=4.5)
    ax.text(0.97, 0.99, "0.8 lag", fontsize=7.5, ha="right", va="center", color=ORANGE)
    ax.text(1.97, 1.03, "0.8 lead", fontsize=7.5, ha="center", va="bottom", color=ORANGE)
    ax.text(1.03, 0.33, "under-excited\n(lagging current)", fontsize=8.5, ha="right", va="center", color="#444444")
    ax.text(1.85, 0.08, "over-excited\n(leading current)", fontsize=8.5, ha="center", va="bottom", color="#444444")
    ax.set_xlim(0.4, 2.3)
    ax.set_ylim(0, 1.3)
    ax.set_xlabel(r"Excitation EMF $E_f$ (pu, $\propto$ field current)")
    ax.set_ylabel("Armature current $I$ (pu)")
    save(fig, "07", "fig-7-5-v-curves")


# ---------------------------------------------------------------------------
def fig_7_6():
    """Capability chart of the 20 MVA, 0.8 pf generator."""
    Xs, V = 1.65, 1.0
    Ef = abs(1 + 1j * Xs * (0.8 - 0.6j))
    c0, R = -V ** 2 / Xs, Ef * V / Xs
    fig, ax = new_fig(6.4, 4.2)
    # region: inside armature circle, inside field circle, P <= 0.8, right of UEL
    Q = np.linspace(-0.8, 1.0, 1201)
    Pa = np.sqrt(np.clip(1 - Q ** 2, 0, None)) * (np.abs(Q) <= 1)
    Pf = np.sqrt(np.clip(R ** 2 - (Q - c0) ** 2, 0, None))
    # UEL line Q = -0.45 + (0.15/0.8) P: allowed region lies to its right
    Puel = np.where(Q < -0.3, np.clip((Q + 0.45) / 0.15 * 0.8, 0, None), 10.0)
    Ptop = np.minimum.reduce([Pa, Pf, np.full_like(Q, 0.8), Puel])
    ax.fill_between(Q, 0, Ptop, where=Ptop > 0, color="#DCEAF5", zorder=0, label="allowed region")
    th = np.linspace(0, np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=BLUE, lw=1.6)
    thf = np.linspace(0, np.pi / 2, 400)
    xf, yf = c0 + R * np.cos(thf), R * np.sin(thf)
    m = (xf >= -0.8) & (yf <= 1.1)
    ax.plot(xf[m], yf[m], color=ORANGE, lw=1.6)
    ax.axhline(0.8, color=GREEN, lw=1.4)
    ax.plot([-0.45, -0.3], [0, 0.8], color=PINK, lw=1.6)
    ax.plot([c0, c0], [0, 1.1], color=PINK, lw=0.8, ls=":")
    ax.text(c0 + 0.02, 1.09, "theoretical stability\nlimit ($\\delta$ = 90°)", fontsize=7.5, color=PINK,
            ha="left", va="top")
    ax.plot(c0, 0, "+", color=ORANGE, ms=8, mew=1.2)
    ax.text(c0 - 0.015, 0.03, r"$-V^2/X_s$", fontsize=8, color=ORANGE, ha="right", va="bottom")
    ax.plot(c0 + R, 0, "o", color=ORANGE, ms=4)
    ax.text(c0 + R - 0.03, 0.03, f"{c0 + R:.2f}", fontsize=8, color=ORANGE, ha="right", va="bottom")
    ax.plot(0.6, 0.8, "o", color=INK, ms=6, zorder=5)
    ax.annotate("rated point\n(0.6, 0.8)", xy=(0.6, 0.8), xytext=(0.66, 0.95), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    for q, lab in ((0.496, "0.85 lag"), (-0.263, "0.95 lead")):
        ax.plot([q, q], [0.76, 0.84], color=INK, lw=1.8)
        ax.text(q + 0.015, 0.735, lab, fontsize=7.5, ha="left" if q < 0 else "center", va="top")
    ax.text(0.86, 0.36, "armature\nlimit", color=BLUE, fontsize=8.5, ha="center")
    yq = np.sqrt(R ** 2 - (0.42 - c0) ** 2)
    ax.annotate("field limit", xy=(0.42, yq), xytext=(0.18, 1.05), color=ORANGE, fontsize=8.5, ha="right",
                va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    ax.text(0.02, 0.82, "prime-mover limit", color=GREEN, fontsize=8.5, ha="left", va="bottom")
    ax.text(-0.37, 0.25, "under-excitation\nlimit (UEL)", color=PINK, fontsize=8, ha="left", va="center")
    ax.text(0.15, 0.35, "allowed\noperation", color=BLUE, fontsize=9, ha="center")
    ax.axvline(0, color="#999999", lw=0.6)
    ax.set_xlim(-0.8, 1.0)
    ax.set_ylim(0, 1.1)
    ax.set_aspect("equal")
    ax.set_xlabel("Reactive power $Q$ (pu)\n← absorbing (under-excited)        supplying (over-excited) →")
    ax.set_ylabel("Active power $P$ (pu)")
    save(fig, "07", "fig-7-6-capability-chart")


if __name__ == "__main__":
    fig_7_1()
    fig_7_2()
    fig_7_3()
    fig_7_4()
    fig_7_5()
    fig_7_6()
