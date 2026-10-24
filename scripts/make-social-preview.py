"""Render the GitHub social preview (1280x640) to docs/social-preview.png.

    python scripts/make-social-preview.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "social-preview.png"

BG = "#0b2230"
INK = "#f2f5f9"
MUTED = "#9fb8c8"
ACCENT = ["#56B4E9", "#E69F00", "#009E73", "#CC79A7", "#F0E442"]

plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "cm"})
fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor=BG)

# Upper right: induction-motor torque-speed curves for three rotor resistances (Chapter 6).
ax = fig.add_axes([0.62, 0.55, 0.35, 0.36], facecolor=BG)
s = np.linspace(1e-3, 1, 600)
R1, X, V = 0.02, 0.12, 1.0
for R2, c in zip((0.03, 0.08, 0.2), ACCENT):
    T = 3 * V**2 * R2 / s / ((R1 + R2 / s) ** 2 + X**2)
    ax.plot(1 - s, T / 10, color=c, lw=2.4)
ax.plot([0, 1], [0.35, 0.55], color=MUTED, lw=1.2, ls="--", alpha=0.8)
ax.text(1.02, 0.55, "load", color=MUTED, fontsize=12, va="center")
ax.set_xlim(0, 1.15)
ax.set_ylim(0, 1.25)
ax.axis("off")

# Lower right: synchronous-machine power-angle curves, round rotor and salient pole (Chapter 7).
ax2 = fig.add_axes([0.64, 0.08, 0.31, 0.38], facecolor=BG)
d = np.linspace(0, np.pi, 400)
ax2.plot(d, np.sin(d), color=ACCENT[0], lw=2.4)
ax2.plot(d, np.sin(d) + 0.25 * np.sin(2 * d), color=ACCENT[1], lw=2.4)
ax2.fill_between(d[d < 0.6], 0, np.sin(d[d < 0.6]), color=ACCENT[2], alpha=0.35, lw=0)
ax2.axhline(0.55, color=MUTED, lw=0.8, ls=":", alpha=0.8)
ax2.text(np.pi + 0.08, 0.02, r"$\delta$", color=MUTED, fontsize=16)
ax2.text(1.3, 1.2, r"$P=\frac{EV}{X_s}\sin\delta$", color=INK, fontsize=15)
ax2.set_xlim(0, np.pi + 0.3)
ax2.set_ylim(-0.05, 1.45)
ax2.axis("off")

# Left panel: title block.
fig.text(0.06, 0.83, "BOOK 5  ·  EEE CORE", color=ACCENT[0], fontsize=20, weight="bold")
fig.text(0.06, 0.63, "Electrical Energy\nand Machines", color=INK, fontsize=38, weight="bold",
         va="center", linespacing=1.12)
fig.text(0.06, 0.45, "Magnetic circuits, transformers and machines,\ndrives, generation and storage, "
         "power systems,\nprotection, power quality and the modern grid.",
         color=MUTED, fontsize=16, style="italic", va="top", linespacing=1.35)
fig.text(0.06, 0.24, r"$T_e=\frac{\partial W'_{\mathrm{fld}}(i,\theta)}{\partial\theta}$", color=INK, fontsize=19)
fig.text(0.06, 0.14, "8 parts · 30 chapters · 174 figures · 600-page PDF · MCP server", color=INK, fontsize=14)
fig.text(0.06, 0.07, "github.com/The-Studio-of-Sadiq/Electrical-Energy-and-Machines", color=MUTED, fontsize=12)

OUT.parent.mkdir(exist_ok=True)
fig.savefig(OUT, facecolor=BG)
print(f"wrote {OUT.relative_to(ROOT)}")
