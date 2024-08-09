import CoSimIO

def cosimio_check_equal(a, b):
    assert a == b

# Connection Settings
settings = CoSimIO.Info()
settings.SetString("my_name", "my_code")
settings.SetString("connect_to", "Kratos")
settings.SetInt("echo_level", 1)
settings.SetString("version", "1.25")

# Connecting
return_info = CoSimIO.Connect(settings)
cosimio_check_equal(return_info.GetInt("connection_status"), CoSimIO.ConnectionStatus.Connected)
connection_name = return_info.GetString("connection_name")

# Create origin and destination ModelParts
model_part_origin = CoSimIO.ModelPart("my_mesh_origin")
model_part_destination = CoSimIO.ModelPart("my_mesh_destination")

# Fill the ModelParts with nodes & elements
for i in range(10):
    model_part_origin.CreateNewNode(i+1, 1.1*i, 0, 0)
    model_part_destination.CreateNewNode(i+1, 1.2*i, 0, 0)

for i in range(5):
    model_part_origin.CreateNewElement(i+1, CoSimIO.ElementType.Line2D2, [i+1, i+2])
    model_part_destination.CreateNewElement(i+1, CoSimIO.ElementType.Line2D2, [i+1, i+2])

# Send origin mesh to Kratos
info = CoSimIO.Info()
info.SetString("identifier", "mesh_origin")
info.SetString("connection_name", connection_name)
CoSimIO.ExportMesh(info, model_part_origin)

# Send destination mesh to Kratos
info.SetString("identifier", "mesh_destination")
info.SetString("connection_name", connection_name)
CoSimIO.ExportMesh(info, model_part_destination)

# Prepare the data to be mapped (example scalar data)
data_to_map = CoSimIO.DoubleVector([100.0 + i for i in range(model_part_origin.NumberOfNodes())])

# Send the origin data to Kratos for mapping
info.SetString("identifier", "data_to_map")
info.SetString("connection_name", connection_name)
CoSimIO.ExportData(info, data_to_map)

# Receive the mapped destination data from Kratos
mapped_data = CoSimIO.DoubleVector()

info.SetString("identifier", "mapped_data")
info.SetString("connection_name", connection_name)
CoSimIO.ImportData(info, mapped_data)

# (Optional) Print or process the mapped data
print("Mapped Data:", mapped_data)

# Disconnecting
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
return_info = CoSimIO.Disconnect(disconnect_settings)
cosimio_check_equal(return_info.GetInt("connection_status"), CoSimIO.ConnectionStatus.Disconnected)

print("Mesh mapping and data exchange with Kratos completed and disconnected.")