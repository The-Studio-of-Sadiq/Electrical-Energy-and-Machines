# Electrical Energy and Machines — Master Syllabus

**Book 5 — Electrical Energy & Machines Core**

**Objective:** Explain electrical energy conversion, electromechanical systems, power generation and delivery, and modern energy technologies.

Structure: 8 Parts · 30 Chapters. Each part is a folder `part-N-<slug>/`: its `README.md` is the part opener and `NN-<slug>.md` is Chapter NN.

The backbone is **magnetic circuits → energy conversion → transformers and machines → drives → generation and storage → power-system analysis → transmission, distribution and protection → power quality and the modern grid → safety and design practice**. One idea runs through all of it: energy stored in a magnetic field or carried through a network is converted with losses, and those losses set efficiency, temperature and rating.

---

## Part I — Magnetic Circuits and Energy Conversion · `part-1-magnetic-circuits-and-energy-conversion/`

### Chapter 1. Magnetic Circuit Fundamentals · `01-magnetic-circuit-fundamentals.md`
- Magnetic flux
- Magnetic field intensity
- Flux density
- Permeability
- Reluctance
- Magnetomotive force
- Series and parallel magnetic paths
- Air gaps
- Fringing
- Magnetic saturation

### Chapter 2. Electromagnetic Induction · `02-electromagnetic-induction.md`
- Faraday's law
- Lenz's law
- Motional EMF
- Induced voltage
- Self-inductance
- Mutual inductance
- Energy conversion
- Electromagnetic torque
- Electromechanical energy balance

### Chapter 3. Energy Conversion Principles · `03-energy-conversion-principles.md`
- Electrical-to-mechanical conversion
- Mechanical-to-electrical conversion
- Force and torque production
- Magnetic co-energy
- Energy balance
- Rotating magnetic fields
- Loss mechanisms
- Efficiency
- Thermal constraints

## Part II — Transformers and Electrical Machines · `part-2-transformers-and-electrical-machines/`

### Chapter 4. Transformers · `04-transformers.md`
- Transformer operating principle
- Ideal transformer
- EMF equation
- Equivalent circuit
- Phasor diagrams
- Losses and efficiency
- Voltage regulation
- Open-circuit and short-circuit tests
- Transformer polarity
- Parallel operation
- Three-phase transformers
- Autotransformers
- Instrument transformers

### Chapter 5. DC Machines · `05-dc-machines.md`
- DC machine construction
- Armature windings
- EMF generation
- Torque production
- Separately excited machines
- Shunt and series machines
- Compound machines
- Characteristics
- Speed control
- Starting
- Braking
- Losses and efficiency

### Chapter 6. Induction Machines · `06-induction-machines.md`
- Three-phase induction principle
- Rotating magnetic field
- Slip
- Equivalent circuit
- Torque-speed characteristics
- Starting methods
- Speed control
- Losses and efficiency
- Single-phase induction motors
- Motor selection

### Chapter 7. Synchronous Machines · `07-synchronous-machines.md`
- Synchronous-machine construction
- Alternator operation
- EMF generation
- Phasor diagrams
- Voltage regulation
- Power-angle relationships
- Synchronization
- Parallel operation
- Synchronous motors
- Excitation and reactive power
- Stability fundamentals

### Chapter 8. Special Electrical Machines · `08-special-electrical-machines.md`
- Permanent-magnet synchronous motors
- Brushless DC motors
- Switched-reluctance motors
- Stepper motors
- Universal motors
- Linear motors
- Servo motors
- Specialized generators
- Selection and application trade-offs

### Chapter 9. Electrical Machine Design and Performance · `09-electrical-machine-design-and-performance.md`
- Rating and duty cycles
- Loss calculations
- Thermal limits
- Efficiency
- Insulation systems
- Cooling
- Winding design fundamentals
- Material selection
- Performance testing
- Reliability and maintenance

## Part III — Motor Drives · `part-3-motor-drives/`

