import os
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

# Definir las rutas de las carpetas de origen y destino
source_dir = 'ruta/a/tu/carpeta/de/imagenes'
dest_dir = 'ruta/a/tu/carpeta/de/dataset'

# Crear las carpetas de destino si no existen
os.makedirs(dest_dir, exist_ok=True)

# Función para copiar imágenes a la carpeta de destino
def copy_images_to_dataset(source_dir, dest_dir):
    for category in os.listdir(source_dir):
        category_path = os.path.join(source_dir, category)
        if os.path.isdir(category_path):
            dest_category_path = os.path.join(dest_dir, category)
            os.makedirs(dest_category_path, exist_ok=True)
            for img_name in os.listdir(category_path):
                img_path = os.path.join(category_path, img_name)
                if img_name.endswith(('jpg', 'jpeg', 'png')):  # Asegurarse de que sea una imagen
                    shutil.copy(img_path, dest_category_path)

# Copiar imágenes
copy_images_to_dataset(source_dir, dest_dir)

# Definir los parámetros del preprocesamiento
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32

# Crear un generador de datos para cargar y preprocesar las imágenes
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2  # Usar un 20% de las imágenes para validación
)

train_generator = datagen.flow_from_directory(
    dest_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'  # Datos de entrenamiento
)

validation_generator = datagen.flow_from_directory(
    dest_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'  # Datos de validación
)