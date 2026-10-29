import unittest
from unittest.mock import Mock, patch

import requests

from itunes_search import BASE_URL, search


class RequestTimeoutTests(unittest.TestCase):
    def setUp(self):
        self.session = Mock(spec=requests.Session)
        self.results = [{"trackName": "Planet Money"}]
        self.session.get.return_value.json.return_value = {"results": self.results}
        self.default_params = {
            "term": "planet money",
            "country": "US",
            "media": "all",
            "limit": 50,
            "lang": "en_us",
            "explicit": "Yes",
        }

    def test_omitted_timeout_preserves_defaults_and_results(self):
        self.assertIs(search("planet money", session=self.session), self.results)
        self.session.get.assert_called_once_with(BASE_URL, params=self.default_params, timeout=None)

    def test_explicit_timeouts_are_request_options(self):
        for timeout in (None, 10, 2.5, (3, 15), (None, 15), (3, None), (None, None)):
            with self.subTest(timeout=timeout):
                self.session.get.reset_mock()
                search("planet money", session=self.session, timeout=timeout)
                self.session.get.assert_called_once_with(BASE_URL, params=self.default_params, timeout=timeout)

    def test_all_api_parameters_are_forwarded(self):
        search(
            "economics",
            country="CA",
            media="podcast",
            entity="podcast",
            attribute="titleTerm",
            limit=5,
            lang="ja_jp",
            explicit="No",
            session=self.session,
            timeout=(2, 10),
        )
        self.session.get.assert_called_once_with(
            BASE_URL,
            params={
                "term": "economics",
                "country": "CA",
                "media": "podcast",
                "entity": "podcast",
                "attribute": "titleTerm",
                "limit": 5,
                "lang": "ja_jp",
                "explicit": "No",
            },
            timeout=(2, 10),
        )

    def test_none_api_parameters_remain_omitted(self):
        search("planet money", entity=None, attribute=None, session=self.session)
        self.session.get.assert_called_once_with(BASE_URL, params=self.default_params, timeout=None)

    def test_existing_positional_session_still_works(self):
        search("planet money", "US", "all", None, None, 50, "en_us", "Yes", self.session)
        self.session.get.assert_called_once_with(BASE_URL, params=self.default_params, timeout=None)

    def test_created_session_receives_timeout(self):
        with patch("itunes_search.requests.Session", return_value=self.session):
            search("planet money", timeout=5)
        self.session.get.assert_called_once_with(BASE_URL, params=self.default_params, timeout=5)

    def test_timeout_exception_propagates_unchanged(self):
        error = requests.exceptions.Timeout("read timed out")
        self.session.get.side_effect = error
        with self.assertRaises(requests.exceptions.Timeout) as raised:
            search("planet money", session=self.session, timeout=1)
        self.assertIs(raised.exception, error)


if __name__ == "__main__":
    unittest.main()
