import socket
import time
import random

HOST = 'gateway'
PORT = 65432

def run_sensor():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                while True:
                    temp = random.uniform(15.0, 30.0)
                    message = f"Temperatura: {temp:.2f}°C"
                    s.sendall(message.encode())
                    print(f"Enviado: {message}")
                    time.sleep(5)
        except ConnectionRefusedError:
            print("Falha ao conectar ao Gateway, tentando novamente em 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    run_sensor()