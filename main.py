"""
Daniel Mathew Daniel — Individual Web Portfolio
Computer Programming I · Semester 1, 2026
Built with Flet Python Framework
"""

import flet as ft
import base64
import os
import math
import threading
import time

# ─── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def asset(name):
    return os.path.join(ASSETS_DIR, name)

def b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def data_uri(path, mime="image/jpeg"):
    if not os.path.exists(path):
        return ""
    return f"data:{mime};base64,{b64(path)}"

def get_image_uri(name, mime="image/jpeg"):
    mapping = {
        "profile.jpg":      ("PROFILE_B64",  "image/jpeg"),
        "commits.png":      ("COMMITS_B64",  "image/png"),
        "github_repo.png":  ("REPO_B64",     "image/png"),
    }
    path = asset(name)
    if os.path.exists(path):
        return data_uri(path, mime)
    try:
        import assets_data
        if name in mapping:
            var_name, detected_mime = mapping[name]
            encoded = getattr(assets_data, var_name, "")
            if encoded:
                return f"data:{detected_mime};base64,{encoded}"
    except ImportError:
        pass
    return ""

# ─── COLOURS ──────────────────────────────────────────────────────────────────
BG       = "#08090C"
SURFACE  = "#0F1117"
SURFACE2 = "#161B25"
GOLD     = "#C8A96E"
GOLD_DIM = "#1A1509"
GOLD_BDR = "#3D2E1A"
MUTED    = "#7A8494"
TEXT     = "#E8EDF5"
CODE_BG  = "#0D1117"
CODE_FG  = "#7BC8F6"
GREEN    = "#3fb950"
PURPLE   = "#818cf8"

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def pad(h=0, v=0, l=0, r=0, t=0, b=0):
    if h or v:
        return ft.Padding(left=h, right=h, top=v, bottom=v)
    return ft.Padding(left=l, right=r, top=t, bottom=b)

def mgn(l=0, r=0, t=0, b=0):
    return ft.Margin(left=l, right=r, top=t, bottom=b)

def bdr(width, color):
    s = ft.BorderSide(width=width, color=color)
    return ft.Border(left=s, right=s, top=s, bottom=s)

def bdr_left(width, color):
    return ft.Border(
        left=ft.BorderSide(width=width, color=color),
        right=ft.BorderSide(width=0, color="transparent"),
        top=ft.BorderSide(width=0, color="transparent"),
        bottom=ft.BorderSide(width=0, color="transparent"),
    )

def br(r=12):
    return ft.BorderRadius(top_left=r, top_right=r,
                           bottom_left=r, bottom_right=r)

def lbl(text):
    return ft.Text(text.upper(), size=10, color=GOLD,
                   weight=ft.FontWeight.W_500)

def title(text):
    return ft.Text(text, size=26, color=TEXT,
                   weight=ft.FontWeight.BOLD, font_family="Georgia")

def gold_bar():
    return ft.Container(width=40, height=2, bgcolor=GOLD,
                        border_radius=br(2), margin=mgn(b=20))

def hdr(label, text):
    return ft.Column(spacing=5, controls=[lbl(label), title(text), gold_bar()])

def chip(text):
    return ft.Container(
        content=ft.Text(text, size=9, color=GOLD),
        padding=pad(h=8, v=3),
        border=bdr(0.5, GOLD_BDR),
        border_radius=br(4),
        bgcolor=GOLD_DIM,
    )

def code_blk(text):
    return ft.Container(
        content=ft.Text(text, font_family="monospace",
                        size=11, color=CODE_FG, selectable=True),
        bgcolor=CODE_BG,
        border=bdr(0.5, "#1F3040"),
        border_radius=br(8),
        padding=12,
        margin=mgn(t=7, b=7),
    )

def feat(text):
    return ft.Row(spacing=8, controls=[
        ft.Container(width=5, height=5, bgcolor=GOLD, border_radius=br(3)),
        ft.Text(text, size=11, color=MUTED),
    ])

