import CoSimIO

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "py_import_mesh")    # my name
settings.SetString("connect_to", "py_export_mesh") # to whom I want to connect to
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as py_import_mesh!")

# Prepare to import the mesh
import_info = CoSimIO.Info()
import_info.SetString("identifier", "fluid_mesh")
import_info.SetString("connection_name", connection_name)

# Create an empty model part to receive the mesh
model_part = CoSimIO.ModelPart("imported_model_part")

# Import the mesh
import_info = CoSimIO.ImportMesh(import_info, model_part)
print("Mesh imported successfully!")

# Display the imported nodes and elements
print("Imported Nodes:")
for node in model_part.Nodes:
    print(f"Node {node.Id()}: ({node.X()}, {node.Y()}, {node.Z()})")

print("Imported Elements:")
for elem in model_part.Elements:
    node_ids = [node.Id() for node in elem.Nodes]
    print(f"Element {elem.Id()} with nodes {node_ids}")

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected py_import_mesh!")




