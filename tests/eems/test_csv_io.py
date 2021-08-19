from __future__ import division

import pytest
import six

from mpilot.libraries.eems.exceptions import InvalidDataFile

if six.PY3:
    from unittest.mock import mock_open, patch
else:
    from mock import mock_open, patch

from mpilot.libraries.eems.csv.io import EEMSRead


def test_read_empty_field():
    mock = mock_open(read_data="a,b,c\n1,2,3\n4,,6")

    with patch("mpilot.libraries.eems.csv.io.open", mock):
        with pytest.raises(InvalidDataFile) as ex:
            EEMSRead("ReadResult").execute(InFileName="test.csv", InFieldName="b")

    assert 'in the field "b" on line 3' in str(ex)
