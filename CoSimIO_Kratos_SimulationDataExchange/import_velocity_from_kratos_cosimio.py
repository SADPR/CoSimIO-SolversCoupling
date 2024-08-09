import CoSimIO

def ReceiveVelocities():
    # Create settings for the connection
    settings = CoSimIO.Info()
    settings.SetString("my_name", "import_velocity_from_kratos_cosimio")
    settings.SetString("connect_to", "export_velocity_from_kratos_cosimio")
    settings.SetInt("echo_level", 1)
    settings.SetString("solver_version", "1.25")

    # Establish the connection
    info = CoSimIO.Connect(settings)
    connection_name = info.GetString("connection_name")

    # Loop to import data for each time step
    for timestep in range(1, 301):  # Adjust according to your simulation steps
        # Prepare to import data
        import_info = CoSimIO.Info()
        import_info.SetString("identifier", f"velocity_data_timestep_{timestep}")
        import_info.SetString("connection_name", connection_name)
        data_to_import = CoSimIO.DoubleVector()

        # Import the data
        return_info = CoSimIO.ImportData(import_info, data_to_import)
        velocities = list(data_to_import)
        print(f"Data imported successfully for Time Step {timestep}!")
        print("Imported data:", velocities)

        # Acknowledge receipt of data
        ack_info = CoSimIO.Info()
        ack_info.SetString("identifier", f"acknowledge_timestep_{timestep}")
        ack_info.SetString("connection_name", connection_name)
        ack_data = CoSimIO.DoubleVector([1.0])  # Dummy data to send as acknowledgment
        CoSimIO.ExportData(ack_info, ack_data)

    # Disconnect from CoSimIO
    disconnect_settings = CoSimIO.Info()
    disconnect_settings.SetString("connection_name", connection_name)
    CoSimIO.Disconnect(disconnect_settings)

if __name__ == "__main__":
    ReceiveVelocities()

