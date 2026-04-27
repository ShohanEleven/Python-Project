#name : Md Mehedi Hassan Shohan
#Student ID : 10705819



import tkinter as tk
import tkinter.messagebox as msg
import json
import random

DATA_FILE = "data.txt"


class ProgramGUI:
    def __init__(self):
        self.data = self.load_data()
        if len(self.data) == 0:
            msg.showinfo("Info", "No jokes available.")
            exit()

        self.index = 0
        self.order = list(range(len(self.data)))
        random.shuffle(self.order)

        self.root = tk.Tk()
        self.root.title("Joke Catalogue")

        self.progress_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.progress_label.pack(pady=5)

        # Setup label (bold)
        self.setup_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), wraplength=400, justify="left")
        self.setup_label.pack(padx=10, pady=10)

        # Punchline label (normal)
        self.punchline_label = tk.Label(self.root, text="", font=("Arial", 12), wraplength=400, justify="left")
        self.punchline_label.pack(padx=10, pady=5)

        # Current Ratings label
        self.rating_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.rating_label.pack(pady=5)

        # Rating buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.laugh_button = tk.Button(button_frame, text="Laugh", width=10, command=lambda: self.rate_joke("laughs"))
        self.laugh_button.pack(side="left", padx=5)

        self.groan_button = tk.Button(button_frame, text="Groan", width=10, command=lambda: self.rate_joke("groans"))
        self.groan_button.pack(side="left", padx=5)

        self.abstain_button = tk.Button(button_frame, text="Abstain", width=10,
                                        command=lambda: self.rate_joke("abstain"))
        self.abstain_button.pack(side="left", padx=5)

        # Display first joke
        self.show_joke()

        self.root.mainloop()

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                msg.showerror("Error", "Corrupted data file format.")
                exit()
            # Add abstain count if not present
            for joke in data:
                if "abstain" not in joke:
                    joke["abstain"] = 0
            return data
        except:
            msg.showerror("Error", f"Cannot load data file {DATA_FILE}.")
            exit()

    def show_joke(self):
        current_joke = self.data[self.order[self.index]]
        current_pos = self.index + 1
        total = len(self.data)
        self.progress_label.config(text=f"Joke {current_pos} / {total}")
        self.setup_label.config(text=current_joke["setup"])
        self.punchline_label.config(text=current_joke["punchline"])
        self.rating_label.config(
            text=f"Laughs: {current_joke['laughs']}  Groans: {current_joke['groans']}  Abstains: {current_joke['abstain']}")

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.data, f)
        except Exception as e:
            msg.showerror("Error", f"Failed to save data:\n{str(e)}")

    def rate_joke(self, rating_type):
        idx = self.order[self.index]
        if rating_type == "laughs":
            self.data[idx]["laughs"] += 1
        elif rating_type == "groans":
            self.data[idx]["groans"] += 1
        elif rating_type == "abstain":
            self.data[idx]["abstain"] += 1
        self.save_data()
        self.index += 1
        if self.index >= len(self.data):
            msg.showinfo("Info", "No more jokes. Exiting...")
            self.root.destroy()
        else:
            self.show_joke()


if __name__ == "__main__":
    gui = ProgramGUI()
