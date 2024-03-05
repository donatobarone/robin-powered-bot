import email
import os

from robot.requests import RetrySession


class UserInfo:

    USER_URL_TEMPLATE = "https://api.robinpowered.com/v1.0/users/{}"

    def __init__(self, email: str, stime: int, duration: int, sid: int, rid: int = None, tz: str = None):
        self.email = email
        self.seat_id = sid
        self.start_time = stime
        self.duration = duration
        user_info = self._get_user_info() if not rid or not tz else None
        self.reserver_id = rid if rid else user_info['id']
        self.timezone = tz if tz else user_info['time_zone']

        self._token = os.getenv("ROBIN_AUTH_TOKEN")
        self._session = RetrySession()
        self._session.headers = {"Authorization": f"Access-Token {self._token}"}
        self._session.verify = False

    @classmethod
    def build_user_url(cls, email: str) -> str:
        return cls.USER_URL_TEMPLATE.format(email)

    def _get_user_info(self):
        url = self.build_user_url(self.email)
        response = self._session.get(url)
        if response.status_code == 200:
            return response.json()['data']

        raise Exception(f"user {email} not found")
