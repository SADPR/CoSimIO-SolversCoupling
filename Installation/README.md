## Installation

This repository is based on the official [CoSimIO tutorial](https://kratosmultiphysics.github.io/CoSimIO/) provided by Kratos Multiphysics. Some files and examples have been adapted to suit specific needs for coupling solvers and data exchange.

### 1. Clone the CoSimIO Repository

```bash
git clone https://github.com/KratosMultiphysics/CoSimIO.git
cd CoSimIO
```

### 2. Build the Python Interface
Use the provided script to build CoSimIO with Python bindings:

For GNU/Linux or macOS:

```bash
bash scripts/build_python.sh
```

### 3. Set Up Environment Variables
After building, add the bin directory to your PYTHONPATH and LD_LIBRARY_PATH:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/CoSimIO/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/CoSimIO/bin
```
Replace /path/to/CoSimIO with the actual path to your cloned CoSimIO directory.

## Hello CoSimIO

After integrating CoSimIO in your code, it's time to say hello:

Make sure to set up your environment variables first (this is my case):

```
export PYTHONPATH=$PYTHONPATH:/home/sares/CoSimIO/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/sares/CoSimIO/bin
```

To try saying hello, please run:
```
python3 hello.py
```

Expected Ouput:
```
Hello, this is the CoSimIO
The detached interface for coupled simulations together with the
CoSimulationApplication of KratosMultiphysics
"https://github.com/KratosMultiphysics/Kratos/tree/master/applications/CoSimulationApplication"
Version:
    Major: 4
    Minor: 3
    Patch: 1
For more information please visit "https://github.com/KratosMultiphysics/CoSimIO"
CoSimIO-Info; containing 3 entries
  name: major_version | value: 4 | type: int
  name: minor_version | value: 3 | type: int
  name: patch_version | value: 1 | type: string

CoSimIO version: 4.3.1
```
