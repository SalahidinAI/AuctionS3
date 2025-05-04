import os
import boto3
import sys
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get AWS credentials from environment
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    region_name = os.getenv('AWS_S3_REGION_NAME')
    
    if not all([aws_access_key, aws_secret_key, bucket_name, region_name]):
        print("ERROR: Missing required AWS credentials in environment variables.")
        print("Required variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME")
        sys.exit(1)
    
    # Create S3 client
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        
        # Test bucket existence and permissions
        print(f"Testing access to bucket: {bucket_name}")
        
        # Test GET operation
        try:
            s3.head_bucket(Bucket=bucket_name)
            print("✅ Bucket exists and is accessible")
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == '403':
                print("❌ Access denied to bucket (403 Forbidden)")
                print("   Check your IAM permissions and bucket policy")
            elif error_code == '404':
                print(f"❌ Bucket '{bucket_name}' does not exist")
            else:
                print(f"❌ Error accessing bucket: {str(e)}")
            return
        
        # Test object operations
        test_key = 'test-permissions/test.txt'
        test_content = b'This is a test file to verify S3 permissions'
        
        try:
            # Test PUT operation
            print(f"Testing PUT operation...")
            s3.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=test_content,
                ContentType='text/plain',
                ACL='public-read'
            )
            print("✅ PUT operation successful")
            
            # Test GET operation
            print(f"Testing GET operation...")
            s3.get_object(Bucket=bucket_name, Key=test_key)
            print("✅ GET operation successful")
            
            # Test DELETE operation
            print(f"Testing DELETE operation...")
            s3.delete_object(Bucket=bucket_name, Key=test_key)
            print("✅ DELETE operation successful")
            
            print("\n✅ All S3 operations successful! Your credentials and permissions are correct.")
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            print(f"❌ Error during S3 operations: {error_code}")
            print(f"   Error details: {str(e)}")
            
            if error_code == '403':
                print("\nSUGGESTIONS:")
                print("1. Make sure your IAM user has the following permissions:")
                print("   - s3:GetObject")
                print("   - s3:PutObject")
                print("   - s3:DeleteObject")
                print("   - s3:ListBucket")
                print("2. Check if bucket has Block Public Access settings enabled")
                print("3. Verify your bucket policy allows these operations")
                
    except Exception as e:
        print(f"❌ General error: {str(e)}")

if __name__ == "__main__":
    main() 