# Contributing — Electrical Energy and Machines

Corrections, clearer explanations, better figures and new worked examples are welcome. Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to contribute

- **Found an error?** Open an [Erratum](../../issues/new?template=erratum.yml) issue with the section number (e.g. §6.5), what the book says and what it should say, with a derivation or a numerical check.
- **A figure is wrong or unclear?** Open a [Figure](../../issues/new?template=figure.yml) issue, or fix `figures/scripts/chNN.py` and send a pull request.
- **Build, figure-script or MCP-server problem?** Open a [Tooling bug](../../issues/new?template=tooling-bug.yml).
- **Bigger change** (a new section, a rewrite, a new worked example)? Open a [Proposal](../../issues/new?template=proposal.yml) first so the scope can be agreed.

## Pull requests

1. One topic per pull request: a fix, a figure, a section.
2. Follow the house style below; every number you add must be checked (e.g. with Python).
3. Run the checks locally before pushing (CI runs the same ones):

```bash
npm ci
```

```bash
npm run check
```

```bash
python scripts/build-figures.py ch06
```

4. Changed a figure? Commit the script and the regenerated PNG together. Added a figure marker? Draw it, run `node scripts/insert-figures.mjs` and `npm run figures:plan`.
5. Leave `pdf/` alone; the PDF is rebuilt and attached to each release by the release workflow.

By contributing you agree that your contribution is licensed under the repository's [MIT License](LICENSE).

---

# House Style

The master outline is [`TOC.md`](TOC.md). It is fixed: 8 parts, 30 chapters. Do not skip, merge or rename listed topics; every bullet in the TOC must be covered by a section or subsection of its chapter.

## Files

- Each part is a folder `part-N-<slug>/`. Its `README.md` is the part opener; `NN-<slug>.md` (NN two digits, global chapter number) is a chapter. The exact file names are listed in the TOC.
- Markdown only. Math is GitHub-style LaTeX: `$...$` inline, `$$...$$` display (display math on its own lines). Never `\(...\)` or `\[...\]`.
- In tables, never put a raw `|` inside math; use `\lvert ... \rvert` or `\Vert`.
- Use `\mathrm{}` for units in math, e.g. `$X_s=1.8\ \mathrm{pu}$`, `$B=1.6\ \mathrm{T}$`. Prefer plain text units outside math.
- Use $j=\sqrt{-1}$ (engineering convention). Phasors in bold or with a bar are both acceptable, but be consistent inside a chapter. RMS values unless stated otherwise; three-phase voltages are line-to-line unless stated otherwise.
- **No exercises, problems, quizzes or answer sections.** Worked examples inside the text are welcome.

## Chapter layout

```
# Chapter N — Title

*Part X · Part title*

Opening paragraph that starts from an engineering problem (a transformer that runs hot at light load, a motor that will not start a loaded conveyor, a feeder whose end voltage sags every evening, a blackout that spread from one tripped line).

> **Question 1?**
> **Question 2?**

| Concept | Engineering destination |
|---|---|
| ... | ... |

**Roadmap.** Short arrow-chain through the sections (N.1 → N.2–N.3 → ...).

---

## N.1 Section title
...
---
## N.2 ...
...
## What remains open

| Open question | Where it is answered |
|---|---|

**Next:** one sentence pointing to the next chapter.
```

Use `### ` subsections freely inside sections. Separate `## ` sections with `---`.

## Voice and method

