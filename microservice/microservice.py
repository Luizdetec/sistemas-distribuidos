import pika
import grpc
from concurrent import futures
import sensor_pb2
import sensor_pb2_grpc

RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'sensor_data'


class SensorService(sensor_pb2_grpc.SensorServiceServicer):
    def ProcessSensorData(self, request, context):
        data = request.data
        print(f"Dado processado: {data}")
        return sensor_pb2.SensorDataResponse(message=f"Processado: {data}")


def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(SensorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server rodando na porta 50051")
    server.wait_for_termination()


def consume_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)

            def callback(ch, method, properties, body):
                data = body.decode()
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = sensor_pb2_grpc.SensorServiceStub(channel)
                    response = stub.ProcessSensorData(sensor_pb2.SensorDataRequest(data=data))
                    print(f"Resposta gRPC: {response.message}")

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
            print("Aguardando mensagens do RabbitMQ...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Falha ao conectar ao RabbitMQ, tentando novamente em 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    import threading

    threading.Thread(target=start_grpc_server, daemon=True).start()
    consume_rabbitmq()