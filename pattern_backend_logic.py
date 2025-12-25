 # File: pattern_backend_logic.py
import tkinter as tk
import time
import math
import pandas as pd
import numpy as np
import os
import joblib

# --- Configuration (Unchanged) ---
TRAINING_DATA_CSV = "pattern_training_data.csv"
MODEL_FILE = "pattern_model.joblib"
USER_CREDENTIALS_CSV = "pattern_user_credentials.csv"
ENROLLMENT_SESSIONS = 5

# --- PatternCaptureWindow Class (Unchanged from previous version) ---
class PatternCaptureWindow(tk.Toplevel):
    # This entire class is the same as the last version.
    # It handles the pop-up window for drawing the pattern.
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Pattern Capture")
        self.geometry("350x400")
        self.focus_force()
        self.grab_set()

        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (350 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (400 // 2)
        self.geometry(f"+{x}+{y}")

        self.message_label = tk.Label(self, text=message, font=("Helvetica", 12), wraplength=300)
        self.message_label.pack(pady=10)
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

        self.GRID_SIZE = 3
        self.NODE_RADIUS = 25
        self.nodes = []
        self._create_grid()

        self.is_drawing = False
        self.current_pattern = []
        self.lines = []
        
        self.start_time = 0
        self.hold_times = []
        self.flight_times = []
        self.last_node_exit_time = 0
        self.current_node_enter_time = 0
        
        self.result = None
        self._bind_events()

    def _create_grid(self):
        spacing = 300 / (self.GRID_SIZE + 1)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x, y = spacing * (col + 1), spacing * (row + 1)
                node_id = row * self.GRID_SIZE + col
                self.canvas.create_oval(x - self.NODE_RADIUS, y - self.NODE_RADIUS, x + self.NODE_RADIUS, y + self.NODE_RADIUS, fill="#CCCCCC", outline="#CCCCCC", tags=f"node_{node_id}")
                self.nodes.append({'id': node_id, 'x': x, 'y': y, 'visited': False})

    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def get_node_at_pos(self, x, y):
        for node in self.nodes:
            dist = math.sqrt((node['x'] - x)**2 + (node['y'] - y)**2)
            if dist <= self.NODE_RADIUS:
                return node
        return None

    def on_mouse_down(self, event):
        self.is_drawing = True
        self.start_time = time.time()
        node = self.get_node_at_pos(event.x, event.y)
        if node:
            self.visit_node(node)

    def on_mouse_move(self, event):
        if not self.is_drawing: return
        node = self.get_node_at_pos(event.x, event.y)
        if node and not node['visited']:
            self.visit_node(node)

    def visit_node(self, node):
        if self.current_pattern:
            flight_time = time.time() - self.last_node_exit_time
            self.flight_times.append(flight_time)
            hold_time = self.last_node_exit_time - self.current_node_enter_time
            self.hold_times.append(hold_time)

        self.current_node_enter_time = time.time()
        node['visited'] = True
        self.current_pattern.append(node['id'])
        self.canvas.itemconfig(f"node_{node['id']}", fill="#77C3EC")

        if len(self.current_pattern) > 1:
            prev_node = self.nodes[self.current_pattern[-2]]
            self.canvas.create_line(prev_node['x'], prev_node['y'], node['x'], node['y'], fill="#77C3EC", width=5)
        
        self.last_node_exit_time = time.time()

    def on_mouse_up(self, event):
        if not self.is_drawing: return
        self.is_drawing = False

        if self.current_pattern:
             hold_time = time.time() - self.current_node_enter_time
             self.hold_times.append(hold_time)
        
        total_duration = time.time() - self.start_time
        self.result = {
            "pattern": self.current_pattern,
            "hold_times": self.hold_times,
            "flight_times": self.flight_times,
            "total_duration": total_duration
        }
        self.destroy()

# --- Wrapper and Feature Calculation (Unchanged) ---
def capture_pattern_in_gui(root_window, message):
    capture_window = PatternCaptureWindow(root_window, message)
    root_window.wait_window(capture_window)
    return capture_window.result

def calculate_features(pattern_data):
    if not pattern_data or not pattern_data['hold_times'] or not pattern_data['flight_times']:
        return None
    
    return {
        'mean_hold_time': np.mean(pattern_data['hold_times']),
        'std_hold_time': np.std(pattern_data['hold_times']),
        'mean_flight_time': np.mean(pattern_data['flight_times']),
        'std_flight_time': np.std(pattern_data['flight_times']),
        'total_duration': pattern_data['total_duration']
    }

# --- MODIFIED: CSV now only stores username and pattern sequence ---
def initialize_csv():
    if not os.path.exists(TRAINING_DATA_CSV):
        pd.DataFrame(columns=['mean_hold_time', 'std_hold_time', 'mean_flight_time', 'std_flight_time', 'total_duration', 'label']).to_csv(TRAINING_DATA_CSV, index=False)
    if not os.path.exists(USER_CREDENTIALS_CSV):
        # --- REMOVED 'password_hash' column ---
        pd.DataFrame(columns=['username', 'pattern_sequence']).to_csv(USER_CREDENTIALS_CSV, index=False)

# --- MODIFIED: Registration no longer uses a password ---
def register_user(username, root_window, status_label, progress_bar):
    initialize_csv()
    cred_df = pd.read_csv(USER_CREDENTIALS_CSV)
    if username in cred_df['username'].values:
        return False, "Username already exists."
    # --- REMOVED: Password length check ---
    
    all_feature_rows = []
    master_pattern = None
    
    for i in range(ENROLLMENT_SESSIONS):
        status_label.config(text=f"Processing attempt {i+1}/{ENROLLMENT_SESSIONS}...")
        progress_bar["value"] = ((i + 1) / ENROLLMENT_SESSIONS) * 100
        root_window.update_idletasks()
        
        message = f"Registration Step {i+1}/{ENROLLMENT_SESSIONS}\nPlease draw your secret pattern."
        pattern_data = capture_pattern_in_gui(root_window, message)

        if not pattern_data or len(pattern_data['pattern']) < 4:
            return False, f"Pattern too short or invalid on attempt {i+1}. Please restart."

        if i == 0:
            master_pattern = pattern_data['pattern']
        elif pattern_data['pattern'] != master_pattern:
            return False, "Patterns did not match. Please restart registration."

        features = calculate_features(pattern_data)
        features['label'] = username
        all_feature_rows.append(features)

    # --- MODIFIED: Save credentials without a password hash ---
    pattern_str = "-".join(map(str, master_pattern))
    new_cred = pd.DataFrame([{'username': username, 'pattern_sequence': pattern_str}])
    new_cred.to_csv(USER_CREDENTIALS_CSV, mode='a', header=False, index=False)
    
    # Save feature data
    pd.DataFrame(all_feature_rows).to_csv(TRAINING_DATA_CSV, mode='a', header=not os.path.exists(TRAINING_DATA_CSV), index=False)
    
    return True, "Registration successful! The model must be trained before login."

# --- MODIFIED: Login no longer uses a password ---
def login_user(username, root_window):
    initialize_csv()
    if not os.path.exists(MODEL_FILE):
        return False, {"message": "Model not trained yet."}

    try:
        cred_df = pd.read_csv(USER_CREDENTIALS_CSV)
        user_cred = cred_df[cred_df['username'] == username]
        if user_cred.empty:
            return False, {"message": "User not found (Incorrect Username)."}
        
        # --- REMOVED: Password checking logic ---
        
        stored_pattern_str = user_cred['pattern_sequence'].iloc[0]
        stored_pattern = [int(p) for p in stored_pattern_str.split('-')]

    except Exception as e:
        return False, {"message": f"Error reading user data: {e}"}

    # Immediately capture the pattern for verification
    message = "Please draw your pattern to verify your identity."
    pattern_data = capture_pattern_in_gui(root_window, message)

    if not pattern_data or pattern_data['pattern'] != stored_pattern:
        return False, {"message": "Access Denied: Incorrect pattern sequence."}

    # Pattern is correct, now check timing dynamics
    model = joblib.load(MODEL_FILE)
    login_features = calculate_features(pattern_data)
    if not login_features:
        return False, {"message": "Could not capture timing pattern."}

    feature_vector = pd.DataFrame([login_features])[['mean_hold_time', 'std_hold_time', 'mean_flight_time', 'std_flight_time', 'total_duration']]
    predicted_user = model.predict(feature_vector)[0]

    if predicted_user == username:
        training_df = pd.read_csv(TRAINING_DATA_CSV)
        user_data = training_df[training_df['label'] == username]
        stored_avg_vector = user_data[feature_vector.columns].mean().values
        
        return True, {
            "message": f"Welcome, {username}!",
            "login_vector": feature_vector.values.flatten(),
            "stored_vector": stored_avg_vector
        }
    else:
        return False, {"message": "Access Denied: Your drawing pattern does not match your profile."}