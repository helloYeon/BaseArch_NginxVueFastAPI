"""tests/services/test_http_external_service.py

・親クラスであるHttpExternalServiceを継承したHttpAuthenticateServiceとHttpAccessPointServiceのテストを行う。
・親クラスであるHttpExternalServiceのテストは行わない。
・実際のテストは、外部APIとの通信を行うため、pytest.mark.external_apiを付与している。
・実行する際はmake be-test-extで実行する。
"""

import json
import os
import subprocess
import zipfile
from datetime import datetime
from io import BytesIO
from typing import Callable, Optional

import pendulum
import pytest
import test_http_external_service_params as params
from enums import TransformDataType
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from services.http_access_point_service import HttpAccessPointService
from services.http_authenticate_service import HttpAuthenticateService

# see: https://www.selenium.dev/documentation/en/webdriver/driver_requirements/
# see: https://docs.google.com/spreadsheets/d/1HD46hp2TRLluQH1c0g3YUY43TsbBdg4GFdTjQIEpn0U/edit?gid=0#gid=0
TEST_UD = "witest4774@infosys.sakura.ne.jp"
TEST_PWD = "Test1234"
CHROME_PATH = "/usr/bin/chromium"


def create_save_dir() -> str:
    """保存先ディレクトリを作成してそのパスを返す"""
    save_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(save_dir, "storage", pendulum.now().format("YYYYMMDDHHmm"))
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


class UserSessionInfo(BaseModel):
    """BaseItem"""

    userId: Optional[int] = Field(default=None)
    esCompanyId: Optional[int] = Field(default=None)
    peppolId: Optional[str] = Field(default=None)
    apiId: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    authKey: Optional[str] = Field(default=None)
    xml: Optional[str] = Field(default=None)


@pytest.fixture(scope="session", autouse=False)
def shared_session() -> Callable[[], UserSessionInfo]:
    """テスト間で共有するデータを保持するための辞書"""
    session_info = UserSessionInfo()

    def _user_session() -> UserSessionInfo:
        return session_info

    return _user_session


@pytest.fixture
def http_authenticate_service() -> HttpAuthenticateService:
    """HttpAuthenticateServiceのインスタンスを返す"""
    return HttpAuthenticateService()


@pytest.fixture
def http_access_point_service() -> HttpAccessPointService:
    """HttpAccessPointServiceのインスタンスを返す"""
    return HttpAccessPointService()


