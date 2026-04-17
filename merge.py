import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import time
from pygame import mixer
from time import gmtime, strftime
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# ---------------- Config ----------------
TEST_DURATION_DEFAULT = 60
DEVIATION_THRESHOLD = 120
ATTENTION_TIMEOUT = 2.0

# Blink thresholds (seconds)
MIN_BLINK_DURATION = 0.1   # 100 ms
MAX_BLINK_DURATION = 0.8   # 800 ms

# ---------------- Utils ----------------
def initializeFiles(name, age):
    with open("patientBlinkRate.txt", "w") as f:
        f.write(f"Name: {name}\nAge: {age}\n")
    with open("patientBlinkTime.txt", "w") as f:
        f.write(f"Name: {name}\nAge: {age}\n")
    with open("patientAttentionLog.txt", "w") as f:
        f.write(f"Name: {name}\nAge: {age}\n")

# ---------------- App ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ADHD Zero - Attention & Blink Analysis")
        self.geometry("1300x850")
        self.configure(bg="#0f172a")

        self.stop_flag = False
        self.running = False

        self.create_ui()

    def create_ui(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 14))
        style.configure("TButton", font=("Segoe UI", 13, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 30, "bold"), foreground="#38bdf8")

        header = ttk.Label(self, text="🧠 ADHD Zero – Attention & Blink Analysis", style="Header.TLabel")
        header.pack(pady=12)

        # -------- Top Controls --------
        top_frame = tk.Frame(self, bg="#020617", padx=20, pady=15)
        top_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(top_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(top_frame, text="Age:").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Label(top_frame, text="Duration (s):").grid(row=0, column=4, sticky="w", padx=5)

        self.entry_name = ttk.Entry(top_frame, width=18, font=("Segoe UI", 14))
        self.entry_age = ttk.Entry(top_frame, width=6, font=("Segoe UI", 14))
        self.entry_duration = ttk.Entry(top_frame, width=6, font=("Segoe UI", 14))

        self.entry_duration.insert(0, str(TEST_DURATION_DEFAULT))

        self.entry_name.grid(row=0, column=1, padx=10)
        self.entry_age.grid(row=0, column=3, padx=10)
        self.entry_duration.grid(row=0, column=5, padx=10)

        self.start_btn = ttk.Button(top_frame, text="▶ Start Test", command=self.start_test)
        self.stop_btn = ttk.Button(top_frame, text="⏹ Finish Test", command=self.stop_test)

        self.start_btn.grid(row=0, column=6, padx=15)
        self.stop_btn.grid(row=0, column=7, padx=15)

        # -------- Main Content --------
        content = tk.Frame(self, bg="#0f172a")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Camera + Status
        left_frame = tk.Frame(content, bg="#020617", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.video_label = tk.Label(left_frame, bg="black")
        self.video_label.pack(fill="both", expand=True)

        self.status_label = ttk.Label(left_frame, text="Status: Idle", font=("Segoe UI", 16, "bold"))
        self.status_label.pack(pady=12)

        # Right: Results + Graphs
        right_frame = tk.Frame(content, bg="#020617", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        title_results = tk.Label(
            right_frame, text="📊 Results", bg="#020617", fg="#e5e7eb",
            font=("Segoe UI", 20, "bold")
        )
        title_results.pack(pady=8)

        # Progress bar (Attention Gauge)
        tk.Label(
            right_frame, text="Attention Level", bg="#020617", fg="#e5e7eb",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=5)

        self.attention_var = tk.DoubleVar(value=0)

        self.attention_bar = ttk.Progressbar(
            right_frame, orient="horizontal", length=300, mode="determinate",
            maximum=100, variable=self.attention_var
        )
        self.attention_bar.pack(pady=10)

        self.attention_label = tk.Label(
            right_frame, text="0 %", bg="#020617", fg="#38bdf8",
            font=("Segoe UI", 18, "bold")
        )
        self.attention_label.pack(pady=5)

        self.result_text = tk.StringVar()
        self.result_text.set("Run a test to see results.")

        self.results_label = tk.Label(
            right_frame, textvariable=self.result_text, justify="left",
            bg="#020617", fg="#e5e7eb", font=("Segoe UI", 16)
        )
        self.results_label.pack(pady=10, anchor="w")

        # Matplotlib Figures
        self.fig1, self.ax1 = plt.subplots(figsize=(5.5, 3.0))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=right_frame)
        self.canvas1.get_tk_widget().pack(pady=10)

        self.fig2, self.ax2 = plt.subplots(figsize=(5.5, 3.0))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right_frame)
        self.canvas2.get_tk_widget().pack(pady=10)

    # -------- Control Logic --------
    def start_test(self):
        if self.running:
            return

        name = self.entry_name.get()
        age = self.entry_age.get()

        if not name or not age:
            self.status_label.config(text="Status: Please enter Name and Age")
            return

        try:
            self.test_duration = int(self.entry_duration.get())
        except:
            self.test_duration = TEST_DURATION_DEFAULT

        initializeFiles(name, age)

        self.stop_flag = False
        self.running = True
        self.status_label.config(text="Status: Running...")

        self.run_test()

    def stop_test(self):
        if self.running:
            self.stop_flag = True

    def run_test(self):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier("CustomBlinkCascade.xml")

        cap = cv2.VideoCapture(0)

        # -------- Blink State Machine --------
        blink_count = 0
        eye_state = "OPEN"
        eye_closed_start = None

        # Timing
        start_time = time.time()
        last_frame_time = start_time

        deviated_time = 0.0
        attention_status = "Focused"
        last_face_time = time.time()

        time_points = []
        deviation_points = []

        while cap.isOpened() and not self.stop_flag:
            self.update_idletasks()
            self.update()

            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            elapsed = now - start_time
            frame_delta = now - last_frame_time
            last_frame_time = now

            if elapsed >= self.test_duration:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_h, frame_w = frame.shape[:2]
            frame_center_x = frame_w // 2

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            deviated_now = False

            if len(faces) == 0:
                if now - last_face_time > ATTENTION_TIMEOUT:
                    attention_status = "Not Attentive"
                    deviated_now = True
            else:
                last_face_time = now
                (x, y, w, h) = faces[0]
                face_center_x = x + w // 2

                if abs(face_center_x - frame_center_x) > DEVIATION_THRESHOLD:
                    attention_status = "Looking Away"
                    deviated_now = True
                else:
                    attention_status = "Focused"
                    deviated_now = False

                roi_gray = gray[y:y + h, x:x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, 5)
                eyes_open_now = len(eyes) > 0

                # ---- Blink State Machine ----
                if eye_state == "OPEN":
                    if not eyes_open_now:
                        eye_state = "CLOSED"
                        eye_closed_start = now

                elif eye_state == "CLOSED":
                    if eyes_open_now:
                        blink_duration = now - eye_closed_start
                        if MIN_BLINK_DURATION <= blink_duration <= MAX_BLINK_DURATION:
                            blink_count += 1
                            with open("patientBlinkTime.txt", "a") as f:
                                f.write("Blink Detected at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
                        eye_state = "OPEN"
                        eye_closed_start = None

            if deviated_now:
                deviated_time += frame_delta

            time_points.append(elapsed)
            deviation_points.append(1 if deviated_now else 0)

            # Display frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (650, 420))
            pil_image = Image.fromarray(frame_rgb)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.video_label.configure(image=tk_image)
            self.video_label.image = tk_image

            self.status_label.config(
                text=f"Status: {attention_status} | Blinks: {blink_count} | Time Left: {int(self.test_duration - elapsed)}s"
            )

        cap.release()
        self.running = False

        total_time = min(time.time() - start_time, self.test_duration)
        focused_time = max(0.0, total_time - deviated_time)

        attention_score = max(0.0, 100.0 * (focused_time / total_time)) if total_time > 0 else 0.0

        # Update progress bar
        self.attention_var.set(attention_score)
        self.attention_label.config(text=f"{attention_score:.2f} %")

        # Update results panel
        self.result_text.set(
            f"Blink Count: {blink_count}\n"
            f"Total Time: {total_time:.2f} s\n"
            f"Focused Time: {focused_time:.2f} s\n"
            f"Deviated Time: {deviated_time:.2f} s\n"
        )

        # Plot deviation over time
        self.ax1.clear()
        self.ax1.plot(time_points, deviation_points, linewidth=2)
        self.ax1.set_title("Deviation Over Time")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("State (0=Focused, 1=Deviated)")
        self.ax1.grid(True)
        self.canvas1.draw()

        # Plot attention score
        self.ax2.clear()
        self.ax2.bar(["Attention"], [attention_score])
        self.ax2.set_ylim(0, 100)
        self.ax2.set_title("Attention Score (%)")
        self.canvas2.draw()

        self.status_label.config(text="Status: Test Finished")

# ---------------- Run ----------------
if __name__ == "__main__":
    app = App()
    app.mainloop()