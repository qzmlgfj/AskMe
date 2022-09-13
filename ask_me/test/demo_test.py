import unittest

from ask_me import create_app
from ask_me import db

class DemoTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        with self.app_context:
            db.create_all()