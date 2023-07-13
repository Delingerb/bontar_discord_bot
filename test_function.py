import math

def calculate_min_max_levels(user_level):
    minimum_level = math.ceil(user_level * (2/3))
    maximum_level = math.ceil(user_level * (3/2))

    message = f"A level {user_level} can share experience with levels **{minimum_level}** to **{maximum_level}**."
    return message

# Ejemplo de uso
user_level = int(input("Ingresa el nivel del usuario: "))
result_message = calculate_min_max_levels(user_level)
print(result_message)
