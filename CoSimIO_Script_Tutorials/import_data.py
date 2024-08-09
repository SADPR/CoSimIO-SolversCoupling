import CoSimIO
import time  # Import time module to use sleep for synchronization

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "py_import_data")    # my name
settings.SetString("connect_to", "py_export_data") # to whom I want to connect to
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as py_import_data!")

# Prepare to import data
import_info = CoSimIO.Info()
import_info.SetString("identifier", "vector_of_pi")
import_info.SetString("connection_name", connection_name)
data_to_import = CoSimIO.DoubleVector()

# Import the data
return_info = CoSimIO.ImportData(import_info, data_to_import)
print("Data imported successfully!")
print("Imported data:", list(data_to_import))

# Adding a small delay to ensure all operations complete before disconnection
time.sleep(2)

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected py_import_data!")


