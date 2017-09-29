# Pasa las imágenes de un directorio a otro
import os
import sys
from azure.storage.blob import *

if len(sys.argv) != 7:
    print("Usage: python azure-blob-transfer.py account1 key1 container1 account2 key2 container2")

# Info de cuenta del directorio que contiene las imágenes a cambiar
myaccount_prev = sys.argv[1]
mykey_prev = sys.argv[2]
# Conexión
block_blob_service_prev = BlockBlobService(account_name=myaccount_prev, account_key=mykey_prev)

# Info de cuenta del directorio al que se mandarán los datos
myaccount_new = sys.argv[4]
mykey_new = sys.argv[5]
# Conexión
block_blob_service_new = BlockBlobService(account_name=myaccount_new, account_key=mykey_new)

# Directorios
#Directorio que tiene la imagen que quieres cambiar a otro directorio
img_container = sys.argv[3]
#Directorio a donde se mandará la imagen
img_container_desired = sys.argv[6]

# Folder de los blob
generator_prev = block_blob_service_prev.list_blobs(img_container[:-1])

# Ciclo por cada blob
for blob in generator_prev:
    # Guardar temporalmente un blob
    block_blob_service_prev.get_blob_to_path(img_container[:-1], blob.name, blob.name)

    # Crear blob en un container diferente, en este caso lo pasamos del folder general al que tendrá las imagenes consideradas como paredes y pilares
    block_blob_service_new.create_blob_from_path(img_container_desired[:-1], blob.name, blob.name,
                                             content_settings=ContentSettings(content_type=''))

    # Metodo para eliminar el blob del container inicial
    block_blob_service_prev.delete_blob(img_container[:-1], blob.name)

    # Remueve el archivo temporal
    os.remove(blob.name)