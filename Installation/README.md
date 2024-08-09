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
