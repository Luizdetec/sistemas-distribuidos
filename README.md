

```markdown
# Plataforma Distribuída de Monitoramento e Controle de Ambientes Inteligentes

Este projeto foi desenvolvido como parte da disciplina de **Programação Distribuída e Paralela** do curso de Ciência da Computação. O objetivo é simular o monitoramento e controle de ambientes inteligentes (como salas de aula e laboratórios) em um campus universitário, utilizando uma arquitetura distribuída moderna.

## 🧠 Equipe
- Luiz Eduardo Estrella Alvares  
- Leonardo de Medeiros Bernardes  
- Renan Rodrigues Moreira  

---

## 🎯 Objetivos
- Simular o monitoramento de ambientes inteligentes em tempo real.
- Utilizar comunicação eficiente com **Sockets TCP**, **gRPC** e **RabbitMQ**.
- Disponibilizar uma interface web com **Flask** para visualização dos dados.

---

## 🧱 Arquitetura do Sistema

```
[Sensor] --(Socket TCP)--> [Gateway] --(RabbitMQ)--> [Microsserviço gRPC]
                                      --(RabbitMQ)--> [Painel Gerencial (Flask)]
```

Componentes principais:

- **Simulador de Sensor**: envia dados simulados de temperatura para o gateway via TCP.
- **Gateway**: recebe os dados e publica na fila `sensor_data` do RabbitMQ.
- **Microsserviço gRPC**: consome e processa dados da fila.
- **Middleware (RabbitMQ)**: comunicação assíncrona entre componentes.
- **Painel Gerencial (Flask)**: exibe os últimos dados recebidos.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12
- Sockets TCP
- gRPC
- RabbitMQ
- Flask
- Docker & Docker Compose

---

## 📁 Estrutura do Projeto

```
smartcampus/
├── sensor/
├── gateway/
├── microservice/
├── dashboard/
└── docker-compose.yml
```

---

## 🚀 Como Executar

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.12 (opcional, apenas para gerar arquivos gRPC)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd smartcampus
```

2. (Opcional) Gere os arquivos gRPC:
```bash
cd microservice
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sensor.proto
cd ..
```

3. Inicie os containers:
```bash
docker-compose up --build
```

4. Acesse:
- Painel Gerencial: [http://localhost:5000](http://localhost:5000)
- RabbitMQ: [http://localhost:15672](http://localhost:15672)  
  (usuário: `guest`, senha: `guest`)

### Parar os serviços
```bash
docker-compose down
```

---

## 🧪 Testes

- O sensor simula temperaturas a cada 5 segundos.
- Os dados são enviados via TCP, publicados no RabbitMQ, processados via gRPC e exibidos no painel Flask.
- O painel mostra as últimas 10 leituras em tempo real.

Verifique logs com:
```bash
docker-compose logs <nome-do-serviço>
```

---

## 📚 Referências

- [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
- [gRPC for Python](https://grpc.io/docs/languages/python/)
- [Flask Docs](https://flask.palletsprojects.com/)
- [Docker Docs](https://docs.docker.com/)

---
