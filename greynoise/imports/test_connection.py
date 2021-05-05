from swimbundle_utils.helpers import create_test_conn
from sw_greynoise import GreynoiseBaseClass


class Test(GreynoiseBaseClass):
    def connect(self):
        response = self.session.test_connection()
        if response["message"] != "pong":
            raise Exception("Connection Error: " + response)


SwMain = create_test_conn(Test, "connect")
