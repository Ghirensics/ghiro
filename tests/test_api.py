# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import json
import os
from django.test import Client
from django.test import TestCase

from users.models import Profile
from analyses.models import Case, Analysis


class NewCaseTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.c = Client()

    def test_success_new_case_with_description(self):
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Case.objects.filter(name="test").exists())

    def test_success_new_case_no_description(self):
        response = self.c.post("/api/cases/new", {"name": "test2", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Case.objects.filter(name="test2").exists())

    def test_fail_auth_new_case_no_api(self):
        """Tests failed auth with no api key."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test"})
        self.assertEqual(response.status_code, 403)

    def test_fail_auth_new_case_wrong_api(self):
        """Tests failed auth with wrong api key."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": "aaaaa"})
        self.assertEqual(response.status_code, 403)

    def test_success_auth_new_case(self):
        """Tests success auth.."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)

class ShowCaseTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.c = Client()

    def test_fail_auth_show_case_no_api(self):
        """Tests failed auth with no api key."""
        response = self.c.post("/api/cases/show", {"case_id": 1})
        self.assertEqual(response.status_code, 403)

    def test_fail_auth_new_case_wrong_api(self):
        """Tests failed auth with wrong api key."""
        response = self.c.post("/api/cases/show", {"case_id": 1, "api_key": "aaaaa"})
        self.assertEqual(response.status_code, 403)

    def test_success_auth_show_case(self):
        """Tests success auth."""
        case = Case.objects.create(name="aaa", owner=self.user)
        anal = Analysis.objects.create(owner=self.user, case=case)
        response = self.c.post("/api/cases/show", {"case_id": case.id, "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["id"], case.id)
        self.assertEqual(response_data["images"][0], anal.id)

class NewImageTest(TestCase):
    def setUp(self):
        self.image = os.path.join("tests", "fixtures", "images", "1x1.png")
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.case = Case.objects.create(name="aaa", owner=self.user)
        self.c = Client()

    def test_success_new_image_no_case(self):
        """Uploads an image to any case."""
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd, "api_key": self.user.api_key})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(Analysis.objects.filter(file_name="1x1.png").exists())

    def test_success_new_image_to_case(self):
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd, "case_id": self.case.pk, "api_key": self.user.api_key})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(Analysis.objects.filter(file_name="1x1.png").exists())

    def test_fail_new_image_wrong_case(self):
        """Uploads an image to a case you have no permissions."""
        user = Profile.objects.create_user(username="test2", email="a@a.cp,", password="Test")
        case = Case.objects.create(name="bbb", owner=user)
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd, "case_id": case.pk, "api_key": self.user.api_key})
            self.assertEqual(response.status_code, 400)

    def test_fail_new_image_closed_case(self):
        """Uploads an image to a closed case."""
        case = Case.objects.create(name="ccc", owner=self.user, state="C")
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd, "case_id": case.pk, "api_key": self.user.api_key})
            self.assertEqual(response.status_code, 400)

    def test_fail_auth_wrong_key(self):
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd, "api_key": "aaa"})
            self.assertEqual(response.status_code, 403)

    def test_fail_auth_no_key(self):
        with open(self.image) as fd:
            response = self.c.post("/api/images/new", {"image": fd})
            self.assertEqual(response.status_code, 403)