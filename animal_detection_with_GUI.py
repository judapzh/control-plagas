animal_detection_with_GUI.py
import cv2
import tensorflow as tf
import numpy as np
import time
from gpiozero import LED
import threading
import tkinter as tk
from tkinter import messagebox

# Configuración de los pines GPIO (ajusta los números de pines según tu configuración)
altavoces = LED(17)  # Reemplaza 17 con el pin GPIO al que están conectados los altavoces
rociadores = LED(27)  # Reemplaza 27 con el pin GPIO al que están conectados los rociadores

# Cargar el modelo de IA pre-entrenado
modelo_IA = tf.keras.models.load_model('modelo_IA.h5')

# Función para procesar fotogramas del video
def procesar_fotograma(frame):
    # Preprocesamiento de la imagen
    img = cv2.resize(frame, (224, 224))  # Redimensionar a tamaño de entrada del modelo
    img = img / 255.0  # Normalización
    img = np.expand_dims(img, axis=0)  # Añadir dimensión batch

    # Aplicar el modelo de IA para reconocer características
    caracteristicas = modelo_IA.predict(img)

    # Aquí asumimos que el modelo devuelve una probabilidad de detección
    # Puedes ajustar esto según la salida específica de tu modelo
    if caracteristicas[0][0] > 0.5:  # Si la característica detectada supera un umbral
        print("Características detectadas:", caracteristicas)
        activar_dispositivos()

# Función para activar altavoces y rociadores
def activar_dispositivos():
    print("Activando altavoces y rociadores")
    
    # Encender altavoces por 2 minutos
    threading.Thread(target=encender_altavoces).start()

    # Encender rociadores por 25 segundos
    threading.Thread(target=encender_rociadores).start()

def encender_altavoces():
    altavoces.on()
    time.sleep(120)  # 2 minutos
    altavoces.off()

def encender_rociadores():
    rociadores.on()
    time.sleep(25)  # 25 segundos
    rociadores.off()

# Función para capturar video en tiempo real
def iniciar_captura_video():
    cap = cv2.VideoCapture(0)  # 0 para la cámara web, o ruta al archivo de video

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar fotograma
        procesar_fotograma(frame)

        # Mostrar fotograma en la ventana de la GUI
        cv2.imshow('Video', frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

# Función para iniciar la captura de video en un hilo separado
def iniciar_hilo_captura():
    threading.Thread(target=iniciar_captura_video).start()

# Crear la interfaz de usuario con tkinter
root = tk.Tk()
root.title("Detección de Animales en Tiempo Real")

# Crear y configurar los widgets
label = tk.Label(root, text="Presiona el botón para iniciar la detección de animales")
label.pack(pady=20)

button = tk.Button(root, text="Iniciar Detección", command=iniciar_hilo_captura)
button.pack(pady=20)

# Ejecutar el bucle principal de tkinter
root.mainloop()
