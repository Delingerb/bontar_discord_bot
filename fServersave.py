from datetime import datetime, timedelta


current_time = datetime.utcnow()
# Create a time object for 10:00 a.m. in UTC (8:00 a.m. in CEST)
target_time = datetime(current_time.year, current_time.month, current_time.day, 8, 0, 0)

# Set the target time for the next day if it has already passed
if current_time.hour >= 8:
    target_time = target_time + timedelta(days=1)

# Calculate the remaining time in seconds
time_remaining = target_time - current_time
remaining_seconds = time_remaining.total_seconds()

# Calculate the remaining hours and minutes
remaining_hours = int(remaining_seconds // 3600)
remaining_minutes = int((remaining_seconds % 3600) // 60)

# Format the result in hh:mm format
toserversave = f"{remaining_hours:02d}:{remaining_minutes:02d}"
print(toserversave)
