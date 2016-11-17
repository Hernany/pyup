# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from unittest import TestCase
from pyup.config import Config, RequirementConfig, CompileConfig


class ConfigTestCase(TestCase):

    def test_repr(self):
        config = Config()
        self.assertEqual(config.__repr__(), str(config.__dict__))

    def test_defaults(self):
        config = Config()
        self.assertEqual(config.close_prs, True)
        self.assertEqual(config.branch, "master")
        self.assertEqual(config.pin, True)
        self.assertEqual(config.search, True)
        self.assertEqual(config.requirements, [])
        self.assertEqual(config.schedule, "")
        self.assertEqual(config.assignees, [])
        self.assertEqual(config.update, "all")

    def test_can_pin(self):
        config = Config()
        config.requirements = [
            RequirementConfig(path="foo.txt", pin=False)
        ]

        self.assertEqual(config.can_pin("foo.txt"), False)

        config.pin = False
        config.requirements[0].pin = True

        self.assertEqual(config.can_pin("foo.txt"), True)

        self.assertEqual(config.can_pin("other.txt"), False)

    def test_can_update_all(self):
        config = Config()
        config.requirements = [
            RequirementConfig(path="foo.txt", update="insecure")
        ]

        self.assertEqual(config.can_update_all("foo.txt"), False)

        config.update = "insecure"
        config.requirements[0].update = "all"

        self.assertEqual(config.can_update_all("foo.txt"), True)

        self.assertEqual(config.can_update_all("other.txt"), False)

    def test_can_update_insecure(self):
        config = Config()
        config.requirements = [
            RequirementConfig(path="foo.txt", update=False)
        ]

        self.assertEqual(config.can_update_insecure("foo.txt"), False)

        config.update = False
        config.requirements[0].update = "insecure"

        self.assertEqual(config.can_update_insecure("foo.txt"), True)

        config.requirements[0].update = "all"

        self.assertEqual(config.can_update_insecure("foo.txt"), True)

        self.assertEqual(config.can_update_insecure("other.txt"), False)

    def test_update(self):
        update = {
            "branch": "some branch",
            "search": False,
            "requirements": [
                "foo.txt",
                {"bar.txt": {"pin": True, "compile": {"specs": ["baz.in", "foo.in"]}}}
            ]
        }
        config = Config()
        self.assertEqual(config.requirements, [])
        self.assertEqual(config.branch, "master")

        config.update_config(update)

        self.assertEqual(config.branch, "some branch")
        self.assertFalse(config.search)
        self.assertEqual(config.requirements[0].path, "foo.txt")
        self.assertEqual(config.requirements[1].path, "bar.txt")
        self.assertEqual(config.requirements[2].path, "baz.in")
        self.assertEqual(config.requirements[3].path, "foo.in")
        self.assertEqual(config.requirements[1].pin, True)
        self.assertEqual(config.requirements[1].compile.specs, ["baz.in", "foo.in"])

    def test_valid_schedule(self):
        config = Config()

        for sched in [
                "every day",
                "every week",
                "every week on monday",
                "every week on tuesday",
                "every week on wednesday",
                "every week on thursday",
                "every week on friday",
                "every week on saturday",
                "every week on sunday",
                "every two weeks",
                "every two weeks on monday",
                "every two weeks on monday",
                "every two weeks on tuesday",
                "every two weeks on wednesday",
                "every two weeks on thursday",
                "every two weeks on friday",
                "every two weeks on saturday",
                "every two weeks on sunday",
                "every month"]:
            config.schedule = sched
            self.assertTrue(config.is_valid_schedule())

        for sched in [
                "every day on monday",
                "every month on tuesday",
                "some other crap",
                "every bla",
                "foo"]:
            config.schedule = sched
            self.assertFalse(config.is_valid_schedule())

    def test_assignees(self):
        config = Config()
        self.assertEqual(config.assignees, [])

        config.update_config({"assignees": "jay"})
        self.assertEqual(config.assignees, ["jay"])

        config.update_config({"assignees": ["jay", "bla"]})
        self.assertEqual(config.assignees, ["jay", "bla"])


class RequirementConfigTestCase(TestCase):

    def test_repr(self):
        config = RequirementConfig(path="foo.txt")
        self.assertEqual(config.__repr__(), str(config.__dict__))


class CompileConfigTestCase(TestCase):

    def test_repr(self):
        config = CompileConfig()
        self.assertEqual(config.__repr__(), str(config.__dict__))

    def test_default(self):
        config = CompileConfig()
        self.assertEqual(config.specs, [])
