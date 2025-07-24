import os
from dotenv import load_dotenv

# --- IMPORTANT ---
# Load environment variables FIRST, before any other imports that need them.
load_dotenv()

# Now import the rest of the libraries
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import core_logic # This can now be safely imported

# Check for the key after loading it
if not os.getenv("GOOGLE_API_KEY"):
    messagebox.showerror("API Key Error", "GOOGLE_API_KEY not found in .env file. Please create it and restart the application.")
    exit()

def run_scan_thread(text_widget, button_widget):
    """Function to run the scan in a separate thread to keep the GUI responsive."""
    try:
        button_widget.config(state=tk.DISABLED, text="Scanning...")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Step 1: Gathering system data...\n\n")

        system_data = core_logic.gather_and_save_system_data()
        text_widget.insert(tk.END, "Step 2: System data gathered. Sending to AI for analysis...\n\n")
        
        report = core_logic.analyze_with_llm(system_data)

        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "--- AI Security Analysis Complete ---\n\n" + report)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"An error occurred. Please check the console.\n{e}")
    finally:
        button_widget.config(state=tk.NORMAL, text="Start Scan")

def main():
    """Main function to create and run the Tkinter GUI."""
    root = tk.Tk()
    root.title("AI Keylogger Detector")
    root.geometry("800x600")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    scan_button = tk.Button(frame, text="Start Scan", font=("Helvetica", 12, "bold"), command=lambda: threading.Thread(target=run_scan_thread, args=(results_text, scan_button), daemon=True).start())
    scan_button.pack(pady=10)

    results_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier New", 10))
    results_text.pack(fill=tk.BOTH, expand=True)
    results_text.insert(tk.END, "Click 'Start Scan' to begin the analysis.")

    root.mainloop()

if __name__ == "__main__":
    main()