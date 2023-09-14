from greynoise import GreyNoise
from sw_greynoise import GreynoiseBaseClass

PLUGIN_VERSION = "v1.2.0"


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]
        self.api_key = context.asset["api_key"]
        self.session = GreyNoise(
            api_key=self.api_key,
            integration_name="greynoise-community-swimlane-" + PLUGIN_VERSION,
            offering="community",
        )

    def execute(self):
        output = []
        response = self.session.ip(self.ip_address)
        output.append(response)

        return output
