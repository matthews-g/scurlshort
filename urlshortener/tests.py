from rest_framework.test import RequestsClient, APITestCase
import json
import string
import random

# Correct usage means the successful queries that were mandatory according to the document
# Incorrect usage means the unsuccessful queries that were mandatory according to the document


class TestBase(APITestCase):

    def __init__(self, client: RequestsClient, server_address: str, url_shortcode: dict):
        self.client = client
        self.server_address = server_address
        self.url = ""
        self.url_shortcode = url_shortcode  # For manual shortcode testing

    """def test_correct(self):
        response = self.client.post(self.url, data=self.url_shortcode)  # example
        # test the optimal usage
        pass

    def test_incorrect(self):
        # test incorrect usage
        pass

    def test_all(self):
        self.test_correct()
        self.test_incorrect()"""


class ShortenTest(TestBase):
    def __init__(self, client, server_address, url_shortcode):
        super().__init__(client, server_address, url_shortcode)

        self.url = self.server_address + "shorten/"

    def test_correct(self):
        # Automatic shortcode
        response = self.client.post(self.url, data={"url": "https://www.example.com/"})
        json_resp = json.loads(response.text)
        assert response.status_code == 201, "Response code should be 201"
        assert json_resp['shortcode'] is not None, "Shortcode should be in response"

        # Manual shortcode
        response = self.client.post(self.url, data=self.url_shortcode)
        json_resp = json.loads(response.text)
        assert response.status_code == 201, "Response code should be 201"
        assert json_resp['shortcode'] is not None, "Shortcode should be in response"

        print("All shortening related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        # We only check for status codes because they are explicitly declared with the error msg
        # Only after correct testing!

        response = self.client.post(self.url, data={"url": "https://www.example.com/", "shortcode": "ß$a123"})
        assert response.status_code == 412, "Response code should be 412"
        response = self.client.post(self.url, data={"url": "", "shortcode": "ß$a123"})
        assert response.status_code == 400, "Response code should be 400"
        response = self.client.post(self.url, data=self.url_shortcode)
        assert response.status_code == 409, "Response code should be 409"

        print("All shortening related tests passed regarding incorrect cases!")
        return True


class ShortCodeTest(TestBase):
    def __init__(self, client: RequestsClient, server_address: str, url_shortcode: dict):
        super().__init__(client, server_address, url_shortcode)
        self.url = self.server_address+url_shortcode['shortcode']+"/"
        self.incorrect_url = self.server_address+"te$$$/"

    def test_correct(self):
        response = self.client.get(self.url, allow_redirects=False)  # Redirects disabled
        assert response.status_code == 302, "Response code should be 302"
        print("All shortcode redirect related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        response = self.client.get(self.incorrect_url, allow_redirects=False)  # Redirects disabled
        assert response.status_code == 404, "Response code should be 404"
        print("All shortcode redirect related tests passed regarding incorrect cases!")
        return True


class StatTest(TestBase):
    def __init__(self, client: RequestsClient, server_address: str, url_shortcode: dict):
        super().__init__(client, server_address, url_shortcode)
        self.url = self.server_address+url_shortcode['shortcode']+"/stats/"
        self.incorrect_url = self.server_address + "te$$$/stats/"

    def test_correct(self):
        response = self.client.get(self.url)
        json_resp = json.loads(response.text)
        assert response.status_code == 200, "Response code should be 200"
        assert json_resp['created'] is not None, "Created should not be none!"
        assert json_resp['lastRedirect'] is not None, "lastRedirect should not be none!"
        assert json_resp['redirectCount'] is not None, "redirectCount should not be none!"
        print("All shortcode redirect related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        response = self.client.get(self.incorrect_url)
        assert response.status_code == 404, "Response code should be 404"
        print("All shortcode redirect related tests passed regarding incorrect cases!")
        return True


def main():
    # This is the main function to run the tests
    # Variables
    code_chars = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits + "_")

    test_shortcode = random.sample(code_chars, 6)

    client = RequestsClient()

    server_address = "http://127.0.0.1:8000/"
    url_shortcode = {"url": "https://www.example.com/", "shortcode": "".join(test_shortcode)}

    shorten_test = ShortenTest(client, server_address, url_shortcode)
    shorten_test.test_all()

    shortcode_test = ShortCodeTest(client, server_address, url_shortcode)
    shortcode_test.test_all()

    stat_test = StatTest(client, server_address, url_shortcode)
    stat_test.test_all()

    print("All tests passed in all cases, the API is working correctly!")
    return True


if __name__ == '__main__':
    main()
