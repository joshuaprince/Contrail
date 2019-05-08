class BucketIterator:
    """
    Iterator for all files in an S3 bucket.

    Example usage: `for file in BucketFileIterator(s3client): ...`

    Each iteration returns a dict with keys: 'Key', 'LastModified', 'ETag', 'Size', 'StorageClass', 'Owner', 'ID'
    """

    def __init__(self, s3client, bucket_name):
        self.s3client = s3client
        self.bucket_name = bucket_name
        self.key_list = []
        self.last_key = ''
        self.truncated = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.key_list:
            if not self.truncated:
                raise StopIteration

            resp = self.s3client.list_objects(Bucket=self.bucket_name, Marker=self.last_key)
            self.key_list = resp['Contents']

            if resp['IsTruncated']:
                self.last_key = resp['Contents'][-1]['Key']
            else:
                self.truncated = False

        return self.key_list.pop(0)

