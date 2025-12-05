from __future__ import absolute_import

import numpy
from netCDF4 import Dataset
from numpy.ma import is_masked

from mpilot import params
from mpilot.commands import Command
from mpilot.utils import insure_fuzzy
from .exceptions import NoSuchVariable, InvalidPositiveData, InvalidFuzzyData
from ..mixins import SameArrayShapeMixin

FUZZY_MIN = -1
FUZZY_MAX = 1


class EEMSRead(Command):
    """Reads a variable from a file, converting floats to nearest int when necessary."""

    display_name = "Read"
    inputs = {
        "InFileName": params.PathParameter(must_exist=True),
        "InFieldName": params.StringParameter(),
        "MissingValue": params.NumberParameter(required=False),
        "DataType": params.DataTypeParameter(
            required=False,
            valid_types={
                "Float": numpy.float64,
                "Integer": int,
                "Positive Float": numpy.float64,
                "Positive Integer": numpy.uint,
                "Fuzzy": numpy.float64,
            },
        ),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        path = kwargs["InFileName"]
        variable_name = kwargs["InFieldName"]
        data_type = kwargs.get("DataType", "Float")

        with Dataset(kwargs["InFileName"], "r") as dataset:
            if kwargs["InFieldName"] not in dataset.variables:
                raise NoSuchVariable(path, variable_name, lineno=self.lineno)

            variable = dataset[variable_name]
            data = variable[:]

        if self.get_argument_value("DataType", "Float") in ("Positive Integer", "Positive Float") and data.min() < 0:
            raise InvalidPositiveData(path, kwargs["DataType"], lineno=self.lineno)

        if numpy.issubdtype(data.dtype, numpy.float64) and data_type in (
            int,
            numpy.uint,
        ):
            data = numpy.rint(data, out=data)  # round in-place

        result = numpy.ma.array(
            data,
            mask=data.mask if is_masked(data) else False,
            dtype=data_type,
            fill_value=999999 if data_type in (int, numpy.uint) else None,
        )

        if kwargs.get("DataType", "Float") == "Fuzzy":
            fuzzy_pad = 0.01 * (FUZZY_MAX - FUZZY_MIN)

            if data.max() > FUZZY_MAX + fuzzy_pad or data.min() < FUZZY_MIN - fuzzy_pad:
                raise InvalidFuzzyData(path, lineno=self.lineno)

            insure_fuzzy(result, FUZZY_MIN, FUZZY_MAX)

        result.soften_mask()

        # Mask missing values
        if "MissingValue" in kwargs:
            missing_value = (
                int(kwargs["MissingValue"])
                if numpy.issubdtype(result.mask.dtype, int)
                else float(kwargs["MissingValue"])
            )

            self.result.mask = numpy.where(result.data == missing_value, True, result.mask or False)

        result.data[result.mask] = result.fill_value

        return result


class EEMSWrite(SameArrayShapeMixin, Command):
    """Writes one or more file"""

    display_name = "Write"
    inputs = {
        "OutFileName": params.PathParameter(must_exist=False),
        "OutFieldNames": params.ListParameter(params.ResultParameter(params.DataParameter())),
        "DimensionFileName": params.PathParameter(must_exist=True),
        "DimensionFieldName": params.StringParameter(),
    }
    output = params.BooleanParameter()

    def execute(self, **kwargs):
        commands = kwargs["OutFieldNames"]
        arrays = [c.result for c in commands]
        self.validate_array_shapes(arrays)

        with Dataset(kwargs["OutFileName"], "w") as dataset:
            with Dataset(kwargs["DimensionFileName"]) as dim_dataset:
                dimensions = dim_dataset[kwargs["DimensionFieldName"]].dimensions
                for dimension in dimensions:
                    in_dimension_variable = dim_dataset[dimension]
                    dataset.createDimension(dimension, in_dimension_variable.size)
                    out_dimension_variable = dataset.createVariable(
                        dimension,
                        in_dimension_variable.dtype,
                        [dimension],
                        fill_value=in_dimension_variable.get_fill_value(),
                    )

                    for attribute in dir(in_dimension_variable):
                        if attribute not in dir(out_dimension_variable) and attribute not in (
                            "_FillValue",
                            "missing_value",
                        ):
                            setattr(out_dimension_variable, attribute, getattr(in_dimension_variable, attribute))

                    for ncattr in in_dimension_variable.ncattrs():
                        if ncattr != "_FillValue":
                            out_dimension_variable.setncattr(ncattr, in_dimension_variable.getncattr(ncattr))

                    out_dimension_variable[:] = in_dimension_variable[:]

                # Discover CRS metadata (ESRI and CF)
                esri_pe = None
                grid_mapping = None
                for variable in dim_dataset.variables.values():
                    if "esri_pe_string" in variable.ncattrs():
                        esri_pe = variable.getncattr("esri_pe_string")
                        if "grid_mapping" in variable.ncattrs():
                            grid_mapping_name = variable.getncattr("grid_mapping")
                            if grid_mapping_name in dim_dataset.variables:
                                grid_mapping = grid_mapping_name
                                grid_mapping_in = dim_dataset.variables[grid_mapping]

                                for dimension in grid_mapping_in.dimensions:
                                    if dimension not in dataset.dimensions:
                                        dataset.createDimension(dimension, dim_dataset.dimensions[dimension].size)

                                grid_mapping_out = dataset.createVariable(
                                    grid_mapping, grid_mapping_in.dtype, grid_mapping_in.dimensions
                                )

                                for ncattr in grid_mapping_in.ncattrs():
                                    grid_mapping_out.setncattr(ncattr, grid_mapping_in.getncattr(ncattr))

                        break

            mask = numpy.copy(arrays[0].mask)
            for arr in arrays[1:]:
                mask |= arr.mask

            for command in commands:
                variable = dataset.createVariable(
                    command.result_name,
                    command.result.dtype.char,
                    dimensions,
                    fill_value=command.result.fill_value,
                    compression="zlib",
                    complevel=1,
                )
                variable[:] = numpy.ma.MaskedArray(command.result.data, mask)

                # Apply CRS metadata
                if esri_pe:
                    variable.setncattr("esri_pe_string", esri_pe)
                if grid_mapping:
                    variable.setncattr("grid_mapping", grid_mapping)

        return True
