import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import ImageTk, Image
from datetime import datetime, timedelta
import sys
import time

class WelcomeScreen:
    def __init__(self, window):
        self.window = window
        self.window.title("Welcome to Assignment Reminder")
        self.window.geometry("400x240")
        self.window.configure(bg="#FFFFE0")  # Warna latar belakang krem
        self.window.resizable(False, False)
        
        # Agar Muncul tepat di tengah layar
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 400
        window_height = 240
        x_position = int((screen_width / 2) - (window_width / 2))
        y_position = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        self.label_welcome = tk.Label(self.window, text="Welcome to Assignments Reminder", font=("Elephant", 16), bg="#FFFFE0")
        self.label_welcome.pack(pady=10)

        self.label_name = tk.Label(self.window, text="Made by\nAbdul Fattah Rahmadiansyah", font=("Elephant", 12), bg="#FFFFE0")
        self.label_name.pack(pady=10)

        self.button_login = tk.Button(self.window, text="Masuk", command=self.login, font=("Arial", 12, "bold"), bg="#FFA500", fg="white")
        self.button_login.pack(pady=10)

        self.button_exit = tk.Button(self.window, text="Keluar", command=self.exit_program, font=("Arial", 12, "bold"), bg="#FFA500", fg="white")
        self.button_exit.pack(pady=10)


    def login(self):
        self.window.destroy()  # tutup jendela WelcomeScreen
        window = tk.Tk()  # buat jendela utama
        app = AssignmentsReminder(window)  # buat objek AssignmentReminder
        window.mainloop()  # jalanin GUI loop

    def exit_program(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to exit?"):
            self.window.quit()

class AssignmentsReminder:
    def __init__(self, window):
        # Window Aplikasi
        self.window = window
        self.window.title("Assignments Reminder")
        self.window.geometry("780x580")
        self.window.resizable(False, False)
        bg_color1 = "#FFFFE0" 
        self.window.configure(bg=bg_color1)
        self.font_title = ("Montserrat", 20, "bold")
        self.font_author = ("Montserrat", 12)
        self.font_button = ("Montserrat", 12, "bold")
        self.font_clock = ("DS-Digital","bold")  
        
        # Agar Muncul tepat di tengah layar
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 780
        window_height = 580
        x_position = int((screen_width / 2) - (window_width / 2))
        y_position = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Judul Program
        self.label_heading = tk.Label(self.window, text="Assignments Reminder", font=("Rockwell Extra Bold",24), fg="#FFA500", bg=bg_color1)
        self.label_heading.place(x=30, y=40)

        # Elemen jam
        self.label_clock = tk.Label(self.window, font=(self.font_clock, 60), fg="orange", justify="right", bg=bg_color1)  
        self.label_clock.place(x=630, y=20, anchor="n")
        self.update_clock() 

        # Elemen penambah tugas
        self.label_add_task = tk.Label(self.window, text="Add Task:", font=self.font_button, fg="#FFA500", bg=bg_color1)
        self.label_add_task.place(x=30, y=130)

        self.entry_task = tk.Entry(self.window, font=self.font_button, width=31, bg=bg_color1)
        self.entry_task.place(x=160, y=130)

        self.button_add_task = tk.Button(self.window, text="Add", command=self.add_task, font=self.font_button, width=12, bg="#FFA500", fg="white")
        self.button_add_task.place(x=445, y=130)

        # Elemen deadline
        self.label_deadline = tk.Label(self.window, text="Deadline:", font=self.font_button, fg="#FFA500", bg=bg_color1)
        self.label_deadline.place(x=30, y=195)

        self.entry_deadline = tk.Entry(self.window, font=self.font_button, width=31, state="readonly", bg=bg_color1)
        self.entry_deadline.place(x=160, y=195)

        self.button_set_deadline = tk.Button(self.window, text="Set Deadline", command=self.set_deadline, font=self.font_button, width=12, bg="#FFA500", fg="white")
        self.button_set_deadline.place(x=445, y=195)

        # Elemen daftar Tugas
        self.label_task_list = tk.Label(self.window, text="Daftar Tugas:", font=self.font_button, fg="#FFA500", bg=bg_color1)
        self.label_task_list.place(x=30, y=260)#label daftar tugas

        self.listbox_tasks = tk.Listbox(self.window, font=self.font_button, height=10, width=60, bg=bg_color1)
        self.listbox_tasks.place(x=30, y=300)#list daftar tugas

        self.button_delete_task = tk.Button(self.window, text="Delete", command=self.delete_task, font=self.font_button, bg="#FFA500", fg="white")
        self.button_delete_task.place(x=30, y=525)#button delete tugas

        self.button_undo_delete = tk.Button(self.window, text="Undo", command=self.undo_delete, font=self.font_button, bg="#FFA500", fg="white")
        self.button_undo_delete.place(x=230, y=525)#button undo delete

        self.button_reminder = tk.Button(self.window, text="Show Reminder", command=self.show_reminder, font=self.font_button, bg="#FFA500", fg="white")
        self.button_reminder.place(x=435, y=525)#Reminder from my Yotsuba

        # Elemen pomodoro timer
        self.label_pomodoro = tk.Label(self.window, text="Pomodoro Timer:", font=self.font_button, fg="#FFA500", bg=bg_color1)
        self.label_pomodoro.place(x=601, y=130)

        self.label_pomodoro_time = tk.Label(self.window, text="30:00", font=("Ds-Digital", 30), fg="#FFA500", bg=bg_color1)
        self.label_pomodoro_time.place(x=621, y=150)

        self.button_pomodoro_start = tk.Button(self.window, text="Start", command=self.start_pomodoro, font=self.font_button, bg="#FFA500", fg="white")
        self.button_pomodoro_start.place(x=611, y=200)

        self.button_pomodoro_reset = tk.Button(self.window, text="Reset", command=self.reset_pomodoro, font=self.font_button, bg="#FFA500", fg="white")
        self.button_pomodoro_reset.place(x=641, y=240)

        self.button_pomodoro_stop = tk.Button(self.window, text="Stop", command=self.stop_pomodoro, font=self.font_button, bg="#FFA500", fg="white")
        self.button_pomodoro_stop.place(x=671, y=200)

        # Elemen timer istirahat
        self.label_istirahat = tk.Label(self.window, text="Charging Up Timer:", font=self.font_button, bg=bg_color1,fg="#FFA500" )
        self.label_istirahat.place(x=601, y=295)

        self.label_istirahat_time = tk.Label(self.window, text="05:00", font=("Ds-Digital", 30), bg=bg_color1,fg="#FFA500")
        self.label_istirahat_time.place(x=625, y=320)

        self.button_istirahat_start = tk.Button(self.window, text="Start", command=self.start_istirahat, font=self.font_button, bg="#FFA500",fg="white")
        self.button_istirahat_start.place(x=610, y=365)

        self.button_istirahat_stop = tk.Button(self.window, text="Stop", command=self.stop_istirahat, font=self.font_button, bg="#FFA500",fg="white")
        self.button_istirahat_stop.place(x=671, y=365)

        self.button_istirahat_reset = tk.Button(self.window, text="Reset", command=self.reset_istirahat, font=self.font_button, bg="#FFA500",fg="white")
        self.button_istirahat_reset.place(x=631, y=405)

        # Elemen Menu
        self.menubar = tk.Menu(self.window)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.exit_application)
        self.menubar.add_cascade(label="You Done?", menu=self.file_menu)
        self.window.config(menu=self.menubar)


        #Stack
        self.deleted_tasks = []  # Menyimpan tugas yang dihapus
        
        #Elemen Timer 
        self.pomodoro_running = False
        self.istirahat_running = False
        self.pomodoro_time = timedelta(minutes=30)
        self.istirahat_time = timedelta(minutes=5)
        self.timer_end = datetime.now()
        self.timer_start = datetime.now()
        
    #FITUR-FITUR SUBSTANSI NAMBAH, DELETE, NGATUR DEADLINE, DAN JAM
    #Fungsi update jam 
    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")  #waktu saat ini
        self.label_clock.config(text=current_time, anchor="center")
        self.label_clock.after(1000, self.update_clock)  # memperbarui setiap 1 detik

    def add_task(self):
        task = self.entry_task.get()
        deadline = self.entry_deadline.get()       
        current_date = time.strftime("%Y-%m-%d") #tanggal real-time
        self.update_clock()
        if deadline:
            if task:
                task_with_deadline = f"{task}"
                self.entry_task.delete(0, tk.END)
                self.entry_deadline.config(state="normal")
                self.entry_deadline.delete(0, tk.END)
                self.entry_deadline.config(state="readonly")
                if deadline >= current_date:  # ngecek deadline udh lewat belum
                    task_with_deadline = f"{task} (Deadline: {deadline})"
                    self.listbox_tasks.insert(tk.END, task_with_deadline)
                    self.entry_task.delete(0, tk.END)
                    self.entry_deadline.delete(0, tk.END)
                else:
                    messagebox.showwarning("Invalid Deadline", "Deadline has passed!")
            else:
                messagebox.showwarning("Empty Task", "Please enter a task!")
        else:
            messagebox.showwarning("Empty Deadline", "Please set a deadline!")

    def show_reminder(self):
        messagebox.showinfo("Yotsuba, your wife", "Jangan lupa kerjain tugasnya ya, sayang!")
        
    def delete_task(self):
        selected_task_index = self.listbox_tasks.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this task?")
            if confirm:
                self.listbox_tasks.delete(selected_task_index)

    def set_deadline(self):
        top = tk.Toplevel(self.window)
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=10)

        def set_selected_date():
            selected_date = cal.get_date()
            
            current_date = time.strftime("%Y-%m-%d")  # Mendapatkan tanggal real-time
            
            if selected_date >= current_date:  # Pengecekan apakah deadline masih belum lewat
                self.entry_deadline.config(state="normal")
                self.entry_deadline.delete(0, tk.END)
                self.entry_deadline.insert(tk.END, selected_date)
                self.entry_deadline.config(state="readonly")
                top.destroy()
            else:
                messagebox.showwarning("Invalid Deadline", "Deadline has passed!")

        button_select_date = tk.Button(top, text="Select Date", command=set_selected_date, font=self.font_button)
        button_select_date.pack(pady=10)
        
    def undo_delete(self):
        if self.deleted_tasks:
            last_deleted_task = self.deleted_tasks.pop()
            self.listbox_tasks.insert(tk.END, last_deleted_task)
    
    def delete_task(self):
        selected_task_index = self.listbox_tasks.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this task?")
            if confirm:
                deleted_task = self.listbox_tasks.get(selected_task_index)
                self.listbox_tasks.delete(selected_task_index)
                self.deleted_tasks.append(deleted_task)  # Menyimpan tugas yang dihapus ke dalam Stack
                
                
    #FIUR POMOORO 
    def start_pomodoro(self):
        if not self.pomodoro_running:
            self.timer_end = datetime.now() + self.pomodoro_time
            self.pomodoro_running = True
            self.update_pomodoro_timer()
            self.button_istirahat_start.config(state="disabled")  # Menonaktifkan tombol untuk memulai istirahat
            self.button_istirahat_reset.config(state="disabled")  # Menonaktifkan tombol untuk mereset istirahat
            self.button_istirahat_stop.config(state="disabled")  # Menonaktifkan tombol untuk menghentikan istirahat

    def stop_pomodoro(self):
        self.pomodoro_running = False
        self.button_istirahat_start.config(state="normal")  # Mengaktifkan kembali tombol untuk memulai istirahat
        self.button_istirahat_stop.config(state="normal")  # Mengaktifkan kembali tombol untuk mereset istirahat
        self.button_istirahat_reset.config(state="normal")  # Mengaktifkan kembali tombol untuk menghentikan istirahat

    def reset_pomodoro(self):
        self.timer_end = datetime.now()
        self.pomodoro_running = False
        self.label_pomodoro_time.config(text="30:00")
        self.button_istirahat_start.config(state="normal")  # Mengaktifkan kembali tombol untuk memulai istirahat
        self.button_istirahat_stop.config(state="normal")  # Mengaktifkan kembali tombol untuk mereset istirahat
        self.button_istirahat_reset.config(state="normal")  # Mengaktifkan kembali tombol untuk menghentikan istirahat

    def start_istirahat(self):
        if not self.istirahat_running:
            self.timer_end = datetime.now() + self.istirahat_time
            self.istirahat_running = True
            self.update_istirahat_timer()
            self.button_pomodoro_start.config(state="disabled")  # Menonaktifkan tombol untuk memulai pomodoro
            self.button_pomodoro_reset.config(state="disabled")  # Menonaktifkan tombol untuk mereset pomodoro
            self.button_pomodoro_stop.config(state="disabled")  # Menonaktifkan tombol untuk menghentikan pomodoro

    def stop_istirahat(self):
        self.istirahat_running = False
        self.button_pomodoro_start.config(state="normal")  # Mengaktifkan kembali tombol untuk memulai pomodoro
        self.button_pomodoro_reset.config(state="normal")  # Mengaktifkan kembali tombol untuk mereset pomodoro
        self.button_pomodoro_stop.config(state="normal")  # Mengaktifkan kembali tombol untuk menghentikan pomodoro

    def reset_istirahat(self):
        self.timer_end = datetime.now()
        self.istirahat_running = False
        self.label_istirahat_time.config(text="05:00")
        self.button_pomodoro_start.config(state="normal")  # Mengaktifkan kembali tombol untuk memulai pomodoro
        self.button_pomodoro_start.config(state="normal")  
        self.button_pomodoro_reset.config(state="normal")  
        self.button_pomodoro_stop.config(state="normal")
        
    def update_pomodoro_timer(self):
        if self.pomodoro_running:
            time_left = self.timer_end - datetime.now()
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                seconds = int(time_left.total_seconds() % 60)
                timer_text = f"{minutes:02d}:{seconds:02d}"
                self.label_pomodoro_time.config(text=timer_text)
                self.label_pomodoro_time.after(1000, self.update_pomodoro_timer)
            else:
                self.pomodoro_running = False
                self.label_pomodoro_time.config(text="00:00")
                messagebox.showinfo("Reminder", "Kick back and relax. You deserve it!")
                self.reset_pomodoro()

    def update_istirahat_timer(self):
        if self.istirahat_running:
            time_left = self.timer_end - datetime.now()
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                seconds = int(time_left.total_seconds() % 60)
                timer_text = f"{minutes:02d}:{seconds:02d}"
                self.label_istirahat_time.config(text=timer_text)
                self.label_istirahat_time.after(1000, self.update_istirahat_timer)
            else:
                self.istirahat_running = False
                self.label_istirahat_time.config(text="00:00")
                messagebox.showinfo("Reminder", "Rest is over. You can continue work or call it a day. Your choice, my Lord.")
                self.reset_istirahat()


    def exit_application(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to exit?"):
            self.window.quit()
            sys.exit()

# Bikin jendela utama
window = tk.Tk()

# Bikin objek WelcomeScreen
welcome_screen = WelcomeScreen(window)

# Menjalankan GUI loop
window.mainloop()


