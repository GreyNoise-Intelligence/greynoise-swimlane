from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        raw_data_subsections = ["scan", "web", "ja3", "hassh"]
        response = {}

        quick_response = self.session.quick(self.ip_address, include_invalid=True)

        for result in quick_response:
            if result.get("noise") or result.get("riot"):
                response["noise"] = result.get("noise")
                response["riot"] = result.get("riot")
                response["code"] = result.get("code")
                response["code_message"] = result.get("code_message")
                response["viz_url"] = "https://viz.greynoise.io/ip/" + self.ip_address
            if result["riot"]:
                riot_response = self.session.riot(self.ip_address)
                riot_response["classification"] = "RIOT"
                response.update(riot_response)

            if result["noise"]:
                context_response = self.session.ip(self.ip_address)
                context_response["message"] = "Success."
                for section in raw_data_subsections:
                    if len(context_response["raw_data"][section]) > 1000:
                        context_response["raw_data"][section] = context_response["raw_data"][section][:1000]
                        context_response["message"] = (
                            str(context_response["message"]) + " Raw Data - " + section + " truncated to 1000 results."
                        )
                response.update(context_response)
            else:
                response.update(result)

        output.append(response)

        return output
