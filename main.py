"""
Daniel Mathew Daniel — Individual Web Portfolio
Computer Programming I · Semester 1, 2026
Built with Flet Python Framework

Sections:
  0. Home (Hero)
  1. Project Timeline
  2. GitHub Evidence
  3. Technical Blog (Confidence in Concepts + video)
  4. MATLAB Achievement Hub (9 certs + Credly)
  5. App Showcase (MechTek + Flet site)
  6. Contact
"""

import flet as ft
import base64
import os

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
    return ft.BorderRadius(top_left=r, top_right=r, bottom_left=r, bottom_right=r)

def section_label(text):
    return ft.Text(text.upper(), size=11, color=GOLD,
                   weight=ft.FontWeight.W_500)

def section_title(text):
    return ft.Text(text, size=30, color=TEXT,
                   weight=ft.FontWeight.BOLD, font_family="Georgia")

def gold_line():
    return ft.Container(width=44, height=2, bgcolor=GOLD,
                        border_radius=br(2), margin=mgn(b=28))

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

def card(content, p=22):
    return ft.Container(
        content=content,
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=p,
    )

def code_block(text):
    return ft.Container(
        content=ft.Text(text, font_family="monospace", size=12,
                        color=CODE_FG, selectable=True),
        bgcolor=CODE_BG,
        border=border_all(0.5, "#1F3040"),
        border_radius=br(8),
        padding=14,
        margin=mgn(t=10, b=10),
    )

def feat_row(text):
    return ft.Row(spacing=10, controls=[
        ft.Container(width=6, height=6, bgcolor=GOLD, border_radius=br(3)),
        ft.Text(text, size=13, color=MUTED),
    ])

