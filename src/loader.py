import csv
from pathlib import Path

from model import Message, Channel


def load_tasks(filename):
    #Загрузка сообщений и параметров канала из CSV.

    messages = []
    channel = None

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            message = Message(
                name=row["name"],
                priority=int(row["priority"]),
                size_bits=int(row["size_bits"]),
                period_ms=float(row["period_ms"])
            )
            messages.append(message)

            current_channel = Channel(
                speed_bps=float(row["speed_bps"]),
                propagation_delay_ms=float(row["propagation_delay_ms"]),
                processing_delay_ms=float(row["processing_delay_ms"])
            )

            if channel is None:
                channel = current_channel
            elif channel != current_channel:
                raise ValueError(
                    "Параметры канала должны быть одинаковыми "
                    "для всех сообщений"
                )

    if not messages:
        raise ValueError("Файл CSV не содержит сообщений")

    return messages, channel


if __name__ == "__main__":
    filename = Path(__file__).resolve().parent.parent / "data" / "messages.csv"

    messages, channel = load_tasks(filename)

    print("Параметры канала:")
    print(channel)

    print("\nЗагруженные сообщения:")
    for message in messages:
        print(message)
