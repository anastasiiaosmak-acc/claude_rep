import json
import os
import tempfile
import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_load_missing_store_is_empty(self):
        self.assertEqual(notes.load(self.path), [])

    def test_add_assigns_incrementing_ids(self):
        first = notes.add("write the rules", self.path)
        second = notes.add("wire the hooks", self.path)
        self.assertEqual((first["id"], second["id"]), (1, 2))
        self.assertEqual(len(notes.load(self.path)), 2)

    def test_add_rejects_blank_text(self):
        with self.assertRaises(ValueError):
            notes.add("   ", self.path)

    def test_done_marks_only_the_target(self):
        notes.add("one", self.path)
        notes.add("two", self.path)
        notes.done(1, self.path)
        stored = {n["id"]: n["done"] for n in notes.load(self.path)}
        self.assertEqual(stored, {1: True, 2: False})

    def test_done_unknown_id_raises(self):
        with self.assertRaises(KeyError):
            notes.done(42, self.path)

    def test_render_hides_done_unless_asked(self):
        notes.add("open", self.path)
        notes.add("closed", self.path)
        notes.done(2, self.path)
        rows = notes.load(self.path)
        self.assertNotIn("closed", notes.render(rows))
        self.assertIn("closed", notes.render(rows, show_all=True))

    def test_store_is_valid_json(self):
        notes.add("persisted", self.path)
        with open(self.path, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)[0]["text"], "persisted")


if __name__ == "__main__":
    unittest.main()
