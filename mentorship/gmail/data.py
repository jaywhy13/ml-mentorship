from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class Label:

    id: str


@dataclass_json
@dataclass
class Header:

    name: str
    value: str


@dataclass_json
@dataclass
class MessageId:

    id: str
    thread_id: str


@dataclass_json
@dataclass
class MessagePart:

    id: str
    mime_type: str
    filename: str
    headers: List[Header]
    body: str


@dataclass_json
@dataclass
class Message:

    id: MessageId
    date: float
    snippet: str
    labels: List[Label]
    headers: List[Header]
    mime_type: str
    parts: List[MessagePart]

