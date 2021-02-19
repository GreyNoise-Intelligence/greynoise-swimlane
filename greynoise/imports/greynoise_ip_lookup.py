from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        riot_response = self.session.riot(self.ip_address)
        if "riot" in riot_response:
            riot_response["viz_url"] = (
                "https://viz.greynoise.io/riot/" + self.ip_address
            )
            output.append(riot_response)
        else:
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
                    output.append(context_response)
                else:
                    output.append(result)

        return output
