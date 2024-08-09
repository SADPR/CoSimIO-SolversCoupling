# CoSimIO Script Tutorials

This section provides hands-on examples of using CoSimIO for data exchange between Python scripts. These tutorials are designed to help you understand the fundamentals of CoSimIO communication, including connecting, disconnecting, and exchanging data such as velocities and mesh information. The examples do not require solvers and are a great starting point for integrating CoSimIO into more complex workflows.

## CoSimIO Example Repository

This repository is based on the official [CoSimIO tutorial](https://kratosmultiphysics.github.io/CoSimIO/) provided by Kratos Multiphysics. Some files and examples have been adapted to suit specific needs for coupling solvers and data exchange. We encourage you to visit the official documentation for more details.

## Corrected Python Files

This section contains corrected `.py` files with adjustments made to the examples.

### Connecting and Disconnecting

To connect and disconnect, please find attached my files and run:

In one command window:
```
python3 connect_disconnect_a.py
```

In another command window:
```
python3 connect_disconnect_b.py
```

Expected Ouput:

connect_disconnect_a.py:
```
CoSimIO: CoSimIO from "py_connect_disconnect_a" to "py_connect_disconnect_b" uses communication format: socket
CoSimIO: Establishing connection for "py_connect_disconnect_a_py_connect_disconnect_b"
    from: "py_connect_disconnect_a"
    to:   "py_connect_disconnect_b"
    as PRIMARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_connect_disconnect_a_py_connect_disconnect_b/CoSimIO_py_connect_disconnect_a_py_connect_disconnect_b_compatibility_check_secondary_to_primary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_connect_disconnect_a_py_connect_disconnect_b/CoSimIO_py_connect_disconnect_a_py_connect_disconnect_b_compatibility_check_secondary_to_primary.dat"
CoSimIO: Connection established
Connected as py_connect_disconnect_a!
CoSimIO: Disconnecting "py_connect_disconnect_a_py_connect_disconnect_b" ...
CoSimIO: Disconnecting successful
Disconnected py_connect_disconnect_a!
```

connect_disconnect_b.py:
```
CoSimIO: CoSimIO from "py_import_data" to "py_export_data" uses communication format: socket
CoSimIO: Establishing connection for "py_export_data_py_import_data"
    from: "py_import_data"
    to:   "py_export_data"
    as SECONDARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_primary_to_secondary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_primary_to_secondary.dat"
CoSimIO: Connection established
Connected as py_import_data!
Data imported successfully!
Imported data: [3.14, 3.14, 3.14, 3.14]
CoSimIO: Disconnecting "py_export_data_py_import_data" ...
CoSimIO: Disconnecting successful
Disconnected py_import_data!
```

### Data Exchange

For data exchange between different solvers/software tools:

In one command window:
```
python3 export_data.py
```

In another command window:
```
python3 import_data.py
```

export_data.py:
```
CoSimIO: CoSimIO from "py_export_data" to "py_import_data" uses communication format: socket
CoSimIO: Establishing connection for "py_export_data_py_import_data"
    from: "py_export_data"
    to:   "py_import_data"
    as PRIMARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_secondary_to_primary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_secondary_to_primary.dat"
CoSimIO: Connection established
Connected as py_export_data!
Data exported successfully!
CoSimIO: Disconnecting "py_export_data_py_import_data" ...
CoSimIO: Disconnecting successful
Disconnected py_export_data!
```

import_data.py:
```
CoSimIO: CoSimIO from "py_import_data" to "py_export_data" uses communication format: socket
CoSimIO: Establishing connection for "py_export_data_py_import_data"
    from: "py_import_data"
    to:   "py_export_data"
    as SECONDARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_primary_to_secondary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_export_data_py_import_data/CoSimIO_py_export_data_py_import_data_compatibility_check_primary_to_secondary.dat"
CoSimIO: Connection established
Connected as py_import_data!
Data imported successfully!
Imported data: [3.14, 3.14, 3.14, 3.14]
CoSimIO: Disconnecting "py_export_data_py_import_data" ...
CoSimIO: Disconnecting successful
Disconnected py_import_data!
```

### Mesh Exchange

For mesh exchange:

In one command window:
```
python3 export_mesh.py
```

In another command window:
```
python3 import_mesh.py
```

Expected Ouput:

export_mesh.py
```
CoSimIO: CoSimIO from "py_export_mesh" to "py_import_mesh" uses communication format: socket
CoSimIO: Establishing connection for "py_export_mesh_py_import_mesh"
    from: "py_export_mesh"
    to:   "py_import_mesh"
    as PRIMARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_export_mesh_py_import_mesh/CoSimIO_py_export_mesh_py_import_mesh_compatibility_check_secondary_to_primary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_export_mesh_py_import_mesh/CoSimIO_py_export_mesh_py_import_mesh_compatibility_check_secondary_to_primary.dat"
CoSimIO: Connection established
Connected as py_export_mesh!
Mesh exported successfully!
CoSimIO: Disconnecting "py_export_mesh_py_import_mesh" ...
CoSimIO: Disconnecting successful
Disconnected py_export_mesh!
```

import_mesh.py
```
CoSimIO: CoSimIO from "py_import_mesh" to "py_export_mesh" uses communication format: socket
CoSimIO: Establishing connection for "py_export_mesh_py_import_mesh"
    from: "py_import_mesh"
    to:   "py_export_mesh"
    as SECONDARY connection; working directory: "." ...
CoSimIO: Waiting for: "./.CoSimIOComm_py_export_mesh_py_import_mesh/CoSimIO_py_export_mesh_py_import_mesh_compatibility_check_primary_to_secondary.dat"
CoSimIO: Found: "./.CoSimIOComm_py_export_mesh_py_import_mesh/CoSimIO_py_export_mesh_py_import_mesh_compatibility_check_primary_to_secondary.dat"
CoSimIO: Connection established
Connected as py_import_mesh!
Mesh imported successfully!
Imported Nodes:
Node 1: (0.0, 0.0, 0.0)
Node 2: (1.0, 0.0, 0.0)
Node 3: (1.0, 1.0, 0.0)
Node 4: (0.0, 1.0, 0.0)
Imported Elements:
Element 1 with nodes [1, 2, 3]
Element 2 with nodes [1, 3, 4]
CoSimIO: Disconnecting "py_export_mesh_py_import_mesh" ...
CoSimIO: Disconnecting successful
Disconnected py_import_mesh!
```