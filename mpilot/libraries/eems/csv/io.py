from __future__ import absolute_import

import csv

import numpy

from mpilot import params
from mpilot.commands import Command
from mpilot.libraries.eems.exceptions import EmptyDataFile, InvalidDataFile
from mpilot.libraries.eems.mixins import SameArrayShapeMixin


class EEMSRead(Command):
    """Reads a variable from a file"""

    display_name = "Read"
    inputs = {
        "InFileName": params.PathParameter(must_exist=True),
        "InFieldName": params.StringParameter(),
        "ReturnType": params.DataTypeParameter(required=False),  # Not used
        "NewFieldName": params.StringParameter(required=False),  # Not used
        "MissingVal": params.NumberParameter(required=False),
        "DataType": params.DataTypeParameter(
            required=False, valid_types={"Float": float, "Integer": int}
        ),
    }
    output = params.DataParameter()

    def execute(self, **kwargs):
        path = kwargs["InFileName"]

        with open(path, "r") as f:
            reader = csv.reader(f.readlines())

            try:
                headers = next(reader)
            except StopIteration:
                raise EmptyDataFile(path)

            field_name = kwargs["InFieldName"]
            try:
                idx = headers.index(field_name)
            except ValueError:
                raise InvalidDataFile(
                    "The data file doesn't contain the header {}: {}".format(
                        field_name, path
                    )
                )

            values = []
            for i, row in enumerate(reader):
                if row:
                    try:
                        values.append(float(row[idx]))
                    except ValueError:
                        raise InvalidDataFile(
                            'The data file contains an invalid value in the field "{}" on line {}.'.format(
                                field_name, i + 2
                            ),
                            solution="Verify that the data file doesn't contain any empty or NULL values, and that all values are numeric.",
                        )

        fill_value = kwargs.get("MissingVal")
        data_type = kwargs.get("DataType", float)
        if fill_value is not None:
            data = numpy.ma.array(
                values, mask=False, dtype=data_type, fill_value=data_type(fill_value)
            )
            mask = numpy.ma.where(data == data_type(fill_value), True, False)

        data = numpy.ma.array(values, mask=False, dtype=data_type)
        data.soften_mask()

        if fill_value is not None:
            data.mask = mask

        return data


class EEMSWrite(SameArrayShapeMixin, Command):
    display_name = "Write"
    inputs = {
        "OutFileName": params.PathParameter(must_exist=False),
        "OutFieldNames": params.ListParameter(
            params.ResultParameter(params.DataParameter())
        ),
    }

    def execute(self, **kwargs):
        commands = kwargs["OutFieldNames"]
        arrays = [c.result for c in commands]
        self.validate_array_shapes(arrays)

        with open(kwargs["OutFileName"], "w") as f:
            writer = csv.writer(f, lineterminator="\n")

            # Write headers
            writer.writerow([c.result_name for c in commands])

            # Assumption: 1d arrays
            out_arr = numpy.ma.array(arrays)
            out_arr = out_arr.transpose([1, 0])

            writer.writerows(out_arr[i, :] for i in range(out_arr.shape[0]))
