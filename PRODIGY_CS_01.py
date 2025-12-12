import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class CaesarCipherApp(tb.Window):
    def __init__(self):
        super().__init__(themename="cyborg") # Modern dark theme
        self.title("Caesar Cipher Pro")
        self.geometry("600x650")
        
        # Variables
        self.shift_var = tk.IntVar(value=3)
        self.mode_var = tk.StringVar(value="encrypt")
        
        # --- UI LAYOUT ---
        self.create_header()
        self.create_input_section()
        self.create_controls_section()
        self.create_output_section()
        self.create_footer()

        # Initial Trigger
        self.process_text()

    def create_header(self):
        """Top section with title"""
        header_frame = tb.Frame(self)
        header_frame.pack(fill=X, pady=20)
        
        title = tb.Label(
            header_frame, 
            text="🔒 CAESAR CIPHER", 
            font=("Helvetica", 20, "bold"),
            bootstyle="info"
        )
        title.pack()
        
        subtitle = tb.Label(
            header_frame,
            text="Real-time Encryption & Decryption Tool",
            font=("Helvetica", 10),
            bootstyle="secondary"
        )
        subtitle.pack()

    def create_input_section(self):
        """Input text area"""
        input_frame = tb.Labelframe(self, text=" Input Message ", padding=15, bootstyle="primary")
        input_frame.pack(fill=X, padx=20, pady=10)
        
        self.entry_text = tb.Text(
            input_frame, 
            height=3, 
            font=("Consolas", 11), 
            wrap="word",
            bd=0,
            highlightthickness=0
        )
        self.entry_text.pack(fill=X)
        self.entry_text.bind("<KeyRelease>", self.process_text)

    def create_controls_section(self):
        """Slider and Mode Toggle"""
        control_frame = tb.Frame(self, padding=10)
        control_frame.pack(fill=X, padx=20)

        # 1. Shift Control (Slider)
        shift_frame = tb.Labelframe(control_frame, text=" Shift Key ", padding=10, bootstyle="warning")
        shift_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Label to show current shift number
        self.shift_display = tb.Label(shift_frame, text="3", font=("Helvetica", 18, "bold"), bootstyle="warning")
        self.shift_display.pack(side=RIGHT, padx=10)

        # The Slider
        self.shift_scale = tb.Scale(
            shift_frame, 
            from_=0, 
            to=25, 
            variable=self.shift_var, 
            command=self.on_slider_move,
            bootstyle="warning"
        )
        self.shift_scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # 2. Mode Toggle (Encrypt/Decrypt)
        mode_frame = tb.Labelframe(control_frame, text=" Mode ", padding=10, bootstyle="success")
        mode_frame.pack(side=RIGHT, fill=BOTH)
        
        self.chk_mode = tb.Checkbutton(
            mode_frame, 
            text="Decrypt Mode", 
            variable=self.mode_var, 
            onvalue="decrypt", 
            offvalue="encrypt",
            bootstyle="success-round-toggle",
            command=self.process_text
        )
        self.chk_mode.pack(padx=10, pady=5)

    def create_output_section(self):
        """Result area"""
        output_frame = tb.Labelframe(self, text=" Result ", padding=15, bootstyle="info")
        output_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        self.output_text = tb.Text(
            output_frame, 
            height=4, 
            font=("Consolas", 12, "bold"), 
            wrap="word",
            state="disabled", # Read-only
            bg="#222",        # Slightly darker background
            fg="#00bc8c"      # Matrix green text
        )
        self.output_text.pack(fill=BOTH, expand=YES)

    def create_footer(self):
        """Action buttons"""
        btn_frame = tb.Frame(self, padding=20)
        btn_frame.pack(fill=X, side=BOTTOM)

        # Copy Button
        btn_copy = tb.Button(btn_frame, text="Copy Result", bootstyle="info-outline", command=self.copy_to_clipboard)
        btn_copy.pack(side=LEFT, fill=X, expand=YES, padx=5)

        # Brute Force Button
        btn_brute = tb.Button(btn_frame, text="Crack (Try All)", bootstyle="warning-outline", command=self.open_brute_force)
        btn_brute.pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        # Clear Button
        btn_clear = tb.Button(btn_frame, text="Reset", bootstyle="danger-outline", command=self.clear_all)
        btn_clear.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # --- LOGIC ---

    def caesar_logic(self, text, shift, mode):
        result = ""
        # Adjust shift for decryption
        if mode == "decrypt":
            shift = -shift

        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                # The math: (char_code - base + shift) % 26 + base
                new_char = chr((ord(char) - base + shift) % 26 + base)
                result += new_char
            else:
                result += char
        return result

    def on_slider_move(self, value):
        # Update the number label next to the slider
        val = int(float(value))
        self.shift_display.config(text=str(val))
        self.process_text()

    def process_text(self, event=None):
        text = self.entry_text.get("1.0", "end-1c")
        shift = self.shift_var.get()
        mode = self.mode_var.get()

        encrypted = self.caesar_logic(text, shift, mode)
        
        # Update Output (Must enable state to write, then disable again)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", encrypted)
        self.output_text.config(state="disabled")

    def copy_to_clipboard(self):
        result = self.output_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(result)
        
        # Visual feedback on the button
        current_text = self.create_footer
        # Simple flash effect is tricky in pure tk, so we just print to console or simple logic
        print("Copied to clipboard!")

    def clear_all(self):
        self.entry_text.delete("1.0", "end")
        self.shift_var.set(3)
        self.shift_display.config(text="3")
        self.process_text()

    def open_brute_force(self):
        # New Window
        bf_window = tb.Toplevel(self)
        bf_window.title("Brute Force Attack")
        bf_window.geometry("500x600")
        
        lbl = tb.Label(bf_window, text="Trying all 26 possible shifts...", font=("Helvetica", 12), bootstyle="warning")
        lbl.pack(pady=10)

        # Scrollable text area
        txt = tb.Text(bf_window, font=("Consolas", 10))
        txt.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        text_to_crack = self.entry_text.get("1.0", "end-1c")
        
        for s in range(26):
            # We use 'decrypt' logic here effectively by shifting BACKWARDS
            attempt = self.caesar_logic(text_to_crack, s, "decrypt")
            
            # Format: Shift # -> Result
            txt.insert("end", f"SHIFT -{s:<2} :  {attempt}\n")

if __name__ == "__main__":
    app = CaesarCipherApp()
    app.mainloop()
