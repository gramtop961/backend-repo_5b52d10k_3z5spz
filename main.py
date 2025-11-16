import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="KIR MAN 1 HST API", description="API untuk situs Komunitas Karya Ilmiah Remaja MAN 1 HST")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# --- Content endpoints for the site ---
SITE_CONTENT = {
    "title": "Komunitas Karya Ilmiah Remaja MAN 1 HST",
    "tagline": "Eksplorasi Sains, Menembus Galaksi Pengetahuan",
    "info": "Komunitas KIR MAN 1 Hulu Sungai Tengah (HST) adalah wadah bagi pelajar untuk bereksperimen, meneliti, dan mempublikasikan karya ilmiah. Kami berfokus pada pengembangan rasa ingin tahu, berpikir kritis, dan kolaborasi riset lintas bidang.",
    "profil": {
        "sejarah": "Didirikan oleh para pendidik dan siswa pecinta sains, KIR MAN 1 HST rutin mengikuti kompetisi, mengadakan kelas riset, dan proyek laboratorium.",
        "kegiatan": [
            "Kelas Metodologi Penelitian",
            "Eksperimen Laboratorium (Biologi, Kimia, Fisika)",
            "Pelatihan Presentasi Ilmiah",
            "Publikasi Ringkas (popular science)",
            "Pembinaan Olimpiade Sains"
        ]
    },
    "tujuan": [
        "Menumbuhkan budaya riset di kalangan pelajar",
        "Mendorong publikasi dan kompetisi ilmiah",
        "Membentuk jejaring dengan komunitas sains lainnya"
    ],
    "visi": "Menjadi komunitas pelajar yang unggul dalam riset ilmiah dan berdaya saing tingkat nasional.",
    "misi": [
        "Menyelenggarakan program riset terstruktur",
        "Menyediakan fasilitas pembelajaran dan bimbingan",
        "Membangun kultur kolaboratif dan etika ilmiah",
        "Berpartisipasi aktif di kompetisi dan konferensi",
        "Mengomunikasikan sains secara inklusif"
    ],
}

ACHIEVEMENTS = [
    {"tahun": 2024, "bidang": "Biologi (KSN-K)", "tingkat": "Kabupaten", "prestasi": "Juara 1"},
    {"tahun": 2024, "bidang": "Fisika (KSN-K)", "tingkat": "Kabupaten", "prestasi": "Juara 2"},
    {"tahun": 2023, "bidang": "Kimia (KSN-P)", "tingkat": "Provinsi", "prestasi": "Finalis"},
    {"tahun": 2023, "bidang": "Karya Tulis Ilmiah", "tingkat": "Nasional", "prestasi": "Harapan"},
]

@app.get("/api/site")
def get_site_content():
    return {"content": SITE_CONTENT}

@app.get("/api/achievements")
def get_achievements():
    return {"items": ACHIEVEMENTS}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
