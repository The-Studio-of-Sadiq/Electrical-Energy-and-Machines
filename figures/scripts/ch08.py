"""Figures for Chapter 8 — Special Electrical Machines.

Run from the repository root:  python figures/scripts/ch08.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle, Polygon, FancyArrowPatch
from matplotlib.transforms import Affine2D
from scipy.interpolate import PchipInterpolator

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

BLUE, ORANGE, GREEN, PINK, YELLOW, SKY = COLORS[:6]
STEEL = "#D9DEE4"
STEEL_DARK = "#B9C1CA"
MAG_N, MAG_S = "#D55E00", "#0072B2"


def _pol(r, a_deg):
    a = np.radians(a_deg)
    return np.array([r * np.cos(a), r * np.sin(a)])


def _rot_rect(ax, r_in, r_out, width, ang_deg, **kw):
    rect = Rectangle((r_in, -width / 2), r_out - r_in, width, **kw)
    rect.set_transform(Affine2D().rotate_deg(ang_deg) + ax.transData)
    ax.add_patch(rect)


def _rotate(pts, ang_deg):
    a = np.radians(ang_deg)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    return (R @ np.asarray(pts).T).T


# ---------------------------------------------------------------------------
def fig_8_1():
    """SPM and IPM rotor cross-sections with d- and q-axes."""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.8, 3.9))
    for ax in (axa, axb):
        ax.set_aspect("equal")
        ax.axis("off")

    # ---------------- (a) SPM ----------------
    ax = axa
    r_core, r_mag, r_sl, r_bore, r_so = 54, 59, 60, 61, 92
    ax.add_patch(Circle((0, 0), r_so, fc=STEEL, ec=INK, lw=0.9))
    ax.add_patch(Circle((0, 0), r_bore, fc="white", ec=INK, lw=0.9))
    for k in range(48):
        _rot_rect(ax, r_bore - 0.5, r_bore + 14, 3.6, k * 7.5 + 3.75, fc="#F2C9A8", ec=INK, lw=0.3)
    ax.add_patch(Circle((0, 0), r_sl, fc="#999999", ec=INK, lw=0.6))  # sleeve
    ax.add_patch(Circle((0, 0), r_mag, fc=STEEL_DARK, ec="none"))
    for k in range(8):
        c = 22.5 + 45 * k
        ax.add_patch(Wedge((0, 0), r_mag, c - 20, c + 20, width=r_mag - r_core,
                           fc=MAG_N if k % 2 == 0 else MAG_S, ec=INK, lw=0.5))
        ax.text(*_pol(56.5, c), "N" if k % 2 == 0 else "S", ha="center", va="center", fontsize=6.5,
                color="white", weight="bold")
    ax.add_patch(Circle((0, 0), r_core, fc=STEEL_DARK, ec=INK, lw=0.6))
    ax.add_patch(Circle((0, 0), 15, fc="#888888", ec=INK, lw=0.6))
    for ang, col, lab in ((22.5, PINK, "d"), (45, GREEN, "q")):
        p1 = _pol(108, ang)
        ax.plot([0, p1[0]], [0, p1[1]], ls="-.", color=col, lw=1.0)
        ax.text(*_pol(113, ang), lab, color=col, fontsize=10, ha="center", va="center")
    kw = dict(fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("arc magnet 5 mm", xy=_pol(57, 160), xytext=(-118, 88), ha="left", **kw)
    ax.annotate("sleeve 1 mm", xy=_pol(60, 200), xytext=(-118, -82), ha="left", **kw)
    ax.annotate("48-slot stator", xy=_pol(80, 240), xytext=(-118, -104), ha="left", **kw)
    ax.annotate("air gap 1 mm", xy=_pol(60.5, 300), xytext=(30, -110), ha="left", **kw)
    ax.text(0, 122, "(a) SPM, rotor Ø120 mm\n$L_d = L_q$", ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-120, 120)
    ax.set_ylim(-118, 150)

    # ---------------- (b) IPM with V magnets ----------------
    ax = axb
    R = 80
    ax.add_patch(Circle((0, 0), R, fc=STEEL_DARK, ec=INK, lw=0.9))
    # pole-local geometry (x along d-axis): magnet inner end at x=58, y=+-2.5, angle 38 deg off radial
    alpha = np.radians(38)
    u = np.array([np.cos(alpha), np.sin(alpha)])          # along the magnet
    n = np.array([-np.sin(alpha), np.cos(alpha)])         # across the magnet
    p_in = np.array([57.0, 2.5])
    corners = [p_in, p_in + 20 * u, p_in + 20 * u + 4 * n, p_in + 4 * n]
    outer_end = p_in + 20 * u
    # flux barrier: from magnet outer end to 1 mm below the surface
    tip_ang = np.degrees(np.arctan2(outer_end[1] + 2, outer_end[0]))
    bar = [outer_end, outer_end + 4 * n,
           _pol(R - 1, tip_ang + 2.4), _pol(R - 1, tip_ang - 1.5)]
    inner_bar = [p_in, p_in + 4 * n, np.array([p_in[0] - 3, 1.0])]
    for k in range(8):
        c = 45 * k
        col = MAG_N if k % 2 == 0 else MAG_S
        for s in (+1, -1):
            flip = np.array([1, s])
            mag = _rotate([pt * flip for pt in corners], c)
            br = _rotate([pt * flip for pt in bar], c)
            ib = _rotate([pt * flip for pt in inner_bar], c)
            ax.add_patch(Polygon(br, closed=True, fc="white", ec=INK, lw=0.4))
            ax.add_patch(Polygon(ib, closed=True, fc="white", ec=INK, lw=0.4))
            ax.add_patch(Polygon(mag, closed=True, fc=col, ec=INK, lw=0.5))
    ax.add_patch(Circle((0, 0), 22, fc="#888888", ec=INK, lw=0.6))
    # flux paths
    # q-axis: down the inter-pole iron at 22.5 deg, under the V of the pole at 45 deg, up at 67.5 deg
    th = np.linspace(22.5, 67.5, 60)
    rr = 47 + 0 * th
    path = np.vstack([np.array([_pol(r, 22.5) for r in np.linspace(80, 47, 15)]),
                      np.array([_pol(r, t) for r, t in zip(rr, th)]),
                      np.array([_pol(r, 67.5) for r in np.linspace(47, 80, 15)])])
    ax.plot(path[:, 0], path[:, 1], color=GREEN, lw=7, alpha=0.45, solid_capstyle="round")
    # d-axis: along pole centre at 180 deg, through both magnet legs? (crosses V) -> yoke -> back at 225
    th = np.linspace(190, 215, 40)
    path = np.vstack([np.array([_pol(r, 180) for r in np.linspace(80, 68, 6)]),
                      np.array([_pol(r, a) for r, a in zip(np.linspace(68, 44, 10), np.linspace(180, 190, 10))]),
                      np.array([_pol(44, t) for t in th]),
                      np.array([_pol(r, a) for r, a in zip(np.linspace(44, 68, 10), np.linspace(215, 225, 10))]),
                      np.array([_pol(r, 225) for r in np.linspace(68, 80, 6)])])
    ax.plot(path[:, 0], path[:, 1], color=PINK, lw=2.0, ls=(0, (3, 1.5)))
    for ang, col, lab in ((0, PINK, "d"), (22.5, GREEN, "q")):
        p1 = _pol(100, ang)
        ax.plot([0, p1[0]], [0, p1[1]], ls="-.", color=col, lw=1.0)
        ax.text(*_pol(106, ang), lab, color=col, fontsize=10, ha="center", va="center")
    kw = dict(fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    mid_mag = _rotate([p_in + 10 * u + 2 * n], 90)[0]
    ax.annotate("V magnet\n20 × 4 mm", xy=mid_mag, xytext=(-118, 112), ha="left", **kw)
    ax.annotate("flux barrier,\n1 mm bridge", xy=_pol(78.5, 90 + tip_ang), xytext=(52, 104), ha="left", **kw)
    ax.annotate("central web", xy=_pol(56, 90), xytext=(-118, 90), ha="left", **kw)
    ax.annotate("q-axis path:\nall iron (wide)", xy=_pol(47, 45), xytext=(70, -60), ha="left",
                color=GREEN, fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6, color=GREEN))
    ax.annotate("d-axis path:\ncrosses magnets\n(narrow)", xy=_pol(40, 202), xytext=(-118, -88), ha="left",
                color=PINK, fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6, color=PINK))
    ax.text(0, 122, "(b) IPM, rotor Ø160 mm\n$L_d < L_q$", ha="center", va="bottom", fontsize=9)
    ax.set_xlim(-120, 120)
    ax.set_ylim(-118, 150)
    fig.subplots_adjust(left=0.01, right=0.99, wspace=0.04)
    save(fig, "08", "fig-8-1-spm-ipm-rotors")


# ---------------------------------------------------------------------------
IPM = dict(p=4, psi=0.08, Ld=0.2e-3, Lq=0.5e-3, Imax=400.0, Vmax=400 / np.sqrt(3))


def _ipm_T(beta):
    c = IPM
    return 1.5 * c["p"] * (c["psi"] * c["Imax"] * np.cos(beta)
                           + (c["Ld"] - c["Lq"]) * (-c["Imax"] * np.sin(beta)) * c["Imax"] * np.cos(beta))


def _ipm_lam(beta):
    c = IPM
    return np.hypot(c["psi"] - c["Ld"] * c["Imax"] * np.sin(beta), c["Lq"] * c["Imax"] * np.cos(beta))


def _ipm_envelope(rpm):
    """Maximum torque of the ideal IPM motor (worked example) under |i| <= 400 A and
    |v| <= Vdc/sqrt(3). Below base speed: MTPA. Above: current angle advanced along the
    current limit until the flux linkage equals Vmax/omega_e (psi_m/L_d = Imax, so the
    optimum stays on the current circle at every speed)."""
    from scipy.optimize import brentq, minimize_scalar
    b0 = minimize_scalar(lambda b: -_ipm_T(b), bounds=(0, 1.5), method="bounded").x
    out = []
    for n in rpm:
        we = n * 2 * np.pi / 60 * IPM["p"]
        lim = IPM["Vmax"] / we
        if _ipm_lam(b0) <= lim:
            out.append(_ipm_T(b0))
        else:
            b = brentq(lambda x: _ipm_lam(x) - lim, b0, np.pi / 2 - 1e-9)
            out.append(_ipm_T(b))
    nb = IPM["Vmax"] / _ipm_lam(b0) / IPM["p"] * 60 / (2 * np.pi)
    return np.array(out), nb


def fig_8_2():
    """Torque-speed and power-speed envelope of the EV IPM motor."""
    rpm = np.linspace(1, 14000, 281)
    T, nb = _ipm_envelope(rpm)
    P = T * rpm * 2 * np.pi / 60 / 1e3
    Tm = T[0]
    fig, ax = new_fig(6.4, 3.9)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax.axvspan(0, nb, color="#EEF3F8", zorder=0)
    ax.plot(rpm, T, color=BLUE, lw=2.0)
    ax2.plot(rpm, P, color=ORANGE, lw=2.0)
    # id = 0: magnet torque only, valid until its own base speed
    nb0 = 400 / np.sqrt(3) / np.hypot(0.08, 0.5e-3 * 400) / 4 * 60 / (2 * np.pi)
    ax.plot([0, nb0], [192, 192], ls="--", color=BLUE, lw=1.3)
    ax.text(100, 185, "$i_d$ = 0: 192 N·m\n(magnet only)", fontsize=7.5, color=BLUE, va="top")
    ax.axvline(nb, color="#666666", lw=0.8, ls=":")
    ax.text(nb + 100, 75, f"base speed\n{nb:.0f} rpm", ha="left", va="center", fontsize=8)
    ax.text(nb / 2, 255, "constant torque\n(MTPA)", ha="center", va="center", fontsize=8.5)
    ax.text(8500, 30, "constant power (field weakening)", ha="center", fontsize=8.5)
    ax.text(600, Tm + 6, f"{Tm:.0f} N·m", fontsize=8.5, color=BLUE, va="bottom")
    ax.text(12500, T[np.searchsorted(rpm, 12500)] - 14, "torque", color=BLUE, fontsize=9, ha="center", va="top")
    ax2.text(12500, P[np.searchsorted(rpm, 12500)] + 4, "power", color=ORANGE, fontsize=9, ha="center",
             va="bottom")
    Pb = Tm * nb * 2 * np.pi / 60 / 1e3
    ax2.plot(nb, Pb, "o", color=ORANGE, ms=5)
    ax2.annotate(f"MTPA corner\n{Tm:.0f} N·m, {Pb:.0f} kW", xy=(nb, Pb), xytext=(4500, 45), fontsize=8,
                 color=ORANGE, arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    # worked example: 30 deg advance, 291 N m at 3101 rpm, 94.5 kW
    ax.plot(3101, 291, "s", mfc="white", mec=INK, ms=5, zorder=6)
    ax.annotate("worked example (30° advance):\n291 N·m at 3101 rpm, 94.5 kW", xy=(3101, 291),
                xytext=(4300, 380), fontsize=7.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.6))
    i13 = np.searchsorted(rpm, 13000)
    ax.plot(13000, T[i13], "o", color=BLUE, ms=4)
    ax.annotate(f"{T[i13]:.0f} N·m, {P[i13]:.0f} kW\nat 13 000 rpm", xy=(13000, T[i13]),
                xytext=(10200, 165), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.set_xlim(0, 14000)
    ax.set_ylim(0, 400)
    ax2.set_ylim(0, 160)
    ax.set_xlabel("Motor speed (rpm)")
    ax.set_ylabel("Torque (N·m)", color=BLUE)
    ax2.set_ylabel("Power (kW)", color=ORANGE)
    ax.text(0.99, 0.62, "ideal lossless model: 400 A peak, 400 V DC, $\\psi_m/L_d$ = 400 A",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color="#555555")
    save(fig, "08", "fig-8-2-pmsm-torque-power-envelope")


# ---------------------------------------------------------------------------
def _trap(theta):
    """Unit trapezoid: +1 flat on 0..120, falls 120..180, -1 on 180..300, rises 300..360."""
    t = np.mod(theta, 360)
    return np.interp(t, [0, 120, 180, 300, 360], [1, 1, -1, -1, 1])


def _block(theta):
    t = np.mod(theta, 360)
    return np.where(t < 120, 1.0, np.where((t >= 180) & (t < 300), -1.0, 0.0))


def fig_8_3():
    """BLDC trapezoidal EMFs, six-step currents and Hall signals."""
    Ep = 8.15 / 2          # phase EMF flat top: line-to-line EMF 8.15 V across two phases in series
    Ipk = 15
    th = np.linspace(0, 360, 3601)
    fig, axs = plt.subplots(3, 1, figsize=(6.4, 5.0), sharex=True,
                            gridspec_kw=dict(height_ratios=[1.1, 1.1, 1.0], hspace=0.18))
    names = ["a", "b", "c"]
    cols = [BLUE, ORANGE, GREEN]
    for k in range(3):
        sh = 120 * k
        axs[0].plot(th, Ep * _trap(th - sh), color=cols[k], lw=1.6, label=f"$e_{names[k]}$")
        i = Ipk * _block(th - sh)
        # model: the incoming phase rises with a small dip, outgoing phase decays over ~5 deg
        i_s = i.copy()
        for edge, lvl in ((120, 1), (300, -1)):
            e = np.mod(th - sh - edge, 360)
            m = e < 6
            i_s[m] = lvl * Ipk * np.exp(-e[m] / 1.6)
        for edge, lvl in ((0, 1), (180, -1)):
            e = np.mod(th - sh - edge, 360)
            m = e < 6
            i_s[m] = lvl * Ipk * (1 - np.exp(-e[m] / 1.2))
        axs[1].plot(th, i_s, color=cols[k], lw=1.5, label=f"$i_{names[k]}$")
    axs[0].set_ylabel("Back-EMF (V)")
    axs[0].set_ylim(-6.5, 6.5)
    axs[0].set_yticks([-Ep, 0, Ep])
    axs[0].set_yticklabels([f"−{Ep:.2f}", "0", f"{Ep:.2f}"])
    axs[0].legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8.5)
    axs[0].text(2, 5.6, "phase EMF; $e_{ab}$ = 8.15 V during each step", fontsize=7.5, color="#555555")
    axs[1].set_ylabel("Current (A)")
    axs[1].set_ylim(-20, 20)
    axs[1].set_yticks([-15, 0, 15])
    axs[1].legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8.5)
    # Hall signals: H1 high 0..180, H2 120..300, H3 240..420
    ax = axs[2]
    for k in range(3):
        h = (np.mod(th - 120 * k, 360) < 180).astype(float)
        off = (2 - k) * 1.5
        ax.plot(th[:-1], off + h[:-1], color=cols[k], lw=1.5, drawstyle="steps-post")
        ax.text(-6, off + 0.5, f"H{k + 1}", ha="right", va="center", fontsize=8.5, color=cols[k])
    for s in range(6):
        c = 60 * s + 30
        h = [(np.mod(c - 120 * k, 360) < 180) for k in range(3)]
        code = "".join("1" if v else "0" for v in h)
        ax.text(c, 4.35, f"{s + 1}\n{code}", ha="center", va="bottom", fontsize=7.5)
    ax.set_ylim(-0.3, 5.4)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylabel("Hall\nsignals", labelpad=24)
    ax.set_xlim(0, 360)
    ax.set_xticks(np.arange(0, 361, 60))
    ax.set_xlabel("Rotor electrical angle (degrees)")
    for a in axs:
        for x in range(0, 361, 60):
            a.axvline(x, color="#CCCCCC", lw=0.6, zorder=0)
        a.axhline(0, color="#999999", lw=0.5, zorder=0) if a is not axs[2] else None
    axs[1].annotate("commutation\ntransient", xy=(120.5, 9), xytext=(140, 14), fontsize=7.5,
                    arrowprops=dict(arrowstyle="-", lw=0.6))
    save(fig, "08", "fig-8-3-bldc-six-step-waveforms")


# ---------------------------------------------------------------------------
def _srm_L(theta):
    """Phase-A inductance (mH) over one rotor pole pitch (0..60 mech deg); aligned at 30 deg."""
    return np.interp(np.mod(theta, 60), [0, 7.5, 27.5, 32.5, 52.5, 60], [2, 2, 20, 20, 2, 2])


def fig_8_4():
    """8/6 SRM geometry and idealised inductance, current and torque."""
    fig = plt.figure(figsize=(6.8, 4.2))
    axg = fig.add_axes([0.0, 0.02, 0.44, 0.92])
    axg.set_aspect("equal")
    axg.axis("off")
    # stator
    Rso, Rsy, Rsb, Rr, Rry = 1.0, 0.82, 0.52, 0.49, 0.30
    axg.add_patch(Circle((0, 0), Rso, fc=STEEL, ec=INK, lw=0.9))
    axg.add_patch(Circle((0, 0), Rsy, fc="white", ec=INK, lw=0.9))
    beta_s, beta_r = 20.0, 22.0
    for k in range(8):
        c = 90 + 45 * k
        a0, a1 = np.radians(c - beta_s / 2), np.radians(c + beta_s / 2)
        w = Rsb * np.sin(np.radians(beta_s / 2))
        _rot_rect(axg, Rsb, Rsy + 0.01, 2 * w, c, fc=STEEL, ec=INK, lw=0.6)
        is_a = k in (0, 4)
        col = ORANGE if is_a else "#E8D3B8"
        for s in (+1, -1):
            off = np.degrees(np.arctan2(s * (w + 0.045), 0.68))
            _rot_rect(axg, 0.58, 0.79, 0.08, c + off, fc=col, ec=INK, lw=0.4)
        if is_a:
            axg.text(*_pol(0.91, c), "A", ha="center", va="center", fontsize=9, weight="bold", color=ORANGE)
    # rotor: 6 poles, one pole 15 deg before alignment with phase A (stator pole at 90 deg)
    rot0 = 90 - 15
    pts = []
    for k in range(6):
        c = rot0 + 60 * k
        for a in np.linspace(c - beta_r / 2, c + beta_r / 2, 8):
            pts.append(_pol(Rr, a))
        for a in np.linspace(c + beta_r / 2 + 4, c + 60 - beta_r / 2 - 4, 8):
            pts.append(_pol(Rry, a))
    axg.add_patch(Polygon(pts, closed=True, fc=STEEL_DARK, ec=INK, lw=0.8))
    axg.add_patch(Circle((0, 0), 0.1, fc="#888888", ec=INK, lw=0.6))
    p1 = _pol(0.62, rot0)
    axg.plot([0, p1[0]], [0, p1[1]], color=BLUE, lw=0.9, ls="-.")
    axg.plot([0, 0], [0, 0.62], color=ORANGE, lw=0.9, ls="-.")
    from matplotlib.patches import Arc
    axg.add_patch(Arc((0, 0), 0.8, 0.8, theta1=rot0, theta2=90, color=INK, lw=0.8))
    axg.text(*_pol(0.47, 96), "15°", fontsize=8, ha="right", va="center")
    kw = dict(fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    axg.annotate("phase A coils", xy=_pol(0.70, 270 + 13), xytext=(0.35, -1.13), ha="left", **kw)
    axg.annotate("rotor pole\n(6 poles)", xy=_pol(0.45, rot0 + 120), xytext=(-1.12, 0.92), ha="left", **kw)
    axg.annotate("air gap 0.4 mm\n(exaggerated)", xy=_pol(0.505, rot0 + 240), xytext=(-1.12, -1.10),
                 ha="left", **kw)
    axg.text(0, 1.10, "(a) 8/6 SRM", ha="center", va="bottom", fontsize=9.5)
    axg.set_xlim(-1.15, 1.15)
    axg.set_ylim(-1.25, 1.3)

    # (b) curves
    th = np.linspace(0, 60, 1201)
    L = _srm_L(th)
    dL = np.gradient(L * 1e-3, np.radians(th))
    i = np.where((th >= 7.5) & (th <= 25.0), 30.0, 0.0)
    tail = (th > 25.0) & (th < 38)
    i[tail] = 30 * np.clip(1 - (th[tail] - 25.0) / 13.0, 0, 1)
    T = 0.5 * i ** 2 * dL
    left, w = 0.55, 0.43
    ax1 = fig.add_axes([left, 0.68, w, 0.25])
    ax2 = fig.add_axes([left, 0.39, w, 0.25], sharex=ax1)
    ax3 = fig.add_axes([left, 0.10, w, 0.25], sharex=ax1)
    ax1.plot(th, L, color=BLUE)
    ax1.set_ylabel("$L$ (mH)")
    ax1.set_ylim(0, 24)
    ax1.set_yticks([2, 20])
    ax1.text(1, 4, "$L_u$", fontsize=8.5, color=BLUE)
    ax1.text(30, 21, "$L_a$", fontsize=8.5, color=BLUE, ha="center", va="bottom")
    ax1.set_title("(b) phase A against rotor angle", fontsize=9.5)
    ax2.plot(th, i, color=ORANGE)
    ax2.set_ylabel("$i$ (A)")
    ax2.set_ylim(0, 38)
    ax2.set_yticks([0, 30])
    ax2.text(38.5, 8, "tail after\nturn-off", fontsize=7.5, color=ORANGE)
    ax3.plot(th, T, color=GREEN)
    ax3.axhline(0, color="#999999", lw=0.5)
    ax3.set_ylabel("$T$ (N·m)")
    ax3.set_ylim(-12, 30)
    ax3.set_yticks([0, 23.2])
    ax3.annotate("negative torque\n(current into falling $L$)", xy=(34.5, -3.5), xytext=(39, -11), fontsize=7.5,
                 va="bottom", arrowprops=dict(arrowstyle="-", lw=0.6))
    ax3.set_xlabel("Rotor angle (mechanical degrees)")
    ax3.set_xlim(0, 60)
    ax3.set_xticks(np.arange(0, 61, 10))
    for a in (ax1, ax2, ax3):
        a.axvspan(7.5, 27.5, color="#EEF3F8", zorder=0)
        if a is not ax3:
            plt.setp(a.get_xticklabels(), visible=False)
    for a in (ax1, ax2, ax3):
        a.axvline(15, color="#888888", lw=0.8, ls=":")
    ax1.text(15.5, 22.5, "position in (a)", fontsize=7, color="#555555", ha="left", va="bottom")
    ax1.text(17.5, 5, "rising $L$", fontsize=7.5, ha="center", color="#555555", rotation=0)
    save(fig, "08", "fig-8-4-srm-geometry-inductance")


# ---------------------------------------------------------------------------
def fig_8_5():
    """Stepper pull-in and pull-out curves."""
    n = np.linspace(0, 1500, 1501)
    po_pts_n = [0, 30, 60, 75, 90, 120, 200, 300, 450, 600, 800, 1000, 1250, 1500]
    po_pts_t = [1.9, 1.75, 1.6, 1.32, 1.5, 1.52, 1.48, 1.4, 1.2, 1.0, 0.76, 0.55, 0.41, 0.3]
    po = PchipInterpolator(po_pts_n, po_pts_t)(n)
    pi_pts_n = [0, 30, 60, 75, 90, 150, 250, 350, 420, 450]
    pi_pts_t = [1.45, 1.38, 1.3, 1.05, 1.2, 1.08, 0.75, 0.38, 0.1, 0.0]
    pin = np.clip(PchipInterpolator(pi_pts_n, pi_pts_t)(np.clip(n, 0, 450)), 0, None)
    pin[n > 450] = 0
    fig, ax = new_fig(6.4, 3.9)
    ax.fill_between(n, 0, pin, color="#DCEAF5", zorder=0)
    ax.fill_between(n, pin, po, color="#FBE6D6", zorder=0)
    ax.plot(n, po, color=ORANGE, lw=2.0)
    ax.plot(n[n <= 450], pin[n <= 450], color=BLUE, lw=2.0)
    ax.plot(0, 1.9, "o", color=INK, ms=5, clip_on=False, zorder=5)
    ax.annotate("holding torque 1.9 N·m", xy=(0, 1.9), xytext=(140, 1.93), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.annotate("mid-band\nresonance", xy=(76, 1.33), xytext=(160, 1.68), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.text(700, 1.05, "pull-out torque", color=ORANGE, fontsize=9, ha="left")
    ax.text(300, 0.66, "pull-in\ntorque", color=BLUE, fontsize=9, ha="left")
    ax.text(140, 0.32, "start–stop\nregion", ha="center", fontsize=8.5, color=BLUE)
    ax.text(820, 0.38, "slew region\n(reach by ramping)", ha="center", fontsize=8.5, color=ORANGE)
    ax.plot(600, 0.04, "D", color=INK, ms=5, zorder=5)
    ax.annotate("worked example:\n600 rpm, 0.035 N·m", xy=(600, 0.04), xytext=(1080, 0.12), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 2.0)
    ax.set_xlabel("Speed (rpm)")
    ax.set_ylabel("Torque (N·m)")
    top = ax.secondary_xaxis("top", functions=(lambda r: r * 200 / 60, lambda s: s * 60 / 200))
    top.set_xlabel("Full-step rate (steps/s)")
    top.set_xticks(np.arange(0, 5001, 1000))
    ax.spines["top"].set_visible(True)
    ax.text(1490, 1.9, "NEMA 23, 1.8°, 48 V,\n1/16 microstepping", fontsize=7.5, color="#555555",
            ha="right", va="top")
    save(fig, "08", "fig-8-5-stepper-pull-in-pull-out")


# ---------------------------------------------------------------------------
def _blades(ax, x, y, s=0.55):
    for a in (90, 210, 330):
        tip = np.array([x, y]) + s * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
        side = 0.08 * np.array([-np.sin(np.radians(a)), np.cos(np.radians(a))])
        ax.add_patch(Polygon([[x, y], tip + side, tip], closed=True, fc="#9BB3C9", ec=INK, lw=0.6))
    ax.add_patch(Circle((x, y), 0.09, fc="#666666", ec=INK, lw=0.6, zorder=3))


def _conv(ax, x, y, w, h, text, fc="#F4F0E6"):
    box(ax, x, y, w, h, "", fc=fc)
    ax.plot([x + 0.06, x + w - 0.06], [y + 0.06, y + h - 0.06], color=INK, lw=0.6)
    ax.text(x + 0.12, y + h - 0.1, text[0], fontsize=7, ha="left", va="top")
    ax.text(x + w - 0.12, y + 0.1, text[1], fontsize=7, ha="right", va="bottom")


def _xfmr(ax, x, y, r=0.2):
    ax.add_patch(Circle((x - 0.13, y), r, fc="none", ec=INK, lw=1.0))
    ax.add_patch(Circle((x + 0.13, y), r, fc="none", ec=INK, lw=1.0))


def _flow(ax, x0, y0, x1, y1, text, color=ORANGE, va="bottom", dy=0.06):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.45", color=color, lw=2.2,
                                shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 + (dy if va == "bottom" else -dy), text, color=color,
            fontsize=8, ha="center", va=va, weight="bold")


def fig_8_6():
    """DFIG and full-converter PMSG wind-turbine single-line diagrams."""
    fig, ax = schematic(6.8, 5.0, xlim=(0, 11.4), ylim=(1.1, 9.4))
    # ---------------- (a) DFIG ----------------
    y = 7.2
    ax.text(0.0, 9.25, "(a) Doubly fed induction generator (DFIG), s = −0.25", fontsize=9.5, va="top")
    _blades(ax, 0.6, y)
    ax.plot([0.69, 1.2], [y, y], color=INK, lw=2.0)
    box(ax, 1.2, y - 0.4, 1.2, 0.8, "gearbox\n≈ 1:100", fontsize=7.5)
    ax.plot([2.4, 2.8], [y, y], color=INK, lw=2.0)
    ax.add_patch(Circle((3.35, y), 0.55, fc="#EEF3F8", ec=INK, lw=1.0))
    ax.text(3.35, y, "WRIG\n690 V", fontsize=7.5, ha="center", va="center")
    # stator line to 690 V bus
    busx = 8.0
    ax.plot([3.9, busx], [y, y], color=INK, lw=1.4)
    ax.plot([busx, busx], [5.2, 7.7], color=INK, lw=3.0)
    ax.text(busx, 7.8, "690 V", fontsize=7.5, ha="center", va="bottom")
    _xfmr(ax, 9.0, 6.5)
    ax.plot([busx, 8.67], [6.5, 6.5], color=INK, lw=1.4)
    ax.plot([9.33, 10.0], [6.5, 6.5], color=INK, lw=1.4)
    ax.plot([10.0, 10.0], [5.9, 7.1], color=INK, lw=3.0)
    ax.text(9.0, 6.0, "690 V/33 kV", fontsize=7, ha="center", va="top")
    ax.text(10.1, 6.5, "33 kV\ngrid", fontsize=7.5, ha="left", va="center")
    # rotor via slip rings
    ax.plot([3.35, 3.35], [y - 0.55, 5.6], color=INK, lw=1.4)
    ax.text(3.25, 6.3, "slip\nrings", fontsize=7, ha="right", va="center")
    ax.plot([3.35, 4.1], [5.6, 5.6], color=INK, lw=1.4)
    _conv(ax, 4.1, 5.2, 0.9, 0.8, ("AC", "DC"))
    ax.plot([5.0, 5.6], [5.75, 5.75], color=INK, lw=1.0)
    ax.plot([5.0, 5.6], [5.45, 5.45], color=INK, lw=1.0)
    ax.text(5.3, 5.15, "DC link\n1100 V", fontsize=6.5, ha="center", va="top")
    _conv(ax, 5.6, 5.2, 0.9, 0.8, ("DC", "AC"))
    ax.plot([6.5, busx], [5.6, 5.6], color=INK, lw=1.4)
    ax.text(4.55, 6.06, "machine-side", fontsize=6.5, ha="center", va="bottom")
    ax.text(6.05, 6.06, "grid-side", fontsize=6.5, ha="center", va="bottom")
    ax.text(5.3, 4.7, "back-to-back converter\n0.5 MW (≈ 25 % rating)", fontsize=7, ha="center", va="top")
    box(ax, 1.65, 5.35, 1.35, 0.5, "crowbar /\nDC chopper", fontsize=6.5, fc="#FBE6D6")
    ax.plot([3.0, 3.35], [5.6, 5.6], color=INK, lw=0.8, ls="--")
    ax.text(7.7, 4.95, "grid-side converter\ncontrols P and Q", fontsize=7, ha="center", va="top",
            style="italic", color="#444444")
    # flows
    _flow(ax, 1.2 - 0.0, y + 0.75, 2.6, y + 0.75, "P$_{mech}$ = 2.0 MW")
    _flow(ax, 4.6, y + 0.15, 6.6, y + 0.15, "P$_{stator}$ = 1.6 MW")
    _flow(ax, 4.2, 6.55, 6.6, 6.55, "P$_{rotor}$ = 0.4 MW", va="bottom", dy=0.04)
    _flow(ax, 8.15, 7.1, 9.7, 7.1, "2.0 MW")

    # ---------------- (b) PMSG ----------------
    y = 2.3
    ax.text(0.0, 3.9, "(b) Full-converter direct-drive PMSG", fontsize=9.5, va="top")
    _blades(ax, 0.6, y)
    ax.plot([0.69, 2.0], [y, y], color=INK, lw=2.0)
    ax.text(1.4, y + 0.12, "no gearbox", fontsize=7, ha="center", va="bottom", style="italic")
    ax.add_patch(Circle((2.7, y), 0.7, fc="#EEF3F8", ec=INK, lw=1.0))
    ax.text(2.7, y, "PMSG\n(direct\ndrive)", fontsize=7.5, ha="center", va="center")
    ax.plot([3.4, 4.1], [y, y], color=INK, lw=1.4)
    _conv(ax, 4.1, y - 0.4, 0.9, 0.8, ("AC", "DC"))
    ax.plot([5.0, 5.6], [y + 0.15, y + 0.15], color=INK, lw=1.0)
    ax.plot([5.0, 5.6], [y - 0.15, y - 0.15], color=INK, lw=1.0)
    _conv(ax, 5.6, y - 0.4, 0.9, 0.8, ("DC", "AC"))
    ax.text(5.3, y - 0.55, "full back-to-back converter, 100 % rating", fontsize=7, ha="center", va="top")
    ax.text(6.05, y - 0.95, "grid-side converter controls P and Q", fontsize=7, ha="center", va="top",
            style="italic", color="#444444")
    ax.plot([6.5, 8.67], [y, y], color=INK, lw=1.4)
    _xfmr(ax, 9.0, y)
    ax.plot([9.33, 10.0], [y, y], color=INK, lw=1.4)
    ax.plot([10.0, 10.0], [y - 0.6, y + 0.6], color=INK, lw=3.0)
    ax.text(9.0, y - 0.3, "LV/66 kV", fontsize=7, ha="center", va="top")
    ax.text(10.1, y, "66 kV\narray\ncable", fontsize=7.5, ha="left", va="center")
    _flow(ax, 3.5, y + 0.6, 9.7, y + 0.6, "all power through the converter")
    ax.plot([0, 11.4], [4.3, 4.3], color="#CCCCCC", lw=0.8)
    save(fig, "08", "fig-8-6-wind-generator-topologies")


if __name__ == "__main__":
    fig_8_1()
    fig_8_2()
    fig_8_3()
    fig_8_4()
    fig_8_5()
    fig_8_6()
