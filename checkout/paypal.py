import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "Adl9_10CxHDSL-VZobkyiOhy49BTN2TvqnvCkSiVcz7hHcxVtiemh1EyOSkRQCBWfgRco8cvDUD9caJK"
        self.client_secret = "EHqp3TH-NHd6X5NPfc1pcDQtLg8_YTfCvObiVRF8lt2SAOUwlZZtCK8mrlIviUBaxLCbeRvfi4EufReT"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
