from gi.repository import Gtk, Gdk
import json
from pages.jira.file_monitor import setup_file_monitor
from pages.jira.jira_assign import change_assign_status
from pages.jira.jira_issue import update_issues
from pages.jira.podomoro import PodomoroDialog

css_provider = Gtk.CssProvider()

css_data = """
#left-button:hover {
    background-color: #f78104;
}
#center-button:hover {
    background-color: #e05780;
}
#right-button:hover {
    background-color: #8ac926;
}
#large-font {
    font-size : 48px
} 
button:hover {
    background-color: #249ea0;  
}
"""

css_provider.load_from_data(css_data.encode())


class JiraPage(Gtk.Box):
    def __init__(self):
        # Initialize your class as before...
        self.selected_issues = {}
        setup_file_monitor(self.call_api)
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        jira_scrolled_window = Gtk.ScrolledWindow()
        jira_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        jira_scrolled_window.set_max_content_height(700)

        # Set a large maximum height
        self.jira_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        jira_scrolled_window.add(self.jira_box)
        self.pack_start(jira_scrolled_window, True, True, 0)

        # Create left, center, and right buttons
        left_button = Gtk.Button(label="Finish Issue")
        center_button = Gtk.Button(label="Reload List")
        right_button = Gtk.Button(label="Podomoro")

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

    def load_issues_from_file(self):
        # Load data from JSON file
        with open("pages/jira/json/jira_issues.json", "r") as f:
            self.issues = json.load(f)

    def call_api(self):
        print("Reloading list of issues...")

        # Reload JSON data from the file
        self.load_issues_from_file()

        # Clear existing widgets from jira_box
        for widget in self.jira_box.get_children():
            self.jira_box.remove(widget)

        # Display each issue in the jira_box
        for issue in self.issues:
            # Limit title to 20 characters
            truncated_title = (
                issue["title"][:35] + "..."
                if len(issue["title"]) > 35
                else issue["title"]
            )

            issue_check_button = Gtk.CheckButton(issue["id"] + " - " + truncated_title)
            issue_check_button.connect("toggled", self.on_check_button_toggled, issue)
            self.set_tooltip(issue_check_button, issue)
            self.jira_box.pack_start(issue_check_button, False, False, 0)

        # Redraw the UI
        self.show_all()

    # tooltips
    def set_tooltip(self, widget, issue):
        tooltip_texts = f"@{issue['project']} \n =>{issue['title']}"
        widget.set_tooltip_text(tooltip_texts)

    def on_check_button_toggled(self, button, issue):
        if button.get_active():
            print(f"Issue {issue['id']} checked.")
            self.selected_issues[issue["id"]] = issue
        else:
            print(f"Issue {issue['id']} unchecked.")
            if issue["id"] in self.selected_issues:
                del self.selected_issues[issue["id"]]

        # Convert the dictionary of selected issues to JSON-like structure and print it
        """
        print(
            "Selected issues:",
            json.dumps(list(self.selected_issues.values()), indent=2),
        )
        """

    def on_left_button_clicked(self, widget):
        listIssues = json.dumps(list(self.selected_issues.values()), indent=2)
        # Convert the JSON string back to Python objects
        issues_list = json.loads(listIssues)

        # Access the id of the first item in the list
        if issues_list:
            first_issue_id = issues_list[0]["id"]
            first_issue_title = issues_list[0]["title"]

            change_assign_status(first_issue_id, first_issue_title, "")

        else:
            print("No issues in the list")

            # alert
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.OTHER,
                buttons=Gtk.ButtonsType.OK,
                text="Select Issue First",
            )
            dialog.run()
            dialog.destroy()

    def on_center_button_clicked(self, widget):
        print("Reload List button clicked.")
        update_issues()

    def on_right_button_clicked(
        self,
        widget,
    ):
        listIssues = json.dumps(list(self.selected_issues.values()), indent=2)
        # Convert the JSON string back to Python objects
        issues_list = json.loads(listIssues)

        # Access the id of the first item in the list
        if issues_list:
            first_project_name = issues_list[0]["project"]
            first_issue_title = issues_list[0]["title"]
            first_issue_id = issues_list[0]["id"]

            dialog = PodomoroDialog(
                self.get_toplevel(),
                project=first_project_name,
                customText=first_issue_title,
            )
            dialog.parent = self.get_toplevel()
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                timeData = dialog.time_data
                change_assign_status(first_issue_id, first_issue_title, timeData)
                dialog.destroy()
            else:
                dialog.destroy()

        else:
            print("No issues in the list")

            # alert
            dialog = Gtk.MessageDialog(
                flags=0,
                message_type=Gtk.MessageType.OTHER,
                buttons=Gtk.ButtonsType.OK,
                text="Select Issue First",
            )
            dialog.run()
            dialog.destroy()
