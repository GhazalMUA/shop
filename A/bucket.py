''' 
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

class Bucket:   
    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        try:
            result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            if 'Contents' in result:
                return result['Contents']
            else:
                return None
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                # Handle the case where the bucket or prefix does not exist
                return None
            else:
                # Handle other errors
                raise
    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

bucket = Bucket()
''' 



import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

class Bucket:   
    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url='https://s3.ir-tbz-sh1.arvanstorage.ir',
        )

    def get_objects(self):
        try:
            logger.info("Fetching objects from S3 bucket...")
            result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            if 'Contents' in result:
                logger.info("Objects fetched successfully.")
                return result['Contents']
            else:
                logger.info("No objects found in the bucket.")
                return None
        except ClientError as e:
            logger.error(f"Error fetching objects from S3 bucket: {e}")
            if e.response['Error']['Code'] == 'NoSuchKey':
                # Handle the case where the bucket or prefix does not exist
                logger.info("Bucket or prefix does not exist.")
                return None
            else:
                # Handle other errors
                raise
    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        logger.info(f"Object with key '{key}' deleted successfully from S3 bucket.")
        return True

bucket = Bucket()
