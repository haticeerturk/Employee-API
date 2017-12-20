aiobotocore
===========
.. image:: https://travis-ci.org/aio-libs/aiobotocore.svg?branch=master
    :target: https://travis-ci.org/aio-libs/aiobotocore
.. image:: https://codecov.io/gh/aio-libs/aiobotocore/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/aio-libs/aiobotocore
.. image:: https://img.shields.io/pypi/v/aiobotocore.svg
    :target: https://pypi.python.org/pypi/aiobotocore
.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/aio-libs/aiobotocore
    :alt: Chat on Gitter



Async client for amazon services using botocore_ and aiohttp_/asyncio_.

Main purpose of this library to support amazon s3 api, but other services
should work (may be with minor fixes). For now we have tested
only upload/download api for s3, other users report that SQS and Dynamo
services work also. More tests coming soon.


Install
-------
::

    $ pip install aiobotocore


Basic Example
-------------

.. code:: python

    import asyncio
    import aiobotocore

    AWS_ACCESS_KEY_ID = "xxx"
    AWS_SECRET_ACCESS_KEY = "xxx"


    async def go(loop):
        bucket = 'dataintake'
        filename = 'dummy.bin'
        folder = 'aiobotocore'
        key = '{}/{}'.format(folder, filename)

        session = aiobotocore.get_session(loop=loop)
        async with session.create_client('s3', region_name='us-west-2',
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                       aws_access_key_id=AWS_ACCESS_KEY_ID) as client:
            # upload object to amazon s3
            data = b'\x01'*1024
            resp = await client.put_object(Bucket=bucket,
                                                Key=key,
                                                Body=data)
            print(resp)

            # getting s3 object properties of file we just uploaded
            resp = await client.get_object_acl(Bucket=bucket, Key=key)
            print(resp)

            # get object from s3
            response = await client.get_object(Bucket=bucket, Key=key)
            # this will ensure the connection is correctly re-used/closed
            async with response['Body'] as stream:
                assert await stream.read() == data

            # list s3 objects using paginator
            paginator = client.get_paginator('list_objects')
            async for result in paginator.paginate(Bucket=bucket, Prefix=folder):
                for c in result.get('Contents', []):
                    print(c)

            # delete object from s3
            resp = await client.delete_object(Bucket=bucket, Key=key)
            print(resp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(loop))


Supported AWS Services
----------------------

This is a non-exuastive list of what tests aiobotocore runs against AWS services. Not all methods are tested but we aim to test the majority of
commonly used methods.

+----------------+-----------------------+
| Service        | Status                |
+================+=======================+
| S3             | Working               |
+----------------+-----------------------+
| DynamoDB       | Basic methods tested  |
+----------------+-----------------------+
| SNS            | Basic methods tested  |
+----------------+-----------------------+
| SQS            | Basic methods tested  |
+----------------+-----------------------+
| CloudFormation | Stack creation tested |
+----------------+-----------------------+

Due to the way boto3 is implemented, its highly likely that even if services are not listed above that you can take any `boto3.client('service')` and
stick `await` infront of methods to make them async, e.g. `await client.list_named_queries()` would asynchronous list all of the named Athena queries.

If a service is not listed here and you could do with some tests or examples feel free to raise an issue.

Run Tests
---------

Make sure you have development requirements installed and your amazon key and
secret accessible via environment variables:

::

    $ cd aiobotocore
    $ export AWS_ACCESS_KEY_ID=xxx
    $ export AWS_SECRET_ACCESS_KEY=xxx
    $ pip install -Ur requirements-dev.txt

Execute tests suite:

::

    $ py.test -v tests


Mailing List
------------

https://groups.google.com/forum/#!forum/aio-libs


Requirements
------------
* Python_ 3.4+
* aiohttp_
* botocore_

.. _Python: https://www.python.org
.. _asyncio: http://docs.python.org/3.4/library/asyncio.html
.. _botocore: https://github.com/boto/botocore
.. _aiohttp: https://github.com/KeepSafe/aiohttp


awscli
------

