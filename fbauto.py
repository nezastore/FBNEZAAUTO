import requests
import random
import string
import json
import hashlib
import time
from faker import Faker

def print_banner():
    banner = """
\x1b[38;5;46m    █▀▄▀█ █▀▀ █▀▀█   █▀▀█ █░░█ ▀▀█▀▀ █▀▀ █▀▀█ 
\x1b[38;5;47m    █░▀░█ █▀▀ █▄▄█   █▄▄█ █░░█ ░░█░░ █▀▀ █▄▄▀ 
\x1b[38;5;48m    ▀░░░▀ ▀▀▀ ▀░░▀   ▀░░▀ ░▀▀▀ ░░▀░░ ▀▀▀ ▀░▀▀ 
\x1b[38;5;226m                Auto Register Facebook
\x1b[38;5;208m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\x1b[38;5;22m❖ › Channel : @NezaFx                ❖ › By : @NezaFvnky
\x1b[38;5;208m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m
"""
    print(banner)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def get_mail_domains():
    url = "https://api.mail.tm/domains"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()['hydra:member']
    except Exception:
        return None
    return None

def create_mail_tm_account():
    print("\x1b[38;5;226m[~] Membuat akun mail.tm...")
    fake = Faker()
    mail_domains = get_mail_domains()
    if mail_domains:
        domain = random.choice(mail_domains)['domain']
        username = generate_random_string(12)
        password = fake.password(length=10)
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
        first_name = fake.first_name()
        last_name = fake.last_name()
        url = "https://api.mail.tm/accounts"
        headers = {"Content-Type": "application/json"}
        data = {"address": f"{username}@{domain}", "password": password}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 201:
                print(f"\x1b[38;5;46m[✓] Email sementara berhasil dibuat.\x1b[0m")
                return f"{username}@{domain}", password, first_name, last_name, birthday
        except Exception as e:
            print(f"\x1b[38;5;196m[!] Gagal membuat email: {e}\x1b[0m")
            return None, None, None, None, None
    print(f"\x1b[38;5;196m[!] Gagal mendapatkan domain dari mail.tm.\x1b[0m")
    return None, None, None, None, None

def register_facebook_account(email, password, first_name, last_name, birthday):
    print("\x1b[38;5;226m[~] Mencoba mendaftar ke Facebook...")
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    req = {
        'api_key': api_key, 'attempt_login': True, 'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'EN', 'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount', 'firstname': first_name, 'format': 'json',
        'gender': gender, 'lastname': last_name, 'email': email, 'locale': 'en_US',
        'method': 'user.register', 'password': password, 'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig
    api_url = 'https://b-api.facebook.com/method/user.register'
    
    reg = _call(api_url, req)
    
    if not reg or 'error_msg' in reg:
        error_message = reg.get('error_msg', 'Koneksi gagal atau respons tidak valid.') if reg else 'Koneksi gagal.'
        print(f"\x1b[38;5;196m[!] PENDAFTARAN GAGAL: {error_message}\x1b[0m")
        return

    id_akun = reg['new_user_id']
    token = reg['session_info']['access_token']
    
    print("\x1b[38;5;46m[✓] PENDAFTARAN BERHASIL!\x1b[0m")
    print_account_info(email, password, id_akun, f"{first_name} {last_name}", birthday, gender, token)

def print_account_info(email, pw, uid, name, dob, gender, token):
    info = f"""
\x1b[38;5;208m    ┌─ \x1b[1;37mINFO AKUN BERHASIL DIBUAT\x1b[0m
\x1b[38;5;208m    ├─ Email    : \x1b[38;5;22m{email}\x1b[0m
\x1b[38;5;208m    ├─ Password : \x1b[38;5;22m{pw}\x1b[0m
\x1b[38;5;208m    ├─ Nama     : \x1b[38;5;22m{name}\x1b[0m
\x1b[38;5;208m    ├─ UID      : \x1b[38;5;22m{uid}\x1b[0m
\x1b[38;5;208m    ├─ TTL      : \x1b[38;5;22m{dob.strftime('%d-%m-%Y')} ({gender})\x1b[0m
\x1b[38;5;208m    └─ Token    : \x1b[38;5;22m{token[:25]}...\x1b[0m
    """
    print(info)

def _call(url, params, post=True):
    headers = {'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'}
    try:
        if post:
            response = requests.post(url, data=params, headers=headers, timeout=15)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=15)
        return response.json()
    except Exception as e:
        print(f"\x1b[38;5;196m[!] Error Koneksi: {e}\x1b[0m")
        return None

# --- Loop Utama ---
if __name__ == "__main__":
    print_banner()
    try:
        jumlah_akun = int(input('\x1b[38;5;226m[?] Berapa banyak akun yang ingin Anda buat?: \x1b[0m'))
        print('\x1b[38;5;208m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m')

        for i in range(jumlah_akun):
            print(f"\n\x1b[1;37m--- Memproses Akun #{i+1} dari {jumlah_akun} ---\x1b[0m")
            email, password, first_name, last_name, birthday = create_mail_tm_account()
            if email:
                register_facebook_account(email, password, first_name, last_name, birthday)
            else:
                print(f"\x1b[38;5;196m[!] Gagal membuat email, proses untuk akun #{i+1} dihentikan.\x1b[0m")
            
            # Beri jeda antar pembuatan akun untuk mengurangi risiko
            time.sleep(3)

    except ValueError:
        print("\n\x1b[38;5;196m[!] Input tidak valid. Harap masukkan angka.\x1b[0m")
    except KeyboardInterrupt:
        print("\n\x1b[38;5;226m[!] Proses dihentikan oleh pengguna.\x1b[0m")
    except Exception as e:
        print(f"\n\x1b[38;5;196m[!] Terjadi error tak terduga: {e}\x1b[0m")

    print('\n\x1b[38;5;208m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m')
    print("\x1b[38;5;46m[✓] Selesai.\x1b[0m")
