import unittest
from contextlib import ExitStack
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import requests

from itunes_search import BASE_URL, search


class SessionCleanupTests(unittest.TestCase):
    def test_success_preserves_results_parameters_and_session_ownership(self):
        for caller_owned in (False, True):
            with self.subTest(caller_owned=caller_owned):
                session = requests.Session()
                response = requests.Response()
                response.status_code = 200
                response._content = b'{"results": [{"trackName": "Planet Money"}]}'
                with ExitStack() as stack:
                    factory = stack.enter_context(patch("itunes_search.requests.Session", return_value=session))
                    send = stack.enter_context(patch.object(session, "send", return_value=response))
                    close = stack.enter_context(patch.object(session, "close", wraps=session.close))
                    result = search("planet money", session=session if caller_owned else None)
                    self.assertEqual(result, [{"trackName": "Planet Money"}])
                    self.assertEqual(close.call_count, 0 if caller_owned else 1)
                    self.assertEqual(factory.call_count, 0 if caller_owned else 1)
                    request = send.call_args.args[0]
                    self.assertEqual(request.url.split("?")[0], BASE_URL)
                    self.assertEqual(
                        parse_qs(urlparse(request.url).query),
                        {
                            "term": ["planet money"],
                            "country": ["US"],
                            "media": ["all"],
                            "limit": ["50"],
                            "lang": ["en_us"],
                            "explicit": ["Yes"],
                        },
                    )
                session.close()

    def test_failures_preserve_exceptions_and_session_ownership(self):
        for caller_owned in (False, True):
            for failure in ("transport", "http", "json"):
                with self.subTest(caller_owned=caller_owned, failure=failure):
                    session = requests.Session()
                    response = requests.Response()
                    response.status_code = 503 if failure == "http" else 200
                    response._content = b"invalid JSON" if failure == "json" else b'{"results": []}'
                    transport_error = requests.Timeout("request timed out")
                    expected_error = {
                        "transport": requests.Timeout,
                        "http": requests.HTTPError,
                        "json": requests.exceptions.JSONDecodeError,
                    }[failure]
                    with ExitStack() as stack:
                        stack.enter_context(patch("itunes_search.requests.Session", return_value=session))
                        stack.enter_context(
                            patch.object(
                                session,
                                "send",
                                return_value=response,
                                side_effect=transport_error if failure == "transport" else None,
                            )
                        )
                        close = stack.enter_context(patch.object(session, "close", wraps=session.close))
                        with self.assertRaises(expected_error) as raised:
                            search("planet money", session=session if caller_owned else None)
                        if failure == "transport":
                            self.assertIs(raised.exception, transport_error)
                        elif failure == "http":
                            self.assertIs(raised.exception.response, response)
                        self.assertEqual(close.call_count, 0 if caller_owned else 1)
                    session.close()


if __name__ == "__main__":
    unittest.main()
