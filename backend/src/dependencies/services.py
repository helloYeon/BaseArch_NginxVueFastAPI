"""dependencies/services.py"""

from database import get_db
from fastapi import Depends
from services.admin_service import AdminService
from services.company_service import CompanyService
from services.csv_service import CsvService
from services.download_service import DownloadService
from services.invoice_detail_service import InvoiceDetailService
from services.invoice_service import InvoiceService
from services.output_service import OutputService
from services.receive_service import ReceiveService
from services.setting_service import SettingService
from services.user_service import UserService
from sqlalchemy.orm import Session


def depend_admin_service(db: Session = Depends(get_db)) -> AdminService:
    """AdminRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        AdminService:管理サービス
    """
    return AdminService(db)


def depend_company_service(db: Session = Depends(get_db)) -> CompanyService:
    """CompanyRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        CompanyService:ユーザーサービス
    """
    return CompanyService(db)


def depend_csv_service(db: Session = Depends(get_db)) -> CsvService:
    """CsvRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        CsvService:CSVサービス
    """
    return CsvService(db)


def depend_download_service(db: Session = Depends(get_db)) -> DownloadService:
    """DownloadRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        DownloadService:ダウンロードサービス
    """
    return DownloadService(db)


def depend_invoice_detail_service(
    db: Session = Depends(get_db),
) -> InvoiceDetailService:
    """InvoiceDetailRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        InvoiceDetailService:請求書詳細サービス
    """
    return InvoiceDetailService(db)


def depend_invoice_service(db: Session = Depends(get_db)) -> InvoiceService:
    """InvoiceRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        InvoiceService:請求書サービス
    """
    return InvoiceService(db)


def depend_output_service(db: Session = Depends(get_db)) -> OutputService:
    """OutputRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        OutputService:出力サービス
    """
    return OutputService(db)


def depend_receive_service(db: Session = Depends(get_db)) -> ReceiveService:
    """ReceiveRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).


    Returns:
        ReceiveService:受取サービス
    """
    return ReceiveService(db)


def depend_setting_service(db: Session = Depends(get_db)) -> SettingService:
    """SettingRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        SettingService:設定サービス
    """
    return SettingService(db)


def depend_user_service(db: Session = Depends(get_db)) -> UserService:
    """UserRepository のインスタンスを依存性注入で取得

    Args:
        db (Session, optional): dbセッション. Defaults to Depends(get_db).

    Returns:
        UserService:ユーザーサービス
    """
    return UserService(db)
