
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


# цвета в консоли
if os.name == "nt":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    mode = ctypes.c_uint()

    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def main():
    # Загрузка сообщений и параметро канала.
    filename = Path(__file__).resolve().parent.parent / "data" / "messages.csv"
    messages, channel = load_tasks(filename)

    print("Расчет характеристик канала передачи данных")
    print()

    print(f"Скорость канала: {channel.speed_bps:.0f} бит/с")
    print(f"Задержка распространения: {channel.propagation_delay_ms:.3f} мс")
    print(f"Задержка обработки: {channel.processing_delay_ms:.3f} мс")
    print()

    # Вывод заголовка таблицы.
    print(
        f"{'Имя':<8}"
        f"{'Приор.':<9}"
        f"{'Размер':<10}"
        f"{'Передача':<12}"
        f"{'Доставка':<12}"
        f"{'Арбитраж':<12}"
        f"{'Джиттер':<11}"
        f"{'Дедлайн':<11}"
        f"{'Итог'}"
    )

    print("-" * 95)

    results = []
    all_ok = True

    for msg in messages:
        # Параметры сообщения.
        tx = transmission_time(msg, channel)
        delay = delivery_delay(msg, channel)
        arb = arbitration_time(msg, messages, channel)
        jit = jitter([delay, arb])

        # Проверка соблюдения дедлайна.
        deadline = msg.period_ms
        ok = meets_deadline(arb, deadline)

        results.append((msg, delay, arb, jit))

        if ok:
            status = f"{GREEN}Да{RESET}"
        else:
            status = f"{RED}Нет{RESET}"
            all_ok = False

        # Вывод строки таблицы.
        print(
            f"{msg.name:<8}"
            f"{msg.priority:<9}"
            f"{msg.size_bits:<10}"
            f"{tx:<12.3f}"
            f"{delay:<12.3f}"
            f"{arb:<12.3f}"
            f"{jit:<11.3f}"
            f"{deadline:<11.3f}"
            f"{status}"
        )

    # Вывод.
    print()
    print("Вывод")

    for msg, delay, arb, jit in results:
        waiting = arb - delay

        print(
            f"{msg.name}: дополнительная задержка "
            f"{waiting:.3f} мс, джиттер {jit:.3f} мс"
        )

    if all_ok:
        print(f"\n{GREEN}Все сообщения укладываются в дедлайны.{RESET}")
    else:
        print(f"\n{RED}Некоторые сообщения нарушают дедлайны.{RESET}")


if __name__ == "__main__":
    main()
