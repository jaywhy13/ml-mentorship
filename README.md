# Machine Learning Mentorship

Code for my ML Mentorship with `#noneofconsequence`.

## Setup

1. Go to [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/js) and enable the **Gmail API**.

2. Download the Client Configuration (`credentials.json`) and save it as `mentorship/secret.json` (note the rename).

3. Setup a `.env` file with the following optional properties.

```ini
DEBUG_PIPELINE=0 # Set to 1 to stop at each stage of the pipeline
NUMBER_OF_EMAILS=100000 # Number of emails to download in the obtain step of the pipeline
```

4. Install and run the pipeline

```bash
# Install requirements
$ make install
# run the email classification pipleine
$ make start
```

## Playbook

### Fetching a list of messaging from Google

```python
from mentorship.gmail.api import GmailApi
api = GmailApi()
api.initialize() # opens browser to authenticate
messages = api.get_messages(after="2019/01/01", limit=1000)
```
