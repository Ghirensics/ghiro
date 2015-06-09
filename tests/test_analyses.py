# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.test import TestCase

from users.models import Profile
from analyses.models import Case


class CaseModelTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.user2 = Profile.objects.create_user(username="test2", email="b@a.cp,", password="Test")

    def test_case_is_owner(self):
        case = Case.objects.create(name="aaa", owner=self.user)
        self.assertTrue(case.is_owner(self.user))
        self.assertFalse(case.is_owner(self.user2))