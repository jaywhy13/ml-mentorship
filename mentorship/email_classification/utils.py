def extract_subject(row):
    headers = row.get("headers")
    matches = [
        header.get("value") for header in headers if header.get("name") == "Subject"
    ]
    if matches:
        return matches[0]
