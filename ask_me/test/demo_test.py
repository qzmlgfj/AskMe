import logging
import sys
import unittest

from ask_me import create_app, db

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class QuestionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(is_test=True)
        cls.app_context = cls.app.app_context()
        with cls.app_context:
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app_context:
            db.session.remove()
            db.drop_all()

    def test_add_question(self):
        self.app.test_client().post(
            "/api/question/add", json={"title": "Hello", "question": "Hello World"}
        )
        ret = self.app.test_client().get("/api/question/all")

        self.assertEqual(ret.get_json()[0]["title"], "Hello")
        self.assertEqual(ret.get_json()[0]["question"], "Hello World")

    def test_answer_question(self):
        ret = self.app.test_client().get("/api/question/all")
        id = ret.get_json()[0]["id"]

        self.app.test_client().post(
            "/api/question/answer", json={"id": id, "answer": "This is an answer"}
        )

        ret = self.app.test_client().get("/api/question/all")
        self.assertEqual(ret.get_json()[0]["answer"], "This is an answer")
