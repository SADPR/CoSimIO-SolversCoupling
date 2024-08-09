from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Execution.BasicRunner import BasicRunner
import os
import sys

# Redirect standard error output to a null device to suppress error messages
sys.stderr = open(os.devnull, 'w')

# Define the case directory
case_dir = "/home/sebastianadpr/OpenFOAM/sebastianadpr-11/run/cylinder/pitzDaily"

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
    simple_foam = BasicRunner(argv=["simpleFoam", "-case", case_dir], silent=False)
    simple_foam.start()

    # Process data here (you can load and process OpenFOAM data)
    # For example, read velocity data from the "outlet.xy" file in the postProcessing directory
    post_process_dir = os.path.join(case_dir, "postProcessing", "outletVelocity", f"{end_time}")
    velocity_file = os.path.join(post_process_dir, "outlet.xy")
    
    if os.path.exists(velocity_file):
        with open(velocity_file, 'r') as file:
            data = file.read()
            print(f"Time Step {end_time} - Velocity at outlet boundary:\n{data}")

    # Increment time steps
    start_time = end_time
    end_time += 1

    # Update controlDict for the next step
    control_dict["startTime"] = start_time
    control_dict["endTime"] = end_time
    control_dict.writeFile()








