"""tests/api/test_PP002_params.py"""

import datetime
import logging
from typing import Any

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoice import (
    AdditionalInfoItem,
    BanksItem,
    CustomerItem,
    DetailsItem,
    InvoiceBaseItem,
    ListInfoItem,
    PaidInfoItem,
    PublisherItem,
    RefundInfoItem,
    SellerAttachedFileItem,
)
from core.constant import const
from core.message import messages
from enums import (
    DataType,
    InputTaxType,
    IsConfirmation,
    IsDownload,
    PaymentMethod,
    ReducedTaxFlg,
    SumExemptFlg,
    TaxCalcType,
    TaxType,
)
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo, Invoice


def test_PP002() -> (
    list[tuple[int, CompanyInfo, list[int], InvoiceBaseItem, dict[str, Any]]]
):
    """PP002APIテストパラメータ"""
    mock_invoice = Invoice(
        isConfirmation=IsConfirmation.CONFIRMED,
        isDownload=IsDownload.DOWNLOADED,
        IBT005="unittestIBT005",
        inv_no="1",
        invoice_title="unittestInvoiceTitle",
        list_info=ListInfoItem(
            product_sec="unittestProductSec",
            private_user_name="unittestPrivateUserName",
            approver_name="unittestApproverName",
            billing_name="unittestBillingName",
            issue_user_name="unittestIssueUserName",
            phone="unittestPhone",
            send_date="unittestSendDate",
            remind_date="unittestRemindDate",
            seal_flg=False,
            fax_send_flg=False,
            qa_history=False,
            seal_date="unittestSealDate",
            destination_code="unittestDestinationCode",
            destination_name="unittestDestinationName",
        ),
        pay_due_date=datetime.datetime(year=2024, month=5, day=27),
        inv_amount=100000,
        payment_method=PaymentMethod.BANK_TRANSFER,
        publisher=PublisherItem(
            publisher_peppol_scheme_id="unittestPublisherPeppolSchemeId",
            publisher_peppol_id="unittestPublisherPeppolId",
            publisher_corp_genuine_id=1,
            publisher_tax_corp_id="unittestPublisherTaxCorpId",
            publisher_mail="unittestPublisherMail",
            publisher_company_name_org="unittestPublisherCompanyNameOrg",
            publisher_mng_num="unittestPublisherMngNum",
            publisher_company_name="unittestPublisherCompanyName",
            publisher_section="unittestPublisherSection",
            publisher_zip="unittestPublisherZip",
            publisher_country_subentity="unittestPublisherCountrySubentity",
            publisher_city_name="unittestPublisherCityName",
            publisher_street_name="unittestPublisherStreetName",
            publisher_phone="unittestPublisherPhone",
            biz_type="unittestBizType",
            biz_regist_no="unittestBizRegistNo",
            nta_biz_regist_no_result="unittestNtaBizRegistNoResult",
            nta_registered_date="unittestNtaRegisteredDate",
            nta_process="unittestNtaProcess",
            nta_company_name="unittestNtaCompanyName",
            nta_area="unittestNtaArea",
            nta_address="unittestNtaAddress",
            nta_update_date="unittestNtaUpdateDate",
            nta_trade_name="unittestNtaTradeName",
            nta_common_name="unittestNtaCommonName",
            nta_cancel_date="unittestNtaCancelData",
            nta_lapse_date="unittestNtaLapseDate",
        ),
        banks=[
            BanksItem(
                transfer_code="unittestTransferCode",
                fncl_inst_code="unittestFnclInstCode",
                fncl_inst_name="unittestFnclInstName",
                fncl_inst_kana="unittestFnclInstKana",
                branch_code="unittestBranchCode",
                branch_name="unittestBranchName",
                branch_kana="unittestBranchKana",
                deposit_sec="unittestDepositSec",
                account_num="unittestAccountNum",
                depositor_name="unittestDepositorName",
                depositor_kana="unittestDepositorKana",
            )
        ],
        data_type=DataType.STANDARD,
        customer=CustomerItem(
            peppol_scheme_id="unittestPeppolSchemeId",
            peppol_id="unittestPeppolId",
            tax_corp_id="unittestTaxCorpId",
            private_cust_cd="unittestPrivateCustCd",
            corp_genuine_id=1,
            company_name_org="unittestCompanyNameOrg",
            zip="unittestZip",
            country_subentity="unittestCountrySubentity",
            city_name="unittestCityName",
            street_name="unittestStreetName",
            user_email="unittestUserEmail",
            phone="unittestPhone",
        ),
        seller_attached_file=[
            SellerAttachedFileItem(file="unittestFile", file_name="unittestFileName")
        ],
        remarks="unittestRemarks",
        inv_tax=1000,
        inv_without_tax_tr10=1000,
        inv_without_tax_tr8=1000,
        inv_without_tax_tr8_reduced=1000,
        inv_without_tax_tr5=1000,
        inv_without_tax_tr0=1000,
        inv_without_tax_free=1000,
        inv_without_tax_non=1000,
        inv_without_tax_exemption=1000,
        inv_tax_tr10=1000,
        inv_tax_tr8=1000,
        inv_tax_tr8_reduced=1000,
        inv_tax_tr5=1000,
        inv_tax_tr0=1000,
        inv_tax_free=1000,
        inv_tax_non=1000,
        inv_tax_exemption=1000,
        inv_amount_tr10=1000,
        inv_amount_tr8=1000,
        inv_amount_tr8_reduced=1000,
        inv_amount_tr5=1000,
        inv_amount_tr0=1000,
        inv_amount_free=1000,
        inv_amount_non=1000,
        inv_amount_exemption=1000,
        paid_info=[
            PaidInfoItem(
                paid_without_tax=1000,
            )
        ],
        refund_info=[
            RefundInfoItem(
                refund_without_tax=10000,
                tax_type=TaxType.TAX,
                tax_rate_sec=10,
                reduced_tax_flg=ReducedTaxFlg.REDUCED,
            )
        ],
        additional_info=[
            AdditionalInfoItem(
                additional_without_tax=10000,
                tax_type=TaxType.TAX,
                tax_rate_sec=10,
                reduced_tax_flg=ReducedTaxFlg.REDUCED,
            )
        ],
        details=[
            DetailsItem(
                item_slip_date="unittestItemSlipDate",
                item_slip_no="unittestItemSlipNo",
                item_prod_code="unittestItemProdCode",
                item_name="unittestItemName",
                item_qty=1,
                item_price=100,
                item_unit="unittestItemUnit",
                item_without_tax=10000,
                item_tax=1000,
                item_amount=11000,
                item_sec_code="unittestItemSecCode",
                item_sec_name="unittestItemSecName",
                detail_remarks="unittestDetailRemarks",
                item_free_txt1="unittestItemFreeTxt",
                item_free_txt2="unittestItemFreeTxt2",
                item_free_txt3="unittestItemFreeTxt3",
                item_free_txt4="unittestItemFreeTxt4",
                item_free_txt5="unittestItemFreeTxt5",
                item_free_txt6="unittestItemFreeTxt6",
                item_free_txt7="unittestItemFreeTxt7",
                item_free_txt8="unittestItemFreeTxt8",
                item_free_txt9="unittestItemFreeTxt9",
                item_free_txt10="unittestItemFreeTxt10",
                item_free_txt_l="unittestItemFreeTxtl",
                tax_type=TaxType.TAX,
                tax_rate_sec=10,
                reduced_tax_flg=ReducedTaxFlg.REDUCED,
                input_tax_type=InputTaxType.INPUT_TAX,
                tax_calc_type=TaxCalcType.WITH_OUT_TAX,
                sum_exempt_flg=SumExemptFlg.SUM_EXEMPT,
            )
        ],
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
    )

    return [
        (
            # case 1 : invoice_id:1の請求書を取得
            1,
            CompanyInfo(
                id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
            ),
            [1],
            InvoiceBaseItem(
                isConfirmation=mock_invoice.isConfirmation,
                isDownload=mock_invoice.isDownload,
                currencyCode=mock_invoice.IBT005,
                inv_no=mock_invoice.inv_no,
                invoice_title=mock_invoice.invoice_title,
                list_info=mock_invoice.list_info,
                pay_due_date=(mock_invoice.pay_due_date.strftime(const.DATE_FORMAT)),
                inv_amount=mock_invoice.inv_amount,
                payment_method=mock_invoice.payment_method,
                publisher=mock_invoice.publisher,
                banks=mock_invoice.banks,
                data_type=mock_invoice.data_type,
                customer=mock_invoice.customer,
                seller_attached_file=mock_invoice.seller_attached_file,
                remarks=mock_invoice.remarks,
                inv_without_tax=mock_invoice.inv_without_tax,
                inv_tax=mock_invoice.inv_tax,
                inv_without_tax_tr10=mock_invoice.inv_without_tax_tr10,
                inv_without_tax_tr8=mock_invoice.inv_without_tax_tr8,
                inv_without_tax_tr8_reduced=mock_invoice.inv_without_tax_tr8_reduced,
                inv_without_tax_tr5=mock_invoice.inv_without_tax_tr5,
                inv_without_tax_tr0=mock_invoice.inv_without_tax_tr0,
                inv_without_tax_free=mock_invoice.inv_without_tax_free,
                inv_without_tax_non=mock_invoice.inv_without_tax_non,
                inv_without_tax_exemption=mock_invoice.inv_without_tax_exemption,
                inv_tax_tr10=mock_invoice.inv_tax_tr10,
                inv_tax_tr8=mock_invoice.inv_tax_tr8,
                inv_tax_tr8_reduced=mock_invoice.inv_tax_tr8_reduced,
                inv_tax_tr5=mock_invoice.inv_tax_tr5,
                inv_tax_tr0=mock_invoice.inv_tax_tr0,
                inv_tax_free=mock_invoice.inv_tax_free,
                inv_tax_non=mock_invoice.inv_tax_non,
                inv_tax_exemption=mock_invoice.inv_tax_exemption,
                inv_amount_tr10=mock_invoice.inv_amount_tr10,
                inv_amount_tr8=mock_invoice.inv_amount_tr8,
                inv_amount_tr8_reduced=mock_invoice.inv_amount_tr8_reduced,
                inv_amount_tr5=mock_invoice.inv_amount_tr5,
                inv_amount_tr0=mock_invoice.inv_amount_tr0,
                inv_amount_free=mock_invoice.inv_amount_free,
                inv_amount_non=mock_invoice.inv_amount_non,
                inv_amount_exemption=mock_invoice.inv_amount_exemption,
                paid_info=mock_invoice.paid_info,
                refund_info=mock_invoice.refund_info,
                additional_info=mock_invoice.additional_info,
                details=mock_invoice.details,
                IBG04=mock_invoice.IBG04,
                IBG07=mock_invoice.IBG07,
            ),
            {
                "header": {"code": "", "message": ""},
                "payload": {
                    "isConfirmation": 1,
                    "isDownload": 1,
                    "currencyCode": "unittestIBT005",
                    "inv_no": "1",
                    "invoice_title": "unittestInvoiceTitle",
                    "list_info": {
                        "product_sec": "unittestProductSec",
                        "private_user_name": "unittestPrivateUserName",
                        "approver_name": "unittestApproverName",
                        "billing_name": "unittestBillingName",
                        "issue_user_name": "unittestIssueUserName",
                        "phone": "unittestPhone",
                        "send_date": "unittestSendDate",
                        "remind_date": "unittestRemindDate",
                        "seal_flg": False,
                        "fax_send_flg": False,
                        "qa_history": False,
                        "seal_date": "unittestSealDate",
                        "destination_code": "unittestDestinationCode",
                        "destination_name": "unittestDestinationName",
                    },
                    "pay_due_date": "2024-05-27",
                    "inv_amount": 100000,
                    "payment_method": 0,
                    "publisher": {
                        "publisher_peppol_scheme_id": "unittestPublisherPeppolSchemeId",
                        "publisher_peppol_id": "unittestPublisherPeppolId",
                        "publisher_corp_genuine_id": 1,
                        "publisher_tax_corp_id": "unittestPublisherTaxCorpId",
                        "publisher_mail": "unittestPublisherMail",
                        "publisher_company_name_org": "unittestPublisherCompanyNameOrg",
                        "publisher_mng_num": "unittestPublisherMngNum",
                        "publisher_company_name": "unittestPublisherCompanyName",
                        "publisher_section": "unittestPublisherSection",
                        "publisher_zip": "unittestPublisherZip",
                        "publisher_country_subentity": "unittestPublisherCountrySubentity",
                        "publisher_city_name": "unittestPublisherCityName",
                        "publisher_street_name": "unittestPublisherStreetName",
                        "publisher_phone": "unittestPublisherPhone",
                        "biz_type": "unittestBizType",
                        "biz_regist_no": "unittestBizRegistNo",
                        "nta_biz_regist_no_result": "unittestNtaBizRegistNoResult",
                        "nta_registered_date": "unittestNtaRegisteredDate",
                        "nta_process": "unittestNtaProcess",
                        "nta_company_name": "unittestNtaCompanyName",
                        "nta_area": "unittestNtaArea",
                        "nta_address": "unittestNtaAddress",
                        "nta_update_date": "unittestNtaUpdateDate",
                        "nta_trade_name": "unittestNtaTradeName",
                        "nta_common_name": "unittestNtaCommonName",
                        "nta_cancel_date": "unittestNtaCancelData",
                        "nta_lapse_date": "unittestNtaLapseDate",
                    },
                    "banks": [
                        {
                            "transfer_code": "unittestTransferCode",
                            "fncl_inst_code": "unittestFnclInstCode",
                            "fncl_inst_name": "unittestFnclInstName",
                            "fncl_inst_kana": "unittestFnclInstKana",
                            "branch_code": "unittestBranchCode",
                            "branch_name": "unittestBranchName",
                            "branch_kana": "unittestBranchKana",
                            "deposit_sec": "unittestDepositSec",
                            "account_num": "unittestAccountNum",
                            "depositor_name": "unittestDepositorName",
                            "depositor_kana": "unittestDepositorKana",
                        }
                    ],
                    "data_type": 1,
                    "customer": {
                        "peppol_scheme_id": "unittestPeppolSchemeId",
                        "peppol_id": "unittestPeppolId",
                        "tax_corp_id": "unittestTaxCorpId",
                        "private_cust_cd": "unittestPrivateCustCd",
                        "corp_genuine_id": 1,
                        "company_name_org": "unittestCompanyNameOrg",
                        "zip": "unittestZip",
                        "country_subentity": "unittestCountrySubentity",
                        "city_name": "unittestCityName",
                        "street_name": "unittestStreetName",
                        "user_email": "unittestUserEmail",
                        "phone": "unittestPhone",
                    },
                    "seller_attached_file": [
                        {"file": "unittestFile", "file_name": "unittestFileName"}
                    ],
                    "remarks": "unittestRemarks",
                    "inv_without_tax": None,
                    "inv_tax": 1000,
                    "inv_without_tax_tr10": 1000,
                    "inv_without_tax_tr8": 1000,
                    "inv_without_tax_tr8_reduced": 1000,
                    "inv_without_tax_tr5": 1000,
                    "inv_without_tax_tr0": 1000,
                    "inv_without_tax_free": 1000,
                    "inv_without_tax_non": 1000,
                    "inv_without_tax_exemption": 1000,
                    "inv_tax_tr10": 1000,
                    "inv_tax_tr8": 1000,
                    "inv_tax_tr8_reduced": 1000,
                    "inv_tax_tr5": 1000,
                    "inv_tax_tr0": 1000,
                    "inv_tax_free": 1000,
                    "inv_tax_non": 1000,
                    "inv_tax_exemption": 1000,
                    "inv_amount_tr10": 1000,
                    "inv_amount_tr8": 1000,
                    "inv_amount_tr8_reduced": 1000,
                    "inv_amount_tr5": 1000,
                    "inv_amount_tr0": 1000,
                    "inv_amount_free": 1000,
                    "inv_amount_non": 1000,
                    "inv_amount_exemption": 1000,
                    "paid_info": {
                        "paid_without_tax": 1000,
                    },
                    "refund_info": {
                        "refund_without_tax": 10000,
                        "tax_type": "0",
                        "tax_rate_sec": 10,
                        "reduced_tax_flg": "1",
                    },
                    "additional_info": {
                        "additional_without_tax": 10000,
                        "tax_type": "0",
                        "tax_rate_sec": 10,
                        "reduced_tax_flg": "1",
                    },
                    "details": [
                        {
                            "item_slip_date": "unittestItemSlipDate",
                            "item_slip_no": "unittestItemSlipNo",
                            "item_prod_code": "unittestItemProdCode",
                            "item_name": "unittestItemName",
                            "item_qty": 1,
                            "item_price": 100,
                            "item_unit": "unittestItemUnit",
                            "item_without_tax": 10000,
                            "item_tax": 1000,
                            "item_amount": 11000,
                            "item_sec_code": "unittestItemSecCode",
                            "item_sec_name": "unittestItemSecName",
                            "detail_remarks": "unittestDetailRemarks",
                            "item_free_txt1": "unittestItemFreeTxt",
                            "item_free_txt2": "unittestItemFreeTxt2",
                            "item_free_txt3": "unittestItemFreeTxt3",
                            "item_free_txt4": "unittestItemFreeTxt4",
                            "item_free_txt5": "unittestItemFreeTxt5",
                            "item_free_txt6": "unittestItemFreeTxt6",
                            "item_free_txt7": "unittestItemFreeTxt7",
                            "item_free_txt8": "unittestItemFreeTxt8",
                            "item_free_txt9": "unittestItemFreeTxt9",
                            "item_free_txt10": "unittestItemFreeTxt10",
                            "item_free_txt_l": "unittestItemFreeTxtl",
                            "tax_type": "0",
                            "tax_rate_sec": 10,
                            "reduced_tax_flg": "1",
                            "input_tax_type": "2",
                            "tax_calc_type": "0",
                            "sum_exempt_flg": "1",
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
                },
            },
        )
    ]


test_PP002_exception = [
    (
        # case 1 : I0001: invoice_idが数値ではない
        "a",
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
        # case3 : I0004: 指定したcompany_infos_idが所属企業、結合企業に該当しない
        1,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
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
        # case4 : E9999: サーバーエラー
        1,
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
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
