
## What to do?

In this assignment 2, you will be implementing a RocksDB replication in Python using the design from this [C++ replicator](https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d).  You can use Lab 1 as a based line. Differences form the replicator are:

You will be using GRPC Python server instead of Thrift server.
You will be exploring more into GRPC sync, async, and streaming.
You can ignore all cluster management features from the replicator.

## How to run:

### Create Stubs from proto file using:

``` ssh
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. replication.proto
```
### Run server.py using:
``` ssh
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py
```
### Run client.py using:
``` ssh
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
```
### Run clientTest.py using:
``` ssh
docker run -it --rm --name lab1-clientTest -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 clientTest.py 192.168.0.1
```
### Output server.py:
``` ssh

Server started at...3000
Client connected
Storing key=1, value=abc to server db
operation: put, key: 1, value:abc
Storing key=2, value=def to server db
operation: put, key: 2, value:def
Deleting key=1 from server db
operation: delete, key: 1

```
### Output client.py:

``` ssh

Client is connecting to Server at 192.168.0.1:3000...
connection to server successful
operation: put, key: 1, value: abc
operation: put, key: 2, value: def
operation: delete, key: 1

```
### Output clientTest.py:

``` ssh
Test1:
success
Test2:
success
Test3:
success

```




