# 🔐 Timing-Sensitive Pattern Lock Authentication System

A behavioral biometric authentication system that verifies users based on **how they draw a pattern**, not just the pattern shape.  
The system analyzes **timing dynamics** such as inter-node delay, stroke duration, and drawing rhythm to enhance security.

This project is developed as an **academic AIML project** demonstrating the application of machine learning in secure authentication systems.

---

## 🚀 Features
- Pattern-based authentication
- Behavioral biometric analysis
- User enrollment and training
- Machine learning–based verification
- Secure rejection even if the pattern is known
- Runs locally on localhost

---

## 🧠 Working Principle

### Enrollment Phase
- User registers with a username
- Draws the same pattern multiple times
- Timing-based features are captured automatically
- Training data is generated dynamically

### Training Phase
- Machine learning model is trained using captured timing features
- A user-specific behavioral profile is created

### Authentication Phase
- User draws the pattern once
- System compares timing behavior with the trained model
- Access is granted or denied

---

## 🛠️ Tech Stack
- Python
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Flask (local server logic)

---

## 📂 Project Structure
