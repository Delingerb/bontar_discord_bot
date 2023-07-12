import pytz
from datetime import datetime

def obtener_hora(pais):
    try:
        zona_horaria = pytz.timezone(pais)
        hora_actual = datetime.now(tz=zona_horaria)
        return hora_actual.strftime('%Y-%m-%d %H:%M:%S')
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"No se encontró la zona horaria para {pais}")

# Ejemplo de uso
hora_arg = obtener_hora('America/Buenos_Aires')  
hora_chile = obtener_hora('America/Santiago')
hora_ecuador = obtener_hora('America/Guayaquil')
hora_mex = obtener_hora('America/Mexico_City')
hora_estados_unidos = obtener_hora('America/New_York') 
hora_espana = obtener_hora('Europe/Madrid') 

