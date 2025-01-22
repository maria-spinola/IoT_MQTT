import sqlite3

class DatabaseManager:
    def __init__(self, db_path='sensores.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_table()

    def _initialize_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS datos_sensores
                               (sensor_id TEXT, sensor_type TEXT, value REAL, 
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def insert_data(self, sensor_id, sensor_type, value):
        self.cursor.execute("INSERT INTO datos_sensores (sensor_id, sensor_type, value) VALUES (?, ?, ?)",
                            (sensor_id, sensor_type, value))
        self.conn.commit()

    def insert_batch(self, data_batch):
        self.cursor.executemany("INSERT INTO datos_sensores (sensor_id, sensor_type, value) VALUES (?, ?, ?)",
                                [(d['sensor_id'], d['sensor_type'], d['value']) for d in data_batch])
        self.conn.commit()

    def close(self):
        self.conn.close()
