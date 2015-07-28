import json
import os
from time import sleep
from subprocess import call

import boto
import boto.sqs


def check_queue():
    script_principal_id = 'AWS:{0}'.format(get_script_principal_id())
    # TODO: load region, queue and bucket from config file
    conn = boto.sqs.connect_to_region('eu-west-1')
    queue = conn.get_queue('imageResize')

    while(True):
        messages = queue.get_messages()
        print('{0} messages'.format(len(messages)))

        for message in messages:
            data = json.loads(message.get_body())
            if valid(data, script_principal_id):
                filename = data['Records'][0]['s3']['object']['key']
                print('Compressing {0}'.format(filename))
                compress_s3_file(filename)
            queue.delete_message(message)
        # TODO: get sleep time from config file
        sleep(1)


def valid(data, script_principal_id):
    # TOOD: check event wasn't a delete here
    if 'Records' in data:
        principal_id = data['Records'][0]['userIdentity']['principalId']
        if principal_id != script_principal_id:
            return True
    return False


def compress_s3_file(filename):
    compressed_filename = 'compressed-{0}'.format(filename)
    key = get_key_from_s3(filename)
    key.get_contents_to_filename(filename)
    compress_file(filename, compressed_filename)
    key.set_contents_from_filename(compressed_filename)
    os.remove(filename)
    os.remove(compressed_filename)


def get_key_from_s3(s3_filename):
    conn = boto.s3.connection.S3Connection()
    bucket = conn.get_bucket('pxg-image-resizer')
    return bucket.get_key(s3_filename)


def compress_file(filename, compressed_filename):
    # Got flags from here https://www.progville.com/frontend/optimizing-jpeg-images-mozjpeg/
    # TODO: move jpegtran path to config file
    call(['/usr/local/Cellar/mozjpeg/3.1/bin/jpegtran',
        '-outfile', compressed_filename,
        '-optimise', '-copy', 'none',
        filename])


def get_script_principal_id():
    conn = boto.connect_iam()
    return conn.get_user().user_id


if __name__ == "__main__":
    check_queue()
