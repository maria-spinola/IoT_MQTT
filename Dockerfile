# Usar una imagen base ligera de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt desde la raíz del proyecto al contenedor
COPY requirements.txt ./

# Instalar las dependencias definidas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos de la aplicación al contenedor
COPY app/ /app/

# Exponer el puerto 8000 para las métricas de Prometheus
EXPOSE 8000

# Establecer el comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
