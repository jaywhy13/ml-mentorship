shell:
	pipenv run python

download_emails:
	pipenv run python tasks.py download_emails

download_labels:
	pipenv run python tasks.py download_labels

run:
	pipenv run python tasks.py run_pipeline

clean:
	rm -rf mentorship/emails.pickle