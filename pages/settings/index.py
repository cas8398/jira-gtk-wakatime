import gi
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class SettingsPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Creating a TreeView to display data
        self.treeview = Gtk.TreeView()
        self.liststore = Gtk.ListStore(str, str)
        self.treeview.set_model(self.liststore)

        # Creating columns for the TreeView
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)  # Make the cell renderer editable
        renderer_text.connect("edited", self.on_value_edited)  # Connect edited signal
        renderer_text.set_property("wrap-mode", Gtk.WrapMode.WORD)
        renderer_text.set_property("wrap-width", 280)
        column1 = Gtk.TreeViewColumn("Key", renderer_text, text=0)
        column2 = Gtk.TreeViewColumn(
            "Value", renderer_text, text=1
        )  # Use the same renderer for both columns
        self.treeview.append_column(column1)
        self.treeview.append_column(column2)

        self.pack_start(self.treeview, True, True, 0)

        label = Gtk.Label()
        label.set_markup(
            "<small>Built with love ❤️ by <a href='https://github.com/cas8398'>@cas8398</a></small> | version : 0.1.2"
        )
        self.pack_start(label, False, False, 0)

        github_link = Gtk.LinkButton.new_with_label(
            "https://github.com/cas8398/jira-gtk-wakatime",
            "Write Issue or 🌟 Give Star on Github",
        )
        self.pack_start(github_link, False, False, 5)

        # Load data from JSON
        self.load_data_from_json("pages/jira/json/setting.json")

    def load_data_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    for key, value in item.items():
                        self.liststore.append([key, str(value)])
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

    def save_data_to_json(self, filename):
        data = []
        for row in self.liststore:
            data.append({row[0]: row[1]})
        with open(filename, "w") as file:
            json.dump(data, file)

    def on_value_edited(self, renderer, path, new_text):
        self.liststore[path][1] = new_text  # Update the value in the liststore
        self.save_data_to_json("pages/jira/json/setting.json")
