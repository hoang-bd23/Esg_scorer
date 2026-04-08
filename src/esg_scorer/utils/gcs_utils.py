import os
import logging
from google.cloud import storage

logger = logging.getLogger(__name__)

def upload_to_gcs(bucket_name: str, source_file_path: str, destination_blob_name: str) -> bool:
    """
    Upload file từ ổ đĩa lên bộ lưu trữ GCP Storage (Bucket).
    Yêu cầu phải cấu hình biến môi trường GOOGLE_APPLICATION_CREDENTIALS trỏ tới file JSON key.
    """
    try:
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            logger.error("Không tìm thấy biến GOOGLE_APPLICATION_CREDENTIALS. Bỏ qua việc push lên GCP.")
            return False

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        logger.info(f"Đang đồng bộ {source_file_path} lên gs://{bucket_name}/{destination_blob_name} ...")
        blob.upload_from_filename(source_file_path)
        logger.info(f"Tải lên thành công: {destination_blob_name}")
        
        return True
    except Exception as e:
        logger.error(f"Lỗi khi push file lên GCS: {e}", exc_info=True)
        return False
