"""Figures for Chapter 18 — Power-Flow Analysis.

Run from the repository root:  python figures/scripts/ch18.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Polygon, FancyBboxPatch  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402

CH = "18"

# ------------------------------------------------- three-bus example model
LINES = [(0, 1, 0.02 + 0.10j, 0.04), (0, 2, 0.015 + 0.08j, 0.03), (1, 2, 0.02 + 0.10j, 0.04)]


def ybus(shunt2=0.0):
    Y = np.zeros((3, 3), complex)
    for i, k, z, B in LINES:
        y = 1 / z
        Y[i, i] += y + 1j * B / 2
        Y[k, k] += y + 1j * B / 2
        Y[i, k] -= y
        Y[k, i] -= y
    Y[1, 1] += 1j * shunt2
    return Y


def newton(Y, lam=1.0, q3_fixed=None, tol=1e-10):
    """Newton-Raphson (numerical Jacobian) for the three-bus system.

    Bus 1 slack 1.05/0; bus 2 PQ load lam*(3.0 + j1.4) pu; bus 3 PV 2.0 pu at 1.03 pu,
    or PQ with Q3 = q3_fixed when its reactive limit is enforced."""
    V = np.array([1.05, 1.0, 1.03])
    d = np.zeros(3)
    P2, Q2, P3 = -3.0 * lam, -1.4 * lam, 2.0

    def unpack(x):
        dd, VV = d.copy(), V.copy()
        dd[1], dd[2], VV[1] = x[:3]
        if q3_fixed is not None:
            VV[2] = x[3]
        return dd, VV

    def calc(x):
        dd, VV = unpack(x)
        Vc = VV * np.exp(1j * dd)
        S = Vc * np.conj(Y @ Vc)
        r = [S[1].real, S[2].real, S[1].imag]
        if q3_fixed is not None:
            r.append(S[2].imag)
        return np.array(r)

    spec = np.array([P2, P3, Q2] + ([q3_fixed] if q3_fixed is not None else []))
    x = np.array([0.0, 0.0, 1.0] + ([1.03] if q3_fixed is not None else []))
    for _ in range(40):
        F = spec - calc(x)
        if np.abs(F).max() < tol:
            break
        J = np.zeros((len(x), len(x)))
        f0 = calc(x)
        for j in range(len(x)):
            xx = x.copy()
            xx[j] += 1e-7
            J[:, j] = (calc(xx) - f0) / 1e-7
        x = x + np.linalg.solve(J, F)
    d, V = unpack(x)
    Vc = V * np.exp(1j * d)
    S = Vc * np.conj(Y @ Vc)
    return V, np.degrees(d), S * 100  # MVA


def branch_flows(V, d):
    Vc = V * np.exp(1j * np.radians(d))
    out = {}
    for i, k, z, B in LINES:
        y = 1 / z
        out[(i, k)] = Vc[i] * np.conj((Vc[i] - Vc[k]) * y + Vc[i] * 1j * B / 2) * 100
        out[(k, i)] = Vc[k] * np.conj((Vc[k] - Vc[i]) * y + Vc[k] * 1j * B / 2) * 100
    return out


# --------------------------------------------------- 18.1 three-bus system
def fig_18_1():
    Y = ybus()
    V, d, S = newton(Y)
    F = branch_flows(V, d)
    fig, ax = schematic(6.8, 4.6, xlim=(0, 14.4), ylim=(0, 9.6))
    b1, b3, b2 = (2.6, 7.0), (11.8, 7.0), (7.2, 2.0)
    for (x, y) in (b1, b3, b2):
        ax.plot([x - 1.1, x + 1.1], [y, y], color=INK, lw=3.4, solid_capstyle="butt", zorder=4)
    # generators
    for (x, y), lab in ((b1, "G1"), (b3, "G3")):
        ax.plot([x, x], [y, y + 0.7], color=INK, lw=1.1)
        ax.add_patch(Circle((x, y + 1.15), 0.45, fc="white", ec=INK, lw=1.1, zorder=5))
        ax.text(x, y + 1.15, "~", ha="center", va="center", fontsize=12, zorder=6)
    ax.text(b1[0] - 0.6, b1[1] + 1.15, "Bus 1 (slack)\n$V_1$ = 1.05∠0°", ha="right", va="center", fontsize=8.5)
    ax.text(b1[0] + 0.6, b1[1] + 1.55, f"{S[0].real:.1f} MW\n+ j{S[0].imag:.1f} Mvar", ha="left",
            va="bottom", fontsize=8, color=COLORS[1])
    ax.text(b3[0] + 0.6, b3[1] + 1.15, f"Bus 3 (PV)\n200 MW, $V_3$ = 1.03\nδ$_3$ = +{d[2]:.2f}°",
            ha="left", va="center", fontsize=8.5)
    ax.text(b3[0] - 0.6, b3[1] + 1.55, f"Q$_3$ = {S[2].imag:.1f} Mvar\n(limits −30 … +50)", ha="right",
            va="bottom", fontsize=8, color=COLORS[1])
    # load
    ax.annotate("", xy=(b2[0], b2[1] - 1.1), xytext=(b2[0], b2[1]),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=INK, mutation_scale=13))
    ax.text(b2[0] + 0.25, b2[1] - 0.85, "load 300 MW + j140 Mvar", ha="left", va="center", fontsize=8.5)
    ax.text(b2[0] - 1.3, b2[1] + 0.05, f"Bus 2 (PQ)\n$V_2$ = {V[1]:.3f}∠{d[1]:.2f}°", ha="right",
            va="center", fontsize=8.5)
    # lines
    p12a, p12b = (b1[0] + 0.3, b1[1]), (b2[0] - 0.6, b2[1])
    p13a, p13b = (b1[0] + 0.9, b1[1]), (b3[0] - 0.9, b3[1])
    p32a, p32b = (b3[0] - 0.3, b3[1]), (b2[0] + 0.6, b2[1])
    for a, b in ((p12a, p12b), (p13a, p13b), (p32a, p32b)):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.2, zorder=2)

    def flow_arrow(a, b, f0=0.22, f1=0.42, off=0.0):
        a, b = np.array(a), np.array(b)
        u = (b - a) / np.linalg.norm(b - a)
        nrm = np.array([-u[1], u[0]]) * off
        ax.annotate("", xy=a + (b - a) * f1 + nrm, xytext=a + (b - a) * f0 + nrm,
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color=COLORS[0], mutation_scale=12), zorder=6)

    flow_arrow(p12a, p12b, off=0.35)
    flow_arrow(p13b, p13a, f0=0.72, f1=0.9, off=-0.3)
    flow_arrow(p32a, p32b, off=-0.35)
    fs = dict(fontsize=7.8, color=COLORS[0])
    s12, r12 = F[(0, 1)], -F[(1, 0)]
    s31, r31 = F[(2, 0)], -F[(0, 2)]
    s32, r32 = F[(2, 1)], -F[(1, 2)]
    ax.text(4.1, 4.75, f"1→2 send {s12.real:.1f} + j{s12.imag:.1f}\n     recv {r12.real:.1f} + j{r12.imag:.1f}",
            ha="right", va="center", **fs)
    ax.text(7.6, 7.2, f"3→1 send {s31.real:.1f} MW", ha="center", va="bottom", **fs)
    ax.text(10.3, 4.75, f"3→2 send {s32.real:.1f} + j{s32.imag:.1f}\n     recv {r32.real:.1f} MW",
            ha="left", va="center", **fs)
    # line data
    ld = dict(fontsize=7.5, color="#555555")
    ax.text(5.2, 4.2, "0.02 + j0.10\nB = 0.04", ha="left", va="center", **ld)
    ax.text(7.2, 6.75, "0.015 + j0.08, B = 0.03", ha="center", va="top", **ld)
    ax.text(9.2, 4.2, "0.02 + j0.10\nB = 0.04", ha="right", va="center", **ld)
    loss = S.real.sum()
    ax.text(0.2, 0.35, f"230 kV, 100 MVA base; flows in MW + j Mvar.  Total losses {loss:.1f} MW",
            fontsize=8, color=INK)
    save(fig, CH, "fig-18-1-three-bus-system")


# -------------------------------------------------------- 18.2 nose curves
def _nose(pf, lead, X=0.2, E=1.0, n=600):
    phi = np.arccos(pf)
    t = -np.tan(phi) if lead else np.tan(phi)
    s = np.sin(phi) * (-1 if lead else 1)
    pmax = E ** 2 * pf / (2 * X * (1 + s))
    P = np.linspace(0, pmax, n)
    Q = P * t
    b = E ** 2 - 2 * Q * X
    disc = np.clip(b ** 2 - 4 * X ** 2 * (P ** 2 + Q ** 2), 0, None)
    Vu = np.sqrt((b + np.sqrt(disc)) / 2)
    Vl = np.sqrt((b - np.sqrt(disc)) / 2)
    return P, Vu, Vl, pmax, E / np.sqrt(2 * (1 + s))


def fig_18_2():
    fig, ax = new_fig(6.6, 4.3)
    cases = [(0.9, False, "0.9 lagging", COLORS[1]), (1.0, False, "unity", COLORS[0]),
             (0.95, True, "0.95 leading", COLORS[2])]
    for pf, lead, lab, c in cases:
        P, Vu, Vl, pm, vn = _nose(pf, lead)
        ax.plot(P, Vu, color=c, label=f"{lab} (nose {pm:.2f} pu, {vn:.3f} pu)")
        ax.plot(P, Vl, color=c, ls=":", lw=1.4)
        ax.plot([pm], [vn], "o", color=c, ms=5, zorder=5)
    ax.axhline(0.95, color=INK, ls="--", lw=0.9)
    ax.text(2.2, 0.958, "0.95 pu limit", fontsize=8, va="bottom")
    # leading-case margin annotation
    P, Vu, Vl, pm, vn = _nose(0.95, True)
    p95 = np.interp(-0.95, -Vu, P)
    ax.annotate("", xy=(pm, 0.925), xytext=(p95, 0.925),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=COLORS[2], mutation_scale=7))
    ax.plot([pm, pm], [vn, 0.95], color=COLORS[2], lw=0.6, ls=":")
    ax.text(3.22, 0.905, f"leading pf: V still\nreads 0.95 pu only\n{pm - p95:.2f} pu ({(pm - p95) * 100:.0f} MW)\nfrom the nose",
            ha="right", va="top", fontsize=7.5, color=COLORS[2])
    ax.set_xlim(0, 3.6)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("Load active power $P$ (pu on 100 MVA)")
    ax.set_ylabel("Load voltage $V$ (pu)")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.615), fontsize=7.5,
              title="load pf (solid: upper, stable branch;\ndotted: lower branch)", title_fontsize=7.5)
    ax.text(0.03, 1.07, "$E$ = 1.0 pu, $X$ = 0.2 pu", fontsize=8, va="top")
    # inset: three-bus example, V2 against load scaling factor
    ins = ax.inset_axes([0.66, 0.13, 0.32, 0.30])
    Y = ybus()
    lam = np.linspace(1.0, 2.0, 41)
    v2 = np.array([newton(Y, lam=l)[0][1] for l in lam])
    marks = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    vm = np.array([newton(Y, lam=l)[0][1] for l in marks])
    ins.plot(lam, v2, color=COLORS[3], lw=1.4)
    ins.plot(marks, vm, "o", color=COLORS[3], ms=3)
    for l, v in zip(marks, vm):
        ins.text(l + (0.04 if l < 2 else -0.04), v + 0.012, f"{v:.3f}", fontsize=6,
                 ha="left" if l < 2 else "right", va="bottom")
    ins.set_xlim(0.95, 2.08)
    ins.set_ylim(0.55, 0.98)
    ins.set_xlabel("load scaling λ (three-bus example)", fontsize=7, labelpad=1)
    ins.set_ylabel("$V_2$ (pu)", fontsize=7, labelpad=1)
    ins.tick_params(labelsize=6.5, pad=1)
    ins.set_facecolor("white")
    save(fig, CH, "fig-18-2-nose-curves")


# ---------------------------------------------------- 18.3 convergence
def fig_18_3():
    fig, ax = new_fig(6.4, 3.9)
    gs = [0.602, 0.0430, 0.00822, 0.00217, 0.000561, 0.000159, 0.0000438]
    nr = [2.85, 0.213, 0.00492, 3.1e-6, 1.2e-12]
    fd = [0.0993, 0.00865, 0.000697, 0.0000537]
    ax.semilogy(range(1, 8), gs, "o-", color=COLORS[1], label="Gauss–Seidel (linear, ×~4 per iteration)")
    ax.semilogy(range(0, 5), nr, "s-", color=COLORS[0], label="Newton–Raphson (quadratic)")
    ax.semilogy(range(1, 5), fd, "^-", color=COLORS[2], label="fast-decoupled (linear, ×~12 per iteration)")
    ax.axhline(1e-4, color=INK, ls="--", lw=0.9)
    ax.text(7.95, 1.4e-4, "tolerance 10$^{-4}$ pu", ha="right", va="bottom", fontsize=8)
    ax.set_xlim(0, 8)
    ax.set_ylim(1e-13, 10)
    ax.set_xlabel("Iteration number")
    ax.set_ylabel("Largest power mismatch (pu)")
    ax.grid(True, which="major", color=GRID, lw=0.5)
    ax.legend(loc="lower left", fontsize=8)
    save(fig, CH, "fig-18-3-convergence-comparison")


# ------------------------------------------------------ 18.4 NR flowchart
def fig_18_4():
    fig, ax = schematic(6.8, 5.6, xlim=(0, 15.2), ylim=(0.4, 12.4))
    fcb, fcd = "#EEF3F8", "#FFF4D6"
    W, H, DH = 6.2, 0.8, 1.6

    def rbox(cx, cy, t, w=W, h=H, fc=fcb):
        box(ax, cx - w / 2, cy - h / 2, w, h, t, fc=fc, fontsize=7.6)

    def diamond(cx, cy, t, w=W, h=DH):
        ax.add_patch(Polygon([[cx, cy + h / 2], [cx + w / 2, cy], [cx, cy - h / 2], [cx - w / 2, cy]],
                             fc=fcd, ec=INK, lw=1.0))
        ax.text(cx, cy, t, ha="center", va="center", fontsize=7.6)

    def path(xs, ys, head=True):
        if len(xs) > 2:
            ax.plot(xs[:-1], ys[:-1], color=INK, lw=1.0)
        ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-2], ys[-2]),
                    arrowprops=dict(arrowstyle="-|>" if head else "-", lw=1.0, color=INK,
                                    mutation_scale=9, shrinkA=0, shrinkB=0))

    def tag(x, y, t, ha="left"):
        ax.text(x, y, t, fontsize=7.5, fontweight="bold", ha=ha, va="center")

    xl, xr = 3.65, 11.3
    # inner Newton loop
    rbox(xl, 11.8, "Read data, build $\\mathbf{Y}_{bus}$ (Chapter 17)")
    rbox(xl, 10.7, "Initialise $V$, δ (flat start or previous case)")
    rbox(xl, 9.6, "Compute $P$, $Q$; form mismatches")
    diamond(xl, 7.9, "max |mismatch| < 10$^{-4}$ pu ?")
    rbox(xl, 6.2, "Form Jacobian; sparse LU factorise")
    rbox(xl, 5.1, "Solve for corrections; update $V$, δ")
    diamond(xl, 3.4, "iteration count < 20 ?")
    rbox(xl, 1.3, "Report divergence", w=3.6, fc="#F8DCDC")
    path([xl, xl], [11.4, 11.1])
    path([xl, xl], [10.3, 10.0])
    path([xl, xl], [9.2, 8.7])
    path([xl, xl], [7.1, 6.6])
    tag(xl + 0.15, 6.85, "No")
    path([xl, xl], [5.8, 5.5])
    path([xl, xl], [4.7, 4.2])
    path([xl, xl], [2.6, 1.7])
    tag(xl + 0.15, 2.15, "No")
    path([xl - W / 2, 0.25, 0.25, xl - W / 2], [3.4, 3.4, 9.6, 9.6])
    tag(0.35, 3.65, "Yes")
    # outer loop: reactive limits, then taps and shunts
    diamond(xr, 7.9, "any PV bus outside\n$Q_{min}$ … $Q_{max}$ ?")
    rbox(xr, 9.6, "Convert to PQ at the limit")
    diamond(xr, 5.6, "tap changer or switched\nshunt outside its band ?")
    rbox(xr, 3.6, "Adjust tap or shunt step")
    rbox(xr + 0.2, 1.4, "Compute slack power, line flows, losses;\ncheck thermal and voltage limits; report",
         w=6.6, h=1.2)
    path([xl + W / 2, xr - W / 2], [7.9, 7.9])
    tag(xl + W / 2 + 0.15, 8.15, "Yes")
    ax.text((xl + xr) / 2, 7.6, "outer loop", fontsize=7.5, style="italic", color="#555555", ha="center", va="top")
    path([xr, xr], [8.7, 10.0 - H])
    tag(xr + 0.15, 8.95, "Yes")
    path([xr, xr], [7.1, 6.4])
    tag(xr + 0.15, 6.75, "No")
    path([xr, xr], [4.8, 4.0])
    tag(xr + 0.15, 4.4, "Yes")
    # re-solve paths back to the mismatch calculation
    path([xr - W / 2, xl + W / 2], [9.6, 9.6])
    ax.plot([xr + W / 2, 14.9, 14.9, 7.1, 7.1], [3.6, 3.6, 11.1, 11.1, 9.6], color=INK, lw=1.0)
    ax.text(7.25, 9.75, "re-solve", fontsize=7.5, style="italic", color="#555555", va="bottom")
    ax.text(14.8, 7.3, "re-solve", fontsize=7.5, style="italic", color="#555555", rotation=90, ha="right",
            va="center")
    # no tap or shunt action -> final report
    path([xr - W / 2, 7.3, 7.3, xr + 0.2 - 3.3], [5.6, 5.6, 1.4, 1.4])
    tag(7.45, 5.85, "No")
    save(fig, CH, "fig-18-4-nr-flowchart")


# --------------------------------------------------- 18.5 voltage profiles
def fig_18_5():
    cases = []
    V, d, S = newton(ybus())
    cases.append(("base case", V, S.real.sum()))
    V, d, S = newton(ybus(), q3_fixed=0.50)
    cases.append(("gen. 3 at Q limit (50 Mvar)", V, S.real.sum()))
    V, d, S = newton(ybus(0.5))
    cases.append(("50 Mvar capacitor at bus 2", V, S.real.sum()))
    V, d, S = newton(ybus(0.8))
    cases.append(("80 Mvar capacitor at bus 2", V, S.real.sum()))
    fig, ax = new_fig(6.6, 4.0)
    w = 0.19
    cols = [COLORS[7], COLORS[1], COLORS[5], COLORS[2]]
    for k, (lab, V, loss) in enumerate(cases):
        x = np.arange(3) + (k - 1.5) * w
        ax.bar(x, V - 0.90, w * 0.92, bottom=0.90, color=cols[k], alpha=0.85 if k else 0.6,
               label=f"{lab}: losses {loss:.1f} MW")
        ax.text(x[1], V[1] + 0.002, f"{V[1]:.3f}", ha="center", va="bottom", fontsize=7, rotation=90)
    for yl in (0.95, 1.05):
        ax.axhline(yl, color=INK, ls="--", lw=0.9)
    ax.text(3.15, 1.048, "planning\nlimit 1.05", ha="right", va="top", fontsize=8)
    ax.text(3.15, 0.952, "planning\nlimit 0.95", ha="right", va="bottom", fontsize=8)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["bus 1 (slack)", "bus 2 (load)", "bus 3 (PV)"])
    ax.set_xlim(-0.5, 3.15)
    ax.set_ylim(0.90, 1.12)
    ax.set_yticks(np.arange(0.90, 1.071, 0.02))
    ax.set_ylabel("Bus voltage (pu)")
    ax.legend(loc="upper center", fontsize=7.5, ncol=2, columnspacing=1.0, handlelength=1.2)
    ax.spines["left"].set_bounds(0.90, 1.07)
    save(fig, CH, "fig-18-5-voltage-profiles")


# --------------------------------------------------- 18.6 capability curve
def fig_18_6():
    S, pf = 600.0, 0.85
    Pr, Qr = S * pf, S * np.sqrt(1 - pf ** 2)
    xd = 1.8                      # synchronous reactance, pu on 600 MVA (assumed)
    qc = -S / xd                  # centre of field-current circle (V = 1 pu)
    rf = np.hypot(Pr, Qr - qc)    # radius through the rated point
    fig, ax = new_fig(6.6, 4.3)
    th = np.linspace(0, np.pi, 400)
    ax.plot(S * np.cos(th), S * np.sin(th), color=COLORS[0], ls="--", lw=1.2)
    ax.text(-390, 608, "armature current limit (600 MVA)", color=COLORS[0], fontsize=8, ha="left")
    # field current limit arc
    qf = np.linspace(Qr - 60, qc + rf, 300)
    pf_arc = np.sqrt(np.clip(rf ** 2 - (qf - qc) ** 2, 0, None))
    ax.plot(qf, pf_arc, color=COLORS[1], lw=1.6)
    ax.text(440, 190, "field current\nlimit", color=COLORS[1], fontsize=8, ha="right")
    # prime-mover limit
    ax.plot([-400, 500], [Pr, Pr], color=COLORS[2], lw=1.2, ls="-.")
    ax.text(-390, Pr + 8, f"prime-mover limit {Pr:.0f} MW", color=COLORS[2], fontsize=8, va="bottom")
    # under-excitation limit
    ax.plot([-200, -150], [0, Pr], color=COLORS[3], lw=1.6)
    ax.text(-215, 180, "under-excitation\nlimit", color=COLORS[3], fontsize=8, ha="right")
    # permissible region
    qa = np.linspace(Qr, qc + rf, 200)
    pa = np.sqrt(rf ** 2 - (qa - qc) ** 2)
    region = [(-200, 0), (-150, Pr), (Qr, Pr)] + list(zip(qa, pa)) + [(qc + rf, 0)]
    ax.add_patch(Polygon(region, fc=COLORS[5], alpha=0.18, ec="none"))
    ax.text(150, 220, "permissible\noperating region", ha="center", fontsize=9, color="#1f5f8b")
    ax.plot([Qr], [Pr], "o", color=INK, ms=6, zorder=5)
    ax.annotate(f"rated point\n{Pr:.0f} MW, {Qr:.0f} Mvar\n(0.85 pf lagging)", xy=(Qr, Pr), xytext=(330, 590),
                fontsize=8, ha="left", va="center", arrowprops=dict(arrowstyle="-", lw=0.7))
    ax.axvline(0, color="#999999", lw=0.7)
    ax.text(-390, 15, "← leading (under-excited)", fontsize=8, color="#555555")
    ax.text(490, 15, "lagging (over-excited) →", fontsize=8, color="#555555", ha="right")
    ax.set_xlim(-400, 500)
    ax.set_ylim(0, 650)
    ax.set_xlabel("Reactive power $Q$ (Mvar)")
    ax.set_ylabel("Active power $P$ (MW)")
    ax.grid(True, color=GRID, lw=0.5)
    save(fig, CH, "fig-18-6-generator-capability")


if __name__ == "__main__":
    fig_18_1()
    fig_18_2()
    fig_18_3()
    fig_18_4()
    fig_18_5()
    fig_18_6()