### Chapter 10. Drive-System Fundamentals · `10-drive-system-fundamentals.md`
- Motor-load matching
- Torque and speed requirements
- Load characteristics
- Four-quadrant operation
- Starting and braking
- Drive efficiency
- Protection
- Drive selection

### Chapter 11. DC Motor Drives · `11-dc-motor-drives.md`
- Armature control
- Field control
- Chopper-fed drives
- Speed regulation
- Torque control
- Regenerative braking
- Practical drive architecture

### Chapter 12. AC Motor Drives · `12-ac-motor-drives.md`
- Variable-frequency drives
- Scalar control
- Vector control fundamentals
- Field-oriented control
- Direct torque control
- PWM inverters
- Induction motor speed control
- PMSM control fundamentals
- Drive commissioning

## Part IV — Power Generation · `part-4-power-generation/`

### Chapter 13. Power-System Structure · `13-power-system-structure.md`
- Generation, transmission, and distribution
- Grid architecture
- Power-system components
- AC versus DC systems
- Energy flow
- Load demand
- Reliability and resilience
- Power-system planning

### Chapter 14. Conventional Generation · `14-conventional-generation.md`
- Steam power plants
- Gas-turbine plants
- Combined-cycle plants
- Hydroelectric generation
- Nuclear generation
- Generator systems
- Plant efficiency
- Auxiliary loads
- Environmental considerations

### Chapter 15. Renewable Energy Systems · `15-renewable-energy-systems.md`
- Solar photovoltaic generation
- Wind generation
- Hydroelectric systems
- Biomass generation
- Geothermal energy
- Renewable-resource assessment
- Energy conversion
- Capacity factor
- Variability and forecasting

### Chapter 16. Energy Storage · `16-energy-storage.md`
- Battery technologies
- Battery energy and power ratings
- Battery management systems
- State of charge
- State of health
- Supercapacitors
- Flywheels
- Pumped hydro
- Thermal storage
- Hydrogen energy storage
- Storage economics and safety

## Part V — Power-System Analysis · `part-5-power-system-analysis/`

### Chapter 17. Per-Unit Systems and Network Modeling · `17-per-unit-systems-and-network-modeling.md`
- Per-unit quantities
- Base values
- Impedance conversion
- Single-line diagrams
- Equipment models
- Network reduction
- Bus and branch representation
- System-data preparation

### Chapter 18. Power-Flow Analysis · `18-power-flow-analysis.md`
- Bus classifications
- Power-balance equations
- Load-flow formulation
- Gauss–Seidel method
- Newton–Raphson method
- Fast-decoupled load flow
- Voltage profiles
- Reactive-power management
- Convergence and interpretation

### Chapter 19. Fault Analysis · `19-fault-analysis.md`
- Short-circuit fundamentals
- Symmetrical faults
- Unsymmetrical faults
- Symmetrical components
- Sequence networks
- Fault-current calculation
- Equipment fault ratings
- Fault-location concepts

### Chapter 20. Power-System Stability · `20-power-system-stability.md`
- Rotor-angle stability
- Voltage stability
- Frequency stability
- Small-signal stability
- Transient stability
- Disturbance response
- Stability margins
- Stability improvement
- Simulation and interpretation

## Part VI — Transmission, Distribution, and Protection · `part-6-transmission-distribution-and-protection/`

### Chapter 21. Transmission Lines · `21-transmission-lines.md`
- Line parameters
- Resistance, inductance, and capacitance
- Short, medium, and long line models
- Voltage regulation
- Efficiency
- Ferranti effect
- Corona
- Compensation
- High-voltage AC transmission
- HVDC fundamentals

### Chapter 22. Distribution Systems · `22-distribution-systems.md`
- Distribution architectures
- Radial and ring systems
- Distribution transformers
- Feeder analysis
- Voltage drop
- Distribution losses
- Voltage regulation
- Distributed generation
- Distribution planning

