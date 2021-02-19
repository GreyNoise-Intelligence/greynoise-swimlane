from sw_greynoise import GreynoiseBaseClass


class SwMain(GreynoiseBaseClass):
    def execute(self):
        response = str(self.session.test_connection())
        if response != "Success: Access and API Key Valid":
            return {
                "successful": False,
                "errorMessage": "API returned Code: " + str(response),
            }
        else:
            return {"successful": True}
