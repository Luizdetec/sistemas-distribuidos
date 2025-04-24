import socket
import pika
import threading
import time

HOST = '0.0.0.0'
PORT = 65432
RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'sensor_data'

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Falha ao conectar ao RabbitMQ, tentando novamente em 5 segundos...")
            time.sleep(5)

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Recebido: {message}")
            # Publicar no RabbitMQ
            connection = connect_rabbitmq()
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)
            channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
            connection.close()

def run_gateway():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Gateway ouvindo em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    run_gateway()