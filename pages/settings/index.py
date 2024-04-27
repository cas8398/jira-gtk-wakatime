import os
from gi.repository import Gtk
import shelve


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
            "<small>Built with love ❤️ by <a href='https://github.com/cas8398'>@cas8398</a> | version : 0.1.2 </small> "
        )
        self.pack_start(label, False, False, 0)

        github_link = Gtk.LinkButton.new_with_label(
            "https://github.com/cas8398/jira-gtk-wakatime",
            "Write Issue or 🌟 Give Star on Github",
        )
        self.pack_start(github_link, False, False, 5)

        # Initialize shelve database
        self.initialize_shelve_database()

        # load shelve database
        self.load_data_from_shelve()

    def load_data_from_shelve(self):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Initialize the shelve database file
        fix_path_save = os.path.join(home_dir, ".local", "share", "jira_settings_db")

        try:
            # Open the shelve database file
            with shelve.open(fix_path_save, writeback=True) as db:
                # Iterate over items in the database and add them to the liststore
                for key, value in db.items():
                    self.liststore.append([key, str(value)])
        except Exception as e:
            print(f"Error loading data from shelve database: {e}")

    def initialize_shelve_database(self):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Initialize the shelve database file path
        fix_path_save = os.path.join(home_dir, ".local", "share", "jira_settings_db")

        # Check if the database file already exists
        if not os.path.exists(fix_path_save):
            try:
                # Open the shelve database file
                with shelve.open(fix_path_save, writeback=True) as db:
                    # Set the values in the shelve database
                    db["accountId"] = "change_this"
                    db["id_done"] = "change_this"
                    db["default_desc"] = "change_this"
                    db["email"] = "change_this@gmail.com"
                    db["jira_url"] = "change_this.atlassian.net"
                    db["jira_token"] = "change_this"
            except Exception as e:
                print(f"Error initializing shelve database: {e}")
        else:
            print("Shelve database already exists. Skipping initialization.")

    def on_value_edited(self, renderer, path, new_text):
        # Update the value in the liststore
        self.liststore[path][1] = new_text

        # Get the key corresponding to the edited row
        key = self.liststore[path][0]

        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Initialize the shelve database file path
        fix_path_save = os.path.join(home_dir, ".local", "share", "jira_settings_db")

        try:
            # Open the shelve database file
            with shelve.open(fix_path_save, writeback=True) as db:
                # Update the value in the shelve database
                db[key] = new_text
        except Exception as e:
            print(f"Error updating shelve database: {e}")
