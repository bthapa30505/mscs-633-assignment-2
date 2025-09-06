#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
from datetime import datetime

class QRCodeGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("800x800")
        self.root.resizable(True, True)
        
        self.setup_styles()
        
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4,
        )
        
        self.current_qr_image = None
        self.current_url = ""
        
        self.create_widgets()
        
        self.url_entry.focus()
    
    def setup_styles(self):
        style = ttk.Style()
        
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'background': '#F5F5F5',
            'text': '#2C3E50'
        }
        
        self.root.configure(bg=self.colors['background'])
    
    def create_widgets(self):
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        title_label = tk.Label(
            main_frame, 
            text="QR Code Generator",
            font=("Arial", 18, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        url_frame = ttk.LabelFrame(main_frame, text="Enter URL", padding="15")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(
            url_frame, 
            textvariable=self.url_var,
            font=("Arial", 11),
            width=50
        )
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        self.url_entry.bind('<Return>', self.generate_qr_code)
        
        self.generate_btn = ttk.Button(
            url_frame,
            text="Generate QR",
            command=self.generate_qr_code
        )
        self.generate_btn.grid(row=0, column=2)
        
        self.fill_color_var = tk.StringVar(value="black")
        self.back_color_var = tk.StringVar(value="white")
        
        qr_frame = ttk.LabelFrame(main_frame, text="Generated QR Code", padding="15")
        qr_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        qr_frame.columnconfigure(0, weight=1)
        qr_frame.rowconfigure(0, weight=1)
        
        self.qr_canvas = tk.Canvas(
            qr_frame,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2,
            width=400,
            height=400
        )
        self.qr_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.show_placeholder()
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Enter a URL to generate QR code")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding="5"
        )
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def show_placeholder(self):
        self.qr_canvas.delete("all")
        canvas_width = self.qr_canvas.winfo_reqwidth()
        canvas_height = self.qr_canvas.winfo_reqheight()
        
        self.qr_canvas.create_text(
            canvas_width // 2, canvas_height // 2,
            text="Enter a URL above\nto generate QR code",
            font=("Arial", 14),
            fill="gray",
            justify=tk.CENTER
        )
    
    def validate_url(self, url):
        url = url.strip()
        if not url:
            return False, ""
        
        if not url.startswith(('http://', 'https://', 'ftp://', 'ftps://')):
            url = 'http://' + url
        
        if '.' not in url or len(url) < 7:
            return False, url
        
        return True, url
    
    def on_url_change(self, event=None):
        url = self.url_var.get().strip()
        if url:
            self.status_var.set(f"Ready to generate QR code for: {url[:50]}{'...' if len(url) > 50 else ''}")
        else:
            self.status_var.set("Ready - Enter a URL to generate QR code")
    
    def generate_qr_code(self, event=None):
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Input Required", "Please enter a URL")
            self.url_entry.focus()
            return
        
        is_valid, processed_url = self.validate_url(url)
        if not is_valid:
            messagebox.showerror("Invalid URL", "Please enter a valid URL")
            self.url_entry.focus()
            return
        
        try:
            self.status_var.set("Generating QR code...")
            self.root.update_idletasks()
            
            self.qr.clear()
            
            self.qr.add_data(processed_url)
            self.qr.make(fit=True)
            
            fill_color = self.fill_color_var.get()
            back_color = self.back_color_var.get()
            
            qr_img = self.qr.make_image(
                fill_color=fill_color,
                back_color=back_color
            )
            
            display_size = (350, 350)
            qr_img = qr_img.resize(display_size, Image.Resampling.NEAREST)
            
            self.current_qr_image = ImageTk.PhotoImage(qr_img)
            self.current_url = processed_url
            
            self.qr_canvas.delete("all")
            canvas_width = self.qr_canvas.winfo_width()
            canvas_height = self.qr_canvas.winfo_height()
            
            x = (canvas_width - display_size[0]) // 2
            y = (canvas_height - display_size[1]) // 2
            
            self.qr_canvas.create_image(
                x, y,
                anchor=tk.NW,
                image=self.current_qr_image
            )
            
            self.status_var.set(f"QR code generated for: {processed_url}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{str(e)}")
            self.status_var.set("Error generating QR code")


def main():
    try:
        root = tk.Tk()
        
        try:
            pass
        except:
            pass
        
        app = QRCodeGUI(root)
        
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()