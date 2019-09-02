from dataclasses import dataclass
from typing import List


@dataclass
class Label:

    id: str


@dataclass
class Header:

    name: str
    value: str


@dataclass
class MessageId:

    id: str
    thread_id: str


@dataclass
class MessagePart:

    id: str
    mime_type: str
    filename: str
    headers: List[Header]
    body: str


@dataclass
class Message:

    id: MessageId
    date: float
    snippet: str
    labels: List[Label]
    headers: List[Header]
    mime_type: str
    parts: List[MessagePart]

