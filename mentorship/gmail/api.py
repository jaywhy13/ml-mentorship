from __future__ import print_function

import os.path
import pickle
from datetime import date
from os.path import abspath, dirname
from typing import Optional, List, Dict

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from mentorship.gmail.data import Message, MessageId, Label, Header, MessagePart
from mentorship.gmail.factory import MessageFactory, MessageIdFactory

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILENAME = os.path.join(
    dirname(dirname(abspath(__file__))), "credentials.pickle"
)
SECRET_FILENAME = os.path.join(dirname(dirname(abspath(__file__))), "secret.json")


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

    def get_messages(
        self,
        after: Optional[date] = None,
        before: Optional[date] = None,
        includeSpamTrash: Optional[bool] = True,
        limit: Optional[int] = 1000,
    ) -> List[MessageId]:
        """ Retrieves emails for the user
        """
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
            )
            .execute()
        )
        messages = results.get("messages", [])
        return [MessageIdFactory.build(message) for message in messages]

    def get_message(self, id: str, user_id="me") -> Message:
        """Retrieves a single message
        """
        result = (
            self.get_service().users().messages().get(userId=user_id, id=id).execute()
        )
        return MessageFactory.build(result)

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
