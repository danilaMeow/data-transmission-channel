import csv
from pathlib import Path

from model import Message, Channel


def load_tasks(filename):
    # Загрузка сообщений и параметров канала из CSV.

    messages = []
    channel = None
    names = set()
    priorities = set()

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        # Проверка наличия необходимых столбцов.
        required = {
            "name",
            "priority",
            "size_bits",
            "period_ms",
            "speed_bps",
            "propagation_delay_ms",
            "processing_delay_ms"
        }

        if reader.fieldnames is None:
            raise ValueError("CSV-файл пуст")

        missing = required - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Отсутствуют столбцы: {', '.join(sorted(missing))}"
            )

        for number, row in enumerate(reader, start=2):
            try:
                # Создание сообщения.
                message = Message(
                    name=row["name"].strip(),
                    priority=int(row["priority"]),
                    size_bits=int(row["size_bits"]),
                    period_ms=float(row["period_ms"])
                )

                # Создание параметров канала.
                current_channel = Channel(
                    speed_bps=float(row["speed_bps"]),
                    propagation_delay_ms=float(row["propagation_delay_ms"]),
                    processing_delay_ms=float(row["processing_delay_ms"])
                )

            except (ValueError, TypeError, AttributeError, KeyError) as error:
                raise ValueError(
                    f"Некорректные данные в строке {number}: {error}"
                ) from error

            # Проверка имени сообщения.
            if not message.name:
                raise ValueError(f"Строка {number}: пустое имя сообщения")

            if message.name in names:
                raise ValueError(f"Повторяется имя: {message.name}")

            names.add(message.name)

            # Проверка приоритета.
            if message.priority <= 0:
                raise ValueError(
                    f"Строка {number}: приоритет должен быть больше нуля"
                )

            if message.priority in priorities:
                raise ValueError(
                    f"Строка {number}: повторяется приоритет "
                    f"{message.priority}"
                )

            priorities.add(message.priority)

            # Проверка размера и периода сообщения.
            if message.size_bits <= 0:
                raise ValueError(
                    f"Строка {number}: размер должен быть больше нуля"
                )

            if not (0 < message.period_ms < float("inf")):
                raise ValueError(
                    f"Строка {number}: период должен быть положительным"
                )

            # Проверка параметров канала.
            # current_channel.speed_bps - скорость канала в битах в секунду
            if not (0 < current_channel.speed_bps < float("inf")):
                raise ValueError(
                    "Скорость канала должна быть положительной"
                )

            # current_channel.propagation_delay_ms - задержка распространения в миллисекундах
            if not (0 <= current_channel.propagation_delay_ms < float("inf")):
                raise ValueError(
                    "Некорректная задержка распространения"
                )
            # current_channel.processing_delay_ms - задержка обработки в миллисекундах
            if not (0 <= current_channel.processing_delay_ms < float("inf")):
                raise ValueError(
                    "Некорректная задержка обработки"
                )

            # Проверка одинаковых параметров канала.
            if channel is None:
                channel = current_channel
            elif channel != current_channel:
                raise ValueError(
                    "Параметры канала должны совпадать "
                    "для всех сообщений"
                )

            messages.append(message)

    if not messages:
        raise ValueError("CSV-файл не содержит сообщений")

    return messages, channel


if __name__ == "__main__":
    # Проверка загрузки CSV.
    filename = Path(__file__).resolve().parent.parent / "data" / "messages.csv"

    messages, channel = load_tasks(filename)

    print("Параметры канала:")
    print(channel)

    print("\nЗагруженные сообщения:")

    for message in messages:
        print(message)

