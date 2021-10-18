import application
import boto3
import os


url = 'https://tistory1.daumcdn.net/tistory/3814687/skin/images/jingo2.png'
name = 'hello'
extension = url.split('.')[-1]
tempimg = application.urllib.request.urlopen(url).read()

s3 = boto3.client('s3',
                  aws_access_key_id='AKIAYH3J2NAOFYHB7UVV',
                  aws_secret_access_key='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'
                  )
print(extension)
s3.put_object(
    ACL='public-read',
    Bucket='mysparta2',
    Body=tempimg,
    Key='images/' + name + '.' + extension,
    # ContentType=
)
