1. Change branch to develop
2. Flatten repo
3. Push to Gitub
4. README. Including installation
5. Research daemonising. User supervisor?
6. Research multi-treaded
7. Read-up on SQS
8. Can we automate any of the annoying policy steps

User ARN: arn:aws:iam::239820892130:user/pete


arn:aws:iam::123456789012:user/David

http://docs.aws.amazon.com/AmazonS3/latest/dev/s3-bucket-user-policy-specifying-principal-intro.html
"Principal":{"CanonicalUser":"64-digit-alphanumeric-value"}

https://console.aws.amazon.com/iam/home?#users

***

"Browser" principal ID = "AWS:AIDAJTQ6QLZUPQLDMW2PE" in this me?
Script principal ID =  "AWS:AIDAJ22F5JNYL3GCHHM4O"
user_id AIDAJ22F5JNYL3GCHHM4O


<ErrorResponse xmlns="https://iam.amazonaws.com/doc/2010-05-08/">
  <Error>
    <Type>Sender</Type>
    <Code>AccessDenied</Code>
    <Message>User: arn:aws:iam::239820892130:user/s3-image-resizer is not authorized to perform: iam:GetUser on resource: user s3-image-resizer</Message>
  </Error>
  <RequestId>7cde51eb-3518-11e5-9c83-7d4a35a9d7b0</RequestId>
</ErrorResponse>


# Delete queue

***

{'awsRegion': 'eu-west-1',
 'eventName': 'ObjectCreated:Put',
 'eventSource': 'aws:s3',
 'eventTime': '2015-07-28T10:14:18.255Z',
 'eventVersion': '2.0',
 'requestParameters': {'sourceIPAddress': '37.157.36.218'},
 'responseElements': {'x-amz-id-2': 'lEPwgzy+UXPDRnNCBmHfOzOKtnIJ9ykyvA+MYJwOcsNQrfWjk27xoY2HjMzIpt6TGr6DnW+NBhY=',
                      'x-amz-request-id': 'B47FEE01041AE73D'},
 's3': {'bucket': {'arn': 'arn:aws:s3:::pxg-image-resizer',
                   'name': 'pxg-image-resizer',
                   'ownerIdentity': {'principalId': 'A1PWI4M3I9Z57A'}},
        'configurationId': 'NotificationObjectCreated',
        'object': {'eTag': 'dd34b94d7a954d479febc35a819231b5',
                   'key': 'turdus_philomelos.jpg',
                   'size': 251073},
        's3SchemaVersion': '1.0'},
 'userIdentity': {'principalId': 'AWS:AIDAJ22F5JNYL3GCHHM4O'}}
(Pdb) pprint(data)
{'Records': [{'awsRegion': 'eu-west-1',
              'eventName': 'ObjectCreated:Put',
              'eventSource': 'aws:s3',
              'eventTime': '2015-07-28T10:14:18.255Z',
              'eventVersion': '2.0',
              'requestParameters': {'sourceIPAddress': '37.157.36.218'},
              'responseElements': {'x-amz-id-2': 'lEPwgzy+UXPDRnNCBmHfOzOKtnIJ9ykyvA+MYJwOcsNQrfWjk27xoY2HjMzIpt6TGr6DnW+NBhY=',
                                   'x-amz-request-id': 'B47FEE01041AE73D'},
              's3': {'bucket': {'arn': 'arn:aws:s3:::pxg-image-resizer',
                                'name': 'pxg-image-resizer',
                                'ownerIdentity': {'principalId': 'A1PWI4M3I9Z57A'}},
                     'configurationId': 'NotificationObjectCreated',
                     'object': {'eTag': 'dd34b94d7a954d479febc35a819231b5',
                                'key': 'turdus_philomelos.jpg',
                                'size': 251073},
                     's3SchemaVersion': '1.0'},
              'userIdentity': {'principalId': 'AWS:AIDAJ22F5JNYL3GCHHM4O'}}]}
(Pdb)














***

 - Add queue back in

 - Move API keys to environment variables
 - Push to Github. Share Rob and Rach
 - Can we check that the file was uploaded by my AWS user (API key) and ignore

 - Tests? Talk to Rob

***

0. Create SQS. Principals everybody. Actions all SQS actions
1. Create bucket
2. Add notifications to be pushed to SQS
3. Create new AWS user. Get credentials
4. Attach policy to user AmazonSQSFullAccess
5. Add a file. Check queue again


***

http://tonyfy.com/
OpenCV research

***

brew install mozjpeg

***

Rzf track time
