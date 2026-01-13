# 🤝 Contributing to Vocal Remover (Demucs-based Web App)

Thank you for your interest in contributing to this project!  
All kinds of contributions are welcome — from bug fixes and documentation to new features and improvements.

---

## 📌 Project Overview

This project is a **Python + Flask web application** that uses **Demucs** to separate vocals and instrumentals from audio files.  
It is designed to be **beginner-friendly**, modular, and suitable for **open-source contributions**.

---

## 🧑‍💻 How to Contribute

### 1️⃣ Fork the Repository
Click the **Fork** button on GitHub to create your own copy of the repository.

---

### 2️⃣ Clone Your Fork

```bash
git clone https://github.com/<your-username>/vocal-remover.git
cd vocal-remover
```
---
### 3️⃣ Create a Virtual Environment

```bash
python -m venv venv
```
---
### Activate it
---
## Windows
```bash
venv\Scripts\activate
```
## Linux / macOS
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
---
### 5️⃣ Create a New Branch
```bash
git checkout -b feature/your-feature-name
```

Examples:

 -feature/ui-improvement
 -fix/upload-bug
 -docs/update-readme

---
### 6️⃣ Make Your Changes

You can contribute by:

-Improving UI (HTML / CSS)
-Optimizing audio processing
-Refactoring backend code
-Improving documentation
-Fixing bugs
-Adding new features

📁 Important files:

app.py → Flask backend

audio_separator.py → Demucs logic

templates/ → Frontend HTML

uploads/ → Uploaded audio files

separated/ → Output audio files

7️⃣ Test Your Changes

Before committing:

Ensure the app runs correctly

Upload an audio file and verify output

Check console for errors

Run:

python app.py

8️⃣ Commit Your Changes

Follow clear commit messages:

git add .
git commit -m "Add feature: improve upload validation"

9️⃣ Push to Your Fork
git push origin feature/your-feature-name

🔟 Open a Pull Request

Go to the original repository

Click Compare & Pull Request

Clearly describe:

What you changed

Why it is needed

Any issues fixed (if applicable)

🧹 Code Guidelines

Follow PEP8 for Python code

Keep functions small and readable

Use meaningful variable names

Add comments where logic is complex

Avoid committing large audio files

🐛 Reporting Issues

If you find a bug:

Open an Issue

Clearly explain:

Steps to reproduce

Expected behavior

Actual behavior

Screenshots/logs (if any)

🌱 Beginner-Friendly Contributions

Good first contributions include:

Improving README or docs

UI enhancements

Code cleanup and refactoring

Adding error handling

Improving user experience

📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

💬 Need Help?

Feel free to:

Open an issue

Ask questions in discussions

Reach out via GitHub

Happy contributing! 🚀🎵
