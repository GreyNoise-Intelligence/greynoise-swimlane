from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.ip_address = context.inputs["ip_address"]

    def execute(self):
        output = []
        raw_data_subsections = ["scan", "web", "ja3", "hassh"]
        response = self.session.quick(self.ip_address, include_invalid=True)
        for result in response:
            if result["noise"]:
                context_response = self.session.ip(self.ip_address)
                context_response["viz_url"] = (
                        "https://www.greynoise.io/viz/ip/" + self.ip_address
                )
                context_response["noise"] = result["noise"]
                context_response["code"] = result["code"]
                context_response["code_message"] = result["code_message"]
                context_response["message"] = "Success."
                for section in raw_data_subsections:
                    if len(context_response["raw_data"][section]) > 1000:
                        context_response["raw_data"][section] = \
                            context_response["raw_data"][section][:1000]
                        context_response["message"] = \
                            str(context_response["message"]) + " Raw Data - " + section\
                            + " truncated to 1000 results."
                output.append(context_response)
            else:
                output.append(result)

        return output
