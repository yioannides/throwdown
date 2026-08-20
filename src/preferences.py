from gi.repository import Adw, Gio, Gtk

@Gtk.Template(resource_path="/io/github/yioannides/Throwdown/preferences.ui")
class PreferencesDialog(Adw.PreferencesDialog):
    __gtype_name__ = 'PreferencesDialog'

    spin_360 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new("io.github.yioannides.Throwdown")

        self.settings.bind(
            "enable-360-spins",
            self.spin_360,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )
