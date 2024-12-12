"""tests/services/test_base_service_params.py"""

import os

from core.constant import const

test_remove_none_values = [
    # case 1 : 文字列の場合
    ("a", "a"),
    # case 2 : 配列の場合
    ([None, "a", None, "1", 111, None], ["a", "1", 111]),
    # case 3 : 辞書の場合
    ({"a": None}, {}),
    # case 4 : 混合の場合
    (
        {
            "a": 1,
            "b": None,
            "c": {"d": 2, "e": None, "f": [3, None, {"g": 4, "h": None}]},
            "d": [{"aaa": None}, None, 1],
        },
        {
            "a": 1,
            "c": {"d": 2, "f": [3, {"g": 4}]},
            "d": [{}, 1],
        },
    ),
]

test_unzip_with_subprocess = [
    # case 1 : 成功する場合
    (
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../storage/for_test/receive.zip",
        ),
        "/1",
        const.PROC_RESULT_SUCCESS,
    ),
    # case 1 : zipファイルが存在しない場合
    (
        "not_found.zip",
        "/2",
        const.PROC_RESULT_FAILED,
    ),
]
