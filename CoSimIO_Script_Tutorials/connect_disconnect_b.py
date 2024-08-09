import CoSimIO

# Create settings for the connection
settings = CoSimIO.Info()
settings.SetString("my_name", "py_connect_disconnect_b")    # my name
settings.SetString("connect_to", "py_connect_disconnect_a") # to whom I want to connect to
settings.SetInt("echo_level", 1)
settings.SetString("solver_version", "1.25")

# Establish the connection
info = CoSimIO.Connect(settings)

# Check the connection status
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Connected:
    print("Connected as py_connect_disconnect_b!")

# Prepare to disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)

# Check the disconnection status
if info.GetInt("connection_status") == CoSimIO.ConnectionStatus.Disconnected:
    print("Disconnected py_connect_disconnect_b!")
