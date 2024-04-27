import os
import shelve
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Initialize the shelve database file
fix_path_save = os.path.join(home_dir, ".local", "share", "logs_db")


class WakatimePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Creating a ScrolledWindow to contain the TreeView
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_max_content_height(300)

        # Creating a TreeView to display data
        self.treeview = Gtk.TreeView()
        self.liststore = Gtk.ListStore(str, str)
        self.treeview.set_model(self.liststore)

        # Creating columns for the TreeView
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("wrap-mode", Gtk.WrapMode.WORD)
        renderer_text.set_property("wrap-width", 280)
        column1 = Gtk.TreeViewColumn("Datetime", renderer_text, text=0)
        column2 = Gtk.TreeViewColumn("Message", renderer_text, text=1)
        self.treeview.append_column(column1)
        self.treeview.append_column(column2)

        scrolled_window.add(self.treeview)
        self.pack_start(scrolled_window, True, True, 0)

        # Creating a button to reload Shelve data
        reload_button = Gtk.Button(label="Reload Logs")
        reload_button.connect("clicked", self.reload_shelve)
        self.pack_end(reload_button, False, False, 0)

        # Load data from Shelve
        self.load_data_from_shelve()

    def load_data_from_shelve(self):
        try:
            # Open the shelve database file
            with shelve.open(fix_path_save) as db:
                # Get the logs list from the database
                logs = db.get("logs", [])

                # Sort the logs in descending order based on datetime
                sorted_logs = sorted(logs, key=lambda x: x["datetime"], reverse=True)

                # Iterate over sorted logs
                for log in sorted_logs:
                    # Add each log entry to the liststore
                    self.liststore.append([log["datetime"], log["message"]])
        except Exception as e:
            print(f"Error loading data from Shelve: {e}")

    def reload_shelve(self, widget):
        # Clear existing data from the liststore
        self.liststore.clear()
        # Reload and display the Shelve data
        self.load_data_from_shelve()
