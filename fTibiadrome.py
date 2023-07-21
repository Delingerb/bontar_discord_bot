from datetime import datetime, timedelta

# Definir la fecha objetivo para un miércoles específico
target_date = datetime(2023, 7, 26, 8, 0)
current_date = datetime.utcnow()
remaining_time = target_date - current_date

if remaining_time.total_seconds() <= 0:
    target_date += timedelta(days=14)
    remaining_time = target_date - current_date

days = remaining_time.days
remaining_hours, remaining_seconds = divmod(remaining_time.seconds, 3600)
remaining_minutes = remaining_seconds // 60

next_drome = f"{days} days {remaining_hours:02d}:{remaining_minutes:02d}"
print(next_drome)
