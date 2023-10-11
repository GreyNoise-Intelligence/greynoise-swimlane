from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.inputs = context.inputs

    def execute(self):
        response = self.session.timelinedaily(ip_address=self.inputs.get("ip_address"), days=self.inputs.get("days"), cursor=self.inputs.get("cursor"), limit=self.inputs.get("limit"))
        return response