import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class CaesarCipherApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Caesar Cipher Pro")
        self.geometry("600x650")
        
        # State Variables
        self.shift_var = tk.IntVar(value=3)
        self.mode_var = tk.StringVar(value="encrypt")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Builds the User Interface"""
        
        # --- Header ---
        header_frame = tb.Frame(self)
        header_frame.pack(fill=X, pady=20)
        tb.Label(header_frame, text="🛡️ Caesar Cipher Tool", 
                 font=("Segoe UI", 24, "bold"), bootstyle="info").pack()

        # --- Controls Area (Shift & Mode) ---
        controls_frame = tb.Labelframe(self, text="Configuration", padding=15)
        controls_frame.pack(fill=X, padx=20, pady=10)

        # Shift Slider
        shift_container = tb.Frame(controls_frame)
        shift_container.pack(fill=X, pady=5)
        
        tb.Label(shift_container, text="Shift Key:", font=("Segoe UI", 10)).pack(side=LEFT)
        self.shift_label = tb.Label(shift_container, text="3", font=("Segoe UI", 12, "bold"), width=3)
        self.shift_label.pack(side=RIGHT)
        
        self.shift_scale = tb.Scale(
            shift_container, 
            from_=0, 
            to=25, 
            variable=self.shift_var, 
            command=self.on_input_change,
            bootstyle="info"
        )
        self.shift_scale.pack(side=LEFT, fill=X, expand=True, padx=10)

        # Mode Toggle (Encrypt/Decrypt)
        mode_container = tb.Frame(controls_frame)
        mode_container.pack(fill=X, pady=10)
        
        tb.Label(mode_container, text="Mode:", font=("Segoe UI", 10)).pack(side=LEFT, padx=(0, 10))
        
        tb.Radiobutton(mode_container, text="Encrypt", variable=self.mode_var, 
                       value="encrypt", command=self.on_input_change, bootstyle="info-toolbutton").pack(side=LEFT, padx=5)
        tb.Radiobutton(mode_container, text="Decrypt", variable=self.mode_var, 
                       value="decrypt", command=self.on_input_change, bootstyle="secondary-toolbutton").pack(side=LEFT, padx=5)

        # --- Input Area ---
        input_frame = tb.Labelframe(self, text="Input Text", padding=15)
        input_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.input_text = tb.Text(input_frame, height=5, font=("Consolas", 11), wrap="word")
        self.input_text.pack(fill=BOTH, expand=True)
        self.input_text.bind("<KeyRelease>", self.on_input_change)

        # --- Output Area ---
        output_frame = tb.Labelframe(self, text="Result", padding=15)
        output_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.output_text = tb.Text(output_frame, height=5, font=("Consolas", 11), wrap="word", state="disabled")
        self.output_text.pack(fill=BOTH, expand=True)

        # --- Action Buttons ---
        btn_frame = tb.Frame(self, padding=20)
        btn_frame.pack(fill=X, side=BOTTOM)

        tb.Button(btn_frame, text="Try All Shifts (Brute Force)", 
                  bootstyle="outline-warning", command=self.open_brute_force).pack(side=LEFT)
        
        tb.Button(btn_frame, text="Clear", bootstyle="danger", command=self.clear_all).pack(side=RIGHT, padx=5)
        
        tb.Button(btn_frame, text="Copy Result", bootstyle="success", 
                  command=self.copy_to_clipboard).pack(side=RIGHT, padx=5)

    def logic_caesar(self, text, shift, mode):
        """Core cryptographic logic"""
        result = ""
        # Adjust shift for decryption
        if mode == "decrypt":
            shift = -shift

        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                # Python's modulo operator handles negative numbers correctly automatically
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result

    def on_input_change(self, *args):
        """Triggered on typing, sliding, or mode switching"""
        # Update shift label number
        current_shift = self.shift_var.get()
        self.shift_label.config(text=str(current_shift))

        # Get content
        text = self.input_text.get("1.0", "end-1c")
        mode = self.mode_var.get()

        # Process
        encrypted = self.logic_caesar(text, current_shift, mode)

        # Update Output (Must enable state to write, then disable to make read-only)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", encrypted)
        self.output_text.config(state="disabled")

    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(content)
        
        # Visual feedback (change button text briefly)
        original_text = "Copy Result"
        # Access the button in the bottom frame (a bit hacky, normally keep a reference)
        # But for this simple app, we'll just flash the border
        self.output_text.config(bootstyle="success") 
        self.after(500, lambda: self.output_text.config(bootstyle="default"))

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.on_input_change()

    def open_brute_force(self):
        """Opens a window showing all 26 possible shifts"""
        bf_window = tb.Toplevel(self)
        bf_window.title("Brute Force Analysis")
        bf_window.geometry("500x600")

        input_str = self.input_text.get("1.0", "end-1c")
        if not input_str.strip():
            tb.Label(bf_window, text="Please enter text in the main window first.", bootstyle="danger").pack(pady=20)
            return

        scrolly = tb.Scrollbar(bf_window, bootstyle="round")
        scrolly.pack(side=RIGHT, fill=Y)

        txt_display = tb.Text(bf_window, font=("Consolas", 10), yscrollcommand=scrolly.set)
        txt_display.pack(fill=BOTH, expand=True, padx=10, pady=10)
        scrolly.config(command=txt_display.yview)

        for s in range(26):
            # We always "decrypt" for brute force to find the hidden meaning
            attempt = self.logic_caesar(input_str, s, "decrypt")
            
            # Formatting: Bold the Shift number
            txt_display.insert("end", f"Shift -{s:<2}: ", "bold_tag")
            txt_display.insert("end", f"{attempt}\n\n")

        txt_display.tag_configure("bold_tag", foreground="#5bc0de", font=("Consolas", 10, "bold"))
        txt_display.config(state="disabled")

if __name__ == "__main__":
    app = CaesarCipherApp()
    app.mainloop()
