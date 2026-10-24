"""Figures for Chapter 9 — Electrical Machine Design and Performance.

Run from the repository root:  python figures/scripts/ch09.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Patch

from figstyle import new_fig, schematic, save, COLORS, INK

BLUE, ORANGE, GREEN, PINK, YELLOW, SKY = COLORS[:6]


# ---------------------------------------------------------------------------
def _first_order(t, segments, tau, th0=0.0):
    """Temperature rise for piecewise-constant ultimate rises.
    segments: list of (t_end, theta_inf) in increasing t_end."""
    out = np.empty_like(t)
    th_start, t_start = th0, 0.0
    idx = 0
    for t_end, th_inf in segments:
        m = (t >= t_start) & (t <= t_end)
        out[m] = th_inf + (th_start - th_inf) * np.exp(-(t[m] - t_start) / tau)
        th_start = th_inf + (th_start - th_inf) * np.exp(-(t_end - t_start) / tau)
        t_start = t_end
    return out


def fig_9_1():
    """Temperature rise under S1, S2 30 min and S3 40 % duty."""
    tau, th_r = 73.0, 80.0
    t = np.linspace(0, 300, 30001)
    s1 = th_r * (1 - np.exp(-t / tau))
    s2 = _first_order(t, [(30, 2.97 * th_r), (300, 0.0)], tau)
    segs = []
    for k in range(30):
        segs += [(10 * k + 4, 2.5 * th_r), (10 * k + 10, 0.0)]
    s3 = _first_order(t, segs, tau)
    a, b = np.exp(-4 / tau), np.exp(-6 / tau)
    hi = 2.5 * th_r * (1 - a) / (1 - a * b)
    lo = hi * b
    fig, ax = new_fig(6.4, 3.9)
    ax.axhspan(lo, hi, color="#F3E6F0", zorder=0)
    ax.plot(t, s3, color=PINK, lw=1.0, label="S3 40 % (4 min on, 6 min off) at 2.5× rated loss")
    ax.plot(t, s1, color=BLUE, lw=2.0, label="S1 continuous at rated loss")
    ax.plot(t, s2, color=ORANGE, lw=2.0, label="S2 30 min at 2.97× rated loss")
    ax.axhline(80, color=INK, ls="--", lw=0.9)
    ax.axhline(105, color=INK, ls="--", lw=0.9)
    ax.text(100, 84.5, "80 K: class B rise limit", ha="left", va="bottom", fontsize=8)
    ax.text(298, 106, "105 K: class F rise limit", ha="right", va="bottom", fontsize=8)
    ax.plot(73, th_r * (1 - np.exp(-1)), "o", color=BLUE, ms=4)
    ax.annotate(r"$\tau$ = 73 min, 50.6 K (63 %)", xy=(73, 50.6), xytext=(90, 42), fontsize=8,
                color=BLUE, arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    ax.plot(30, s2[np.searchsorted(t, 30)], "o", color=ORANGE, ms=4)
    ax.annotate("80 K at 30 min,\nthen cools", xy=(30, 80), xytext=(42, 92), fontsize=8, color=ORANGE,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))
    ax.annotate(f"steady band {lo:.1f}–{hi:.1f} K", xy=(255, lo), xytext=(205, 60), fontsize=8,
                color=PINK, arrowprops=dict(arrowstyle="-", lw=0.6, color=PINK))
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 110)
    ax.set_xticks(np.arange(0, 301, 30))
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Winding temperature rise (K)")
    ax.legend(loc="lower right", fontsize=7.5, bbox_to_anchor=(1.0, 0.17))
    save(fig, "09", "fig-9-1-duty-cycle-temperature")


# ---------------------------------------------------------------------------
def fig_9_2():
    """Loss components and efficiency of the 75 kW IE3 motor against load."""
    x = np.linspace(0, 1.25, 501)
    core, fw = 0.789, 0.355
    scu, rcu, stray = 1.421 * x ** 2, 0.750 * x ** 2, 0.632 * x ** 2
    layers = [np.full_like(x, core), np.full_like(x, fw), scu, rcu, stray]
    labels = ["core 0.789 kW", "friction & windage 0.355 kW", "stator copper 1.421$x^2$",
              "rotor copper 0.750$x^2$", "stray load 0.632$x^2$"]
    cols = ["#9DB7CF", "#C9D7E4", "#E9A27A", "#F2C4A6", "#E8D9A8"]
    fig, ax = new_fig(6.4, 4.0)
    ax.stackplot(x, layers, colors=cols, labels=labels, edgecolor="white", linewidth=0.4)
    P0 = core + fw
    PL = 2.803 * x ** 2
    ax.plot(x, np.full_like(x, P0), color=INK, lw=1.0, ls="--")
    ax.plot(x, PL, color=INK, lw=1.0, ls=":")
    ax.text(1.24, P0 + 0.05, "fixed losses 1.145 kW", ha="right", va="bottom", fontsize=7.5)
    ax.text(1.02, 2.803 * 1.02 ** 2 + 0.75, "load losses\n2.803$x^2$", ha="left", va="bottom", fontsize=7.5)
    ax.annotate("", xy=(1.06, 2.803 * 1.06 ** 2), xytext=(1.05, 2.803 * 1.02 ** 2 + 0.75),
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.set_xlim(0, 1.25)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel("Load fraction $x$ (output / rated)")
    ax.set_ylabel("Loss (kW)")
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    xe = x[x >= 0.1]
    eta = 75 * xe / (75 * xe + P0 + 2.803 * xe ** 2) * 100
    ax2.plot(xe, eta, color=BLUE, lw=2.2)
    xo = np.sqrt(P0 / 2.803)
    eo = 75 * xo / (75 * xo + 2 * P0) * 100
    ax2.plot(xo, eo, "o", color=BLUE, ms=6)
    ax2.annotate(f"$\\eta_{{max}}$ = {eo:.1f} % at $x$ = {xo:.2f}", xy=(xo, eo), xytext=(0.30, 96.45),
                 fontsize=8.5, color=BLUE, ha="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=BLUE))
    for xp in (0.25, 0.5, 0.75, 1.0, 1.15):
        ep = 75 * xp / (75 * xp + P0 + 2.803 * xp ** 2) * 100
        ax2.plot(xp, ep, "o", mfc="white", mec=BLUE, ms=4)
        ax2.text(xp, ep - 0.22, f"{ep:.1f}", ha="center", va="top", fontsize=7.5, color=BLUE)
    ax.axvline(xo, color="#777777", lw=0.7, ls=":")
    ax.plot(xo, P0, "o", color=INK, ms=4)
    ax2.set_ylim(85, 97)
    ax2.set_ylabel("Efficiency (%)", color=BLUE)
    ax2.text(0.13, 88.3, "efficiency", color=BLUE, fontsize=9)
    ax.legend(loc="upper center", fontsize=7.5, bbox_to_anchor=(0.5, -0.17), ncol=3)
    save(fig, "09", "fig-9-2-losses-efficiency-vs-load")


# ---------------------------------------------------------------------------
def _resistor(ax, p0, p1, label, value, side=+1, n=6, amp=0.16, lead=0.35, color=INK, fs=7.5):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nrm = np.array([-u[1], u[0]])
    lead = max((L - 1.6) / 2, 0.2)
    body = L - 2 * lead
    pts = [p0, p0 + lead * u]
    for k in range(n):
        s = lead + body * (k + 0.5) / n
        pts.append(p0 + s * u + amp * (1 if k % 2 == 0 else -1) * nrm)
    pts += [p0 + (L - lead) * u, p1]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.1)
    mid = p0 + d / 2
    off = nrm * side * 0.42
    horiz = abs(u[0]) > 0.5
    ax.text(*(mid + off), f"{label}\n{value}", ha="center" if horiz else ("left" if side * nrm[0] > 0 else "right"),
            va=("bottom" if side * nrm[1] > 0 else "top") if horiz else "center", fontsize=fs, color=color,
            linespacing=1.1)


def _isource(ax, gnd, node, label, color=ORANGE, r=0.38):
    gnd, node = np.asarray(gnd, float), np.asarray(node, float)
    c = (gnd + node) / 2
    u = (node - gnd) / np.hypot(*(node - gnd))
    ax.plot([gnd[0], (c - r * u)[0]], [gnd[1], (c - r * u)[1]], color=INK, lw=1.1)
    ax.plot([(c + r * u)[0], node[0]], [(c + r * u)[1], node[1]], color=INK, lw=1.1)
    ax.add_patch(Circle(c, r, fc="white", ec=color, lw=1.3, zorder=3))
    ax.annotate("", xy=c + 0.26 * u, xytext=c - 0.26 * u,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, mutation_scale=8), zorder=4)
    ax.text(c[0] + 0.5, c[1], label, ha="left", va="center", fontsize=7.5, color=color)
    _ground(ax, gnd)


def _ground(ax, p):
    x, y = p
    for k, w in enumerate((0.32, 0.21, 0.10)):
        ax.plot([x - w, x + w], [y - 0.1 * k, y - 0.1 * k], color=INK, lw=1.1)


def _wire(ax, *pts):
    pts = np.array(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=1.1)


def _node(ax, p, name, rise, dx=0.0, dy=0.25, ha="center", va="bottom"):
    ax.add_patch(Circle(p, 0.09, fc=INK, ec=INK, zorder=5))
    ax.text(p[0] + dx, p[1] + dy, f"{name}\n{rise:.0f} K", ha=ha, va=va, fontsize=8, weight="bold",
            color=BLUE, linespacing=1.1)


def _solve_thermal():
    # nodes: 0 slot, 1 end winding, 2 teeth, 3 yoke, 4 rotor, 5 internal air, 6 frame
    R = {(0, 2): 0.008, (1, 5): 0.03, (2, 3): 0.004, (3, 6): 0.006, (4, 2): 0.02, (5, 6): 0.03, (6, -1): 0.0125}
    P = np.array([0.6 * 1421, 0.4 * 1421, 0.4 * 789, 0.6 * 789, 1382, 355, 0.0])
    G = np.zeros((7, 7))
    for (a, b), r in R.items():
        g = 1 / r
        G[a, a] += g
        if b >= 0:
            G[b, b] += g
            G[a, b] -= g
            G[b, a] -= g
    return np.linalg.solve(G, P), P


def fig_9_3():
    """Lumped thermal network of the 75 kW TEFC motor."""
    th, P = _solve_thermal()
    fig, ax = schematic(6.8, 4.9, xlim=(-0.3, 16.6), ylim=(-1.4, 11.9))
    S, T, Y = (2.0, 4.6), (6.0, 4.6), (10.0, 4.6)
    E, Ro, A = (2.0, 8.1), (6.0, 8.1), (10.0, 8.1)
    Fb, Ft = (13.5, 4.6), (13.5, 8.1)
    g = 0.6                                    # ground level for the lower sources
    # resistors
    _resistor(ax, S, T, "slot insulation", "0.008 K/W", side=-1)
    _resistor(ax, T, Y, "teeth→yoke", "0.004 K/W", side=-1)
    _resistor(ax, Y, Fb, "yoke→frame contact", "0.006 K/W", side=-1)
    _resistor(ax, Ro, T, "rotor→air gap\n→stator", "0.02 K/W", side=-1)
    _wire(ax, A, (11.2, 8.1))
    _resistor(ax, (11.2, 8.1), Ft, "internal air→frame", "0.03 K/W", side=+1)
    _wire(ax, E, (2.0, 10.6))
    _wire(ax, A, (10.0, 10.6))
    _resistor(ax, (2.0, 10.6), (10.0, 10.6), "end winding→internal air", "0.03 K/W", side=+1)
    _wire(ax, Fb, Ft)
    _resistor(ax, Fb, (13.5, g), "frame→ambient\n(external fan)", "0.0125 K/W", side=+1)
    _ground(ax, (13.5, g))
    ax.text(13.95, g - 0.1, "ambient\n40 °C", ha="left", va="center", fontsize=7.5)
    # heat sources (current sources from the ambient reference)
    _isource(ax, (2.0, g), S, f"{P[0] / 1e3:.2f} kW\nslot Cu (60 %)")
    _isource(ax, (6.0, g), T, f"{P[2] / 1e3:.2f} kW\ncore (teeth)")
    _isource(ax, (10.0, g), Y, f"{P[3] / 1e3:.2f} kW\ncore (yoke)")
    _wire(ax, E, (0.6, 8.1))
    _isource(ax, (0.6, 6.0), (0.6, 8.1), f"{P[1] / 1e3:.2f} kW\nend Cu")
    _wire(ax, Ro, (7.6, 8.1))
    _isource(ax, (7.6, 6.0), (7.6, 8.1), f"{P[4] / 1e3:.2f} kW\nrotor Cu\n+ stray")
    _isource(ax, (11.0, 6.0), (11.0, 8.1), f"{P[5] / 1e3:.2f} kW\nF&W")
    # nodes
    _node(ax, S, "slot winding", th[0], dx=-0.2, dy=0.15, ha="right")
    _node(ax, T, "teeth", th[2], dx=0.2, dy=0.15, ha="left")
    _node(ax, Y, "yoke", th[3], dx=0.2, dy=0.15, ha="left")
    _node(ax, E, "end winding", th[1], dx=0.2, dy=0.15, ha="left")
    _node(ax, Ro, "rotor", th[4], dx=0.2, dy=0.15, ha="left")
    _node(ax, A, "internal\nair", th[5], dx=-0.2, dy=0.15, ha="right")
    _node(ax, (13.5, 6.35), "frame", th[6], dx=0.2, dy=0.0, ha="left", va="center")
    avg = 0.6 * th[0] + 0.4 * th[1]
    ax.text(8.1, -0.25,
            f"Solved rises above ambient (total loss {P.sum() / 1e3:.2f} kW): winding average ≈ {avg:.0f} K, "
            f"end-winding hot spot ≈ {th[1]:.0f} K, equivalent ≈ {avg / P.sum():.3f} K/W\n"
            f"(single-body value of §9.3: 80 K / 3.95 kW = 0.020 K/W). Resistance values are illustrative.",
            ha="center", va="top", fontsize=7, color="#444444", linespacing=1.3)
    save(fig, "09", "fig-9-3-motor-thermal-network")


# ---------------------------------------------------------------------------
def fig_9_4():
    """Slot cross-section of a 6.6 kV form-wound two-layer winding."""
    W, D = 14.0, 60.0
    strand_t, strand_w, s_ins, turn_ins, gw, arm = 1.2, 5.0, 0.1, 0.3, 2.2, 0.2
    n_turns = 6
    turn_h = 2 * (strand_t + 2 * s_ins) + 2 * turn_ins
    turn_w = strand_w + 2 * s_ins + 2 * turn_ins
    cs_h = n_turns * turn_h + 2 * (gw + arm)
    cs_w = turn_w + 2 * (gw + arm)
    bottom_pack, sep, wedge = 1.0, 2.0, 5.0
    top_fill = D - wedge - bottom_pack - 2 * cs_h - sep
    side = (W - cs_w) / 2
    C = dict(core="#C9CED6", copper="#D9822B", strand="#7A3E10", turn="#F3E3A0", gw="#B8860B",
             armour="#333333", wedge="#7FA37A", pack="#E7E1D0", sep="#A9C7E3")
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ax.set_aspect("equal")
    ax.axis("off")
    # laminated core around slot
    ax.add_patch(Rectangle((-12, -6), W + 24, D + 6, fc=C["core"], ec=INK, lw=0.8))
    for yy in np.arange(-5, D, 1.6):
        ax.plot([-12, 0], [yy, yy], color="#AEB4BD", lw=0.4)
        ax.plot([W, W + 12], [yy, yy], color="#AEB4BD", lw=0.4)
    for xx in np.arange(-11.5, W + 12, 1.6):
        ax.plot([xx, xx], [-6, -0.01], color="#AEB4BD", lw=0.0)
    ax.add_patch(Rectangle((0, 0), W, D, fc="white", ec=INK, lw=1.0))
    # packing / wedge / separator
    ax.add_patch(Rectangle((0, 0), W, bottom_pack, fc=C["pack"], ec=INK, lw=0.4))
    y_cs1 = bottom_pack
    y_sep = y_cs1 + cs_h
    y_cs2 = y_sep + sep
    y_fill = y_cs2 + cs_h
    ax.add_patch(Rectangle((0, y_sep), W, sep, fc=C["sep"], ec=INK, lw=0.4))
    ax.add_patch(Rectangle((0, y_fill), W, top_fill, fc=C["pack"], ec=INK, lw=0.4))
    ax.add_patch(Rectangle((-0.8, D - wedge), W + 1.6, wedge, fc=C["wedge"], ec=INK, lw=0.6))
    ax.add_patch(Rectangle((0, D - 0.01), W, 0.02, fc="white", ec="none"))
    for y0 in (y_cs1, y_cs2):
        ax.add_patch(Rectangle((0, y0), side, cs_h, fc=C["pack"], ec=INK, lw=0.3))
        ax.add_patch(Rectangle((W - side, y0), side, cs_h, fc=C["pack"], ec=INK, lw=0.3))
        x0 = side
        ax.add_patch(Rectangle((x0, y0), cs_w, cs_h, fc=C["armour"], ec=INK, lw=0.4))
        ax.add_patch(Rectangle((x0 + arm, y0 + arm), cs_w - 2 * arm, cs_h - 2 * arm, fc=C["gw"], ec="none"))
        xi, yi = x0 + arm + gw, y0 + arm + gw
        for k in range(n_turns):
            ty = yi + k * turn_h
            ax.add_patch(Rectangle((xi, ty), turn_w, turn_h, fc=C["turn"], ec=INK, lw=0.25))
            for s in range(2):
                sy = ty + turn_ins + s * (strand_t + 2 * s_ins)
                ax.add_patch(Rectangle((xi + turn_ins, sy), strand_w + 2 * s_ins, strand_t + 2 * s_ins,
                                       fc=C["strand"], ec="none"))
                ax.add_patch(Rectangle((xi + turn_ins + s_ins, sy + s_ins), strand_w, strand_t,
                                       fc=C["copper"], ec="none"))
    # dimensions
    def dim_h(x0, x1, y, text, va="bottom"):
        ax.annotate("", xy=(x0, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
        ax.text((x0 + x1) / 2, y + (0.6 if va == "bottom" else -0.6), text, ha="center", va=va, fontsize=7.5)

    def dim_v(x, y0, y1, text, ha="left"):
        ax.annotate("", xy=(x, y0), xytext=(x, y1),
                    arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
        ax.text(x + (0.7 if ha == "left" else -0.7), (y0 + y1) / 2, text, ha=ha, va="center", fontsize=7.5)

    dim_h(0, W, D + 3.0, "14 mm (open slot)")
    ax.plot([0, 0], [D, D + 3.6], color=INK, lw=0.5)
    ax.plot([W, W], [D, D + 3.6], color=INK, lw=0.5)
    dim_v(-26, 0, D, "60 mm", ha="right")
    ax.text(W + 0.8, D + 0.8, "bore (air-gap side)", ha="left", va="bottom", fontsize=7, color="#555555")
    ax.plot([-26.6, -12], [0, 0], color=INK, lw=0.5, ls=":")
    ax.plot([-26.6, -12], [D, D], color=INK, lw=0.5, ls=":")
    dim_v(-14, y_cs2, y_cs2 + cs_h, f"{cs_h:.1f} mm", ha="right")
    ax.plot([-14.6, side], [y_cs2, y_cs2], color=INK, lw=0.4, ls=":")
    ax.plot([-14.6, side], [y_cs2 + cs_h, y_cs2 + cs_h], color=INK, lw=0.4, ls=":")
    dim_h(side, side + cs_w, -9.5, f"coil side {cs_w:.1f} mm", va="top")
    ax.plot([side, side], [y_cs1, -10.1], color=INK, lw=0.4, ls=":")
    ax.plot([side + cs_w, side + cs_w], [y_cs1, -10.1], color=INK, lw=0.4, ls=":")
    # callouts on right
    kw = dict(fontsize=7.5, va="center", ha="left", arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    xr = W + 19
    ax.annotate("slot wedge 5 mm", xy=(W - 1, D - 2.5), xytext=(xr, D - 2.5), **kw)
    ax.annotate(f"filler {top_fill:.1f} mm", xy=(W - 1, y_fill + top_fill / 2), xytext=(xr, D - 7.5), **kw)
    ax.annotate("top coil side", xy=(W - side - 0.5, y_cs2 + cs_h - 4), xytext=(xr, y_cs2 + cs_h - 4), **kw)
    ax.annotate("separator 2 mm", xy=(W - 1, y_sep + 1), xytext=(xr, y_sep + 1), **kw)
    ax.annotate("bottom coil side", xy=(W - side - 0.5, y_cs1 + 10), xytext=(xr, y_cs1 + 10), **kw)
    ax.annotate("bottom packing", xy=(W - 1, 0.5), xytext=(xr, 1.5), **kw)
    ax.annotate("side packing", xy=(W - side / 2, y_cs1 + cs_h / 2 + 4), xytext=(xr, y_cs1 + 18), **kw)
    # legend of materials
    items = [("copper strand 1.2 × 5 mm", C["copper"]), ("strand insulation 0.1 mm", C["strand"]),
             ("turn insulation (mica tape) 0.3 mm", C["turn"]), ("groundwall mica–epoxy 2.2 mm", C["gw"]),
             ("semiconducting armour 0.2 mm", C["armour"]), ("slot wedge", C["wedge"]),
             ("packing / filler", C["pack"]), ("separator", C["sep"]), ("laminated core", C["core"])]
    handles = [Patch(fc=c, ec=INK, lw=0.4, label=l) for l, c in items]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 0.0), fontsize=7, handlelength=1.4,
              title="6 turns × 2 strands per coil side", title_fontsize=7.5)
    ax.set_xlim(-100, W + 46)
    ax.set_ylim(-14, D + 7)
    save(fig, "09", "fig-9-4-form-wound-slot-cross-section")


# ---------------------------------------------------------------------------
def fig_9_5():
    """Thermal life of class B, F and H insulation (10 K halving rule)."""
    T = np.linspace(100, 200, 201)
    fig, ax = new_fig(6.4, 4.0)
    for Tc, lab, c in ((130, "class B (130)", BLUE), (155, "class F (155)", ORANGE), (180, "class H (180)", GREEN)):
        L = 20000 * 2 ** ((Tc - T) / 10)
        ax.semilogy(T, L, color=c, lw=2.0)
        x_lab = Tc + (5 if Tc == 180 else 12)
        ax.text(x_lab + 1.5, 20000 * 2 ** ((Tc - x_lab) / 10) * 1.15, lab, color=c, fontsize=8.5,
                rotation=-33, ha="left", va="bottom", rotation_mode="anchor")
    ax.axhline(100000, color="#777777", ls="--", lw=0.9)
    ax.axhline(20000, color="#777777", ls=":", lw=0.9)
    ax.text(199, 108000, "100 000 h (≈ 11 years continuous)", ha="right", va="bottom", fontsize=8)
    ax.text(101, 21500, "20 000 h (nominal life at class temperature)", ha="left", va="bottom", fontsize=8)
    pts = [(120, "120 °C: 226 000 h\n(full load, 30 °C ambient)", (102, 520000)),
           (130, "130 °C: 113 000 h\n(full load, 40 °C ambient)", (139, 300000)),
           (155, "155 °C: 20 000 h\n(120 % load)", (101, 1300))]
    for Th, lab, xyt in pts:
        L = 20000 * 2 ** ((155 - Th) / 10)
        ax.plot(Th, L, "o", color=ORANGE, mec=INK, ms=6, zorder=5)
        ax.annotate(lab, xy=(Th, L), xytext=xyt, fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.set_xlim(100, 200)
    ax.set_ylim(1e3, 1e6)
    ax.set_xlabel("Hot-spot temperature (°C)")
    ax.set_ylabel("Thermal life (h)")
    ax.grid(True, which="major", color="#EEEEEE", lw=0.6)
    save(fig, "09", "fig-9-5-insulation-life-vs-temperature")


# ---------------------------------------------------------------------------
def fig_9_6():
    """Failure causes of large induction motors, IEEE and EPRI surveys."""
    cats = ["Bearings", "Stator winding", "Rotor", "Other"]
    ieee = [44, 26, 8, 22]
    epri = [41, 36, 9, 14]
    mech = ["lubrication faults, misalignment,\nbearing currents (VFD)",
            "insulation ageing, contamination,\nsurges, loose coils",
            "broken bars on frequent or\nhigh-inertia starts",
            "external and accessory\nfailures, unknown"]
    y = np.arange(len(cats))[::-1]
    h = 0.36
    fig, ax = new_fig(6.4, 3.6)
    b1 = ax.barh(y + h / 2, ieee, h, color=BLUE, label="IEEE survey")
    b2 = ax.barh(y - h / 2, epri, h, color=ORANGE, label="EPRI survey")
    for bars in (b1, b2):
        for r in bars:
            ax.text(r.get_width() + 0.6, r.get_y() + r.get_height() / 2, f"{r.get_width():.0f} %",
                    va="center", fontsize=8)
    for yy, m, a, b in zip(y, mech, ieee, epri):
        ax.text(max(a, b) + 6.5, yy, m, va="center", fontsize=7.5, color="#444444")
    ax.set_yticks(y)
    ax.set_yticklabels(cats)
    ax.set_xlim(0, 50)
    ax.set_xticks(np.arange(0, 51, 10))
    ax.set_xlabel("Share of failures (%)")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(0, 80)
    ax.spines["bottom"].set_bounds(0, 50)
    save(fig, "09", "fig-9-6-motor-failure-causes")


if __name__ == "__main__":
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    fig_9_5()
    fig_9_6()