1. **Start from the engineering problem**, not a definition: a utility power-factor penalty, a pump motor that overheats on a weak supply, a generator that loses synchronism after a fault, a breaker that must clear 40 kA, a rooftop-PV feeder whose voltage rises at noon, an arc-flash label on a switchboard. Draw examples from across the energy field: utilities, industrial plants, buildings, traction and electric vehicles, renewable plants, data centres, mining, marine and aircraft systems.
2. **Model → analysis → consequence.** Every method is introduced as a model with stated assumptions, solved with the right mathematics, and taken to a measurable consequence on a real machine, drive or power system (a temperature rise, a fault current, a voltage drop, a kWh bill, a stability margin).
3. **Every concept gets an engineering destination.** The opening table maps concepts to where an engineer uses them.
4. **Status box after every important law, theorem or rule**, using exactly one of four labels:
   - **Fundamental** — follows from physical law (Faraday's law and Ampère's law from Maxwell's equations, energy conservation in the electromechanical energy balance, charge conservation in KCL).
   - **Derived** — a mathematical consequence of more basic results (the transformer EMF equation, force from co-energy, the power-angle equation, symmetrical components, the swing equation, Newton–Raphson load flow).
   - **Approximate** — valid under stated simplifying assumptions (linear magnetics, the approximate transformer equivalent circuit, the constant-flux V/f assumption, the short-line model, the equal-area criterion with classical generator model). State the assumptions and the domain.
   - **Empirical** — fitted to observation (the Steinmetz hysteresis-loss law, Peek's corona formula, insulation life halving per 10 °C, IEC/IEEE curve shapes for inverse-time relays, battery cycle-life curves, arc-flash incident-energy equations).

   Format:
   ```
   > **Status of the principle: Name**
   > *Derived.* One sentence on why and where it holds.
   ```
5. **Show why an approximation works, then where it fails.** Linear magnetics fails at saturation; the per-phase equivalent circuit fails under unbalance; the short-line model fails beyond ~80 km; the classical generator model fails for long transients. A failure is missing physics or a changed regime, never an arbitrary exception.
6. **Real numbers.** Give representative values (with units) in tables: saturation flux densities and core losses of electrical steels, transformer impedances and efficiencies, motor slips and efficiency classes (IE1–IE4), synchronous reactances in per unit, line parameters per km, fault levels, relay settings, plant heat rates, capacity factors, battery energy densities and cycle lives, voltage limits from grid codes, harmonic limits, body-current thresholds. Values must be correct to typical handbook accuracy; say "typical" or give ranges where they vary, and name the standard (IEC, IEEE, NFPA 70E) when a limit comes from one. Recompute every worked example.
7. **Worked examples** as `**Worked example — title.**` paragraphs with full numbers.
8. **Respect the boundaries** (see the table at the end of `TOC.md`). Recap a result from a sibling book in a sentence or short paragraph and use it; never re-derive it. The physics in particular is owned by *Engineering Physics*: this book extends it (see below). Add a short `> **Boundary.**` note where a chapter leans on another book, with a link to the exact chapter (see below).
9. Do not overclaim. State domains of validity.

## Cross-references to the sibling books

When a chapter uses physics or circuit theory owned by another book, cite the exact chapter and section with a link. Link targets:

- *Engineering Physics: Top Down* — `https://github.com/The-Studio-of-Sadiq/Engineering-Physics/blob/main/CHAPTERS/CHAPTER%20N.md`, cited as *Engineering Physics*, Ch. N §N.k.
- *Circuits, Signals and Communications* (Book 3) — `https://github.com/The-Studio-of-Sadiq/Circuits-Signals-and-Communications/blob/main/<part folder>/<NN-slug>.md`, cited as *Circuits, Signals and Communications*, Ch. N.

### Extend *Engineering Physics*, do not repeat it

This book is the continuation of *Engineering Physics: Top Down*, not a second copy of its physics. *Engineering Physics* descends from Maxwell's equations to the quasi-static limit (Ch. 11 §11.12), the lumping criterion (Ch. 16 §16.10) and the effort–flow template with its transformer and gyrator elements (Ch. 17). This book starts at that point and carries the physics into hardware: real cores with air gaps, fringing, saturation and loss; windings and their inductances; force and torque from co-energy in real geometries; rotating fields in slotted machines; ratings set by heat.

- **Do not re-derive** Maxwell's equations, Faraday's or Ampère's law, magnetostatics, constitutive relations, Poynting's theorem, the laws of thermodynamics, Carnot efficiency, rigid-body rotation, heat-conduction or transport laws, band theory, or anything else the table below lists. State the result in one line (at most one displayed equation), cite the exact *Engineering Physics* chapter and section with a link, and move on.
- **Add what *Engineering Physics* does not have**: engineering forms and approximations (magnetic-circuit analogy, reluctance networks, the $B$–$H$ curve as data, fringing corrections, practical inductance and winding formulas, loss separation, thermal ratings), real materials and numbers, design trade-offs, failure modes, and worked examples on real devices.
- **Make the hand-off visible**: Part I chapters open their first section with a short "Where *Engineering Physics* leaves off" paragraph naming the result taken over and the link; later chapters use `> **Boundary.**` notes. Where this book goes beyond the physics book's validity limits (saturation, hysteresis, eddy currents at frequency, non-quasi-static surges), say so explicitly.

The physics chapters of this book — Part I above all, and wherever a chapter rests on electromagnetism, thermodynamics, mechanics or solid-state physics — build on these sections of *Engineering Physics*:

| Topic in this book | Engineering Physics |
|---|---|
| Maxwell's equations; Faraday's law and Ampère's law in integral form | Ch. 11 §11.4 |
| Constitutive relations ($B=\mu H$, permeability, magnetisation) | Ch. 11 §11.9 |
| Magnetostatics (Biot–Savart, Ampère's law for steady currents) | Ch. 11 §11.11 |
| Quasi-static limit: why lumped circuits and magnetic circuits work | Ch. 11 §11.12; Ch. 16 §16.10 |
| Energy and power flow in fields (Poynting's theorem) | Ch. 11 §11.8 |
| Lumping, effort–flow variables, energy accounting | Ch. 17 §17.1–17.3, §17.9 |
| Transformer and gyrator elements (ideal transformer, motor/generator as a gyrator) | Ch. 17 §17.5 |
| Rigid-body rotation, moment of inertia, rotational mechanical systems | Ch. 9 §9.7; Ch. 19 §19.2 |
| Laws of thermodynamics, Carnot efficiency | Ch. 10 §10.5–10.6 |
| Thermodynamic cycles (Rankine, Brayton, combined) | Ch. 19 §19.5 |
| Heat transfer, thermal-resistance networks (machine cooling, thermal limits) | Ch. 14 §14.7; Ch. 19 §19.6 |
| Fluid systems as hydraulic circuits (hydro, pumps, fans) | Ch. 19 §19.7; Ch. 15 |
| Electrical resistivity, Ohm's and Fourier's laws from transport theory | Ch. 13 §13.4–13.5; Ch. 14 §14.1 |
| Band theory, semiconductors (photovoltaic cells), nuclear physics (fission) | Ch. 6; Ch. 14 §14.5 |
| Superconductivity (superconducting cables, fault-current limiters, SMES) | Ch. 7 |
| Electromagnetic waves (lightning and switching surges as travelling waves) | Ch. 12 |
| Phasors, AC power, power electronics in outline | Ch. 18 §18.2, §18.8 |

Circuit topics come from *Circuits, Signals and Communications*: capacitors, inductors and coupled coils (Ch. 5, `part-1-circuit-fundamentals/05-capacitors-and-inductors.md`), sinusoidal steady state (Ch. 8, `part-2-transient-and-ac-analysis/08-sinusoidal-steady-state-analysis.md`), AC power (Ch. 9, `part-2-transient-and-ac-analysis/09-ac-power.md`), three-phase circuits (Ch. 10, `part-2-transient-and-ac-analysis/10-three-phase-circuits.md`), Laplace-domain analysis (Ch. 11, `part-3-advanced-network-theory/11-laplace-domain-circuit-analysis.md`), transmission-line wave theory (Ch. 14, `part-3-advanced-network-theory/14-transmission-lines.md`), and feedback and control (Ch. 33–35, `part-7-control-system-fundamentals/`).

## Figure markers

Planned figures are recorded in the chapter as an HTML comment on its own line, at the exact point the figure should appear (invisible in the PDF until the figure exists):

```
<!-- FIGURE 6.3 | figures/ch06/fig-6-3-torque-speed-curve.png | plot | Caption sentence. | Content: what is drawn, axes, data ranges, labels. -->
```

Fields: number, target path, kind (`plot`, `circuit`, `schematic`, `block-diagram`, `phasor`, `cross-section`, `single-line`, `flowchart`, `table-graphic`), caption, and a brief content spec for whoever draws it. Captions and specs must not contain the `|` character.

Figures are drawn by `figures/scripts/chNN.py` (shared style in `figures/scripts/figstyle.py`; circuit drawings may use `schemdraw`) and saved to the marker's path. `node scripts/insert-figures.mjs` then places each drawn figure directly below its marker; the marker stays as the figure's specification:

```
<!-- FIGURE 6.3 | ... -->

![Figure 6.3 — Caption](../figures/ch06/fig-6-3-torque-speed-curve.png)

*Figure 6.3 — Caption.*
```

The full plan is collected in [`FIGURES.md`](FIGURES.md) (`node scripts/figure-plan.mjs`).
