import flet as ft
from supabase import create_client, Client
import toml
import os
import requests
from io import BytesIO
from PIL import Image

# ============================================================
# 1. KREDENSIAL & KONEKSI (Smart Loader)
# ============================================================
def load_secrets():
    """Membaca kredensial dari file lokal atau environment variable."""
    # Prioritas 1: File lokal (untuk Desktop/APK)
    if os.path.exists("secrets.toml"):
        config = toml.load("secrets.toml")
        return config["supabase"]["url"], config["supabase"]["key"]
    
    # Prioritas 2: Environment (untuk Deployment Streamlit Cloud)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return url, key

SUPABASE_URL, SUPABASE_KEY = load_secrets()

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# ============================================================
# 2. KONFIGURASI VISUAL LUXURY
# ============================================================
NAVY_POLRI = "#001F5B"
GOLD_PRESISI = "#FFC107"
WHITE = "#FFFFFF"
GRAY_LUXURY = "#F8FAFC"
GRAY_BORDER = "#E2E8F0"

# Assets URL (Stored in Supabase Bucket)
URL_LOGO_JITU = "https://bxlfaofmraznomebbrlh.supabase.co/storage/v1/object/public/assets/logo_jitu.png"
URL_SPLASH = "https://bxlfaofmraznomebbrlh.supabase.co/storage/v1/object/public/assets/splash.png"

# ============================================================
# 3. KELAS UTAMA JITU PRESISI
# ============================================================
def main(page: ft.Page):
    # Pengaturan Canvas (Standar Mobile)
    page.title = "JITU PRESISI"
    page.window_width = 420
    page.window_height = 820
    page.window_resizable = False
    page.bgcolor = WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START

    # --- UI Component: Inset Input (280px) ---
    def create_input(label, icon, is_password=False):
        return ft.Container(
            width=280,
            content=ft.TextField(
                label=label,
                prefix_icon=icon,
                password=is_password,
                can_reveal_password=is_password,
                border_radius=27,
                border_color=GRAY_BORDER,
                bgcolor=WHITE,
                focused_border_color=NAVY_POLRI,
                text_size=14,
                content_padding=15
            )
        )

    # --- View: Splash Screen ---
    def show_splash():
        page.clean()
        splash_container = ft.Container(
            expand=True,
            bgcolor=NAVY_POLRI,
            content=ft.Column([
                ft.Image(src=URL_SPLASH, width=120, animate_opacity=300),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.add(splash_container)
        page.update()
        
        # Jeda 2 detik sebelum masuk login
        import time
        time.sleep(2)
        show_login()

    # --- View: Login Page (Proportional Layout) ---
    def show_login():
        page.clean()
        
        # 1. Hero Section (Flexible Space)
        hero = ft.Container(
            expand=True,
            content=ft.Column([
                ft.Image(src=URL_LOGO_JITU, width=100),
                ft.Row([
                    ft.Text("JITU", size=22, weight="bold", color="black"),
                    ft.Text(" PRESISI", size=22, weight="bold", color=GOLD_PRESISI),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # 2. Form Section (Fixed Bottom)
        form = ft.Container(
            padding=ft.padding.only(bottom=60),
            content=ft.Column([
                # Badge Akses Aman (320px)
                ft.Container(
                    width=320, height=45, bgcolor=GRAY_LUXURY, border_radius=22,
                    alignment=ft.alignment.center,
                    content=ft.Text("AKSES AMAN", weight="bold", color="#64748B", size=12)
                ),
                ft.Divider(height=15, color="transparent"),
                
                # Input Area (280px)
                nrp_field = create_input("NRP / NIP", ft.icons.PERSON_OUTLINE),
                pass_field = create_input("Password", ft.icons.LOCK_OUTLINE, is_password=True),
                
                ft.Divider(height=25, color="transparent"),
                
                # Action Button (320px)
                ft.Container(
                    width=320, height=60,
                    content=ft.ElevatedButton(
                        text="MASUK",
                        style=ft.ButtonStyle(
                            color=WHITE, 
                            bgcolor=NAVY_POLRI, 
                            shape=ft.RoundedRectangleBorder(radius=30)
                        ),
                        on_click=lambda _: handle_login(nrp_field.content.value)
                    )
                ),
                ft.TextButton(text="Lupa Password?", style=ft.ButtonStyle(color="#94A3B8"))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        page.add(ft.Column([hero, form], expand=True))
        page.update()

    # --- Logic: Handle Login ---
    def handle_login(nrp):
        if not supabase:
            page.snack_bar = ft.SnackBar(ft.Text("Koneksi Supabase belum siap!"))
            page.snack_bar.open = True
            page.update()
            return
        
        print(f"Mencoba login untuk NRP: {nrp}")
        # Logika query ke tabel Tunkin Puskeu Polri akan ditambahkan di sini

    show_splash()

if __name__ == "__main__":
    ft.app(target=main)
