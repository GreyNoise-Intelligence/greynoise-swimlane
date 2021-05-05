from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        response = {}
        riot_response = self.session.riot(self.ip_address)
        if riot_response["riot"]:
            riot_response["viz_url"] = (
                "https://viz.greynoise.io/riot/" + self.ip_address
            )
            riot_response["classification"] = "benign"
            response.update(riot_response)
        if not riot_response["riot"]:
            response.update(riot_response)

        quick_response = self.session.quick(self.ip_address, include_invalid=True)
        for result in quick_response:
            if result["noise"]:
                context_response = self.session.ip(self.ip_address)
                context_response["viz_url"] = (
                    "https://viz.greynoise.io/ip/" + self.ip_address
                )
                context_response["noise"] = result["noise"]
                context_response["code"] = result["code"]
                context_response["code_message"] = result["code_message"]
                response.update(context_response)
            else:
                response.update(result)

        output.append(response)

        return output
