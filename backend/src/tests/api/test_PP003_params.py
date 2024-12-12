"""tests/api/test_PP003_params.py"""

import datetime
import logging
from typing import Any

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.peppol import BaseItem, invoiceLineInPeppolDetailItem
from core.constant import const
from core.message import messages
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo, Invoice, InvoiceDetail


def test_PP003() -> (
    list[tuple[int, CompanyInfo, list[int], None, BaseItem, dict[str, Any]]]
):
    """PP003APIテストパラメータ"""
    mock_invoice = Invoice(
        IBT024="unittestIBT024",
        IBT023="unittestIBT023",
        IBT001="unittestIBT001",
        IBT002=datetime.datetime(year=2024, month=5, day=27),
        IBT003="unittestIBT003",
        IBT009=datetime.datetime(year=2024, month=5, day=27),
        IBT022="unittestIBT022",
        IBT168="12:23:34",
        IBT005="unittestIBT005",
        IBT006="unittestIBT006",
        IBT007=datetime.datetime(year=2024, month=5, day=27),
        IBT019="unittestIBT019",
        IBT010="unittestIBT010",
        IBG14={"IBT-073": "2023-10-18", "IBT-074": "2023-10-18", "IBT-008": ""},
        AUTO2={"IBT-013": "O-998877", "IBT-014": "SO-12343"},
        IBG03=[{"AUTO-3": {"IBT-025": "123", "IBT-026": "2023-10-20"}}],
        AUTO4={"IBT-016": "despadv-3"},
        AUTO5={"IBT-015": "resadv-1"},
        AUTO6={"IBT-017": "ppid-123"},
        AUTO7={"IBT-012": "framework no 1"},
        AUTO8={"IBT-018": {"value": "DR35141", "schemeID": "147"}, "AUTO-9": "130"},
        IBG24=[
            {
                "IBT-122": "doc1",
                "IBT-123": "Usage summary",
                "AUTO-10": {
                    "IBT-125": {
                        "value": "aHR0cHM6Ly90ZXN0LXZlZmEuZGlmaS5uby8==",
                        "filename": "report.csv",
                        "mimeCode": "text/csv",
                    },
                    "AUTO-11": {
                        "IBT-124": "http://www.salescompany.com/breakdown001.html"
                    },
                },
            }
        ],
        AUTO12={"IBT-011": "project333"},
        IBG04={
            "AUTO-13": {
                "IBT-034": {"value": "", "schemeID": ""},
                "AUTO-14": [{"IBT-029": {"value": "", "schemeID": ""}}],
                "AUTO-15": {"IBT-090": {"value": "", "schemeID": ""}},
                "AUTO-17": {"IBT-028": ""},
                "IBG-05": {
                    "IBT-035": "",
                    "IBT-036": "",
                    "IBT-037": "",
                    "IBT-038": "",
                    "IBT-039": "",
                    "AUTO-18": {"IBT-162": ""},
                    "AUTO-19": {"IBT-040": ""},
                },
                "AUTO-20": {"IBT-031": "", "AUTO-21": {"IBT-031-1": ""}},
                "AUTO-22": {"IBT-032": "", "AUTO-23": {"AUTO-24": ""}},
                "AUTO-25": {
                    "IBT-027": "",
                    "IBT-030": {"value": "", "schemeID": ""},
                    "IBT-033": "",
                },
                "IBG-06": {"IBT-041": "", "IBT-042": "", "IBT-043": ""},
            }
        },
        IBG07={
            "AUTO-26": {
                "IBT-049": {"value": "1234567890123", "schemeID": "147"},
                "AUTO-27": {
                    "IBT-046": {"value": "654321:000321:0147:1", "schemeID": "147"}
                },
                "AUTO-28": {"IBT-045": "株式会社 〇〇物産"},
                "IBG-08": {
                    "IBT-050": "北区",
                    "IBT-051": "北十二条西76-X",
                    "IBT-052": "札幌市",
                    "IBT-053": "0010012",
                    "IBT-054": "北海道",
                    "AUTO-29": {"IBT-163": "9999-999"},
                    "AUTO-30": {"IBT-055": "JP"},
                },
                "AUTO-31": {
                    "IBT-048": "T3210987654321",
                    "AUTO-32": {"IBT-048-1": "VAT"},
                },
                "AUTO-33": {
                    "IBT-044": "株式会社 〇〇物産",
                    "IBT-047": {"value": "654321:000321:0147:1", "schemeID": "147"},
                },
                "IBG-09": {
                    "IBT-056": "株式会社 〇〇物産",
                    "IBT-057": "011-757-1xxx",
                    "IBT-058": "shirou_aoki@〇〇co.jp",
                },
            }
        },
        IBG10={
            "AUTO-34": {
                "IBT-060": {"value": "123456:000124:0147:1", "schemeID": "147"}
            },
            "AUTO-35": {"IBT-059": "Payee party"},
            "AUTO-36": {
                "IBT-061": {"value": "123456:000124:0147:1", "schemeID": "147"}
            },
        },
        IBG11={
            "AUTO-37": {"IBT-062": "TaxRepresentative Name"},
            "IBG-12": {
                "IBT-064": "四谷4-32-X",
                "IBT-065": "〇〇商事ビル",
                "IBT-066": "新宿区",
                "IBT-067": "1600044",
                "IBT-068": "東京都",
                "AUTO-38": {"IBT-164": "Third line"},
                "AUTO-39": {"IBT-069": "JP"},
            },
            "AUTO-40": {
                "IBT-063": "T7654321098765",
                "AUTO-41": {"IBT-063-1": "VAT"},
            },
        },
        IBG13={
            "IBT-072": "2023-10-18",
            "AUTO-42": {
                "IBT-071": {"value": "123456:000123:0147:1", "schemeID": "147"},
                "IBG-15": {
                    "IBT-075": "北区",
                    "IBT-076": "北十二条西76-X",
                    "IBT-077": "札幌市",
                    "IBT-078": "0010012",
                    "IBT-079": "北海道",
                    "AUTO-43": {"IBT-165": "Gate 15"},
                    "AUTO-44": {"IBT-080": "JP"},
                },
            },
            "AUTO-45": {"AUTO-46": {"IBT-070": "株式会社 〇〇物産 札幌支社"}},
        },
        IBG16=[
            {
                "IBT-178": "",
                "IBT-081": {"value": "30", "name": "Credit transfer"},
                "IBT-083": [{"value": "", "schemeID": "147"}],
                "IBG-18": {"IBT-087": "", "AUTO-47": "", "IBT-088": ""},
                "IBG-17": {
                    "IBT-084": {"value": "1234:567:1:3242394", "schemeID": "147"},
                    "IBT-085": "ｶ)ﾏﾙﾏﾙｼﾖｳｼﾞ",
                    "AUTO-48": {
                        "IBT-086": "",
                        "IBG-34": {
                            "IBT-169": "",
                            "IBT-170": "",
                            "IBT-171": "",
                            "IBT-172": "",
                            "IBT-173": "",
                            "AUTO-49": {"IBT-174": ""},
                            "AUTO-50": {"IBT-175": ""},
                        },
                    },
                },
                "IBG-19": {"IBT-089": "", "AUTO-51": {"IBT-091": ""}},
            }
        ],
        IBG33=[
            {
                "IBT-187": "JP",
                "IBT-020": "月末締め翌月20日払い, 銀行手数料振込人負担",
                "IBT-176": {"value": "1000", "currencyID": "JPY"},
                "IBT-177": "2023-09-15",
            }
        ],
        IBG35=[
            {
                "IBT-179": "12345",
                "IBT-180": {"value": "123000", "currencyID": "JPY"},
                "IBT-181": "2023-10-18",
                "IBT-182": "Aa",
            }
        ],
        IBG20=[
            {
                "AUTO-54": False,
                "IBT-098": "95",
                "IBT-097": "値引",
                "IBT-094": "10",
                "IBT-092": {"value": "30000", "currencyID": "JPY"},
                "IBT-093": {"value": "30000", "currencyID": "JPY"},
                "AUTO-57": {
                    "IBT-095": "S",
                    "IBT-096": "10",
                    "AUTO-58": {"IBT-095-1": "VAT"},
                },
            }
        ],
        IBG21=[
            {
                "AUTO-59": True,
                "IBT-105": "FC",
                "IBT-104": "配送サービス",
                "IBT-101": "10",
                "IBT-099": {"value": "30000", "currencyID": "JPY"},
                "IBT-100": {"value": "30000", "currencyID": "JPY"},
                "AUTO-62": {
                    "IBT-102": "S",
                    "IBT-103": "10",
                    "AUTO-63": {"IBT-102-1": "VAT"},
                },
            }
        ],
        AUTO64={
            "IBT-110": {"value": "26000", "currencyID": "JPY"},
            "IBG-23": [
                {
                    "IBT-116": {"value": "260000", "currencyID": "JPY"},
                    "IBT-117": {"value": "26000", "currencyID": "JPY"},
                    "AUTO-68": {
                        "IBT-118": "S",
                        "IBT-119": "10",
                        "AUTO-69": {"IBT-118-1": "VAT"},
                    },
                }
            ],
        },
        IBG37={
            "IBT-111": {"value": "26000", "currencyID": "JPY"},
            "IBG-38": [
                {
                    "IBT-190": {"value": "26000", "currencyID": "JPY"},
                    "AUTO-72": {"IBT-192": "S", "IBT-193": "10"},
                }
            ],
        },
        IBG22={
            "IBT-106": {"value": "255990", "currencyID": "JPY"},
            "IBT-109": {"value": "263490", "currencyID": "JPY"},
            "IBT-112": {"value": "289490", "currencyID": "JPY"},
            "IBT-107": {"value": "179", "currencyID": "JPY"},
            "IBT-108": {"value": "7679", "currencyID": "JPY"},
            "IBT-113": {"value": "0", "currencyID": "JPY"},
            "IBT-114": {"value": "0", "currencyID": "JPY"},
            "IBT-115": {"value": "289490", "currencyID": "JPY"},
        },
    )

    mock_details = [
        InvoiceDetail(
            id=1,
            IBT126="unittestIBT126",
            IBG31={
                "IBT-154": "",
                "IBT-153": "デスクチェア",
                "AUTO-95": {"IBT-156": "b-13214"},
                "AUTO-96": {"IBT-155": "97iugug876"},
                "AUTO-97": {"IBT-157": {"value": "4503994155481", "schemeID": "147"}},
                "AUTO-98": {"IBT-159": "JP"},
                "AUTO-99": [
                    {
                        "IBT-158": {
                            "value": "86776",
                            "listID": "TST",
                            "listVersionID": "19.05.01",
                        }
                    }
                ],
                "IBG-30": [
                    {
                        "IBT-151": "S",
                        "IBT-152": "10",
                        "IBT-166": {"value": "0", "currencyID": "JPY"},
                        "AUTO-101": {"IBT-167": "VAT"},
                    }
                ],
                "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "脚"}],
            },
            IBG29={
                "IBT-146": {"value": "50000", "currencyID": "JPY"},
                "IBT-149": {"value": "1", "unitCode": "H87"},
                "AUTO-103": {
                    "AUTO-104": False,
                    "IBT-147": {"value": "100", "currencyID": "JPY"},
                    "IBT-148": {"value": "600", "currencyID": "JPY"},
                },
            },
            IBT131={"value": "250000", "currencyID": "JPY"},
            IBG26={"IBT-134": "2023-09-15", "IBT-135": "2023-09-15"},
            IBG36={"IBT-188": "D001-1", "IBT-189": "12345"},
        )
    ]

    return [
        # case 1 : invoice_id:1のpeppol詳細を取得
        (
            1,
            CompanyInfo(
                id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
            ),
            [1],
            None,
            BaseItem(
                IBT003=mock_invoice.IBT003,
                IBT001=mock_invoice.IBT001,
                IBT002=mock_invoice.IBT002.strftime(const.DATE_FORMAT),
                IBT009=mock_invoice.IBT009.strftime(const.DATE_FORMAT),
                IBT022=mock_invoice.IBT022,
                IBT168=mock_invoice.IBT168.strftime(const.TIME_FORMAT),
                IBT005=mock_invoice.IBT005,
                IBT006=mock_invoice.IBT006,
                IBT007=mock_invoice.IBT007.strftime(const.DATE_FORMAT),
                IBT010=mock_invoice.IBT010,
                IBG14=mock_invoice.IBG14,
                AUTO12=mock_invoice.AUTO12,
                AUTO7=mock_invoice.AUTO7,
                AUTO2=mock_invoice.AUTO2,
                AUTO5=mock_invoice.AUTO5,
                AUTO4=mock_invoice.AUTO4,
                AUTO6=mock_invoice.AUTO6,
                AUTO8=mock_invoice.AUTO8,
                IBT019=mock_invoice.IBT019,
                IBT024=mock_invoice.IBT024,
                IBT023=mock_invoice.IBT023,
                IBG33=mock_invoice.IBG33,
                IBG03=mock_invoice.IBG03,
                IBG24=mock_invoice.IBG24,
                IBG04=mock_invoice.IBG04,
                IBG07=mock_invoice.IBG07,
                IBG10=mock_invoice.IBG10,
                IBG11=mock_invoice.IBG11,
                IBG13=mock_invoice.IBG13,
                IBG16=mock_invoice.IBG16,
                IBG35=mock_invoice.IBG35,
                IBG20=mock_invoice.IBG20,
                IBG21=mock_invoice.IBG21,
                IBG22=mock_invoice.IBG22,
                AUTO64=mock_invoice.AUTO64,
                IBG37=mock_invoice.IBG37,
                invoiceLineInPeppolDetail=[
                    invoiceLineInPeppolDetailItem(
                        id=record.id,
                        IBT126=record.IBT126,
                        IBG31=record.IBG31,
                        IBG29=record.IBG29,
                        IBT131=record.IBT131,
                        IBG26=record.IBG26,
                        IBG36=record.IBG36,
                    )
                    for record in mock_details
                ],
            ),
            {
                "header": {"code": "", "message": ""},
                "payload": {
                    "IBT-003": "unittestIBT003",
                    "IBT-001": "unittestIBT001",
                    "IBT-002": "2024-05-27",
                    "IBT-009": "2024-05-27",
                    "IBT-022": "unittestIBT022",
                    "IBT-168": "12:23:34",
                    "IBT-005": "unittestIBT005",
                    "IBT-006": "unittestIBT006",
                    "IBT-007": "2024-05-27",
                    "IBT-010": "unittestIBT010",
                    "IBG-14": {
                        "IBT-073": "2023-10-18",
                        "IBT-074": "2023-10-18",
                        "IBT-008": "",
                    },
                    "AUTO-12": {"IBT-011": "project333"},
                    "AUTO-7": {"IBT-012": "framework no 1"},
                    "AUTO-2": {"IBT-013": "O-998877", "IBT-014": "SO-12343"},
                    "AUTO-5": {"IBT-015": "resadv-1"},
                    "AUTO-4": {"IBT-016": "despadv-3"},
                    "AUTO-6": {"IBT-017": "ppid-123"},
                    "AUTO-8": {
                        "IBT-018": {"value": "DR35141", "schemeID": "147"},
                        "AUTO-9": "130",
                    },
                    "IBT-019": "unittestIBT019",
                    "IBT-024": "unittestIBT024",
                    "IBT-023": "unittestIBT023",
                    "IBG-33": [
                        {
                            "IBT-187": "JP",
                            "IBT-020": "月末締め翌月20日払い, 銀行手数料振込人負担",
                            "IBT-176": {"value": "1000", "currencyID": "JPY"},
                            "IBT-177": "2023-09-15",
                        }
                    ],
                    "IBG-03": [{"AUTO-3": {"IBT-025": "123", "IBT-026": "2023-10-20"}}],
                    "IBG-24": [
                        {
                            "IBT-122": "doc1",
                            "IBT-123": "Usage summary",
                            "AUTO-10": {
                                "IBT-125": {
                                    "value": "aHR0cHM6Ly90ZXN0LXZlZmEuZGlmaS5uby8==",
                                    "filename": "report.csv",
                                    "mimeCode": "text/csv",
                                },
                                "AUTO-11": {
                                    "IBT-124": "http://www.salescompany.com/breakdown001.html"
                                },
                            },
                        }
                    ],
                    "IBG-04": {
                        "AUTO-13": {
                            "IBT-034": {"value": "", "schemeID": ""},
                            "AUTO-14": [{"IBT-029": {"value": "", "schemeID": ""}}],
                            "AUTO-15": {"IBT-090": {"value": "", "schemeID": ""}},
                            "AUTO-17": {"IBT-028": ""},
                            "IBG-05": {
                                "IBT-035": "",
                                "IBT-036": "",
                                "IBT-037": "",
                                "IBT-038": "",
                                "IBT-039": "",
                                "AUTO-18": {"IBT-162": ""},
                                "AUTO-19": {"IBT-040": ""},
                            },
                            "AUTO-20": {"IBT-031": "", "AUTO-21": {"IBT-031-1": ""}},
                            "AUTO-22": {"IBT-032": "", "AUTO-23": {"AUTO-24": ""}},
                            "AUTO-25": {
                                "IBT-027": "",
                                "IBT-030": {"value": "", "schemeID": ""},
                                "IBT-033": "",
                            },
                            "IBG-06": {"IBT-041": "", "IBT-042": "", "IBT-043": ""},
                        }
                    },
                    "IBG-07": {
                        "AUTO-26": {
                            "IBT-049": {"value": "1234567890123", "schemeID": "147"},
                            "AUTO-27": {
                                "IBT-046": {
                                    "value": "654321:000321:0147:1",
                                    "schemeID": "147",
                                }
                            },
                            "AUTO-28": {"IBT-045": "株式会社 〇〇物産"},
                            "IBG-08": {
                                "IBT-050": "北区",
                                "IBT-051": "北十二条西76-X",
                                "IBT-052": "札幌市",
                                "IBT-053": "0010012",
                                "IBT-054": "北海道",
                                "AUTO-29": {"IBT-163": "9999-999"},
                                "AUTO-30": {"IBT-055": "JP"},
                            },
                            "AUTO-31": {
                                "IBT-048": "T3210987654321",
                                "AUTO-32": {"IBT-048-1": "VAT"},
                            },
                            "AUTO-33": {
                                "IBT-044": "株式会社 〇〇物産",
                                "IBT-047": {
                                    "value": "654321:000321:0147:1",
                                    "schemeID": "147",
                                },
                            },
                            "IBG-09": {
                                "IBT-056": "株式会社 〇〇物産",
                                "IBT-057": "011-757-1xxx",
                                "IBT-058": "shirou_aoki@〇〇co.jp",
                            },
                        }
                    },
                    "IBG-10": {
                        "AUTO-34": {
                            "IBT-060": {
                                "value": "123456:000124:0147:1",
                                "schemeID": "147",
                            }
                        },
                        "AUTO-35": {"IBT-059": "Payee party"},
                        "AUTO-36": {
                            "IBT-061": {
                                "value": "123456:000124:0147:1",
                                "schemeID": "147",
                            }
                        },
                    },
                    "IBG-11": {
                        "AUTO-37": {"IBT-062": "TaxRepresentative Name"},
                        "IBG-12": {
                            "IBT-064": "四谷4-32-X",
                            "IBT-065": "〇〇商事ビル",
                            "IBT-066": "新宿区",
                            "IBT-067": "1600044",
                            "IBT-068": "東京都",
                            "AUTO-38": {"IBT-164": "Third line"},
                            "AUTO-39": {"IBT-069": "JP"},
                        },
                        "AUTO-40": {
                            "IBT-063": "T7654321098765",
                            "AUTO-41": {"IBT-063-1": "VAT"},
                        },
                    },
                    "IBG-13": {
                        "IBT-072": "2023-10-18",
                        "AUTO-42": {
                            "IBT-071": {
                                "value": "123456:000123:0147:1",
                                "schemeID": "147",
                            },
                            "IBG-15": {
                                "IBT-075": "北区",
                                "IBT-076": "北十二条西76-X",
                                "IBT-077": "札幌市",
                                "IBT-078": "0010012",
                                "IBT-079": "北海道",
                                "AUTO-43": {"IBT-165": "Gate 15"},
                                "AUTO-44": {"IBT-080": "JP"},
                            },
                        },
                        "AUTO-45": {
                            "AUTO-46": {"IBT-070": "株式会社 〇〇物産 札幌支社"}
                        },
                    },
                    "IBG-16": [
                        {
                            "IBT-178": "",
                            "IBT-081": {"value": "30", "name": "Credit transfer"},
                            "IBT-083": [{"value": "", "schemeID": "147"}],
                            "IBG-18": {"IBT-087": "", "AUTO-47": "", "IBT-088": ""},
                            "IBG-17": {
                                "IBT-084": {
                                    "value": "1234:567:1:3242394",
                                    "schemeID": "147",
                                },
                                "IBT-085": "ｶ)ﾏﾙﾏﾙｼﾖｳｼﾞ",
                                "AUTO-48": {
                                    "IBT-086": "",
                                    "IBG-34": {
                                        "IBT-169": "",
                                        "IBT-170": "",
                                        "IBT-171": "",
                                        "IBT-172": "",
                                        "IBT-173": "",
                                        "AUTO-49": {"IBT-174": ""},
                                        "AUTO-50": {"IBT-175": ""},
                                    },
                                },
                            },
                            "IBG-19": {"IBT-089": "", "AUTO-51": {"IBT-091": ""}},
                        }
                    ],
                    "IBG-35": [
                        {
                            "IBT-179": "12345",
                            "IBT-180": {"value": "123000", "currencyID": "JPY"},
                            "IBT-181": "2023-10-18",
                            "IBT-182": "Aa",
                        }
                    ],
                    "IBG-20": [
                        {
                            "AUTO-54": False,
                            "IBT-098": "95",
                            "IBT-097": "値引",
                            "IBT-094": "10",
                            "IBT-092": {"value": "30000", "currencyID": "JPY"},
                            "IBT-093": {"value": "30000", "currencyID": "JPY"},
                            "AUTO-57": {
                                "IBT-095": "S",
                                "IBT-096": "10",
                                "AUTO-58": {"IBT-095-1": "VAT"},
                            },
                        }
                    ],
                    "IBG-21": [
                        {
                            "AUTO-59": True,
                            "IBT-105": "FC",
                            "IBT-104": "配送サービス",
                            "IBT-101": "10",
                            "IBT-099": {"value": "30000", "currencyID": "JPY"},
                            "IBT-100": {"value": "30000", "currencyID": "JPY"},
                            "AUTO-62": {
                                "IBT-102": "S",
                                "IBT-103": "10",
                                "AUTO-63": {"IBT-102-1": "VAT"},
                            },
                        }
                    ],
                    "IBG-22": {
                        "IBT-106": {"value": "255990", "currencyID": "JPY"},
                        "IBT-109": {"value": "263490", "currencyID": "JPY"},
                        "IBT-112": {"value": "289490", "currencyID": "JPY"},
                        "IBT-107": {"value": "179", "currencyID": "JPY"},
                        "IBT-108": {"value": "7679", "currencyID": "JPY"},
                        "IBT-113": {"value": "0", "currencyID": "JPY"},
                        "IBT-114": {"value": "0", "currencyID": "JPY"},
                        "IBT-115": {"value": "289490", "currencyID": "JPY"},
                    },
                    "AUTO-64": {
                        "IBT-110": {"value": "26000", "currencyID": "JPY"},
                        "IBG-23": [
                            {
                                "IBT-116": {"value": "260000", "currencyID": "JPY"},
                                "IBT-117": {"value": "26000", "currencyID": "JPY"},
                                "AUTO-68": {
                                    "IBT-118": "S",
                                    "IBT-119": "10",
                                    "AUTO-69": {"IBT-118-1": "VAT"},
                                },
                            }
                        ],
                    },
                    "IBG-37": {
                        "IBT-111": {"value": "26000", "currencyID": "JPY"},
                        "IBG-38": [
                            {
                                "IBT-190": {"value": "26000", "currencyID": "JPY"},
                                "AUTO-72": {"IBT-192": "S", "IBT-193": "10"},
                            }
                        ],
                    },
                    "invoiceLineInPeppolDetail": [
                        {
                            "id": 1,
                            "IBT-126": "unittestIBT126",
                            "IBG-31": {
                                "IBT-154": "",
                                "IBT-153": "デスクチェア",
                                "AUTO-95": {"IBT-156": "b-13214"},
                                "AUTO-96": {"IBT-155": "97iugug876"},
                                "AUTO-97": {
                                    "IBT-157": {
                                        "value": "4503994155481",
                                        "schemeID": "147",
                                    }
                                },
                                "AUTO-98": {"IBT-159": "JP"},
                                "AUTO-99": [
                                    {
                                        "IBT-158": {
                                            "value": "86776",
                                            "listID": "TST",
                                            "listVersionID": "19.05.01",
                                        }
                                    }
                                ],
                                "IBG-30": [
                                    {
                                        "IBT-151": "S",
                                        "IBT-152": "10",
                                        "IBT-166": {"value": "0", "currencyID": "JPY"},
                                        "AUTO-101": {"IBT-167": "VAT"},
                                    }
                                ],
                                "IBG-32": [
                                    {"IBT-160": "表示単位名称", "IBT-161": "脚"}
                                ],
                            },
                            "IBG-29": {
                                "IBT-146": {"value": "50000", "currencyID": "JPY"},
                                "IBT-149": {"value": "1", "unitCode": "H87"},
                                "AUTO-103": {
                                    "AUTO-104": False,
                                    "IBT-147": {"value": "100", "currencyID": "JPY"},
                                    "IBT-148": {"value": "600", "currencyID": "JPY"},
                                },
                            },
                            "IBT-131": {"value": "250000", "currencyID": "JPY"},
                            "IBG-26": {
                                "IBT-134": "2023-09-15",
                                "IBT-135": "2023-09-15",
                            },
                            "IBG-36": {"IBT-188": "D001-1", "IBT-189": "12345"},
                        }
                    ],
                },
            },
        ),
    ]


test_PP003_exception = [
    (
        # case 1 : I0001: invoice_idが数値ではない
        "a",
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoice_id is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case2 : I0002: 該当請求書レコードが存在しない
        1,
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_DATA_NOT_FOUND_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                }
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case3 : I0003: 該当請求書明細レコードが存在しない
        1,
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                }
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case4 : I0004: 指定したcompany_infos_idが所属企業、結合企業に該当しない
        1,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case5 : E9999: サーバーエラー
        1,
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INTERNAL_SERVER_ERROR.code,
                message=messages.INTERNAL_SERVER_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
]
