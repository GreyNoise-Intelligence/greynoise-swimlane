from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def __init__(self, context):
        super(SwMain, self).__init__(context)

    def execute(self):
        results = self.session.metadata()

        output = []
        for result in results["metadata"]:
            output.append(result)
        return output
