from rest_framework.test import RequestsClient, APITestCase
import json
import string
import random

# Correct usage means the successful queries that were mandatory according to the document
# Incorrect usage means the unsuccessful queries that were mandatory according to the document


code_chars = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits + "_")

test_shortcode = random.sample(code_chars, 6)

CLIENT = RequestsClient()

SERVER_ADDRESS = "http://127.0.0.1:8000/"
URL_SHORTCODE = {"url": "https://www.example.com/", "shortcode": "".join(test_shortcode)}


class ShortCodeCreation(APITestCase):

    def test_correct(self):
        # Automatic shortcode
        response = CLIENT.post(SERVER_ADDRESS+"shorten/", data={"url": "https://www.example.com/"})
        json_resp = json.loads(response.text)
        assert response.status_code == 201, "Response code should be 201"
        assert json_resp['shortcode'] is not None, "Shortcode should be in response"

        # Manual shortcode
        response = CLIENT.post(SERVER_ADDRESS+"shorten/", data={"url": "https://www.example.com/",
                                                                "shortcode": URL_SHORTCODE['shortcode']})
        json_resp = json.loads(response.text)
        assert response.status_code == 201, "Response code should be 201"
        assert json_resp['shortcode'] is not None, "Shortcode should be in response"

        print("All shortening related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        # We only check for status codes because they are explicitly declared with the error msg
        # Only after correct testing!

        response = CLIENT.post(SERVER_ADDRESS+"shorten/", data={"url": "https://www.example.com/", "shortcode": "ß!a123"})
        assert response.status_code == 412, "Response code should be 412"
        response = CLIENT.post(SERVER_ADDRESS+"shorten/", data={"url": "", "shortcode": "ß$a123"})
        assert response.status_code == 400, "Response code should be 400"

        response = CLIENT.post(SERVER_ADDRESS + "shorten/", data={"url": "https://www.example.com/",
                                                                  "shortcode": URL_SHORTCODE['shortcode']})
        response = CLIENT.post(SERVER_ADDRESS + "shorten/", data={"url": "https://www.example.com/",
                                                                "shortcode": URL_SHORTCODE['shortcode']})
        assert response.status_code == 409, "Response code should be 409"

        print("All shortening related tests passed regarding incorrect cases!")
        return True

class ShortCodeTest(APITestCase):

    def test_correct(self):
        response = CLIENT.post(SERVER_ADDRESS + "shorten/", data={"url": "https://www.example.com/",
                                                                  "shortcode": URL_SHORTCODE['shortcode']})
        response = CLIENT.get(SERVER_ADDRESS + URL_SHORTCODE['shortcode']+"/", allow_redirects=False)
        assert response.status_code == 302, "Response code should be 302"
        print("All shortcode redirect related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        response = CLIENT.get(SERVER_ADDRESS + 'asdasjdsjd/', allow_redirects=False)  # Redirects disabled
        assert response.status_code == 404, "Response code should be 404"
        print("All shortcode redirect related tests passed regarding incorrect cases!")
        return True


class StatTest(APITestCase):

    def test_correct(self):
        response = CLIENT.post(SERVER_ADDRESS + "shorten/", data={"url": "https://www.example.com/",
                                                                  "shortcode": URL_SHORTCODE['shortcode']})
        response = CLIENT.get(SERVER_ADDRESS + URL_SHORTCODE['shortcode'] + "/stats/")
        json_resp = json.loads(response.text)
        assert response.status_code == 200, "Response code should be 200"
        assert json_resp['created'] is not None, "Created should not be none!"
        assert json_resp['lastRedirect'] is not None, "lastRedirect should not be none!"
        assert json_resp['redirectCount'] is not None, "redirectCount should not be none!"
        print("All shortcode redirect related tests passed regarding correct cases!")
        return True

    def test_incorrect(self):
        response = CLIENT.get(SERVER_ADDRESS + "asdasdasd" + "/stats/")
        assert response.status_code == 404, "Response code should be 404"
        print("All shortcode redirect related tests passed regarding incorrect cases!")
        return True
