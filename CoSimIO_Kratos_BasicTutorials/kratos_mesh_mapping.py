import KratosMultiphysics as KM
from KratosMultiphysics.CoSimulationApplication import CoSimIO
import KratosMultiphysics.MappingApplication as KratosMapping

# Create the Kratos ModelParts that contain the meshes
model = KM.Model()
model_part_origin = model.CreateModelPart("mp_origin")
model_part_destination = model.CreateModelPart("mp_destination")

# Allocate memory for nodal data
model_part_origin.AddNodalSolutionStepVariable(KM.TEMPERATURE)
model_part_destination.AddNodalSolutionStepVariable(KM.AMBIENT_TEMPERATURE)
model_part_origin.AddNodalSolutionStepVariable(KM.VELOCITY)
model_part_destination.AddNodalSolutionStepVariable(KM.MESH_VELOCITY)

# Connection Settings
connection_settings = CoSimIO.Info()
connection_settings.SetString("my_name", "Kratos")
connection_settings.SetString("connect_to", "my_code")
connection_settings.SetInt("echo_level", 1)

# Connecting
info = CoSimIO.Connect(connection_settings)
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Connected:
    raise Exception("Connecting failed")

# Import origin mesh
import_mesh_info_o = CoSimIO.Info()
import_mesh_info_o.SetString("connection_name", connection_name)
import_mesh_info_o.SetString("identifier", "mesh_origin")
CoSimIO.ImportMesh(import_mesh_info_o, model_part_origin, KM.ParallelEnvironment.GetDefaultDataCommunicator())

# Import destination mesh
import_mesh_info_d = CoSimIO.Info()
import_mesh_info_d.SetString("connection_name", connection_name)
import_mesh_info_d.SetString("identifier", "mesh_destination")
CoSimIO.ImportMesh(import_mesh_info_d, model_part_destination, KM.ParallelEnvironment.GetDefaultDataCommunicator())

# Import data to be mapped (simplified approach without DataLocation)
import_data_info = CoSimIO.Info()
import_data_info.SetString("connection_name", connection_name)
import_data_info.SetString("identifier", "data_to_map")
data_container = CoSimIO.DoubleVector()
CoSimIO.ImportData(import_data_info, data_container)

# Assign data to nodes (assuming scalar data)
for i, node in enumerate(model_part_origin.Nodes):
    node.SetSolutionStepValue(KM.TEMPERATURE, 0, data_container[i])

# Mapping Setup
mapper_settings = KM.Parameters("""{
    "mapper_type": "nearest_neighbor",
    "echo_level" : 1
}""")
mapper = KratosMapping.MapperFactory.CreateMapper(model_part_origin, model_part_destination, mapper_settings)

# Perform the mapping
mapper.Map(KM.TEMPERATURE, KM.AMBIENT_TEMPERATURE)
mapper.Map(KM.VELOCITY, KM.MESH_VELOCITY)

# Collect mapped data from nodes
mapped_data_container = CoSimIO.DoubleVector()
for node in model_part_destination.Nodes:
    mapped_data_container.append(node.GetSolutionStepValue(KM.AMBIENT_TEMPERATURE))

# Export mapped data
export_data_info = CoSimIO.Info()
export_data_info.SetString("connection_name", connection_name)
export_data_info.SetString("identifier", "mapped_data")
CoSimIO.ExportData(export_data_info, mapped_data_container)

# Disconnecting
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Disconnected:
    raise Exception("Disconnecting failed")

print("Mesh mapping and data exchange with my_code completed and disconnected.")

