import os
import unittest
from unittest.mock import patch, Mock
from scripts import publish_preflight


class PublishPreflightTests(unittest.TestCase):
    def test_only_reads_identity(self):
        response = Mock()
        response.json.return_value = {"sub": "example"}
        with patch.object(publish_preflight.platforms, "_linkedin_token", return_value="secret"), \
             patch.object(publish_preflight.platforms.requests, "get", return_value=response) as get, \
             patch.object(publish_preflight.platforms.requests, "post") as post:
            publish_preflight.check_linkedin()
        get.assert_called_once_with("https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": "Bearer secret"}, timeout=30)
        post.assert_not_called()

    def test_auth_error_stops_before_publishing(self):
        response = Mock()
        response.raise_for_status.side_effect = RuntimeError("sensitive provider body")
        with patch.object(publish_preflight.platforms, "_linkedin_token", return_value="secret"), \
             patch.object(publish_preflight.platforms.requests, "get", return_value=response):
            with self.assertRaises(SystemExit) as error:
                publish_preflight.main()
        self.assertNotIn("sensitive", str(error.exception))
        self.assertNotIn("secret", str(error.exception))

    def test_missing_subject_fails_closed(self):
        response = Mock()
        response.json.return_value = {}
        with patch.object(publish_preflight.platforms, "_linkedin_token", return_value="secret"), \
             patch.object(publish_preflight.platforms.requests, "get", return_value=response):
            with self.assertRaises(RuntimeError):
                publish_preflight.check_linkedin()

    def test_disabled_linkedin_does_not_contact_provider(self):
        with patch.dict(os.environ, {"LINKEDIN_POSTS_PER_DAY": "0"}), \
             patch.object(publish_preflight.platforms, "_linkedin_token") as token:
            publish_preflight.check_linkedin()
        token.assert_not_called()
