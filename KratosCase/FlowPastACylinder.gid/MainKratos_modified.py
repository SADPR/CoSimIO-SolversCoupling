import sys
import time
import importlib
import numpy as np
import KratosMultiphysics
import os

def CreateAnalysisStage(cls, global_model, parameters):
    class AnalysisStage(cls):
        def __init__(self, model, project_parameters):
            super().__init__(model, project_parameters)
            self.model = model
            self.case_dir = "/home/sebastianadpr/Documents/CoSimIO/Kratos-OpenFoam/OpenFoam/pitzDaily"
            self.time_step = 1

        def InitializeSolutionStep(self):
            super().InitializeSolutionStep()

            # Path to OpenFOAM velocity data
            post_process_dir = os.path.join(self.case_dir, "postProcessing", "outletVelocity", f"{self.time_step}")
            velocity_file = os.path.join(post_process_dir, "outlet.xy")

            with open(velocity_file, 'r') as file:
                data = file.readlines()[1:]  # Skip the header
                velocities = [list(map(float, line.split())) for line in data]

            model_part = self.model.GetModelPart("FluidModelPart").GetSubModelPart("AutomaticInlet2D_Inlet")

            for node in model_part.Nodes:
                interpolated_velocity = self.interpolate_velocity(node.X, node.Y, velocities)
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_X, interpolated_velocity[0])
                node.SetSolutionStepValue(KratosMultiphysics.VELOCITY_Y, interpolated_velocity[1])
                node.Fix(KratosMultiphysics.VELOCITY_X)
                node.Fix(KratosMultiphysics.VELOCITY_Y)

            self.time_step += 1

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
    with open("ProjectParameters_modified.json", 'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    analysis_stage_module_name = parameters["analysis_stage"].GetString()
    analysis_stage_class_name = analysis_stage_module_name.split('.')[-1]
    analysis_stage_class_name = ''.join(x.title() for x in analysis_stage_class_name.split('_'))

    analysis_stage_module = importlib.import_module(analysis_stage_module_name)
    analysis_stage_class = getattr(analysis_stage_module, analysis_stage_class_name)

    global_model = KratosMultiphysics.Model()
    simulation = CreateAnalysisStage(analysis_stage_class, global_model, parameters)
    simulation.Run()
