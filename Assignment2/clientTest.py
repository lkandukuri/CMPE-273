'''
################################## clientTest.py #############################
# 
################################## clientTest.py #############################
'''

import grpc
import replication_pb2
import argparse

PORT = 3000

class ReplicationClientTest():
    def __init__(self, host='192.168.0.1', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replication_pb2.ReplicationStub(self.channel)

    def put(self, key, data):
        return self.stub.put(replication_pb2.Request(key=key, data=data))

    def delete(self, key):
        return self.stub.delete(replication_pb2.Request(key=key))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("clientTest is connecting to Server at {}:{}...".format(args.host, PORT))
    client = ReplicationClientTest(host=args.host)

    
    resp = client.put('1', 'abc')
    print("Test1:")
    print(resp.data)

    resp = client.put('2', 'def')
    print("Test2:")
    print(resp.data)

    resp = client.delete('1')
    print("Test3:")
    print(resp.data)


if __name__ == "__main__":
    main()


