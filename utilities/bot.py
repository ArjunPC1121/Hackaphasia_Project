import tkinter as tk
import requests


# API URL to fetch jokes or facts
api_url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"


def show_fact():
    """
    Fetch a joke from the API and display it in a Tkinter window.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        fact = data.get('joke', "Could not retrieve a fact.")
    except requests.RequestException as e:
        fact = f"Error retrieving fact: {e}"

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Daily Fact")

    # Create a label with the fact
    label = tk.Label(window, text=fact, font=("Arial", 16), padx=20, pady=20, wraplength=400, justify="center")
    label.pack()

    # Button to close the pop-up
    button = tk.Button(window, text="Close", command=window.destroy)
    button.pack(pady=10)

    # Display the window
    window.mainloop()


def schedule_daily_fact(window):
    """
    Schedule the fact display function to run every 24 hours.
    """
    show_fact()
    # Schedule the next run after 24 hours (86400000 ms)
    window.after(60000, schedule_daily_fact, window)


def start_gui():
    """
    Initialize the main Tkinter window and start scheduling.
    """
    window = tk.Tk()
    window.title("Fact Generator")

    # Start the scheduling function
    schedule_daily_fact(window)

    # Start the Tkinter event loop
    window.mainloop()


