def calcular_experiencia(lvl_actual, lvl_deseado):
    experiencia_total = 0

    if lvl_actual >= lvl_deseado:
        mensaje = "Advertencia: El nivel actual debe ser menor al nivel deseado."
        return mensaje

    for nivel in range(lvl_actual, lvl_deseado):
        experiencia_nivel = 50 * nivel ** 2 - 150 * nivel + 200
        experiencia_total += experiencia_nivel

    experiencia_formateada = "{:,}".format(experiencia_total)
    mensaje = f"Para subir del nivel {lvl_actual} al nivel {lvl_deseado}, se necesitan {experiencia_formateada} puntos de experiencia."
    return mensaje

# Ejemplo de uso
lvl_actual = 59
lvl_deseado = 60

resultado = calcular_experiencia(lvl_actual, lvl_deseado)
print(resultado)
