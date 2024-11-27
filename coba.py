import csv
import os

def clear():
    """Membersihkan layar terminal, kompatibel dengan Windows dan UNIX."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_users(file_path):
    """Memuat data pengguna dari file CSV."""
    users = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    return users

def load_complaints(file_path):
    """Memuat data keluhan dari file CSV."""
    complaints = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] not in complaints:
                    complaints[row['email']] = []
                complaints[row['email']].append(row['keluhan'])
    except FileNotFoundError:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'keluhan'])
            writer.writeheader()
    return complaints

def save_complaint(email, complaint, file_path):
    """Menyimpan keluhan pengguna ke file CSV."""
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'keluhan'])
            writer.writerow({'email': email, 'keluhan': complaint})
        print("\nKeluhan berhasil disimpan!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan keluhan: {e}")

def login(email, password, users):
    """Memverifikasi login dan mengembalikan data pengguna jika ditemukan."""
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    return None

def register_user(email, password, name, address, file_path):
    """Menambahkan data pengguna baru ke file CSV."""
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'password', 'nama', 'alamat'])
            writer.writerow({'email': email, 'password': password, 'nama': name, 'alamat': address})
        print("Registrasi berhasil!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def choose_complaint():
    """Memungkinkan pengguna memilih poli, penyakit, dan mendapatkan dokter."""
    poli_options = {
        '1': {'name': 'Poli Umum', 'penyakit': ['Demam - Dr. Budi', 'Flu - Dr. Sari', 'Sakit Kepala - Dr. Andi', 'Pusing - Dr. Maya']},
        '2': {'name': 'Poli Mata', 'penyakit': ['Mata Minus - Dr. Dinda', 'Katarak - Dr. Iwan', 'Mata Kering - Dr. Siska', 'Iritasi - Dr. Fajar']},
        '3': {'name': 'Poli Gigi', 'penyakit': ['Gigi Berlubang - Dr. Rani', 'Karang Gigi - Dr. Adi', 'Gigi Sensitif - Dr. Bima', 'Infeksi Gusi - Dr. Risa']},
        '4': {'name': 'Poli THT', 'penyakit': ['Radang Tenggorokan - Dr. Hana', 'Sinusitis - Dr. Arif', 'Hidung Tersumbat - Dr. Dewi', 'Infeksi Telinga - Dr. Putra']}
    }

    print("\nPilih Poli:")
    for key, poli in poli_options.items():
        print(f"{key}. {poli['name']}")

    poli_choice = input("Masukkan pilihan poli (1-4): ").strip()
    if poli_choice in poli_options:
        selected_poli = poli_options[poli_choice]
        print(f"\nAnda memilih: {selected_poli['name']}")

        print("\nPilih Penyakit:")
        for i, penyakit in enumerate(selected_poli['penyakit'], 1):
            print(f"{i}. {penyakit}")

        penyakit_choice = input("Masukkan pilihan penyakit (1-4): ").strip()
        if penyakit_choice.isdigit() and 1 <= int(penyakit_choice) <= 4:
            selected_penyakit = selected_poli['penyakit'][int(penyakit_choice) - 1]
            return f"{selected_poli['name']} - {selected_penyakit}"
        else:
            print("Pilihan penyakit tidak valid!")
    else:
        print("Pilihan poli tidak valid!")
    return None

def lihat_riwayat_penyakit(email, complaints):
    """Menampilkan riwayat keluhan/penyakit yang pernah diajukan oleh pengguna."""
    if email in complaints and complaints[email]:
        clear()
        print("\nRiwayat Penyakit Anda:")
        for i, keluhan in enumerate(complaints[email], 1):
            print(f"{i}. {keluhan}")
    else:
        print("Belum ada riwayat penyakit yang diajukan.")

def main():
    user_file_path = 'users.csv'
    complaint_file_path = 'keluhan.csv'

    # Jika file kosong, tambahkan header untuk pertama kali
    try:
        with open(user_file_path, mode='r') as file:
            pass
    except FileNotFoundError:
        with open(user_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'password', 'nama', 'alamat'])
            writer.writeheader()

    while True:
        clear()
        users = load_users(user_file_path)
        complaints = load_complaints(complaint_file_path)

        print("="*50)
        print("Selamat datang! Pilih opsi:")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        print("="*50)

        choice = input("Masukkan pilihan Anda (1/2/3): ")
        if choice == '1':
            # Login
            clear()
            email = input("Masukkan email: ").strip().lower()
            password = input("Masukkan password: ")

            user = login(email, password, users)
            if user:
                clear()
                print("="*50)
                print("Login berhasil!")
                print("-"*50)
                print("Informasi Pengguna:")
                print(f"Nama: {user['nama']}")
                print(f"Alamat: {user['alamat']}")
                print("="*50)

                # Pilihan setelah login
                while True:
                    
                    print("\nPilih opsi setelah login:")
                    print("1. Mengajukan keluhan")
                    print("2. Lihat riwayat penyakit")
                    print("3. Logout")

                    user_choice = input("Masukkan pilihan Anda (1/2/3): ").strip()
                    if user_choice == '1':
                        keluhan = choose_complaint()
                        if keluhan:
                            save_complaint(email, keluhan, complaint_file_path)

                            # Perbarui complaints secara langsung
                            if email not in complaints:
                                complaints[email] = []
                            complaints[email].append(keluhan)
                    elif user_choice == '2':
                        lihat_riwayat_penyakit(email, complaints)
                        input("\nTekan Enter untuk kembali ke menu...")  # Menunggu input agar bisa kembali
                    elif user_choice == '3':
                        print("Anda telah logout.")
                        break
                    else:
                        print("Pilihan tidak valid! Kembali ke menu...")
                        input("\nTekan Enter untuk melanjutkan...")
            else:
                print("\nEmail atau password salah!")
                retry = input("Kembali ke menu awal? (y/n): ").lower()
                if retry != 'y':
                    break

        elif choice == '2':
            # Registrasi
            clear()
            print("Silakan masukkan data untuk registrasi:")
            email = input("Masukkan email: ").strip().lower()
            password = input("Masukkan password: ")
            name = input("Masukkan nama: ")
            address = input("Masukkan alamat: ")

            # Periksa apakah email sudah ada
            if any(user['email'] == email for user in users):
                print("Email sudah terdaftar. Silakan gunakan email lain.")
            else:
                register_user(email, password, name, address, user_file_path)
        elif choice == '3':
            print("Terima kasih telah menggunakan sistem. Sampai jumpa!")
            break

# Jalankan program utama
main()
