from swimbundle_utils.helpers import create_test_conn
from sw_greynoise import GreynoiseBaseClass


class Test(GreynoiseBaseClass):
    def connect(self):
        response = str(self.session.test_connection())
        if response != "Success: Access and API Key Valid":
            raise Exception("Connection Error: " + response)


SwMain = create_test_conn(Test, "connect")
