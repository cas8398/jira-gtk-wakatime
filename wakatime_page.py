import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class WakatimePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        label = Gtk.Label()
        label.set_markup("<big>Wakatime</big>")
        self.pack_start(label, False, False, 5)  # Change the packing options here
