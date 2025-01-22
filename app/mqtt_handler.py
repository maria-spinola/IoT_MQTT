import paho.mqtt.client as mqtt
import json
import time
from queue import Queue

import paho.mqtt.client as mqtt
import json
import time
from queue import Queue
from prometheus_client import Counter
messages_received = Counter("messages_received", "Number of messages received from MQTT broker")

class MQTTHandler:
    def __init__(self, broker_address, broker_port, topic, stop_event, data_queue):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.stop_event = stop_event
        self.data_queue = data_queue
        self.client = mqtt.Client()
        self.message_count = 0
        self.start_time = time.time()

    def on_message(self, client, userdata, message):
        self.message_count += 1
        data = json.loads(message.payload.decode("utf-8"))
        self.data_queue.put(data)
        messages_received.inc()

        # Calcular el número de mensajes por segundo
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1:
            print(f"Mensajes recibidos por segundo: {self.message_count}")
            self.message_count = 0
            self.start_time = time.time()

    def start_mqtt_loop(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.subscribe(self.topic)
        self.client.on_message = self.on_message

        # Iniciar el bucle MQTT en un hilo
        self.client.loop_forever()

        