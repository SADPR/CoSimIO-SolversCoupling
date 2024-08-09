import importlib
import numpy as np
import KratosMultiphysics
import CoSimIO

def CreateAnalysisStageInstance(cls, global_model, parameters):
    class AnalysisStage(cls):
        def __init__(self, model, project_parameters):
            super().__init__(model, project_parameters)
            self.model = model
            self.time_step_cosimio = 1
            
            # Initialize CoSimIO and connect
            settings = CoSimIO.Info()
            settings.SetString("my_name", "kratos_cosimio_receiver")
            settings.SetString("connect_to", "openfoam_cosimio_sender")
            settings.SetInt("echo_level", 1)
            settings.SetString("solver_version", "1.25")
            info = CoSimIO.Connect(settings)
            self.connection_name = info.GetString("connection_name")

        def InitializeSolutionStep(self):
            super().InitializeSolutionStep()

            # Import the data from OpenFOAM via CoSimIO
            identifier = f"outlet_velocity_timestep_{str(self.time_step_cosimio).replace('.', '_')}" # It does not allow 0.1, it has to be 0_1 instead.
            import_info = CoSimIO.Info()
            import_info.SetString("identifier", identifier)
            import_info.SetString("connection_name", self.connection_name)
            data_to_import = CoSimIO.DoubleVector()

            return_info = CoSimIO.ImportData(import_info, data_to_import)
            velocities = list(data_to_import)
            num_points = len(velocities) // 6  # 3 for coordinates and 3 for velocity components (open-foam's is a 3D case).
            velocities = np.reshape(velocities, (num_points, 6))

            inlet_model_part = self.model.GetModelPart("FluidModelPart").GetSubModelPart("AutomaticInlet2D_Inlet")

            for node in inlet_model_part.Nodes:
                interpolated_velocity = self.interpolate_velocity(node.X, node.Y, velocities)
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_X, interpolated_velocity[0])
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_Y, interpolated_velocity[1])
                node.Fix(KratosMultiphysics.VELOCITY_X)
                node.Fix(KratosMultiphysics.VELOCITY_Y)

            # Acknowledge receipt of data
            identifier = f"acknowledge_timestep_{str(self.time_step_cosimio).replace('.', '_')}" # It does not allow 0.1, it has to be 0_1 instead.
            ack_info = CoSimIO.Info()
            ack_info.SetString("identifier", identifier)
            ack_info.SetString("connection_name", self.connection_name)
            ack_data = CoSimIO.DoubleVector([1.0])  # Dummy data to send as acknowledgment
            CoSimIO.ExportData(ack_info, ack_data)

            self.time_step_cosimio += 1

        def interpolate_velocity(self, x, y, velocities):
            # Calculate distances and corresponding weights
            distances = []
            for vel in velocities:
                dist = np.sqrt((vel[0] - x) ** 2 + (vel[1] - y) ** 2)
                if dist == 0:
                    return vel[3], vel[4]  # Directly return if the point matches exactly
                distances.append((1.0 / dist, vel))

            # Sort by distance (smallest distance = highest weight)
            distances.sort(reverse=True, key=lambda pair: pair[0])

            # Take the three closest points
            closest = distances[:3]

            # Normalize the weights
            sum_weights = sum([pair[0] for pair in closest])
            normalized_weights = [pair[0] / sum_weights for pair in closest]

            # Interpolate the velocity
            U_x_interp = sum(w * vel[3] for w, (_, vel) in zip(normalized_weights, closest))
            U_y_interp = sum(w * vel[4] for w, (_, vel) in zip(normalized_weights, closest))

            return U_x_interp, U_y_interp

    return AnalysisStage(global_model, parameters)

if __name__ == "__main__":
    with open("../KratosCase/FlowPastACylinder.gid/ProjectParameters_modified.json", 'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    # Here, I am adapting the paths for the inputs/outputs.
    parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString("../KratosCase/FlowPastACylinder.gid/FlowPastACylinder")
    parameters["solver_settings"]["material_import_settings"]["materials_filename"].SetString("../KratosCase/FlowPastACylinder.gid/FluidMaterials.json")
    parameters["output_processes"]["vtk_output"][0]["Parameters"]["output_path"].SetString("../KratosCase/FlowPastACylinder.gid/vtk_output")

    analysis_stage_module_name = parameters["analysis_stage"].GetString()
    analysis_stage_class_name = analysis_stage_module_name.split('.')[-1]
    analysis_stage_class_name = ''.join(x.title() for x in analysis_stage_class_name.split('_'))

    analysis_stage_module = importlib.import_module(analysis_stage_module_name)
    analysis_stage_class = getattr(analysis_stage_module, analysis_stage_class_name)

    global_model = KratosMultiphysics.Model()
    simulation = CreateAnalysisStageInstance(analysis_stage_class, global_model, parameters)
    simulation.Run()


