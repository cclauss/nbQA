"""Check :code:`isort` works as intended."""

import difflib
import os
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from nbqa.__main__ import main

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture


def test_isort_works(
    tmp_notebook_for_testing: "Path", capsys: "CaptureFixture"
) -> None:
    """
    Check isort works.

    Parameters
    ----------
    tmp_notebook_for_testing
        Temporary copy of :code:`notebook_for_testing.ipynb`.
    capsys
        Pytest fixture to capture stdout and stderr.
    """
    # check diff
    with open(tmp_notebook_for_testing, "r") as handle:
        before = handle.readlines()
    path = os.path.abspath(os.path.join("tests", "data", "notebook_for_testing.ipynb"))
    with pytest.raises(SystemExit):
        main(["isort", path, "--nbqa-mutate"])

    with open(tmp_notebook_for_testing, "r") as handle:
        after = handle.readlines()
    diff = difflib.unified_diff(before, after)
    result = "".join([i for i in diff if any([i.startswith("+ "), i.startswith("- ")])])
    expected = '+    "import glob\\n",\n-    "\\n",\n-    "import glob\\n",\n'
    assert result == expected

    # check out and err
    out, err = capsys.readouterr()
    expected_out = f"Fixing {path}{os.linesep}"
    expected_err = ""
    assert out == expected_out
    assert err == expected_err


def test_isort_initial_md(
    tmp_notebook_starting_with_md: "Path", capsys: "CaptureFixture"
) -> None:
    """
    Check isort works when a notebook starts with a markdown cell.

    Parameters
    ----------
    tmp_notebook_starting_with_md
        Temporary copy of :code:`notebook_for_testing.ipynb`.
    capsys
        Pytest fixture to capture stdout and stderr.
    """
    # check diff
    with open(tmp_notebook_starting_with_md, "r") as handle:
        before = handle.readlines()
    path = os.path.abspath(
        os.path.join("tests", "data", "notebook_starting_with_md.ipynb")
    )
    with pytest.raises(SystemExit):
        main(["isort", path, "--nbqa-mutate"])

    with open(tmp_notebook_starting_with_md, "r") as handle:
        after = handle.readlines()
    diff = difflib.unified_diff(before, after)
    result = "".join([i for i in diff if any([i.startswith("+ "), i.startswith("- ")])])
    expected = '+    "import glob\\n",\n-    "\\n",\n-    "import glob\\n",\n'
    assert result == expected

    # check out and err
    out, err = capsys.readouterr()
    expected_out = f"Fixing {path}{os.linesep}"
    expected_err = ""
    assert out == expected_out
    assert err == expected_err


def test_isort_separated_imports(capsys: "CaptureFixture") -> None:
    """
    Check isort works when a notebook has imports in different cells.

    We will pass --treat-comment-as-code '# %%'.

    Parameters
    ----------
    tmp_notebook_starting_with_md
        Temporary copy of :code:`notebook_for_testing.ipynb`.
    capsys
        Pytest fixture to capture stdout and stderr.
    """
    with open(".nbqa.ini", "w") as handle:
        handle.write(
            dedent(
                """\
            [isort]
            addopts = --treat-comment-as-code "# %%%%"
            """
            )
        )

    path = os.path.abspath(
        os.path.join("tests", "data", "notebook_with_separated_imports.ipynb")
    )
    with pytest.raises(SystemExit):
        main(["isort", path, "--nbqa-mutate"])

    Path(".nbqa.ini").unlink()

    # check out and err
    out, err = capsys.readouterr()
    expected_out = ""
    expected_err = ""
    assert out == expected_out
    assert err == expected_err
