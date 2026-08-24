# window.py
#
# Copyright 2026 yiannis ioannides
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gettext import gettext as _
from gi.repository import Adw, Gio, Gtk
from .randomizer import generate_trick


@Gtk.Template(resource_path="/io/github/yioannides/Throwdown/window.ui")
class ThrowdownWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ThrowdownWindow'

    main_stack = Gtk.Template.Child()
    trick_stack = Gtk.Template.Child()
    difficulty_button = Gtk.Template.Child()

    trick_a = Gtk.Template.Child()
    trick_b = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.difficulty = None
        self._current_trick_page = "a"

        self._add_action("easy", lambda *_: self.set_difficulty("easy"))
        self._add_action("medium", lambda *_: self.set_difficulty("medium"))
        self._add_action("hard", lambda *_: self.set_difficulty("hard"))
        self._add_action("pro", lambda *_: self.set_difficulty("pro"))
        self._add_action("random", lambda *_: self.set_difficulty("random"))
        self._add_action("next-trick", lambda *_: self.next_trick())

        self.trick_stack.set_visible_child_name("a")

    def _add_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

        labels = {
            "easy": _("Easy"),
            "medium": _("Medium"),
            "hard": _("Hard"),
            "pro": _("Pro"),
            "random": _("Random"),
        }

        self.difficulty_button.set_label(labels[difficulty])

        self.main_stack.set_visible_child_name("trick")

        self._current_trick_page = "a"
        self.trick_stack.set_visible_child_name("a")
        self.trick_a.set_label("")
        self.trick_b.set_label("")

        self.next_trick()

    def next_trick(self):
        if self.difficulty is None:
            return

        trick = generate_trick(self.difficulty)

        if self._current_trick_page == "a":
            self.trick_b.set_label(trick)
            self.trick_stack.set_visible_child_name("b")
            self._current_trick_page = "b"
        else:
            self.trick_a.set_label(trick)
            self.trick_stack.set_visible_child_name("a")
            self._current_trick_page = "a"
