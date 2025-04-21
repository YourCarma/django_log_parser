from pathlib import Path
import pytest

from main import main


filepath = Path(__file__).parent.joinpath("test.log")
def test_pipeline():
    with pytest.raises(TypeError):
        main(filepath)
    filepaths = [filepath]
    main(filepaths)
    main(filepaths, "TEST_REPORT")
        