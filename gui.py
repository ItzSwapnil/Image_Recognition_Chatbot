import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import app
import threading

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conversational AI with Image Recognition")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3F4F")

        self.image_path = tk.StringVar()
        self.query = tk.StringVar()
        self.response = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Image Path Frame
        image_frame = tk.Frame(self.root, bg="#2E3F4F")
        image_frame.pack(pady=10)

        image_label = tk.Label(image_frame, text="Image Path:", bg="#2E3F4F", fg="#FFFFFF")
        image_label.pack(side=tk.LEFT, padx=10)

        image_entry = tk.Entry(image_frame, textvariable=self.image_path, width=50)
        image_entry.pack(side=tk.LEFT, padx=10)

        browse_button = tk.Button(image_frame, text="Browse", command=self.browse_image, bg="#4E5D6C", fg="#FFFFFF")
        browse_button.pack(side=tk.LEFT, padx=10)

        # Query Frame
        query_frame = tk.Frame(self.root, bg="#2E3F4F")
        query_frame.pack(pady=10)

        query_label = tk.Label(query_frame, text="Query:", bg="#2E3F4F", fg="#FFFFFF")
        query_label.pack(side=tk.LEFT, padx=10)

        query_entry = tk.Entry(query_frame, textvariable=self.query, width=60)
        query_entry.pack(side=tk.LEFT, padx=10)

        send_button = tk.Button(query_frame, text="Send", command=self.send_query, bg="#4E5D6C", fg="#FFFFFF")
        send_button.pack(side=tk.LEFT, padx=10)

        # Response Frame
        response_frame = tk.Frame(self.root, bg="#2E3F4F")
        response_frame.pack(pady=10)

        response_label = tk.Label(response_frame, text="Response:", bg="#2E3F4F", fg="#FFFFFF")
        response_label.pack(side=tk.LEFT, padx=10)

        self.response_text = tk.Text(response_frame, width=60, height=10)
        self.response_text.pack(side=tk.LEFT, padx=10)

        # Image Display Frame
        image_display_frame = tk.Frame(self.root, bg="#2E3F4F")
        image_display_frame.pack(pady=10)

        self.image_label = tk.Label(image_display_frame, text="No Image Selected", bg="#2E3F4F", fg="#FFFFFF")
        self.image_label.pack(side=tk.LEFT, padx=10)

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        self.image_path.set(path)
        self.display_image(path)

    def display_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img
        except Exception as e:
            print(e)

    def send_query(self):
        image_path = self.image_path.get()
        query = self.query.get()
        if image_path and query:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, "Processing...")
            threading.Thread(target=self.process_query, args=(image_path, query)).start()
        else:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, "Please select an image and enter a query.")

    def process_query(self, image_path, query):
        response = app.chat_with_image(image_path, query)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
