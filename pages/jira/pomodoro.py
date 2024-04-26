import gi
from datetime import datetime, timedelta

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


class PomodoroDialog(Gtk.Dialog):
    def __init__(self, parent, project, customText):
        super().__init__(title="@" + project, transient_for=parent, flags=0)

        # Add custom buttons
        self.back_button = Gtk.Button(label="Cancel")
        self.start_button = Gtk.Button(label="Start")
        self.finish_button = Gtk.Button(label="Finish")
        self.stop_button = Gtk.Button(label="Stop")

        self.back_button.set_name("center-button")  # Add a name for the CSS selector
        self.start_button.set_name("right-button")  # Add a name for the CSS selector
        self.finish_button.set_name("left-button")  # Add a name for the CSS selector
        self.stop_button.set_name("center-button")  # Add a name for the CSS selector

        self.back_button.connect("clicked", self.on_back_button_clicked)
        self.start_button.connect("clicked", self.on_start_button_clicked)
        self.finish_button.connect("clicked", self.on_finish_button_clicked)
        self.stop_button.connect("clicked", self.on_stop_button_clicked)

        self.get_action_area().pack_start(self.back_button, True, True, 0)
        self.get_action_area().pack_start(self.start_button, True, True, 0)
        self.get_action_area().pack_start(self.finish_button, True, True, 0)
        self.get_action_area().pack_start(self.stop_button, True, True, 0)
        # Hide the finish and stop buttons initially
        self.finish_button.set_visible(False)
        self.stop_button.set_visible(False)

        self.set_default_size(200, 100)

        # Label Title
        self.title_label = Gtk.Label()
        self.title_label.set_markup(f"issue : {customText}")
        self.title_label.set_justify(Gtk.Justification.CENTER)
        self.title_label.set_line_wrap(True)
        self.title_label.set_max_width_chars(70)
        # Add padding to the left and right
        self.title_label.set_margin_top(3)
        self.title_label.set_margin_left(2)
        self.title_label.set_margin_right(2)

        # Create a label to display the stopwatch time
        self.timer_label = Gtk.Label()
        self.timer_label.set_markup(f"00:00")
        self.timer_label.set_hexpand(True)
        self.timer_label.set_vexpand(True)
        self.timer_label.set_name("large-font")  # Add a name for the CSS selector

        # Add the label to the content area
        box = self.get_content_area()
        box.add(self.title_label)
        box.add(self.timer_label)

        # Initialize the stopwatch
        self.elapsed_time = 0
        self.time_data = None  # Initialize a variable to store time data

        self.show_all()

        # Hide the finish and stop buttons initially
        self.finish_button.set_visible(False)
        self.stop_button.set_visible(False)

    def start_stopwatch(self):
        # Update the stopwatch label every second
        self.timeout_id = GObject.timeout_add(1000, self.update_stopwatch)

    def update_stopwatch(self):
        # Update the elapsed time
        self.elapsed_time += 1

        # Calculate minutes and seconds
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60

        # Update the stopwatch label
        self.timer_label.set_text(f"{minutes:02d}:{seconds:02d}")

        # Return True to continue the timeout
        return True

    def on_back_button_clicked(self, button):
        # Implement the function to be called when the "Back" button is clicked
        print("Back button clicked")
        # Close the dialog
        self.response(Gtk.ResponseType.CANCEL)

    def on_start_button_clicked(self, button):
        # Implement the function to be called when the "Start" button is clicked
        print("Start Podomoro")
        # Start the stopwatch
        self.start_stopwatch()

        # Hide the "Back" and "Start" buttons
        self.back_button.set_visible(False)
        self.start_button.set_visible(False)

        self.finish_button.set_visible(True)
        self.stop_button.set_visible(True)

    def on_finish_button_clicked(self, button):
        GObject.source_remove(self.timeout_id)
        # Implement the function to be called when the "Finish" button is clicked
        # Calculate elapsed time in hours, minutes, and seconds
        elapsed_hours = self.elapsed_time // 3600
        elapsed_minutes = (self.elapsed_time % 3600) // 60
        elapsed_seconds = self.elapsed_time % 60

        # Get the start and end date/time
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_date = (datetime.now() + timedelta(seconds=self.elapsed_time)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        TimeData = "\n".join(
            [
                f"Elapsed Time: {elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}",
                f"Start Date: {start_date}",
                f"End Date: {end_date}",
            ]
        )

        # Send TimeData as the response
        self.time_data = TimeData

        # Close the dialog with OK response
        self.response(Gtk.ResponseType.OK)

    def on_stop_button_clicked(self, button):
        # Implement the function to be called when the "Stop" button is clicked
        print("Stop Podomoro")
        GObject.source_remove(self.timeout_id)
        # Hide the "Finish" and "Stop" buttons
        self.finish_button.set_visible(False)
        self.stop_button.set_visible(False)
        self.back_button.set_visible(True)
        self.start_button.set_visible(True)
