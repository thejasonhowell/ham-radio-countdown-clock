import tkinter as tk
from tkinter import simpledialog
import platform

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.duration = 600  # Default duration: 10 minutes
        self.remaining_time = self.duration
        self.running = False

        # Set up the window without transparency
        self.root.title("Ham Radio ID Countdown")  # Updated window title
        self.root.geometry("800x400")
        self.root.configure(bg="black")  # Set the background color to black
        self.root.attributes("-topmost", True)  # Keep the window on top

        # Configure the timer label
        self.timer_label = tk.Label(
            self.root,
            text=self.format_time(self.remaining_time),
            font=("Digital-7 Mono", 200, "bold"),
            fg="red",
            bg="black",
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            anchor='center'
        )
        self.timer_label.pack(expand=True, fill="both")  # Fill the window completely

        # Instruction label (optional)
        self.instruction_label = tk.Label(
            self.root,
            text="Press SPACE to start/reset\nRight-click to set time",
            font=("Helvetica", 12),
            fg="white",
            bg="black"
        )
        self.instruction_label.pack(side="bottom", pady=5)

        # Set focus to the root window
        self.root.focus_set()

        # Bind events
        self.bind_events()
        self.root.bind("<Configure>", self.resize_font)  # Adjust font on window resize

    def bind_events(self):
        # Ensure the root window has focus
        self.root.focus_set()

        # Bind spacebar event globally
        self.root.bind_all("<space>", self.handle_spacebar)

        # Bind right-click event to the timer label
        system = platform.system()
        if system == "Darwin":  # macOS compatibility
            # Support for Control-click and two-finger click
            self.timer_label.bind("<Button-2>", self.set_time)            # Middle-click
            self.timer_label.bind("<Button-3>", self.set_time)            # Right-click
            self.timer_label.bind("<Control-Button-1>", self.set_time)    # Control + Left-click
        else:
            self.timer_label.bind("<Button-3>", self.set_time)  # Right-click on Windows/Linux

        # Disable the default context menu by overriding the right-click event on the root window
        self.root.bind("<Button-3>", lambda e: "break")

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def handle_spacebar(self, event=None):
        if self.running:
            self.reset_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.running = True
        self.timer_label.config(fg="red")  # Reset to red when starting
        self.update_timer()

    def reset_timer(self):
        self.running = False
        self.remaining_time = self.duration
        self.timer_label.config(
            text=self.format_time(self.remaining_time), fg="red"
        )

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=self.format_time(self.remaining_time))
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.flash_red()

    def flash_red(self):
        if not self.running:
            return
        current_color = self.timer_label.cget("fg")
        next_color = "black" if current_color == "red" else "red"
        self.timer_label.config(fg=next_color)
        self.root.after(500, self.flash_red)

    def set_time(self, event=None):
        try:
            # Pause the timer while setting a new time
            was_running = self.running
            self.running = False

            # Temporarily disable the 'topmost' attribute
            self.root.attributes("-topmost", False)

            user_input = simpledialog.askinteger(
                "Set Timer",
                "Enter duration in minutes:",
                parent=self.root,
                minvalue=1,
                maxvalue=60
            )

            # Re-enable the 'topmost' attribute
            self.root.attributes("-topmost", True)

            if user_input is not None:
                self.duration = user_input * 60
                self.reset_timer()
                if was_running:
                    self.start_timer()
            else:
                # If the user cancels, resume the timer if it was running
                self.running = was_running
                if self.running:
                    self.update_timer()
        except Exception as e:
            print(f"Error in setting time: {e}")
        finally:
            # Ensure the focus returns to the root window
            self.root.focus_set()

    def resize_font(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        font_size = int(min(width / 2, height / 1.1))
        font_size = max(font_size, 10)
        self.timer_label.config(font=("Digital-7 Mono", font_size, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    timer = CountdownTimer(root)
    root.mainloop()