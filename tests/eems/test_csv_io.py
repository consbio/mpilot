from __future__ import division

import numpy
import pytest
import six

from mpilot.libraries.eems.exceptions import InvalidDataFile
from tests.utils import create_command_with_result

if six.PY3:
    from unittest.mock import mock_open, patch, call
else:
    from mock import mock_open, patch, call

from mpilot.libraries.eems.csv.io import EEMSRead, EEMSWrite


def test_eems_write():
    a_command = create_command_with_result("AResult", numpy.ma.masked_array([1, 2, 3]))
    mock = mock_open()

    with patch("mpilot.libraries.eems.csv.io.open", mock):
        EEMSWrite("WriteResult").execute(
            OutFileName="test.csv", OutFieldNames=[a_command]
        )

        mock.assert_has_calls([call("test.csv", "w")])
        mock().write.assert_has_calls(
            [call("AResult\n"), call("1\n"), call("2\n"), call("3\n")]
        )


def test_read_empty_field():
    mock = mock_open(read_data="a,b,c\n1,2,3\n4,,6")

    with patch("mpilot.libraries.eems.csv.io.open", mock):
        with pytest.raises(InvalidDataFile) as ex:
            EEMSRead("ReadResult").execute(InFileName="test.csv", InFieldName="b")

    assert 'in the field "b" on line 3' in str(ex)
