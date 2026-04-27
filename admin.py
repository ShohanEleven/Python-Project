#name : Md Mehedi Hassan Shohan
#Student ID : 10705819


import json
import textwrap

DATA_FILE = "data.txt"
MAX_SETUP_LEN = 50


def input_int(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            n = int(user_input)
            if n >= 1:
                return n
        print("Please enter an integer value of 1 or more.")


def input_something(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input != "":
            return user_input
        print("Input cannot be empty.")


def save_data(data_list):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data_list, f)
    except Exception as e:
        print("Error saving data:", e)


def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data_list = json.load(f)
        if not isinstance(data_list, list):
            print("Data format error, starting with empty list.")
            return []
        return data_list
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def shorten_setup(text):
    return textwrap.shorten(text, width=MAX_SETUP_LEN, placeholder="...")


def show_joke(joke, index):

    setup_short = shorten_setup(joke["setup"])
    return f"{index}. {setup_short}"


def show_joke_full(joke):
    s = joke["setup"]
    p = joke["punchline"]
    s_lines = [s]
    if joke["laughs"] >= 10:
        s_lines.append("That's hilarious!")
    if joke["groans"] >= 10:
        s_lines.append("Groan... groan... groan..")
    punch_line = '\n'.join(s_lines) + '\n' + p
    return punch_line


def add_joke(data):
    print("Add a new joke")
    setup = input_something("Enter joke setup: ")
    punchline = input_something("Enter joke punchline: ")
    data.append({"setup": setup, "punchline": punchline, "laughs": 0, "groans": 0})
    save_data(data)
    print("Joke added successfully!")


def list_jokes(data):
    if len(data) == 0:
        print("No jokes saved.")
        return
    print("Joke List:")
    for i, joke in enumerate(data, 1):
        print(show_joke(joke, i))


def search_jokes(data, keyword):
    results = []
    keyword_lower = keyword.lower()
    for i, joke in enumerate(data, 1):
        if keyword_lower in joke["setup"].lower() or keyword_lower in joke["punchline"].lower():
            results.append((i, joke))
    return results


def view_joke(data, index):
    if index < 1 or index > len(data):
        print("Invalid joke index.")
        return
    joke = data[index - 1]
    full_text = show_joke_full(joke)
    print(full_text)
    print(f"Ratings: Laughs={joke['laughs']} Groans={joke['groans']}")


def delete_joke(data, index):
    if index < 1 or index > len(data):
        print("Invalid joke index.")
        return
    removed = data.pop(index - 1)
    save_data(data)
    print(f"Deleted joke: {shorten_setup(removed['setup'])}")


def top_joke(data):
    if len(data) == 0:
        print("No jokes saved.")
        return
    most_laughs = max(data, key=lambda x: x["laughs"])
    most_groans = max(data, key=lambda x: x["groans"])
    print("Top Jokes:")
    print(f"Most laughs: {shorten_setup(most_laughs['setup'])} ({most_laughs['laughs']} laughs)")
    print(f"Most groans: {shorten_setup(most_groans['setup'])} ({most_groans['groans']} groans)")


def main():
    data = load_data()
    print("Welcome to the Joke Catalogue!")
    while True:
        print("\nCommands:")
        print("a - Add joke")
        print("l - List jokes")
        print("s - Search jokes")
        print("v - View joke")
        print("d - Delete joke")
        print("t - Show top jokes")
        print("q - Quit")
        command = input("Enter command: ").strip()

        if command == "":
            continue

        cmd = command[0].lower()
        arg = command[1:].strip()

        if cmd == 'a':
            add_joke(data)
        elif cmd == 'l':
            list_jokes(data)
        elif cmd == 's':
            if arg == "":
                arg = input_something("Enter search keyword: ")
            results = search_jokes(data, arg)
            if len(results) == 0:
                print("No results found.")
            else:
                print(f"Search results for '{arg}':")
                for i, joke in results:
                    print(show_joke(joke, i))
        elif cmd == 'v':
            if arg == "":
                arg = input_something("Enter joke index to view: ")
            if arg.isdigit():
                view_joke(data, int(arg))
            else:
                print("Invalid index.")
        elif cmd == 'd':
            if arg == "":
                arg = input_something("Enter joke index to delete: ")
            if arg.isdigit():
                delete_joke(data, int(arg))
            else:
                print("Invalid index.")
        elif cmd == 't':
            top_joke(data)
        elif cmd == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
