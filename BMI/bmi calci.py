import tkinter as tk
from tkinter import messagebox, ttk
import json
import datetime
import os

# -------------------------
# Files (users + history)
# -------------------------
USER_FILE = "users.json"
HISTORY_FILE = "bmi_history.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

bmi_history = load_history()

# -------------------------
# Main login window (modern)
# -------------------------
def main_login():
    global login_root
    login_root = tk.Tk()
    login_root.title("BMI Login")
    login_root.geometry("1000x620")
    login_root.configure(bg="#eaf4ff")
    login_root.minsize(900, 550)

    # --- Blue welcome card (centered) ---
    big_card = tk.Frame(login_root, bg="#1e90ff", width=820, height=460)
    big_card.place(relx=0.5, rely=0.5, anchor="center")

    # left: welcome text
    welcome_title = tk.Label(big_card, text="WELCOME", bg="#1e90ff",
                             fg="white", font=("Segoe UI", 36, "bold"))
    welcome_title.place(relx=0.24, rely=0.29, anchor="center")

    welcome_sub = tk.Label(big_card,
                           text="Track your BMI. Stay healthy.\nMonitor your progress easily.",
                           bg="#1e90ff", fg="white", font=("Segoe UI", 14),
                           justify="center")
    welcome_sub.place(relx=0.24, rely=0.45, anchor="center")

    # Create account button on left side
    def open_register_window_wrapper():
        open_register_window(login_root)
    create_acc_btn = tk.Button(big_card, text="Create New Account",
                               bg="white", fg="#1e90ff",
                               font=("Segoe UI", 12, "bold"),
                               relief=tk.FLAT, padx=16, pady=8,
                               command=open_register_window_wrapper)
    create_acc_btn.place(relx=0.24, rely=0.61, anchor="center")

    # --- Floating Sign-in white box on right (with shadow) ---
    # shadow
    shadow = tk.Frame(big_card, bg="#b0cfff", width=340, height=360)
    shadow.place(relx=0.72 + 0.01, rely=0.5 + 0.01, anchor="center")

    sign_box = tk.Frame(big_card, bg="white", width=340, height=360)
    sign_box.place(relx=0.72, rely=0.5, anchor="center")

    # Title
    sign_title = tk.Label(sign_box, text="Sign In", bg="white", fg="#1e90ff",
                          font=("Segoe UI", 26, "bold"))
    sign_title.pack(pady=(18, 6))

    # Fields container to control spacing
    fields_frame = tk.Frame(sign_box, bg="white")
    fields_frame.pack(pady=4)

    # Centered Username label + spaced Entry (doesn't touch box)
    username_label = tk.Label(fields_frame, text="Username", bg="white",
                              font=("Segoe UI", 12))
    username_label.pack(pady=(6, 2))
    # wrap entry inside a small padded frame so it doesn't stick to border
    user_outer = tk.Frame(fields_frame, bg="white", padx=12, pady=2)
    user_outer.pack()
    user_entry = tk.Entry(user_outer, font=("Segoe UI", 12), justify="center", width=24, bd=1, relief="solid")
    user_entry.pack()

    # Password
    password_label = tk.Label(fields_frame, text="Password", bg="white",
                              font=("Segoe UI", 12))
    password_label.pack(pady=(12, 2))
    pass_outer = tk.Frame(fields_frame, bg="white", padx=12, pady=2)
    pass_outer.pack()
    pass_entry = tk.Entry(pass_outer, font=("Segoe UI", 12), justify="center", width=24, bd=1, relief="solid", show="*")
    pass_entry.pack()

    # Login action (validate + animate)
    def on_login_clicked():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()
        users = load_users()
        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return
        if username in users and users[username] == password:
            # success: play slide-down animation and then open dashboard
            login_btn.config(state="disabled")
            play_slide_animation_then_open(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # Login button with hover effect
    def on_enter(e):
        login_btn.config(bg="#155fb3")
    def on_leave(e):
        login_btn.config(bg="#1e68d1")

    login_btn = tk.Button(sign_box, text="Login", bg="#1e68d1", fg="white",
                          font=("Segoe UI", 13, "bold"), relief=tk.FLAT,
                          width=20, height=1, command=on_login_clicked)
    login_btn.pack(pady=(18, 6))
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    # helper animation: slide a colored frame from top to bottom over whole window
    def play_slide_animation_then_open(username):
        # Create an overlay frame above everything, initially just above the visible area
        overlay = tk.Frame(login_root, bg="#1e90ff", width=login_root.winfo_width(),
                           height=login_root.winfo_height())
        # place it just above the window
        overlay.place(x=0, y=-login_root.winfo_height())

        # a label in overlay
        lb = tk.Label(overlay, text="Logging in...", bg="#1e90ff", fg="white",
                      font=("Segoe UI", 26, "bold"))
        lb.place(relx=0.5, rely=0.45, anchor="center")

        # animate slide down using after (non-blocking)
        total_steps = 30
        start_y = -login_root.winfo_height()
        end_y = 0
        dy = (end_y - start_y) / total_steps
        step = 0

        def step_anim():
            nonlocal step
            y = int(start_y + dy * step)
            overlay.place(x=0, y=y)
            step += 1
            if step <= total_steps:
                login_root.after(12, step_anim)
            else:
                # keep overlay for a short time then proceed
                login_root.after(700, lambda: finish_overlay(overlay, username))

        step_anim()

    def finish_overlay(overlay, username):
        # destroy overlay and open the dashboard
        overlay.destroy()
        open_bmi_window(username)
        # close the login window cleanly
        try:
            login_root.destroy()
        except:
            pass

    # Pressing Enter triggers login
    login_root.bind('<Return>', lambda e: on_login_clicked())

    login_root.mainloop()


# -------------------------
# Registration window (same logic)
# -------------------------
def open_register_window(parent=None):
    # parent: the login root
    reg = tk.Toplevel(parent) if parent else tk.Toplevel()
    reg.title("Register")
    reg.geometry("420x340")
    reg.configure(bg="#f0f7ff")
    reg.resizable(False, False)

    tk.Label(reg, text="Create Account", bg="#f0f7ff", fg="#1e68d1",
             font=("Segoe UI", 20, "bold")).pack(pady=16)

    frame = tk.Frame(reg, bg="#f0f7ff")
    frame.pack(pady=6)

    tk.Label(frame, text="Username:", bg="#f0f7ff", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", padx=6, pady=8)
    e_user = tk.Entry(frame, font=("Segoe UI", 12), width=28)
    e_user.grid(row=0, column=1, padx=6, pady=8)

    tk.Label(frame, text="Password:", bg="#f0f7ff", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=6, pady=8)
    e_pass = tk.Entry(frame, font=("Segoe UI", 12), width=28, show="*")
    e_pass.grid(row=1, column=1, padx=6, pady=8)

    def register():
        username = e_user.get().strip()
        password = e_pass.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "All fields required!")
            return
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "User already exists!")
            return
        users[username] = password
        save_users(users)
        messagebox.showinfo("Success", "Account created!")
        reg.destroy()

    tk.Button(reg, text="Register", bg="#1e68d1", fg="white",
              font=("Segoe UI", 12, "bold"), relief=tk.FLAT,
              command=register).pack(pady=18)


