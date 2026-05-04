import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Поля для ввода
        frame_input = ttk.Frame(self.root, padding="10")
        frame_input.grid(row=0, column=0, sticky="W")

        ttk.Label(frame_input, text="Дата (дд.мм.гггг):").grid(row=0, column=0, sticky="W")
        self.date_entry = ttk.Entry(frame_input)
        self.date_entry.grid(row=0, column=1)

        ttk.Label(frame_input, text="Температура (°C):").grid(row=1, column=0, sticky="W")
        self.temp_entry = ttk.Entry(frame_input)
        self.temp_entry.grid(row=1, column=1)

        ttk.Label(frame_input, text="Описание погоды:").grid(row=2, column=0, sticky="W")
        self.desc_entry = ttk.Entry(frame_input)
        self.desc_entry.grid(row=2, column=1)

        ttk.Label(frame_input, text="Осадки (да/нет):").grid(row=3, column=0, sticky="W")
        self.precip_var = tk.StringVar()
        self.precip_combo = ttk.Combobox(frame_input, textvariable=self.precip_var, values=["да", "нет"], state="readonly")
        self.precip_combo.grid(row=3, column=1)
        self.precip_combo.current(1)

        # Buttons for adding, saving, loading
        frame_buttons = ttk.Frame(self.root, padding="10")
        frame_buttons.grid(row=1, column=0, sticky="W")

        ttk.Button(frame_buttons, text="Добавить запись", command=self.add_record).grid(row=0, column=0, padx=5)
        ttk.Button(frame_buttons, text="Сохранить в JSON", command=self.save_to_json).grid(row=0, column=1, padx=5)
        ttk.Button(frame_buttons, text="Загрузить из JSON", command=self.load_from_json).grid(row=0, column=2, padx=5)

        # Фильтры
        frame_filter = ttk.Frame(self.root, padding="10")
        frame_filter.grid(row=2, column=0, sticky="W")

        ttk.Label(frame_filter, text="Фильтр по дате (дд.мм.гггг):").grid(row=0, column=0, sticky="W")
        self.filter_date_entry = ttk.Entry(frame_filter)
        self.filter_date_entry.grid(row=0, column=1)
        ttk.Button(frame_filter, text="Применить", command=self.filter_by_date).grid(row=0, column=2, padx=5)
        ttk.Button(frame_filter, text="Очистить фильтр", command=self.refresh_table).grid(row=0, column=3, padx=5)

        ttk.Label(frame_filter, text="Фильтр по температуре (> °C):").grid(row=1, column=0, sticky="W")
        self.filter_temp_entry = ttk.Entry(frame_filter)
        self.filter_temp_entry.grid(row=1, column=1)
        ttk.Button(frame_filter, text="Применить", command=self.filter_by_temp).grid(row=1, column=2, padx=5)
        ttk.Button(frame_filter, text="Очистить фильтр", command=self.refresh_table).grid(row=1, column=3, padx=5)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Температура", "Описание", "Осадки"), show="headings")
        for col in ("Дата", "Температура", "Описание", "Осадки"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=3, column=0, padx=10, pady=10)

    def validate_input(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте дд.мм.гггг")
            return False

        # Проверка температуры
        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return False

        # Проверка описания
        if not desc.strip():
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return False

        return True

    def add_record(self):
        if not self.validate_input():
            return

        record = {
            "date": self.date_entry.get(),
            "temperature": float(self.temp_entry.get()),
            "description": self.desc_entry.get(),
            "precipitation": self.precip_var.get() == "да"
        }
        self.records.append(record)
        self.refresh_table()
        self.clear_inputs()

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_combo.current(1)

    def refresh_table(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if records is None:
            records = self.records
        for rec in records:
            self.tree.insert("", tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                "да" if rec["precipitation"] else "нет"
            ))

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.records = json.load(f)
            self.refresh_table()

    def filter_by_date(self):
        date_str = self.filter_date_entry.get()
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра")
            return
        filtered = [rec for rec in self.records if rec["date"] == date_str]
        self.refresh_table(filtered)

    def filter_by_temp(self):
        try:
            temp_threshold = float(self.filter_temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовое значение для фильтра по температуре")
            return
        filtered = [rec for rec in self.records if rec["temperature"] > temp_threshold]
        self.refresh_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
