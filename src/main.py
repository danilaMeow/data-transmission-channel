from pathlib import Path

from loader import load_tasks
from calculations import transmission_time, delivery_delay


def main():
    filename = Path(__file__).resolve().parent.parent / "data" / "messages.csv"

    messages, channel = load_tasks(filename)

    print("Расчет времени передачи и задержки доставки")

    for msg in messages:
        tx = transmission_time(msg, channel)
        delay = delivery_delay(msg, channel)

        print(f"Сообщение: {msg.name}")
        print(f"Время передачи: {tx:.3f} мс")
        print(f"Задержка доставки: {delay:.3f} мс")
        print()


if __name__ == "__main__":
    main()
