import pytest


@pytest.mark.parametrize(
    "content,expected",
    [
        (1, 1),
    ],
)
def test_eval(content, expected):
    result = content
    assert result == expected, "{0} != {1}".format(result, expected)
