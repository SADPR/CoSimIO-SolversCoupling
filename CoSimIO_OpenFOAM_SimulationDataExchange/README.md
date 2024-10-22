# Data Exchange with OpenFOAM using CoSimIO

This example demonstrates how to set up a simple data exchange where OpenFOAM exports velocity data using CoSimIO, and another script receives and processes this data.

## Prerequisites
Ensure that CoSimIO and OpenFOAM are installed and configured correctly:

- [CoSimIO Installation Guide](https://kratosmultiphysics.github.io/CoSimIO/tutorials/python/integration_co_sim_io.html)
- [OpenFOAM Installation Guide](https://openfoam.org/download/11-ubuntu/)

I used OpenFOAM v11 on Ubuntu 22.04 LTS (codename jammy). This version is compatible with Ubuntu versions 20.04, 22.04, 23.04, and 24.04. It includes ParaView support using the standard paraview package on Ubuntu 22.04.

## Steady Turbulent Flow over a Backward-Facing Step

This example explores steady turbulent flow over a backward-facing step using OpenFOAM's `simpleFoam` solver. It introduces mesh grading with `blockMesh` and demonstrates the solution of steady, incompressible turbulent flow.

For more details, refer to the [OpenFOAM tutorial guide](https://www.openfoam.com/documentation/tutorial-guide/3-compressible-flow/3.1-steady-turbulent-flow-over-a-backward-facing-step).

### Files Included

The case files are included in this repository under [OpenFoamCase/pitzDaily](../OpenFoamCase/pitzDaily).

You can also download the original tutorial files [here](https://develop.openfoam.com/Development/openfoam/tree/master/tutorials/incompressible/simpleFoam/pitzDaily).

<p align="center">
  <img src="media/openfoam_case.gif" alt="OpenFOAM Case Simulation" />
</p>

## Instructions
1. Run the OpenFOAM Export Script
Open a command window and run:

```bash
python3 export_velocity_from_openfoam.py
```

This script initializes the CoSimIO connection, runs the OpenFOAM case, and exports velocity data at each time step.

2. Run the Data Import Script
In another command window, run:

```bash
python3 import_velocity_from_openfoam.py
```

This script connects to the OpenFOAM exporter, waits for the data at each time step, processes it, and prints the imported velocities.

## Key Operations in the Scripts
### Export Script (export_velocity_from_openfoam.py):

- Connects to the receiver using CoSimIO.
- After each simulation step, it gathers velocity data and exports it using CoSimIO.
- Waits for acknowledgment from the receiver before proceeding.

### Import Script (import_velocity_from_openfoam.py):

- Connects to the OpenFOAM exporter.
- Imports velocity data for each time step and acknowledges the receipt of data.
- Processes and prints the received data.

## Note on OpenFOAM Integration
To the best of my knowledge, OpenFOAM does not provide a straightforward Python interface for controlling each time step's solution directly. As a workaround, this example restarts the simulation at each time step, utilizing OpenFOAM's built-in functions to output the desired data. The data exchange itself is completely handled by CoSimIO.

The Python script uses the PyFoam library, which can be installed from [PyPi](https://pypi.org/project/PyFoam/), to interact with OpenFOAM. You can visualize the results using paraFoam in the directory they were saved, which in this case is [OpenFoamCase/pitzDaily](../OpenFoamCase/pitzDaily).

Here is an example code snippet from the export_velocity_from_openfoam.py script:

```python
# Loop over each time step
while end_time <= final_time:
    # Run blockMesh (only once at the start)
    if start_time == 0:
        block_mesh = BasicRunner(argv=["blockMesh", "-case", case_dir], silent=False)
        block_mesh.start()

    # Run the solver (e.g., simpleFoam)
    simple_foam = BasicRunner(argv=["foamRun", "-solver", "incompressibleFluid", "-case", case_dir], silent=False)
    simple_foam.start()

    # Read the velocity data from postProcessing
    post_process_dir = os.path.join(case_dir, "postProcessing", "outletVelocity", f"{end_time}")
    velocity_file = os.path.join(post_process_dir, "outlet.xy")

    # ... (rest of the data export and communication with CoSimIO)
```

This will allow you to see the data exchange in action, with the import script receiving and processing the velocity data exported by OpenFOAM.
