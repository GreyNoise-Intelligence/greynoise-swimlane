from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.tag_name = context.inputs["tag_name"]

    def execute(self):
        results = self.session.metadata()

        output = []
        for result in results["metadata"]:
            if result["name"] == self.tag_name:
                output.append(result)
        return output
