from gendiff.scripts.gendiff import generate_diff

def test_empty_dictionaries(load_json_txt):
    assert generate_diff({}, {}) == ''

    first_dict = load_json_txt("gendiff_input1.json")
    second_dict = load_json_txt("gendiff_input2.json")
    expected1 = load_json_txt("gendiff_expected_file1_empty.txt").strip()
    expected2 = load_json_txt("gendiff_expected_file2_empty.txt").strip()
    assert generate_diff({}, second_dict) == expected1
    assert generate_diff(first_dict, {}) == expected2

def test_expected_right_result(load_json_txt):
    first_dict = load_json_txt("gendiff_input1.json")
    second_dict = load_json_txt("gendiff_input2.json")
    expected = load_json_txt("gendiff_expected.txt").strip()

    assert generate_diff(first_dict, second_dict) == expected
