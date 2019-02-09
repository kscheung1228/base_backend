import datetime
import os
import boto3
# from django.conf import settings

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_ACCESS_KEY_ID = 'AKIAI3R3ENTXROWAVZVA'
AWS_SECRET_ACCESS_KEY = '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'

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'base_backend.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'base_backend.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'kscheung1228base'
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
AWS_OBJECT_DOWNLOAD_HOURS = 1


class AWS:
    access_key      = AWS_ACCESS_KEY_ID
    secret_key      = AWS_SECRET_ACCESS_KEY
    region          = S3DIRECT_REGION
    bucket          = AWS_STORAGE_BUCKET_NAME
    s3_client       = None
    client          = None
    session         = None
    s3_session      = None


    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_session(self):
        if self.session == None:
            session = boto3.Session(
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name = self.region
                )
            self.session = session
        return self.session

    def get_client(self, service='s3'):
        if self.client == None:
            client = boto3.client(service,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name = self.region
                )
            self.client = client
        return self.client


    def get_s3_client(self):
        if self.s3_client == None:
            s3_client = self.get_client(service='s3')
            if s3_client is None:
                return None
            self.s3_client = s3_client
        return self.s3_client

    def get_s3_session(self):
        if self.s3_session == None:
            session = self.get_session()
            if session is None:
                return None # Raise some error
            s3_session = session.resource("s3")
            self.s3_session = s3_session
        return self.s3_session

    def get_download_url(self, key=None, force_download=True, filename=None, expires_in=AWS_OBJECT_DOWNLOAD_HOURS):
        '''
        For any key, grab a signed url, that expires
        '''
        if key is None:
            return ""
        s3_client = self.get_s3_client()
        if s3_client is None:
            return ""

        download_args = {}
        if force_download:
            download_args = {
                'ResponseContentType': 'application/force-download'
            }
            if filename is not None:
                download_args['ResponseContentDisposition'] = f'attachment; filename="{filename}"'
        url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params = {
                    'Bucket': self.bucket,
                    'Key': key,
                    **download_args
                },
                ExpiresIn=datetime.timedelta(hours=expires_in).total_seconds()
                )
        return url

    def presign_post_url(self, key=None, is_public=False):
        acl = 'private'
        if is_public:
            acl = 'public-read'
        fields = {"acl": acl}
        conditions = [
            {"acl": acl}
        ]
        if key is None:
            return ""
        s3_client = self.get_s3_client()
        if s3_client is None:
            return ""
        data = s3_client.generate_presigned_post(
                Bucket = self.bucket,
                Key = key,
                Fields= fields,
                Conditions = conditions
            )
        return data

    def upload_file(self, fileobj=None, key=None):
        s3_client = self.get_s3_client()
        data = s3_client.upload_fileobj(
            Fileobj = fileobj, 
            Bucket = self.bucket,
            Key = key,
            ExtraArgs=None, 
            Callback=None, 
            Config=None)
        return data