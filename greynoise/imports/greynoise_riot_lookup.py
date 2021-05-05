from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        response = self.session.riot(self.ip_address)
        if response["riot"]:
            response["viz_url"] = "https://viz.greynoise.io/riot/" + self.ip_address
            riot_response["classification"] = "benign"
        output.append(response)

        return output
