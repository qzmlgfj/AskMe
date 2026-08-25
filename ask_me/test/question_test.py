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

        client = cls.app.test_client()
        # 注册管理员并登录换取 token，供管理接口使用
        ret = client.post("/api/auth/register", json={"username": "admin", "password": "pass"})
        if ret.get_json()["status"] != "ok":
            raise AssertionError("register admin failed")
        ret = client.post("/api/auth/login", json={"username": "admin", "password": "pass"})
        cls.token = ret.get_json().get("token")
        if not cls.token:
            raise AssertionError("login failed, no token returned")

    @classmethod
    def tearDownClass(cls):
        with cls.app_context:
            db.session.remove()

    def setUp(self):
        self.client = self.app.test_client()

    def _add_question(self, **extra):
        payload = {"title": "Hello", "content": "Hello World", "private": False}
        payload.update(extra)
        return self.client.post("/api/question/add", json=payload)

    def _get_token_header(self):
        return {"token": self.token}

    def test_add_question(self):
        ret = self._add_question()
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.get_json()["status"], "ok")

    def test_answer_question(self):
        id = self._add_question().get_json()["id"]

        self.client.post(
            "/api/question/answer",
            json={"id": id, "answer": "This is an answer"},
            headers=self._get_token_header(),
        )

        ret = self.client.get(f"/api/question/get_question/{id}")
        result = ret.get_json()[0]
        self.assertEqual(result["answer"], "This is an answer")
        self.assertTrue(result["answered"])
        # 未标注时 AI 参与位默认均为 False
        self.assertFalse(result["ai_question"])
        self.assertFalse(result["ai_answer"])

    def test_answer_empty_keeps_unanswered(self):
        id = self._add_question().get_json()["id"]

        self.client.post(
            "/api/question/answer",
            json={"id": id, "answer": "", "ai_answer": True},
            headers=self._get_token_header(),
        )

        result = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertFalse(result["answered"])
        self.assertFalse(result["ai_answer"])
        self.assertIsNone(result["answered_at"])

    def test_add_question_as_ai(self):
        ret = self._add_question(ai_question=True)
        id = ret.get_json()["id"]
        result = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertTrue(result["ai_question"])
        self.assertFalse(result["ai_answer"])

    def test_answer_as_ai(self):
        id = self._add_question().get_json()["id"]

        self.client.post(
            "/api/question/answer",
            json={"id": id, "answer": "AI 回答", "ai_answer": True},
            headers=self._get_token_header(),
        )

        result = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertTrue(result["ai_answer"])
        self.assertFalse(result["ai_question"])

    def test_edit_toggles_ai_flags(self):
        id = self._add_question(ai_question=True).get_json()["id"]

        self.client.post(
            "/api/question/edit",
            json={
                "id": id,
                "title": "Hello",
                "content": "Hello World",
                "private": False,
                "answer": "edited",
                "ai_question": False,
                "ai_answer": True,
            },
            headers=self._get_token_header(),
        )

        result = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertFalse(result["ai_question"])
        self.assertTrue(result["ai_answer"])

        # 清空回答时应同步清除 AI 回答标记
        self.client.post(
            "/api/question/edit",
            json={
                "id": id,
                "title": "Hello",
                "content": "Hello World",
                "private": False,
                "answer": "",
                "ai_question": True,
                "ai_answer": True,
            },
            headers=self._get_token_header(),
        )
        result = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertTrue(result["ai_question"])
        self.assertFalse(result["answered"])
        self.assertFalse(result["ai_answer"])
        self.assertIsNone(result["answered_at"])

    def test_export_includes_ai_flags(self):
        id = self._add_question(ai_question=True).get_json()["id"]
        self.client.post(
            "/api/question/answer",
            json={"id": id, "answer": "ans", "ai_answer": True},
            headers=self._get_token_header(),
        )

        exported = {q["id"]: q for q in self.client.get(
            "/api/question/export", headers=self._get_token_header()
        ).get_json()}
        self.assertTrue(exported[id]["ai_question"])
        self.assertTrue(exported[id]["ai_answer"])

    def test_export_import_roundtrip(self):
        id = self._add_question(ai_question=True).get_json()["id"]
        self.client.post(
            "/api/question/answer",
            json={"id": id, "answer": "ans", "ai_answer": True},
            headers=self._get_token_header(),
        )

        exported = self.client.get(
            "/api/question/export", headers=self._get_token_header()
        ).get_json()
        item = next(q for q in exported if q["id"] == id)

        # 时间必须带 UTC 时区信息，前端才能换算成本地时间
        self.assertTrue(item["created_at"].endswith("+00:00"))
        self.assertTrue(item["answered_at"].endswith("+00:00"))

        # 删除原记录后原样导入，验证时间与 AI 标注可完整还原
        self.client.post(
            "/api/question/delete", json={"id": id}, headers=self._get_token_header()
        )
        ret = self.client.post(
            "/api/question/import", json=exported, headers=self._get_token_header()
        )
        result = ret.get_json()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["result"]["failed"], [])

        restored = self.client.get(f"/api/question/get_question/{id}").get_json()[0]
        self.assertEqual(restored["created_at"], item["created_at"])
        self.assertEqual(restored["answered_at"], item["answered_at"])
        self.assertTrue(restored["ai_question"])
        self.assertTrue(restored["ai_answer"])

    def test_skill_md_served(self):
        for path in ("/SKILL.md", "/skill.md", "/SKILL.md/", "/skill.md/"):
            ret = self.client.get(path)
            self.assertEqual(ret.status_code, 200, f"{path} should be served")
            self.assertEqual(ret.mimetype, "text/markdown")
            self.assertIn(b"api/question/add", ret.data)

    def test_get_all_question(self):
        ret = self.client.get("/api/question/all", headers=self._get_token_header())
        self.assertEqual(ret.status_code, 200)
        questions = ret.get_json()
        self.assertIsInstance(questions, list)
        for question in questions:
            self.assertIn("ai_question", question)
            self.assertIn("ai_answer", question)

    def test_get_unanswered_question(self):
        ret = self.client.get("/api/question/unanswered", headers=self._get_token_header())
        self.assertEqual(ret.status_code, 200)
        questions = ret.get_json()
        self.assertIsInstance(questions, list)
        self.assertTrue(all(not question["answered"] for question in questions))
