import customtkinter as ctk
from tkinter import messagebox, simpledialog
from supabase import create_client, Client
from PIL import Image
import requests
from io import BytesIO
import locale
import os

# ============================================================
# 1. KONFIGURASI & KONSTANTA (Locked)
# ============================================================
URL = "https://bxlfaofmraznomebbrlh.supabase.co"
KEY = "sb_publishable_SIb5TK2e9wZqUbxS8kqkig_pwm7wQIH"
supabase: Client = create_client(URL, KEY)

URL_SPLASH = f"{URL}/storage/v1/object/public/assets/splash.png"
URL_LOGO_JITU = f"{URL}/storage/v1/object/public/assets/logo_jitu.png"

# Palet Warna Luxury
NAVY_DEEP = "#001F5B"      
GOLD_PRESISI = "#FFC107"   
WHITE = "#FFFFFF"
GRAY_LUXURY = "#F8FAFC"
GRAY_BORDER = "#E2E8F0"
GRAY_SUBTLE = "#94A3B8"

ctk.set_appearance_mode("light")

# ============================================================
# 2. KAMUS TRANSLASI
# ============================================================
LANG_DATA = {
    "ID": {
        "access": "AKSES AMAN",
        "user": "NRP / NIP", "pass": "Password", "login": "MASUK",
        "or": "──────── atau ────────", "google": "Login dengan Google",
        "forgot": "Lupa Password?"
    },
    "EN": {
        "access": "SECURE ACCESS",
        "user": "ID Number", "pass": "Password", "login": "SIGN IN",
        "or": "──────── or ────────", "google": "Sign in with Google",
        "forgot": "Forgot Password?"
    }
}

# ============================================================
# 3. UTILITAS & HELPER
# ============================================================
def load_cloud_image(url, target_width):
    try:
        response = requests.get(url, timeout=5)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        w, h = img.size
        new_height = int(target_width / (w/h))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(target_width, new_height))
    except: return None

# ============================================================
# 4. KELAS UTAMA APLIKASI
# ============================================================
class JituApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JITU PRESISI")
        self.geometry("420x820")
        self.resizable(False, False)
        self.configure(fg_color=WHITE)

        self.current_lang = "ID" 
        self.pass_visible = False
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.init_splash()

    def create_inset_input(self, parent, icon, placeholder, show="", pady=0):
        # Inset Luxury: 280px
        f = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color=GRAY_BORDER, 
                         width=280, height=52, corner_radius=26)
        f.pack(pady=pady); f.pack_propagate(False)
        ctk.CTkLabel(f, text=icon, font=("Arial", 16)).pack(side="left", padx=(15, 5))
        e = ctk.CTkEntry(f, placeholder_text=placeholder, show=show, border_width=0, 
                         fg_color="transparent", font=("Arial", 14))
        e.pack(side="left", fill="x", expand=True, padx=(0, 20))
        return f, e

    def init_splash(self):
        for w in self.container.winfo_children(): w.destroy()
        splash = ctk.CTkFrame(self.container, fg_color=NAVY_DEEP, corner_radius=0)
        splash.pack(fill="both", expand=True)
        img = load_cloud_image(URL_SPLASH, 100)
        if img: ctk.CTkLabel(splash, image=img, text="").place(relx=0.5, rely=0.45, anchor="center")
        self.after(2000, self.init_login)

    def init_login(self):
        for w in self.container.winfo_children(): w.destroy()
        t = LANG_DATA[self.current_lang]

        # A. Language Selector (EN | ID)
        lang_f = ctk.CTkFrame(self.container, fg_color="transparent")
        lang_f.place(relx=0.92, y=40, anchor="ne")
        ctk.CTkButton(lang_f, text="EN", width=25, text_color=NAVY_DEEP if self.current_lang=="EN" else GRAY_SUBTLE, 
                      fg_color="transparent", font=("Arial", 12, "bold"), command=lambda: self.switch_lang("EN")).pack(side="left")
        ctk.CTkLabel(lang_f, text="|", text_color=GRAY_BORDER).pack(side="left", padx=2)
        ctk.CTkButton(lang_f, text="ID", width=25, text_color=NAVY_DEEP if self.current_lang=="ID" else GRAY_SUBTLE, 
                      fg_color="transparent", font=("Arial", 12, "bold"), command=lambda: self.change_lang("ID")).pack(side="left")

        # B. BRANDING AREA (Pakar Calibrated: 140px)
        img_l = load_cloud_image(URL_LOGO_JITU, 90)
        if img_l: ctk.CTkLabel(self.container, image=img_l, text="").pack(pady=(140, 5)) 
        
        brand_f = ctk.CTkFrame(self.container, fg_color="transparent")
        brand_f.pack(pady=(0, 30))
        ctk.CTkLabel(brand_f, text="JITU", font=("Arial", 18, "bold"), text_color="black").pack(side="left")
        ctk.CTkLabel(brand_f, text=" PRESISI", font=("Arial", 18, "bold"), text_color=GOLD_PRESISI).pack(side="left")

        # C. Form Area (Simetris 320px)
        ctk.CTkLabel(self.container, text=t["access"], font=("Arial", 12, "bold"), 
                     text_color="#64748B", fg_color=GRAY_LUXURY, width=320, height=45, corner_radius=22).pack(pady=(0, 20))

        _, self.nrp_ent = self.create_inset_input(self.container, "👤", t["user"], pady=(0, 15))
        
        # Pass + Eye Toggle
        f_pass = ctk.CTkFrame(self.container, fg_color="white", border_width=1, border_color=GRAY_BORDER, width=280, height=52, corner_radius=26)
        f_pass.pack(pady=(0, 25)); f_pass.pack_propagate(False)
        self.eye_btn = ctk.CTkButton(f_pass, text="🔒", width=30, fg_color="transparent", text_color="black", hover_color=WHITE, command=self.toggle_eye)
        self.eye_btn.pack(side="left", padx=(10, 0))
        self.pw_ent = ctk.CTkEntry(f_pass, placeholder_text=t["pass"], show="*", border_width=0, fg_color="transparent", font=("Arial", 14))
        self.pw_ent.pack(side="left", fill="x", expand=True, padx=(0, 20))

        # D. Action Area (Simetris 320px)
        ctk.CTkButton(self.container, text=t["login"], fg_color=NAVY_DEEP, font=("Arial", 16, "bold"), 
                      height=60, width=320, corner_radius=30).pack(pady=(10, 20))
        
        ctk.CTkLabel(self.container, text=t["or"], text_color="#E2E8F0", font=("Arial", 10)).pack()
        ctk.CTkButton(self.container, text=t["google"], fg_color="white", text_color="black", border_width=1, 
                      border_color=GRAY_BORDER, height=55, width=320, corner_radius=27).pack(pady=(20, 10))
        
        ctk.CTkButton(self.container, text=t["forgot"], text_color=GRAY_SUBTLE, fg_color="transparent", 
                      font=("Arial", 11, "bold")).pack(pady=10)

    # --- Bisnis Logika ---
    def switch_lang(self, lang):
        self.current_lang = lang
        self.init_login()

    def toggle_eye(self):
        self.pass_visible = not self.pass_visible
        self.pw_ent.configure(show="" if self.pass_visible else "*")
        self.eye_btn.configure(text="👁️" if self.pass_visible else "🔒")

if __name__ == "__main__":
    app = JituApp()
    app.mainloop()