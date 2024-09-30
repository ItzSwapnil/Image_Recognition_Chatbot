import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import app

root = tk.Tk()
root.title("Conversational AI with Image Recognition")
root.geometry("800x600")
root.configure(bg="#2E3F4F")

conversation_history = []

# Fonts and Colors
header_font = ("Arial", 16, "bold")
text_font = ("Arial", 12)
bg_color = "#2E3F4F"
fg_color = "#FFFFFF"
button_color = "#4E5D6C"


def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, file_path)
    display_image(file_path)


def display_image(file_path):
    try:
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.photo = img
    except Exception as e:
        print(e)


def send_message():
    global conversation_history
    query = query_entry.get()
    image_path = image_path_entry.get()
    response, conversation_history = app.chat_with_image(image_path, query, conversation_history)

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"User: {query}\n", "user")
    chat_box.insert(tk.END, f"AI: {response}\n\n", "ai")
    chat_box.config(state=tk.DISABLED)

    query_entry.delete(0, tk.END)


# Image Path Frame
image_frame = tk.Frame(root, bg=bg_color)
image_frame.pack(pady=10)

image_label = tk.Label(image_frame, text="No Image Selected", bg=bg_color, fg=fg_color)
image_label.pack(side=tk.LEFT, padx=10)

image_path_entry = tk.Entry(image_frame, width=50, font=text_font)
image_path_entry.pack(side=tk.LEFT, padx=10)

browse_button = tk.Button(image_frame, text="Browse", command=select_image, bg=button_color, fg=fg_color,
                          font=text_font)
browse_button.pack(side=tk.LEFT, padx=10)

# Query Frame
query_frame = tk.Frame(root, bg=bg_color)
query_frame.pack(pady=10)

query_label = tk.Label(query_frame, text="Your Query:", bg=bg_color, fg=fg_color, font=text_font)
query_label.pack(side=tk.LEFT, padx=10)

query_entry = tk.Entry(query_frame, width=60, font=text_font)
query_entry.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(query_frame, text="Send", command=send_message, bg=button_color, fg=fg_color, font=text_font)
send_button.pack(side=tk.LEFT, padx=10)

# Chat Box
chat_box_frame = tk.Frame(root)
chat_box_frame.pack(pady=20, fill=tk.BOTH, expand=True)

chat_box = scrolledtext.ScrolledText(chat_box_frame, wrap=tk.WORD, font=text_font, bg="#1E2A36", fg=fg_color)
chat_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
chat_box.tag_config("user", foreground="cyan")
chat_box.tag_config("ai", foreground="yellow")
chat_box.config(state=tk.DISABLED)

root.mainloop()