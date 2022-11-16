

class S3: 
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.s3 """

    def create_s3_bucket(self, s3_bucket_name, policy='private'):
        return self._client.create_bucket(
            Bucket=s3_bucket_name,
            ACL=policy
            )

    def update_policy(self, s3_bucket_name, s3_bucket_policy ):

        return self._client.put_bucket_policy(
            Bucket=s3_bucket_name, 
            Policy=s3_bucket_policy
            )


    def list_buckets(self):
        return self._client.list_buckets()

    def delete_bucket(self, s3_bucket_name):
        print("Deleting S3 bucket: " + s3_bucket_name)
        return self._client.delete_bucket(
        Bucket=s3_bucket_name,
        )

    def put_object_to_site(self, bucket_name, body, file_name):
        print("Adding {0} file to bucket {1}".format(file_name, bucket_name))
        return self._client.put_object(
            ACL='public-read',
            Body=body,
            ContentType='text/html',
            Bucket=bucket_name,
            Key=file_name
            )

    def put_bucket_site(self, bucket_name):
        print("Making bucket {0} into a website".format(bucket_name))
        return self._client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'ErrorDocument': {
                    'Key':'error.html'
                },
                'IndexDocument': {
                    'Suffix':'index.html'
                },
            },
        )

    def list_s3_objects(self, bucket_name):
        return self._client.list_objects(
            Bucket=bucket_name
        )

    def delete_s3_object(self, bucket_name, key):
        print("Deleting {0} from bucket {1}".format(key, bucket_name))
        return self._client.delete_object(
            Bucket=bucket_name,
            Key=key
        )


