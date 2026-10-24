"""Figures for Chapter 4 — Transformers.

Run from the repository root:  python figures/scripts/ch04.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Ellipse, Circle, Arc, FancyArrowPatch  # noqa: E402

from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

BLUE, ORANGE, GREEN, PINK = COLORS[0], COLORS[1], COLORS[2], COLORS[3]
CORE = "#B9BEC4"
LVC = "#A9CBE8"
HVC = "#F3C29B"


def _farrow(ax, x0, y0, x1, y1, color=INK, lw=1.6, ms=12, ls="-", z=3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=ms,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0, zorder=z))


# ---------------------------------------------------------------------------
# Figure 4.1
# ---------------------------------------------------------------------------
def fig_4_1():
    """Core-type (three-limb) and shell-type construction, to scale (metres)."""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.8, 4.3), gridspec_kw=dict(width_ratios=[1.35, 1.0]))
    for ax in (axa, axb):
        ax.set_aspect("equal")
        ax.axis("off")

    # ---------------- (a) three-phase three-limb core type ----------------
    ax = axa
    w = 0.25          # limb width (diameter)
    pitch = 0.55      # limb centre spacing
    hy = 0.25         # yoke height
    hw = 1.20         # window height
    W = 2 * pitch + w
    H = hw + 2 * hy
    ax.add_patch(Rectangle((0, 0), W, H, fc=CORE, ec=INK, lw=1.0, zorder=1))
    for k in range(2):
        x0 = w + k * pitch
        ax.add_patch(Rectangle((x0, hy), pitch - w, hw, fc="white", ec=INK, lw=1.0, zorder=1))
    # windings (section through both sides of every limb)
    clr, blv, duct, bhv = 0.005, 0.040, 0.020, 0.070
    ylv, hlv = hy + 0.06, hw - 0.12
    yhv, hhv = hy + 0.08, hw - 0.16
    for k in range(3):
        xc = w / 2 + k * pitch
        for side in (-1, 1):
            face = xc + side * w / 2
            x_lv = face + side * clr if side > 0 else face - clr - blv
            x_hv = face + side * (clr + blv + duct) if side > 0 else face - (clr + blv + duct) - bhv
            ax.add_patch(Rectangle((x_lv, ylv), blv, hlv, fc=LVC, ec=INK, lw=0.6, zorder=2))
            ax.add_patch(Rectangle((x_hv, yhv), bhv, hhv, fc=HVC, ec=INK, lw=0.6, zorder=2))
    # main flux: dashed loops along the core centre-line
    for k in range(2):
        xl, xr = w / 2 + k * pitch, w / 2 + (k + 1) * pitch
        yb, yt = hy / 2, H - hy / 2
        ax.plot([xl, xl, xr, xr, xl], [yb, yt, yt, yb, yb], ls=(0, (4, 3)), color=BLUE, lw=1.1, zorder=3)
        _farrow(ax, xl, 0.75, xl, 0.95, color=BLUE, lw=1.1, ms=9)
        _farrow(ax, (xl + xr) / 2 - 0.05, yt, (xl + xr) / 2 + 0.05, yt, color=BLUE, lw=1.1, ms=9)
        _farrow(ax, xr, 0.95, xr, 0.75, color=BLUE, lw=1.1, ms=9)
    # leakage flux in the LV-HV duct of the centre limb (right side)
    xc = w / 2 + pitch
    xduct = xc + w / 2 + clr + blv + duct / 2
    for a, b in [(0.040, 0.60), (0.075, 0.66)]:
        ax.add_patch(Ellipse((xduct, hy + hw / 2), 2 * a, 2 * b, fill=False, ec=ORANGE, lw=0.9,
                             ls=(0, (2, 1.5)), zorder=4))
    _farrow(ax, xduct, 0.85, xduct, 1.0, color=ORANGE, lw=1.0, ms=8, z=5)

    # labels
    fs = 8.5
    ax.annotate("yoke", xy=(0.40, H - 0.05), xytext=(0.40, H + 0.12), fontsize=fs, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("limb", xy=(w / 2 - 0.05, 0.40), xytext=(-0.33, 0.25), fontsize=fs, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("LV", xy=(-clr - blv / 2, 1.25), xytext=(-0.33, 1.40), fontsize=fs, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("HV", xy=(-clr - blv - duct - bhv / 2, 1.05), xytext=(-0.33, 1.10), fontsize=fs, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("main flux", xy=(w / 2, 0.62), xytext=(-0.33, 0.62), fontsize=fs, color=BLUE, ha="center",
                va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    ax.annotate("window", xy=(w + (pitch - w) / 2, hy + 0.02), xytext=(0.40, -0.30), fontsize=fs, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("leakage flux (LV–HV duct)", xy=(xduct + 0.05, 1.25), xytext=(1.25, H + 0.12), fontsize=fs,
                color=ORANGE, ha="center", va="bottom", arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    # dimensions
    kw = dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=7)
    xd = W + 0.19
    ax.annotate("", xy=(xd, hy), xytext=(xd, hy + hw), arrowprops=kw, annotation_clip=False)
    ax.text(xd + 0.04, hy + hw / 2, "window\nheight\n1.2 m", fontsize=7.5, va="center", ha="left")
    ax.annotate("", xy=(w / 2 + pitch, -0.08), xytext=(w / 2 + 2 * pitch, -0.08), arrowprops=kw,
                annotation_clip=False)
    ax.text(w / 2 + 1.5 * pitch, -0.11, "0.55 m", fontsize=7.5, ha="center", va="top")
    ax.annotate("", xy=(W - w, -0.30), xytext=(W, -0.30), arrowprops=kw, annotation_clip=False)
    ax.text(W + 0.03, -0.30, "limb 0.25 m", fontsize=7.5, ha="left", va="center")
    ax.set_xlim(-0.55, W + 0.60)
    ax.set_ylim(-0.65, H + 0.36)
    ax.set_title("(a) Three-phase core type (to scale)", fontsize=9.5)
    ax.text(W / 2, -0.58, "radial build: LV 40 mm, oil duct 20 mm, HV 70 mm", fontsize=7.5, ha="center")

    # ---------------- (b) single-phase shell type ----------------
    ax = axb
    wo = 0.20               # outer limb width
    wc = 2 * wo             # centre limb twice as wide
    ww, wh = 0.34, 1.00     # window
    hy = wo
    W = 2 * wo + 2 * ww + wc
    H = wh + 2 * hy
    ax.add_patch(Rectangle((0, 0), W, H, fc=CORE, ec=INK, lw=1.0))
    for x0 in (wo, wo + ww + wc):
        ax.add_patch(Rectangle((x0, hy), ww, wh, fc="white", ec=INK, lw=1.0))
    # interleaved pancake coils around the centre limb (seen in both windows)
    seq = ["LV", "HV", "HV", "LV", "LV", "HV", "HV", "LV"]
    n = len(seq)
    gap = 0.018
    hp = (wh - 0.08 - (n - 1) * gap) / n
    for side in (0, 1):
        x0 = wo + 0.02 if side == 0 else wo + ww + wc + 0.02
        for i, s in enumerate(seq):
            y0 = hy + 0.04 + i * (hp + gap)
            ax.add_patch(Rectangle((x0, y0), ww - 0.04, hp, fc=LVC if s == "LV" else HVC, ec=INK, lw=0.5))
            ax.text(x0 + (ww - 0.04) / 2, y0 + hp / 2, s, fontsize=6.5, ha="center", va="center")
    # flux: up the centre limb, splitting into two return paths
    xcen = wo + ww + wc / 2
    for sgn in (-1, 1):
        xo = xcen + sgn * (ww + wc / 2 + wo / 2)
        xi = xcen + sgn * 0.06
        ax.plot([xi, xi, xo, xo, xi], [hy / 2, H - hy / 2, H - hy / 2, hy / 2, hy / 2],
                ls=(0, (4, 3)), color=BLUE, lw=1.1)
        _farrow(ax, xi, 0.55, xi, 0.75, color=BLUE, lw=1.1, ms=9)
        _farrow(ax, xo, 0.75, xo, 0.55, color=BLUE, lw=1.1, ms=9)
    ax.text(xcen, H + 0.05, r"$\Phi$", fontsize=9, ha="center", va="bottom", color=BLUE)
    ax.text(xcen - (ww + wc / 2 + wo / 2), H + 0.05, r"$\Phi/2$", fontsize=9, ha="center", va="bottom", color=BLUE)
    ax.text(xcen + (ww + wc / 2 + wo / 2), H + 0.05, r"$\Phi/2$", fontsize=9, ha="center", va="bottom", color=BLUE)
    ax.annotate("centre limb (2w)", xy=(xcen - 0.10, 0.10), xytext=(xcen - 0.25, -0.20), fontsize=fs,
                ha="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.annotate("outer limb (w)", xy=(W - wo / 2, 0.30), xytext=(W, -0.38), fontsize=fs, ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.text(W / 2, -0.58, "interleaved pancake coils, HV and LV", fontsize=7.5, ha="center")
    ax.set_xlim(-0.12, W + 0.12)
    ax.set_ylim(-0.65, H + 0.36)
    ax.set_title("(b) Single-phase shell type", fontsize=9.5)
    fig.tight_layout(w_pad=0.5)
    return save(fig, "04", "fig-4-1-core-and-shell-construction")


# ---------------------------------------------------------------------------
# Figure 4.2
# ---------------------------------------------------------------------------
def _shunt_and_load(d, x0, ytop, ybot, items, load_lab, v_lab, xfmr=False):
    """Draw a ladder: source, series items and shunt branches along the top rail.

    items: list of ("series", element, label) or ("shunt", [(element, label), ...]) or ("xfmr",).
    """
    src = d.add(elm.SourceSin().endpoints((x0, ybot), (x0, ytop)).label("$V_1$", loc="top"))
    x = x0
    bottoms = []          # x positions of bottom-rail segments (start, end) pairs
    seg_start = x0
    for it in items:
        if it[0] == "wire":
            d.add(elm.Line().endpoints((x, ytop), (x + it[1], ytop)))
            x += it[1]
        elif it[0] == "series":
            e = it[1]().endpoints((x, ytop), (x + it[3], ytop))
            d.add(e.label(it[2], loc="top") if isinstance(it[2], str) else e.label(it[2][0], loc="top").label(it[2][1], loc="bot"))
            x += it[3]
        elif it[0] == "shunt":
            d.add(elm.Dot().at((x, ytop)))
            e = it[1]().endpoints((x, ytop), (x, ybot))
            if isinstance(it[2], str):
                e = e.label(it[2], loc="bot")
            else:
                e = e.label(it[2][0], loc="bot").label(it[2][1], loc="top")
            d.add(e)
            d.add(elm.Dot().at((x, ybot)))
        elif it[0] == "label":
            d.add(elm.Gap().endpoints((x + it[1], ytop), (x + it[1], ybot)).label(it[2]))
        elif it[0] == "xfmr":
            t = d.add(elm.Transformer(t1=4, t2=4, core=False).anchor("p1").at((x, ytop)))
            d.add(elm.Line().endpoints(t.p2, (t.p2[0], ybot)))
            d.add(elm.Line().endpoints(t.s2, (t.s2[0], ybot)))
            d.add(elm.Dot(radius=0.08).at((t.p1[0] - 0.22, t.p1[1] - 0.45)))
            d.add(elm.Dot(radius=0.08).at((t.s1[0] + 0.22, t.s1[1] - 0.45)))
            d.add(elm.Label().at(((t.p1[0] + t.s1[0]) / 2, ytop + 0.45)).label("$N_1:N_2$"))
            d.add(elm.Label().at(((t.p1[0] + t.s1[0]) / 2, ybot - 0.35)).label("ideal"))
            bottoms.append((seg_start, t.p2[0]))
            seg_start = t.s2[0]
            x = t.s1[0]
    # load and output terminals
    d.add(elm.Dot().at((x, ytop)))
    d.add(elm.Resistor().endpoints((x, ytop), (x, ybot)).label(load_lab, loc="top"))
    d.add(elm.Dot().at((x, ybot)))
    d.add(elm.Line().endpoints((x, ytop), (x + 1.3, ytop)))
    d.add(elm.Line().endpoints((x, ybot), (x + 1.3, ybot)))
    d.add(elm.Dot(open=True).at((x + 1.3, ytop)))
    d.add(elm.Dot(open=True).at((x + 1.3, ybot)))
    d.add(elm.Gap().endpoints((x + 1.3, ytop), (x + 1.3, ybot)).label(["+", v_lab, "−"], loc="bot"))
    bottoms.append((seg_start, x))
    for a, b in bottoms:
        d.add(elm.Line().endpoints((a, ybot), (b, ybot)))


def _draw_on(ax, build):
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=9.5, lw=1.1)
        build(d)
        d.draw(show=False)
    ax.set_aspect("equal")
    ax.axis("off")


def _tee_circuit(ax, referred=False):
    """Exact T circuit; with referred=True the ideal transformer is removed."""
    if not referred:
        items = [("wire", 0.4), ("series", elm.Resistor, "$R_1$", 1.8), ("series", elm.Inductor2, "$jX_{l1}$", 1.8),
                 ("wire", 0.6), ("shunt", elm.Resistor, "$R_c$"), ("wire", 1.4),
                 ("shunt", elm.Inductor2, "$jX_m$"), ("label", 1.6, ["+", "$E_1$", "−"]), ("wire", 2.3), ("xfmr",),
                 ("wire", 0.3), ("series", elm.Resistor, "$R_2$", 1.8), ("series", elm.Inductor2, "$jX_{l2}$", 1.8),
                 ("wire", 0.5)]
        build = lambda d: _shunt_and_load(d, 0, 3, 0, items, "$Z_L$", "$V_2$")
    else:
        items = [("wire", 0.4), ("series", elm.Resistor, "$R_1$", 1.8), ("series", elm.Inductor2, "$jX_{l1}$", 1.8),
                 ("wire", 0.6), ("shunt", elm.Resistor, "$R_c$"), ("wire", 1.4),
                 ("shunt", elm.Inductor2, "$jX_m$"), ("label", 1.6, ["+", "$E_1$", "−"]), ("wire", 2.3),
                 ("series", elm.Resistor, "$R_2'=a^2R_2$", 2.2), ("wire", 0.5),
                 ("series", elm.Inductor2, "$jX_{l2}'=ja^2X_{l2}$", 2.2), ("wire", 0.6)]
        build = lambda d: _shunt_and_load(d, 0, 3, 0, items, "$a^2Z_L$", "$V_2'$")
    _draw_on(ax, build)


def _approx_circuit(ax):
    items = [("wire", 1.0), ("shunt", elm.Resistor, "$R_c$\n$115\\ \\mathrm{k\\Omega}$"), ("wire", 2.4),
             ("shunt", elm.Inductor2, "$jX_m$\n$j34.5\\ \\mathrm{k\\Omega}$"), ("wire", 2.0),
             ("series", elm.Resistor, [r"$R_{eq}=5.88\ \Omega$", "$R_1+R_2'$"], 2.4), ("wire", 0.8),
             ("series", elm.Inductor2, [r"$jX_{eq}=j16.40\ \Omega$", "$j(X_{l1}+X_{l2}')$"], 2.4), ("wire", 0.8)]
    _draw_on(ax, lambda d: _shunt_and_load(d, 0, 3, 0, items, "$a^2Z_L$", "$V_2'$"))


def fig_4_2():
    """Exact, referred and approximate equivalent circuits (100 kVA, 6600/240 V example)."""
    fig, axs = plt.subplots(3, 1, figsize=(6.8, 6.6))
    _tee_circuit(axs[0], referred=False)
    _tee_circuit(axs[1], referred=True)
    _approx_circuit(axs[2])
    titles = ["(a) Exact (T) circuit with ideal transformer",
              "(b) Exact circuit referred to the primary ($a=N_1/N_2$)",
              "(c) Approximate circuit referred to HV: 100 kVA, 6600/240 V example"]
    for ax, t in zip(axs, titles):
        ax.set_title(t, fontsize=9.5, loc="left", pad=12)
    fig.tight_layout(h_pad=1.0)
    return save(fig, "04", "fig-4-2-transformer-equivalent-circuits")


# ---------------------------------------------------------------------------
# Figure 4.3
# ---------------------------------------------------------------------------
def fig_4_3():
    """Phasor diagrams V1 = V2' + I(Req + jXeq) for 0.8 lag, unity, 0.8 lead (drops x5)."""
    r, x = 0.0135, 0.0377
    k = 5.0                      # exaggeration of the impedance drops
    cases = [(-np.degrees(np.arccos(0.8)), "0.8 lagging"), (0.0, "unity"),
             (np.degrees(np.arccos(0.8)), "0.8 leading")]
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 2.7), sharey=True)
    for ax, (ang, name) in zip(axs, cases):
        I = np.exp(1j * np.radians(ang))
        V2 = 1.0 + 0j
        dR = I * r
        dX = 1j * I * x
        V1 = V2 + dR + dX
        p1 = V2 + k * dR
        p2 = p1 + k * dX
        # current (drawn at 0.6 length, own scale)
        Ic = 0.6 * I
        yo = -0.04 if ang == 0 else 0.0
        _farrow(ax, 0, yo, Ic.real, Ic.imag + yo, color=GREEN, lw=1.4, ms=10)
        if ang == 0:
            ax.text(Ic.real - 0.03, yo - 0.03, "$I$", color=GREEN, fontsize=9.5, ha="right", va="top")
        else:
            ax.text(Ic.real + 0.02, Ic.imag + (0.03 if ang > 0 else -0.08), "$I$", color=GREEN, fontsize=9.5)
        _farrow(ax, 0, 0, V2.real, V2.imag, color=INK, lw=1.6)
        ax.text(0.80, -0.045, "$V_2'=1$", ha="center", va="top", fontsize=9.5)
        _farrow(ax, V2.real, V2.imag, p1.real, p1.imag, color=ORANGE, lw=1.3, ms=8)
        _farrow(ax, p1.real, p1.imag, p2.real, p2.imag, color=PINK, lw=1.3, ms=8)
        _farrow(ax, 0, 0, p2.real, p2.imag, color=BLUE, lw=1.6)
        mid = (p1 + p2) / 2
        ax.text(mid.real + 0.035, mid.imag + 0.01, "$jX_{eq}I$", color=PINK, fontsize=9, va="center")
        ax.text(p1.real + 0.02, p1.imag - 0.035, "$R_{eq}I$", color=ORANGE, fontsize=9, ha="left", va="top")
        ax.text(p2.real * 0.5, p2.imag * 0.5 + 0.035, "$V_1$", color=BLUE, fontsize=10, ha="center")
        # delta arc
        dl = np.angle(p2)
        th = np.linspace(0, dl, 30)
        ax.plot(0.95 * np.cos(th), 0.95 * np.sin(th), color=INK, lw=0.7)
        ax.text(0.90 * np.cos(dl / 2) - 0.02, 0.90 * np.sin(dl / 2), r"$\delta$", fontsize=9, va="center", ha="right")
        # phi arc
        if ang != 0:
            th = np.linspace(0, np.radians(ang), 30)
            ax.plot(0.22 * np.cos(th), 0.22 * np.sin(th), color=GREEN, lw=0.7)
            ax.text(0.24 * np.cos(np.radians(ang / 2)), 0.24 * np.sin(np.radians(ang / 2)), r"$\phi$",
                    fontsize=9, color=GREEN, va="center")
        ax.set_title(f"{name}\n$|V_1|$ = {abs(V1):.4f} pu, δ = {np.degrees(np.angle(V1)):.2f}°", fontsize=9)
        ax.set_aspect("equal")
        ax.set_xlim(-0.05, 1.30)
        ax.set_ylim(-0.44, 0.46)
        ax.axis("off")
    fig.text(0.5, 0.02, "Drops $R_{eq}I$ (0.0135 pu) and $jX_{eq}I$ (0.0377 pu) drawn 5× enlarged; "
             "$I$ = 1.0 pu drawn at reduced length.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    return save(fig, "04", "fig-4-3-phasor-diagrams-load-pf")


# ---------------------------------------------------------------------------
# Figure 4.4
# ---------------------------------------------------------------------------
def fig_4_4():
    """Efficiency against load fraction, 100 kVA and 1000 kVA Tier 2 units."""
    x = np.linspace(0.01, 1.25, 600)
    units = [("100 kVA", 100e3, 380.0, 1350.0, BLUE), ("1000 kVA Tier 2", 1000e3, 693.0, 9000.0, ORANGE)]
    fig, ax = new_fig(6.4, 4.0)
    for name, S, P0, Pk, c in units:
        for pf, ls in [(1.0, "-"), (0.8, "--")]:
            eta = 100 * x * S * pf / (x * S * pf + P0 + x ** 2 * Pk)
            ax.plot(x, eta, color=c, ls=ls, label=f"{name}, pf {pf:.1f}")
        xm = np.sqrt(P0 / Pk)
        em = 100 * xm * S / (xm * S + 2 * P0)
        ax.plot(xm, em, "o", color=c, ms=6, zorder=5)
    ax.annotate("x = 0.531, η = 98.59 %", xy=(0.531, 98.59), xytext=(0.66, 97.75), fontsize=8.5, color=BLUE,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    ax.annotate("x = 0.277, η = 99.50 %", xy=(0.2775, 99.50), xytext=(0.36, 99.82), fontsize=8.5, color=ORANGE,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    ax.set_xlim(0, 1.25)
    ax.set_ylim(96, 100)
    ax.set_xlabel("Load fraction $x=S/S_{rated}$")
    ax.set_ylabel("Efficiency η (%)")
    ax.legend(loc="lower right", fontsize=8, ncol=1)
    ax.grid(True, lw=0.5)
    # inset: loss components of the 100 kVA unit
    ins = ax.inset_axes([0.33, 0.10, 0.27, 0.26])
    xi = np.linspace(0, 1.25, 200)
    ins.plot(xi, 380 + 0 * xi, color=INK, lw=1.2)
    ins.plot(xi, 1350 * xi ** 2, color=BLUE, lw=1.2)
    ins.plot(0.531, 380, "o", color=BLUE, ms=4)
    ins.text(1.22, 450, "$P_0$", fontsize=7.5, ha="right")
    ins.text(1.0, 1500, "$x^2P_k$", fontsize=7.5, ha="right", color=BLUE)
    ins.set_xlim(0, 1.25)
    ins.set_ylim(0, 2200)
    ins.set_title("100 kVA losses (W)", fontsize=7.5, pad=2)
    ins.tick_params(labelsize=7)
    ins.set_xlabel("x", fontsize=7.5, labelpad=0)
    return save(fig, "04", "fig-4-4-efficiency-versus-load")


# ---------------------------------------------------------------------------
# Figure 4.5
# ---------------------------------------------------------------------------
def _coil(ax, x, y0, y1, n=4, r=0.16, color=INK, side=1):
    """Vertical coil symbol from y0 to y1 at x (bumps to the right if side=1)."""
    ys = np.linspace(y0, y1, n + 1)
    for a, b in zip(ys[:-1], ys[1:]):
        c = (a + b) / 2
        rr = (b - a) / 2
        th = np.linspace(-np.pi / 2, np.pi / 2, 30)
        ax.plot(x + side * r * np.cos(th), c + rr * np.sin(th), color=color, lw=1.3)


def fig_4_5():
    """Dyn11 winding connections and the HV/LV voltage phasors."""
    fig, (ax, axp) = plt.subplots(1, 2, figsize=(6.8, 4.2), gridspec_kw=dict(width_ratios=[1.25, 1.0]))
    ax.set_aspect("equal")
    ax.axis("off")
    xs = [1.0, 3.0, 5.0]
    hv0, hv1 = 3.0, 4.3
    lv0, lv1 = 0.9, 2.2
    names = ["U", "V", "W"]
    lw = 1.1
    for k, x in enumerate(xs):
        ax.add_patch(Rectangle((x - 0.42, lv0 - 0.15), 0.12, hv1 - lv0 + 0.3, fc=CORE, ec="none"))
        ax.text(x - 0.36, lv0 - 0.32, f"limb {k + 1}", fontsize=7, ha="center", color="#555555")
        _coil(ax, x - 0.30, hv0, hv1, color=ORANGE)
        _coil(ax, x - 0.30, lv0, lv1, color=BLUE)
        ax.plot(x - 0.18, hv1 - 0.12, "o", color=INK, ms=3.5)        # HV dot at top
        ax.plot(x - 0.18, lv0 + 0.12, "o", color=INK, ms=3.5)        # LV dot at bottom
    # HV delta: top of coil k = terminal k; bottom of coil k -> terminal k+1
    yt = 5.75
    for k, x in enumerate(xs):
        xc = x - 0.30
        ax.plot([xc, xc], [hv1, yt], color=INK, lw=lw)
        ax.plot(xc, yt, "o", mfc="white", mec=INK, ms=6)
        ax.text(xc, yt + 0.15, f"1{names[k]}", ha="center", va="bottom", fontsize=9)
    for k, x in enumerate(xs):
        xc = x - 0.30
        xn = xs[(k + 1) % 3] - 0.30
        xj = xc + 1.0
        yj = 4.75 if k < 2 else 5.25
        ax.plot([xc, xc, xj, xj, xn], [hv0, hv0 - 0.25, hv0 - 0.25, yj, yj], color=INK, lw=lw)
        ax.plot(xn, yj, "o", color=INK, ms=3.5)
    # LV star: top ends (non-dot) to the neutral bus, dot ends to terminals at the bottom
    yn = 2.55
    ax.plot([xs[0] - 0.30, xs[2] + 1.0], [yn, yn], color=INK, lw=lw)
    for k, x in enumerate(xs):
        xc = x - 0.30
        ax.plot([xc, xc], [lv1, yn], color=INK, lw=lw)
        ax.plot(xc, yn, "o", color=INK, ms=3.5)
        ax.plot([xc, xc], [lv0, 0.25], color=INK, lw=lw)
        ax.plot(xc, 0.25, "o", mfc="white", mec=INK, ms=6)
        ax.text(xc + 0.15, 0.20, f"2{names[k]}", ha="left", va="top", fontsize=9)
    ax.plot(xs[2] + 1.0, yn, "o", mfc="white", mec=INK, ms=6)
    ax.text(xs[2] + 1.0, yn + 0.15, "2N", ha="center", va="bottom", fontsize=9)
    ax.text(5.95, 3.65, "HV delta\n11 kV\n11 000 V\nper phase", fontsize=7.5, color=ORANGE, va="center")
    ax.text(5.95, 1.45, "LV star\n433 V\n250 V\nper phase", fontsize=7.5, color=BLUE, va="center")
    ax.set_xlim(0.2, 7.3)
    ax.set_ylim(-0.2, 6.3)
    ax.set_title("(a) Windings (1000 kVA, 11 kV/433 V Dyn11)", fontsize=9.5)

    # phasor diagram
    axp.set_aspect("equal")
    axp.axis("off")
    R = 1.0
    th = np.linspace(0, 2 * np.pi, 200)
    axp.plot(1.32 * np.cos(th), 1.32 * np.sin(th), color="#BBBBBB", lw=0.8)
    for h in range(12):
        a = np.radians(90 - 30 * h)
        axp.plot([1.25 * np.cos(a), 1.32 * np.cos(a)], [1.25 * np.sin(a), 1.32 * np.sin(a)], color="#888888", lw=0.8)
    axp.text(0, 1.40, "12", ha="center", va="bottom", fontsize=9)
    a11 = np.radians(120)
    axp.text(1.45 * np.cos(a11), 1.45 * np.sin(a11), "11", ha="center", va="center", fontsize=9)
    hv = {n: R * np.exp(1j * np.radians(a)) for n, a in zip(names, [90, -30, 210])}
    tri = [hv["U"], hv["V"], hv["W"], hv["U"]]
    axp.plot([z.real for z in tri], [z.imag for z in tri], color=ORANGE, lw=1.6)
    for n, z in hv.items():
        axp.plot(z.real, z.imag, "o", color=ORANGE, ms=4)
    axp.text(hv["U"].real + 0.08, hv["U"].imag + 0.02, "1U", color=ORANGE, fontsize=9)
    axp.text(hv["V"].real + 0.05, hv["V"].imag - 0.12, "1V", color=ORANGE, fontsize=9)
    axp.text(hv["W"].real - 0.18, hv["W"].imag - 0.12, "1W", color=ORANGE, fontsize=9)
    rl = 0.62
    for n, a in zip(names, [120, 0, 240]):
        z = rl * np.exp(1j * np.radians(a))
        _farrow(axp, 0, 0, z.real, z.imag, color=BLUE, lw=1.5, ms=10)
        off = 0.13 * np.exp(1j * np.radians(a))
        axp.text(z.real + off.real, z.imag + off.imag, f"2{n}", color=BLUE, fontsize=9, ha="center", va="center")
    axp.plot(0, 0, "o", color=BLUE, ms=3)
    axp.text(0.05, -0.12, "2N", color=BLUE, fontsize=8)
    # 30 degree arc between the 1U direction (12 o'clock) and 2U (11 o'clock)
    a = np.linspace(np.radians(90), np.radians(120), 30)
    axp.plot(0.42 * np.cos(a), 0.42 * np.sin(a), color=INK, lw=0.8)
    axp.plot([0, 0], [0, 0.95], color="#888888", lw=0.7, ls=":")
    axp.text(-0.02, 0.52, "30°", fontsize=8, ha="right")
    axp.set_xlim(-1.6, 1.6)
    axp.set_ylim(-1.45, 1.65)
    axp.set_title("(b) Phasors: 2U leads 1U by 30°", fontsize=9.5)
    axp.text(0, -1.42, "HV triangle (line-to-line); LV star from 2N", fontsize=7.5, ha="center")
    fig.tight_layout(w_pad=0.3)
    return save(fig, "04", "fig-4-5-dyn11-connection-and-vectors")


# ---------------------------------------------------------------------------
# Figure 4.6
# ---------------------------------------------------------------------------
def _ct_emf(I):
    """Smooth excitation curve: log-log slope 1.38 below the knee, 0.03 in saturation,
    fitted through 5 V at 2 mA, 380 V at 50 mA and 450 V at 2 A."""
    a, m1, m2, xk, w = 10.20808, 1.38362, 0.03, -3.04342, 0.09226
    x = np.log(I)
    return np.exp(a + m1 * x - (m1 - m2) * w * np.logaddexp(0, (x - xk) / w))


def fig_4_6():
    """Excitation characteristic of a 400/1 A 5P20 CT with required EMFs."""
    I = np.logspace(-3, 1, 600)
    V = _ct_emf(I)
    # IEC knee: a 10 % rise in voltage needs a 50 % rise in current
    f = _ct_emf(1.5 * I) / V - 1.1
    k = np.where(np.diff(np.sign(f)))[0][0]
    Ik, Vk = I[k], V[k]
    fig, ax = new_fig(6.4, 4.0)
    ax.loglog(I, V, color=BLUE, lw=2.0, label="excitation characteristic")
    ax.plot(Ik, Vk, "o", color=INK, ms=6, zorder=5)
    ax.plot([Ik, 1.5 * Ik], [Vk, 1.1 * Vk], color=INK, lw=0.8)
    ax.annotate(f"knee point ≈ {Vk:.0f} V at {1000 * Ik:.0f} mA\n(+10 % V needs +50 % I)", xy=(Ik, Vk),
                xytext=(0.12, 120), fontsize=8.5, arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    lines = [(360, "required at ALF 20,\nrated burden 15 Ω: 360 V", ORANGE, 1.1e-3, "left"),
             (246, "25 kA symmetrical fault,\nactual burden: 246 V", PINK, 1.1e-3, "left"),
             (78.8, "required at ALF 20, actual burden 3.94 Ω: 78.8 V", GREEN, 9.0, "right")]
    for v, txt, c, xt, ha in lines:
        ax.axhline(v, color=c, ls="--", lw=1.2)
        ax.text(xt, v * (1.06 if v == 360 else 0.94), txt, color=c, fontsize=8.5, ha=ha,
                va="bottom" if v == 360 else "top")
    ax.text(0.003, 4.5, "linear region", fontsize=8.5, color=BLUE, rotation=29)
    ax.text(2.2, 520, "saturation", fontsize=8.5, color=BLUE, ha="center", va="bottom")
    ax.set_xlim(1e-3, 10)
    ax.set_ylim(1, 1000)
    ax.set_xlabel("Secondary excitation current (A rms)")
    ax.set_ylabel("Secondary EMF (V rms)")
    ax.grid(True, which="both", lw=0.4)
    return save(fig, "04", "fig-4-6-ct-excitation-and-burden")


if __name__ == "__main__":
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    fig_4_5()
    fig_4_6()
