from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        response = self.session.quick(self.ip_address, include_invalid=True)
        for result in response:
            output.append(result)

        return output
