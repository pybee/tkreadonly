import unittest

from tkreadonly import normalize_sequence


class SequenceNormalization(unittest.TestCase):

    def test_button(self):
        "Button sequence names can be normalized"
        self.assertEqual(normalize_sequence('<1>'), '<Button-1>')
        self.assertEqual(normalize_sequence('<Button-1>'), '<Button-1>')
        self.assertEqual(normalize_sequence('<ButtonPress-1>'), '<Button-1>')

        self.assertEqual(normalize_sequence('<2>'), '<Button-2>')
        self.assertEqual(normalize_sequence('<Button-2>'), '<Button-2>')
        self.assertEqual(normalize_sequence('<ButtonPress-2>'), '<Button-2>')

        self.assertEqual(normalize_sequence('<5>'), '<Button-5>')
        self.assertEqual(normalize_sequence('<Button-5>'), '<Button-5>')
        self.assertEqual(normalize_sequence('<ButtonPress-5>'), '<Button-5>')

    def test_modified_button(self):
        "Keyboard-modified button sequences can be normalized"
        self.assertEqual(normalize_sequence('<Alt-1>'), '<Alt-Button-1>')
        self.assertEqual(normalize_sequence('<Alt-Button-1>'), '<Alt-Button-1>')
        self.assertEqual(normalize_sequence('<Alt-ButtonPress-1>'), '<Alt-Button-1>')
        self.assertEqual(normalize_sequence('<Alt-Control-1>'), '<Alt-Control-Button-1>')
        self.assertEqual(normalize_sequence('<Alt-Control-Shift-1>'), '<Alt-Control-Shift-Button-1>')

    def test_modifier_order(self):
        "Modifiers are normalized to alphabetical order"
        self.assertEqual(normalize_sequence('<Alt-Shift-1>'), '<Alt-Shift-Button-1>')
        self.assertEqual(normalize_sequence('<Shift-Alt-1>'), '<Alt-Shift-Button-1>')
        self.assertEqual(normalize_sequence('<Shift-Control-1>'), '<Control-Shift-Button-1>')

        self.assertEqual(normalize_sequence('<Control-Shift-Alt-1>'), '<Alt-Control-Shift-Button-1>')
        self.assertEqual(normalize_sequence('<Control-Alt-Shift-1>'), '<Alt-Control-Shift-Button-1>')
        self.assertEqual(normalize_sequence('<Shift-Control-Alt-1>'), '<Alt-Control-Shift-Button-1>')

    def test_double(self):
        "Double click sequences can be normalized"
        self.assertEqual(normalize_sequence('<Double-1>'), '<Double-1>')
        self.assertEqual(normalize_sequence('<Double-2>'), '<Double-2>')
        self.assertEqual(normalize_sequence('<Double-5>'), '<Double-5>')

    def test_modified_double(self):
        "Keyboard-modified double click sequences can be normalized"
        self.assertEqual(normalize_sequence('<Alt-Double-1>'), '<Alt-Double-1>')
        self.assertEqual(normalize_sequence('<Alt-Control-Double-1>'), '<Alt-Control-Double-1>')
        self.assertEqual(normalize_sequence('<Alt-Control-Shift-Double-1>'), '<Alt-Control-Shift-Double-1>')
        self.assertEqual(normalize_sequence('<Alt-Shift-Double-1>'), '<Alt-Shift-Double-1>')
        self.assertEqual(normalize_sequence('<Control-Double-1>'), '<Control-Double-1>')
        self.assertEqual(normalize_sequence('<Control-Shift-Double-1>'), '<Control-Shift-Double-1>')
        self.assertEqual(normalize_sequence('<Shift-Double-1>'), '<Shift-Double-1>')
