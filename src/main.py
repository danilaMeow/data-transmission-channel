
import os
from pathlib import Path

from loader import load_tasks
from calculations import (
    transmission_time,
    delivery_delay,
    arbitration_time,
    jitter,
    meets_deadline
)


# Включение поддержки цветов в консоли Windows.
if os.name == "nt":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    mode = ctypes.c_uint()

    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)


# Цвета текста.
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def main():
    # Путь к файлу с входными данными.
    filename = Path(__file__).resolve().parent.parent / "data" / "messages.csv"

    # Загрузка сообщений и параметров канала.
    messages, channel = load_tasks(filename)

    print("Расчет характеристик канала передачи данных")
    print()

    for msg in messages:
        # Расчет характеристик сообщения.
        tx = transmission_time(msg, channel)
        delay = delivery_delay(msg, channel)
        arbitration = arbitration_time(msg, messages, channel)

        # Расчет джиттера.
        jitter_value = jitter([delay, arbitration])

        # Проверка дедлайна.
        deadline = msg.period_ms
        result = meets_deadline(arbitration, deadline)

        print(f"Сообщение: {msg.name}")
        print(f"Приоритет: {msg.priority}")
        print(f"Время передачи: {tx:.3f} мс")
        print(f"Задержка доставки: {delay:.3f} мс")
        print(f"С учетом арбитража: {arbitration:.3f} мс")
        print(f"Оценка джиттера: {jitter_value:.3f} мс")
        print(f"Дедлайн: {deadline:.3f} мс")

        if result:
            # Зеленый текст, если дедлайн соблюден.
            print(f"Дедлайн соблюден: {GREEN}да{RESET}")
        else:
            # Красный текст, если дедлайн не соблюден.
            print(f"Дедлайн соблюден: {RED}нет{RESET}")

        print()


if __name__ == "__main__":
    main()
