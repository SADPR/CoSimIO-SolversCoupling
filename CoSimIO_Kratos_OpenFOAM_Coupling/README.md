# OpenFOAM-Kratos Coupling Case

This folder contains an example of coupling OpenFOAM and Kratos using CoSimIO for data exchange. The OpenFOAM case simulates the flow over a backward-facing step, and the outlet velocities are used as inlet conditions for a Kratos simulation of flow past a cylinder.

## Files and Directories

- [OpenFoamCase/pitzDaily](../OpenFoamCase/pitzDaily): Contains the OpenFOAM case setup.
- [KratosCase/FlowPastACylinder.gid](../KratosCase/FlowPastACylinder.gid): Contains the Kratos case setup.
- `export_velocity_from_openfoam.py`: Script to run OpenFOAM, export velocity data, and communicate with Kratos via CoSimIO.
- `kratos_cosimio_receiver.py`: Script to run Kratos, import velocity data from OpenFOAM, and perform the coupled simulation.

## Running the Example

### Step 1: Run the OpenFOAM Simulation

Open a terminal and run the `export_velocity_from_openfoam.py` script to simulate the flow in OpenFOAM and send the outlet velocity data to Kratos.

```bash
python3 export_velocity_from_openfoam.py
```

Step 2: Run the Kratos Simulation
In another terminal, run the kratos_cosimio_receiver.py script to simulate the flow past a cylinder in Kratos using the data received from OpenFOAM.

```bash
python3 kratos_cosimio_receiver.py
```

### Note on OpenFOAM Integration
To the best of my knowledge, OpenFOAM does not provide a straightforward Python interface for controlling each time step's  directly. As a workaround, this example restarts the simulation at each time step, utilizing OpenFOAM's built-in functions to output the desired data. The data exchange itself is completely handled by CoSimIO.

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

## Visualization of Results
You can visualize the OpenFOAM results using ParaView by running paraFoam in the OpenFoamCase/pitzDaily directory.

For Kratos, the results can be visualized using the provided output paths in the vtk_output directory within the KratosCase/FlowPastACylinder.gid folder.

## Requirements
- OpenFOAM v11: OpenFOAM Installation Guide
- Kratos Multiphysics: Kratos Installation Guide
- CoSimIO: Installed and available in your Python environment.
- PyFoam: A Python package for interacting with OpenFOAM cases. Install via pip:
```bash
pip install PyFoam
```
