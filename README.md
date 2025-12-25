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
<img width="1919" height="1034" alt="image" src="https://github.com/user-attachments/assets/ebd9cefe-2ae5-4947-af4f-651e50c11b09" />
<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/517e0ef5-25c6-41b9-b60b-eadde0172954" />
<img width="1916" height="1129" alt="image" src="https://github.com/user-attachments/assets/0e009900-ecfd-47fa-b259-fbc119710b27" />


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
