from __future__ import absolute_import

import numpy
from netCDF4 import Dataset
from numpy.ma import is_masked

from mpilot import params
from mpilot.commands import Command
from mpilot.utils import insure_fuzzy
from .exceptions import NoSuchVariable, InvalidPositiveData, InvalidFuzzyData

FUZZY_MIN = -1
FUZZY_MAX = 1


class EEMSRead(Command):
    """ Reads a variable from a file, converting floats to nearest int when necessary. """

    display_name = "Read"
    inputs = {
        "InFileName": params.PathParameter(must_exist=True),
        "InFieldName": params.StringParameter(),
        "MissingValue": params.NumberParameter(required=False),
        "DataType": params.DataTypeParameter(
            required=False,
            valid_types={
                "Float": numpy.float64,
                "Integer": numpy.int,
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
        data_type = kwargs.get("DataType", numpy.float64)

        with Dataset(kwargs["InFileName"], "r") as dataset:
            if kwargs["InFieldName"] not in dataset.variables:
                raise NoSuchVariable(path, variable_name, lineno=self.lineno)

        variable = dataset[variable_name]
        data = variable[:]

        if (
            self.arguments.get("DataType", "Float")
            in ("Positive Integer", "Positive Float")
            and data.min() < 0
        ):
            raise InvalidPositiveData(
                path, self.arguments["DataType"], lineno=self.lineno
            )

        if numpy.issubdtype(data.dtype, numpy.float) and data_type in (
            numpy.int,
            numpy.uint,
        ):
            data = numpy.rint(data, out=data)  # round in-place

        result = numpy.ma.array(
            data,
            mask=data.mask if is_masked(data) else False,
            dtype=data_type,
            fill_value=999999 if data_type in (numpy.int, numpy.uint) else None,
        )

        if self.arguments.get("DataType", "Float") == "Fuzzy":
            fuzzy_pad = 0.01 * (FUZZY_MAX - FUZZY_MIN)

            if data.max() > FUZZY_MAX + fuzzy_pad or data.min() < FUZZY_MIN - fuzzy_pad:
                raise InvalidFuzzyData(path, lineno=self.lineno)

            insure_fuzzy(result)

        result.soften_mask()

        # Mask missing values
        if "MissingValue" in kwargs:
            missing_value = (
                int(kwargs["MissingValue"])
                if numpy.issubdtype(result.mask.dtype, numpy.int)
                else float(kwargs["MissingValue"])
            )

            self.result.mask = numpy.where(
                result.data == missing_value, True, result.mask or False
            )

        result.data[result.mask] = result.fill_value

        return result


class EEMSWrite(Command):
    """ Writes one or more file """

    display_name = "Write"
    inputs = {
        "OutFileName": params.PathParameter(),
        "OutFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
        "DimensionFileName": params.PathParameter(must_exist=True),
        "DimensionFieldName": params.StringParameter(),
    }
    output = params.BooleanParameter()

    def execute(self, **kwargs):
        commands = kwargs["OutFieldNames"]
        arrays = [c.result for c in commands]
        self.validate_array_shapes(arrays)

        with Dataset(kwargs["OutFileName"], "w") as dataset:
            with Dataset(kwargs["DimensionsFileName"]) as dim_dataset:
                dimensions = dim_dataset[kwargs["DimensionFieldName"]].dimensions
                for dimension in dimensions:
                    in_variable = dim_dataset[dimension]
                    out_variable = dataset.createDimension(dimension, in_variable.size)

                    for attribute in dir(in_variable):
                        if attribute not in dir(out_variable) and attribute not in (
                            "_FillValue",
                            "missing_value",
                        ):
                            setattr(
                                out_variable, attribute, getattr(in_variable, attribute)
                            )
                    out_variable[:] = in_variable[:]

            mask = numpy.copy(arrays[0].mask)
            for arr in arrays[1:]:
                mask |= arr.mask

            for command in commands:
                variable = dataset.createVariable(
                    command.result_name,
                    command.result.dtype.char,
                    dimensions,
                    fill_value=command.result.fill_value,
                )
                variable[:] = numpy.ma.MaskedArray(command.result.data, mask)

        return True
