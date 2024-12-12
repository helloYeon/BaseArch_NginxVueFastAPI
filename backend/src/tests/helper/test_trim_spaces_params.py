"""tests/helpers/test_trim_spaces_params.py"""


def test_trim_spaces() -> list[tuple[str | None, str | None]]:
    """trim_spacesテスト"""
    return [
        # case 1: 空文字の場合
        ("", ""),
        # case 2: Noneの場合
        (None, None),
        # case 3: 半角スペースのみの場合
        (" ", ""),
        # case 4: 全角スペースのみの場合
        ("　", ""),
        # case 5: 半角スペースが含まれる場合
        (" value ", "value"),
        # case 6: 全角スペースが含まれる場合
        ("　value　", "value"),
    ]
