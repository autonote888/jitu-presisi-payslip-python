import flet as ft
from supabase import create_client, Client
import toml
import locale
import time
import os

# ============================================================
# 1. LOGIKA SECRETS & KONEKSI SUPABASE
# ============================================================
def load_secrets():
    """Memuat kredensial dari file secrets.toml secara aman."""
    try:
        # Mencari file secrets.toml di direktori yang sama dengan skrip
        config = toml.load("secrets.toml")
        url = config["supabase"]["url"]
        key = config["supabase"]["key"]
        return url, key
    except Exception as e:
        print(f"⚠️ Gagal memuat secrets.toml: {e}")
        return None, None

# Inisialisasi Supabase menggunakan Secrets
SUPABASE_URL, SUPABASE_KEY = load_secrets()
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("❌ Aplikasi tidak dapat terhubung ke Supabase. Periksa secrets.toml!")

# ============================================================
# 2. KONFIGURASI VISUAL (Locked "Luxury Inset")
# ============================================================
NAVY_POLRI = "#001F5B"
GOLD_PRESISI = "#FFC107"
WHITE = "#FFFFFF"
GRAY_LUXURY = "#F8FAFC"
GRAY_BORDER = "#E2E8F0"

# URL Assets Cloud
URL_LOGO_JITU = "https://bxlfaofmraznomebbrlh.supabase.co/storage/v1/object/public/assets/logo_jitu.png"
URL_SPLASH = "https://bxlfaofmraznomebbrlh.supabase.co/storage/v1/object/public/assets/splash.png"

def main(page: ft.Page):
    # Pengaturan Canvas Mobile
    page.title = "JITU PRESISI - DATAGAJI"
    page.window_width = 420
    page.window_height = 820
    page.bgcolor = WHITE
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START

    # State Management
    page.session_storage.set("lang", "ID")

    # --- 3. UI COMPONENTS ---
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
            )
        )

    # --- 4. ANIMATED SPLASH SCREEN ---
    def run_splash():
        page.clean()
        
        # Logo Splash di tengah
        splash_logo = ft.Image(src=URL_SPLASH, width=120)
        
        splash_container = ft.Container(
            expand=True,
            bgcolor=NAVY_POLRI,
            content=ft.Column([
                ft.Container(content=splash_logo, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        page.add(splash_container)
        
        # Animasi Ping-Pong (Simulasi Sederhana di Flet)
        # Untuk Flet, kita gunakan transisi page setelah jeda
        time.sleep(2)
        run_login()

    # --- 5. PROPORTIONAL LOGIN PAGE ---
    def run_login():
        page.clean()
        t = {"ID": "AKSES AMAN", "EN": "SECURE ACCESS"} # Contoh simpel lokalisasi
        
        # A. HERO SECTION (Auto-Center)
        hero_section = ft.Container(
            expand=True,
            content=ft.Column([
                ft.Image(src=URL_LOGO_JITU, width=100),
                ft.Row([
                    ft.Text("JITU", size=22, weight="bold", color="black"),
                    ft.Text(" PRESISI", size=22, weight="bold", color=GOLD_PRESISI),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # B. FORM SECTION (Bottom Weighted)
        form_section = ft.Container(
            padding=ft.padding.only(bottom=60),
            content=ft.Column([
                ft.Container(
                    width=320, height=45, bgcolor=GRAY_LUXURY, border_radius=22,
                    alignment=ft.alignment.center,
                    content=ft.Text(t["ID"], weight="bold", color="#64748B", size=12)
                ),
                ft.Divider(height=15, color="transparent"),
                create_input("NRP / NIP", ft.icons.PERSON_OUTLINE),
                create_input("Password", ft.icons.LOCK_OUTLINE, is_password=True),
                ft.Divider(height=25, color="transparent"),
                
                ft.Container(
                    width=320, height=60,
                    content=ft.ElevatedButton(
                        text="MASUK",
                        style=ft.ButtonStyle(color=WHITE, bgcolor=NAVY_POLRI, shape=ft.RoundedRectangleBorder(radius=30)),
                        on_click=lambda _: print(f"Menghubungkan ke: {SUPABASE_URL}")
                    )
                ),
                ft.TextButton(text="Lupa Password?", style=ft.ButtonStyle(color="#94A3B8"))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        page.add(ft.Column([hero_section, form_section], expand=True))
        page.update()

    # Mulai Aplikasi
    run_splash()

if __name__ == "__main__":
    ft.app(target=main)