awscli depends on a single version of botocore, however aiobotocore only supports a
specific range of botocore versions. To ensure you install the latest version of
awscli that your specific combination or aiobotocore and botocore can support use::

    pip install -U aiobotocore[awscli]

Changes
-------

0.5.2 (2017-12-06)
^^^^^^^^^^^^^^^^^^
* Updated awscli dependency #461

0.5.1 (2017-11-10)
^^^^^^^^^^^^^^^^^^
* Disabled compressed response #430

0.5.0 (2017-11-10)
^^^^^^^^^^^^^^^^^^
* Fix error botocore error checking #190
* Update supported botocore requirement to: >=1.7.28, <=1.7.40
* Bump aiohttp requirement to support compressed responses correctly #298

0.4.5 (2017-09-05)
^^^^^^^^^^^^^^^^^^
* Added SQS examples and tests #336
* Changed requirements.txt structure #336
* bump to botocore 1.7.4
* Added DynamoDB examples and tests #340


0.4.4 (2017-08-16)
^^^^^^^^^^^^^^^^^^
* add the supported versions of boto3 to extras require #324

0.4.3 (2017-07-05)
^^^^^^^^^^^^^^^^^^
* add the supported versions of awscli to extras require #273 (thanks @graingert)

0.4.2 (2017-07-03)
^^^^^^^^^^^^^^^^^^
* update supported aiohttp requirement to: >=2.0.4, <=2.3.0
* update supported botocore requirement to: >=1.5.71, <=1.5.78

0.4.1 (2017-06-27)
^^^^^^^^^^^^^^^^^^
* fix redirects #268

0.4.0 (2017-06-19)
^^^^^^^^^^^^^^^^^^
* update botocore requirement to: botocore>=1.5.34, <=1.5.70
* fix read_timeout due to #245
* implement set_socket_timeout

0.3.3 (2017-05-22)
^^^^^^^^^^^^^^^^^^
* switch to PEP 440 version parser to support 'dev' versions

0.3.2 (2017-05-22)
^^^^^^^^^^^^^^^^^^
* Fix botocore integration
* Provisional fix for aiohttp 2.x stream support
* update botocore requirement to: botocore>=1.5.34, <=1.5.52

0.3.1 (2017-04-18)
^^^^^^^^^^^^^^^^^^
* Fixed Waiter support

0.3.0 (2017-04-01)
^^^^^^^^^^^^^^^^^^
* Added support for aiohttp>=2.0.4 (thanks @achimnol)
* update botocore requirement to: botocore>=1.5.0, <=1.5.33

0.2.3 (2017-03-22)
^^^^^^^^^^^^^^^^^^
* update botocore requirement to: botocore>=1.5.0, <1.5.29

0.2.2 (2017-03-07)
^^^^^^^^^^^^^^^^^^
* set aiobotocore.__all__ for * imports #121 (thanks @graingert)
* fix ETag in head_object response #132

0.2.1 (2017-02-01)
^^^^^^^^^^^^^^^^^^
* Normalize headers and handle redirection by botocore #115 (thanks @Fedorof)

0.2.0 (2017-01-30)
^^^^^^^^^^^^^^^^^^
* add support for proxies (thanks @jjonek)
* remove AioConfig verify_ssl connector_arg as this is handled by the
  create_client verify param
* remove AioConfig limit connector_arg as this is now handled by
  by the Config `max_pool_connections` property (note default is 10)

0.1.1 (2017-01-16)
^^^^^^^^^^^^^^^^^^
* botocore updated to version 1.5.0

0.1.0 (2017-01-12)
^^^^^^^^^^^^^^^^^^
* Pass timeout to aiohttp.request to enforce read_timeout #86 (thanks @vharitonsky)
  (bumped up to next semantic version due to read_timeout enabling change)

0.0.6 (2016-11-19)
^^^^^^^^^^^^^^^^^^

* Added enforcement of plain response #57 (thanks @rymir)
* botocore updated to version 1.4.73 #74 (thanks @vas3k)


0.0.5 (2016-06-01)
^^^^^^^^^^^^^^^^^^

* Initial alpha release

