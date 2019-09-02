from typing import Dict, Any
from base64 import urlsafe_b64decode

from mentorship.gmail.data import Message, MessageId, MessagePart, Header, Label


class MessageHeaderFactory:
    @classmethod
    def build(self, header: Dict[str, str]) -> Header:
        return Header(name=header["name"], value=header["value"])


class MessagePartFactory:
    @classmethod
    def build(cls, part: Dict[str, Any]) -> MessagePart:
        body = part["body"]["data"]
        return MessagePart(
            id=part["partId"],
            mime_type=part["mimeType"],
            filename=part["filename"],
            headers=[MessageHeaderFactory.build(header) for header in part["headers"]],
            # Decode the base64 encoded string
            body=str(urlsafe_b64decode(body), "utf-8"),
        )


class MessageFactory:
    @classmethod
    def build(cls, message: Dict[str, Any]):
        payload = message["payload"]
        message_id = MessageIdFactory.build(message)
        labels = [Label(id=label_id) for label_id in message["labelIds"]]
        headers = [MessageHeaderFactory.build(header) for header in payload["headers"]]
        message_parts = [MessagePartFactory.build(part) for part in payload["parts"]]

        return Message(
            id=message_id,
            date=message["internalDate"],
            snippet=message["snippet"],
            labels=labels,
            headers=headers,
            mime_type=payload["mimeType"],
            parts=message_parts,
        )


class MessageIdFactory:
    @classmethod
    def build(cls, message_id: Dict[str, str]) -> MessageId:
        return MessageId(id=message_id["id"], thread_id=message_id["threadId"])
