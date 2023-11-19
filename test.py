import unittest
import boto3
import time

class TestTerraformS3Bucket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3_client = boto3.client('s3')

    def test_s3_bucket_creation(self):
        # Replace with your actual bucket name
        bucket_name = "my-unique-bucket-name-for-anybody"

        # Give some time for the bucket to be created (adjust as needed)
        time.sleep(10)

        # Check if the S3 bucket exists
        exists = self.bucket_exists(bucket_name)
        self.assertTrue(exists, f"S3 bucket '{bucket_name}' does not exist")

        # Check if the S3 bucket has the expected ACL (Access Control List)
        acl = self.get_bucket_acl(bucket_name)
        self.assertEqual(acl, 'private', f"Unexpected ACL for S3 bucket '{bucket_name}': {acl}")

        # Check if the S3 bucket has the expected tags
        tags = self.get_bucket_tags(bucket_name)
        expected_tags = {'Name': 'MyBucket', 'Environment': 'Dev'}
        self.assertDictEqual(tags, expected_tags, f"Unexpected tags for S3 bucket '{bucket_name}': {tags}")

    def bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except self.s3_client.exceptions.NoSuchBucket:
            return False

    def get_bucket_acl(self, bucket_name):
        response = self.s3_client.get_bucket_acl(Bucket=bucket_name)
        grants = response.get('Grants', [])
        for grant in grants:
            if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                return 'public-read'
        return 'private'

    def get_bucket_tags(self, bucket_name):
        response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)
        return {tag['Key']: tag['Value'] for tag in response['TagSet']}

if __name__ == '__main__':
    unittest.main()


