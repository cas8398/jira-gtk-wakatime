import subprocess
from gi.repository import Gtk, Gdk, Gio
import json
import sys
from notifypy import Notify

css_provider = Gtk.CssProvider()

css_data = """
#left-button:hover {
    background-color: #34c73e;
}
#center-button:hover {
    background-color: #8235db;
}
#right-button:hover {
    background-color: #4287f5;
}
"""

css_provider.load_from_data(css_data.encode())


class JiraPage(Gtk.Box):
    def __init__(self):
        # Initialize your class as before...
        self.selected_issues = {}
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        todoist_scrolled_window = Gtk.ScrolledWindow()
        todoist_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC
        )

        todoist_scrolled_window.set_max_content_height(700)

        # Set a large maximum height
        self.todoist_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        todoist_scrolled_window.add(self.todoist_box)
        self.pack_start(todoist_scrolled_window, True, True, 0)

        # Create left, center, and right buttons
        left_button = Gtk.Button(label="Finish Issue")
        center_button = Gtk.Button(label="Reload List")
        right_button = Gtk.Button(label="Start Podomoro")

        # apply CSS
        left_button.set_name("left-button")  # Add a name for the CSS selector
        center_button.set_name("center-button")  # Add a name for the CSS selector
        right_button.set_name("right-button")  # Add a name for the CSS selector

        left_button.connect("clicked", self.on_left_button_clicked)
        center_button.connect("clicked", self.on_center_button_clicked)
        right_button.connect("clicked", self.on_right_button_clicked)

        # Pack buttons into a horizontal box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.pack_start(left_button, False, False, 0)
        button_box.pack_start(center_button, False, False, 0)
        button_box.pack_end(right_button, False, False, 0)
        self.pack_start(button_box, False, False, 0)

        # Call API when window loads
        self.call_api()

        # Apply CSS styling
        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def call_api(self):
        # Load data from JSON file
        with open("jira_issues.json", "r") as f:
            issues = json.load(f)
        # Display the issues in the todoist_box
        for issue in issues:
            # Limit title to 20 characters
            truncated_title = (
                issue["title"][:75] + "..."
                if len(issue["title"]) > 75
                else issue["title"]
            )
            issue_check_button = Gtk.CheckButton(issue["id"] + " - " + truncated_title)
            issue_check_button.connect("toggled", self.on_check_button_toggled, issue)
            self.todoist_box.pack_start(issue_check_button, False, False, 0)

    def on_check_button_toggled(self, button, issue):
        if button.get_active():
            print(f"Issue {issue['id']} checked.")
            self.selected_issues[issue["id"]] = issue
        else:
            print(f"Issue {issue['id']} unchecked.")
            if issue["id"] in self.selected_issues:
                del self.selected_issues[issue["id"]]

    def on_left_button_clicked(self, widget):
        print("Finish Issue button clicked.")
        # print(self.selected_issues)

        # Display desktop notification
        notification = Notify()
        notification.title = "Cool Title"
        notification.message = "Even cooler message."
        notification.icon = "logo.png"
        notification.audio = "notif.wav"

        notification.send()

    def on_center_button_clicked(self, widget):
        print("Reload List button clicked.")
        subprocess.run([sys.executable, "jira_issue.py"])

    def on_right_button_clicked(self, widget):
        print("Start Podomoro button clicked.")
