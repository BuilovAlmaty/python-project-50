from enum import Enum
from pathlib import Path

from gendiff.scripts.gendiff import load_file, generate_diff


class FileNames(Enum):
    JSON_INPUT_1 = "gendiff_input1.json"
    JSON_INPUT_2 = "gendiff_input2.json"
    YAML_INPUT_1 = "gendiff_input1.yaml"
    YAML_INPUT_2 = "gendiff_input2.yml"
    EMPTY_EXPECTED_1 = "gendiff_expected_file1_empty.txt"
    EMPTY_EXPECTED_2 = "gendiff_expected_file2_empty.txt"
    EMPTY_EXPECTED_PLAIN_2 = "gendiff_expected_plain_file2_empty.txt"
    EXPECTED = "gendiff_expected.txt"
    EXPECTED_REC = "gendiff_rec_expected.txt"
    EXPECTED_PLAIN = "gendiff_expected_plain.txt"
    JSON_INPUT_REC_1 = "gendiff_rec_input1.json"
    JSON_INPUT_REC_2 = "gendiff_rec_input2.json"
    YAML_INPUT_REC_1 = "gendiff_rec_input1.yaml"
    YAML_INPUT_REC_2 = "gendiff_rec_input2.yaml"


def test_empty_dictionaries(test_data):
    first_dict_json = test_data[FileNames.JSON_INPUT_1.value]
    second_dict_json = test_data[FileNames.JSON_INPUT_2.value]

    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    second_dict_yaml = test_data[FileNames.YAML_INPUT_2.value]

    first_dict_rec_yaml = test_data[FileNames.YAML_INPUT_REC_1.value]

    empty_expected_1 = test_data[FileNames.EMPTY_EXPECTED_1.value].strip()
    empty_expected_2 = test_data[FileNames.EMPTY_EXPECTED_2.value].strip()
    empty_expected_3 = test_data[FileNames.EMPTY_EXPECTED_PLAIN_2.value].strip()

    assert generate_diff({}, {}, "linear") == '{\n\n}'
    assert generate_diff({}, second_dict_json, "linear") == empty_expected_1
    assert generate_diff(first_dict_json, {}, "linear") == empty_expected_2
    assert generate_diff({}, second_dict_yaml) == empty_expected_1
    assert generate_diff(first_dict_rec_yaml, {}, "plain") == empty_expected_3


def test_recursive_expected_right_result(test_data):
    first_dict_json = test_data[FileNames.JSON_INPUT_REC_1.value]
    second_dict_json = test_data[FileNames.JSON_INPUT_REC_2.value]

    first_dict_yaml = test_data[FileNames.YAML_INPUT_REC_1.value]
    second_dict_yaml = test_data[FileNames.YAML_INPUT_REC_2.value]

    expected = test_data[FileNames.EXPECTED_REC.value].strip()
    expected_plain = test_data[FileNames.EXPECTED_PLAIN.value].strip()

    assert generate_diff(first_dict_json, second_dict_json) == expected
    assert generate_diff(first_dict_yaml, second_dict_yaml) == expected
    assert generate_diff(first_dict_json, second_dict_yaml, "plain") == expected_plain


def test_expected_right_result(test_data):
    first_dict_json = test_data[FileNames.JSON_INPUT_1.value]
    second_dict_json = test_data[FileNames.JSON_INPUT_2.value]

    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    second_dict_yaml = test_data[FileNames.YAML_INPUT_2.value]
    expected = test_data[FileNames.EXPECTED.value].strip()

    assert generate_diff(first_dict_json, second_dict_json, "linear") == expected
    assert generate_diff(first_dict_yaml, second_dict_yaml, "linear") == expected


def test_load_file(test_data):
    data_directory = Path(__file__).parent / "data"
    first_dict_yaml = test_data[FileNames.YAML_INPUT_1.value]
    assert load_file(
        data_directory / FileNames.YAML_INPUT_1.value
    ) == first_dict_yaml
