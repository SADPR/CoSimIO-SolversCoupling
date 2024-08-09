import CoSimIO
import time

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "import_velocity_from_openfoam")
settings.SetString("connect_to", "export_velocity_from_openfoam")
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as import_velocity_from_openfoam_cosimio!")

# Loop to import data for each time step
for timestep in range(1, 301):
    # Prepare to import data
    import_info = CoSimIO.Info()
    import_info.SetString("identifier", f"outlet_velocity_timestep_{timestep}")
    import_info.SetString("connection_name", connection_name)
    data_to_import = CoSimIO.DoubleVector()

    # Import the data
    return_info = CoSimIO.ImportData(import_info, data_to_import)
    print(f"Data imported successfully for Time Step {timestep}!")
    print("Imported data:", list(data_to_import))

    # Acknowledge receipt of data
    ack_info = CoSimIO.Info()
    ack_info.SetString("identifier", f"acknowledge_timestep_{timestep}")
    ack_info.SetString("connection_name", connection_name)
    ack_data = CoSimIO.DoubleVector([1.0])  # Dummy data to send as acknowledgment
    CoSimIO.ExportData(ack_info, ack_data)

    # Adding a small delay to ensure all operations complete before disconnection
    # time.sleep(2)

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected import_velocity_from_openfoam_cosimio!")


