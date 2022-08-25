"""

SR - CPU Design

"""

import warnings
import requests
import my_logger

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

"""

class to connect to CPPM

"""


class CPPM:
    def __init__(
        self,
        username,
        password,
        m_ip,
        ssl_verify=False,
    ):

        self.client_id = username
        self.client_secret = password
        self.ip = m_ip
        self.access_token = None
        self.session = requests.Session()
        self.ssl_verify = ssl_verify
        self.baseurl = f"https://{m_ip}/api"
        self. headers = {'Content-Type': 'application/json'}
        self.payload = {"grant_type": "client_credentials",
                        "client_id": self.client_id, "client_secret": self.client_secret}

    def token(self):
        url = f"{self.baseurl}/oauth"

        with requests.Session() as session:
            if not self.ssl_verify:
                requests.packages.urllib3.disable_warnings()
            response = session.post(
                url, json=self.payload, headers=self.headers, verify=self.ssl_verify)
            parsed = response.json()
            self.access_token = parsed["access_token"]
        return parsed

    def guest(self):
        token_type = "Bearer"
        url = f"{self.baseurl}/guest?filter=%7B%22%24and%22%3A%5B%7B%22current_state%22%3A+%22disabled%22%7D%2C%7B%22role_name%22%3A+%22WIFI-VISITEUR%22%7D%5D%7D&sort=-id&sort=-id&offset=0&limit=1000&calculate_count=false"
        headers = {'Content-Type': 'application/json',
                   "Authorization": "{} {}".format(token_type, self.access_token)}
        response = self.session.get(
            url, headers=headers, verify=self.ssl_verify)
        parsed = response.json()
        for item in parsed['_embedded']['items']:
            if item['current_state'] == "disabled" and item['role_name'] == "WIFI-VISITEUR":
                client_id = item['id']
                urld = f"{self.baseurl}/guest/{client_id}"
                response = self.session.delete(
                    urld, headers=headers, verify=self.ssl_verify)
                url = response.url.partition('guest')
                server = url[0].strip('https://').strip('/api')
                guest_id = url[2].strip('/')
                my_logger.main_logger.info(
                    f'NAC server {server}: Guest id :{guest_id} was deleted successfully')
        return len(parsed['_embedded']['items'])
