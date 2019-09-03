from __future__ import print_function

import os.path
import pickle
from datetime import date
from os.path import abspath, dirname
from typing import Optional, List, Dict

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from diskcache import Cache

from mentorship.gmail.data import Message, MessageId
from mentorship.gmail.factory import MessageFactory, MessageIdFactory

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILENAME = os.path.join(
    dirname(dirname(abspath(__file__))), "credentials.pickle"
)
SECRET_FILENAME = os.path.join(dirname(dirname(abspath(__file__))), "secret.json")
CACHE_LOCATION = os.getenv("CACHE_LOCATION", "/tmp/ml-mentorship-cache")

cache = Cache(CACHE_LOCATION)


class GmailApi:
    def initialize(self):
        """Calling this authenticates the user with Gmail and builds the internal client
        """
        if not hasattr(self, "_service"):
            self.authenticate()
            self._service = build("gmail", "v1", credentials=self.credentials)

    def get_labels(self):
        results = self.get_service().users().labels().list(userId="me").execute()
        return results

    def get_messages_for_page(
        self,
        after: Optional[date] = None,
        before: Optional[date] = None,
        includeSpamTrash: Optional[bool] = True,
        limit: Optional[int] = 1000,
        page_token: Optional[str] = None,
    ):
        query = self.build_query(after=after, before=before)
        results = (
            self.get_service()
            .users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=limit,
                includeSpamTrash=includeSpamTrash,
                pageToken=page_token,
            )
            .execute()
        )
        return results

    def get_messages(
        self,
        after: Optional[date] = None,
        before: Optional[date] = None,
        includeSpamTrash: Optional[bool] = True,
        limit: int = 1000,
    ) -> List[MessageId]:
        """ Retrieves emails for the user
        """
        cache_key = f"message-ids-{after}-{before}-{limit}-{includeSpamTrash}"
        if cache_key in cache:
            return cache[cache_key]
        messages: List[Dict[str, str]] = []
        next_page_token = None
        while True:
            result = self.get_messages_for_page(
                after=after,
                before=before,
                includeSpamTrash=includeSpamTrash,
                limit=limit,
                page_token=next_page_token,
            )
            messages_on_page = result.get("messages")
            messages.extend(messages_on_page)
            next_page_token = result.get("nextPageToken")
            if not next_page_token or len(messages) > limit:
                # Google doesn't seem to be respecting the limit we pass,
                # so limit things manually here
                break
        # Truncate the messages
        messages = messages[:limit]
        message_ids = [MessageIdFactory.build(message) for message in messages]
        cache.set(cache_key, message_ids, expire=None)
        return message_ids

    def get_message(self, id: str, user_id="me") -> Message:
        """Retrieves a single message
        """
        cache_key = f"message-{id}"
        if cache_key in cache:
            return cache[cache_key]
        result = (
            self.get_service().users().messages().get(userId=user_id, id=id).execute()
        )
        message = MessageFactory.build(result)
        cache.set(cache_key, message, expire=None)
        return message

    def build_query(
        self, after: Optional[date] = None, before: Optional[date] = None
    ) -> str:
        queries = []
        if after:
            queries.append(f"after:{as_date(after)}")
        if before:
            queries.append(f"before:{as_date(before)}")
        return " ".join(queries)

    def get_service(self):
        if not hasattr(self, "_service"):
            raise Exception("Call initialize(), service hasn't been created yet")
        return self._service

    def authenticate(self):
        self.credentials = self.get_or_create_credentials()

        # Refresh the token if necessary
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())

    def get_or_create_credentials(self):
        if os.path.exists(CREDENTIALS_FILENAME):
            with open(CREDENTIALS_FILENAME, "rb") as credentials_file:
                credentials = pickle.load(credentials_file)
                if credentials.valid:
                    return credentials

        # Do the authorization flow
        flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILENAME, SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials
        with open(CREDENTIALS_FILENAME, "wb") as credentials_file:
            pickle.dump(credentials, credentials_file)

        assert credentials
        return credentials


def as_date(date: date):
    return date.strftime("%Y/%m/%d")
