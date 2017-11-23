'''
################################## server.py #############################
# # Assignment2 gRPC RocksDB Server 
# ################################## server.py #############################
# '''

import time
import grpc
import replication_pb2
import replication_pb2_grpc
import queue
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ReplicationService(replication_pb2.ReplicationServicer):
    def __init__(self):
        self.db = rocksdb.DB("assignment2_server.db", rocksdb.Options(create_if_missing=True))
        self.replication_queue = queue.Queue()

    def decoratorForReplication(func):
        def wrapper_func(self, request, context):
            resp = replication_pb2.ReplicationResponse(
                    operation = func.__name__, 
                    key = request.key.encode(), 
                    data = request.data.encode()
                 ) 
            self.replication_queue.put(resp)
            return func(self, request, context)
        return wrapper_func


    @decoratorForReplication
    def put(self, request, context):
        print("Storing key=" + request.key + ", value=" + request.data + " to server db")
        self.db.put(request.key.encode(), request.data.encode())
        return replication_pb2.Response(data='success')


    @decoratorForReplication
    def delete(self, request, context):
        print("Deleting key=" + request.key + " from server db")
        self.db.delete(request.key.encode())
        return replication_pb2.Response(data='success')


    def sync(self, request, context):
        print("Client connected")
        while True:
            resp = self.replication_queue.get()
            if(resp.operation == 'put'):
               print("operation: " + resp.operation + ", key: " + resp.key + ", value:" + resp.data)
            else:
                print("operation: " + resp.operation + ", key: " + resp.key )

            yield resp



def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    replication_pb2_grpc.add_ReplicationServicer_to_server(ReplicationService(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
