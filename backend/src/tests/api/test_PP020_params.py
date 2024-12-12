"""tests/api/test_PP020_params.py"""

import api.v1.schemas.users.me as me_schema
from enums.csv_download_type import CsvDownloadType

test_PP020 = [
    # case 1 : ログインユーザーを正常に返却
    (
        me_schema.ItemResponse(
            payload=me_schema.BaseItem(
                userId=1,
                sessionId="1",
                companyInfosId=1,
                lastName="unit",
                firstName="test",
                csvDownloadType=CsvDownloadType.CREATING_YOUR_OWN_INVOICE,
            )
        ).model_dump(mode="json")
    ),
]
