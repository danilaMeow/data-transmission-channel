
import math

from model import Message, Channel


def transmission_time(msg: Message, channel: Channel) -> float:
    # Время передачи сообщения в миллисекундах.

    if channel.speed_bps <= 0:
        raise ValueError("Скорость канала должна быть больше нуля")

    return msg.size_bits / channel.speed_bps * 1000


def delivery_delay(msg: Message, channel: Channel) -> float:
    # Задержка доставки без конкуренции.

    return (
        transmission_time(msg, channel)
        + channel.propagation_delay_ms
        + channel.processing_delay_ms
    )


def arbitration_time(msg: Message, all_msgs: list[Message],
                     channel: Channel) -> float:
    # Время доставки с учетом более приоритетных сообщений.

    if msg.period_ms <= 0:
        raise ValueError("Период сообщения должен быть больше нуля")

    higher = [m for m in all_msgs if m.priority < msg.priority]

    time = transmission_time(msg, channel)

    for _ in range(1000):
        waiting = 0.0

        for m in higher:
            if m.period_ms <= 0:
                raise ValueError("Период сообщения должен быть больше нуля")

            count = math.ceil(time / m.period_ms)
            waiting += count * transmission_time(m, channel)

        new_time = transmission_time(msg, channel) + waiting

        if abs(new_time - time) < 1e-9:
            return (
                new_time
                + channel.propagation_delay_ms
                + channel.processing_delay_ms
            )

        if new_time > 1e9:
            return float("inf")

        time = new_time

    return float("inf")
