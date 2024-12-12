"""tests/services/test_receive_params.py"""

import os

from core.constant import const
from database import TestSessionLocal
from db.factories import (
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
)
from enums import ReceiveRecordStatus
from models import CompanyInfo, MstPpolItem
from services.http_access_point_service import HttpAccessPointService


def test_xml_data_transform_request() -> list[tuple[str, int | dict]]:
    """xml_data_transform_requestテストパラメータ"""
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../storage/for_test/base_standard_invoices_data_1.xml",
        ),
        mode="r",
        encoding="UTF-8",
    ) as file:
        xml = file.read()

    return [
        # case 1 : 変換可能なxml
        (xml, {"mocked_data": "response"}),
        # case 2 : 変換不可能なxml
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <test>
                test
            </test>""",
            const.PROC_RESULT_FAILED,
        ),
    ]


def test_xml_data_transform_request_exception() -> list:
    """xml_data_transform_request例外テストパラメータ"""
    return []


def test_condition_check() -> list[tuple[list, str, list]]:
    """condition_checkテストパラメータ"""
    return [
        # case 1 : 条件に合致するデータが存在
        (
            [
                {
                    "cbc:ID": {"schemeID": "ABT", "value": "DR35141"},
                    "cbc:DocumentTypeCode": {"value": "130"},
                },
                {
                    "cbc:ID": {"value": "testDoc1"},
                    "cbc:DocumentDescription": {"value": "試験用の添付書類"},
                    "cac:Attachment": {
                        "cbc:EmbeddedDocumentBinaryObject": {
                            "filename": "test.txt",
                            "mimeCode": "text/plain",
                            "value": "dGhpcyUyMGlzJTIwYSUyMHRlc3QlMjB0ZXh0",
                        },
                        "cac:ExternalReference": {
                            "cbc:URI": {
                                "value": "http://www.example.com/summary001.html"
                            }
                        },
                    },
                },
                {
                    "cbc:ID": {"value": "testDoc2"},
                    "cbc:DocumentDescription": {"value": "Usage breakdown"},
                    "cac:Attachment": {
                        "cac:ExternalReference": {
                            "cbc:URI": {
                                "value": "http://www.example.com/breakdown001.html"
                            }
                        }
                    },
                },
            ],
            "AUTO-8",
            [
                {
                    "cbc:ID": {"schemeID": "ABT", "value": "DR35141"},
                    "cbc:DocumentTypeCode": {"value": "130"},
                }
            ],
        ),
        # case 1 : 条件に合致しないデータが存在しない
        ([], "", []),
    ]


def test_condition_check_exception() -> list:
    """condition_check例外テストパラメータ"""
    return []


def test_make_btid_item() -> list[tuple[MstPpolItem, dict[str, str], str, str]]:
    """make_btid_itemテストパラメータ"""
    return [
        # case 1 : 整形できるデータ
        (
            MstPpolItem(
                id=1,
                parentSortOrder=0,
                btId="IBT-024",
                nameEn="CustomizationID",
                nameJp="ビジネスプロセスタイプ",
                nameFull="cbc:CustomizationID",
                condition=None,
                sortOrder=1,
                isExistData=1,
                type=1,
                model=1,
            ),
            {"value": "urn:peppol:pint:billing-1@jp-1"},
            "cbc:CustomizationID",
            "urn:peppol:pint:billing-1@jp-1",
        )
    ]


def test_make_btid_item_exception() -> list:
    """make_btid_item例外テストパラメータ"""
    return []


def test_get_filter_mst_ppol_item() -> list[tuple[str, int, list[MstPpolItem]]]:
    """make_get_filter_mst_ppol_itemテストパラメータ"""
    return [
        # case 1 : 条件に合致するデータが存在
        (
            "cbc:CustomizationID",
            0,
            [
                MstPpolItem(
                    id=1,
                    parentSortOrder=0,
                    btId="IBT-024",
                    nameEn="CustomizationID",
                    nameJp="ビジネスプロセスタイプ",
                    nameFull="cbc:CustomizationID",
                    condition=None,
                    sortOrder=1,
                    isExistData=1,
                    type=1,
                    model=1,
                )
            ],
        ),
        # case 2 : 条件に合致するデータが存在しない
        (
            "test",
            999,
            [],
        ),
    ]


def test_get_filter_mst_ppol_item_exception() -> list:
    """get_filter_mst_ppol_item例外テストパラメータ"""
    return []


def test_deep_dict_shaping() -> (
    list[tuple[dict[str, dict[str, str]], int, str, dict[str, str]]]
):
    """deep_dict_shapingテストパラメータ"""
    return [
        # case 1 : 変換可能なデータ
        (
            {
                "cbc:StartDate": {"value": "2024-01-18"},
                "cbc:EndDate": {"value": "2024-03-31"},
                "cbc:DescriptionCode": {"value": "3"},
            },
            14,
            "cac:InvoicePeriod_",
            {"IBT-073": "2024-01-18", "IBT-074": "2024-03-31", "IBT-008": "3"},
        )
    ]


def test_deep_dict_shaping_exception() -> list:
    """deep_dict_shaping例外テストパラメータ"""
    return []


def test_create_data_for_insertion() -> list[tuple[dict, list, dict, str, int]]:
    """create_data_for_insertionテストパラメータ"""
    return [
        # # case 1 : 登録可能なデータ
        (
            {
                "IBT-024": "urn:peppol:pint:billing-1@jp-1",
                "IBT-023": "urn:peppol:bis:billing",
                "IBT-001": "3",
                "IBT-002": "2024-03-10",
                "IBT-168": "10:00:15",
                "IBT-009": "2024-04-25",
                "IBT-003": "380",
                "IBT-022": "試験用の請求書です",
                "IBT-007": "2024-03-25",
                "IBT-005": "USD",
                "IBT-006": "USD",
                "IBT-019": "4217:2323:2323",
                "IBT-010": "0150abc",
                "IBG-14": {
                    "IBT-073": "2024-01-18",
                    "IBT-074": "2024-03-31",
                    "IBT-008": "3",
                },
                "AUTO-2": {"IBT-013": "O-998877", "IBT-014": "SO-12345"},
                "IBG-03": [{"AUTO-3": {"IBT-025": "123", "IBT-026": "2024-02-25"}}],
                "AUTO-4": {"IBT-016": "desp98"},
                "AUTO-5": {"IBT-015": "resp-1"},
                "AUTO-6": {"IBT-017": "ppid-123"},
                "AUTO-7": {"IBT-012": "contract1"},
                "AUTO-8": {
                    "IBT-018": {"schemeID": "ABT", "value": "DR35141"},
                    "AUTO-9": "130",
                },
                "IBG-24": [
                    {
                        "IBT-122": "testDoc1",
                        "IBT-123": "試験用の添付書類",
                        "AUTO-10": {
                            "IBT-125": {
                                "filename": "test.txt",
                                "mimeCode": "text/plain",
                                "value": "dGhpcyUyMGlzJTIwYSUyMHRlc3QlMjB0ZXh0",
                            },
                            "AUTO-11": {
                                "IBT-124": "http://www.example.com/summary001.html"
                            },
                        },
                    },
                    {
                        "IBT-122": "testDoc2",
                        "IBT-123": "Usage breakdown",
                        "AUTO-10": {
                            "AUTO-11": {
                                "IBT-124": "http://www.example.com/breakdown001.html"
                            }
                        },
                    },
                ],
                "AUTO-12": {"IBT-011": "PID1"},
                "IBG-04": {
                    "AUTO-13": {
                        "IBT-034": {"schemeID": "0188", "value": "1234567890123"},
                        "AUTO-14": [
                            {
                                "IBT-029": {
                                    "schemeID": "0147",
                                    "value": "123456:000123:0147:1",
                                }
                            }
                        ],
                        "AUTO-17": {"IBT-028": "株式会社 テスト売り手商事"},
                        "IBG-05": {
                            "IBT-035": "四谷4-29-X",
                            "IBT-036": "テスト商事ビル",
                            "IBT-037": "新宿区",
                            "IBT-038": "1600044",
                            "IBT-039": "東京都",
                            "AUTO-18": {"IBT-162": "1F 101"},
                            "AUTO-19": {"IBT-040": "JP"},
                        },
                        "AUTO-20": {
                            "IBT-031": "T1234567890123",
                            "AUTO-21": {"IBT-031-1": "VAT"},
                        },
                        "AUTO-22": {
                            "IBT-032": "T9876543210987",
                            "AUTO-23": {"AUTO-24": "NOTVAT"},
                        },
                        "AUTO-25": {
                            "IBT-027": "株式会社 テスト売り手商事",
                            "IBT-030": {"schemeID": "0188", "value": "1234567890123"},
                            "IBT-033": "Public company limited",
                        },
                        "IBG-06": {
                            "IBT-041": "田中 太郎",
                            "IBT-042": "03-3xxx-0001",
                            "IBT-043": "taro_tanaka@example.co.jp",
                        },
                    }
                },
                "IBG-07": {
                    "AUTO-26": {
                        "IBT-049": {"schemeID": "0188", "value": "3210987654321"},
                        "AUTO-27": {
                            "IBT-046": {
                                "schemeID": "0147",
                                "value": "654321:000321:0147:1",
                            }
                        },
                        "AUTO-28": {"IBT-045": "株式会社 テスト買い手物産"},
                        "IBG-08": {
                            "IBT-050": "北区",
                            "IBT-051": "北十二条西76-X",
                            "IBT-052": "札幌市",
                            "IBT-053": "0010012",
                            "IBT-054": "北海道",
                            "AUTO-29": {"IBT-163": "2F 202"},
                            "AUTO-30": {"IBT-055": "JP"},
                        },
                        "AUTO-31": {
                            "IBT-048": "T3210987654321",
                            "AUTO-32": {"IBT-048-1": "VAT"},
                        },
                        "AUTO-33": {
                            "IBT-044": "株式会社 テスト買い手物産",
                            "IBT-047": {
                                "schemeID": "0147",
                                "value": "654321:000321:0147:1",
                            },
                        },
                        "IBG-09": {
                            "IBT-056": "株式会社 テスト買い手物産 札幌支社",
                            "IBT-057": "011-757-1xxx",
                            "IBT-058": "test_purchaser@example.co.jp",
                        },
                    }
                },
                "IBG-10": {
                    "AUTO-34": {
                        "IBT-060": {"schemeID": "0147", "value": "123456:000124:0147:1"}
                    },
                    "AUTO-35": {"IBT-059": "Payee party"},
                    "AUTO-36": {
                        "IBT-061": {"schemeID": "0147", "value": "123456:000124:0147:1"}
                    },
                },
                "IBG-11": {
                    "AUTO-37": {"IBT-062": "TaxRepresentative Name"},
                    "IBG-12": {
                        "IBT-064": "四谷9-99-9",
                        "IBT-065": "テスト商事ビル",
                        "IBT-066": "新宿区",
                        "IBT-067": "1600044",
                        "IBT-068": "東京都",
                        "AUTO-38": {"IBT-164": "税務代理人住所"},
                        "AUTO-39": {"IBT-069": "JP"},
                    },
                    "AUTO-40": {
                        "IBT-063": "T7654321098765",
                        "AUTO-41": {"IBT-063-1": "0147"},
                    },
                },
                "IBG-13": {
                    "IBT-072": "2023-10-18",
                    "AUTO-42": {
                        "IBT-071": {
                            "schemeID": "0147",
                            "value": "123456:000123:0147:1",
                        },
                        "IBG-15": {
                            "IBT-075": "北区",
                            "IBT-076": "北十二条西76-X",
                            "IBT-077": "札幌市",
                            "IBT-078": "0010012",
                            "IBT-079": "北海道",
                            "AUTO-43": {"IBT-165": "2F 202"},
                            "AUTO-44": {"IBT-080": "JP"},
                        },
                    },
                    "AUTO-45": {
                        "AUTO-46": {"IBT-070": "株式会社 テスト買い手物産 札幌支社"}
                    },
                },
                "IBG-16": [
                    {
                        "IBT-178": "1",
                        "IBT-081": {"name": "Credit transfer", "value": "30"},
                        "IBT-083": [{"schemeID": "ABA", "value": "432948234234234"}],
                        "IBG-17": {
                            "IBT-084": {
                                "schemeID": "ZENGIN",
                                "value": "0009:221:1:1234567",
                            },
                            "IBT-085": "ｶ)ﾃｽﾄｳﾘﾃｼｮｳｼﾞ",
                            "AUTO-48": {
                                "IBT-086": "0009",
                                "IBG-34": {
                                    "IBT-169": "四谷4-29-X",
                                    "IBT-170": "テスト商事ビル",
                                    "IBT-171": "新宿区",
                                    "IBT-172": "1600044",
                                    "IBT-173": "東京都",
                                    "AUTO-49": {"IBT-174": "1F 101"},
                                    "AUTO-50": {"IBT-175": "JP"},
                                },
                            },
                        },
                        "IBG-19": {"IBT-089": "1", "AUTO-51": {"IBT-091": "1111"}},
                    }
                ],
                "IBG-33": [
                    {
                        "IBT-187": "1",
                        "IBT-020": "月末締め翌月20日払い, 銀行手数料振込人負担",
                        "IBT-176": {"value": "283400"},
                        "IBT-177": "2024-12-31",
                    }
                ],
                "IBG-35": [
                    {
                        "IBT-179": "1",
                        "IBT-180": {"value": "10000"},
                        "IBT-181": "2023-10-18",
                        "IBT-182": "Credit transfer",
                    }
                ],
                "IBG-20": [
                    {
                        "AUTO-54": "false",
                        "IBT-098": "95",
                        "IBT-097": "値引",
                        "IBT-094": "10",
                        "IBT-092": {"currencyID": "USD", "value": "1000"},
                        "IBT-093": {"currencyID": "USD", "value": "1000"},
                        "AUTO-57": {
                            "IBT-095": "S",
                            "IBT-096": "10",
                            "AUTO-58": {"IBT-095-1": "VAT"},
                        },
                    }
                ],
                "IBG-21": [
                    {
                        "AUTO-59": "true",
                        "IBT-105": "CG",
                        "IBT-104": "配送サービス",
                        "IBT-101": "10",
                        "IBT-099": {"currencyID": "USD", "value": "1000"},
                        "IBT-100": {"currencyID": "USD", "value": "1000"},
                        "AUTO-62": {
                            "IBT-102": "S",
                            "IBT-103": "10",
                            "AUTO-63": {"IBT-102-1": "VAT"},
                        },
                    }
                ],
                "AUTO-64": {
                    "IBT-110": {"currencyID": "USD", "value": "20372"},
                    "IBG-23": [
                        {
                            "IBT-116": {"currencyID": "USD", "value": "100000"},
                            "IBT-117": {"currencyID": "USD", "value": "10000"},
                            "AUTO-68": {
                                "IBT-118": "S",
                                "IBT-119": "10",
                                "AUTO-69": {"IBT-118-1": "VAT"},
                            },
                        },
                        {
                            "IBT-116": {"currencyID": "USD", "value": "3400"},
                            "IBT-117": {"currencyID": "USD", "value": "0"},
                            "AUTO-68": {
                                "IBT-118": "E",
                                "IBT-119": "0",
                                "AUTO-69": {"IBT-118-1": "VAT"},
                            },
                        },
                    ],
                },
                "IBG-37": {
                    "IBT-111": {"currencyID": "USD", "value": "20372"},
                    "IBG-38": [
                        {
                            "IBT-190": {"currencyID": "USD", "value": "10000"},
                            "AUTO-72": {"IBT-192": "S", "IBT-193": "10"},
                        },
                        {
                            "IBT-190": {"currencyID": "USD", "value": "0"},
                            "AUTO-72": {"IBT-192": "E", "IBT-193": "0"},
                        },
                    ],
                },
                "IBG-22": {
                    "IBT-106": {"currencyID": "USD", "value": "100000"},
                    "IBT-109": {"currencyID": "USD", "value": "263028"},
                    "IBT-112": {"currencyID": "USD", "value": "283400"},
                    "IBT-107": {"currencyID": "USD", "value": "1000"},
                    "IBT-108": {"currencyID": "USD", "value": "1000"},
                    "IBT-113": {"currencyID": "USD", "value": "0"},
                    "IBT-114": {"currencyID": "USD", "value": "0"},
                    "IBT-115": {"currencyID": "USD", "value": "283400"},
                },
            },
            [
                {
                    "IBT-126": "1",
                    "IBT-127": "請求書明細行注釈",
                    "IBT-129": {"unitCode": "H87", "value": "2"},
                    "IBT-131": {"currencyID": "USD", "value": "250000"},
                    "IBT-133": "Cost id 654",
                    "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                    "AUTO-82": {"IBT-132": "1", "AUTO-83": {"IBT-183": "1"}},
                    "AUTO-84": {"AUTO-85": "010", "AUTO-86": {"IBT-184": "789"}},
                    "IBG-36": {"IBT-188": "D001-1", "IBT-189": "129"},
                    "AUTO-87": {
                        "IBT-128": {"schemeID": "ABZ", "value": "AB-123"},
                        "AUTO-88": "130",
                    },
                    "IBG-27": [
                        {
                            "AUTO-89": "false",
                            "IBT-140": "95",
                            "IBT-139": "値引",
                            "IBT-138": "10",
                            "IBT-136": {"currencyID": "USD", "value": "1000"},
                            "IBT-137": {"currencyID": "USD", "value": "1000"},
                        }
                    ],
                    "IBG-28": [
                        {
                            "AUTO-92": "true",
                            "IBT-145": "CG",
                            "IBT-144": "クリーニング",
                            "IBT-143": "10",
                            "IBT-141": {"currencyID": "USD", "value": "1500"},
                            "IBT-142": {"currencyID": "USD", "value": "1500"},
                        }
                    ],
                    "IBG-31": {
                        "IBT-154": "デスクチェア",
                        "IBT-153": "デスクチェア",
                        "AUTO-95": {"IBT-156": "b-13214"},
                        "AUTO-96": {"IBT-155": "97iugug876"},
                        "AUTO-97": {
                            "IBT-157": {"schemeID": "0160", "value": "4503994155481"}
                        },
                        "AUTO-98": {"IBT-159": "JP"},
                        "AUTO-99": [
                            {
                                "IBT-158": {
                                    "listID": "TST",
                                    "listVersionID": "19.05.01",
                                    "value": "86776",
                                }
                            }
                        ],
                        "IBG-30": [
                            {
                                "IBT-151": "S",
                                "IBT-152": "10",
                                "IBT-166": {"value": "5000"},
                                "AUTO-101": {"IBT-167": "VAT"},
                            }
                        ],
                        "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "脚"}],
                    },
                    "IBG-29": {
                        "IBT-146": {"currencyID": "USD", "value": "50000"},
                        "IBT-149": {"unitCode": "H87", "value": "2"},
                        "AUTO-103": {
                            "IBT-147": {"currencyID": "USD", "value": "100"},
                            "IBT-148": {"currencyID": "USD", "value": "50500"},
                        },
                    },
                },
                {
                    "IBT-126": "2",
                    "IBT-129": {"unitCode": "H87", "value": "5"},
                    "IBT-131": {"currencyID": "USD", "value": "100000"},
                    "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                    "IBG-36": {"IBT-188": "D001-2"},
                    "IBG-31": {
                        "IBT-153": "コピー用紙（A4）",
                        "AUTO-96": {"IBT-155": "Item3"},
                        "AUTO-97": {
                            "IBT-157": {"schemeID": "0160", "value": "1234567890121"}
                        },
                        "AUTO-99": [{"IBT-158": {"listID": "MP", "value": "43211503"}}],
                        "IBG-30": [
                            {
                                "IBT-151": "S",
                                "IBT-152": "10",
                                "AUTO-101": {"IBT-167": "VAT"},
                            }
                        ],
                        "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "冊"}],
                    },
                    "IBG-29": {
                        "IBT-146": {"currencyID": "USD", "value": "500"},
                        "IBT-149": {"unitCode": "H87", "value": "1"},
                        "AUTO-103": {
                            "AUTO-104": "false",
                            "IBT-147": {"currencyID": "USD", "value": "100"},
                            "IBT-148": {"currencyID": "USD", "value": "600"},
                        },
                    },
                },
                {
                    "IBT-126": "3",
                    "IBT-129": {"unitCode": "H87", "value": "10"},
                    "IBT-131": {"currencyID": "USD", "value": "3490"},
                    "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                    "IBG-36": {"IBT-188": "D001-3"},
                    "IBG-31": {
                        "IBT-153": "検定済教科書(算数)",
                        "IBG-30": [
                            {
                                "IBT-151": "E",
                                "IBT-152": "0",
                                "AUTO-101": {"IBT-167": "VAT"},
                            }
                        ],
                        "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "冊"}],
                    },
                    "IBG-29": {
                        "IBT-146": {"currencyID": "USD", "value": "349"},
                        "IBT-149": {"unitCode": "H87", "value": "1"},
                    },
                },
            ],
            {
                "data_type": 1,
                "invoice_mng_num": 12345,
                "publisher": {
                    "publisher_peppol_scheme_id": "1108",
                    "publisher_peppol_id": "T1234567890123",
                    "publisher_corp_genuine_id": "1234567890123",
                    "publisher_tax_corp_id": "1234567890123",
                    "publisher_mail": "123@123.com",
                    "publisher_company_name_org": "株式会社 テスト売り手商事",
                    "publisher_mng_num": "HKM001",
                    "publisher_company_name": "営業所",
                    "publisher_section": "部署",
                    "publisher_zip": "160-0044",
                    "publisher_country_subentity": "東京都",
                    "publisher_city_name": "新宿区",
                    "publisher_street_name": "四谷9-99-9 テスト商事ビル 1F 101",
                    "publisher_phone": "03-3xxx-0001",
                    "biz_type": "1",
                    "biz_regist_no": "T1234567890123",
                    "nta_biz_regist_no_result": "0",
                    "nta_registered_date": "2012-12-12",
                    "nta_process": "事業者処理区分",
                    "nta_company_name": "氏名又は名称",
                    "nta_area": "都道府県",
                    "nta_address": "住所",
                    "nta_update_date": "2012-12-12",
                    "nta_trade_name": "屋号",
                    "nta_common_nam": "通称・旧姓",
                    "nta_cancel_date": "2099-12-12",
                    "nta_lapse_date": "2099-12-12",
                },
                "invoice_setting_code": "1",
                "inv_no": "3",
                "customer": {
                    "peppol_scheme_id": "1108",
                    "peppol_id": "T9876543210987",
                    "tax_corp_id": "1234567890123",
                    "private_cust_cd": "HKS001",
                    "corp_genuine_id": 123,
                    "company_name_org": "株式会社 テスト買い手物産",
                    "zip": "001-0012",
                    "country_subentity": "北海道",
                    "city_name": "札幌市",
                    "street_name": "北区北十二条西76-X 2F 202",
                    "user_email": "123@123.com",
                    "phone": "011-757-1xxx",
                },
                "invoice_title": "テスト請求書",
                "inv_name": "件名",
                "pay_due_date": "2024-04-25",
                "payment_method": "0",
                "prev_inv_amount": 0,
                "payment": 0,
                "adjustment": 0,
                "carryover_new": 0,
                "paid_info": [
                    {
                        "paid_without_tax": 0,
                    }
                ],
                "refund_info": [
                    {
                        "refund_without_tax": 1000,
                        "tax_type": "0",
                        "tax_rate_sec": 10,
                        "reduced_tax_flg": "0",
                    }
                ],
                "additional_info": [
                    {
                        "additional_without_tax": 1000,
                        "tax_type": "0",
                        "tax_rate_sec": 10,
                        "reduced_tax_flg": "0",
                    }
                ],
                "inv_without_tax": 263028,
                "inv_tax": 20372,
                "inv_amount": 283400,
                "invoice_amount_title": "請求金額タイトル",
                "inv_show_amount": 1001,
                "close_date": "2024-04-30",
                "remarks": "備考テスト",
                "customer_code1": "cd1",
                "customer_code2": "cd2",
                "edi_info": "EDI情報",
                "contact": "担当",
                "inv_free_txt1": "おもての自由項目1",
                "inv_free_txt2": "おもての自由項目2",
                "inv_free_txt3": "おもての自由項目3",
                "inv_free_num1": 1000,
                "inv_free_num2": 1001,
                "inv_free_num3": 1002,
                "inv_free_num4": 1003,
                "inv_free_num5": 1004,
                "inv_free_num6": 1005,
                "inv_free_num7": 1006,
                "unit_tax_calc_sec": "0",
                "inv_coop_post_use_type": "0",
                "private_print_flg": "0",
                "invoice_type": "0",
                "tax_calc_basis": "1",
                "invoice_comment": "補足文言",
                "inv_without_tax_tr10": 100000,
                "inv_tax_tr10": 10000,
                "inv_amount_tr10": 110000,
                "inv_without_tax_tr8_reduced": 920,
                "inv_tax_tr8_reduced": 80,
                "inv_amount_tr8_reduced": 1000,
                "inv_without_tax_tr8": 67528,
                "inv_tax_tr8": 5872,
                "inv_amount_tr8": 73400,
                "inv_without_tax_tr5": 85500,
                "inv_tax_tr5": 4500,
                "inv_amount_tr5": 90000,
                "inv_without_tax_tr0": 10000,
                "inv_tax_tr0": 0,
                "inv_amount_tr0": 10000,
                "inv_without_tax_free": 10000,
                "inv_tax_free": 0,
                "inv_amount_free": 10000,
                "inv_without_tax_exemption": 30000,
                "inv_tax_exemption": 0,
                "inv_amount_exemption": 30000,
                "inv_without_tax_non": 30000,
                "inv_tax_non": 0,
                "inv_amount_non": 30000,
                "details": [
                    {
                        "item_slip_date": "2023-10-18",
                        "item_slip_no": "1",
                        "item_prod_code": "D001-1",
                        "item_name": "デスクチェア",
                        "item_qty": 2,
                        "item_price": 50000,
                        "item_unit": "脚",
                        "item_without_tax": 100000,
                        "item_tax": 10000,
                        "item_amount": 110000,
                        "item_sec_code": "BMCD001",
                        "item_sec_name": "部門",
                        "detail_remarks": "明細備考",
                        "item_free_txt1": "明細メモ1",
                        "item_free_txt2": "明細メモ2",
                        "item_free_txt3": "明細の自由項目3",
                        "item_free_txt4": "明細の自由項目4",
                        "item_free_txt5": "明細の自由項目5",
                        "item_free_txt6": "明細の自由項目6",
                        "item_free_txt7": "明細の自由項目7",
                        "item_free_txt8": "明細の自由項目8",
                        "item_free_txt9": "明細の自由項目9",
                        "item_free_txt10": "明細の自由項目10",
                        "item_free_txt_l": "明細の自由項目11",
                        "tax_type": "0",
                        "tax_rate_sec": 10,
                        "reduced_tax_flg": "0",
                        "input_tax_type": "0",
                        "tax_calc_type": "1",
                        "sum_exempt_flg": "0",
                    }
                ],
                "custom_header": {
                    "custom_name": "カスタム名",
                    "custom_detail_headers": [
                        {
                            "field_seq": 1,
                            "field_name": "カスタム項目",
                            "field_type": "S",
                            "field_num_decimal_places": 0,
                            "field_col_width": 1,
                        }
                    ],
                },
                "custom_details": [
                    {"custom_detail_values": [{"field_seq": 1, "field_value": "A"}]}
                ],
                "banks": [
                    {
                        "transfer_code": "CD001",
                        "fncl_inst_code": "0009",
                        "fncl_inst_name": "金融機関名",
                        "fncl_inst_kana": "カナ",
                        "branch_code": "221",
                        "branch_name": "支店名",
                        "branch_kana": "カナ",
                        "deposit_sec": "1",
                        "account_num": "1234567",
                        "depositor_name": "田中 太郎",
                        "depositor_kana": "タナカ タロウ",
                    }
                ],
                "list_info": {
                    "product_sec": "個別",
                    "private_user_name": "自社担当者",
                    "approver_name": "発行承認者",
                    "billing_name": "請求先",
                    "issue_user_name": "発行先担当者",
                    "phone": "12345-1234-1234",
                    "send_date": "2024-03-10",
                    "remind_date": "2023-12-13",
                    "seal_flg": "true",
                    "fax_send_flg": "false",
                    "qa_history": "false",
                    "seal_date": "2023-12-12 12:12:12",
                    "destination_code": "ATSK001",
                    "destination_name": "宛先名",
                },
                "inv_free_titles": {
                    "inv_free_txt_title1": "おもての自由項目1（文字）タイトル",
                    "inv_free_txt_title2": "おもての自由項目2（文字）タイトル",
                    "inv_free_txt_title3": "おもての自由項目3（文字）タイトル",
                    "inv_free_num_title1": "おもての自由項目1（数値）タイトル",
                    "inv_free_num_title2": "おもての自由項目2（数値）タイトル",
                    "inv_free_num_title3": "おもての自由項目3（数値）タイトル",
                    "inv_free_num_title4": "おもての自由項目4（数値）タイトル",
                    "inv_free_num_title5": "おもての自由項目5（数値）タイトル",
                    "inv_free_num_title6": "おもての自由項目6（数値）タイトル",
                    "inv_free_num_title7": "おもての自由項目7（数値）タイトル",
                    "item_free_txt_title1": "明細の自由項目1（文字）タイトル",
                    "item_free_txt_title2": "明細の自由項目2（文字）タイトル",
                    "item_free_txt_title3": "明細の自由項目3（文字）タイトル",
                    "item_free_txt_title4": "明細の自由項目4（文字）タイトル",
                    "item_free_txt_title5": "明細の自由項目5（文字）タイトル",
                    "item_free_txt_title6": "明細の自由項目6（文字）タイトル",
                    "item_free_txt_title7": "明細の自由項目7（文字）タイトル",
                    "item_free_txt_title8": "明細の自由項目8（文字）タイトル",
                    "item_free_txt_title9": "明細の自由項目9（文字）タイトル",
                    "item_free_txt_title10": "明細の自由項目10（文字）タイトル",
                    "item_free_txt_l_title": "明細の自由項目11（文字）タイトル",
                },
                "wf_status": "10",
                "seller_attached_file": [
                    {
                        "file": "dGhpcyUyMGlzJTIwYSUyMHRlc3QlMjB0ZXh0",
                        "file_name": "test.txt",
                    }
                ],
            },
            "invoices/2/xml/73/base_standard_invoices_data_3.xml",
            const.PROC_RESULT_SUCCESS,
        ),
        # case 2 : 登録不可能なデータ
        ({}, [], {}, "test", const.PROC_RESULT_FAILED),
    ]


def test_create_data_for_insertion_exception() -> list:
    """create_data_for_insertion例外テストパラメータ"""
    return []


def test_xml_data_shaping() -> (
    list[tuple[str, str, None | tuple[dict, list[dict], dict]]]
):
    """xml_data_shapingテストパラメータ"""
    return [
        # case 1 : 変換と正規化が可能なxml
        (
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../storage/for_test/base_standard_invoices_data_1.xml",
            ),
            "test.xml",
            (
                {
                    "IBT-024": "urn:peppol:pint:billing-1@jp-1",
                    "IBT-023": "urn:peppol:bis:billing",
                    "IBT-001": "1",
                    "IBT-002": "2024-03-10",
                    "IBT-168": "10:00:15",
                    "IBT-009": "2024-04-25",
                    "IBT-003": "380",
                    "IBT-022": "試験用の請求書です",
                    "IBT-007": "2024-03-25",
                    "IBT-005": "JPY",
                    "IBT-006": "JPY",
                    "IBT-019": "4217:2323:2323",
                    "IBT-010": "0150abc",
                    "IBG-14": {
                        "IBT-073": "2024-01-18",
                        "IBT-074": "2024-03-31",
                        "IBT-008": "3",
                    },
                    "AUTO-2": {"IBT-013": "O-998877", "IBT-014": "SO-12345"},
                    "IBG-03": [{"AUTO-3": {"IBT-025": "123", "IBT-026": "2024-02-25"}}],
                    "AUTO-4": {"IBT-016": "desp98"},
                    "AUTO-5": {"IBT-015": "resp-1"},
                    "AUTO-6": {"IBT-017": "ppid-123"},
                    "AUTO-7": {"IBT-012": "contract1"},
                    "AUTO-8": {
                        "IBT-018": {"schemeID": "ABT", "value": "DR35141"},
                        "AUTO-9": "130",
                    },
                    "IBG-24": [
                        {
                            "IBT-122": "testDoc1",
                            "IBT-123": "試験用の添付書類",
                            "AUTO-10": {
                                "IBT-125": {
                                    "filename": "test.txt",
                                    "mimeCode": "text/plain",
                                    "value": "dGhpcyUyMGlzJTIwYSUyMHRlc3QlMjB0ZXh0",
                                },
                                "AUTO-11": {
                                    "IBT-124": "http://www.example.com/summary001.html"
                                },
                            },
                        },
                        {
                            "IBT-122": "testDoc2",
                            "IBT-123": "Usage breakdown",
                            "AUTO-10": {
                                "AUTO-11": {
                                    "IBT-124": "http://www.example.com/breakdown001.html"
                                }
                            },
                        },
                    ],
                    "AUTO-12": {"IBT-011": "PID1"},
                    "IBG-04": {
                        "AUTO-13": {
                            "IBT-034": {"schemeID": "0188", "value": "1234567890123"},
                            "AUTO-14": [
                                {
                                    "IBT-029": {
                                        "schemeID": "0147",
                                        "value": "123456:000123:0147:1",
                                    }
                                }
                            ],
                            "AUTO-17": {"IBT-028": "株式会社 テスト売り手商事"},
                            "IBG-05": {
                                "IBT-035": "四谷4-29-X",
                                "IBT-036": "テスト商事ビル",
                                "IBT-037": "新宿区",
                                "IBT-038": "1600044",
                                "IBT-039": "東京都",
                                "AUTO-18": {"IBT-162": "1F 101"},
                                "AUTO-19": {"IBT-040": "JP"},
                            },
                            "AUTO-20": {
                                "IBT-031": "T1234567890123",
                                "AUTO-21": {"IBT-031-1": "VAT"},
                            },
                            "AUTO-22": {
                                "IBT-032": "T9876543210987",
                                "AUTO-23": {"AUTO-24": "NOTVAT"},
                            },
                            "AUTO-25": {
                                "IBT-027": "株式会社 テスト売り手商事",
                                "IBT-030": {
                                    "schemeID": "0188",
                                    "value": "1234567890123",
                                },
                                "IBT-033": "Public company limited",
                            },
                            "IBG-06": {
                                "IBT-041": "田中 太郎",
                                "IBT-042": "03-3xxx-0001",
                                "IBT-043": "taro_tanaka@example.co.jp",
                            },
                        }
                    },
                    "IBG-07": {
                        "AUTO-26": {
                            "IBT-049": {"schemeID": "0188", "value": "3210987654321"},
                            "AUTO-27": {
                                "IBT-046": {
                                    "schemeID": "0147",
                                    "value": "654321:000321:0147:1",
                                }
                            },
                            "AUTO-28": {"IBT-045": "株式会社 テスト買い手物産"},
                            "IBG-08": {
                                "IBT-050": "北区",
                                "IBT-051": "北十二条西76-X",
                                "IBT-052": "札幌市",
                                "IBT-053": "0010012",
                                "IBT-054": "北海道",
                                "AUTO-29": {"IBT-163": "2F 202"},
                                "AUTO-30": {"IBT-055": "JP"},
                            },
                            "AUTO-31": {
                                "IBT-048": "T3210987654321",
                                "AUTO-32": {"IBT-048-1": "VAT"},
                            },
                            "AUTO-33": {
                                "IBT-044": "株式会社 テスト買い手物産",
                                "IBT-047": {
                                    "schemeID": "0147",
                                    "value": "654321:000321:0147:1",
                                },
                            },
                            "IBG-09": {
                                "IBT-056": "株式会社 テスト買い手物産 札幌支社",
                                "IBT-057": "011-757-1xxx",
                                "IBT-058": "test_purchaser@example.co.jp",
                            },
                        }
                    },
                    "IBG-10": {
                        "AUTO-34": {
                            "IBT-060": {
                                "schemeID": "0147",
                                "value": "123456:000124:0147:1",
                            }
                        },
                        "AUTO-35": {"IBT-059": "Payee party"},
                        "AUTO-36": {
                            "IBT-061": {
                                "schemeID": "0147",
                                "value": "123456:000124:0147:1",
                            }
                        },
                    },
                    "IBG-11": {
                        "AUTO-37": {"IBT-062": "TaxRepresentative Name"},
                        "IBG-12": {
                            "IBT-064": "四谷9-99-9",
                            "IBT-065": "テスト商事ビル",
                            "IBT-066": "新宿区",
                            "IBT-067": "1600044",
                            "IBT-068": "東京都",
                            "AUTO-38": {"IBT-164": "税務代理人住所"},
                            "AUTO-39": {"IBT-069": "JP"},
                        },
                        "AUTO-40": {
                            "IBT-063": "T7654321098765",
                            "AUTO-41": {"IBT-063-1": "0147"},
                        },
                    },
                    "IBG-13": {
                        "IBT-072": "2023-10-18",
                        "AUTO-42": {
                            "IBT-071": {
                                "schemeID": "0147",
                                "value": "123456:000123:0147:1",
                            },
                            "IBG-15": {
                                "IBT-075": "北区",
                                "IBT-076": "北十二条西76-X",
                                "IBT-077": "札幌市",
                                "IBT-078": "0010012",
                                "IBT-079": "北海道",
                                "AUTO-43": {"IBT-165": "2F 202"},
                                "AUTO-44": {"IBT-080": "JP"},
                            },
                        },
                        "AUTO-45": {
                            "AUTO-46": {"IBT-070": "株式会社 テスト買い手物産 札幌支社"}
                        },
                    },
                    "IBG-16": [
                        {
                            "IBT-178": "1",
                            "IBT-081": {"name": "Credit transfer", "value": "30"},
                            "IBT-083": [
                                {"schemeID": "ABA", "value": "432948234234234"}
                            ],
                            "IBG-17": {
                                "IBT-084": {
                                    "schemeID": "ZENGIN",
                                    "value": "0009:221:1:1234567",
                                },
                                "IBT-085": "ｶ)ﾃｽﾄｳﾘﾃｼｮｳｼﾞ",
                                "AUTO-48": {
                                    "IBT-086": "0009",
                                    "IBG-34": {
                                        "IBT-169": "四谷4-29-X",
                                        "IBT-170": "テスト商事ビル",
                                        "IBT-171": "新宿区",
                                        "IBT-172": "1600044",
                                        "IBT-173": "東京都",
                                        "AUTO-49": {"IBT-174": "1F 101"},
                                        "AUTO-50": {"IBT-175": "JP"},
                                    },
                                },
                            },
                            "IBG-19": {"IBT-089": "1", "AUTO-51": {"IBT-091": "1111"}},
                        }
                    ],
                    "IBG-33": [
                        {
                            "IBT-187": "1",
                            "IBT-020": "月末締め翌月20日払い, 銀行手数料振込人負担",
                            "IBT-176": {"value": "283400"},
                            "IBT-177": "2024-12-31",
                        }
                    ],
                    "IBG-35": [
                        {
                            "IBT-179": "1",
                            "IBT-180": {"value": "10000"},
                            "IBT-181": "2023-10-18",
                            "IBT-182": "Credit transfer",
                        }
                    ],
                    "IBG-20": [
                        {
                            "AUTO-54": "false",
                            "IBT-098": "95",
                            "IBT-097": "値引",
                            "IBT-094": "10",
                            "IBT-092": {"currencyID": "JPY", "value": "1000"},
                            "IBT-093": {"currencyID": "JPY", "value": "1000"},
                            "AUTO-57": {
                                "IBT-095": "S",
                                "IBT-096": "10",
                                "AUTO-58": {"IBT-095-1": "VAT"},
                            },
                        }
                    ],
                    "IBG-21": [
                        {
                            "AUTO-59": "true",
                            "IBT-105": "CG",
                            "IBT-104": "配送サービス",
                            "IBT-101": "10",
                            "IBT-099": {"currencyID": "JPY", "value": "1000"},
                            "IBT-100": {"currencyID": "JPY", "value": "1000"},
                            "AUTO-62": {
                                "IBT-102": "S",
                                "IBT-103": "10",
                                "AUTO-63": {"IBT-102-1": "VAT"},
                            },
                        }
                    ],
                    "AUTO-64": {
                        "IBT-110": {"currencyID": "JPY", "value": "20372"},
                        "IBG-23": [
                            {
                                "IBT-116": {"currencyID": "JPY", "value": "100000"},
                                "IBT-117": {"currencyID": "JPY", "value": "10000"},
                                "AUTO-68": {
                                    "IBT-118": "S",
                                    "IBT-119": "10",
                                    "AUTO-69": {"IBT-118-1": "VAT"},
                                },
                            },
                            {
                                "IBT-116": {"currencyID": "JPY", "value": "3400"},
                                "IBT-117": {"currencyID": "JPY", "value": "0"},
                                "AUTO-68": {
                                    "IBT-118": "E",
                                    "IBT-119": "0",
                                    "AUTO-69": {"IBT-118-1": "VAT"},
                                },
                            },
                        ],
                    },
                    "IBG-37": {
                        "IBT-111": {"currencyID": "JPY", "value": "20372"},
                        "IBG-38": [
                            {
                                "IBT-190": {"currencyID": "JPY", "value": "10000"},
                                "AUTO-72": {"IBT-192": "S", "IBT-193": "10"},
                            },
                            {
                                "IBT-190": {"currencyID": "JPY", "value": "0"},
                                "AUTO-72": {"IBT-192": "E", "IBT-193": "0"},
                            },
                        ],
                    },
                    "IBG-22": {
                        "IBT-106": {"currencyID": "JPY", "value": "100000"},
                        "IBT-109": {"currencyID": "JPY", "value": "263028"},
                        "IBT-112": {"currencyID": "JPY", "value": "283400"},
                        "IBT-107": {"currencyID": "JPY", "value": "1000"},
                        "IBT-108": {"currencyID": "JPY", "value": "1000"},
                        "IBT-113": {"currencyID": "JPY", "value": "0"},
                        "IBT-114": {"currencyID": "JPY", "value": "0"},
                        "IBT-115": {"currencyID": "JPY", "value": "283400"},
                    },
                },
                [
                    {
                        "IBT-126": "1",
                        "IBT-127": "請求書明細行注釈",
                        "IBT-129": {"unitCode": "H87", "value": "2"},
                        "IBT-131": {"currencyID": "JPY", "value": "250000"},
                        "IBT-133": "Cost id 654",
                        "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                        "AUTO-82": {"IBT-132": "1", "AUTO-83": {"IBT-183": "1"}},
                        "AUTO-84": {"AUTO-85": "010", "AUTO-86": {"IBT-184": "789"}},
                        "IBG-36": {"IBT-188": "D001-1", "IBT-189": "129"},
                        "AUTO-87": {
                            "IBT-128": {"schemeID": "ABZ", "value": "AB-123"},
                            "AUTO-88": "130",
                        },
                        "IBG-27": [
                            {
                                "AUTO-89": "false",
                                "IBT-140": "95",
                                "IBT-139": "値引",
                                "IBT-138": "10",
                                "IBT-136": {"currencyID": "JPY", "value": "1000"},
                                "IBT-137": {"currencyID": "JPY", "value": "1000"},
                            }
                        ],
                        "IBG-28": [
                            {
                                "AUTO-92": "true",
                                "IBT-145": "CG",
                                "IBT-144": "クリーニング",
                                "IBT-143": "10",
                                "IBT-141": {"currencyID": "JPY", "value": "1500"},
                                "IBT-142": {"currencyID": "JPY", "value": "1500"},
                            }
                        ],
                        "IBG-31": {
                            "IBT-154": "デスクチェア",
                            "IBT-153": "デスクチェア",
                            "AUTO-95": {"IBT-156": "b-13214"},
                            "AUTO-96": {"IBT-155": "97iugug876"},
                            "AUTO-97": {
                                "IBT-157": {
                                    "schemeID": "0160",
                                    "value": "4503994155481",
                                }
                            },
                            "AUTO-98": {"IBT-159": "JP"},
                            "AUTO-99": [
                                {
                                    "IBT-158": {
                                        "listID": "TST",
                                        "listVersionID": "19.05.01",
                                        "value": "86776",
                                    }
                                }
                            ],
                            "IBG-30": [
                                {
                                    "IBT-151": "S",
                                    "IBT-152": "10",
                                    "IBT-166": {"value": "5000"},
                                    "AUTO-101": {"IBT-167": "VAT"},
                                }
                            ],
                            "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "脚"}],
                        },
                        "IBG-29": {
                            "IBT-146": {"currencyID": "JPY", "value": "50000"},
                            "IBT-149": {"unitCode": "H87", "value": "2"},
                            "AUTO-103": {
                                "IBT-147": {"currencyID": "JPY", "value": "100"},
                                "IBT-148": {"currencyID": "JPY", "value": "50500"},
                            },
                        },
                    },
                    {
                        "IBT-126": "2",
                        "IBT-129": {"unitCode": "H87", "value": "5"},
                        "IBT-131": {"currencyID": "JPY", "value": "100000"},
                        "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                        "IBG-36": {"IBT-188": "D001-2"},
                        "IBG-31": {
                            "IBT-153": "コピー用紙（A4）",
                            "AUTO-96": {"IBT-155": "Item3"},
                            "AUTO-97": {
                                "IBT-157": {
                                    "schemeID": "0160",
                                    "value": "1234567890121",
                                }
                            },
                            "AUTO-99": [
                                {"IBT-158": {"listID": "MP", "value": "43211503"}}
                            ],
                            "IBG-30": [
                                {
                                    "IBT-151": "S",
                                    "IBT-152": "10",
                                    "AUTO-101": {"IBT-167": "VAT"},
                                }
                            ],
                            "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "冊"}],
                        },
                        "IBG-29": {
                            "IBT-146": {"currencyID": "JPY", "value": "500"},
                            "IBT-149": {"unitCode": "H87", "value": "1"},
                            "AUTO-103": {
                                "AUTO-104": "false",
                                "IBT-147": {"currencyID": "JPY", "value": "100"},
                                "IBT-148": {"currencyID": "JPY", "value": "600"},
                            },
                        },
                    },
                    {
                        "IBT-126": "3",
                        "IBT-129": {"unitCode": "H87", "value": "10"},
                        "IBT-131": {"currencyID": "JPY", "value": "3490"},
                        "IBG-26": {"IBT-134": "2023-10-18", "IBT-135": "2023-10-18"},
                        "IBG-36": {"IBT-188": "D001-3"},
                        "IBG-31": {
                            "IBT-153": "検定済教科書(算数)",
                            "IBG-30": [
                                {
                                    "IBT-151": "E",
                                    "IBT-152": "0",
                                    "AUTO-101": {"IBT-167": "VAT"},
                                }
                            ],
                            "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "冊"}],
                        },
                        "IBG-29": {
                            "IBT-146": {"currencyID": "JPY", "value": "349"},
                            "IBT-149": {"unitCode": "H87", "value": "1"},
                        },
                    },
                ],
                {"mocked_data": "response"},
            ),
        ),
        # case 2 : 変換と正規化が不可能なxml
        (
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../storage/for_test/error.xml",
            ),
            "test.xml",
            None,
        ),
    ]


def test_xml_data_shaping_exception() -> list:
    """xml_data_shaping例外テストパラメータ"""
    return []


def test_zip_data_shaping() -> list[tuple[str, dict, ReceiveRecordStatus]]:
    """zip_data_shapingテストパラメータ"""
    return [
        # case 1 : 登録可能なxmlで作成されたzipファイル
        (
            "../../storage/for_test/receive.zip",
            {
                "send": HttpAccessPointService,
                "get_response": {
                    "status": "0",
                    "error_code": "",
                    "error_detail": "",
                    "b2b_format_datas": [
                        {
                            "data_type": 1,
                            "invoice_mng_num": 12345,
                            "publisher": {
                                "publisher_peppol_scheme_id": "1108",
                                "publisher_peppol_id": "T1234567890123",
                                "publisher_corp_genuine_id": "1234567890123",
                                "publisher_tax_corp_id": "1234567890123",
                                "publisher_mail": "123@123.com",
                                "publisher_company_name_org": "株式会社 テスト売り手商事",
                                "publisher_mng_num": "HKM001",
                                "publisher_company_name": "営業所",
                                "publisher_section": "部署",
                                "publisher_zip": "160-0044",
                                "publisher_country_subentity": "東京都",
                                "publisher_city_name": "新宿区",
                                "publisher_street_name": "四谷9-99-9 テスト商事ビル 1F 101",
                                "publisher_phone": "03-3xxx-0001",
                                "biz_type": "1",
                                "biz_regist_no": "T1234567890123",
                                "nta_biz_regist_no_result": "0",
                                "nta_registered_date": "2012-12-12",
                                "nta_process": "事業者処理区分",
                                "nta_company_name": "氏名又は名称",
                                "nta_area": "都道府県",
                                "nta_address": "住所",
                                "nta_update_date": "2012-12-12",
                                "nta_trade_name": "屋号",
                                "nta_common_nam": "通称・旧姓",
                                "nta_cancel_date": "2099-12-12",
                                "nta_lapse_date": "2099-12-12",
                            },
                            "invoice_setting_code": "1",
                            "inv_no": "3",
                            "customer": {
                                "peppol_scheme_id": "1108",
                                "peppol_id": "T9876543210987",
                                "tax_corp_id": "1234567890123",
                                "private_cust_cd": "HKS001",
                                "corp_genuine_id": 123,
                                "company_name_org": "株式会社 テスト買い手物産",
                                "zip": "001-0012",
                                "country_subentity": "北海道",
                                "city_name": "札幌市",
                                "street_name": "北区北十二条西76-X 2F 202",
                                "user_email": "123@123.com",
                                "phone": "011-757-1xxx",
                            },
                            "invoice_title": "テスト請求書",
                            "inv_name": "件名",
                            "pay_due_date": "2024-04-25",
                            "payment_method": "0",
                            "prev_inv_amount": 0,
                            "payment": 0,
                            "adjustment": 0,
                            "carryover_new": 0,
                            "paid_info": [
                                {
                                    "paid_without_tax": 0,
                                }
                            ],
                            "refund_info": [
                                {
                                    "refund_without_tax": 1000,
                                    "tax_type": "0",
                                    "tax_rate_sec": 10,
                                    "reduced_tax_flg": "0",
                                }
                            ],
                            "additional_info": [
                                {
                                    "additional_without_tax": 1000,
                                    "tax_type": "0",
                                    "tax_rate_sec": 10,
                                    "reduced_tax_flg": "0",
                                }
                            ],
                            "inv_without_tax": 263028,
                            "inv_tax": 20372,
                            "inv_amount": 283400,
                            "invoice_amount_title": "請求金額タイトル",
                            "inv_show_amount": 1001,
                            "close_date": "2024-04-30",
                            "remarks": "備考テスト",
                            "customer_code1": "cd1",
                            "customer_code2": "cd2",
                            "edi_info": "EDI情報",
                            "contact": "担当",
                            "inv_free_txt1": "おもての自由項目1",
                            "inv_free_txt2": "おもての自由項目2",
                            "inv_free_txt3": "おもての自由項目3",
                            "inv_free_num1": 1000,
                            "inv_free_num2": 1001,
                            "inv_free_num3": 1002,
                            "inv_free_num4": 1003,
                            "inv_free_num5": 1004,
                            "inv_free_num6": 1005,
                            "inv_free_num7": 1006,
                            "unit_tax_calc_sec": "0",
                            "inv_coop_post_use_type": "0",
                            "private_print_flg": "0",
                            "invoice_type": "0",
                            "tax_calc_basis": "1",
                            "invoice_comment": "補足文言",
                            "inv_without_tax_tr10": 100000,
                            "inv_tax_tr10": 10000,
                            "inv_amount_tr10": 110000,
                            "inv_without_tax_tr8_reduced": 920,
                            "inv_tax_tr8_reduced": 80,
                            "inv_amount_tr8_reduced": 1000,
                            "inv_without_tax_tr8": 67528,
                            "inv_tax_tr8": 5872,
                            "inv_amount_tr8": 73400,
                            "inv_without_tax_tr5": 85500,
                            "inv_tax_tr5": 4500,
                            "inv_amount_tr5": 90000,
                            "inv_without_tax_tr0": 10000,
                            "inv_tax_tr0": 0,
                            "inv_amount_tr0": 10000,
                            "inv_without_tax_free": 10000,
                            "inv_tax_free": 0,
                            "inv_amount_free": 10000,
                            "inv_without_tax_exemption": 30000,
                            "inv_tax_exemption": 0,
                            "inv_amount_exemption": 30000,
                            "inv_without_tax_non": 30000,
                            "inv_tax_non": 0,
                            "inv_amount_non": 30000,
                            "details": [
                                {
                                    "item_slip_date": "2023-10-18",
                                    "item_slip_no": "1",
                                    "item_prod_code": "D001-1",
                                    "item_name": "デスクチェア",
                                    "item_qty": 2,
                                    "item_price": 50000,
                                    "item_unit": "脚",
                                    "item_without_tax": 100000,
                                    "item_tax": 10000,
                                    "item_amount": 110000,
                                    "item_sec_code": "BMCD001",
                                    "item_sec_name": "部門",
                                    "detail_remarks": "明細備考",
                                    "item_free_txt1": "明細メモ1",
                                    "item_free_txt2": "明細メモ2",
                                    "item_free_txt3": "明細の自由項目3",
                                    "item_free_txt4": "明細の自由項目4",
                                    "item_free_txt5": "明細の自由項目5",
                                    "item_free_txt6": "明細の自由項目6",
                                    "item_free_txt7": "明細の自由項目7",
                                    "item_free_txt8": "明細の自由項目8",
                                    "item_free_txt9": "明細の自由項目9",
                                    "item_free_txt10": "明細の自由項目10",
                                    "item_free_txt_l": "明細の自由項目11",
                                    "tax_type": "0",
                                    "tax_rate_sec": 10,
                                    "reduced_tax_flg": "0",
                                    "input_tax_type": "0",
                                    "tax_calc_type": "1",
                                    "sum_exempt_flg": "0",
                                }
                            ],
                            "custom_header": {
                                "custom_name": "カスタム名",
                                "custom_detail_headers": [
                                    {
                                        "field_seq": 1,
                                        "field_name": "カスタム項目",
                                        "field_type": "S",
                                        "field_num_decimal_places": 0,
                                        "field_col_width": 1,
                                    }
                                ],
                            },
                            "custom_details": [
                                {
                                    "custom_detail_values": [
                                        {"field_seq": 1, "field_value": "A"}
                                    ]
                                }
                            ],
                            "banks": [
                                {
                                    "transfer_code": "CD001",
                                    "fncl_inst_code": "0009",
                                    "fncl_inst_name": "金融機関名",
                                    "fncl_inst_kana": "カナ",
                                    "branch_code": "221",
                                    "branch_name": "支店名",
                                    "branch_kana": "カナ",
                                    "deposit_sec": "1",
                                    "account_num": "1234567",
                                    "depositor_name": "田中 太郎",
                                    "depositor_kana": "タナカ タロウ",
                                }
                            ],
                            "list_info": {
                                "product_sec": "個別",
                                "private_user_name": "自社担当者",
                                "approver_name": "発行承認者",
                                "billing_name": "請求先",
                                "issue_user_name": "発行先担当者",
                                "phone": "12345-1234-1234",
                                "send_date": "2024-03-10",
                                "remind_date": "2023-12-13",
                                "seal_flg": "true",
                                "fax_send_flg": "false",
                                "qa_history": "false",
                                "seal_date": "2023-12-12 12:12:12",
                                "destination_code": "ATSK001",
                                "destination_name": "宛先名",
                            },
                            "inv_free_titles": {
                                "inv_free_txt_title1": "おもての自由項目1（文字）タイトル",
                                "inv_free_txt_title2": "おもての自由項目2（文字）タイトル",
                                "inv_free_txt_title3": "おもての自由項目3（文字）タイトル",
                                "inv_free_num_title1": "おもての自由項目1（数値）タイトル",
                                "inv_free_num_title2": "おもての自由項目2（数値）タイトル",
                                "inv_free_num_title3": "おもての自由項目3（数値）タイトル",
                                "inv_free_num_title4": "おもての自由項目4（数値）タイトル",
                                "inv_free_num_title5": "おもての自由項目5（数値）タイトル",
                                "inv_free_num_title6": "おもての自由項目6（数値）タイトル",
                                "inv_free_num_title7": "おもての自由項目7（数値）タイトル",
                                "item_free_txt_title1": "明細の自由項目1（文字）タイトル",
                                "item_free_txt_title2": "明細の自由項目2（文字）タイトル",
                                "item_free_txt_title3": "明細の自由項目3（文字）タイトル",
                                "item_free_txt_title4": "明細の自由項目4（文字）タイトル",
                                "item_free_txt_title5": "明細の自由項目5（文字）タイトル",
                                "item_free_txt_title6": "明細の自由項目6（文字）タイトル",
                                "item_free_txt_title7": "明細の自由項目7（文字）タイトル",
                                "item_free_txt_title8": "明細の自由項目8（文字）タイトル",
                                "item_free_txt_title9": "明細の自由項目9（文字）タイトル",
                                "item_free_txt_title10": "明細の自由項目10（文字）タイトル",
                                "item_free_txt_l_title": "明細の自由項目11（文字）タイトル",
                            },
                            "wf_status": "10",
                            "seller_attached_file": [
                                {
                                    "file": "dGhpcyUyMGlzJTIwYSUyMHRlc3QlMjB0ZXh0",
                                    "file_name": "test.txt",
                                }
                            ],
                        }
                    ],
                },
            },
            ReceiveRecordStatus.INSERT_OK,
        ),
        # case 2 : 登録不可能なxmlで作成されたzipファイル
        (
            "../../storage/for_test/error.zip",
            {"send": None, "get_response": None},
            ReceiveRecordStatus.TRANSFORM_NG,
        ),
    ]


def test_zip_data_shaping_exception() -> list:
    """zip_data_shaping例外テストパラメータ"""
    return []


def test_is_duplicated_file() -> list[tuple[str, bool]]:
    """is_duplicated_fileテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        originXmlFileName="existing_xml_file.xml",
    )
    session.add(invoice)
    session.commit()
    return [
        # case 1 : 既に正規化済みのファイルを指定した場合True
        ("existing_xml_file.xml", True),
        # case 2 : 正規化されていないファイルを指定した場合False
        ("not_existing_xml_file.xml", False),
    ]


def test_is_duplicated_file_exception() -> list:
    """is_duplicated_file例外テストパラメータ"""
    return []


def test_fetch_peppol_id_info() -> list[tuple[CompanyInfo, dict]]:
    """fetch_peppol_id_infoテストパラメータ"""
    return [
        # case 1 : 正常系
        (
            CompanyInfo(esCompanyId=1),
            {
                "peppolId": "1111:peppolId",
                "apiId": "apiId",
                "password": "password",
                "authKey": "authKey",
            },
        )
    ]
