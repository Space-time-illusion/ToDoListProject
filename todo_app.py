import tkinter as tk
from tkinter import messagebox
import sqlite3

# 创建数据库并初始化
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        task TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# 添加任务
def add_task():
    task = task_entry.get()
    if task != "":
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

# 删除任务
def delete_task():
    try:
        task_id = task_listbox.get(task_listbox.curselection())[0]
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# 加载任务
def load_tasks():
    task_listbox.delete(0, tk.END)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    for task in tasks:
        task_listbox.insert(tk.END, (task[0], task[1]))  # task[0]是ID，task[1]是任务内容
    conn.close()

# 设置GUI
root = tk.Tk()
root.title("Todo List")

# 输入框
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# 添加任务按钮
add_button = tk.Button(root, text="Add Task", width=40, command=add_task)
add_button.pack(pady=10)

# 任务列表框
task_listbox = tk.Listbox(root, height=10, width=40, selectmode=tk.SINGLE)
task_listbox.pack(pady=10)

# 删除任务按钮
delete_button = tk.Button(root, text="Delete Task", width=40, command=delete_task)
delete_button.pack(pady=10)

# 初始化数据库
init_db()

# 加载任务列表
load_tasks()

# 启动应用
root.mainloop()
