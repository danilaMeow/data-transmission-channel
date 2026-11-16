
from model import Message, Channel


def transmission_time(msg: Message, channel: Channel) -> float:
    # Время передачи сообщения в миллисекундах.
    if channel.speed_bps <= 0:
        raise ValueError("Скорость канала должна быть больше нуля")

    return msg.size_bits / channel.speed_bps * 1000


def delivery_delay(msg: Message, channel: Channel) -> float:
    # Задержка доставки без конкуренции в канале.
    return (
        transmission_time(msg, channel)
        + channel.propagation_delay_ms
        + channel.processing_delay_ms
    )
