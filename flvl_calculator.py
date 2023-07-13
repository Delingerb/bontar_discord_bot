def calculate_experience(current_lvl, desired_lvl):
    total_experience = 0

    if current_lvl >= desired_lvl:
        message = "Warning: The current level must be lower than the desired level."
        return message

    for level in range(current_lvl, desired_lvl):
        level_experience = 50 * level ** 2 - 150 * level + 200
        total_experience += level_experience

    formatted_experience = "{:,}".format(total_experience)
    message = f"To level up from {current_lvl} to {desired_lvl}, you need {formatted_experience} experience points."
    return message

# Usage example
current_lvl = 50
desired_lvl = 100

result = calculate_experience(current_lvl, desired_lvl)
print(result)
