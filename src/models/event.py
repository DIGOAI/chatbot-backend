class Event():
    def __init__(self, event: dict[str, str]) -> None:
        self.body = event['Body']
        self.from_phone = event['From']
        self.to_phone = event['To']
        self.media_url = event['MediaUrl0']
