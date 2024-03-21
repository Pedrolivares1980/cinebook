import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Configurations
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-west-1')  # Default to 'eu-west-1' if not found
BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# S3 client
s3 = boto3.client(
    's3',
    region_name=AWS_S3_REGION_NAME,  # Include region name
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file_path, bucket_name, destination_file_name):
    try:
        s3.upload_file(file_path, bucket_name, destination_file_name)
        print(f"File {file_path} successfully uploaded to {bucket_name}/{destination_file_name}")
    except NoCredentialsError:
        print("Credentials not available or incorrect")
    except Exception as e:
        print(f"Error uploading the file: {e}")

# Example usage of the script
if __name__ == "__main__":
    file_path = 'C:/Users/pedro_40bymts/Desktop/fullStack/final/cinebook/media/default.jpg'  # Adjust as needed
    destination_file_name = 'profile_pics/default.jpg'  # Replace with your desired path in the bucket
    upload_file_to_s3(file_path, BUCKET_NAME, destination_file_name)

