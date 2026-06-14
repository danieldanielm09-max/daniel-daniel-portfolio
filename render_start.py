"""
This file is ONLY for Render deployment.
To run locally, use: python main.py
"""
import os
import flet as ft
from main import main, ASSETS_DIR

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.run(
        main,
        assets_dir=ASSETS_DIR,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=port,
    )
