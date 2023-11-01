import pytest
from string import ascii_uppercase, ascii_lowercase
from main import main


@pytest.mark.parametrize("letter", ascii_uppercase + ascii_lowercase)
def test_main(letter, snapshot) -> None:
    assert main(letter) == snapshot


@pytest.mark.parametrize("letter", ascii_uppercase + ascii_lowercase)
def test_prout(letter):
    assert main(main(letter)) == letter.upper()
