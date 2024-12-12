"""tests/services/test_admin_service_params.py"""

from api.v1.schemas.admin.access import BaseItem, PostRequest
from core.message import messages
from database import TestSessionLocal
from db.factories import UserAccessControlFactory
from enums import Access
from exceptions import PeppolHttpException
from models import UserAccessControl


def test_fetch_bulk_user_info() -> list[tuple[int, list, list, list]]:
    """_fetch_bulk_user_infoテストパラメータ"""
    # 230件のユーザーデータを作成
    template = {
        "userId": 1,
        "loginId": "t.test1@example.com",
        "lastName": "アドグローブ",
        "firstName": "1",
        "esCompanyId": 2,
        "createDate": "2024-02-01T18:01:40+09:00",
        "updateDate": "2024-02-01T18:01:51+09:00",
    }
    dictionaries = []
    for i in range(1, 231):
        new_dict = template.copy()
        new_dict["userId"] = i
        new_dict["loginId"] = f"t.test{i}@example.com"
        new_dict["firstName"] = str(i)
        dictionaries.append(new_dict)

    return [
        # case 1 : ユーザー情報1件の場合
        (
            1,
            [],
            [
                {
                    "users": [
                        {
                            "userId": 1,
                            "loginId": "t.test1@example.com",
                            "lastName": "インフォマート様",
                            "firstName": "確認用",
                            "esCompanyId": 1,
                            "createDate": "2024-02-01T18:01:40+09:00",
                            "updateDate": "2024-02-01T18:01:51+09:00",
                        }
                    ],
                    "offset": 1,
                    "limit": 100,
                    "totalCount": 1,
                }
            ],
            [
                {
                    "userId": 1,
                    "loginId": "t.test1@example.com",
                    "lastName": "インフォマート様",
                    "firstName": "確認用",
                    "esCompanyId": 1,
                    "createDate": "2024-02-01T18:01:40+09:00",
                    "updateDate": "2024-02-01T18:01:51+09:00",
                }
            ],
        ),
        # case 2 : ユーザー情報230件の場合
        (
            1,
            [],
            [
                {
                    "users": dictionaries[0:100],
                    "offset": 1,
                    "limit": 100,
                    "totalCount": 230,
                },
                {
                    "users": dictionaries[100:200],
                    "offset": 101,
                    "limit": 100,
                    "totalCount": 230,
                },
                {
                    "users": dictionaries[200:230],
                    "offset": 201,
                    "limit": 100,
                    "totalCount": 230,
                },
            ],
            dictionaries,
        ),
    ]


def test_get_admin_access_setting() -> list[tuple[int, list[BaseItem]]]:
    """get_admin_access_settingテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    user_access_control = UserAccessControlFactory(esCompanyId=1)
    session.add(user_access_control)
    session.commit()

    return [
        # case 1 : esCompanyIdが1のユーザーアクセス情報一覧が存在
        (
            1,
            [
                BaseItem(
                    esCompanyId=user_access_control.esCompanyId,
                    userId=user_access_control.userId,
                    isDeny=user_access_control.isDeny,
                    lastName=user_access_control.lastName,
                    firstName=user_access_control.firstName,
                    loginId=user_access_control.loginId,
                ),
            ],
        ),
    ]


def test_post_admin_access_setting() -> (
    list[tuple[PostRequest, int, UserAccessControl]]
):
    """post_admin_access_settingテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    user_access_control = UserAccessControlFactory(
        esCompanyId=1,
        isDeny=Access.IS_DENY,
        lastName="unittestLastName",
        firstName="unittestFirstName",
        userId=1,
    )
    session.add(user_access_control)
    session.commit()

    update_user_access_control = UserAccessControlFactory(
        esCompanyId=1,
        userId=2,
        isDeny=Access.IS_ALLOW,
        lastName="updateLastName",
        firstName="updateFirstName",
        loginId="2",
    )

    return [
        # case 1 : 存在しているデータに意図通り更新されていることを確認
        (
            PostRequest(
                data=[
                    BaseItem(
                        esCompanyId=update_user_access_control.esCompanyId,
                        userId=update_user_access_control.userId,
                        isDeny=update_user_access_control.isDeny,
                        lastName=update_user_access_control.lastName,
                        firstName=update_user_access_control.firstName,
                        loginId=update_user_access_control.loginId,
                    )
                ]
            ),
            1,
            update_user_access_control,
        ),
    ]


def test_raise_get_bulk_user_info_error() -> list[tuple[dict]]:
    """raise_get_bulk_user_info_errorテストパラメータ"""
    return [
        # case 1 : ユーザー情報一括取得APIエラー
        (
            {
                "exception": PeppolHttpException,
                "message": messages.FAILED_GET_USERS_DATA_MESSAGE.message,
            },
        ),
    ]
