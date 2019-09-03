shell:
	pipenv run python

download_emails:
	pipenv run python tasks.py download_emails

download_labels:
	pipenv run python tasks.py download_labels

install:
	pipenv install

test:
	pipenv run pytest

start:
	pipenv run python tasks.py run_pipeline

clean:
	rm -rf mentorship/emails.pickle