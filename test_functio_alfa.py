def minutes_to_hhmm(minutes):
    days = minutes // 1440
    hours = (minutes % 1440) // 60
    minutes = minutes % 60

    if days > 0:
        return f"{days} día(s) {hours:02d}:{minutes:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}"

# Función para convertir horas en formato hh:mm a minutos
def hhmm_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

current_stamina_str = input("Ingrese la estamina actual en formato hh:mm: ")
desired_stamina_str = input("Ingrese la estamina deseada en formato hh:mm: ")
regen_point_str = "39:00"  # Hora verde en formato hh:mm

current_stamina = hhmm_to_minutes(current_stamina_str)
desired_stamina = hhmm_to_minutes(desired_stamina_str)
regen_point = hhmm_to_minutes(regen_point_str)

# Calcular el tiempo de regeneración
if desired_stamina <= regen_point:
    time_to_regen = (regen_point - current_stamina) * 3
    time_to_regen += 10
else:
    time_to_regen = (regen_point - current_stamina ) * 3 + (desired_stamina - regen_point) * 6
    time_to_regen += 10
    
time_to_regen_formatted = minutes_to_hhmm(time_to_regen)
