import pytest

from multion.client import MultiOn

# Get started with writing tests with pytest at https://docs.pytest.org
# @pytest.mark.skip(reason="Unimplemented")
def test_client() -> None:
    assert True == True
    mu = MultiOn()
    mu.browse(cmd="ls", url="https://www.google.com", use_proxy=True)