import CoSimIO

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "py_export_mesh")    # my name
settings.SetString("connect_to", "py_import_mesh") # to whom I want to connect to
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as py_export_mesh!")

# Create a model part and add some dummy nodes and elements to it
model_part = CoSimIO.ModelPart("exported_model_part")
model_part.CreateNewNode(1, 0.0, 0.0, 0.0)
model_part.CreateNewNode(2, 1.0, 0.0, 0.0)
model_part.CreateNewNode(3, 1.0, 1.0, 0.0)
model_part.CreateNewNode(4, 0.0, 1.0, 0.0)

element_type = CoSimIO.ElementType.Triangle2D3
model_part.CreateNewElement(1, element_type, [1, 2, 3])
model_part.CreateNewElement(2, element_type, [1, 3, 4])

# Prepare to export the mesh
export_info = CoSimIO.Info()
export_info.SetString("identifier", "fluid_mesh")
export_info.SetString("connection_name", connection_name)

# Export the mesh
export_info = CoSimIO.ExportMesh(export_info, model_part)
print("Mesh exported successfully!")

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected py_export_mesh!")