# -------------------------
# BMI Dashboard (original logic adapted)
# -------------------------
def open_bmi_window(username):
    # create a new window for dashboard
    dash = tk.Tk()
    dash.title("BMI Dashboard")
    dash.geometry("1200x700")
    dash.minsize(1000, 600)

    # Sidebar
    sidebar = tk.Frame(dash, bg="#2b5c99", width=260)
    sidebar.pack(side="left", fill="y")

    content_area = tk.Frame(dash, bg="#f4f7ff")
    content_area.pack(fill="both", expand=True)

    tk.Label(sidebar, text=f"Welcome\n{username}", bg="#2b5c99",
             fg="white", font=("Segoe UI", 18, "bold")).pack(pady=30)

    def menu_btn(label, cmd):
        return tk.Button(sidebar, text=label, command=cmd,
                         bg="#4d79ff", fg="white",
                         font=("Segoe UI", 12, "bold"),
                         relief=tk.FLAT, pady=10, width=20)

    # placeholder functions to be filled below
    menu_btn("Home", lambda: None).pack(pady=8)
    menu_btn("Calculate BMI", lambda: calculate_bmi()).pack(pady=8)
    menu_btn("View History", lambda: view_history()).pack(pady=8)
    menu_btn("BMI Statistics", lambda: show_stats()).pack(pady=8)
    menu_btn("Trend Graph", lambda: show_graph()).pack(pady=8)
    menu_btn("Logout", lambda: logout()).pack(pady=30)

    # Main card
    card = tk.Frame(content_area, bg="white", width=850, height=560, bd=3, relief=tk.GROOVE)
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(card, text="BMI DASHBOARD", bg="white", fg="#2b5c99",
             font=("Segoe UI", 24, "bold")).pack(pady=20)

    # Inputs
    input_frame = tk.Frame(card, bg="white")
    input_frame.pack(pady=20)

    tk.Label(input_frame, text="Weight (kg):", bg="white", font=("Segoe UI", 14)).grid(row=0, column=0, padx=16, pady=12, sticky="e")
    weight_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=12, bd=1, relief="solid")
    weight_entry.grid(row=0, column=1, padx=16, pady=12)

    tk.Label(input_frame, text="Height (m):", bg="white", font=("Segoe UI", 14)).grid(row=1, column=0, padx=16, pady=12, sticky="e")
    height_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=12, bd=1, relief="solid")
    height_entry.grid(row=1, column=1, padx=16, pady=12)

    result_label = tk.Label(card, text="", bg="white", font=("Segoe UI", 16, "bold"))
    result_label.pack(pady=12)

    def calculate_bmi():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            bmi = round(weight / (height ** 2), 2)
            if bmi < 18.5:
                status = "Underweight"; color = "#e6b800"
            elif bmi < 25:
                status = "Normal"; color = "#4CAF50"
            elif bmi < 30:
                status = "Overweight"; color = "#ff944d"
            else:
                status = "Obese"; color = "#ff4d4d"

            result_label.config(text=f"BMI: {bmi} ({status})", fg=color)
            # save
            new_record = {
                "user": username,
                "weight": weight,
                "height": height,
                "bmi": bmi,
                "status": status,
                "date": str(datetime.date.today())
            }
            bmi_history.append(new_record)
            save_history(bmi_history)
        except Exception as e:
            messagebox.showerror("Error", "Enter valid numbers")

    def view_history():
        history_win = tk.Toplevel(dash)
        history_win.title("BMI History")
        history_win.geometry("700x460")

        tk.Label(history_win, text="BMI History", font=("Segoe UI", 16, "bold")).pack(pady=10)

        tree = ttk.Treeview(history_win, columns=("Weight", "Height", "BMI", "Status", "Date"), show="headings", height=12)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        for col in ["Weight", "Height", "BMI", "Status", "Date"]:
            tree.heading(col, text=col)
        for item in bmi_history:
            if item.get("user") == username:
                tree.insert("", tk.END, values=(item["weight"], item["height"], item["bmi"], item["status"], item["date"]))

    def show_stats():
        data = [x for x in bmi_history if x.get("user") == username]
        if not data:
            messagebox.showinfo("No Data", "No BMI Records Found!")
            return
        bmis = [x["bmi"] for x in data]
        messagebox.showinfo("BMI Stats",
                            f"Total Records : {len(bmis)}\n"
                            f"Average BMI   : {sum(bmis)/len(bmis):.2f}\n"
                            f"Highest BMI   : {max(bmis)}\n"
                            f"Lowest BMI    : {min(bmis)}")

    def show_graph():
        try:
            import matplotlib.pyplot as plt
        except Exception:
            messagebox.showerror("Error", "matplotlib is required to show graph")
            return
        data = [x for x in bmi_history if x.get("user") == username]
        if not data:
            messagebox.showinfo("No Data", "No BMI Records")
            return
        dates = [x["date"] for x in data]
        bmis = [x["bmi"] for x in data]
        plt.figure(figsize=(8,4))
        plt.plot(dates, bmis, marker="o")
        plt.title("BMI Trend")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def logout():
        dash.destroy()
        # reopen login window
        main_login()

    dash.mainloop()


# -------------------------
# Start the app
# -------------------------
if __name__ == "__main__":
    main_login()
