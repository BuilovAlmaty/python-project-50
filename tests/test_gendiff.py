from enum import Enum
from pathlib import Path

from gendiff.parsing_engine import generate_linear_diff
from gendiff.scripts.gendiff import load_file


class FileNames(Enum):
    JSON_INPUT_1 = "gendiff_input1.json"
    JSON_INPUT_2 = "gendiff_input2.json"
    YAML_INPUT_1 = "gendiff_input1.yaml"
    YAML_INPUT_2 = "gendiff_input2.yml"
    EMPTY_EXPECTED_1 = "gendiff_expected_file1_empty.txt"
    EMPTY_EXPECTED_2 = "gendiff_expected_file2_empty.txt"
    EXPECTED = "gendiff_expected.txt"


def test_empty_dictionaries(test_data):
    assert generate_linear_diff({}, {}) == ''

    first_dict_json = test_data[FileNames.JSON_INPUT_1.value]
    second_dict_json = test_data[FileNames.JSON_INPUT_2.value]

    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    second_dict_yaml = test_data[FileNames.YAML_INPUT_2.value]

    empty_expected_1 = test_data[FileNames.EMPTY_EXPECTED_1.value].strip()
    empty_expected_2 = test_data[FileNames.EMPTY_EXPECTED_2.value].strip()

    assert generate_linear_diff({}, second_dict_json) == empty_expected_1
    assert generate_linear_diff(first_dict_json, {}) == empty_expected_2
    assert generate_linear_diff({}, second_dict_yaml) == empty_expected_1
    assert generate_linear_diff(first_dict_yaml, {}) == empty_expected_2


def test_expected_right_result(test_data):
    first_dict_json = test_data[FileNames.JSON_INPUT_1.value]
    second_dict_json = test_data[FileNames.JSON_INPUT_2.value]

    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    second_dict_yaml = test_data[FileNames.YAML_INPUT_2.value]

    expected = test_data[FileNames.EXPECTED.value].strip()

    assert generate_linear_diff(first_dict_json, second_dict_json) == expected
    assert generate_linear_diff(first_dict_yaml, second_dict_yaml) == expected


def test_load_file(test_data):
    data_directory = Path(__file__).parent / "data"
    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    assert load_file(
        data_directory / FileNames.YAML_INPUT_1.value
    ) == first_dict_yaml