def gbtn(text, url=None, on_click=None):
    return ft.ElevatedButton(
        content=ft.Text(text, size=12, color=BG,
                        weight=ft.FontWeight.W_500),
        bgcolor=GOLD, url=url, on_click=on_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

def obtn(text, url=None, on_click=None):
    return ft.OutlinedButton(
        content=ft.Text(text, size=12, color=GOLD),
        url=url, on_click=on_click,
        style=ft.ButtonStyle(
            side=ft.BorderSide(0.5, GOLD),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

def card(content, p=18):
    return ft.Container(
        content=content,
        bgcolor=SURFACE,
        border=bdr(0.5, "#1A1F2B"),
        border_radius=br(12),
        padding=p,
    )

def crow(icon, label, val, url=None):
    return ft.Container(
        content=ft.Row(spacing=10, controls=[
            ft.Text(icon, size=16),
            ft.Column(spacing=1, controls=[
                ft.Text(label.upper(), size=8, color=MUTED),
                ft.Text(val, size=12, color=TEXT, selectable=True),
            ]),
        ]),
        bgcolor=SURFACE,
        border=bdr(0.5, "#1A1F2B"),
        border_radius=br(10),
        padding=12,
        url=url,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SPINNING RING
# ═══════════════════════════════════════════════════════════════════════════════

def make_photo(profile_uri, page):
    SIZE   = 250
    RADIUS = 125

    ring = ft.Container(
        width=SIZE, height=SIZE,
        border=bdr(1.5, GOLD_BDR),
        border_radius=br(RADIUS),
        rotate=ft.Rotate(angle=0),
        animate_rotation=ft.Animation(10000, ft.AnimationCurve.LINEAR),
    )

    dot = ft.Container(
        width=9, height=9,
        bgcolor=GOLD,
        border_radius=br(5),
        left=RADIUS - 4,
        top=0,
    )

    img_size = SIZE - 20
    photo = ft.Container(
        content=ft.Image(
            src=profile_uri,
            width=img_size, height=img_size,
            fit=ft.BoxFit.COVER,
            border_radius=ft.BorderRadius(
                top_left=img_size//2, top_right=img_size//2,
                bottom_left=img_size//2 - 12, bottom_right=img_size//2 - 12,
            ),
        ),
        border=bdr(3, GOLD),
        border_radius=ft.BorderRadius(
            top_left=img_size//2 + 2, top_right=img_size//2 + 2,
            bottom_left=img_size//2 - 10, bottom_right=img_size//2 - 10,
        ),
        top=10, left=10,
    )

    stack = ft.Stack(width=SIZE, height=SIZE, controls=[ring, dot, photo])

    angle = [0.0]
    running = [True]

    def spin():
        while running[0]:
            angle[0] += 0.01
            if angle[0] > math.pi * 2:
                angle[0] -= math.pi * 2
            ring.rotate = ft.Rotate(angle=angle[0])
            dot.left = RADIUS + RADIUS * math.sin(angle[0]) - 4
            dot.top  = RADIUS - RADIUS * math.cos(angle[0]) - 4
            try:
                ring.update()
                dot.update()
            except Exception:
                break
            time.sleep(0.04)

    t = threading.Thread(target=spin, daemon=True)
    try:
        t.start()
    except RuntimeError:
        pass

    return stack


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD SECTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def build_home(profile_uri, page):
    contact_box = ft.Container(
        content=ft.Column(spacing=6, controls=[
            ft.Row(spacing=6, controls=[ft.Text("📧", size=12),
                ft.Text("danieldanielm09@gmail.com", color=TEXT, size=11, selectable=True)]),
            ft.Row(spacing=6, controls=[ft.Text("📍", size=12),
                ft.Text("Namibia", color=TEXT, size=11)]),
            ft.Row(spacing=6, controls=[ft.Text("🎓", size=12),
                ft.Text("UNAM · Mining Engineering · Year 2", color=TEXT, size=11)]),
            ft.Row(spacing=6, controls=[ft.Text("⎇", size=12),
                ft.Text("github.com/danieldanielm09-max", color=TEXT, size=11, selectable=True)]),
        ]),
        bgcolor="#080A0F",
        border=bdr(0.5, "#1A1F2B"),
        border_radius=br(10),
        padding=12,
        margin=mgn(b=14),
    )

    text_col = ft.Column(spacing=0, controls=[
        ft.Container(
            content=ft.Text("✦  Mining Engineer · Developer · Namibia",
                            size=10, color=GOLD),
            bgcolor=GOLD_DIM,
            border=bdr(0.5, GOLD_BDR),
            border_radius=br(50),
            padding=pad(h=14, v=5),
            margin=mgn(b=14),
        ),
        ft.Text("DANIEL", size=40, color=TEXT,
                weight=ft.FontWeight.BOLD, font_family="Georgia"),
        ft.Text("Mathew Daniel", size=40, color=GOLD,
                italic=True, font_family="Georgia",
                weight=ft.FontWeight.BOLD),
        ft.Container(height=10),
        ft.Container(
            content=ft.Text("Mining Engineering · MATLAB Developer · App Innovator",
                            size=11, color=MUTED),
            border=bdr_left(2, GOLD),
            padding=pad(l=10),
            margin=mgn(b=12),
        ),
        ft.Text(
            "Second-year Mining Engineering student at UNAM — original idea behind "
            "MechTek, a team app for Metallurgical, Mining and Civil modules.",
            size=12, color=MUTED,
        ),
        ft.Container(height=16),
        contact_box,
        ft.Row(spacing=8, wrap=True, controls=[
            gbtn("MATLAB Certificates"),
            obtn("GitHub Profile",
                 url="https://github.com/danieldanielm09-max"),
        ]),
    ])

    photo_col = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Container(height=10),
            ft.Container(
                content=ft.Text("UNAM · Year 2", size=10, color=GOLD),
                bgcolor=SURFACE2, border=bdr(0.5, GOLD_BDR),
                border_radius=br(8), padding=pad(h=10, v=4),
                margin=mgn(b=8),
            ),
            make_photo(profile_uri, page),
            ft.Container(
                content=ft.Text("Mining Eng. & Developer", size=10,
                                color=BG, text_align=ft.TextAlign.CENTER),
                bgcolor=GOLD, border_radius=br(8),
                padding=pad(h=10, v=5),
            ),
        ],
    )

    return ft.Container(
        bgcolor=BG, padding=pad(h=24, v=40),
        content=ft.ResponsiveRow(columns=12, controls=[
            ft.Column(col={"xs": 12, "md": 7}, controls=[text_col]),
            ft.Column(col={"xs": 12, "md": 5},
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                      controls=[photo_col]),
        ]),
    )


def build_timeline():
    ITEMS = [
        ("Week 1 · Conception", "Ideation — Proposing MechTek",
         "Identified the gap: no single tool for engineering module formulas on mobile. "
         "Drafted the concept, named the app MechTek, proposed React Native + Firebase.",
         ["Concept", "Ideation", "React Native"]),
        ("Week 2 · Architecture", "Firebase Setup & Repo Structure",
         "Set up Firebase (Auth + Firestore + Storage), initialised GitHub repo, "
         "created branch strategy, committed package.json, .gitignore, index.js.",
         ["Firebase", "GitHub", "Architecture"]),
        ("Week 3 · Mining Module", "Mining Engineering Calculators",
         "Built blast-hole spacing calculator, rock density lookup, explosive load "
         "estimation. All formulas from UNAM notes. Results saved to Firestore history.",
         ["Mining Module", "Firestore", "Calculators"]),
        ("Week 4 · Side Project", "Python Banking Statement Generator",
         "Built BANKING.py using ReportLab to generate professional PDF bank statements "
         "with colour-coded rows — skills applicable to MechTek's report-export feature.",
         ["Python", "ReportLab", "PDF"]),
        ("Week 5 · Code Review", "PR Reviews — Metallurgical & Civil",
         "Reviewed 3 PRs covering Metallurgical and Civil modules. Caught a "
         "unit-conversion bug in the Civil beam-load formula before merge.",
         ["Code Review", "Pull Requests", "Bug Fix"]),
        ("Week 6 · Flet", "Assisted Flet Asset Manager Deployment",
         "Helped my brother deploy a Flet web app on Replit. Contributed navigation "
         "logic and styling — direct practice with Flet before this portfolio.",
         ["Flet", "Python", "Replit"]),
        ("Week 7 · Docs", "README, Changelog & User Guide",
         "Authored README.md for 20 team members: installation, module descriptions, "
         "contributing guidelines, versioning updates in package.json.",
         ["Documentation", "README", "UX Writing"]),
        ("Week 8 · Release", "APK Build & Final Integration",
         "Led final build with Expo EAS. Ran Android smoke tests, resolved Firebase "
         "read-permission regression, merged final branch. App demo to class cohort.",
         ["APK Build", "Expo", "QA Testing"]),
    ]
    items = [
        ft.Container(
            content=ft.Column(spacing=6, controls=[
                ft.Row(spacing=8, controls=[
                    ft.Container(width=9, height=9, bgcolor=GOLD, border_radius=br(5)),
                    ft.Text(w, size=9, color=GOLD, weight=ft.FontWeight.W_500),
                ]),
                ft.Text(t, size=13, color=TEXT, weight=ft.FontWeight.W_500),
                ft.Text(b, size=11, color=MUTED),
                ft.Row(spacing=5, wrap=True, controls=[chip(x) for x in tags]),
            ]),
            bgcolor=SURFACE, border=bdr(0.5, "#1A1F2B"),
            border_radius=br(10), padding=16, margin=mgn(b=10, l=12),
        )
        for w, t, b, tags in ITEMS
    ]
    return ft.Container(
        bgcolor=SURFACE, padding=pad(h=24, v=40),
        content=ft.Column(spacing=0, controls=[
            hdr("Assessment 1 of 4", "Project Timeline"),
            ft.Text("Weekly log of my contributions to MechTek — I originated the idea "
                    "and led the Firebase integration track.",
                    size=12, color=MUTED),
            ft.Container(height=20),
            ft.Column(spacing=0, controls=items),
        ]),
    )


def build_github(commits_uri, repo_uri):
    COMMITS = [
        ("b631dcb", "Jun 9 2026", "Update package.json",
         "Bumped to v1.2.0, added Firebase SDK v10 peer deps, fixed Expo EAS build scripts."),
        ("4210166", "Jun 8 2026", "Update README.md",
         "Full rewrite: module table, install steps, env docs, contributor guidelines."),
        ("d9bf963", "Jun 8 2026", "Update .gitignore",
         "Added Expo artefacts, .env Firebase secrets, OS metadata exclusions."),
        ("7e6fa16", "Jun 8 2026", "Update index.js",
         "Lazy-loaded module screens, reduced bundle parse time, added error boundaries."),
        ("00fa891", "Jun 8 2026", "Update firebase.js",
         "Migrated to modular SDK v9+ for tree-shaking. Fixed Firestore offline conflict."),
        ("b687ce8", "Jun 8 2026", "Update package.json",
         "Expo SDK 51 locks, aligned React Native across 20 contributors."),
    ]
    commit_cards = [
        ft.Column(col={"xs": 12, "md": 6}, controls=[
            ft.Container(
                content=ft.Column(spacing=6, controls=[
                    ft.Row(spacing=6, controls=[
                        ft.Container(width=7, height=7, bgcolor=GOLD, border_radius=br(4)),
                        ft.Text(h, size=10, color=GOLD, font_family="monospace"),
                        ft.Text("·", color=MUTED, size=10),
                        ft.Text(d, size=9, color=MUTED),
                        ft.Container(
                            content=ft.Text("✓ Verified", size=8, color=GREEN),
                            bgcolor="#0D2010", border=bdr(0.5, GREEN),
                            border_radius=br(3), padding=pad(h=4, v=1),
                        ),
                    ]),
                    ft.Text(m, size=12, color=TEXT, weight=ft.FontWeight.W_500),
                    ft.Text(det, size=10, color=MUTED),
                ]),
                bgcolor=BG, border=bdr(0.5, "#1A1F2B"),
                border_radius=br(10), padding=12,
            )
        ])
        for h, d, m, det in COMMITS
    ]
    return ft.Container(
        bgcolor=BG, padding=pad(h=24, v=40),
        content=ft.Column(spacing=12, controls=[
            hdr("Assessment 2 of 4", "GitHub Evidence"),
            ft.Text("All commits verified under danieldanielm09-max on MechTek (224032909/MechTek).",
                    size=12, color=MUTED),
            ft.ResponsiveRow(columns=12, controls=[
                ft.Column(col={"xs": 12, "md": 8}, controls=[
                    ft.Text("Commit History", size=10, color=MUTED,
                            weight=ft.FontWeight.W_500),
                    ft.Container(height=5),
                    ft.Container(
                        content=ft.Image(src=commits_uri,
                                         fit=ft.BoxFit.CONTAIN,
                                         border_radius=br(8)),
                        border=bdr(0.5, GOLD_BDR), border_radius=br(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        bgcolor=SURFACE2,
                    ),
                ]),
                ft.Column(col={"xs": 12, "md": 4}, controls=[
                    ft.Text("Repository", size=10, color=MUTED,
                            weight=ft.FontWeight.W_500),
                    ft.Container(height=5),
                    ft.Container(
                        content=ft.Image(src=repo_uri,
                                         fit=ft.BoxFit.CONTAIN,
                                         border_radius=br(8)),
                        border=bdr(0.5, GOLD_BDR), border_radius=br(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        bgcolor=SURFACE2,
                    ),
                ]),
            ]),
            ft.Text("COMMIT LOG", size=9, color=GOLD,
                    weight=ft.FontWeight.W_500),
            ft.ResponsiveRow(columns=12, spacing=8,
                             run_spacing=8, controls=commit_cards),
            ft.Container(
                content=ft.Column(spacing=8, controls=[
                    ft.Text("IMPACT SUMMARY", size=9, color=GOLD,
                            weight=ft.FontWeight.W_500),
                    ft.Text(
                        "My commits resolved two production-blocking issues in MechTek: "
                        "a Firebase permission regression and a dependency mismatch failing "
                        "the APK build. My firebase.js migration to modular SDK reduced "
                        "the JS bundle by ~18%, improving cold-start on low-end Android devices.",
                        size=11, color=MUTED,
                    ),
                    gbtn("⎇  View GitHub Profile",
                         url="https://github.com/danieldanielm09-max"),
                ]),
                bgcolor=SURFACE2, border=bdr_left(3, GOLD),
                border_radius=br(10), padding=16,
            ),
        ]),
    )


def build_blog():
    POSTS = [
        ("Variables & Data Types", "Why Every Value Has a Type",
         "In Python every piece of data has a type. In MechTek's blast-hole calculator, "
         "a silent integer division would truncate our answer. Declaring float explicitly prevents this.",
         "spacing = float(burden) * 1.25  # float ensures precision",
         "Never assume your IDE chose the right type. Annotate, test, verify."),
        ("Functions & Scope", "Functions Are Contracts",
         "In MechTek's Mining module each calculator is a pure function: same inputs always "
         "return the same output. This made unit testing trivial across 20 contributors.",
         "def explosive_load(depth: float, density: float) -> float:\n"
         '    """Returns kg of explosive per hole."""\n'
         "    return 0.785 * (0.089**2) * depth * density",
         "The type annotation and docstring form a contract — no surprises for any teammate."),
        ("Loops & Iteration", "Loops as Mining Surveys",
         "In BANKING.py I loop over transactions to compute running totals and colour-code rows. "
         "The same pattern processes drill-core assay data.",
         "balance = opening\nfor txn in transactions:\n    balance += txn['amount']\n"
         "    if balance < 0: flag_overdraft(txn)",
         "Loops are the heartbeat of data-driven engineering tools."),
        ("OOP & Classes", "Modelling a Blast Pattern",
         "A BlastPattern class bundles all relevant attributes and exposes methods for "
         "validation and calculation — mirroring how a blasting engineer groups data.",
         "class BlastPattern:\n    def __init__(self, burden, spacing, depth):\n"
         "        self.burden = burden\n        self.spacing = spacing\n"
         "    def powder_factor(self, kg):\n"
         "        return kg / (self.burden * self.spacing * self.depth)",
         "When MechTek scales to visualisation, this class becomes the single source of truth."),
        ("APIs & Firebase", "Firebase as a Real-Time Data Mine",
         "In MechTek, a lecturer can push updated reference tables and every student sees "
         "them instantly — no app update required. The onSnapshot pattern makes this possible.",
         'const unsub = onSnapshot(\n  doc(db, "references", "densities"),\n'
         "  (snap) => setDensities(snap.data())\n);",
         "The server tells the app when data changes — efficient on a student's mobile data."),
        ("Mathematical Notation", "Sigma Notation = sum()",
         "Engineering Σ notation looks intimidating. But every summation is a loop in disguise. "
         "Once you see sigma as sum(), maths becomes code you can write immediately.",
         "# Total Cost = Σᵢ(Qᵢ × Pᵢ) + Overheads\n"
         "total = sum(q * p for q, p in zip(quantities, prices)) + overheads",
         "This insight made MATLAB programming significantly more intuitive for me."),
    ]
    cards = [
        ft.Column(col={"xs": 12, "md": 6}, controls=[
            ft.Container(
                content=ft.Column(spacing=0, controls=[
                    ft.Text(cat.upper(), size=9, color=GOLD,
                            weight=ft.FontWeight.W_500),
                    ft.Container(height=4),
                    ft.Text(t, size=14, color=TEXT,
                            font_family="Georgia", weight=ft.FontWeight.BOLD),
                    ft.Container(height=6),
                    ft.Text(b, size=11, color=MUTED),
                    code_blk(code),
                    ft.Text(b2, size=11, color=MUTED),
                ]),
                bgcolor=SURFACE, border=bdr(0.5, "#1A1F2B"),
                border_radius=br(12), padding=18,
            )
        ])
        for cat, t, b, code, b2 in POSTS
    ]
    return ft.Container(
        bgcolor=SURFACE, padding=pad(h=24, v=40),
        content=ft.Column(spacing=12, controls=[
            hdr("Assessment 3 of 4", "Technical Blog"),
            ft.Text("Six 'Confidence in Concepts' posts — core programming concepts "
                    "explained through real MechTek engineering problems.",
                    size=12, color=MUTED),
            ft.Container(height=6),
            ft.ResponsiveRow(columns=12, spacing=12,
                             run_spacing=12, controls=cards),
        ]),
    )


def build_matlab():
    CERTS = [
        ("📊", "MATLAB Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=37641ca3-4a5e-48ba-b28e-d99c6e9fff15", False),
        ("📈", "MATLAB Fundamentals",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=7abda403-694d-49f4-9805-4fa1921a6499", False),
        ("🔢", "MATLAB Data Analysis",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=e9e999b8-2ba5-4b99-856b-cb0acea52edd", False),
        ("📐", "Signal Processing Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=13c595d8-bbd8-4e5b-b5c5-b44dc2ad52e1", False),
        ("🤖", "Machine Learning Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=43a417b8-8f6a-4594-a7a7-569503b3a125", False),
        ("🔭", "Deep Learning Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=c3f238f6-6921-4c41-9bde-6d0e1a1a90a6", False),
        ("⚙️", "Simulink Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=b800f762-586f-4e70-b774-b3ebf9b4f8d7", False),
        ("📡", "Image Processing Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=6a34d5c5-18c0-4378-ab46-da344044647f", False),
        ("🖥",  "Computer Vision Onramp",
         "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=9aa5a41f-5070-4dc4-9c73-5f4514f2a818", False),
        ("🥇", "MATLAB Onramp — Credly Badge",
         "https://www.credly.com/badges/b0718504-bd50-4bd3-82d9-e776df73b780/public_url", True),
    ]
    cards = [
        ft.Column(col={"xs": 12, "md": 6, "lg": 4}, controls=[
            ft.Container(
                content=ft.Row(spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=ft.Text(ico, size=16),
                            width=38, height=38,
                            bgcolor=GOLD_DIM,
                            border=bdr(0.5, GOLD_BDR),
                            border_radius=br(8),
                            alignment=ft.Alignment(x=0, y=0),
                        ),
                        ft.Column(spacing=4, controls=[
                            ft.Text(nm, size=12, color=TEXT,
                                    weight=ft.FontWeight.W_500),
                            ft.Text("MathWorks · 2026", size=9, color=MUTED),
                            ft.Container(
                                content=ft.Text(
                                    "Credly Verified" if cred else "Completed ✓",
                                    size=8,
                                    color=PURPLE if cred else GREEN,
                                ),
                                bgcolor="#0D0B1A" if cred else "#0D2010",
                                border=bdr(0.5, PURPLE if cred else GREEN),
                                border_radius=br(3),
                                padding=pad(h=5, v=1),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text(
                                    "View Credly Badge ↗" if cred else "View Certificate ↗",
                                    size=10, color=BG,
                                ),
                                bgcolor=GOLD,
                                url=url,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=6),
                                    padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                                ),
                            ),
                        ]),
                    ],
                ),
                bgcolor=BG, border=bdr(0.5, "#1A1F2B"),
                border_radius=br(10), padding=12,
            )
        ])
        for ico, nm, url, cred in CERTS
    ]
    return ft.Container(
        bgcolor=BG, padding=pad(h=24, v=40),
        content=ft.Column(spacing=12, controls=[
            hdr("Assessment 4 of 4", "MATLAB Achievement Hub"),
            ft.Text("9 completed courses — exceeding the 8 required. "
                    "Each certificate is verifiable. Also holds a Credly badge.",
                    size=12, color=MUTED),
            ft.Container(height=6),
            ft.ResponsiveRow(columns=12, spacing=8,
                             run_spacing=8, controls=cards),
        ]),
    )


def build_app():
    phone = ft.Container(
        width=180, height=310,
        bgcolor=SURFACE2, border=bdr(2, GOLD_BDR),
        border_radius=br(28),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        padding=pad(h=8, v=14),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Container(width=50, height=12, bgcolor=BG,
                             border_radius=ft.BorderRadius(0, 0, 6, 6)),
                ft.Container(height=8),
                ft.Container(
                    width=46, height=46,
                    content=ft.Text("⛏", size=24, text_align=ft.TextAlign.CENTER),
                    bgcolor=GOLD, border_radius=br(10),
                    alignment=ft.Alignment(x=0, y=0),
                ),
                ft.Text("MechTek", size=11, color=TEXT,
                        weight=ft.FontWeight.W_500),
                ft.Text("Mining · Metallurgical\nCivil Engineering",
                        size=9, color=MUTED, text_align=ft.TextAlign.CENTER),
            ],
        ),
    )

    info = ft.Column(spacing=8, controls=[
        ft.Text("MechTek — My Idea, Built by a Team",
                size=20, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text("I proposed building a single mobile app consolidating tools "
                "for all three engineering modules — built by a 20-person team "
                "with me leading the Mining module and Firebase integration.",
                size=11, color=MUTED),
        ft.Column(spacing=4, controls=[
            feat("Mining: blast-hole spacing, explosive load, powder factor"),
            feat("Metallurgical: smelting yield, phase diagram references"),
            feat("Civil: beam load, material strength tables"),
            feat("Firebase real-time reference tables"),
            feat("Offline-capable calculation history"),
        ]),
        ft.Container(height=4),
        gbtn("⬇  Download APK",
             url="https://github.com/danieldanielm09-max/daniel-daniel-portfolio/raw/main/assets/MechTek.apk"),
    ])

    flet_card = ft.Container(
        content=ft.Column(spacing=8, controls=[
            hdr("Flet Experience", "Flet Web Contribution"),
            ft.Text("Assisted my brother deploying a Flet asset management web app on Replit. "
                    "Contributed navigation routing, component layout, and styling — "
                    "direct Flet practice that informed how I built this portfolio.",
                    size=11, color=MUTED),
            ft.Column(spacing=4, controls=[
                feat("Navigation with ft.NavigationRail"),
                feat("Replit deployment pipeline"),
                feat("Responsive layout with ft.ResponsiveRow"),
            ]),
            ft.Container(height=4),
            gbtn("↗  View Live Flet Site",
                 url="https://asset-manager--rafaeladrianota.replit.app/"),
        ]),
        bgcolor=SURFACE, border=bdr(0.5, "#1A1F2B"),
        border_radius=br(12), padding=20,
    )

    return ft.Container(
        bgcolor=SURFACE, padding=pad(h=24, v=40),
        content=ft.Column(spacing=20, controls=[
            hdr("The Project", "App Showcase"),
            ft.ResponsiveRow(columns=12, spacing=24, controls=[
                ft.Column(col={"xs": 12, "md": 7}, controls=[info]),
                ft.Column(col={"xs": 12, "md": 5},
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                          controls=[phone]),
            ]),
            flet_card,
        ]),
    )


def build_contact():
    def stat(label, val):
        return ft.Column(spacing=0, controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Text(label, size=11, color=MUTED),
                ft.Text(val, size=11, color=GOLD, weight=ft.FontWeight.W_500),
            ]),
            ft.Divider(color="#1A1F2B", height=1),
        ])

    facts = ft.Container(
        content=ft.Column(spacing=7, controls=[
            ft.Text("Quick Facts", size=14, color=TEXT,
                    font_family="Georgia", weight=ft.FontWeight.BOLD),
            ft.Divider(color="#1A1F2B", height=1),
            stat("MATLAB Courses",   "9 / 8 required"),
            stat("Verified Commits", "6+ shown"),
            stat("Languages",        "Python · JS · MATLAB"),
            stat("App Role",         "Idea Originator"),
            stat("Blog Posts",       "6 concepts"),
        ]),
        bgcolor=SURFACE, border=bdr(0.5, "#1A1F2B"),
        border_radius=br(12), padding=18,
    )

    left = ft.Column(spacing=10, controls=[
        ft.Text("Let's Connect", size=20, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text("Whether it's about MechTek, MATLAB, or engineering software "
                "collaboration — reach out anytime.",
                size=11, color=MUTED),
        crow("📧", "Email", "danieldanielm09@gmail.com",
             "mailto:danieldanielm09@gmail.com"),
        crow("⎇",  "GitHub", "danieldanielm09-max",
             "https://github.com/danieldanielm09-max"),
        crow("📍", "Location", "Namibia"),
        crow("🎓", "Institution", "UNAM · Mining Engineering · Year 2"),
    ])

    return ft.Container(
        bgcolor=BG, padding=pad(h=24, v=40),
        content=ft.Column(spacing=12, controls=[
            hdr("Get in Touch", "Contact"),
            ft.ResponsiveRow(columns=12, spacing=24, controls=[
                ft.Column(col={"xs": 12, "md": 7}, controls=[left]),
                ft.Column(col={"xs": 12, "md": 5}, controls=[facts]),
            ]),
            ft.Container(height=16),
            ft.Text("© 2026  Daniel Mathew Daniel · UNAM Mining Engineering",
                    size=10, color=MUTED, text_align=ft.TextAlign.CENTER),
        ]),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

# Section keys used for scroll_to
KEYS = ["s0","s1","s2","s3","s4","s5","s6"]
LABELS = ["Home","Timeline","GitHub","Blog","MATLAB","App","Contact"]
ICONS_OFF = [
    ft.Icons.HOME_OUTLINED, ft.Icons.TIMELINE_OUTLINED,
    ft.Icons.CODE_OUTLINED, ft.Icons.ARTICLE_OUTLINED,
    ft.Icons.SCHOOL_OUTLINED, ft.Icons.PHONE_ANDROID_OUTLINED,
    ft.Icons.MAIL_OUTLINED,
]
ICONS_ON = [
    ft.Icons.HOME, ft.Icons.TIMELINE,
    ft.Icons.CODE, ft.Icons.ARTICLE,
    ft.Icons.SCHOOL, ft.Icons.PHONE_ANDROID,
    ft.Icons.MAIL,
]


def main(page: ft.Page):
    page.title      = "Daniel Mathew Daniel | Portfolio"
    page.bgcolor    = BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding    = 0
    page.scroll     = None

    # Load assets
    profile_uri = get_image_uri("profile.jpg",     "image/jpeg")
    commits_uri = get_image_uri("commits.png",     "image/png")
    repo_uri    = get_image_uri("github_repo.png", "image/png")

    # Build section containers, each with a unique key for scroll_to
    sections = [
        build_home(profile_uri, page),
        build_timeline(),
        build_github(commits_uri, repo_uri),
        build_blog(),
        build_matlab(),
        build_app(),
        build_contact(),
    ]
    # Tag each section with its scroll key
    for i, sec in enumerate(sections):
        sec.key = KEYS[i]

    # One big scrollable column — all sections stacked
    content_col = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
        controls=sections,
    )

    # ── Colour-cycling accent blob ─────────────────────────────────────────
    blob = ft.Container(
        width=500, height=500,
        border_radius=br(250),
        bgcolor=GOLD,
        opacity=0.05,
        blur=ft.Blur(sigma_x=80, sigma_y=80),
        right=-100, top=-100,
        animate_opacity=ft.Animation(2000, ft.AnimationCurve.EASE_IN_OUT),
    )

    COLOURS = [GOLD, "#4A7CFF", "#9B59B6", "#26C6DA", "#E74C3C"]
    colour_idx = [0]

    def cycle():
        while True:
            time.sleep(2.5)
            colour_idx[0] = (colour_idx[0] + 1) % len(COLOURS)
            blob.bgcolor = COLOURS[colour_idx[0]]
            try:
                blob.update()
            except Exception:
                break

    threading.Thread(target=cycle, daemon=True).start()

    # Wrap content + blob in a Stack so blob floats behind
    content_stack = ft.Stack(
        expand=True,
        controls=[blob, content_col],
    )

    # ── Navigation destinations ────────────────────────────────────────────
    nav_destinations_rail = [
        ft.NavigationRailDestination(
            icon=ICONS_OFF[i], selected_icon=ICONS_ON[i], label=LABELS[i]
        )
        for i in range(7)
    ]

    nav_destinations_bar = [
        ft.NavigationBarDestination(
            icon=ICONS_OFF[i], selected_icon=ICONS_ON[i], label=LABELS[i]
        )
        for i in range(7)
    ]

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=SURFACE,
        indicator_color=GOLD_DIM,
        indicator_shape=ft.RoundedRectangleBorder(radius=8),
        selected_label_text_style=ft.TextStyle(color=GOLD, size=9),
        unselected_label_text_style=ft.TextStyle(color=MUTED, size=9),
        min_width=75,
        destinations=nav_destinations_rail,
        leading=ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
                controls=[
                    ft.Text("D.", size=18, color=GOLD,
                            font_family="Georgia",
                            weight=ft.FontWeight.BOLD),
                    ft.Text("FOLIO", size=7, color=MUTED),
                ],
            ),
            margin=mgn(b=4),
        ),
    )

    bottom_nav = ft.NavigationBar(
        selected_index=0,
        bgcolor=SURFACE,
        indicator_color=GOLD_DIM,
        destinations=nav_destinations_bar,
    )

    def go(idx):
        rail.selected_index = idx
        bottom_nav.selected_index = idx
        content_col.scroll_to(scroll_key=KEYS[idx], duration=500)
        try:
            rail.update()
            bottom_nav.update()
        except Exception:
            pass

    def on_rail(e):
        go(e.control.selected_index)

    def on_bar(e):
        go(e.control.selected_index)

    rail.on_change       = on_rail
    bottom_nav.on_change = on_bar

    # ── Layout containers ──────────────────────────────────────────────────
    desktop_layout = ft.Row(
        expand=True, spacing=0,
        controls=[
            rail,
            ft.VerticalDivider(width=1, color="#1A1F2B"),
            content_stack,
        ],
    )

    mobile_layout = ft.Column(
        expand=True, spacing=0,
        controls=[content_stack, bottom_nav],
    )

    layout_container = ft.Container(expand=True, content=desktop_layout)

    def apply_layout():
        w = page.width or 800
        if w < 620:
            layout_container.content = mobile_layout
        else:
            layout_container.content = desktop_layout
        try:
            layout_container.update()
        except Exception:
            pass

    def on_resize(e):
        apply_layout()
        page.update()

    page.on_resize = on_resize
    page.add(layout_container)
    apply_layout()


if __name__ == "__main__":
    ft.run(main, assets_dir=ASSETS_DIR)
