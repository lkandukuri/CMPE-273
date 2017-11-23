'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import replication_pb2
import rocksdb
import argparse

PORT = 3000

class ReplicationClient():
    def __init__(self, host='192.168.0.1', port=PORT):
        self.db = rocksdb.DB("assignment2_client.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replication_pb2.ReplicationStub(self.channel)

    def sync(self):
        replicator = self.stub.sync(replication_pb2.ReplicationRequest())
        print("connection to server successful")
        for item in replicator:
            if item.operation == 'put':
                print("operation: " + item.operation + ", key: " + item.key + ", value: " + item.data)
                self.db.put(item.key.encode('utf-8'), item.data.encode('utf-8'))
            elif item.operation == 'delete':
                print("operation: " + item.operation + ", key: " + item.key)
                self.db.delete(item.key.encode('utf-8'))
            

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = ReplicationClient(host=args.host)

    resp = client.sync()

if __name__ == "__main__":
    main()