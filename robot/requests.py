import requests
import requests.adapters


class RetrySession(requests.Session):
    _ALLOWED_METHODS = ["GET", "POST", "PUT"]
    _BACKOFF_FACTOR = 2
    _MOUNT_PROTOCOLS = ["http://", "https://"]
    _RAISE_ON_STATUS = True
    _RETRY_COUNT = 5
    _STATUS_FORCELIST = [429, 500, 502, 503, 504]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        retry_strategy = requests.adapters.Retry(
            total=self._RETRY_COUNT,
            allowed_methods=self._ALLOWED_METHODS,
            status_forcelist=self._STATUS_FORCELIST,
            backoff_factor=self._BACKOFF_FACTOR,
            raise_on_status=self._RAISE_ON_STATUS,
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)

        for protocol in self._MOUNT_PROTOCOLS:
            self.mount(protocol, adapter)
