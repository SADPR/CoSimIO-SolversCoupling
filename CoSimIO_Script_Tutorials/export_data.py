import CoSimIO

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "py_export_data")    # my name
settings.SetString("connect_to", "py_import_data") # to whom I want to connect to
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as py_export_data!")

# Prepare data to be exported
export_info = CoSimIO.Info()
export_info.SetString("identifier", "vector_of_pi")
export_info.SetString("connection_name", connection_name)
data_to_export = CoSimIO.DoubleVector([3.14, 3.14, 3.14, 3.14])

# Export the data
return_info = CoSimIO.ExportData(export_info, data_to_export)
print("Data exported successfully!")

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected py_export_data!")

