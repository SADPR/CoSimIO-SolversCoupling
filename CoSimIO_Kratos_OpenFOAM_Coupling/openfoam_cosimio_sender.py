from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
import os
import sys
import CoSimIO

# Initialize CoSimIO and connect
settings = CoSimIO.Info()
settings.SetString("my_name", "openfoam_cosimio_sender")
settings.SetString("connect_to", "kratos_cosimio_receiver")
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")
info = CoSimIO.Connect(settings)
connection_name = info.GetString("connection_name")

# Redirect standard error output to a null device to suppress error messages
sys.stderr = open(os.devnull, 'w')

# Define the case directory
case_dir = "../OpenFoamCase/pitzDaily" #Change this.

# Load controlDict
control_dict = ParsedParameterFile(os.path.join(case_dir, "system", "controlDict")) 

# Set initial startTime and endTime
start_time = 0
time_step = 1
end_time = 1
final_time = 301  # Set this to the desired end time of the simulation

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
                velocities.extend([
                    float(values[0]), float(values[1]), float(values[2]),  # Coordinates (x, y, z)
                    float(values[3]), float(values[4]), float(values[5])   # Velocity components (Ux, Uy, Uz)
                ])

            # Prepare data to be exported
            identifier = f"outlet_velocity_timestep_{str(end_time).replace('.', '_')}" # It does not allow 0.1, it has to be 0_1 instead.
            export_info = CoSimIO.Info()
            export_info.SetString("identifier", identifier)
            export_info.SetString("connection_name", connection_name)
            data_to_export = CoSimIO.DoubleVector(velocities)

            # Export the data
            CoSimIO.ExportData(export_info, data_to_export)
            print(f"Data exported successfully for Time Step {end_time}!")

    # Wait for acknowledgment from the importing script
    identifier = f"acknowledge_timestep_{str(end_time).replace('.', '_')}" # It does not allow 0.1, it has to be 0_1 instead.
    ack_info = CoSimIO.Info()
    ack_info.SetString("identifier", identifier)
    ack_info.SetString("connection_name", connection_name)
    ack_data = CoSimIO.DoubleVector()
    CoSimIO.ImportData(ack_info, ack_data)

    # Increment time steps
    start_time = end_time
    end_time = round(end_time + time_step + 1e-6, 1) # In case you are working with decimals. Avoid time steps like 3.099999999996.

    # If you want to remove the trailing .0 for whole numbers:
    if end_time.is_integer():
        end_time = int(end_time)

    # Update controlDict for the next step
    control_dict["startTime"] = start_time
    control_dict["endTime"] = end_time
    control_dict.writeFile()

# Disconnect from CoSimIO
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected openfoam_cosimio_sender!")

