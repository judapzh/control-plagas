import cv2
import tensorflow as tf
import numpy as np
import time
from gpiozero import LED
import threading
from flask import Flask, render_template, Response

# Configuración de los pines GPIO (ajusta los números de pines según tu configuración)
altavoces = LED(17)  # Reemplaza 17 con el pin GPIO al que están conectados los altavoces
rociadores = LED(27)  # Reemplaza 27 con el pin GPIO al que están conectados los rociadores

# Cargar el modelo de IA pre-entrenado
modelo_IA = tf.keras.models.load_model('modelo_IA.h5')

# Inicializa Flask
app = Flask(__name__)

def procesar_fotograma(frame):
    img = cv2.resize(frame, (224, 224))  # Redimensionar a tamaño de entrada del modelo
    img = img / 255.0  # Normalización
    img = np.expand_dims(img, axis=0)  # Añadir dimensión batch

    # Aplicar el modelo de IA para reconocer características
    caracteristicas = modelo_IA.predict(img)

    if caracteristicas[0][0] > 0.5:  # Si la característica detectada supera un umbral
        print("Características detectadas:", caracteristicas)
        activar_dispositivos()

def activar_dispositivos():
    threading.Thread(target=encender_altavoces).start()
    threading.Thread(target=encender_rociadores).start()

def encender_altavoces():
    altavoces.on()
    time.sleep(120)  # 2 minutos
    altavoces.off()

def encender_rociadores():
    rociadores.on()
    time.sleep(25)  # 25 segundos
    rociadores.off()

def generar():
    cap = cv2.VideoCapture(0)  # 0 para la cámara web, o ruta al archivo de video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        procesar_fotograma(frame)

        # Codificar el frame como JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generar(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

