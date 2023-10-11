from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.inputs = context.inputs

    def execute(self):
        response = self.session.similar(
            ip_address=self.inputs.get("ip_address"),
            limit=self.inputs.get("limit"),
            min_score=self.inputs.get("min_score"),
        )
        return response
