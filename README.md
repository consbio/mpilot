# MPilot
MPilot is a plugin-based, environmental modeling framework based on a bottom-up, many-to-many workflow that can be 
represented by a directed (not iterating) graph. MPilot is descended from the Environmental Evaluation Modeling System 
(EEMS), which was initially a fuzzy logic modeling package based on EMDS.

[MPilot Documentation](https://consbio.github.io/mpilot/)

# Installing

MPilot with EEMS can be installed with `pip`:

```bash
$ pip install mpilot
```

In order to run MPilot with NetCDF datasets, you'll need to install the NetCDF variant:

```bash
$ pip install mpilot[netcdf]
```

# Creating models
MPilot models are contained in "command files", using a simple scripting language. Here is an example model, which 
loads two columns of integer data from a CSV file, sums them, and writes the result to a second CSV file.

```text
A = EEMSRead(
    InFileName = "input.csv",
    InFieldName = "A",
    DataType = "Integer"
)
B = EEMSRead(
    InFileName = "input.csv",
    InFieldName = "B",
    DataType = "Integer"
)
APlusB = Sum(
    InFieldNames = [A, B]
)
Out = EEMSWrite(
    OutFileName = "output.csv",
    OutFieldNames = [A, B, APlusB]
)
```

# Running models

Models are run using the included `mpilot` program. The following commands will run a model using the EEMS CSV library 
and using the EEMS NetCDF library respectively:

```bash
$ mpilot eems-csv model.mpt
$ mpilot eems-netcdf model.mpt
```
