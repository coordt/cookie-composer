"""
Methods for merging data files.

The merging functions should look similar to the following:

::

    def merge_generic_files(origin: Path, destination: Path, merge_strategy: MergeStrategy):
        '''
        Merge two ??? files into one.

        Raises:
            MergeError: If something goes wrong

        Args:
            origin: The path to the data file to merge
            destination: The path to the data file to merge into and write out.
            merge_strategy: How to do the merge
        '''

The function must write the file to destination.

The function must wrap any errors into a MergeError and raise it.
"""
from typing import Callable, Dict

from pathlib import Path

from cookie_composer.composition import MergeStrategy
from cookie_composer.merge_files.json_file import merge_json_files
from cookie_composer.merge_files.yaml_file import merge_yaml_files

merge_function = Callable[[Path, Path, MergeStrategy], None]

MERGE_FUNCTIONS: Dict[str, merge_function] = {
    ".json": merge_json_files,
    ".yaml": merge_yaml_files,
    ".yml": merge_yaml_files,
}