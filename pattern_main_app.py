 # File: pattern_main_app.py
import tkinter as tk
from tkinter import messagebox, font, ttk
import pattern_backend_logic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Main Application Class (Unchanged) ---
class PatternAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        pattern_backend_logic.initialize_csv()
        self.title("Pattern-Only Authentication")
        self.geometry("450x350") # Window can be shorter now
        self.configure(bg="#f0f0f0")
        self.default_font = font.Font(family="Helvetica", size=12)
        self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegisterPage, ProfilePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont, data=None):
        frame = self.frames[cont]
        if data:
            frame.display_data(data)
        frame.tkraise()

# --- MODIFIED: Login Page UI and Logic ---
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        header_label = tk.Label(self, text="User Login", font=controller.header_font, bg="#f0f0f0")
        username_label = tk.Label(self, text="Username:", font=controller.default_font, bg="#f0f0f0")
        self.username_entry = tk.Entry(self, font=controller.default_font, width=30)
        
        # --- REMOVED: Password Label and Entry ---
        
        login_button = tk.Button(self, text="Login with Pattern", font=controller.default_font, bg="#4CAF50", fg="white", command=self.handle_login)
        switch_label = tk.Label(self, text="Don't have an account?", font=controller.default_font, bg="#f0f0f0")
        switch_button = tk.Button(self, text="Register Here", font=controller.default_font, relief="flat", fg="#007BFF", bg="#f0f0f0", command=lambda: controller.show_frame(RegisterPage))
        
        header_label.pack(pady=(20, 10))
        username_label.pack(pady=5)
        self.username_entry.pack(pady=5)
        login_button.pack(pady=20, ipadx=10)
        switch_label.pack()
        switch_button.pack()

    def handle_login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
            
        # --- MODIFIED: Call to backend no longer includes password ---
        success, data_dict = pattern_backend_logic.login_user(username, self.controller)
        
        if success:
            self.username_entry.delete(0, 'end')
            self.controller.show_frame(ProfilePage, data_dict)
        else:
            messagebox.showerror("Login Failed", data_dict["message"])


# --- MODIFIED: Register Page UI and Logic ---
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        header_label = tk.Label(self, text="Create Account", font=controller.header_font, bg="#f0f0f0")
        username_label = tk.Label(self, text="Username:", font=controller.default_font, bg="#f0f0f0")
        self.username_entry = tk.Entry(self, font=controller.default_font, width=30)
        
        # --- REMOVED: Password Label and Entry ---
        
        self.register_button = tk.Button(self, text="Register with Pattern", font=controller.default_font, bg="#007BFF", fg="white", command=self.handle_register)
        self.status_label = tk.Label(self, text="", font=controller.default_font, bg="#f0f0f0", fg="blue")
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        switch_label = tk.Label(self, text="Already have an account?", font=controller.default_font, bg="#f0f0f0")
        switch_button = tk.Button(self, text="Login Here", font=controller.default_font, relief="flat", fg="#007BFF", bg="#f0f0f0", command=lambda: controller.show_frame(LoginPage))
        
        header_label.pack(pady=(20, 10))
        username_label.pack(pady=5)
        self.username_entry.pack(pady=5)
        self.register_button.pack(pady=20, ipadx=10)
        self.status_label.pack(pady=5)
        self.progress_bar.pack(pady=5)
        switch_label.pack(pady=(10,0))
        switch_button.pack()

    def handle_register(self):
        username = self.username_entry.get().strip()
        self.register_button.config(state="disabled")
        
        # --- MODIFIED: Call to backend no longer includes password ---
        success, message = pattern_backend_logic.register_user(username, self.controller, self.status_label, self.progress_bar)
        
        if success:
            messagebox.showinfo("Success", message)
            self.reset_state()
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Error", message)
            self.reset_state()
            
    def reset_state(self):
        self.register_button.config(state="normal")
        self.status_label.config(text="")
        self.progress_bar["value"] = 0
        self.username_entry.delete(0, 'end')

# --- Profile Page (Unchanged) ---
class ProfilePage(tk.Frame):
    # This entire class is identical to the previous version.
    # It just plots the feature vectors.
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.welcome_label = tk.Label(self, text="", font=controller.header_font, bg="#f0f0f0")
        self.welcome_label.pack(pady=10)
        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.pack(pady=10, padx=10)
        logout_button = tk.Button(self, text="Logout", font=controller.default_font, command=self.logout)
        logout_button.pack(pady=10)

    def logout(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        self.controller.show_frame(LoginPage)

    def display_data(self, data):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        self.welcome_label.config(text=data["message"])
        feature_names = ['Mean Hold', 'Std Hold', 'Mean Flight', 'Std Flight', 'Duration']
        self.plot_signature(data["stored_vector"], data["login_vector"], feature_names)

    def plot_signature(self, stored_vector, login_vector, feature_names):
        combined = np.vstack([stored_vector, login_vector])
        min_vals, max_vals = combined.min(axis=0), combined.max(axis=0)
        range_vals = max_vals - min_vals
        range_vals[range_vals == 0] = 1
        normalized = (combined - min_vals) / range_vals
        stored_norm, login_norm = normalized[0], normalized[1]
        angles = np.linspace(0, 2 * np.pi, len(feature_names), endpoint=False).tolist()
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        stored_values = stored_norm.tolist() + stored_norm.tolist()[:1]
        ax.plot(angles, stored_values, 'o-', color='blue', linewidth=2, label='Stored Profile')
        ax.fill(angles, stored_values, color='blue', alpha=0.25)
        login_values = login_norm.tolist() + login_norm.tolist()[:1]
        ax.plot(angles, login_values, 'o-', color='green', linewidth=2, label='Current Login')
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(feature_names, size=8)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# --- Run the Application ---
if __name__ == "__main__":
    app = PatternAuthApp()
    app.mainloop()