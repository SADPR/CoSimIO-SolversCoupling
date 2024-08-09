import KratosMultiphysics as KM
from KratosMultiphysics.CoSimulationApplication import CoSimIO

# Create Kratos Model and ModelPart
model = KM.Model()
model_part = model.CreateModelPart("mp_test")

# Connection Settings
connection_settings = CoSimIO.Info()
connection_settings.SetString("my_name", "Kratos")
connection_settings.SetString("connect_to", "my_code")
connection_settings.SetInt("echo_level", 0)

# Connecting
info = CoSimIO.Connect(connection_settings)
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Connected:
    raise Exception("Connecting failed")

# Import mesh from "my_code"
import_info = CoSimIO.Info()
import_info.SetString("connection_name", connection_name)
import_info.SetString("identifier", "mesh_exchange_1")
CoSimIO.ImportMesh(import_info, model_part, KM.ParallelEnvironment.GetDefaultDataCommunicator())

# (Optional) Print imported mesh information
print(model_part)

# Export the mesh back to "my_code"
export_info = CoSimIO.Info()
export_info.SetString("connection_name", connection_name)
export_info.SetString("identifier", "mesh_exchange_2")
CoSimIO.ExportMesh(export_info, model_part)

# Disconnecting
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Disconnected:
    raise Exception("Disconnecting failed")

print("Mesh exchange with my_code completed and disconnected.")

