import time
from mqtt_handler import MQTTHandler
from database_manager import DatabaseManager
from data_processing import DataProcessor
from thread_handler import ThreadHandler
from threading import Event
from queue import Queue, Empty
from prometheus_client import start_http_server, Counter

# Configuración
BROKER_ADDRESS = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "sensor_data"
BATCH_SIZE = 200

# Métricas
data_saved = Counter("data_saved", "Number of data points saved to the database")

# Inicialización
data_queue = Queue(maxsize=5000)
filtered_data_queue = Queue(maxsize=5000)
stop_event = Event()

def filter_data():
    processor = DataProcessor()
    batch_data = []

    while not stop_event.is_set():
        try:
            data = data_queue.get()
            batch_data.append(data)

            if len(batch_data) >= BATCH_SIZE:
                filtered_data = processor.filter_outliers(batch_data)
                for item in filtered_data:
                    filtered_data_queue.put(item)
                batch_data.clear()
        except Empty:
            continue

    # Procesar datos restantes
    if batch_data:
        filtered_data = processor.filter_outliers(batch_data)
        for item in filtered_data:
            filtered_data_queue.put(item)

def manage_database():
    db_manager = DatabaseManager()
    insert_count = 0
    start_time = time.time()
    batch_data = []

    while not stop_event.is_set():
        try:
            data = filtered_data_queue.get()
            batch_data.append(data)
            if len(batch_data) >= BATCH_SIZE:
                db_manager.insert_batch(batch_data)
                batch_data.clear()
                data_saved.inc()
            
        except Empty:
            continue
    db_manager.close()

if __name__ == "__main__":
    try:
        # Inicia el servidor de métricas Prometheus
        start_http_server(8000)

        mqtt_handler = MQTTHandler(BROKER_ADDRESS, BROKER_PORT, TOPIC, stop_event, data_queue)
        
        # Iniciar los hilos
        mqtt_thread = ThreadHandler(target=mqtt_handler.start_mqtt_loop, stop_event=stop_event)
        filter_thread = ThreadHandler(target=filter_data, stop_event=stop_event)
        db_thread = ThreadHandler(target=manage_database, stop_event=stop_event)

        mqtt_thread.start()
        filter_thread.start()
        db_thread.start()

        # Esperar a que los hilos terminen
        mqtt_thread.join()
        filter_thread.join()
        db_thread.join()

    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        stop_event.set()
