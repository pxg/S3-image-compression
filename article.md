# S3 Automatic Image Compression

## Overview

The goal of this project is to provide completely automated lossless compression of images uploaded to s3. The project uses the S3 bucket notifications systems to send messages to SQS when a file is uploaded to the bucket.

A Python script reads messages pushed to the queue. When a new message is received the s3 file is downloaded locally. The local file is compressed with mozjpeg, the original S3 file is then replaced with the compressed version.

The motivation behind this project was to experiment with the S3 bucket notification system and Python 3. I wanted to see if working with this system would provide a clean solution for file processing tasks. It could also be useful to use with a CMS which has the ability to write image files to S3 but doesn't provide image compression.

## Getting set-up on AWS

1.  [Create an S3 bucket](https://console.aws.amazon.com/s3/home)

2.  [Create an SQS instance](https://eu-west-1.console.aws.amazon.com/sqs/home). Then set-up the permissions for the Queue. The fastest (but least secure) way is to allow "Everybody" and "All SQS Actions".

    ![AWS SQS UI](https://raw.githubusercontent.com/pxg/S3-image-compression/develop/docs/aws_sqs_ui.png "AWS SQS UI")

3.  Configure S3 bucket notifications to write to the SQS instance.
    This is on the buckets properties. Go to the "Event" section and enter:
    - Events: ObjectCreated (All)
    - SendTo: SQS queue
    - SQS Queue: your-queue-name

    ![AWS S3 UI](https://raw.githubusercontent.com/pxg/S3-image-compression/develop/docs/aws_s3_events_ui.png "AWS S3 UI")

4.  [Create an IAM user](https://console.aws.amazon.com/iam/home#users) and give them write access to the S3 bucket. To do this Create a new policy and use the following for the policy document:
    ```
    {
      "Statement": [
        {
          "Action": "s3:*",
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::your-bucket-name",
            "arn:aws:s3:::your-bucket-name/*"
          ]
        }
      ]
    }
    ```

5.  Give the User access to read/write SQS. The simplest way to do this is attach the policy "AmazonSQSFullAccess" to the user. Of course in a production system you'd want to lock the users access down further.

6.  Give user access to get information about their own account. The reasons for this will be explained next. You'll need to add this policy:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Stmt1438081733000",
                "Effect": "Allow",
                "Action": [
                    "iam:GetUser"
                ],
                "Resource": [
                    "arn:aws:iam::239820892130:user/s3-image-resizer"
                ]
            }
        ]
    }
    ```
    You'll need to change the resource to match your user. Thankfully the Users ARN is easy to find and is at the top of the page in the AWS Web UI.

    ![AWS User UI](https://raw.githubusercontent.com/pxg/S3-image-compression/develop/docs/aws_user_ui.png "AWS User UI")

7.  Finally create an access key for the new user and save the new API credentials.

## Avoiding Infinite loops

Notifications are triggered every time a file is updated on S3. Our script monitors for notification messages, when it gets one it processes files then updates the file on S3.

The problem with this is the script gets struck in an infinite loop, since it triggers notifications that it then receives. When we receive a message about a new or modified file the data looks like this:
```
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
```

The import piece of information here is `'userIdentity': {'principalId': 'AWS:AIDAJ22F5JNYL3GCHHM4O'}` which is related to the AWS user who uploaded the file.

Unfortunately you can't currently get this user detail within the AWS web UI https://console.aws.amazon.com/iam/home?region=eu-west-1#users. However you can run the following code using Boto, the Python AWS library:
```
import boto
conn = boto.connect_iam()
user_id = conn.get_user().user_id
```
Once we have the `user_id` we can test it against the value in the message data. This is the reason we added the `getUser` policy to the IAM user, without it the code would throw an `AccessDenied` error. On start-up the script uses the AWS API to learn it's own user_id, it then can ignore messages about updates made by itself.

## Future work

This code is currently meant as a proof of concept and is not yet used in a production system. They are number of things I'd add before running in a production environment:
 - Logging
 - Error handling for corrupted input files
 - Error handling of potential mozjpeg crashes
 - Support for extra files types (png, gif, etc)

A future experiment could be to build on-top of these techniques to process the image files for alternative usages such as a facial recognition system using OpenCV.

This technique could be used to work with different types of file processing, it could be used for text file analysis, or to test SQL dumps are not corrupted.

The next things I plan to do is enhance the code to use threading techniques to process multiple files concurrently, which will be the subject of a future article.
