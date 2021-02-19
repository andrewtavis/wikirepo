"""
Utilities Tests
---------------
"""

import pytest

from wikirepo import utils


def test__make_var_list():
    assert utils._make_var_list("word") == (["word"], True)


def test__return_given_type():
    assert utils._return_given_type(["word"], var_was_str=False) == ["word"]
    assert utils._return_given_type(["word"], var_was_str=True) == "word"
    assert utils._return_given_type(["word_0", "word_1"], var_was_str=True) == [
        "word_0",
        "word_1",
    ]


def test_try_float():
    assert utils.try_float("1.0") == 1.0
    assert utils.try_float("word") == "word"


def test_round_if_int():
    assert utils.round_if_int(1.0) == 1
    assert utils.round_if_int(1.5) == 1.5


def test_gen_list_of_lists():
    test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert utils.gen_list_of_lists(
        original_list=test_list, new_structure=[3, 3, 3]
    ) == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_check_str_similarity():
    assert utils.check_str_similarity("word", "word") == 1


def test_check_str_args():
    assert utils.check_str_args("word_0", ["word_0", "word_1"]) == "word_0"
    assert utils.check_str_args(["word_0", "word_1"], ["word_0", "word_1"]) == [
        "word_0",
        "word_1",
    ]
    with pytest.raises(ValueError):
        utils.check_str_args("word_2", ["word_0", "word_1"])
