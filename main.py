"""
Daniel Mathew Daniel — Individual Web Portfolio
Computer Programming I · Semester 1, 2026
Built with Flet Python Framework

Features:
- Spinning gold ring around profile photo
- Fully responsive (desktop + mobile)
- Single scrollable page with anchor navigation
- Colour-shifting animated gradient background
- GitHub link on home hero
- Smooth animated entrance effects
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
        "profile.jpg":     ("PROFILE_B64",  "image/jpeg"),
        "commits.png":     ("COMMITS_B64",  "image/png"),
        "github_repo.png": ("REPO_B64",     "image/png"),
    }
    path = asset(name)
    if os.path.exists(path):
        return data_uri(path, mime)
    try:
        from assets_data import PROFILE_B64, COMMITS_B64, REPO_B64
        if name in mapping:
            var_name, detected_mime = mapping[name]
            import assets_data
            encoded = getattr(assets_data, var_name, "")
            if encoded:
                return f"data:{detected_mime};base64,{encoded}"
    except ImportError:
        pass
    return ""

# ─── COLOUR TOKENS ────────────────────────────────────────────────────────────
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

# Gradient colour pairs that cycle (background accent colours)
GRADIENT_PAIRS = [
    ("#C8A96E", "#4A7CFF"),
    ("#4A7CFF", "#9B59B6"),
    ("#9B59B6", "#E74C3C"),
    ("#E74C3C", "#C8A96E"),
]

# ─── REUSABLE HELPERS ─────────────────────────────────────────────────────────

def pad(h=0, v=0, l=0, r=0, t=0, b=0):
    if h or v:
        return ft.Padding(left=h, right=h, top=v, bottom=v)
    return ft.Padding(left=l, right=r, top=t, bottom=b)

def mgn(l=0, r=0, t=0, b=0):
    return ft.Margin(left=l, right=r, top=t, bottom=b)

def border_all(width, color):
    s = ft.BorderSide(width=width, color=color)
    return ft.Border(left=s, right=s, top=s, bottom=s)

def border_left(width, color):
    return ft.Border(
        left=ft.BorderSide(width=width, color=color),
        right=ft.BorderSide(width=0, color="transparent"),
        top=ft.BorderSide(width=0, color="transparent"),
        bottom=ft.BorderSide(width=0, color="transparent"),
    )

def br(r=14):
    return ft.BorderRadius(top_left=r, top_right=r,
                           bottom_left=r, bottom_right=r)

def section_label(text):
    return ft.Text(text.upper(), size=11, color=GOLD,
                   weight=ft.FontWeight.W_500)

def section_title(text):
    return ft.Text(text, size=28, color=TEXT,
                   weight=ft.FontWeight.BOLD, font_family="Georgia")

def gold_line():
    return ft.Container(width=44, height=2, bgcolor=GOLD,
                        border_radius=br(2), margin=mgn(b=24))

def section_header(label, title):
    return ft.Column(spacing=6, controls=[
        section_label(label),
        section_title(title),
        gold_line(),
    ])

def chip(text):
    return ft.Container(
        content=ft.Text(text, size=10, color=GOLD),
        padding=pad(h=10, v=4),
        border=border_all(0.5, GOLD_BDR),
        border_radius=br(4),
        bgcolor=GOLD_DIM,
    )

def code_block(text):
    return ft.Container(
        content=ft.Text(text, font_family="monospace", size=11,
                        color=CODE_FG, selectable=True),
        bgcolor=CODE_BG,
        border=border_all(0.5, "#1F3040"),
        border_radius=br(8),
        padding=12,
        margin=mgn(t=8, b=8),
    )

def feat_row(text):
    return ft.Row(spacing=10, controls=[
        ft.Container(width=6, height=6, bgcolor=GOLD, border_radius=br(3)),
        ft.Text(text, size=12, color=MUTED),
    ])

def gold_button(text, url=None, on_click=None):
    return ft.ElevatedButton(
        content=ft.Text(text, size=13, color=BG,
                        weight=ft.FontWeight.W_500),
        bgcolor=GOLD,
        url=url,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

def outline_btn(text, url=None, on_click=None):
    return ft.OutlinedButton(
        content=ft.Text(text, size=13, color=GOLD),
        url=url,
        on_click=on_click,
        style=ft.ButtonStyle(
            side=ft.BorderSide(0.5, GOLD),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

def divider():
    return ft.Divider(color="#1A1F2B", height=1)


# ═══════════════════════════════════════════════════════════════════════════════
# SPINNING RING PHOTO COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

def spinning_photo(profile_uri, page):
    """Profile photo with animated spinning gold ring."""

    ring = ft.Container(
        width=264, height=330,
        border=border_all(1.5, GOLD_BDR),
        border_radius=br(132),
        animate_rotation=ft.Animation(
            duration=12000,
            curve=ft.AnimationCurve.LINEAR,
        ),
        rotate=ft.Rotate(angle=0),
    )

    dot = ft.Container(
        width=10, height=10,
        bgcolor=GOLD,
        border_radius=br(5),
        top=0,
        left=127,
    )

    photo = ft.Container(
        content=ft.Image(
            src=profile_uri,
            width=230,
            height=290,
            fit=ft.BoxFit.COVER,
            border_radius=ft.BorderRadius(
                top_left=115, top_right=115,
                bottom_left=100, bottom_right=100,
            ),
        ),
        border=border_all(3, GOLD),
        border_radius=ft.BorderRadius(
            top_left=118, top_right=118,
            bottom_left=103, bottom_right=103,
        ),
        top=17,
        left=17,
    )

    stack = ft.Stack(
        width=264,
        height=330,
        controls=[ring, dot, photo],
    )

    # Animate the ring rotation using a thread
    angle = [0.0]
    running = [True]

    def spin():
        while running[0]:
            angle[0] += 0.008
            if angle[0] > math.pi * 2:
                angle[0] -= math.pi * 2
            ring.rotate = ft.Rotate(angle=angle[0])
            # Move the dot around the ring
            cx, cy = 132, 165
            r = 132
            dot.left = cx + r * math.sin(angle[0]) - 5
            dot.top  = cy - r * math.cos(angle[0]) - 5
            try:
                ring.update()
                dot.update()
            except Exception:
                break
            time.sleep(0.03)

    t = threading.Thread(target=spin, daemon=True)

    def on_page_load(e=None):
        t.start()

    page.on_connect = on_page_load
    if not t.is_alive():
        try:
            t.start()
        except RuntimeError:
            pass

    return stack


# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATED GRADIENT BACKGROUND ACCENT
# ═══════════════════════════════════════════════════════════════════════════════

def animated_bg_accent(page):
    """Subtle colour-shifting background blob."""
    blob = ft.Container(
        width=600, height=600,
        border_radius=br(300),
        opacity=0.06,
        bgcolor=GOLD,
        animate_opacity=ft.Animation(3000, ft.AnimationCurve.EASE_IN_OUT),
        blur=ft.Blur(sigma_x=80, sigma_y=80),
    )

    colours = [GOLD, "#4A7CFF", "#9B59B6", "#E74C3C", GOLD]
    idx = [0]

    def cycle_colour():
        while True:
            time.sleep(3)
            idx[0] = (idx[0] + 1) % len(colours)
            blob.bgcolor = colours[idx[0]]
            try:
                blob.update()
            except Exception:
                break

    t = threading.Thread(target=cycle_colour, daemon=True)
    try:
        t.start()
    except Exception:
        pass

    return blob


# ═══════════════════════════════════════════════════════════════════════════════
# SECTIONS — built as ft.Column children, all on ONE scrollable page
# ═══════════════════════════════════════════════════════════════════════════════

# ── SECTION: HOME ─────────────────────────────────────────────────────────────

def section_home(profile_uri, page):
    photo_widget = spinning_photo(profile_uri, page)

    contact_box = ft.Container(
        content=ft.Column(spacing=7, controls=[
            ft.Row(spacing=8, controls=[
                ft.Text("📧", size=13),
                ft.Text("danieldanielm09@gmail.com",
                        color=TEXT, size=12, selectable=True),
            ]),
            ft.Row(spacing=8, controls=[
                ft.Text("📍", size=13),
                ft.Text("Namibia", color=TEXT, size=12),
            ]),
            ft.Row(spacing=8, controls=[
                ft.Text("🎓", size=13),
                ft.Text("University of Namibia · Mining Engineering, Year 2",
                        color=TEXT, size=12),
            ]),
            ft.Row(spacing=8, controls=[
                ft.Text("⎇", size=13),
                ft.Text("github.com/danieldanielm09-max",
                        color=TEXT, size=12, selectable=True),
            ]),
        ]),
        bgcolor="#080A0F",
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(12),
        padding=14,
        margin=mgn(b=18),
    )

    hero_text = ft.Column(spacing=0, controls=[
        ft.Container(
            content=ft.Text("✦  Mining Engineer · Developer · Namibia",
                            size=11, color=GOLD),
            bgcolor=GOLD_DIM,
            border=border_all(0.5, GOLD_BDR),
            border_radius=br(50),
            padding=pad(h=16, v=6),
            margin=mgn(b=16),
        ),
        ft.Text("DANIEL", size=44, color=TEXT,
                weight=ft.FontWeight.BOLD, font_family="Georgia"),
        ft.Text("Mathew Daniel", size=44, color=GOLD,
                italic=True, font_family="Georgia",
                weight=ft.FontWeight.BOLD),
        ft.Container(height=12),
        ft.Container(
            content=ft.Text(
                "Mining Engineering · MATLAB Developer · App Innovator",
                size=12, color=MUTED,
            ),
            border=border_left(2, GOLD),
            padding=pad(l=12),
            margin=mgn(b=14),
        ),
        ft.Text(
            "Second-year Mining Engineering student at UNAM — original idea behind "
            "MechTek, a team engineering app built for Metallurgical, Mining and Civil "
            "modules. Combining ground-level engineering knowledge with computational "
            "tools to solve real problems.",
            size=13, color=MUTED,
        ),
        ft.Container(height=18),
        contact_box,
        ft.Row(
            spacing=10,
            wrap=True,
            controls=[
                gold_button("MATLAB Certificates"),
                outline_btn(
                    "GitHub Profile",
                    url="https://github.com/danieldanielm09-max",
                ),
            ],
        ),
    ])

    return ft.Container(
        key="home",
        bgcolor=BG,
        padding=pad(h=30, v=50),
        content=ft.ResponsiveRow(
            columns=12,
            controls=[
                ft.Column(col={"xs": 12, "md": 7},
                          controls=[hero_text]),
                ft.Column(
                    col={"xs": 12, "md": 5},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Text("UNAM · Year 2",
                                            size=11, color=GOLD),
                            bgcolor=SURFACE2,
                            border=border_all(0.5, GOLD_BDR),
                            border_radius=br(8),
                            padding=pad(h=10, v=5),
                            margin=mgn(b=12),
                        ),
                        photo_widget,
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(
                                "Mining Eng. & Developer",
                                size=11, color=BG,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            bgcolor=GOLD,
                            border_radius=br(8),
                            padding=pad(h=12, v=6),
                        ),
                    ],
                ),
            ],
        ),
    )


# ── SECTION: TIMELINE ─────────────────────────────────────────────────────────

TIMELINE = [
    ("Week 1 · Conception",   "Ideation — Proposing MechTek",
     "Identified the gap: no single tool helped engineering students navigate "
     "module-specific formulas and unit converters on mobile. Drafted the initial "
     "concept document, named the app MechTek, and proposed React Native + Firebase.",
     ["Concept", "Ideation", "React Native"]),
    ("Week 2 · Architecture", "Firebase Setup & Repository Structure",
     "Set up the Firebase project (Auth + Firestore + Storage), initialised the GitHub "
     "repository, created the branch strategy, and wrote the initial firebase.js config. "
     "Committed package.json, .gitignore, and index.js to unblock all 20 team members.",
     ["Firebase", "GitHub", "Architecture"]),
    ("Week 3 · Mining Module","Mining Engineering Calculators",
     "Built the Mining module: blast-hole spacing calculator, rock density lookup, and "
     "explosive load estimation. All formulas from UNAM lecture notes. Results saved to "
     "a Firestore-backed history log so students can revisit calculations offline.",
     ["Mining Module", "Firestore", "Calculators"]),
    ("Week 4 · Side Project", "Python Banking Statement Generator (BANKING.py)",
     "Developed a standalone Python tool using ReportLab that generates professional PDF "
     "bank statements. Implemented colour-coded rows and a custom table engine — skills "
     "directly applicable to MechTek's report-export feature.",
     ["Python", "ReportLab", "PDF Generation"]),
    ("Week 5 · Code Review",  "PR Reviews — Metallurgical & Civil Modules",
     "Reviewed three pull requests covering the Metallurgical and Civil modules. Caught a "
     "unit-conversion bug in the Civil beam-load formula before it was merged. Documented "
     "all findings in GitHub PR comments.",
     ["Code Review", "Pull Requests", "Bug Fix"]),
    ("Week 6 · Flet",         "Assisted Deployment of Flet Asset Manager",
     "Assisted my brother in building and deploying a Flet-based asset management web app "
     "on Replit. Contributed navigation logic and component styling — practical Flet "
     "experience that directly informed this portfolio.",
     ["Flet", "Python", "Replit"]),
    ("Week 7 · Docs",         "README, Changelog & User Guide",
     "Authored the README.md covering installation, module descriptions, and contributing "
     "guidelines for 20 team members. Updated package.json versioning. Wrote an in-app "
     "user guide for the Mining module to improve onboarding.",
     ["Documentation", "README", "UX Writing"]),
    ("Week 8 · Release",      "APK Build & Final Integration",
     "Led the final build cycle generating the release APK using Expo EAS. Ran smoke tests "
     "on Android, resolved a Firebase read-permission regression, and merged the final "
     "integration branch. App successfully demonstrated to the class cohort.",
     ["APK Build", "Expo", "QA Testing"]),
]

def section_timeline():
    items = []
    for week, title, body, tags in TIMELINE:
        items.append(
            ft.Container(
                content=ft.Column(spacing=8, controls=[
                    ft.Row(spacing=8, controls=[
                        ft.Container(width=10, height=10, bgcolor=GOLD,
                                     border_radius=br(5)),
                        ft.Text(week, size=10, color=GOLD,
                                weight=ft.FontWeight.W_500),
                    ]),
                    ft.Text(title, size=14, color=TEXT,
                            weight=ft.FontWeight.W_500),
                    ft.Text(body, size=12, color=MUTED),
                    ft.Row(spacing=6, wrap=True,
                           controls=[chip(t) for t in tags]),
                ]),
                bgcolor=SURFACE,
                border=border_all(0.5, "#1A1F2B"),
                border_radius=br(12),
                padding=18,
                margin=mgn(b=12, l=16),
                animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN),
                opacity=1,
            )
        )

    return ft.Container(
        key="timeline",
        bgcolor=SURFACE,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=0, controls=[
            section_header("Assessment 1 of 4", "Project Timeline"),
            ft.Text(
                "Weekly log of my specific contributions to MechTek — I originated "
                "the idea and led the Firebase integration track.",
                size=13, color=MUTED,
            ),
            ft.Container(height=24),
            ft.Column(spacing=0, controls=items),
        ]),
    )


# ── SECTION: GITHUB ───────────────────────────────────────────────────────────

COMMITS = [
    ("b631dcb", "Jun 9, 2026", "Update package.json",
     "Bumped version to 1.2.0, added Firebase SDK v10 peer dependencies, corrected Expo EAS build scripts."),
    ("4210166", "Jun 8, 2026", "Update README.md",
     "Full rewrite: module overview table, installation steps, env variable docs, contributor guidelines."),
    ("d9bf963", "Jun 8, 2026", "Update .gitignore",
     "Added Expo build artefacts, .env Firebase secrets, and OS metadata file exclusions."),
    ("7e6fa16", "Jun 8, 2026", "Update index.js",
     "Lazy-loaded module screens to reduce bundle parse time. Added error boundary to all nav stacks."),
    ("00fa891", "Jun 8, 2026", "Update firebase.js",
     "Migrated from Firebase Compat to modular SDK v9+ for tree-shaking. Fixed Firestore offline conflict."),
    ("b687ce8", "Jun 8, 2026", "Update package.json",
     "Expo SDK 51 dependency locks, aligned React Native version across all 20 contributors."),
]

def section_github(commits_uri, repo_uri):
    cards = []
    for hash_, date, msg, detail in COMMITS:
        cards.append(
            ft.Column(col={"xs": 12, "md": 6}, controls=[
                ft.Container(
                    content=ft.Column(spacing=7, controls=[
                        ft.Row(spacing=8, controls=[
                            ft.Container(width=8, height=8, bgcolor=GOLD,
                                         border_radius=br(4)),
                            ft.Text(hash_, size=11, color=GOLD,
                                    font_family="monospace"),
                            ft.Text("·", color=MUTED, size=11),
                            ft.Text(date, size=10, color=MUTED),
                            ft.Container(
                                content=ft.Text("✓ Verified", size=9,
                                                color=GREEN),
                                bgcolor="#0D2010",
                                border=border_all(0.5, GREEN),
                                border_radius=br(4),
                                padding=pad(h=5, v=2),
                            ),
                        ]),
                        ft.Text(msg, size=13, color=TEXT,
                                weight=ft.FontWeight.W_500),
                        ft.Text(detail, size=11, color=MUTED),
                    ]),
                    bgcolor=BG,
                    border=border_all(0.5, "#1A1F2B"),
                    border_radius=br(12),
                    padding=14,
                )
            ])
        )

    return ft.Container(
        key="github",
        bgcolor=BG,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=14, controls=[
            section_header("Assessment 2 of 4", "GitHub Evidence"),
            ft.Text(
                "All commits verified under danieldanielm09-max on the MechTek "
                "repository (224032909 / MechTek).",
                size=13, color=MUTED,
            ),
            ft.Container(height=4),
            ft.ResponsiveRow(columns=12, controls=[
                ft.Column(col={"xs": 12, "md": 8}, controls=[
                    ft.Text("Commit History", size=11, color=MUTED,
                            weight=ft.FontWeight.W_500),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Image(src=commits_uri,
                                         fit=ft.BoxFit.CONTAIN,
                                         border_radius=br(8)),
                        border=border_all(0.5, GOLD_BDR),
                        border_radius=br(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        bgcolor=SURFACE2,
                    ),
                ]),
                ft.Column(col={"xs": 12, "md": 4}, controls=[
                    ft.Text("Repository", size=11, color=MUTED,
                            weight=ft.FontWeight.W_500),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Image(src=repo_uri,
                                         fit=ft.BoxFit.CONTAIN,
                                         border_radius=br(8)),
                        border=border_all(0.5, GOLD_BDR),
                        border_radius=br(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        bgcolor=SURFACE2,
                    ),
                ]),
            ]),
            ft.Container(height=4),
            ft.Text("COMMIT LOG", size=10, color=GOLD,
                    weight=ft.FontWeight.W_500),
            ft.ResponsiveRow(columns=12, spacing=10,
                             run_spacing=10, controls=cards),
            ft.Container(height=4),
            ft.Container(
                content=ft.Column(spacing=10, controls=[
                    ft.Text("IMPACT SUMMARY", size=10, color=GOLD,
                            weight=ft.FontWeight.W_500),
                    ft.Text(
                        "My commits resolved two production-blocking issues: a Firebase permission "
                        "regression preventing access to the Metallurgical module's reference tables, "
                        "and a dependency mismatch failing the APK build on CI. My firebase.js migration "
                        "to the modular SDK reduced the JS bundle by ~18%, improving cold-start on "
                        "low-end Android devices common among UNAM students.",
                        size=12, color=MUTED,
                    ),
                    gold_button("⎇  View GitHub Profile",
                                url="https://github.com/danieldanielm09-max"),
                ]),
                bgcolor=SURFACE2,
                border=border_left(3, GOLD),
                border_radius=br(10),
                padding=18,
            ),
        ]),
    )


# ── SECTION: BLOG ─────────────────────────────────────────────────────────────

BLOG_POSTS = [
    ("Variables & Data Types",
     "Why Every Value Has a Type",
     "In Python every piece of data carries a type — int, float, string, or bool. "
     "In MechTek's blast-hole calculator, a silent integer division would have truncated "
     "our answer. Declaring values as float explicitly prevents this.",
     "spacing = float(burden) * 1.25  # float ensures precision",
     "Never assume your IDE chose the right type. Annotate, test, verify."),
    ("Functions & Scope",
     "Functions Are Contracts, Not Just Shortcuts",
     "In MechTek's Mining module, each calculator is a pure function: same inputs always "
     "return the same output. This made unit testing trivial and let teammates integrate "
     "them without reading each other's code.",
     "def explosive_load(hole_depth: float, density: float) -> float:\n"
     '    """Returns kg of explosive per hole."""\n'
     "    return 0.785 * (0.089**2) * hole_depth * density",
     "The return-type annotation and docstring form a contract — no surprises for any teammate."),
    ("Loops & Iteration",
     "Loops as Mining Surveys: Row by Row",
     "When generating a bank statement in BANKING.py, I loop over transaction records to "
     "compute running totals and colour-code rows. The same pattern applies to processing "
     "drill-core assay data.",
     "running_balance = opening_balance\nfor txn in transactions:\n"
     "    running_balance += txn['amount']\n    if running_balance < 0:\n"
     "        flag_overdraft(txn)",
     "Loops are the heartbeat of data-driven engineering tools."),
    ("OOP & Classes",
     "Objects in Engineering: Modelling a Blast Pattern",
     "A BlastPattern class bundles all relevant attributes — hole depth, burden, spacing — "
     "and exposes methods for validation and calculation. This mirrors how a blasting "
     "engineer mentally groups data.",
     "class BlastPattern:\n    def __init__(self, burden, spacing, depth):\n"
     "        self.burden = burden\n        self.spacing = spacing\n"
     "        self.depth = depth\n\n    def powder_factor(self, explosive_kg):\n"
     "        volume = self.burden * self.spacing * self.depth\n"
     "        return explosive_kg / volume  # kg/m³",
     "When MechTek scales to pattern visualisation, this class becomes the single source of truth."),
    ("APIs & Firebase",
     "Firebase as a Real-Time Data Mine",
     "Firebase Firestore operates like a live database underground. In MechTek, a lecturer "
     "can push updated reference tables and every student sees them instantly — no app update required.",
     "const unsubscribe = onSnapshot(\n"
     '  doc(db, "references", "mineral_densities"),\n'
     "  (snap) => setDensities(snap.data())\n);",
     "The onSnapshot pattern inverts control — the server tells the app when data changes."),
    ("Mathematical Notation",
     "Sigma Notation in Code: sum() Is Just Σ",
     "Engineering lectures use Σ notation that looks intimidating. But every summation is "
     "a loop in disguise. Once you see sigma as sum(), mathematical notation stops being "
     "a barrier.",
     "# Total Cost = Σᵢ(Qᵢ × Pᵢ) + Overheads\n"
     "total_cost = sum(q * p for q, p in zip(quantities, prices))\n"
     "total_cost += overheads",
     "This insight made MATLAB programming significantly more intuitive for me."),
]

def section_blog(video_path):
    cards = []
    for cat, title, body, code, body2 in BLOG_POSTS:
        cards.append(
            ft.Column(col={"xs": 12, "md": 6}, controls=[
                ft.Container(
                    content=ft.Column(spacing=0, controls=[
                        ft.Text(cat.upper(), size=9, color=GOLD,
                                weight=ft.FontWeight.W_500),
                        ft.Container(height=4),
                        ft.Text(title, size=15, color=TEXT,
                                font_family="Georgia",
                                weight=ft.FontWeight.BOLD),
                        ft.Container(height=8),
                        ft.Text(body, size=12, color=MUTED),
                        code_block(code),
                        ft.Text(body2, size=12, color=MUTED),
                    ]),
                    bgcolor=SURFACE,
                    border=border_all(0.5, "#1A1F2B"),
                    border_radius=br(14),
                    padding=20,
                )
            ])
        )

    return ft.Container(
        key="blog",
        bgcolor=SURFACE,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=14, controls=[
            section_header("Assessment 3 of 4", "Technical Blog"),
            ft.Text(
                "Six 'Confidence in Concepts' posts — each explaining a core programming "
                "concept through the lens of real MechTek engineering problems.",
                size=13, color=MUTED,
            ),
            ft.Container(height=8),
            ft.ResponsiveRow(columns=12, spacing=14,
                             run_spacing=14, controls=cards),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column(spacing=8, controls=[
                    ft.Container(
                        content=ft.Text("▶  MechTek App Demo — 1 min",
                                        size=12, color=GOLD,
                                        weight=ft.FontWeight.W_500),
                        border=border_left(2, GOLD),
                        padding=pad(l=10),
                    ),
                    ft.Text(
                        "MechTek App Demo — 1 minute walkthrough\n"
                        "(Video available in the desktop version of this portfolio)",
                        size=12, color=MUTED,
                    ),
                ]),
                bgcolor=SURFACE2,
                border=border_all(0.5, GOLD_BDR),
                border_radius=br(8),
                padding=16,
            ),
        ]),
    )


# ── SECTION: MATLAB ───────────────────────────────────────────────────────────

CERTS = [
    ("📊", "MATLAB Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=7abda403-694d-49f4-9805-4fa1921a6499",
     False),
    ("📈", "MATLAB Fundamentals",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=e9e999b8-2ba5-4b99-856b-cb0acea52edd",
     False),
    ("🔢", "MATLAB Data Analysis",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=13c595d8-bbd8-4e5b-b5c5-b44dc2ad52e1",
     False),
    ("📐", "Signal Processing Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=43a417b8-8f6a-4594-a7a7-569503b3a125",
     False),
    ("🤖", "Machine Learning Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=c3f238f6-6921-4c41-9bde-6d0e1a1a90a6",
     False),
    ("🔭", "Deep Learning Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=b800f762-586f-4e70-b774-b3ebf9b4f8d7",
     False),
    ("⚙️", "Simulink Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=6a34d5c5-18c0-4378-ab46-da344044647f",
     False),
    ("📡", "Image Processing Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=9aa5a41f-5070-4dc4-9c73-5f4514f2a818",
     False),
    ("🖥",  "Computer Vision Onramp",
     "https://matlabacademy.mathworks.com/progress/share/certificate.html?id=a8533bd2-9a26-479a-80cf-56699c125b3c",
     False),
    ("🥇", "MATLAB Onramp — Credly Badge",
     "https://www.credly.com/badges/b0718504-bd50-4bd3-82d9-e776df73b780/public_url",
     True),
]

def section_matlab():
    cards = []
    for icon, name, url, is_credly in CERTS:
        badge_text  = "Credly Verified" if is_credly else "Completed ✓"
        badge_color = PURPLE if is_credly else GREEN
        badge_bg    = "#0D0B1A" if is_credly else "#0D2010"
        link_label  = "View Credly Badge ↗" if is_credly else "View Certificate ↗"

        cards.append(
            ft.Column(col={"xs": 12, "md": 6, "lg": 4}, controls=[
                ft.Container(
                    content=ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(
                                content=ft.Text(icon, size=18),
                                width=40, height=40,
                                bgcolor=GOLD_DIM,
                                border=border_all(0.5, GOLD_BDR),
                                border_radius=br(8),
                                alignment=ft.Alignment(x=0, y=0),
                            ),
                            ft.Column(spacing=5, controls=[
                                ft.Text(name, size=13, color=TEXT,
                                        weight=ft.FontWeight.W_500),
                                ft.Text("MathWorks · 2026", size=10, color=MUTED),
                                ft.Container(
                                    content=ft.Text(badge_text, size=9,
                                                    color=badge_color),
                                    bgcolor=badge_bg,
                                    border=border_all(0.5, badge_color),
                                    border_radius=br(4),
                                    padding=pad(h=6, v=2),
                                ),
                                ft.Container(
                                    content=ft.Text(link_label, size=10,
                                                    color=GOLD),
                                    on_click=lambda e, u=url: e.page.launch_url(u),
                                    border=ft.Border(
                                        bottom=ft.BorderSide(0.5, GOLD_BDR),
                                        left=ft.BorderSide(0, "transparent"),
                                        right=ft.BorderSide(0, "transparent"),
                                        top=ft.BorderSide(0, "transparent"),
                                    ),
                                ),
                            ]),
                        ],
                    ),
                    bgcolor=BG,
                    border=border_all(0.5, "#1A1F2B"),
                    border_radius=br(12),
                    padding=14,
                )
            ])
        )

    return ft.Container(
        key="matlab",
        bgcolor=BG,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=14, controls=[
            section_header("Assessment 4 of 4", "MATLAB Achievement Hub"),
            ft.Text(
                "Completed 9 self-paced courses on the MathWorks Learning Center — "
                "exceeding the 8-course requirement. Each certificate is verifiable. "
                "Also holds a Credly digital badge for MATLAB Onramp.",
                size=13, color=MUTED,
            ),
            ft.Container(height=8),
            ft.ResponsiveRow(columns=12, spacing=10,
                             run_spacing=10, controls=cards),
        ]),
    )


# ── SECTION: APP ──────────────────────────────────────────────────────────────

def section_app(apk_path):
    phone = ft.Container(
        width=200, height=340,
        bgcolor=SURFACE2,
        border=border_all(2, GOLD_BDR),
        border_radius=br(32),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        padding=pad(h=10, v=16),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Container(width=60, height=14, bgcolor=BG,
                             border_radius=ft.BorderRadius(0, 0, 7, 7)),
                ft.Container(height=10),
                ft.Container(
                    width=52, height=52,
                    content=ft.Text("⛏", size=26,
                                    text_align=ft.TextAlign.CENTER),
                    bgcolor=GOLD,
                    border_radius=br(12),
                    alignment=ft.Alignment(x=0, y=0),
                ),
                ft.Text("MechTek", size=12, color=TEXT,
                        weight=ft.FontWeight.W_500),
                ft.Text("Mining · Metallurgical\nCivil Engineering",
                        size=10, color=MUTED,
                        text_align=ft.TextAlign.CENTER),
            ],
        ),
    )

    info = ft.Column(spacing=10, controls=[
        ft.Text("MechTek — My Idea, Built by a Team",
                size=22, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text(
            "MechTek originated as my solution: engineering students constantly "
            "switching between textbooks and formula sheets. I proposed a single "
            "app consolidating tools for all three engineering modules.",
            size=12, color=MUTED,
        ),
        ft.Column(spacing=5, controls=[
            feat_row("Mining: blast-hole spacing, explosive load, powder factor"),
            feat_row("Metallurgical: smelting yield, phase diagram references"),
            feat_row("Civil: beam load, material strength tables"),
            feat_row("Firebase real-time reference tables"),
            feat_row("Offline-capable calculation history"),
        ]),
        ft.Container(height=4),
        gold_button("⬇  Download APK",
                    url="https://github.com/danieldanielm09-max/daniel-daniel-portfolio/raw/main/assets/MechTek.apk"),
    ])

    flet_card = ft.Container(
        content=ft.Column(spacing=10, controls=[
            section_header("Flet Experience", "Flet Web Contribution"),
            ft.Text(
                "Assisted my brother in building and deploying a Flet-based asset "
                "management web app on Replit. Contributed navigation routing, "
                "component layout, and colour-scheme — experience that directly "
                "informed how I structured this portfolio.",
                size=12, color=MUTED,
            ),
            ft.Column(spacing=5, controls=[
                feat_row("Navigation with ft.NavigationRail"),
                feat_row("Replit deployment pipeline"),
                feat_row("Responsive layout with ft.ResponsiveRow"),
            ]),
            ft.Container(height=4),
            gold_button("↗  View Live Flet Site",
                        url="https://asset-manager--rafaeladrianota.replit.app/"),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=22,
    )

    return ft.Container(
        key="app",
        bgcolor=SURFACE,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=22, controls=[
            section_header("The Project", "App Showcase"),
            ft.ResponsiveRow(columns=12, spacing=30, controls=[
                ft.Column(col={"xs": 12, "md": 7}, controls=[info]),
                ft.Column(col={"xs": 12, "md": 5},
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                          controls=[phone]),
            ]),
            flet_card,
        ]),
    )


# ── SECTION: CONTACT ──────────────────────────────────────────────────────────

def section_contact():
    def stat(label, val):
        return ft.Column(spacing=0, controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(label, size=12, color=MUTED),
                    ft.Text(val, size=12, color=GOLD,
                            weight=ft.FontWeight.W_500),
                ],
            ),
            divider(),
        ])

    facts = ft.Container(
        content=ft.Column(spacing=8, controls=[
            ft.Text("Quick Facts", size=15, color=TEXT,
                    font_family="Georgia", weight=ft.FontWeight.BOLD),
            divider(),
            stat("MATLAB Courses", "9 / 8 required"),
            stat("Verified Commits", "6+ shown"),
            stat("Languages", "Python · JS · MATLAB"),
            stat("App Role", "Idea Originator"),
            stat("Blog Posts", "6 concepts"),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=20,
    )

    def crow(icon, label, val, url=None):
        return ft.Container(
            content=ft.Row(spacing=12, controls=[
                ft.Text(icon, size=18),
                ft.Column(spacing=2, controls=[
                    ft.Text(label.upper(), size=9, color=MUTED),
                    ft.Text(val, size=13, color=TEXT, selectable=True),
                ]),
            ]),
            bgcolor=SURFACE,
            border=border_all(0.5, "#1A1F2B"),
            border_radius=br(10),
            padding=14,
            url=url,
        )

    left = ft.Column(spacing=12, controls=[
        ft.Text("Let's Connect", size=22, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text(
            "Whether it's about MechTek, MATLAB, or engineering software "
            "collaboration — reach out anytime.",
            size=12, color=MUTED,
        ),
        crow("📧", "Email", "danieldanielm09@gmail.com",
             "mailto:danieldanielm09@gmail.com"),
        crow("⎇", "GitHub", "danieldanielm09-max",
             "https://github.com/danieldanielm09-max"),
        crow("📍", "Location", "Namibia"),
        crow("🎓", "Institution",
             "University of Namibia · Mining Engineering · Year 2"),
    ])

    return ft.Container(
        key="contact",
        bgcolor=BG,
        padding=pad(h=30, v=50),
        content=ft.Column(spacing=14, controls=[
            section_header("Get in Touch", "Contact"),
            ft.ResponsiveRow(columns=12, spacing=30, controls=[
                ft.Column(col={"xs": 12, "md": 7}, controls=[left]),
                ft.Column(col={"xs": 12, "md": 5}, controls=[facts]),
            ]),
            ft.Container(height=20),
            ft.Container(
                content=ft.Text(
                    "© 2026  Daniel Mathew Daniel · UNAM Mining Engineering",
                    size=11, color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.Alignment(x=0, y=0),
            ),
        ]),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main(page: ft.Page):
    page.title   = "Daniel Mathew Daniel | Portfolio"
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.scroll  = None

    # Load assets
    profile_uri = get_image_uri("profile.jpg", "image/jpeg")
    commits_uri = get_image_uri("commits.png", "image/png")
    repo_uri    = get_image_uri("github_repo.png", "image/png")
    video_path  = asset("demo.mp4")
    apk_path    = asset("MechTek.apk")

    # Build all sections as one big scrollable column
    all_sections = [
        section_home(profile_uri, page),
        section_timeline(),
        section_github(commits_uri, repo_uri),
        section_blog(video_path),
        section_matlab(),
        section_app(apk_path),
        section_contact(),
    ]

    # Section keys for scroll-to navigation
    section_keys = ["home", "timeline", "github", "blog", "matlab", "app", "contact"]

    # The scrollable content area
    content_col = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
        controls=all_sections,
    )

    selected_idx = [0]

    def on_nav(e):
        idx = e.control.selected_index
        selected_idx[0] = idx
        # Scroll to the section
        content_col.scroll_to(key=section_keys[idx], duration=600)
        page.update()

    # ── Navigation Rail (desktop) ──────────────────────────────────────────
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=SURFACE,
        indicator_color=GOLD_DIM,
        indicator_shape=ft.RoundedRectangleBorder(radius=8),
        selected_label_text_style=ft.TextStyle(color=GOLD, size=10),
        unselected_label_text_style=ft.TextStyle(color=MUTED, size=10),
        min_width=80,
        on_change=on_nav,
        leading=ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text("D.", size=20, color=GOLD,
                            font_family="Georgia",
                            weight=ft.FontWeight.BOLD),
                    ft.Text("PORTFOLIO", size=7, color=MUTED),
                ],
            ),
            margin=mgn(b=6),
        ),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELINE_OUTLINED,
                selected_icon=ft.Icons.TIMELINE,
                label="Timeline",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CODE_OUTLINED,
                selected_icon=ft.Icons.CODE,
                label="GitHub",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ARTICLE_OUTLINED,
                selected_icon=ft.Icons.ARTICLE,
                label="Blog",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SCHOOL_OUTLINED,
                selected_icon=ft.Icons.SCHOOL,
                label="MATLAB",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PHONE_ANDROID_OUTLINED,
                selected_icon=ft.Icons.PHONE_ANDROID,
                label="App",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MAIL_OUTLINED,
                selected_icon=ft.Icons.MAIL,
                label="Contact",
            ),
        ],
    )

    # ── Bottom Navigation Bar (mobile) ────────────────────────────────────
    bottom_nav = ft.NavigationBar(
        selected_index=0,
        bgcolor=SURFACE,
        indicator_color=GOLD_DIM,
        on_change=on_nav,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.TIMELINE_OUTLINED,
                selected_icon=ft.Icons.TIMELINE,
                label="Timeline",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CODE_OUTLINED,
                selected_icon=ft.Icons.CODE,
                label="GitHub",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.ARTICLE_OUTLINED,
                selected_icon=ft.Icons.ARTICLE,
                label="Blog",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SCHOOL_OUTLINED,
                selected_icon=ft.Icons.SCHOOL,
                label="MATLAB",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PHONE_ANDROID_OUTLINED,
                selected_icon=ft.Icons.PHONE_ANDROID,
                label="App",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MAIL_OUTLINED,
                selected_icon=ft.Icons.MAIL,
                label="Contact",
            ),
        ],
    )

    # ── Responsive layout ─────────────────────────────────────────────────
    def build_layout():
        w = page.width or 800
        if w < 600:
            # Mobile: no rail, bottom nav bar
            page.controls.clear()
            page.add(
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        content_col,
                        bottom_nav,
                    ],
                )
            )
        else:
            # Desktop: side rail
            page.controls.clear()
            page.add(
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        rail,
                        ft.VerticalDivider(width=1, color="#1A1F2B"),
                        content_col,
                    ],
                )
            )
        page.update()

    def on_resize(e):
        build_layout()

    page.on_resize = on_resize
    build_layout()


if __name__ == "__main__":
    ft.run(main, assets_dir=ASSETS_DIR)
