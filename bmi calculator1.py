import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BMI Calculator")

        self.label_name = tk.Label(self, text="Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        self.label_weight = tk.Label(self, text="Weight (kg):")
        self.label_weight.pack()
        self.entry_weight = tk.Entry(self)
        self.entry_weight.pack()

        self.label_height = tk.Label(self, text="Height (cm):")
        self.label_height.pack()
        self.entry_height = tk.Entry(self)
        self.entry_height.pack()

        self.button_calculate = tk.Button(self, text="Calculate BMI", command=self.calculate_bmi)
        self.button_calculate.pack()

        self.label_result = tk.Label(self, text="")
        self.label_result.pack()

        self.button_show_history = tk.Button(self, text="Show History", command=self.show_history)
        self.button_show_history.pack()

        self.listbox_history = tk.Listbox(self)
        self.listbox_history.pack()

        # Database connection
        self.conn = sqlite3.connect('bmi_data.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bmi (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            weight REAL,
                            height REAL,
                            bmi REAL,
                            date TEXT)''')
        self.conn.commit()

    def calculate_bmi(self):
        try:
            name = self.entry_name.get()
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            bmi = (weight / (height * height)) * 10000  # Convert height to meters

            self.label_result.config(text=f"BMI: {bmi:.2f}")

            # Store BMI data in the database
            self.store_bmi_data(name, weight, height, bmi)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid weight and height.")

    def store_bmi_data(self, name, weight, height, bmi):
        cursor = self.conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO bmi (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                       (name, weight, height, bmi, date))
        self.conn.commit()

    def show_history(self):
        name = self.entry_name.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT weight, height, bmi, date FROM bmi WHERE name=?", (name,))
        data = cursor.fetchall()

        if data:
            self.display_history(data)
        else:
            messagebox.showinfo("Info", "No data found for this user.")

    def display_history(self, data):
        self.listbox_history.delete(0, tk.END)
        for row in data:
            self.listbox_history.insert(tk.END, f"Weight: {row[0]}, Height: {row[1]}, BMI: {row[2]}, Date: {row[3]}")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
