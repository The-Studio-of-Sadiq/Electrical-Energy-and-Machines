# Part III — Motor Drives

Part II treated electrical machines as they would behave on a fixed supply: a transformer on a constant-voltage bus, an induction motor started direct-on-line, a synchronous machine locked to the grid frequency. Almost no modern motor of any importance runs that way. Pumps and fans, conveyors and mills, hoists and lifts, machine tools and robots, ship propellers, trains and electric cars all run their motors through power converters that set voltage, current and frequency continuously, under a controller that closes loops on current, speed or position. Motor-driven systems use roughly 45 % of the world's electricity, and the drive decides most of their energy use, dynamics and failure modes. This part treats the motor, its converter, its controller and its mechanical load as one system: how to match them, how to control them, and what each type of drive can and cannot do.

## By the end of this part you should understand

- How a load's torque–speed characteristic, inertia and duty cycle set the torque, speed and quadrants a drive must provide.
- Why motors and converters are sized from peak and RMS torque rather than running power, and how starting and braking energy is accounted for.
- How regeneration, brake resistors and active front ends deal with energy returned by overhauling loads, and what limits regenerative braking in traction.
- How the efficiency of the whole chain is evaluated, and why speed control of pumps and fans saves far more energy than any electrical improvement.
- How drives protect motors, converters and people, including thermal overload classes, safe torque off and the insulation and bearing stresses that PWM converters introduce.
- How a DC motor is controlled by armature voltage below base speed and by field weakening above it, using thyristor and chopper converters, cascaded current and speed loops and regenerative braking.
- How PWM inverters synthesise variable-frequency voltages and what limits their output.
- How V/f, field-oriented and direct torque control of induction motors and MTPA and flux-weakening control of PMSMs work, and how a drive is commissioned in the field.

## Chapters

| Chapter | Central question | What it delivers |
|---|---|---|
| [Chapter 10 — Drive-System Fundamentals](10-drive-system-fundamentals.md) | How do we match a motor and converter to the torque, speed and energy flows its load really demands? | Shaft equation and referred quantities, operating-point stability, duty and RMS-torque sizing, load families, four-quadrant operation, starting and braking, chain efficiency and IEC 61800-9-2 classes, drive protection and safety functions, a selection procedure |
| [Chapter 11 — DC Motor Drives](11-dc-motor-drives.md) | How are the speed and torque of a DC motor controlled, and what does a practical DC drive look like? | Armature and field control, thyristor-bridge and chopper supplies, power factor at low speed, speed regulation, cascaded current and speed control with tuning rules, regenerative braking and its limits, industrial architecture and DC-specific protection |
| [Chapter 12 — AC Motor Drives](12-ac-motor-drives.md) | How does a variable-frequency drive make induction and permanent-magnet motors controllable, and how is it commissioned? | VFD structure, PWM and SVPWM voltage limits, V/f control with boost, induction-motor speed-control methods compared, space vectors and the d–q frame, field-oriented and direct torque control, PMSM MTPA and flux weakening, a commissioning procedure |

## How this part connects to the rest of the book

Part III stands on Part II. The DC machine equations of [Chapter 5](../part-2-transformers-and-electrical-machines/05-dc-machines.md), the induction-motor equivalent circuit and torque–speed curve of [Chapter 6](../part-2-transformers-and-electrical-machines/06-induction-machines.md), the synchronous and permanent-magnet machines of Chapters 7 and 8, and the ratings, losses and thermal limits of Chapter 9 are used here as known models; the rotating field and the co-energy torque expression of Part I underlie the d–q equations of vector control. Looking forward, the drive's input side reappears in the power-quality chapter (Chapter 25), where rectifier harmonics and the reactive demand of thyristor drives are measured and mitigated; the inverter control of Chapter 12, in its grid-connected form, is the basis of the renewable-energy interfaces of Chapters 15 and 27; regenerative braking connects to energy storage in Chapter 16; drive energy savings feed the efficiency audits of Chapter 28; and drive isolation and safe torque off return in the electrical safety of Chapter 29.

Two sibling books carry the theory this part uses. Rotational mechanics, gear trains as mechanical transformers and pump affinity laws are taken from *[Engineering Physics: Top Down](https://github.com/The-Studio-of-Sadiq/Engineering-Physics)*, Ch. 19, and the averaged converter relations from its Ch. 18. Three-phase circuits, the DC-motor transfer function, feedback, PI tuning and digital control are taken from *[Circuits, Signals and Communications](https://github.com/The-Studio-of-Sadiq/Circuits-Signals-and-Communications)*, Ch. 10 and Chs. 33–35. The circuit-level design of rectifiers, choppers and inverters, power semiconductors, gate drivers and the microcontrollers that run drive firmware belongs to *Electronics & Computing*, and robot and automation controllers to the robotics and automation books.
