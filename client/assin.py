import tkinter as tk
from tkinter import scrolledtext
import requests
import json

class PharmacyChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Chatbot")

        # Create GUI components
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
        self.chat_area.grid(row=0, column=0, padx=10, pady=10)

        self.user_input = tk.Entry(root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "Pharmacy Bot: Hello! How can I assist you today?\n")
        self.chat_area.config(state='disabled')

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You", user_message)
            self.user_input.delete(0, tk.END)
            response = self.get_ollama_response(user_message)
            self.display_message("Pharmacy Bot", response)

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def get_ollama_response(self, user_message):
        try:
            # Send a POST request to the FastAPI server
            response = requests.post("http://127.0.0.1:8000/v1/ask", json={"message": user_message})
            response_data = response.json()

            # Return the response from the FastAPI server
            if "response" in response_data:
                return response_data["response"]
            else:
                return response_data.get("error", "Unknown error")

        except requests.RequestException as e:
            return f"Error: {e}"

# Create the GUI window
root = tk.Tk()
app = PharmacyChatbotApp(root)
root.mainloop()
