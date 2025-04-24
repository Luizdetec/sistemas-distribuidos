from flask import Flask, render_template_string
import pika
import threading

app = Flask(__name__)

RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'sensor_data'
sensor_data = []

def consume_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)

            def callback(ch, method, properties, body):
                data = body.decode()
                sensor_data.append(data)
                if len(sensor_data) > 10:  # Limite de 10 mensagens
                    sensor_data.pop(0)

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Falha ao conectar ao RabbitMQ, tentando novamente em 5 segundos...")
            time.sleep(5)

@app.route('/')
def index():
    html = """
    <h1>Painel Gerencial - Monitoramento de Temperatura</h1>
    <ul>
    {% for data in sensor_data %}
        <li>{{ data }}</li>
    {% endfor %}
    </ul>
    <script>
        setInterval(() => location.reload(), 5000); // Atualiza a cada 5 segundos
    </script>
    """
    return render_template_string(html, sensor_data=sensor_data)

if __name__ == '__main__':
    threading.Thread(target=consume_rabbitmq, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)