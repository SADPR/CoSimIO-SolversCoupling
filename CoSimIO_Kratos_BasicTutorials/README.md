

# CoSimIO with Kratos Multiphysics - Basic Tutorials

### Description: 

This section provides simple tutorials for integrating CoSimIO with Kratos Multiphysics, focusing on basic mesh mapping and data exchange between Kratos and external scripts or codes.

### Notes
These examples demonstrate how to connect an external code with Kratos Multiphysics using CoSimIO, and perform operations like mesh mapping. The data_exchange and mesh_exchange examples with Kratos are combined into the kratos_mesh_mapping example for simplicity.

## Prerequisites

Make sure you've properly installed CoSimIO and Kratos Multiphysics and have set up your environment variables:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/CoSimIO/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/CoSimIO/bin
```

Replace /path/to/CoSimIO with the actual path to your CoSimIO installation.

## 1. Connecting to Kratos
In this example, we establish a connection between an external code (my_code) and Kratos.

Running the Example
Run the Kratos Side Script:

```bash
python3 connect_to_kratos.py
```

Run the External Solver (my_code) Script:

```bash
python3 my_code.py
```

Expected Output
connect_to_kratos.py Output:
```
Importing    KratosCoSimulationApplication
    KRATOS  / ___|___/ ___|(_)_ __ ___  _   _| | __ _| |_(_) ___  _ __
           | |   / _ \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \
           | |__| (_) |__) | | | | | | | |_| | | (_| | |_| | (_) | | | |
            \____\___/____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
Initializing KratosCoSimulationApplication...
CoSimIO: CoSimIO from "Kratos" to "my_code" uses communication format: socket
CoSimIO: Establishing connection for "Kratos_my_code"
    from: "Kratos"
    to:   "my_code"
    as PRIMARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_Kratos_my_code/CoSimIO_secondary_Kratos_my_code_conn.sync"
CoSimIO: Found: "./.CoSimIOComm_Kratos_my_code/CoSimIO_secondary_Kratos_my_code_conn.sync"
CoSimIO: Waiting for: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_secondary_to_primary.dat"
CoSimIO: Found: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_secondary_to_primary.dat"
CoSimIO: Using IP-Address: 127.0.0.1 and port number: 46063
CoSimIO: Connection established
Connected to my_code as Kratos_my_code
CoSimIO: Disconnecting "Kratos_my_code" ...
CoSimIO: Waiting for: "./.CoSimIOComm_Kratos_my_code/CoSimIO_secondary_Kratos_my_code_disconn.sync"
CoSimIO: Found: "./.CoSimIOComm_Kratos_my_code/CoSimIO_secondary_Kratos_my_code_disconn.sync"
CoSimIO: Disconnecting successful
Disconnected from my_code
Deregistering CoSimulationApplication
Deregistering KratosMultiphysics
```

Expected Output
my_code.py Output:
```
import CoSimIO

# Establish connection
connection_settings = CoSimIO.Info()
connection_settings.SetString("my_name", "my_code")
connection_settings.SetString("connect_to", "Kratos")
connection_settings.SetInt("echo_level", 2)

info = CoSimIO.Connect(connection_settings)
connection_name = info.GetString("connection_name")
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Connected:
    raise Exception("Connecting failed")

print(f"Connected to Kratos as {connection_name}")

# Perform some operations or wait (optional)
# ...

# Disconnect
disconnect_settings = CoSimIO.Info()
disconnect_settings.SetString("connection_name", connection_name)
info = CoSimIO.Disconnect(disconnect_settings)
if info.GetInt("connection_status") != CoSimIO.ConnectionStatus.Disconnected:
    raise Exception("Disconnecting failed")

print("Disconnected from Kratos")
```

# 2. Mesh Mapping with Kratos
This example demonstrates how to perform mesh mapping between two meshes using Kratos and an external code (my_code). The data exchange and mesh exchange with Kratos are combined in this case.

### Running the Example
Run the Kratos Side Script:

```bash
python3 kratos_mesh_mapping.py
```

Run the External Solver (my_code) Script:

```bash
python3 my_code_mesh_mapping.py
```

Expected Output

kratos_mesh_mapping.py Output:
```
Importing    KratosCoSimulationApplication
    KRATOS  / ___|___/ ___|(_)_ __ ___  _   _| | __ _| |_(_) ___  _ __
           | |   / _ \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \
           | |__| (_) |__) | | | | | | | |_| | | (_| | |_| | (_) | | | |
            \____\___/____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
Initializing KratosCoSimulationApplication...
Importing    KratosMappingApplication
    KRATOS ______  ___                      _____
           ___   |/  /_____ ___________________(_)_____________ _
           __  /|_/ /_  __ `/__  __ \__  __ \_  /__  __ \_  __ `/
           _  /  / / / /_/ /__  /_/ /_  /_/ /  / _  / / /  /_/ /
           /_/  /_/  \__,_/ _  .___/_  .___//_/  /_/ /_/_\__, /
                            /_/     /_/                 /____/
Initializing KratosMappingApplication...
CoSimIO: CoSimIO from "Kratos" to "my_code" uses communication format: socket
CoSimIO: Establishing connection for "Kratos_my_code"
    from: "Kratos"
    to:   "my_code"
    as PRIMARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_secondary_to_primary.dat"
CoSimIO: Found: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_secondary_to_primary.dat"
CoSimIO: Connection established
[WARNING] DEPRECATION-Warning; MappingApplication: The "MapperFactory" was moved to the Core! (used for "CreateMapper")
Mapper search: An average of 2 objects was found while searching
CoSimIO: Disconnecting "Kratos_my_code" ...
CoSimIO: Disconnecting successful
Mesh mapping and data exchange with my_code completed and disconnected.
Deregistering MappingApplication
Deregistering CoSimulationApplication
Deregistering KratosMultiphysics
```

my_code_mesh_mapping.py Output:
```
CoSimIO: CoSimIO from "my_code" to "Kratos" uses communication format: socket
CoSimIO: Establishing connection for "Kratos_my_code"
    from: "my_code"
    to:   "Kratos"
    as SECONDARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_primary_to_secondary.dat"
CoSimIO: Found: "./.CoSimIOComm_Kratos_my_code/CoSimIO_Kratos_my_code_compatibility_check_primary_to_secondary.dat"
CoSimIO: Connection established
Mapped Data: [100, 101, 102, 103, 104, 105, 107, 108, 109, 109]
CoSimIO: Disconnecting "Kratos_my_code" ...
CoSimIO: Disconnecting successful
Mesh mapping and data exchange with Kratos completed and disconnected.
```