def gold_button(text, url=None, on_click=None):
    return ft.ElevatedButton(
        content=ft.Text(text, size=13, color=BG, weight=ft.FontWeight.W_500),
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

def eyebrow(text):
    return ft.Container(
        content=ft.Text(text, size=11, color=GOLD),
        bgcolor=GOLD_DIM,
        border=border_all(0.5, GOLD_BDR),
        border_radius=br(50),
        padding=pad(h=16, v=6),
        margin=mgn(b=18),
    )

def contact_info_row(icon, label, val, url=None):
    return ft.Container(
        content=ft.Row(spacing=12, controls=[
            ft.Text(icon, size=20),
            ft.Column(spacing=2, controls=[
                ft.Text(label.upper(), size=10, color=MUTED),
                ft.Text(val, size=14, color=TEXT, selectable=True),
            ]),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(10),
        padding=16,
        url=url,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — HOME / HERO
# ═══════════════════════════════════════════════════════════════════════════════

def build_home(profile_uri):
    photo = ft.Container(
        content=ft.Image(
            src=profile_uri,
            width=230, height=290,
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
    )

    hero_text = ft.Column(spacing=0, controls=[
        eyebrow("✦  Mining Engineer · Developer · Namibia"),
        ft.Text("DANIEL", size=50, color=TEXT,
                weight=ft.FontWeight.BOLD, font_family="Georgia"),
        ft.Text("Mathew Daniel", size=50, color=GOLD,
                italic=True, font_family="Georgia",
                weight=ft.FontWeight.BOLD),
        ft.Container(height=14),
        ft.Container(
            content=ft.Text(
                "Mining Engineering · MATLAB Developer · App Innovator",
                size=13, color=MUTED,
            ),
            border=border_left(2, GOLD),
            padding=pad(l=12),
            margin=mgn(b=16),
        ),
        ft.Text(
            "Second-year Mining Engineering student at UNAM — original idea behind "
            "MechTek, a team engineering app built for Metallurgical, Mining and Civil "
            "modules. Combining ground-level engineering knowledge with computational "
            "tools to solve real problems.",
            size=13, color=MUTED, width=440,
        ),
        ft.Container(height=20),
        ft.Container(
            content=ft.Column(spacing=7, controls=[
                ft.Row(spacing=8, controls=[
                    ft.Text("📧", size=14),
                    ft.Text("danieldanielm09@gmail.com",
                            color=TEXT, size=13, selectable=True),
                ]),
                ft.Row(spacing=8, controls=[
                    ft.Text("📍", size=14),
                    ft.Text("Namibia", color=TEXT, size=13),
                ]),
                ft.Row(spacing=8, controls=[
                    ft.Text("🎓", size=14),
                    ft.Text("University of Namibia · Mining Engineering, Year 2",
                            color=TEXT, size=13),
                ]),
                ft.Row(spacing=8, controls=[
                    ft.Text("⎇", size=14),
                    ft.Text("github.com/danieldanielm09-max",
                            color=TEXT, size=13, selectable=True),
                ]),
            ]),
            bgcolor="#080A0F",
            border=border_all(0.5, "#1A1F2B"),
            border_radius=br(12),
            padding=16,
            margin=mgn(b=20),
        ),
        ft.Row(spacing=12, controls=[
            gold_button("MATLAB Certificates"),
            outline_btn("GitHub Evidence"),
        ]),
    ])

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        ft.Column(col={"xs": 12, "md": 7},
                                  controls=[hero_text]),
                        ft.Column(
                            col={"xs": 12, "md": 5},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(height=30),
                                ft.Container(
                                    content=ft.Text("UNAM · Year 2",
                                                    size=11, color=GOLD),
                                    bgcolor=SURFACE2,
                                    border=border_all(0.5, GOLD_BDR),
                                    border_radius=br(8),
                                    padding=pad(h=10, v=5),
                                    margin=mgn(b=12),
                                ),
                                photo,
                                ft.Container(height=12),
                                ft.Container(
                                    content=ft.Text("Mining Eng. & Developer",
                                                    size=11, color=BG,
                                                    text_align=ft.TextAlign.CENTER),
                                    bgcolor=GOLD,
                                    border_radius=br(8),
                                    padding=pad(h=12, v=6),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PROJECT TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════

TIMELINE = [
    {
        "week": "Week 1 · Project Conception",
        "title": "Ideation — Proposing MechTek to the Team",
        "body": (
            "Identified the gap: no single tool helped engineering students navigate "
            "module-specific formulas, unit converters, and reference material on mobile. "
            "Drafted the initial concept document, named the app MechTek, and presented "
            "the scope to the group. Proposed React Native + Firebase for cross-platform delivery."
        ),
        "tags": ["Concept", "Ideation", "React Native"],
    },
    {
        "week": "Week 2 · Architecture",
        "title": "Firebase Setup & Repository Structure",
        "body": (
            "Set up the Firebase project (Authentication + Firestore + Storage), initialised "
            "the GitHub repository, created the branch strategy, and wrote the initial "
            "firebase.js configuration. Committed package.json, .gitignore, and index.js "
            "scaffolding to unblock all 20 team members."
        ),
        "tags": ["Firebase", "GitHub", "Architecture"],
    },
    {
        "week": "Week 3 · Core Module — Mining",
        "title": "Mining Engineering Calculators",
        "body": (
            "Built the Mining module: blast-hole spacing calculator, rock density lookup, "
            "and explosive load estimation. All formulas derived from UNAM lecture notes. "
            "Integrated results into a Firestore-backed history log so students can revisit "
            "previous calculations offline."
        ),
        "tags": ["Mining Module", "Firestore", "Calculators"],
    },
    {
        "week": "Week 4 · Banking System Side-Project",
        "title": "Python Banking Statement Generator (BANKING.py)",
        "body": (
            "Developed a standalone Python tool using ReportLab that generates professional-grade "
            "bank statement PDFs. Implemented multi-style typography, colour-coded transaction rows, "
            "and a custom table engine — skills directly applicable to MechTek's report-export feature."
        ),
        "tags": ["Python", "ReportLab", "PDF Generation"],
    },
    {
        "week": "Week 5 · Code Review & Pull Requests",
        "title": "PR Reviews — Metallurgical & Civil Modules",
        "body": (
            "Reviewed three pull requests covering the Metallurgical (smelting yield) and Civil "
            "(beam load) modules. Caught a unit-conversion bug in the Civil beam-load formula and "
            "requested corrections before merge. Documented findings in GitHub PR comments."
        ),
        "tags": ["Code Review", "Pull Requests", "Bug Fix"],
    },
    {
        "week": "Week 6 · Flet Web Portfolio",
        "title": "Assisted Deployment of Flet Asset Manager",
        "body": (
            "Assisted my brother in building and deploying a Flet-based asset management web app "
            "on Replit (asset-manager--rafaeladrianota.replit.app). Contributed navigation logic "
            "and component styling — practical Flet experience that directly informed this portfolio."
        ),
        "tags": ["Flet", "Python", "Replit"],
    },
    {
        "week": "Week 7 · Documentation",
        "title": "Project README, Changelog & User Guide",
        "body": (
            "Authored the README.md covering installation, module descriptions, and contributing "
            "guidelines for a 20-person team. Updated package.json with correct versioning. "
            "Wrote an in-app user guide for the Mining module to improve onboarding."
        ),
        "tags": ["Documentation", "README", "UX Writing"],
    },
    {
        "week": "Week 8 · Release & APK",
        "title": "APK Build & Final Integration",
        "body": (
            "Led the final build cycle, generating the release APK using Expo's build service. "
            "Ran smoke tests on Android, resolved a Firebase read-permission regression, and "
            "merged the final integration branch. App successfully demonstrated to the class cohort."
        ),
        "tags": ["APK Build", "Expo", "QA Testing"],
    },
]


def tl_item(item):
    return ft.Container(
        content=ft.Column(spacing=8, controls=[
            ft.Row(spacing=10, controls=[
                ft.Container(width=10, height=10, bgcolor=GOLD,
                             border_radius=br(5),
                             border=border_all(2, BG)),
                ft.Text(item["week"], size=11, color=GOLD,
                        weight=ft.FontWeight.W_500),
            ]),
            ft.Text(item["title"], size=15, color=TEXT,
                    weight=ft.FontWeight.W_500),
            ft.Text(item["body"], size=13, color=MUTED),
            ft.Row(spacing=6, wrap=True,
                   controls=[chip(t) for t in item["tags"]]),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(12),
        padding=20,
        margin=mgn(b=14, l=20),
    )


def build_timeline():
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=0, controls=[
                    section_header("Assessment 1 of 4", "Project Timeline"),
                    ft.Text(
                        "A weekly log of my specific contributions to MechTek — a cross-disciplinary "
                        "engineering app serving Metallurgical, Mining, and Civil Engineering modules. "
                        "I originated the idea and led the Firebase integration track.",
                        size=14, color=MUTED,
                    ),
                    ft.Container(height=28),
                    ft.Column(spacing=0, controls=[tl_item(i) for i in TIMELINE]),
                ]),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — GITHUB EVIDENCE
# ═══════════════════════════════════════════════════════════════════════════════

COMMITS = [
    ("b631dcb", "Jun 9, 2026", "Update package.json",
     "Bumped version to 1.2.0, added missing peer dependencies for Firebase SDK v10 "
     "compatibility and corrected build scripts for Expo EAS."),
    ("4210166", "Jun 8, 2026", "Update README.md",
     "Comprehensive rewrite: added module overview table, installation steps, environment "
     "variable docs, and contributor guidelines for the 20-person team."),
    ("d9bf963", "Jun 8, 2026", "Update .gitignore",
     "Added exclusions for Expo build artefacts, .env files containing Firebase secrets, "
     "and OS-specific metadata files."),
    ("7e6fa16", "Jun 8, 2026", "Update index.js",
     "Refactored entry point to lazy-load module screens, reducing initial bundle parse time. "
     "Added error boundary wrapping all navigation stacks."),
    ("00fa891", "Jun 8, 2026", "Update firebase.js",
     "Migrated from Firebase Compat SDK to modular (v9+) API for tree-shaking. "
     "Resolved a Firestore offline persistence conflict on Android."),
    ("b687ce8", "Jun 8, 2026", "Update package.json",
     "Added Expo SDK 51 dependency locks, aligned React Native version across contributors "
     "to eliminate divergent node_modules builds on Windows/macOS."),
]


def commit_card(hash_, date, msg, detail):
    verified = ft.Container(
        content=ft.Text("Verified", size=10, color=GREEN),
        bgcolor="#0D2010",
        border=border_all(0.5, "rgba(63,185,80,0.3)"),
        border_radius=br(4),
        padding=pad(h=6, v=2),
    )
    return ft.Container(
        content=ft.Column(spacing=7, controls=[
            ft.Row(spacing=8, controls=[
                ft.Container(width=8, height=8, bgcolor=GOLD, border_radius=br(4)),
                ft.Text(hash_, size=12, color=GOLD, font_family="monospace"),
                ft.Text("·", color=MUTED, size=12),
                ft.Text(date, size=11, color=MUTED),
                verified,
            ]),
            ft.Text(msg, size=14, color=TEXT, weight=ft.FontWeight.W_500),
            ft.Text(detail, size=12, color=MUTED),
        ]),
        bgcolor=BG,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(12),
        padding=16,
    )


def build_github(commits_uri, repo_uri):
    commit_cards = [
        ft.Column(col={"xs": 12, "md": 6},
                  controls=[commit_card(h, d, m, det)])
        for h, d, m, det in COMMITS
    ]

    impact = ft.Container(
        content=ft.Column(spacing=10, controls=[
            ft.Text("IMPACT SUMMARY", size=11, color=GOLD, weight=ft.FontWeight.W_500),
            ft.Text(
                "My commits directly resolved two production-blocking issues in MechTek: "
                "a Firebase permission regression that prevented read access to the Metallurgical "
                "module's reference tables, and a dependency mismatch that caused the APK build "
                "to fail on CI. As the original app ideator and Firebase integration lead, I also "
                "authored the documentation that enabled all 20 team members to contribute without "
                "environment conflicts. My firebase.js migration to the modular SDK reduced the "
                "JavaScript bundle by ~18%, improving cold-start performance on low-end Android devices.",
                size=13, color=MUTED,
            ),
            ft.Container(height=4),
            gold_button("⎇  View GitHub Profile",
                        url="https://github.com/danieldanielm09-max"),
        ]),
        bgcolor=SURFACE2,
        border=border_left(3, GOLD),
        border_radius=br(10),
        padding=20,
    )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=16, controls=[
                    section_header("Assessment 2 of 4", "GitHub Evidence"),
                    ft.Text(
                        "All commits verified under danieldanielm09-max on the MechTek repository "
                        "(224032909 / MechTek). Screenshots confirm consistent, meaningful contributions.",
                        size=14, color=MUTED,
                    ),
                    ft.Container(height=6),
                    # Screenshots
                    ft.ResponsiveRow(columns=12, controls=[
                        ft.Column(col={"xs": 12, "md": 8}, controls=[
                            ft.Text("Commit History Screenshot", size=12, color=MUTED,
                                    weight=ft.FontWeight.W_500),
                            ft.Container(height=6),
                            ft.Container(
                                content=ft.Image(
                                    src=commits_uri,
                                    fit=ft.BoxFit.CONTAIN,
                                    border_radius=br(10),
                                ),
                                border=border_all(0.5, GOLD_BDR),
                                border_radius=br(10),
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                bgcolor=SURFACE2,
                            ),
                        ]),
                        ft.Column(col={"xs": 12, "md": 4}, controls=[
                            ft.Text("Repository", size=12, color=MUTED,
                                    weight=ft.FontWeight.W_500),
                            ft.Container(height=6),
                            ft.Container(
                                content=ft.Image(
                                    src=repo_uri,
                                    fit=ft.BoxFit.CONTAIN,
                                    border_radius=br(10),
                                ),
                                border=border_all(0.5, GOLD_BDR),
                                border_radius=br(10),
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                bgcolor=SURFACE2,
                            ),
                        ]),
                    ]),
                    ft.Container(height=6),
                    ft.Text("COMMIT LOG", size=11, color=GOLD, weight=ft.FontWeight.W_500),
                    ft.ResponsiveRow(columns=12, spacing=12,
                                     run_spacing=12, controls=commit_cards),
                    ft.Container(height=6),
                    impact,
                ]),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — TECHNICAL BLOG
# ═══════════════════════════════════════════════════════════════════════════════

BLOG_POSTS = [
    {
        "cat": "Variables & Data Types",
        "title": "Why Every Value Has a Type",
        "body": (
            "In Python, every piece of data carries a type — int, float, string, or bool. "
            "This matters enormously in engineering calculations. When I built the blast-hole "
            "spacing calculator for MechTek, a silent integer division would have truncated our "
            "answer. Declaring values as float explicitly prevents this."
        ),
        "code": "spacing = float(burden) * 1.25  # float ensures precision",
        "body2": (
            "Never assume your IDE chose the right type. Annotate, test, and verify — "
            "especially when the formula feeds a real engineering decision."
        ),
        "video": False,
    },
    {
        "cat": "Functions & Scope",
        "title": "Functions Are Contracts, Not Just Shortcuts",
        "body": (
            "A function should do exactly one thing and be predictable. In MechTek's Mining module, "
            "each calculator is a pure function: given the same inputs it always returns the same "
            "output. This made unit testing trivial and let teammates integrate them without reading "
            "each other's code."
        ),
        "code": (
            "def explosive_load(hole_depth: float, density: float) -> float:\n"
            '    """Returns kg of explosive per hole."""\n'
            "    return 0.785 * (0.089**2) * hole_depth * density"
        ),
        "body2": (
            "The return-type annotation and docstring form a contract. Any engineer on the team "
            "knows exactly what to pass in and what comes back — no surprises."
        ),
        "video": False,
    },
    {
        "cat": "Loops & Iteration",
        "title": "Loops as Mining Surveys: Row by Row",
        "body": (
            "When generating a bank statement in BANKING.py, I loop over transaction records to "
            "compute running totals and colour-code rows. The same pattern applies to processing "
            "drill-core assay data: iterate, accumulate, flag anomalies."
        ),
        "code": (
            "running_balance = opening_balance\n"
            "for txn in transactions:\n"
            "    running_balance += txn['amount']\n"
            "    if running_balance < 0:\n"
            "        flag_overdraft(txn)"
        ),
        "body2": (
            "Loops are the heartbeat of data-driven engineering tools. Understanding them deeply "
            "means understanding how software processes the real world — one record at a time."
        ),
        "video": True,
    },
    {
        "cat": "OOP & Classes",
        "title": "Objects in Engineering: Modelling a Blast Pattern",
        "body": (
            "OOP lets us model real-world entities. A BlastPattern class bundles all "
            "relevant attributes — hole depth, burden, spacing — and exposes methods for "
            "validation and calculation. This mirrors how a blasting engineer mentally groups data."
        ),
        "code": (
            "class BlastPattern:\n"
            "    def __init__(self, burden, spacing, depth):\n"
            "        self.burden  = burden\n"
            "        self.spacing = spacing\n"
            "        self.depth   = depth\n\n"
            "    def powder_factor(self, explosive_kg):\n"
            "        volume = self.burden * self.spacing * self.depth\n"
            "        return explosive_kg / volume  # kg/m³"
        ),
        "body2": (
            "When MechTek scales to include pattern visualisation, this class becomes the single "
            "source of truth — easy to extend, impossible to misuse."
        ),
        "video": False,
    },
    {
        "cat": "APIs & Firebase",
        "title": "Firebase as a Real-Time Data Mine",
        "body": (
            "Firebase Firestore operates like a live database underground: you set up listeners "
            "and data flows to you the moment it changes. In MechTek, a lecturer can push updated "
            "reference tables and every student sees them instantly — no app update required."
        ),
        "code": (
            "// Real-time listener on mineral density table\n"
            "const unsubscribe = onSnapshot(\n"
            '  doc(db, "references", "mineral_densities"),\n'
            "  (snap) => setDensities(snap.data())\n"
            ");"
        ),
        "body2": (
            "The onSnapshot pattern inverts control: the server tells the app when data changes, "
            "rather than the app polling endlessly. Resource-efficient on a student's mobile data plan."
        ),
        "video": False,
    },
    {
        "cat": "Mathematical Notation",
        "title": "Sigma Notation in Code: sum() Is Just Σ",
        "body": (
            "Engineering lectures use Σ (sigma) notation that can look intimidating. "
            "But every summation is a loop in disguise. The total project cost formula "
            "below illustrates the direct translation from maths to Python:"
        ),
        "code": (
            "# Total Cost = Σᵢ(Qᵢ × Pᵢ) + Overheads\n"
            "total_cost = sum(q * p for q, p in zip(quantities, prices))\n"
            "total_cost += overheads"
        ),
        "body2": (
            "Once you see sigma as sum(), mathematical notation stops being a barrier and "
            "becomes precise shorthand you can code immediately. This insight made MATLAB "
            "programming significantly more intuitive."
        ),
        "video": False,
    },
]


def blog_card(post, video_path=None):
    items = [
        ft.Text(post["cat"].upper(), size=10, color=GOLD, weight=ft.FontWeight.W_500),
        ft.Container(height=4),
        ft.Text(post["title"], size=16, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Container(height=8),
        ft.Text(post["body"], size=13, color=MUTED),
        code_block(post["code"]),
        ft.Text(post["body2"], size=13, color=MUTED),
    ]

    if post.get("video") and video_path:
        items += [
            ft.Container(height=14),
            ft.Container(
                content=ft.Text("▶  MechTek App Demo — 1 min",
                                size=12, color=GOLD,
                                weight=ft.FontWeight.W_500),
                border=border_left(2, GOLD),
                padding=pad(l=10),
                margin=mgn(b=8),
            ),
            ft.Container(
                content=ft.Text(
                    "MechTek App Demo — 1 minute walkthrough\n"
                    "(Video available in the desktop version)",
                    size=12, color=MUTED, selectable=True,
                ),
                bgcolor=SURFACE2,
                border=border_all(0.5, GOLD_BDR),
                border_radius=br(8),
                padding=14,
            ),
        ]

    return ft.Container(
        content=ft.Column(spacing=0, controls=items),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=22,
    )


def build_blog(video_path):
    cards = [
        ft.Column(col={"xs": 12, "md": 6},
                  controls=[blog_card(p, video_path)])
        for p in BLOG_POSTS
    ]
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=16, controls=[
                    section_header("Assessment 3 of 4", "Technical Blog"),
                    ft.Text(
                        "Six 'Confidence in Concepts' posts — each explaining a core programming "
                        "concept through the lens of real MechTek engineering problems.",
                        size=14, color=MUTED,
                    ),
                    ft.Container(height=8),
                    ft.ResponsiveRow(columns=12, spacing=16,
                                     run_spacing=16, controls=cards),
                ]),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MATLAB ACHIEVEMENT HUB
# ═══════════════════════════════════════════════════════════════════════════════

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


def cert_card(icon, name, url, is_credly):
    badge_text  = "Credly Verified" if is_credly else "Completed"
    badge_color = PURPLE if is_credly else GREEN
    badge_bg    = "#0D0B1A" if is_credly else "#0D2010"
    link_label  = "View Credly Badge ↗" if is_credly else "View Certificate ↗"

    return ft.Container(
        content=ft.Row(spacing=12, vertical_alignment=ft.CrossAxisAlignment.START,
                       controls=[
            ft.Container(
                content=ft.Text(icon, size=18),
                width=42, height=42,
                bgcolor=GOLD_DIM,
                border=border_all(0.5, GOLD_BDR),
                border_radius=br(8),
                alignment=ft.Alignment(x=0, y=0),
            ),
            ft.Column(spacing=5, controls=[
                ft.Text(name, size=14, color=TEXT, weight=ft.FontWeight.W_500),
                ft.Text("MathWorks Learning Center · 2026",
                        size=11, color=MUTED),
                ft.Container(
                    content=ft.Text(badge_text, size=10, color=badge_color),
                    bgcolor=badge_bg,
                    border=border_all(0.5, badge_color),
                    border_radius=br(4),
                    padding=pad(h=7, v=2),
                ),
                ft.Container(
                    content=ft.Text(link_label, size=11, color=GOLD),
                    on_click=lambda e, u=url: e.page.launch_url(u),
                    border=ft.Border(
                        bottom=ft.BorderSide(width=0.5, color=GOLD_BDR),
                        left=ft.BorderSide(width=0, color="transparent"),
                        right=ft.BorderSide(width=0, color="transparent"),
                        top=ft.BorderSide(width=0, color="transparent"),
                    ),
                ),
            ]),
        ]),
        bgcolor=BG,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(12),
        padding=16,
    )


def build_matlab():
    cards = [
        ft.Column(col={"xs": 12, "md": 6, "lg": 4},
                  controls=[cert_card(ico, nm, url, cred)])
        for ico, nm, url, cred in CERTS
    ]
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=16, controls=[
                    section_header("Assessment 4 of 4", "MATLAB Achievement Hub"),
                    ft.Text(
                        "Completed 9 self-paced courses on the MathWorks Learning Center — "
                        "exceeding the 8-course requirement. Each certificate is directly verifiable "
                        "via the link. Also holds a Credly digital badge for MATLAB Onramp.",
                        size=14, color=MUTED,
                    ),
                    ft.Container(height=8),
                    ft.ResponsiveRow(columns=12, spacing=12,
                                     run_spacing=12, controls=cards),
                ]),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — APP SHOWCASE
# ═══════════════════════════════════════════════════════════════════════════════

def build_app(apk_path):
    phone = ft.Container(
        width=210,
        height=360,
        bgcolor=SURFACE2,
        border=border_all(2, GOLD_BDR),
        border_radius=br(34),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        padding=pad(h=10, v=20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Container(
                    width=70, height=18,
                    bgcolor=BG,
                    border_radius=ft.BorderRadius(
                        top_left=0, top_right=0,
                        bottom_left=9, bottom_right=9,
                    ),
                ),
                ft.Container(height=20),
                ft.Container(
                    width=56, height=56,
                    content=ft.Text("⛏", size=28,
                                    text_align=ft.TextAlign.CENTER),
                    bgcolor=GOLD,
                    border_radius=br(14),
                    alignment=ft.Alignment(x=0, y=0),
                ),
                ft.Text("MechTek", size=13, color=TEXT,
                        weight=ft.FontWeight.W_500),
                ft.Text(
                    "Mining · Metallurgical · Civil\nEngineering Reference App",
                    size=11, color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    app_info = ft.Column(spacing=12, controls=[
        ft.Text("MechTek — My Idea, Built by a Team",
                size=26, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text(
            "MechTek originated as my solution to a real problem: engineering students "
            "constantly switching between textbooks, formula sheets, and unit converters. "
            "I proposed building a single mobile app consolidating tools for Metallurgical, "
            "Mining, and Civil modules.",
            size=13, color=MUTED,
        ),
        ft.Text(
            "Built with React Native and Firebase by a 20-person team, with me leading "
            "the Mining module and Firebase integration. Available on Android.",
            size=13, color=MUTED,
        ),
        ft.Column(spacing=6, controls=[
            feat_row("Mining: blast-hole spacing, explosive load, powder factor"),
            feat_row("Metallurgical: smelting yield, phase diagram references"),
            feat_row("Civil: beam load, material strength tables"),
            feat_row("Firebase real-time reference tables — no app update needed"),
            feat_row("Offline-capable calculation history"),
        ]),
        ft.Container(height=6),
        gold_button("⬇  Download APK (Android)",
                    url="https://github.com/danieldanielm09-max/daniel-daniel-portfolio/raw/main/assets/MechTek.apk"),
    ])

    flet_section = ft.Container(
        content=ft.Column(spacing=12, controls=[
            section_header("Flet Experience", "Flet Web Contribution"),
            ft.Text(
                "I assisted my brother in building and deploying a Flet-based asset management "
                "web app on Replit. Contributed navigation routing, component layout, and "
                "colour-scheme implementation — practical Flet experience that directly informed "
                "how I structured this very portfolio.",
                size=13, color=MUTED,
            ),
            ft.Column(spacing=6, controls=[
                feat_row("Navigation with ft.NavigationRail"),
                feat_row("Replit deployment pipeline"),
                feat_row("Responsive layout with ft.ResponsiveRow"),
            ]),
            ft.Container(height=8),
            gold_button("↗  View Live Flet Site",
                        url="https://asset-manager--rafaeladrianota.replit.app/"),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=24,
    )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=24, controls=[
                    section_header("The Project", "App Showcase"),
                    ft.ResponsiveRow(columns=12, spacing=40, controls=[
                        ft.Column(col={"xs": 12, "md": 7}, controls=[app_info]),
                        ft.Column(col={"xs": 12, "md": 5},
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                  controls=[phone]),
                    ]),
                    flet_section,
                ]),
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — CONTACT
# ═══════════════════════════════════════════════════════════════════════════════

def build_contact():
    def stat(label, val):
        return ft.Column(spacing=0, controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(label, size=13, color=MUTED),
                    ft.Text(val, size=13, color=GOLD,
                            weight=ft.FontWeight.W_500),
                ],
            ),
            ft.Divider(color="#1A1F2B", height=1),
        ])

    facts = ft.Container(
        content=ft.Column(spacing=10, controls=[
            ft.Text("Quick Facts", size=16, color=TEXT,
                    font_family="Georgia", weight=ft.FontWeight.BOLD),
            ft.Divider(color="#1A1F2B", height=1),
            stat("MATLAB Courses", "9 / 8 required"),
            stat("Verified Commits", "6+ shown"),
            stat("Languages", "Python · JS · MATLAB"),
            stat("App Role", "Idea Originator"),
            stat("Blog Posts", "6 concepts"),
        ]),
        bgcolor=SURFACE,
        border=border_all(0.5, "#1A1F2B"),
        border_radius=br(14),
        padding=22,
    )

    left = ft.Column(spacing=14, controls=[
        ft.Text("Let's Connect", size=24, color=TEXT,
                font_family="Georgia", weight=ft.FontWeight.BOLD),
        ft.Text(
            "Whether it's about MechTek, MATLAB, or engineering software collaboration — "
            "reach out. I'm always open to learning and building with driven people.",
            size=13, color=MUTED,
        ),
        ft.Container(height=4),
        contact_info_row("📧", "Email",
                         "danieldanielm09@gmail.com",
                         "mailto:danieldanielm09@gmail.com"),
        contact_info_row("⎇", "GitHub",
                         "danieldanielm09-max",
                         "https://github.com/danieldanielm09-max"),
        contact_info_row("📍", "Location", "Namibia"),
        contact_info_row("🎓", "Institution",
                         "University of Namibia · Mining Engineering, Year 2"),
    ])

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=BG,
                padding=pad(h=40, v=50),
                content=ft.Column(spacing=16, controls=[
                    section_header("Get in Touch", "Contact"),
                    ft.ResponsiveRow(columns=12, spacing=40, controls=[
                        ft.Column(col={"xs": 12, "md": 7}, controls=[left]),
                        ft.Column(col={"xs": 12, "md": 5}, controls=[facts]),
                    ]),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Text(
                            "© 2026  Daniel Mathew Daniel · UNAM Mining Engineering",
                            size=12, color=MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.Alignment(x=0, y=0),
                    ),
                ]),
            ),
        ],
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
    profile_uri  = data_uri(asset("profile.jpg"),  "image/jpeg")
    commits_uri  = data_uri(asset("commits.png"),  "image/png")
    repo_uri     = data_uri(asset("github_repo.png"), "image/png")
    video_path   = asset("demo.mp4")
    apk_path     = asset("MechTek.apk")

    # Build all page views (built once, swapped on nav)
    pages = [
        build_home(profile_uri),
        build_timeline(),
        build_github(commits_uri, repo_uri),
        build_blog(video_path),
        build_matlab(),
        build_app(apk_path),
        build_contact(),
    ]

    content = ft.Container(
        content=pages[0],
        expand=True,
        bgcolor=BG,
    )

    def on_nav(e):
        content.content = pages[e.control.selected_index]
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=SURFACE,
        indicator_color=GOLD_DIM,
        indicator_shape=ft.RoundedRectangleBorder(radius=8),
        selected_label_text_style=ft.TextStyle(color=GOLD, size=11),
        unselected_label_text_style=ft.TextStyle(color=MUTED, size=11),
        min_width=90,
        on_change=on_nav,
        leading=ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text("D.", size=22, color=GOLD,
                            font_family="Georgia",
                            weight=ft.FontWeight.BOLD),
                    ft.Text("PORTFOLIO", size=8, color=MUTED),
                ],
            ),
            margin=mgn(b=8),
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

    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[
                rail,
                ft.VerticalDivider(width=1, color="#1A1F2B"),
                content,
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main, assets_dir=ASSETS_DIR)
