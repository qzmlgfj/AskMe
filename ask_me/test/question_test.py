import logging
import sys
import unittest
import os

from ask_me import create_app, db

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class QuestionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists("instance/test.sqlite"):
            os.remove("instance/test.sqlite")

        cls.app = create_app(is_test=True)
        cls.app_context = cls.app.app_context()
        with cls.app_context:
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app_context:
            db.session.remove()

    def test_add_question(self):
        ret = self.app.test_client().post(
            "/api/question/add", json={"title": "Hello", "content": "Hello World", "private": False}
        )

        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.get_json()["status"], "ok")

    def test_answer_question(self):
        ret = self.app.test_client().get("/api/question/all")
        id = ret.get_json()[0]["id"]

        self.app.test_client().post(
            "/api/question/answer", json={"id": id, "answer": "This is an answer"}
        )

        ret = self.app.test_client().get("/api/question/all")
        self.assertEqual(ret.get_json()[0]["answer"], "This is an answer")

    def test_get_all_question(self):
        ret = self.app.test_client().get("/api/question/all")
        logger.debug(ret.get_json())

    def test_get_unanswered_question(self):
        ret = self.app.test_client().get("/api/question/unanswered")
        logger.debug(ret.get_json())
