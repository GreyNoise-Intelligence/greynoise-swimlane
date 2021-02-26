from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def execute(self):
        results = self.session.metadata()

        output = []
        for result in results["metadata"]:
            output.append(result)
        return output
