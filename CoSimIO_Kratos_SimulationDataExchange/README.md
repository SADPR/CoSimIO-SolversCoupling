# Simulation Data Exchange with Kratos using CoSimIO
This example demonstrates how to set up a simulation where Kratos Multiphysics exports velocity data using CoSimIO, and another script receives and processes this data.

## Prerequisites
Ensure that CoSimIO and KratosMultiphysics are installed and set up correctly:

- [CoSimIO Installation Guide](https://kratosmultiphysics.github.io/CoSimIO/tutorials/python/integration_co_sim_io.html)
- [KratosMultiphysics Installation Guide](https://github.com/KratosMultiphysics/Kratos/blob/master/INSTALL.md)

## Flow Past a Cylinder Flow Simulation

This 2D CFD simulation explores the flow past a cylinder benchmark using Kratos. The case involves a cylinder placed in a channel with an inlet velocity and no-slip conditions on the walls. The simulation captures the development of a Von Karman vortex street downstream.

For more details, refer to the [Kratos Example](https://github.com/KratosMultiphysics/Examples/blob/master/fluid_dynamics/validation/body_fitted_cylinder_100Re/README.md).

### Files Included

The case files are included in this repository under [KratosCase/FlowPastACylinder](../KratosCase/FlowPastACylinder.gid).

<div style="text-align: center;">
  <img src="media/flow_past_cylinder.gif" alt="Flow Past a Cylinder" />
</div>

#### Note
The geometry was adapted so that the outlet of the OpenFOAM case directly connects to the inlet of the Kratos simulation, enabling seamless coupling between the two solvers.

## Instructions
1. Run the Kratos Export Script
Open a command window and run:

```bash
python3 export_velocity_from_kratos.py
```

This script initializes the CoSimIO connection, sets up the simulation, and exports velocity data at each solution step.

2. Run the Data Import Script
In another command window, run:

```bash
python3 import_velocity_from_kratos.py
```

This script connects to the Kratos exporter, waits for the data at each time step, processes it, and prints the imported velocities.

## Key Operations in the Scripts
### Export Script (export_velocity_from_kratos.py):

- Connects to the receiver using CoSimIO.
- After each solution step, it gathers velocity data and exports it using CoSimIO.
- Waits for acknowledgment from the receiver before proceeding.

### Import Script (import_velocity_from_kratos.py):

- Connects to the Kratos exporter.
- Imports velocity data for each time step and acknowledges the receipt of data.
- Processes and prints the received data.

This will allow you to see the data exchange in action, with the import script receiving and processing the velocity data exported by Kratos.
