# Changelog

All notable changes to *Electrical Energy and Machines*. Dates are ISO 8601. Versions follow the tags in this repository; each release attaches the compiled PDF.

## [1.0.0] — 2026-10-24

First complete edition.

### Added
- **Part I — Magnetic Circuits and Energy Conversion** (Chapters 1–3): magnetic circuits, electromagnetic induction, energy conversion. Each chapter opens where *Engineering Physics* leaves off and links the exact sections it builds on.
- **Part II — Transformers and Electrical Machines** (4–9): transformers, DC, induction, synchronous and special machines, machine design and performance.
- **Part III — Motor Drives** (10–12): drive-system fundamentals, DC drives, AC drives.
- **Part IV — Power Generation** (13–16): power-system structure, conventional and renewable generation, energy storage.
- **Part V — Power-System Analysis** (17–20): per-unit modelling, power flow, faults, stability.
- **Part VI — Transmission, Distribution, and Protection** (21–24): transmission lines, distribution, protection, high-voltage engineering.
- **Part VII — Power Quality and Grid Modernization** (25–28): power quality, smart grids, grid integration of renewables, energy efficiency and management.
- **Part VIII — Electrical Safety and Engineering Practice** (29–30): electrical safety, electrical system design.
- Eight part openers, one per part folder.
- 174 figures, each drawn by a reproducible script in `figures/scripts/chNN.py` from the chapter's own numbers; figure plan in `FIGURES.md`.
- `pdf/Electrical-Energy-and-Machines.pdf` (600 pages) with clickable contents, PDF bookmarks and KaTeX math, built by `scripts/build-pdf.mjs`.
- MCP server (`mcp/server.mjs`) to list, read, search and typeset the book and fetch its figures.
- Book checks (`scripts/check-book.mjs`, now also rejecting tab characters left by an unescaped `\t` in LaTeX), CI and release workflows, issue and pull-request templates, community files, citation file, social preview image and wiki generator.

### Fixed (before release, from figure-agent cross-checks)
- Ch. 1–3: inductance/current trade-off on one basis; open-armature flux linkage 0.97 Wb-turn; switched-reluctance energy loop.
- Ch. 4–6: transformer annual-loss figures and phasor wording; DC-machine speed and stray-load statements; induction-motor power flow made consistent with an equivalent circuit without core-loss branch.
- Ch. 7–9: synchronous-machine power-angle values; PM-motor field-weakening envelope; BLDC line-to-line EMF; stepper resonance band; hoist average power 373 kW; thermal-network and slot-insulation figures.
- Ch. 10–12: braking-resistor threshold, hoist quadrants, DC-drive commutation limit (Figure 11.1 redrawn), rotor-loss figure.
- Ch. 13–16: cable reactive power generated, not absorbed; combined-cycle heat rate; hydro-turbine head ranges; hydrogen density; hydrogen-cavern energy ratios; pumped-hydro gross head.
- Ch. 17–21: transformer ohmic impedance; swing-curve angles; line-model error table relative to the exact model (Figure 21.2 redrawn); SIL 516 MW; lossless power-angle values marked as such.
- Ch. 22–30: distribution, protection, high-voltage, demand-response, ride-through, peak-shaving and design worked examples made internally consistent.
