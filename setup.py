import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pages.jira.index import JiraPage
from pages.wakatime.index import WakatimePage
from pages.settings.index import SettingsPage


class StackWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Jira GTK Wakatime")
        # Set the icon for the application
        self.set_icon_from_file("assets/logo.png")
        self.set_border_width(10)
        self.set_default_size(300, 300)

        # Creating a box vertically oriented with a space of 100 pixel.
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.add(vbox)

        # Creating stack, transition type, and transition duration.
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        # Add Todoist page to the stack
        todoist_page = JiraPage()
        stack.add_titled(todoist_page, "jira", "Jira Task")

        # Add Wakatime page to the stack
        wakatime_page = WakatimePage()
        stack.add_titled(wakatime_page, "wakatime", "Wakatime")

        # Add Wakatime page to the stack
        setting_page = SettingsPage()
        stack.add_titled(setting_page, "setting", "Settings")

        # Implementation of stack switcher.
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(stack, True, True, 0)


win = StackWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
