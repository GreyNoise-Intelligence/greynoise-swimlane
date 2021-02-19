from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.query = context.inputs["query"]
        self.limit = context.inputs["limit"]

    def execute(self):
        output = []
        response = self.session.query(self.query, size=self.limit)
        if response["count"] >= 1:
            for result in response["data"]:
                result["viz_url"] = "https://viz.greynoise.io/ip/" + result["ip"]
                output.append(result)

        else:
            output.append(response)

        return output
