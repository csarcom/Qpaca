.. image:: https://travis-ci.org/csarcom/python-pubsub.svg?branch=master
    :target: https://travis-ci.org/csarcom/python-pubsub

=============
python-pubsub
=============

=============
Build and Run
=============

We can run python-pubsub using normal docker containers or docker-compose

Docker Containers
-----------------

Pulling and Starting RabbitMQ::

	docker pull rabbitmq:3-management
	docker run -d --name my_rabbitmq -p 15672:15672 rabbitmq:3-management

You can access now RabbitMQ Management using http://localhost:15672 using credentials: guest/guest

Pulling and Starting python-pubsub image::

	docker pull csarcom/python-pubsub:latest
	docker run -it -p 8000:8000 --link my_rabbitmq:my_rabbitmq -v /$(pwd):/app csarcom/python-pubsub

Docker Compose
--------------

	docker-compose up

Running tests
-------------

	docker run -it -v /$(pwd):/app csarcom/python-pubsub bash
	py.test pubsub/tests

Build python-pubsub
-------------------

Build docker container python-pubsub, you just need to do this if you want do update/create a new image::

	docker build -t python-pubsub .


=======
License
=======

	The MIT License (MIT)

	Copyright (c) 2015, Charles Sartori

	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
