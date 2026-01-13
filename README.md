<!-- README refresh -->
# 🎵 Vocal Remover (Demucs-based Web App)

A simple web-based **vocal remover** built using **Python, Flask, and Demucs**.  
This application allows users to upload an audio file and separate **vocals** and **instrumentals** using the **htdemucs** model.

---

## 🚀 Features

- Upload audio files (`.mp3`, `.wav`)
- Separate vocals and background music using **Demucs**
- Simple web interface built with **Flask**
- Automatically saves separated audio outputs
- Clean project structure (no large files committed)

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Demucs (htdemucs model)**
- **HTML (Jinja templates)**
- **Git & GitHub**

---

## 📂 Project Structure

```
vocal-remover/
│
├── app.py                  # Flask application
├── audio_separator.py      # Demucs separation logic
├── templates/
│   └── index.html          # Web UI
├── uploads/                # Uploaded audio files (ignored in git)
├── separated/              # Output files (ignored in git)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ananya-singh21/vocal-remover.git
cd vocal-remover
```

### 2️⃣ Create and activate virtual environment
```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install flask demucs
```

### 4️⃣ Run the application
```bash
python app.py
```

Open browser at:
```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. User uploads an audio file
2. Flask saves the file in `uploads/`
3. Demucs (`htdemucs`) processes the audio
4. Separated vocals & instrumentals are saved in `separated/`
5. User can access the outputs

---

## 🚧 Limitations

- Large audio files may take time to process
- Currently runs locally (not deployed)
- No progress bar for separation yet

---

## 🌱 Future Improvements

- Add progress indicator
- Deploy on cloud (Render / HuggingFace Spaces)
- Support more audio formats
- Improve UI/UX
- Add download buttons for separated tracks

---

## 👩‍💻 Author

**Ananya Singh**  
Aspiring GSoC Contributor | Interested in Open Source, AI & Backend Development

---

## 📜 License

This project is open-source and available under the **MIT License**.
