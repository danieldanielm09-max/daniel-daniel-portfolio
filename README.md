# Daniel Mathew Daniel — Individual Web Portfolio
**Computer Programming I · Semester 1, 2026**
Built with the **Flet Python Framework**

---

## Structure

```
portfolio/
├── main.py            # Flet app — all 7 sections
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── assets/
    ├── profile.jpg    # Profile photo
    ├── commits.png    # GitHub commit history screenshot
    ├── github_repo.png # Repository screenshot
    ├── demo.mp4       # MechTek app demo (60 seconds)
    └── MechTek.apk    # Android APK download
```

## Sections

| # | Section | CA Requirement |
|---|---------|----------------|
| 0 | **Home** — Hero with photo, contact details | — |
| 1 | **Project Timeline** — Weekly contribution log | Assessment 1 |
| 2 | **GitHub Evidence** — Commits, screenshots, impact summary | Assessment 2 |
| 3 | **Technical Blog** — 6 "Confidence in Concepts" posts + video | Assessment 3 |
| 4 | **MATLAB Achievement Hub** — 9 certificates + Credly badge | Assessment 4 |
| 5 | **App Showcase** — MechTek APK + Flet site contribution | — |
| 6 | **Contact** — Email, GitHub, quick facts | — |

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run as desktop app
```bash
python main.py
```

### 3. Run as web app (for deployment)
```bash
flet run --web main.py
```
or with a specific port:
```bash
flet run --web --port 8080 main.py
```

### 4. Deploy to Replit / cloud
Upload the entire `portfolio/` folder including `assets/`.  
Set the run command to:
```
python main.py
```
or for web:
```
flet run --web --port 8080 main.py
```

## Notes
- The demo video (`assets/demo.mp4`) is exactly 60 seconds, cut from the original project recording.
- All MATLAB certificate links are live and verifiable.
- The GitHub profile is **danieldanielm09-max** — all commits shown are verified.
- The MechTek APK (`assets/MechTek.apk`) is the release build from Expo EAS.
