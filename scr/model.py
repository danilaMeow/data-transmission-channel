from dataclasses import dataclass


@dataclass
class Message:
    name: str
    priority: int
    size_bits: int
    period_ms: float


@dataclass
class Channel:
    speed_bps: float
    propagation_delay_ms: float
    processing_delay_ms: float