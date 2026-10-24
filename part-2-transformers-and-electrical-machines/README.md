# Part II — Transformers and Electrical Machines

Part I established the physics of conversion in its engineering form: magnetic circuits with air gaps and saturation, induced EMF and inductance in real windings, force and torque from co-energy, the rotating magnetic field, and the losses and heat that set every rating. Part II applies that physics to the devices that carry almost all electrical energy from generation to use. Every kilowatt-hour from a power station passes through a synchronous generator and four or five transformers before it reaches a load, and most of it ends up in a motor. This part builds the model engineers use for each machine: an equivalent circuit whose parameters come from standard tests, a set of characteristics that show how the machine behaves under load, and the numbers (impedances, slips, efficiencies, temperature rises) that decide how it is specified, connected, started, controlled and protected. Each device is described by a model with stated assumptions, solved for its running performance, and followed to where the model fails: inrush, commutation, deep-bar effects, stability limits, demagnetisation, and heat in all of them.

## By the end of this part you should understand

- How a real transformer departs from the ideal one, how its equivalent circuit, losses and regulation are measured, and how units are paralleled, connected in three-phase groups, or built as autotransformers and instrument transformers.
- How the commutator makes a DC machine's EMF and torque follow $E=k\Phi\omega$ and $T=k\Phi I_a$, and how the field connection shapes its characteristics, starting, speed control and braking.
- How slip governs the induction motor: its per-phase equivalent circuit, power flow, torque–speed curve, starting methods, speed control, efficiency classes and selection for a load.
- How a synchronous machine generates, how its power-angle relationship and excitation set active and reactive power, and how it is synchronised and kept stable on a grid.
- How permanent-magnet, brushless DC, switched-reluctance, stepper, universal, linear and servo motors work, and when each is the right choice.
- How temperature, insulation, duty and cooling set a machine's rating, and how machines are tested and maintained.

## Chapters

| Chapter | Central question | What it delivers |
|---|---|---|
| [Chapter 4 — Transformers](04-transformers.md) | How does a real transformer differ from the ideal one, and how are its losses, impedance and connections chosen and checked? | The equivalent circuit from open- and short-circuit tests; efficiency, all-day efficiency and regulation; polarity, parallel operation, vector groups, autotransformers and instrument transformers |
| [Chapter 5 — DC Machines](05-dc-machines.md) | How does a commutated machine convert energy, and how do its field connections fix its behaviour? | EMF and torque equations with winding constants; separately excited, shunt, series and compound characteristics; speed control, starter design, braking, losses and efficiency |
| [Chapter 6 — Induction Machines](06-induction-machines.md) | How does a short-circuited rotor produce torque, and how is the motor started, controlled and selected? | Slip, the per-phase equivalent circuit and power flow; torque–speed curve and design classes; starting methods and voltage dip; speed control; IE efficiency classes; single-phase motors; selection |
| [Chapter 7 — Synchronous Machines](07-synchronous-machines.md) | How does a generator turning at exactly synchronous speed deliver active and reactive power to a grid? | Phasor diagrams and regulation; the power-angle equation; synchronisation and parallel operation; synchronous motors; excitation and reactive power; stability fundamentals |
| [Chapter 8 — Special Electrical Machines](08-special-electrical-machines.md) | Which machines replace the classical three when efficiency, power density or precise motion matter? | Principles and characteristics of PMSM, BLDC, switched-reluctance, stepper, universal, linear and servo motors and specialised generators; selection trade-offs |
| [Chapter 9 — Electrical Machine Design and Performance](09-electrical-machine-design-and-performance.md) | What limits a machine's rating, and how are performance and reliability verified? | Duty cycles, loss calculation, thermal limits, insulation systems, cooling, winding and material choices, performance testing, reliability and maintenance |

## How this part connects to the rest of the book

Part II rests on Part I and on two sibling books. The electromagnetic laws, the quasi-static limit and the transformer and gyrator elements of the bond graph come from [*Engineering Physics: Top Down*](https://github.com/The-Studio-of-Sadiq/Engineering-Physics) (Ch. 11 and Ch. 17). Coupled coils, the ideal transformer, phasors, AC power and three-phase circuits come from [*Circuits, Signals and Communications*](https://github.com/The-Studio-of-Sadiq/Circuits-Signals-and-Communications) (Chapters 5, 8, 9 and 10).

The machine models built here are the plants of Part III, where DC drives (Chapter 11) and AC drives (Chapter 12) control them with power electronics. The synchronous generator and the transformer are the building blocks of generation in Part IV, of the per-unit network models, load flow, fault and stability studies of Part V, and of the distribution and protection systems of Part VI, where instrument transformers and transformer differential protection reappear. Motor efficiency returns in Chapter 28 and equipment selection in Chapter 30.
