"""
NyumbaFind – Free House Hunting Platform

Fully free and open platform to find homes in Nairobi.
No payments, no featured listings, no premium features.

Run: python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, os, uuid
from werkzeug.utils import secure_filename
from datetime import datetime

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

app = Flask(__name__)
CORS(app)

# ── CONFIG ──────────────────────────────────────────────────────
UPLOAD_FOLDER      = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
DB_PATH            = 'nyumbafind.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16 MB


# ── DATABASE ────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        # Core listings table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                area            TEXT    NOT NULL,
                location        TEXT,
                size            TEXT    NOT NULL,
                price           INTEGER NOT NULL,
                phone           TEXT    NOT NULL,
                image           TEXT,
                active          INTEGER DEFAULT 1,
                created         TEXT    DEFAULT (datetime('now'))
            )""")

        # Add location column if it doesn't exist (for existing databases)
        try:
            conn.execute("ALTER TABLE listings ADD COLUMN location TEXT")
        except:
            pass

        conn.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── PRICE RANGES ────────────────────────────────────────────────
PRICE_RANGES = {
    '5000-7000':   (5000,  7000),
    '8000-10000':  (8000,  10000),
    '10000-15000': (10000, 15000),
    '15000-20000': (15000, 20000),
}


# ── HELPERS ─────────────────────────────────────────────────────
def save_upload(file, folder):
    """Save an uploaded file with a UUID name. Returns the filename."""
    if file and allowed_file(file.filename):
        ext  = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        name = f"{uuid.uuid4().hex}.{ext}"
        file.save(os.path.join(folder, name))
        return name
    return None


# ── STATIC FILES ────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ════════════════════════════════════════════════════════════════
# LISTINGS API – Completely Free Platform
# ════════════════════════════════════════════════════════════════

@app.route('/api/listings', methods=['GET'])
def get_listings():
    """
    Query listings with optional filtering.
    Params: type = price | area | size
            value = selected filter value
    """
    ftype  = request.args.get('type', '')
    fvalue = request.args.get('value', '')

    query  = "SELECT * FROM listings WHERE active=1"
    params = []

    if ftype == 'price' and fvalue in PRICE_RANGES:
        lo, hi  = PRICE_RANGES[fvalue]
        query  += " AND price BETWEEN ? AND ?"
        params += [lo, hi]
    elif ftype == 'area':
        query  += " AND area = ?"
        params += [fvalue]
    elif ftype == 'size':
        query  += " AND size = ?"
        params += [fvalue]

    # Sort by newest first, no featured tier
    query += " ORDER BY created DESC LIMIT 50"

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()

    return jsonify({'success': True, 'listings': [dict(r) for r in rows]})


@app.route('/api/listings', methods=['POST'])
def add_listing():
    """
    Create a new FREE listing. No limits, no payments, no verification required.
    Form fields: area, size, price, phone, location, image (file)
    """
    area     = request.form.get('area', '').strip()
    location = request.form.get('location', '').strip()
    size     = request.form.get('size', '').strip()
    price    = request.form.get('price', '').strip()
    phone    = request.form.get('phone', '').strip()

    if not all([area, size, price, phone, location]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    try:
        price = int(price)
    except ValueError:
        return jsonify({'success': False, 'message': 'Price must be a number'}), 400

    image_name = save_upload(request.files.get('image'), UPLOAD_FOLDER)

    with get_db() as conn:
        conn.execute(
            """INSERT INTO listings (area, location, size, price, phone, image)
               VALUES (?,?,?,?,?,?)""",
            (area, location, size, price, phone, image_name)
        )
        conn.commit()

    return jsonify({'success': True, 'message': 'Listing added successfully'})


@app.route('/api/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    with get_db() as conn:
        conn.execute("UPDATE listings SET active=0 WHERE id=?", (listing_id,))
        conn.commit()
    return jsonify({'success': True})


@app.route('/api/my-listings-count')
def my_listings_count():
    with get_db() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM listings WHERE active=1"
        ).fetchone()[0]
    return jsonify({'success': True, 'count': count})


# ── SEED DATA ────────────────────────────────────────────────────
def seed_demo_data():
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
        if count == 0:
            samples = [
                ('Kahawa Wendani',       'Single Room', 6000,  '+254712345678', None),
                ('Kahawa Sukari',        'Bedsitter',   6500,  '+254723456789', None),
                ('Kenyatta Market Area', 'Studio',       9000,  '+254734567890', None),
                ('Kahawa Garrison',      '1 Bedroom',   10000, '+254745678901', None),
                ('Kahawa Wendani',       '2 Bedroom',   13000, '+254756789012', None),
                ('Kahawa Sukari',        '3 Bedroom',   17000, '+254767890123', None),
                ('Kenyatta Market Area', 'Bedsitter',    5500,  '+254778901234', None),
                ('Kahawa Garrison',      'Single Room',  5000,  '+254789012345', None),
            ]
            conn.executemany(
                "INSERT INTO listings (area,size,price,phone,image) VALUES(?,?,?,?,?)",
                samples
            )
            conn.commit()
            print("Demo listings seeded.")


# ── MAIN ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    seed_demo_data()
    print("🏠 NyumbaFind - Free House Hunting Platform running at http://127.0.0.1:5000")
    print("   100% Free • No Payments • No Premium Features")
    app.run(debug=True, use_reloader=False)
