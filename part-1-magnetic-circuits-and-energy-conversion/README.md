# Part I — Magnetic Circuits and Energy Conversion

Almost every kilowatt-hour generated, transmitted or used in industry passes through a magnetic field at least twice: once in a generator, once or more in a transformer, and usually again in a motor. Part I builds the engineering tools for that field. It starts where *Engineering Physics: Top Down* stops, with quasi-static, lumped Maxwell equations and the motor as an ideal gyrator, and carries that physics into hardware: iron cores with air gaps that fringe and leak, steels that saturate and dissipate energy, windings whose flux linkage depends on current and on the position of a rotor, forces and torques computed from stored energy, a rotating field produced by stationary windings, and losses that set efficiency, temperature and rating. The examples, from data-centre filter reactors and refinery pump motors to lifting magnets and electric-vehicle traction motors, show the same principles at work across the energy field.

## By the end of this part you should understand

- how to model an iron core with air gaps as a magnetic circuit of reluctances, compute its flux, inductance and ampere-turn requirement, and correct the result for fringing, leakage and the slotted gaps of machines;
- how saturation changes inductance, how to solve a nonlinear magnetic circuit from a $B$–$H$ curve, and where saturation sets limits on transformers, current transformers, machines and drives;
- how Faraday's law, written for a flux linkage that depends on current and position, separates transformer EMF from speed EMF, and why the applied voltage, not the current, sets the flux of a winding;
- how Lenz's law explains shading rings, eddy-current brakes, laminations and the trapped flux of disconnected motors;
- how self- and mutual inductances of real windings depend on saturation and position;
- how the energy balance of a lossless coupling field gives torque, and how co-energy gives force in saturating devices;
- how three-phase windings create a rotating magnetic field, and what sets synchronous speed, magnetising current, reversal and the effects of unbalance;
- where losses arise, how they set efficiency, and how insulation temperature limits turn losses into ratings.

## Chapters

| Chapter | Central question | What it delivers |
|---|---|---|
| [Chapter 1 — Magnetic Circuit Fundamentals](01-magnetic-circuit-fundamentals.md) | How do you predict the flux, inductance and ampere-turn requirement of an iron core with air gaps, and where does the linear model fail? | Flux, field intensity, flux density and permeability as engineering data; MMF and reluctance; series and parallel paths in E–I and three-limb cores; air gaps and inductor design; fringing corrections and Carter's coefficient; saturation, the $B$–$H$ curve, hysteresis and the permanent-magnet load line |
| [Chapter 2 — Electromagnetic Induction](02-electromagnetic-induction.md) | How does a changing flux linkage, from changing current or from motion, produce voltage, and how does the energy balance produce torque? | Faraday's law for $\lambda(i,\theta)$; transformer and speed EMF; Lenz's law in contactors, brakes and machines; motional EMF and its limits; volt-second control of flux; secant, incremental, magnetising, leakage and position-dependent inductances; mutual coupling in machines and with pipelines; the lossless coupling field; reluctance and alignment torque; the full electromechanical energy balance |
| [Chapter 3 — Energy Conversion Principles](03-energy-conversion-principles.md) | How do electromagnetic devices convert energy in both directions, and how do losses set efficiency, temperature and rating? | Air-gap shear stress and machine sizing; generator action and regenerative braking; co-energy and force in saturating actuators; magnetic pressure; energy-conversion loops; the rotating magnetic field and magnetising current; loss mechanisms and lamination choice; efficiency and IE classes; insulation classes, thermal time constants and short-time ratings |

## How this part connects to the rest of the book

Part I is the foundation for everything that converts energy through a magnetic field. In Part II the transformer of Chapter 4 is the magnetic circuit of Chapter 1 with the coupled windings of Chapter 2 and the losses of Chapter 3; the DC, induction, synchronous and special machines of Chapters 5–8 are the coupling field, rotating field and torque mechanisms of Chapters 2 and 3 in particular geometries; and Chapter 9 turns the loss and thermal principles into design and rating. The drives of Part III control flux and torque through the volt-second and co-energy relations developed here, and Parts IV–VII rely throughout on the saturation, inductance and loss behaviour introduced in this part.

Part I deliberately does not repeat its foundations. The physics (Maxwell's equations, constitutive relations, magnetostatics, the quasi-static limit, the effort–flow template, Poynting's theorem, thermodynamics and heat transfer) is taken from [*Engineering Physics: Top Down*](https://github.com/The-Studio-of-Sadiq/Engineering-Physics), chiefly Chapters 11, 14, 17 and 19. The circuit theory of inductance, coupled coils, AC power and three-phase circuits is taken from [*Circuits, Signals and Communications*](https://github.com/The-Studio-of-Sadiq/Circuits-Signals-and-Communications), chiefly Chapters 5 and 10. The microstructural origins of permeability, core loss and insulation ageing belong to *The Materials Core*.
