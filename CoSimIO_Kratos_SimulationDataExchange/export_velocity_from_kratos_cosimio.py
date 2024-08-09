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
            settings.SetString("my_name", "export_velocity_from_kratos_cosimio")
            settings.SetString("connect_to", "import_velocity_from_kratos_cosimio")
            settings.SetInt("echo_level", 1)
            settings.SetString("solver_version", "1.25")
            info = CoSimIO.Connect(settings)
            self.connection_name = info.GetString("connection_name")

        def InitializeSolutionStep(self):
            super().InitializeSolutionStep()

            inlet_model_part = self.model.GetModelPart("FluidModelPart").GetSubModelPart("AutomaticInlet2D_Inlet")

            for node in inlet_model_part.Nodes:
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_X, 10.0)
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_Y, 0.0)
                node.Fix(KratosMultiphysics.VELOCITY_X)
                node.Fix(KratosMultiphysics.VELOCITY_Y)

        def FinalizeSolutionStep(self):
            super().FinalizeSolutionStep()

            model_part = self.model.GetModelPart("FluidModelPart").GetSubModelPart("Outlet2D_Outlet")

            velocities = []
            for node in model_part.Nodes:
                velocities.append(node.X)
                velocities.append(node.Y)
                velocities.append(node.Z)
                velocities.append(node.GetSolutionStepValue(KratosMultiphysics.VELOCITY_X))
                velocities.append(node.GetSolutionStepValue(KratosMultiphysics.VELOCITY_Y))
                velocities.append(node.GetSolutionStepValue(KratosMultiphysics.VELOCITY_Z))

            # Prepare data to be exported
            export_info = CoSimIO.Info()
            export_info.SetString("identifier", f"outlet_velocity_timestep_{self.time_step_cosimio}")
            export_info.SetString("connection_name", self.connection_name)
            data_to_export = CoSimIO.DoubleVector(velocities)

            # Export the data
            CoSimIO.ExportData(export_info, data_to_export)
            print(f"Data exported successfully for Time Step {self.time_step_cosimio}!")

            # Wait for acknowledgment from the importing script
            ack_info = CoSimIO.Info()
            ack_info.SetString("identifier", f"acknowledge_timestep_{self.time_step_cosimio}")
            ack_info.SetString("connection_name", self.connection_name)
            ack_data = CoSimIO.DoubleVector()
            CoSimIO.ImportData(ack_info, ack_data)

            self.time_step_cosimio += 1

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