### Chapter 23. Power-System Protection · `23-power-system-protection.md`
- Protection principles
- Overcurrent protection
- Differential protection
- Distance protection
- Earth-fault protection
- Circuit breakers
- Fuses and relays
- Instrument transformers
- Protection coordination
- Selectivity and sensitivity

### Chapter 24. High-Voltage Engineering · `24-high-voltage-engineering.md`
- High-voltage generation and measurement
- Insulation coordination
- Dielectric breakdown
- Partial discharge
- Lightning and switching surges
- Surge arresters
- Grounding
- High-voltage testing
- Safety procedures

## Part VII — Power Quality and Grid Modernization · `part-7-power-quality-and-grid-modernization/`

### Chapter 25. Power Quality · `25-power-quality.md`
- Voltage variation
- Frequency variation
- Harmonics
- Flicker
- Transients
- Voltage sags and swells
- Unbalance
- Power-factor correction
- Measurement and mitigation

### Chapter 26. Smart Grids · `26-smart-grids.md`
- Smart-metering systems
- Grid communication
- Distributed energy resources
- Microgrids
- Demand response
- Grid automation
- Grid observability
- Energy management systems
- Cybersecurity fundamentals
- Resilience

### Chapter 27. Grid Integration of Renewable Energy · `27-grid-integration-of-renewable-energy.md`
- Grid-connected inverters
- Synchronization
- Active and reactive power control
- Grid-code fundamentals
- Anti-islanding
- Frequency support
- Voltage support
- Storage coordination
- Forecasting
- Renewable penetration limits

### Chapter 28. Energy Efficiency and Management · `28-energy-efficiency-and-management.md`
- Energy auditing
- Load profiles
- Demand management
- Industrial energy efficiency
- Motor efficiency
- Power-factor correction
- Energy monitoring
- Loss reduction
- Life-cycle energy cost
- Efficiency improvement strategies

## Part VIII — Electrical Safety and Engineering Practice · `part-8-electrical-safety-and-engineering-practice/`

### Chapter 29. Electrical Safety · `29-electrical-safety.md`
- Shock hazards
- Arc-flash hazards
- Grounding and bonding
- Protective devices
- Isolation and lockout
- Safe testing
- Overcurrent protection
- Electrical installation safety
- Hazard assessment

### Chapter 30. Electrical System Design · `30-electrical-system-design.md`
- Load estimation
- Cable sizing
- Equipment ratings
- Transformer selection
- Generator selection
- Protection selection
- Grounding design
- Voltage-drop calculations
- Design documentation
- Standards and compliance

---

## Boundary

This book owns electromechanical energy conversion, electrical machines and drives, power generation and storage at system level, power-system analysis, transmission, distribution, protection, power quality, the modern grid, and electrical safety and design practice. Circuit theory, three-phase phasor analysis and control theory are taken from Book 3; semiconductor device physics and converter circuit internals belong to *Electronics & Computing*.

## Relation to the other books

| Topic | Where it lives |
|---|---|
| Complex numbers, linear algebra, ODEs, Laplace and Fourier transforms, numerical methods (the mathematics itself) | The Mathematics Universe |
| Electromagnetic fields, Maxwell's equations, thermodynamics and heat transfer (the physics itself) | Engineering Physics |
| Magnetic, conductor, insulating and battery materials (structure and properties) | The Materials Core |
| Circuit laws, AC phasors and power, three-phase circuits, coupled coils, transmission-line wave theory, Laplace-domain analysis, feedback and control theory | Circuits, Signals and Communications (Book 3) |
| Power-semiconductor devices, gate drivers, converter circuit internals, microcontrollers and data converters | Electronics & Computing |
| Practical robot and industrial-automation controllers | Robotics and automation books |
| Machines, drives, generation, storage, power-system analysis, transmission, distribution, protection, power quality, smart grids, electrical safety and design | **This book** |
