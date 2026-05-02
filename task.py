import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Файл для хранения истории
HISTORY_FILE = "quotes_history.json"

# Предопределенные цитаты (текст, автор, тема)
DEFAULT_QUOTES = [
    {"text": "Будь тем изменением, которое хочешь видеть в мире", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Единственный способ делать великую работу - любить то, что ты делаешь", "author": "Стив Джобс", "topic": "Работа"},
    {"text": "Сначала ты не замечаешь перемен, затем они становятся неизбежными", "author": "Франц Кафка", "topic": "Жизнь"},
    {"text": "Успех - это способность идти от неудачи к неудаче, не теряя энтузиазма", "author": "Уинстон Черчилль", "topic": "Мотивация"},
    {"text": "Любовь - это единственная сила, способная превратить врага в друга", "author": "Мартин Лютер Кинг", "topic": "Любовь"},
    {"text": "Чтение делает человека знающим, разговор - находимым, а привычка записывать - точным", "author": "Фрэнсис Бэкон", "topic": "Учеба"},
    {"text": "Не бойся идти медленно, бойся стоять на месте", "author": "Китайская пословица", "topic": "Мотивация"},
    {"text": "Лучший способ предсказать будущее - изобрести его", "author": "Алан Кей", "topic": "Будущее"},
    {"text": "Счастье - это когда то, что ты думаешь, говоришь и делаешь, находится в гармонии", "author": "Махатма Ганди", "topic": "Счастье"},
    {"text": "Знание - сила", "author": "Фрэнсис Бэкон", "topic": "Учеба"},
    {"text": "Всё гениальное - просто", "author": "Альберт Эйнштейн", "topic": "Мудрость"},
    {"text": "Делай, что можешь, с тем, что имеешь, там, где ты есть", "author": "Теодор Рузвельт", "topic": "Мотивация"},
    {"text": "Путь в тысячу миль начинается с первого шага", "author": "Лао-Цзы", "topic": "Мудрость"},
    {"text": "Ваше время ограничено, не тратьте его на жизнь чужой жизнью", "author": "Стив Джобс", "topic": "Жизнь"},
]

# Глобальные переменные
quotes = []  # Список всех цитат
history = []  # История сгенерированных цитат


# --- ФУНКЦИИ РАБОТЫ С JSON ---
def load_data():
    """Загружает цитаты и историю из файлов"""
    global quotes, history

    # Загружаем цитаты
    if os.path.exists("quotes.json"):
        try:
            with open("quotes.json", "r", encoding="utf-8") as f:
                quotes = json.load(f)
        except (json.JSONDecodeError, IOError):
            quotes = DEFAULT_QUOTES.copy()
    else:
        quotes = DEFAULT_QUOTES.copy()

    # Загружаем историю
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []


def save_quotes():
    """Сохраняет все цитаты в JSON файл"""
    try:
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить цитаты: {e}")


def save_history():
    """Сохраняет историю в JSON файл"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")


# --- ФУНКЦИИ РАБОТЫ С ЦИТАТАМИ ---
def generate_quote():
    """Генерирует случайную цитату"""
    if not quotes:
        messagebox.showwarning("Внимание", "Список цитат пуст. Добавьте новые цитаты!")
        return

    # Выбираем случайную цитату
    quote = random.choice(quotes)

    # Добавляем в историю с отметкой времени
    history_record = {
        "text": quote["text"],
        "author": quote["author"],
        "topic": quote["topic"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.insert(0, history_record)  # Новые вверху
    save_history()

    # Отображаем цитату
    display_quote(quote)

    # Обновляем таблицу истории
    update_history_table()

    # Обновляем счетчик
    update_stats()


def display_quote(quote):
    """Отображает цитату на экране"""
    quote_text.config(text=f'"{quote["text"]}"')
    author_label.config(text=f"— {quote['author']}")
    topic_label.config(text=f"Тема: {quote['topic']}")


def update_history_table():
    """Обновляет таблицу истории"""
    # Очищаем таблицу
    for item in history_tree.get_children():
        history_tree.delete(item)

    # Применяем фильтры
    filtered_history = history.copy()

    # Фильтр по автору
    filter_author = filter_author_entry.get().strip()
    if filter_author:
        filtered_history = [h for h in filtered_history if filter_author.lower() in h["author"].lower()]

    # Фильтр по теме
    filter_topic = filter_topic_entry.get().strip()
    if filter_topic:
        filtered_history = [h for h in filtered_history if filter_topic.lower() in h["topic"].lower()]

    # Добавляем записи в таблицу
    for record in filtered_history:
        history_tree.insert("", "end", values=(
            record["date"],
            record["text"][:50] + "..." if len(record["text"]) > 50 else record["text"],
            record["author"],
            record["topic"]
        ))

    # Обновляем статус
    status_label.config(text=f"Показано записей: {len(filtered_history)} из {len(history)}")


def update_stats():
    """Обновляет статистику"""
    total_quotes = len(quotes)
    total_history = len(history)
    unique_authors = len(set(q["author"] for q in quotes))
    unique_topics = len(set(q["topic"] for q in quotes))

    stats_label.config(text=f"📚 Цитат: {total_quotes} | 📜 В истории: {total_history} | ✍️ Авторов: {unique_authors} | 🏷️ Тем: {unique_topics}")


def apply_filters():
    """Применяет фильтры к истории"""
    update_history_table()


def reset_filters():
    """Сбрасывает фильтры"""
    filter_author_entry.delete(0, tk.END)
    filter_topic_entry.delete(0, tk.END)
    update_history_table()


def clear_history():
    """Очищает всю историю"""
    if messagebox.askyesno("Подтверждение", "Вы действительно хотите очистить всю историю?"):
        global history
        history = []
        save_history()
        update_history_table()
        update_stats()
        messagebox.showinfo("Успех", "История очищена")


def add_new_quote():
    """Открывает окно для добавления новой цитаты"""
    add_window = tk.Toplevel(root)
    add_window.title("Добавить новую цитату")
    add_window.geometry("500x400")
    add_window.resizable(False, False)

    # Поля ввода
    tk.Label(add_window, text="Текст цитаты:", font=("Arial", 11, "bold")).pack(pady=(20, 5))
    text_entry = tk.Text(add_window, height=5, width=50, font=("Arial", 10))
    text_entry.pack(pady=5)

    tk.Label(add_window, text="Автор:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
    author_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
    author_entry.pack(pady=5)

    tk.Label(add_window, text="Тема:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
    topic_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
    topic_entry.pack(pady=5)

    def save_new_quote():
        text = text_entry.get("1.0", tk.END).strip()
        author = author_entry.get().strip()
        topic = topic_entry.get().strip()

        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым")
            return
        if not topic:
            messagebox.showerror("Ошибка", "Тема не может быть пустой")
            return

        # Добавляем цитату
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        quotes.append(new_quote)
        save_quotes()
        update_stats()

        messagebox.showinfo("Успех", "Цитата добавлена!")
        add_window.destroy()

    tk.Button(add_window, text="Сохранить цитату", command=save_new_quote,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20).pack(pady=20)


def delete_selected_quote():
    """Удаляет выбранную цитату из списка цитат"""
    if messagebox.askyesno("Подтверждение", "Удалить выбранную цитату?"):
        # Получаем текущую отображаемую цитату
        current_text = quote_text.cget("text").strip('"')
        for i, q in enumerate(quotes):
            if q["text"] == current_text:
                quotes.pop(i)
                save_quotes()
                update_stats()
                messagebox.showinfo("Успех", "Цитата удалена")
                # Генерируем новую цитату
                if quotes:
                    generate_quote()
                else:
                    quote_text.config(text="Нет доступных цитат")
                    author_label.config(text="")
                    topic_label.config(text="")
                return

        messagebox.showwarning("Внимание", "Не удалось найти цитату для удаления")


def on_double_click(event):
    """Показывает полную цитату из истории при двойном клике"""
    selected = history_tree.selection()
    if selected:
        item = history_tree.item(selected[0])
        values = item['values']

        info = f"📅 Дата: {values[0]}\n\n"
        info += f"📖 Цитата:\n{values[1]}\n\n"
        info += f"✍️ Автор: {values[2]}\n"
        info += f"🏷️ Тема: {values[3]}"

        messagebox.showinfo("Полная цитата", info)


# --- СОЗДАНИЕ ИНТЕРФЕЙСА ---
def create_interface():
    global root, quote_text, author_label, topic_label, history_tree
    global filter_author_entry, filter_topic_entry, status_label, stats_label

    root = tk.Tk()
    root.title("Random Quote Generator - Генератор случайных цитат")
    root.geometry("1000x700")

    # Заголовок
    title_label = tk.Label(root, text="✨ Генератор случайных цитат ✨",
                           font=("Arial", 18, "bold"), fg="#2C3E50")
    title_label.pack(pady=15)

    # --- Фрейм для отображения цитаты ---
    quote_frame = tk.Frame(root, bg="#F0F0F0", relief="ridge", bd=2)
    quote_frame.pack(fill="x", padx=20, pady=10)

    quote_text = tk.Label(quote_frame, text="Нажмите кнопку для генерации цитаты",
                          font=("Arial", 14, "italic"), wraplength=800, justify="center",
                          bg="#F0F0F0", fg="#555555")
    quote_text.pack(pady=(30, 10))

    author_label = tk.Label(quote_frame, text="", font=("Arial", 12, "bold"),
                            bg="#F0F0F0", fg="#2196F3")
    author_label.pack(pady=(0, 10))

    topic_label = tk.Label(quote_frame, text="", font=("Arial", 10),
                           bg="#F0F0F0", fg="#9E9E9E")
    topic_label.pack(pady=(0, 20))

    # --- Кнопки управления ---
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    generate_button = tk.Button(button_frame, text="🎲 Сгенерировать цитату", command=generate_quote,
                                bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
    generate_button.pack(side="left", padx=5)

    add_button = tk.Button(button_frame, text="➕ Добавить цитату", command=add_new_quote,
                           bg="#2196F3", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
    add_button.pack(side="left", padx=5)

    delete_button = tk.Button(button_frame, text="🗑️ Удалить текущую цитату", command=delete_selected_quote,
                              bg="#F44336", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
    delete_button.pack(side="left", padx=5)

    # --- Статистика ---
    stats_label = tk.Label(root, text="", font=("Arial", 10), fg="#666666")
    stats_label.pack(pady=5)

    # --- Фрейм фильтрации ---
    filter_frame = tk.LabelFrame(root, text="🔍 Фильтрация истории", font=("Arial", 11, "bold"), padx=10, pady=5)
    filter_frame.pack(fill="x", padx=20, pady=10)

    # Фильтр по автору
    tk.Label(filter_frame, text="Автор:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    filter_author_entry = tk.Entry(filter_frame, width=20, font=("Arial", 10))
    filter_author_entry.grid(row=0, column=1, padx=5, pady=5)

    # Фильтр по теме
    tk.Label(filter_frame, text="Тема:", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
    filter_topic_entry = tk.Entry(filter_frame, width=20, font=("Arial", 10))
    filter_topic_entry.grid(row=0, column=3, padx=5, pady=5)

    # Кнопки фильтрации
    filter_button = tk.Button(filter_frame, text="Применить фильтр", command=apply_filters,
                              bg="#FF9800", fg="white", font=("Arial", 9))
    filter_button.grid(row=0, column=4, padx=5, pady=5)

    reset_button = tk.Button(filter_frame, text="Сбросить", command=reset_filters,
                             bg="#9E9E9E", fg="white", font=("Arial", 9))
    reset_button.grid(row=0, column=5, padx=5, pady=5)

    # --- История цитат ---
    history_frame = tk.LabelFrame(root, text="📜 История сгенерированных цитат", font=("Arial", 11, "bold"), padx=10, pady=5)
    history_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Таблица истории
    columns = ("Дата", "Цитата", "Автор", "Тема")
    history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

    history_tree.heading("Дата", text="Дата")
    history_tree.heading("Цитата", text="Цитата")
    history_tree.heading("Автор", text="Автор")
    history_tree.heading("Тема", text="Тема")

    history_tree.column("Дата", width=140)
    history_tree.column("Цитата", width=400)
    history_tree.column("Автор", width=150)
    history_tree.column("Тема", width=150)

    # Скроллбар
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
    history_tree.configure(yscrollcommand=scrollbar.set)

    history_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Двойной клик для просмотра полной цитаты
    history_tree.bind("<Double-1>", on_double_click)

    # --- Кнопка очистки истории ---
    clear_button = tk.Button(root, text="🗑️ Очистить историю", command=clear_history,
                             bg="#F44336", fg="white", font=("Arial", 10), padx=15)
    clear_button.pack(pady=(0, 10))

    # --- Статусная строка ---
    status_label = tk.Label(root, text="Готов к работе", bd=1, relief=tk.SUNKEN,
                            anchor=tk.W, font=("Arial", 9))
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Инициализация данных ---
    load_data()
    update_stats()
    update_history_table()

    return root


# --- ЗАПУСК ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    print("Загрузка Random Quote Generator...")
    print("Доступные цитаты загружены")

    root = create_interface()
    root.mainloop()