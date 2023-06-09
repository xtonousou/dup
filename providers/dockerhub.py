import requests


class Provider(object):

    def __init__(self, session: requests.Session, token: str):
        self.session = session
        self.session.headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
        }

    def compare_image(self, image: dict):
        namespace = image["name"]
        tag = image["tag"]

        print(namespace, tag, sep=" ---- ")
