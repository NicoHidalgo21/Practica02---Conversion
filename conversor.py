import json
from datetime import datetime
import random


def cargar_tasas(ruta):
    """Lee un archivo json y retorna un objeto"""
    with open(ruta, "r") as archivo:
        return json.load(archivo)


def convertir(precio_usd, moneda_destino, tasas):
    """Convierte el valor a otra moneda"""
    #Obtiene la tasa de cambio de USD a moneda destino   
    tasa = tasas["USD"].get(moneda_destino)
    #Si la moneda de destino no existe, lanza una excepción
    if not tasa:
        raise ValueError("Moneda no soportada")
    return precio_usd * tasa


def registrar_transaccion(producto, precio_convertido, moneda, ruta_log):
    """EScribe una nueva linea en el archivo de registro"""
    with open(ruta_log, "a") as archivo:
        # Obtener la fecha actual con formato yyyy-mm-dd HH:mm:ss
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #Escribir una linea nueva linea en el archivo de registro
        archivo.write(f"{fecha} | {producto}: {precio_convertido:.2f} {moneda}\n")

def actualizar_tasas(ruta):
    # Simular API: Cambiar tasas aleatoriamente ±2%
    with open(ruta, "r+") as archivo:
        tasas = json.load(archivo)
        for moneda in tasas["USD"]:
            tasas["USD"][moneda] *= 0.98 + (0.04 * random.random())
        tasas["actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.seek(0)
        json.dump(tasas, archivo, indent=2)


# Ejemplo de uso
if __name__ == "__main__":
    actualizar_tasas("data/tasas.json")
    tasas = cargar_tasas("data/tasas.json")
    precio_usd = 100.00
    eur = convertir(precio_usd, "EUR", tasas)
    registrar_transaccion("Laptop", eur, "EUR", "logs/historial.txt")
