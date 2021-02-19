from greynoise import GreyNoise


class GreynoiseBaseClass(object):
    def __init__(self, context):
        self.api_key = context.asset["api_key"]
        self.session = GreyNoise(
            api_key=self.api_key, integration_name="greynoise-swimlane-v1.0.0"
        )
