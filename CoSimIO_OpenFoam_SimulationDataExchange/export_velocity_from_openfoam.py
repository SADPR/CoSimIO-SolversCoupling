from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
import os
import sys
import CoSimIO

# Initialize CoSimIO and connect
settings = CoSimIO.Info()
settings.SetString("my_name", "export_velocity_from_openfoam")
settings.SetString("connect_to", "import_velocity_from_openfoam")
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")
info = CoSimIO.Connect(settings)
connection_name = info.GetString("connection_name")

# Redirect standard error output to a null device to suppress error messages
sys.stderr = open(os.devnull, 'w')

# Define the case directory
case_dir = "/home/sebastianadpr/Documents/CoSimIO/Kratos-OpenFoam/OpenFoam/pitzDaily"

# Load controlDict
control_dict = ParsedParameterFile(os.path.join(case_dir, "system", "controlDict"))

# Set initial startTime and endTime
start_time = 0
end_time = 1
final_time = 100  # Set this to the desired end time of the simulation

# Update the controlDict file
control_dict["startTime"] = start_time
control_dict["endTime"] = end_time
control_dict.writeFile()

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

    if os.path.exists(velocity_file):
        with open(velocity_file, 'r') as file:
            data = file.readlines()[1:]  # Skip the header
            velocities = []
            for line in data:
                values = line.split()
                velocities.extend([float(values[3]), float(values[4]), float(values[5])])  # Extract U_x, U_y, U_z

            # Prepare data to be exported
            export_info = CoSimIO.Info()
            export_info.SetString("identifier", f"outlet_velocity_timestep_{end_time}")
            export_info.SetString("connection_name", connection_name)
            data_to_export = CoSimIO.DoubleVector(velocities)

            # Export the data
            CoSimIO.ExportData(export_info, data_to_export)
            print(f"Data exported successfully for Time Step {end_time}!")

    # Wait for acknowledgment from the importing script
    ack_info = CoSimIO.Info()
    ack_info.SetString("identifier", f"acknowledge_timestep_{end_time}")
    ack_info.SetString("connection_name", connection_name)
    ack_data = CoSimIO.DoubleVector()
    CoSimIO.ImportData(ack_info, ack_data)

    # Increment time steps
    start_time = end_time
    end_time += 1

    # Update controlDict for the next step
    control_dict["startTime"] = start_time
    control_dict["endTime"] = end_time
    control_dict.writeFile()

# Disconnect from CoSimIO
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected openfoam_cosimio_pitzDaily!")



