# Simulation Data Exchange with Kratos using CoSimIO
This example demonstrates how to set up a simulation where Kratos Multiphysics exports velocity data using CoSimIO, and another script receives and processes this data.

## Prerequisites
Ensure that CoSimIO and KratosMultiphysics are installed and set up correctly:

- [CoSimIO Installation Guide](https://kratosmultiphysics.github.io/CoSimIO/tutorials/python/integration_co_sim_io.html)
- [KratosMultiphysics Installation Guide](https://github.com/KratosMultiphysics/Kratos/blob/master/INSTALL.md)

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
