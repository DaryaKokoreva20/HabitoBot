import re
from datetime import time


def parse_time_input(text: str, context: str = None) -> time | None:
    text = text.replace('.', ':').strip()

    try:
        return time.fromisoformat(text)
    except ValueError:
        pass

    numbers = list(map(int, re.findall(r'\d+', text)))

    if len(numbers) >= 2:
        h, m = numbers[0], numbers[1]
    elif len(numbers) == 1:
        h, m = numbers[0], 0
    else:
        return None
    
    if context == 'sleep':
        if 8 <= h <= 12:
            # Преобразуем "10" в "22", "11" в "23", "12" в "0"
            h = (h + 12) % 24

    if 0 <= h < 24 and 0 <= m < 60:
        return time(hour=h, minute=m)

    return None


import re
from datetime import time

def parse_time_input(user_input: str, context: str = None) -> time | None:
    # Извлекаем число
    numbers = re.findall(r'\d+', user_input)

    if not numbers:
        return None

    hour = int(numbers[0])
    minute = int(numbers[1]) if len(numbers) > 1 else 0

    # Обработка специального случая сна
    if context == 'sleep':
        if 8 <= hour <= 12:
            # Преобразуем "10" в "22", "11" в "23", "12" в "0"
            hour = (hour + 12) % 24

    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return time(hour, minute)

    return None
