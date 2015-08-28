# S3 Automatic Image Compression

This project provides automatic lossless compression of jpegs when they are added to an s3 bucket. Read [this article](http://petegraham.co.uk/s3-automatic-image-compression/) for a full explanation of how to set-up AWS to get this working.

## Installation

The has been been tested on Python 3.4.3 on OS X. It should run on Linux but the mozjpeg installation instructions will differ. OS X ships with Python 2 but you can install multiple versions https://www.python.org/downloads/.

0.  Install mozjpeg. For OS X this can be done with:
    ```
    brew install mozjpeg
    ```

1.  Set environment variables for AWS.
    ```
    export AWS_ACCESS_KEY_ID=<your-aws-access-key>
    export AWS_SECRET_ACCESS_KEY-<your-aws-secret-key>
    ```

2.  Optional: Create Virtual Enviroment for Python 3 (you may need to  change the python location depending on your set-up).
    ```
    mkvirtualenv --python=/usr/local/bin/python3 s3-image-resize
    ```

3.  Install requirements
    ```
    pip install -r requirements.txt
    ```

4.  Run code
    ```
    python connect_to_queue.py
    ```
    When updates are made to s3 they'll automatically be compressed an uploaded again.
