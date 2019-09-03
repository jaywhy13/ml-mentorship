from typing import List
import os
from os.path import dirname, abspath
import pickle
from datetime import datetime

from pandas import DataFrame
from tqdm import tqdm


from mentorship.engine import Step
from mentorship.gmail.api import GmailApi
from mentorship.email_classification.utils import extract_subject

gmail_api = GmailApi()

EMAIL_DATABASE_FILENAME = os.path.join(
    dirname(dirname(abspath(__file__))), "emails.pickle"
)
RETRIEVE_EMAILS_BEFORE = datetime.strptime(
    os.getenv("RETRIEVE_EMAILS_BEFORE", "2019/09/01"), "%Y/%m/%d"
)
NUMBER_OF_EMAILS = int(os.getenv("NUMBER_OF_EMAILS", "1"))


def identity(dataframe: DataFrame) -> DataFrame:
    """No-op, just return the input
    """
    return dataframe


def obtain_emails(dataframe: DataFrame) -> DataFrame:
    print(f"Will obtain maximum of {NUMBER_OF_EMAILS} emails")
    gmail_api.initialize()
    if os.path.exists(EMAIL_DATABASE_FILENAME):
        print(f"Retrieving emails from {EMAIL_DATABASE_FILENAME}")
        messages = pickle.load(open(EMAIL_DATABASE_FILENAME, "rb"))
    else:
        print("Retrieving message ids")
        message_ids = gmail_api.get_messages(
            limit=NUMBER_OF_EMAILS, before=RETRIEVE_EMAILS_BEFORE
        )
        messages = []
        print("Downloading emails")
        for message_id in tqdm(message_ids):
            messages.append(gmail_api.get_message(message_id.id))
        with open(EMAIL_DATABASE_FILENAME, "wb") as f:
            pickle.dump(messages, f)
    print(f"Retrieved {len(messages)} emails")
    return DataFrame([message.to_dict() for message in messages])


def scrub_emails(dataframe: DataFrame) -> DataFrame:
    dataframe["subject"] = dataframe.apply(extract_subject, axis=1)
    return dataframe


def get_pipeline_steps() -> List[Step]:
    pipeline_steps: List[Step] = [
        obtain_emails,
        scrub_emails,
        identity,
        identity,
        identity,
    ]
    return pipeline_steps
