# 🏠 NyumbaFind – VS Code Setup Guide

## What You're Getting
| File | Purpose |
|------|---------|
| `index.html` | Full frontend – slideshow, search, listings grid, admin panel |
| `app.py` | Flask backend – API, SQLite database, image uploads |
| `requirements.txt` | Python dependencies |

---

## STEP 1 – Install Prerequisites

### Python (if not installed)
1. Go to https://python.org/downloads
2. Download Python 3.11+ and install it
3. ✅ Tick **"Add Python to PATH"** during install

### VS Code (if not installed)
1. Go to https://code.visualstudio.com
2. Download and install for your OS

---

## STEP 2 – Open the Project in VS Code

1. Create a folder called `nyumbafind` anywhere on your computer
2. Copy all 3 files (`index.html`, `app.py`, `requirements.txt`) into that folder
3. Open VS Code → **File → Open Folder** → select `nyumbafind`

---

## STEP 3 – Install Recommended VS Code Extensions

Open the Extensions panel (`Ctrl+Shift+X`) and install:
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- **Live Server** (by Ritwick Dey) ← lets you preview HTML instantly

---

## STEP 4 – Set Up Python Virtual Environment

Open the VS Code terminal (`Ctrl+`` ` ``):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

You should see `(venv)` appear in your terminal prompt.

---

## STEP 5 – Run the Flask Backend

In the terminal (with venv active):

```bash
python app.py
```

You should see:
```
✓ Demo listings seeded.
🏠 NyumbaFind backend running at http://127.0.0.1:5000
```

**Leave this terminal running.**

---

## STEP 6 – Open the Frontend

**Option A – Open directly in browser:**
- Right-click `index.html` → Open With → your browser

**Option B – Use Live Server (recommended):**
- Right-click `index.html` in the VS Code file explorer
- Click **"Open with Live Server"**
- Browser opens automatically at `http://127.0.0.1:5500`

---

## STEP 7 – Test the Portal

1. **Search**: Click a price range (e.g. KES 5,000–7,000) → click **Search Vacancies**
   - You'll see 8 demo listings in a 2×4 grid
   - Each card shows location + WhatsApp button

2. **Admin Login**: Click **"Caretaker Login"** (top right)
   - Username: `admin`
   - Password: `nyumba2025`
   - Upload a listing with photo, price, area, WhatsApp number

3. **WhatsApp Link**: Click **"Chat on WhatsApp"** on any card — it opens WhatsApp with a pre-filled message

---

## STEP 8 – Change Your Admin Password

Open `index.html`, find this section near the top of `<script>`:

```javascript
const ADMIN_USER = 'admin';
const ADMIN_PASS = 'nyumba2025';   // ← change this
```

Change the password to something only you know and save the file.

---

## PROJECT STRUCTURE

```
nyumbafind/
├── index.html          ← Frontend (edit this for design changes)
├── app.py              ← Backend (edit for new features)
├── requirements.txt    ← Python packages
├── nyumbafind.db       ← SQLite database (auto-created on first run)
└── uploads/            ← Uploaded images (auto-created on first run)
```

---

## DEPLOYING ONLINE (to make it public)

### Free option – PythonAnywhere
1. Go to https://www.pythonanywhere.com → sign up free
2. Upload your files
3. Set up a Flask web app pointing to `app.py`
4. Update `API_BASE` in `index.html` from `http://127.0.0.1:5000` to your live URL

### Paid option – Render.com or Railway.app
- Both support Flask apps with free tiers
- Upload your project via GitHub for easy deployment

---

## TROUBLESHOOTING

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` with venv active |
| Search shows no results | Make sure Flask is running (`python app.py`) |
| Images not showing | Check the `uploads/` folder exists in your project |
| WhatsApp not opening | Ensure phone number starts with country code e.g. `+254...` |
| Port 5000 already in use | Change `app.run(port=5001)` in `app.py` and update `API_BASE` in HTML |

---

*Built for NyumbaFind · Nairobi, Kenya*
