# 🧠 ADHD Detection Based on Eye Movements During Natural Viewing

An intelligent desktop-based system developed using **Python**, **OpenCV**, and **Tkinter** to analyze user attention levels and blink behavior through webcam monitoring.

This project helps identify ADHD-related attention patterns by tracking **eye movements**, **blink frequency**, and **focus deviation** during a timed natural viewing test.

---

## 📌 Project Overview

Attention Deficit Hyperactivity Disorder (ADHD) can often be associated with irregular visual attention patterns and blinking behavior.

This system uses real-time computer vision techniques to monitor a user through a webcam and generate attention-based metrics.

The application provides:

✅ Real-time face and eye detection
✅ Blink rate analysis
✅ Looking-away / distraction detection
✅ Attention percentage score
✅ Result graphs and statistics
✅ User-friendly GUI interface

---

## 🚀 Features

* 🎥 Live webcam monitoring
* 👀 Face detection using Haar Cascade
* 👁️ Eye tracking & blink detection
* 📉 Deviation graph over time
* 📊 Final attention score (%)
* 🖥️ Interactive Tkinter GUI
* 📁 Automatic report log generation

---

## 🛠️ Technologies Used

* Python
* OpenCV
* Tkinter
* NumPy
* Matplotlib
* Pillow (PIL)
* Pygame

---

## 📂 Project Structure

```bash
ADHD-Detection-EyeMovement/
│── merge.py
│── haarcascade_frontalface_default.xml
│── CustomBlinkCascade.xml
│── patientBlinkRate.txt
│── patientBlinkTime.txt
│── patientAttentionLog.txt
│── README.md
```

---

## ⚙️ How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Saiketan123/ADHD-Detection-EyeMovement.git
cd ADHD-Detection-EyeMovement
```

### 2️⃣ Install Required Libraries

```bash
pip install opencv-python numpy matplotlib pillow pygame
```

### 3️⃣ Run Application

```bash
python merge.py
```

---

## 🧪 How It Works

1. Enter **Name**, **Age**, and **Test Duration**
2. Click **Start Test**
3. Webcam starts monitoring user
4. System tracks:

   * Face position
   * Eye open/close state
   * Attention deviation
   * Blink count
5. Final results displayed:

   * Blink Count
   * Focused Time
   * Deviated Time
   * Attention Score
   * Graphical Analysis

---

## 📊 Output Includes

* Attention Level Progress Bar
* Deviation Over Time Graph
* Final Attention Score (%)
* Blink Count Summary

---

## 🎯 Future Improvements

* Deep Learning based eye tracking
* ADHD classification using ML models
* Cloud report storage
* Multi-user dataset analysis
* Improved accuracy with dlib / MediaPipe

---

## 👨‍💻 Developed By

**Sai Ketan**
Engineering Student | Python Developer | AI Enthusiast

GitHub: https://github.com/Saiketan123

---

## ⭐ Support

If you found this project useful, please give it a **star ⭐** on GitHub.