@pytest.fixture(scope="module", autouse=False)
def get_session_id() -> str:
    """セッションIDを取得する"""
    # return "1"
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(
        service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options
    )

    driver.get("http://www1.awsinfomart.co.jp/scripts/logon.asp")
    # time.sleep(1)

    uid = driver.find_element(By.NAME, "UID")
    pwd = driver.find_element(By.NAME, "PWD")

    uid.clear()
    pwd.clear()

    uid.send_keys(TEST_UD)
    pwd.send_keys(TEST_PWD)

    uid.submit()
    # time.sleep(1)

    cookies = driver.get_cookies()

    target_cookie_name = "cookies%5Fcomputer%5Fes"

    session_info = next(
        (cookie for cookie in cookies if cookie["name"] == target_cookie_name), None
    )

    return session_info["value"] if session_info is not None else ""


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_session_verified()
)
@pytest.mark.external_api
def test_get_session_verified(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    get_session_id: str,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 31. セッション検証API

    Test for HttpAuthenticateService.get_session_verified function.
    """
    result = http_authenticate_service.get_session_verified(
        session_id=get_session_id
    ).send(
        json={"ipAddress": ("39.110.235.25")}
    )  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"

    # ユーザー情報を保持
    session_info = shared_session()
    session_info.userId = int(response_data["userId"])
    session_info.esCompanyId = int(response_data["esCompanyId"])


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_user_info()
)
@pytest.mark.external_api
def test_get_user_info(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 40. ユーザー情報取得API

    Test for HttpAuthenticateService.test_get_user_info function.
    """
    session_info = shared_session()
    assert session_info.userId is not None, "Missing userId"

    result = http_authenticate_service.get_user_info(
        user_id=session_info.userId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_service_activation()
)
@pytest.mark.external_api
def test_get_service_activation(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 41. サービスアクティベーション情報取得API

    Test for HttpAuthenticateService.get_service_activation function.
    """
    session_info = shared_session()
    assert session_info.esCompanyId is not None, "Missing esCompanyId"

    result = http_authenticate_service.get_service_activation(
        es_company_id=session_info.esCompanyId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_option_activation()
)
@pytest.mark.external_api
def test_get_option_activation(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 42. オプションアクティベーション情報取得API

    Test for HttpAuthenticateService.get_option_activation function.
    """
    session_info = shared_session()
    assert session_info.esCompanyId is not None, "Missing esCompanyId"

    result = http_authenticate_service.get_option_activation(
        es_company_id=session_info.esCompanyId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_company_info()
)
@pytest.mark.external_api
def test_get_company_info(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 50. 企業情報取得API

    Test for HttpAuthenticateService.get_company_info function.
    """
    session_info = shared_session()
    assert session_info.esCompanyId is not None, "Missing esCompanyId"

    result = http_authenticate_service.get_company_info(
        es_company_id=session_info.esCompanyId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_peppol_id_mapping_info()
)
@pytest.mark.external_api
def test_get_peppol_id_mapping_info(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 100. 企業・Peppol ID紐づけ情報取得API

    Test for HttpAuthenticateService.get_peppol_id_mapping_info function.
    """
    session_info = shared_session()
    assert session_info.esCompanyId is not None, "Missing esCompanyId"

    result = http_authenticate_service.get_peppol_id_mapping_info(
        es_company_id=session_info.esCompanyId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"

    session_info.peppolId = response_data["peppolId"]


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_peppol_id_related_info()
)
@pytest.mark.external_api
def test_get_peppol_id_related_info(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 110. Peppol ID情報取得API

    Test for HttpAuthenticateService.get_peppol_id_related_info function.
    """
    session_info = shared_session()
    assert session_info.peppolId is not None, "Missing peppolId"

    result = http_authenticate_service.get_peppol_id_related_info(
        icd_code=session_info.peppolId.split(":")[0],
        corporate_number=session_info.peppolId.split(":")[1],
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()
    for field in expected_fields:
        assert field in response_data, f"Missing field: {field}"

    session_info.apiId = response_data["apiId"]
    session_info.password = response_data["password"]
    session_info.authKey = response_data["authKey"]


@pytest.mark.parametrize(
    "expected_status, expected_fields", params.test_get_bulk_user_info()
)
@pytest.mark.external_api
def test_get_bulk_user_info(
    expected_status,
    expected_fields,
    http_authenticate_service: HttpAuthenticateService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[認証] 200. ユーザー情報一括取得API

    Test for HttpAuthenticateService.get_bulk_user_info function.
    """
    session_info = shared_session()
    assert session_info.esCompanyId is not None, "Missing esCompanyId"

    result = http_authenticate_service.get_bulk_user_info(
        es_company_id=session_info.esCompanyId
    ).send()  # type: ignore

    response = result.get_response()
    assert response.status_code == expected_status

    response_data = response.json()

    for user in response_data.get("users", []):
        for field in expected_fields:
            assert field in user, f"Missing field: {field} in user: {user}"


@pytest.mark.parametrize(
    "expected_status, expected_content_type", params.test_post_receive()
)
@pytest.mark.external_api
def test_post_receive(
    expected_status,
    expected_content_type,
    http_access_point_service: HttpAccessPointService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[受取] 1. API_アクセスポイント連携（受取）API

    Test for HttpAccessPointService.post_receive function.
    """
    session_info = shared_session()
    assert session_info.apiId is not None, "Missing apiId"
    assert session_info.password is not None, "Missing password"
    assert session_info.authKey is not None, "Missing authKey"

    result = http_access_point_service.post_receive().send(
        json={
            "peppol_api_id": session_info.apiId,
            "peppol_password": session_info.password,
            "authentication_key": session_info.authKey,
            "gettime_from": "202001020304",
            "gettime_to": "202301020304",
        },
    )  # type: ignore

    response = result.get_response()

    assert response.status_code == expected_status
    assert response.headers["Content-Type"] == expected_content_type
    assert response.content is not None

    # response.content が bytes であることを保証
    if isinstance(response.content, bytes):
        # 保存先ディレクトリを作成
        save_dir = create_save_dir()

        # ZIPファイルを保存
        zip_path = os.path.join(save_dir, "response.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # ZIPを解凍
        result = subprocess.run(
            ["unzip", "-o", zip_path, "-d", save_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
        )

        zip_content = response.content
        with zipfile.ZipFile(BytesIO(zip_content)) as zf:
            file_info = zf.infolist()[0]

            with zf.open(file_info) as file:
                session_info.xml = file.read().decode("utf-8")


@pytest.mark.parametrize(
    "expected_status, expected_content_type", params.test_post_transform()
)
@pytest.mark.external_api
def test_post_transform(
    expected_status,
    expected_content_type,
    http_access_point_service: HttpAccessPointService,
    shared_session: Callable[[], UserSessionInfo],
) -> None:
    """[受取] 2. 請求書・通知書データ変換(受取)API

    Test for HttpAccessPointService.post_receive function.
    """
    session_info = shared_session()
    assert session_info.xml is not None, "Missing xml"

    result = http_access_point_service.post_transform().send(
        json={
            "peppol_format_data_list": [
                {"data_type": TransformDataType.SELF_BILLING, "data": session_info.xml}
            ]
        }
    )  # type: ignore

    response = result.get_response()

    assert response.content is not None

    # JSONを読み込んでデコード
    # response.contentを文字列に変換してJSONをデコード
    response_data = json.loads(bytes(response.content).decode("utf-8"))
    decoded_response = json.dumps(response_data, ensure_ascii=False)

    # 保存先ディレクトリを作成
    save_dir = create_save_dir()

    # 送信したXMLを保存
    xml_path = os.path.join(save_dir, "sent_xml.xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(session_info.xml)

    # レスポンスされたJSONを保存
    json_path = os.path.join(save_dir, "response.json")
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(decoded_response)

    assert response.status_code == expected_status
    assert response.headers["Content-Type"] == expected_content_type
