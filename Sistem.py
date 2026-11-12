from datetime import datetime

import msvcrt

def input_password(prompt="Password : "):
    print(prompt, end="", flush=True)
    password = ""

    while True:
        karakter = msvcrt.getwch()

        if karakter == "\r":
            print()
            break

        elif karakter == "\b":
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)

        elif karakter in ("\x00", "\xe0"):
            msvcrt.getwch()

        else:
            password += karakter
            print("*", end="", flush=True)

    return password


def daftar_akun():
    print("\n========== DAFTAR AKUN SMK MART ==========")
    print("1. Admin")
    print("2. Gudang")
    print("3. Kasir")

    pilihan = input("Pilih role: ")

    if pilihan == "1":
        role = "Admin"
        nama_file = "data/admin.txt"
    elif pilihan == "2":
        role = "Gudang"
        nama_file = "data/gudang_akun.txt"
    elif pilihan == "3":
        role = "Kasir"
        nama_file = "data/kasir.txt"
    else:
        print("Pilihan tidak valid!")
        return

    nama = input("Nama     : ")
    username = input("Username : ")
    password = input_password("Password : ")

    if nama == "" or username == "" or password == "":
        print("Semua data harus diisi!")
        return

    daftar_file = [
        "data/admin.txt",
        "data/gudang_akun.txt",
        "data/kasir.txt"
    ]

    for file_akun in daftar_file:
        file = open(file_akun, "r")
        isi = file.read()
        file.close()

        daftar_pengguna = isi.split("\n")

        for pengguna in daftar_pengguna:
            data = pengguna.split("|")

            if len(data) == 4 or len(data) == 5:
                if data[1] == username:
                    print("Username sudah pernah digunakan!")
                    return

    file = open(nama_file, "a")
    file.write(
        nama + "|" + username + "|" +
        password + "|" + role + "|Aktif\n"
    )
    file.close()

    print("\nPendaftaran berhasil!")
    print("Nama:", nama)
    print("Username:", username)
    print("Role:", role)
    print("Status: Aktif")



keranjang = []
keranjang_kasir = []

nama_pengguna_aktif = ""
role_aktif = ""


def login():
    global nama_pengguna_aktif, role_aktif

    print("\n========== LOGIN SMK MART ==========")

    username = input("Username : ")
    password = input("Password : ")

    daftar_file = [
        "data/admin.txt",
        "data/gudang_akun.txt",
        "data/kasir.txt"
    ]

    for nama_file in daftar_file:
        file = open(nama_file, "r")
        isi = file.read()
        file.close()

        daftar_pengguna = isi.split("\n")

        for pengguna in daftar_pengguna:
            data = pengguna.split("|")

            if len(data) == 4 or len(data) == 5:
                status = "Aktif"

                if len(data) == 5:
                    status = data[4]

                if data[1] == username and data[2] == password:

                    if status == "Tidak Aktif":
                        print("Akun kamu sudah tidak aktif!")
                        return

                    nama_pengguna_aktif = data[0]
                    role_aktif = data[3]

                    print("\nLogin berhasil!")
                    print("Selamat datang,", nama_pengguna_aktif)
                    print("Role:", role_aktif)

                    if role_aktif == "Admin":
                        catat_aktivitas(
                            "data/admin_aktivitas.txt",
                            nama_pengguna_aktif,
                            "Login"
                        )
                        menu_admin()

                    elif role_aktif == "Gudang":
                        catat_aktivitas(
                            "data/gudang_aktivitas.txt",
                            nama_pengguna_aktif,
                            "Login"
                        )
                        menu_gudang()

                    elif role_aktif == "Kasir":
                        catat_aktivitas(
                            "data/kasir_aktivitas.txt",
                            nama_pengguna_aktif,
                            "Login"
                        )
                        menu_kasir()

                    return

    print("Username atau password salah!")


def menu_admin():
    while True:
        print("\n========== MENU ADMIN ==========")
        print("1. Kelola Akun")
        print("2. Kelola Barang")
        print("3. Laporan Penjualan")
        print("4. Laporan Seluruh Aktivitas")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            kelola_akun()

        elif pilihan == "2":
            while True:
                print("\n========== KELOLA BARANG ==========")
                print("1. Tambah Barang")
                print("2. Edit Barang")
                print("3. Nonaktifkan Barang")
                print("4. Aktifkan Barang")
                print("5. Kembali")

                pilih_barang = input("Pilih menu: ")

                if pilih_barang == "1":
                    tambah_barang()
                elif pilih_barang == "2":
                    edit_barang()
                elif pilih_barang == "3":
                    hapus_barang()
                elif pilih_barang == "4":
                    aktifkan_barang()
                elif pilih_barang == "5":
                    break
                else:
                    print("Pilihan tidak valid!")

        elif pilihan == "3":
            lihat_laporan()

        elif pilihan == "4":
            lihat_semua_aktivitas()

        elif pilihan == "5":
            print("Admin berhasil logout.")
            catat_aktivitas(
                "data/admin_aktivitas.txt",
                nama_pengguna_aktif,
                "Logout"
            )
            break

        else:
            print("Pilihan tidak valid!")


def menu_gudang():
    while True:
        print("\n====== MENU PETUGAS GUDANG ======")
        print("1. Lihat Stok")
        print("2. Barang Masuk")
        print("3. Riwayat Barang Masuk")
        print("4. Barang Keluar")
        print("5. Riwayat Barang Keluar")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_stok()

        elif pilihan == "2":
            barang_masuk()

        elif pilihan == "3":
            lihat_riwayat_barang_masuk()

        elif pilihan == "4":
            barang_keluar()

        elif pilihan == "5":
            lihat_riwayat_barang_keluar()

        elif pilihan == "6":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak valid.")


def menu_kasir():
    while True:
        print("\n========== MENU KASIR ==========")
        print("1. Lihat Barang")
        print("2. Tambah Barang ke Keranjang")
        print("3. Lihat Keranjang")
        print("4. Proses Pesanan")
        print("5. Riwayat Transaksi")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_barang()

        elif pilihan == "2":
            tambah_keranjang_kasir()

        elif pilihan == "3":
            lihat_keranjang_kasir()

        elif pilihan == "4":
            bayar(keranjang_kasir)

        elif pilihan == "5":
            lihat_riwayat_transaksi()

        elif pilihan == "6":
            catat_aktivitas(
                "data/kasir_aktivitas.txt",
                nama_pengguna_aktif,
                "Logout"
            )

            print("Berhasil logout dari akun Kasir.")
            break

        else:
            print("Pilihan tidak valid.")


def lihat_barang():
    print("\n==================== DAFTAR BARANG SMK MART ====================")

    try:
        file = open("data/gudang.txt", "r")
        isi = file.readlines()
        file.close()

        print("-" * 85)
        print(f"{'Kode':<12}{'Nama Barang':<25}{'Harga':>12}{'Stok':>8}{'Min Stok':>12}")
        print("-" * 85)

        ada_barang = False

        for barang in isi:
            data = barang.strip().split("|")

            if len(data) == 6 and data[5] == "Aktif":
                kode = data[0]
                nama = data[1]
                harga = int(data[2])
                stok = int(data[3])
                min_stok = int(data[4])

                print(f"{kode:<12}{nama:<25}{harga:>12,}{stok:>8}{min_stok:>12}")
                ada_barang = True

        if ada_barang == False:
            print("Belum ada barang aktif.")

        print("-" * 85)

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")
    except ValueError:
        print("Data barang tidak valid.")


def lihat_keranjang():
    print("\n========== KERANJANG PEMBELI ==========")

    if len(keranjang) == 0:
        print("Keranjang masih kosong.")
        return

    total = 0

    print("-" * 60)
    print(f"{'Nama Barang':<22}{'Harga':>12}{'Jumlah':>8}{'Subtotal':>15}")
    print("-" * 60)

    for barang in keranjang:
        nama = barang[1]
        harga = barang[2]
        jumlah = barang[3]
        subtotal = harga * jumlah
        total = total + subtotal

        print(f"{nama:<22}{harga:>12,}{jumlah:>8}{subtotal:>15,}")

    print("-" * 60)
    print(f"{'TOTAL':>42}{total:>18,}")
    print("-" * 60)


def bayar(daftar_keranjang):
    if not daftar_keranjang:
        print("Keranjang masih kosong.")
        return

    total = 0

    for barang in daftar_keranjang:
        total += barang[2] * barang[3]

    while True:
        try:
            uang = int(input("Masukkan uang pembayaran (0 untuk batal): Rp"))

            if uang == 0:
                print("Pesanan dibatalkan.")
                return

            elif uang < 0:
                print("Uang pembayaran tidak boleh negatif.")

            elif uang < total:
                kurang = total - uang
                print("Uang pembayaran tidak mencukupi.")
                print(f"Uang kurang: Rp{kurang:,}")
                print("Silakan masukkan pembayaran kembali.")

            else:
                break

        except ValueError:
            print("Masukkan angka bulat yang valid.")

    try:
        with open("data/gudang.txt", "r") as file:
            isi = file.readlines()

        daftar_barang = []

        for baris in isi:
            data = baris.strip().split("|")

            if len(data) == 6:
                daftar_barang.append(data)

        for barang in daftar_keranjang:
            jumlah_total = 0

            for barang_lain in daftar_keranjang:
                if barang_lain[0] == barang[0]:
                    jumlah_total += barang_lain[3]

            ditemukan = False

            for data in daftar_barang:
                if data[0] == barang[0]:
                    ditemukan = True

                    if data[5] != "Aktif":
                        print("Barang", data[1], "sudah tidak aktif.")
                        return

                    stok = int(data[3])

                    if stok < jumlah_total:
                        print("Stok", data[1], "tidak mencukupi.")
                        print("Stok tersedia:", stok)
                        print("Jumlah diminta:", jumlah_total)
                        return

                    break

            if ditemukan == False:
                print("Barang", barang[1], "tidak ditemukan di gudang.")
                return

        for data in daftar_barang:
            jumlah_total = 0

            for barang in daftar_keranjang:
                if barang[0] == data[0]:
                    jumlah_total += barang[3]

            if jumlah_total > 0:
                data[3] = str(int(data[3]) - jumlah_total)

        tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open("data/riwayat.txt", "a") as file:
            for barang in daftar_keranjang:
                subtotal = barang[2] * barang[3]

                file.write(
                    tanggal + "|" +
                    barang[0] + "|" +
                    barang[1] + "|" +
                    str(barang[2]) + "|" +
                    str(barang[3]) + "|" +
                    str(subtotal) + "|" +
                    str(total) + "|Aktif\n"
                )

        with open("data/gudang.txt", "w") as file:
            for data in daftar_barang:
                file.write("|".join(data) + "\n")

        catat_aktivitas(
            "data/kasir_aktivitas.txt",
            nama_pengguna_aktif,
            "Memproses pembayaran dengan total Rp" + str(total)
        )

        kembalian = uang - total

        print("\n")
        print("=" * 42)
        print("              SMK MART")
        print("           STRUK PEMBELIAN")
        print("=" * 42)
        print("Tanggal :", tanggal)
        print("-" * 42)
        print(f"{'Nama Barang':<20}{'Qty':>5}{'Subtotal':>17}")
        print("-" * 42)

        for barang in daftar_keranjang:
            subtotal = barang[2] * barang[3]
            print(f"{barang[1]:<20}{barang[3]:>5}{subtotal:>17,}")

        print("-" * 42)
        print(f"{'Total Belanja':<25}Rp{total:>14,}")
        print(f"{'Uang Bayar':<25}Rp{uang:>14,}")
        print(f"{'Kembalian':<25}Rp{kembalian:>14,}")
        print("=" * 42)
        print("     Terima kasih telah berbelanja!")
        print("=" * 42)

        daftar_keranjang.clear()

    except ValueError:
        print("Data barang di gudang tidak valid.")

    except FileNotFoundError:
        print("File data/gudang.txt atau data/riwayat.txt tidak ditemukan.")

    except OSError as e:
        print("Terjadi kesalahan saat menyimpan data:", e)



def lihat_riwayat_transaksi():
    print("\n========== RIWAYAT TRANSAKSI SMK MART ==========")

    try:
        with open("data/riwayat.txt", "r") as file:
            isi = file.readlines()

        ada_transaksi = False

        print("-" * 105)
        print(f"{'Tanggal':<20}{'Kode':<10}{'Nama Barang':<22}{'Harga':>10}{'Jumlah':>8}{'Subtotal':>14}{'Total':>14}")
        print("-" * 105)

        for transaksi in isi:
            data = transaksi.strip().split("|")

            if len(data) == 7 or len(data) == 8:
                status = "Aktif"

                if len(data) == 8:
                    status = data[7]

                if status == "Aktif":
                    tanggal = data[0]
                    kode = data[1]
                    nama = data[2]
                    harga = int(data[3])
                    jumlah = int(data[4])
                    subtotal = int(data[5])
                    total = int(data[6])

                    print(
                        f"{tanggal:<20}{kode:<10}{nama:<22}"
                        f"{harga:>10,}{jumlah:>8}{subtotal:>14,}{total:>14,}"
                    )

                    ada_transaksi = True

        if ada_transaksi == False:
            print("Belum ada transaksi aktif.")

        print("-" * 105)

    except FileNotFoundError:
        print("Belum ada riwayat transaksi.")

    except ValueError:
        print("Data riwayat transaksi tidak valid.")


def barang_masuk():
    print("\n========== BARANG MASUK ==========")

    kode_cari = input("Masukkan kode barang: ").strip().upper()

    if kode_cari == "":
        print("Kode barang tidak boleh kosong.")
        return

    try:
        jumlah = int(input("Masukkan jumlah barang masuk: "))

        if jumlah <= 0:
            print("Jumlah barang harus lebih dari 0.")
            return

        file = open("data/gudang.txt", "r")
        isi = file.readlines()
        file.close()

        daftar_barang = []
        ditemukan = False
        nama_barang = ""
        stok_baru = 0

        for barang in isi:
            data = barang.strip().split("|")

            if len(data) == 6:
                if data[0].upper() == kode_cari and data[5] == "Aktif":
                    nama_barang = data[1]

                    try:
                        stok_lama = int(data[3])
                    except ValueError:
                        print("Data stok barang tidak valid.")
                        return

                    stok_baru = stok_lama + jumlah
                    data[3] = str(stok_baru)

                    ditemukan = True

                    print("Nama Barang :", nama_barang)
                    print("Stok berhasil ditambahkan.")
                    print("Stok sekarang:", stok_baru)

            daftar_barang.append(data)

        if ditemukan == False:
            print("Barang aktif tidak ditemukan di daftar stok.")

            pilihan = input(
                "Apakah kamu ingin menambahkan barang baru? (y/n): "
            ).strip().lower()

            if pilihan == "y":
                tambah_barang()

            elif pilihan == "n":
                print("Kembali ke menu Gudang.")

            else:
                print("Pilihan tidak valid.")

            return

        file = open("data/gudang.txt", "w")

        for data in daftar_barang:
            file.write("|".join(data) + "\n")

        file.close()

        print("Data stok berhasil disimpan.")

        catat_barang_masuk(
            kode_cari,
            nama_barang,
            jumlah,
            stok_baru
        )

        catat_aktivitas(
            "data/gudang_aktivitas.txt",
            nama_pengguna_aktif,
            "Barang masuk " + kode_cari +
            " - " + nama_barang +
            " sebanyak " + str(jumlah)
        )

    except ValueError:
        print("Jumlah harus berupa angka bulat.")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")

    except OSError as e:
        print("Terjadi kesalahan file:", e)


def tambah_barang():
    print("\n========== TAMBAH BARANG ==========")

    try:
        file = open("data/gudang.txt", "r")
        isi = file.readlines()
        file.close()

        nomor_terakhir = 0
        daftar_kode = []

        for barang in isi:
            data = barang.strip().split("|")

            if len(data) == 6:
                kode_lama = data[0].strip().upper()

                if kode_lama.startswith("BRG"):
                    nomor = kode_lama[3:]

                    if nomor.isdigit():
                        nomor = int(nomor)
                        daftar_kode.append(kode_lama)

                        if nomor > nomor_terakhir:
                            nomor_terakhir = nomor

        kode = "BRG" + str(nomor_terakhir + 1).zfill(3)

        while kode in daftar_kode:
            nomor_terakhir += 1
            kode = "BRG" + str(nomor_terakhir + 1).zfill(3)

        print("Kode Barang Otomatis:", kode)

        nama = input("Masukkan nama barang: ").strip()

        if nama == "" or "|" in nama:
            print("Nama barang tidak valid.")
            return

        harga = int(input("Masukkan harga barang: Rp"))
        stok = int(input("Masukkan stok awal: "))
        min_stok = int(input("Masukkan stok minimum: "))

        if harga <= 0 or stok < 0 or min_stok < 0:
            print("Harga harus lebih dari 0 dan stok tidak boleh negatif.")
            return

        with open("data/gudang.txt", "a") as file:
            file.write(
                kode + "|" + nama + "|" +
                str(harga) + "|" + str(stok) + "|" +
                str(min_stok) + "|Aktif\n"
            )

        catat_aktivitas(
            "data/admin_aktivitas.txt",
            nama_pengguna_aktif,
            "Menambahkan barang " + kode + " - " + nama
        )

        print("\nBarang berhasil ditambahkan!")
        print("Kode Barang:", kode)

    except ValueError:
        print("Harga dan stok harus berupa angka bulat.")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")



def edit_barang():
    print("\n========== EDIT BARANG ==========")

    kode_cari = input("Masukkan kode barang yang ingin diedit: ").strip().upper()

    try:
        with open("data/gudang.txt", "r") as file:
            isi = file.readlines()

        daftar_barang = []
        ditemukan = False

        for barang in isi:
            data = barang.strip().split("|")

            if len(data) == 6:
                if data[0].upper() == kode_cari and data[5] == "Aktif":
                    ditemukan = True

                    print("\nData barang saat ini:")
                    print("Kode         :", data[0])
                    print("Nama         :", data[1])
                    print("Harga        : Rp", data[2])
                    print("Stok         :", data[3])
                    print("Stok minimum :", data[4])

                    print("\nTekan Enter jika ingin mempertahankan data lama.")

                    nama_baru = input("Nama barang baru: ").strip()
                    harga_baru = input("Harga baru: ").strip()
                    stok_baru = input("Stok baru: ").strip()
                    min_stok_baru = input("Stok minimum baru: ").strip()

                    if nama_baru != "":
                        if "|" in nama_baru:
                            print("Nama barang tidak valid.")
                            return
                        data[1] = nama_baru

                    if harga_baru != "":
                        harga = int(harga_baru)
                        if harga <= 0:
                            print("Harga harus lebih dari 0.")
                            return
                        data[2] = str(harga)

                    if stok_baru != "":
                        stok = int(stok_baru)
                        if stok < 0:
                            print("Stok tidak boleh negatif.")
                            return
                        data[3] = str(stok)

                    if min_stok_baru != "":
                        min_stok = int(min_stok_baru)
                        if min_stok < 0:
                            print("Stok minimum tidak boleh negatif.")
                            return
                        data[4] = str(min_stok)

                    nama_barang = data[1]

            daftar_barang.append(data)

        if ditemukan == False:
            print("Barang aktif tidak ditemukan.")
            return

        with open("data/gudang.txt", "w") as file:
            for data in daftar_barang:
                file.write("|".join(data) + "\n")

        catat_aktivitas(
            "data/admin_aktivitas.txt",
            nama_pengguna_aktif,
            "Mengedit barang " + kode_cari + " - " + nama_barang
        )

        print("\nBarang berhasil diperbarui!")

    except ValueError:
        print("Harga dan stok harus berupa angka bulat.")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")


def hapus_barang():
    print("\n========== NONAKTIFKAN BARANG ==========")

    kode_cari = input("Masukkan kode barang: ").strip().upper()

    if kode_cari == "":
        print("Kode barang tidak boleh kosong.")
        return

    try:
        with open("data/gudang.txt", "r") as file:
            isi = file.readlines()

        daftar_barang = []
        ditemukan = False
        nama_barang = ""

        for barang in isi:
            data = barang.strip().split("|")

            if len(data) == 6 and data[0].upper() == kode_cari:
                if data[5] == "Aktif":
                    ditemukan = True
                    nama_barang = data[1]

                    print("\nBarang yang akan dinonaktifkan:")
                    print("Kode :", data[0])
                    print("Nama :", data[1])
                    print("Stok :", data[3])

                    data[5] = "Tidak Aktif"

            daftar_barang.append(data)

        if ditemukan == False:
            print("Barang aktif tidak ditemukan.")
            return

        konfirmasi = input(
            "\nYakin ingin menonaktifkan barang? (y/n): "
        ).strip().lower()

        if konfirmasi != "y":
            print("Penonaktifan dibatalkan.")
            return

        verifikasi = input(
            "Ketik ulang kode barang untuk konfirmasi: "
        ).strip().upper()

        if verifikasi != kode_cari:
            print("Kode barang tidak cocok!")
            print("Penonaktifan dibatalkan.")
            return

        with open("data/gudang.txt", "w") as file:
            for data in daftar_barang:
                file.write("|".join(data) + "\n")

        catat_aktivitas(
            "data/admin_aktivitas.txt",
            nama_pengguna_aktif,
            "Menonaktifkan barang " + kode_cari + " - " + nama_barang
        )

        print("Barang berhasil dinonaktifkan!")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")


def aktifkan_barang():
    print("\n========== AKTIFKAN BARANG ==========")

    daftar_barang = []

    try:
        with open("data/gudang.txt", "r") as file:
            for baris in file:
                data = baris.strip().split("|")

                if len(data) == 6 and data[5] == "Tidak Aktif":
                    print(f"{data[0]} - {data[1]}")

                daftar_barang.append(data)

        kode = input(
            "\nMasukkan kode barang yang ingin diaktifkan: "
        ).strip().upper()

        if kode == "":
            print("Kode barang tidak boleh kosong.")
            return

        ditemukan = False
        nama_barang = ""

        for data in daftar_barang:
            if len(data) == 6 and data[0].upper() == kode and data[5] == "Tidak Aktif":
                nama_barang = data[1]
                ditemukan = True
                break

        if ditemukan == False:
            print("Barang tidak ditemukan atau sudah aktif.")
            return

        konfirmasi = input(
            "Yakin ingin mengaktifkan barang ini? (y/n): "
        ).strip().lower()

        if konfirmasi != "y":
            print("Pengaktifan barang dibatalkan.")
            return

        for data in daftar_barang:
            if len(data) == 6 and data[0].upper() == kode:
                data[5] = "Aktif"
                break

        with open("data/gudang.txt", "w") as file:
            for data in daftar_barang:
                file.write("|".join(data) + "\n")

        catat_aktivitas(
            "data/admin_aktivitas.txt",
            nama_pengguna_aktif,
            "Mengaktifkan barang " + kode + " - " + nama_barang
        )

        print("Barang berhasil diaktifkan!")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")


def kelola_akun():
    while True:
        print("\n========== KELOLA AKUN ==========")
        print("1. Daftar Akun")
        print("2. Lihat Akun")
        print("3. Nonaktifkan Akun")
        print("4. Aktifkan Akun")
        print("5. Kembali")

        pilihan_akun = input("Pilih menu: ")

        if pilihan_akun == "1":
            daftar_akun()

        elif pilihan_akun == "2":
            lihat_akun()

        elif pilihan_akun == "3":
            hapus_akun()

        elif pilihan_akun == "4":
            aktifkan_akun()

        elif pilihan_akun == "5":
            break

        else:
            print("Pilihan tidak valid!")


def lihat_akun():
    print("\n========== DAFTAR AKUN ==========")

    daftar_file = [
        "data/admin.txt",
        "data/gudang_akun.txt",
        "data/kasir.txt"
    ]

    print("-" * 75)
    print(f"{'Nama':<20}{'Username':<18}{'Role':<15}{'Status':<15}")
    print("-" * 75)

    jumlah = 0

    for nama_file in daftar_file:
        try:
            file = open(nama_file, "r")
            isi = file.readlines()
            file.close()

            for pengguna in isi:
                data = pengguna.strip().split("|")

                if len(data) == 4 or len(data) == 5:
                    status = "Aktif"

                    if len(data) == 5:
                        status = data[4]

                    print(
                        f"{data[0]:<20}"
                        f"{data[1]:<18}"
                        f"{data[3]:<15}"
                        f"{status:<15}"
                    )

                    jumlah += 1

        except FileNotFoundError:
            print("File tidak ditemukan:", nama_file)

    print("-" * 75)

    if jumlah == 0:
        print("Belum ada akun terdaftar.")



def hapus_akun():
    print("\n========== NONAKTIFKAN AKUN ==========")

    username_cari = input("Masukkan username: ").strip()

    if username_cari == "":
        print("Username tidak boleh kosong.")
        return

    daftar_file = [
        "data/admin.txt",
        "data/gudang_akun.txt",
        "data/kasir.txt"
    ]

    ditemukan = False
    nama_file_ditemukan = ""
    data_ditemukan = []

    for nama_file in daftar_file:
        file = open(nama_file, "r")
        isi = file.readlines()
        file.close()

        for pengguna in isi:
            data = pengguna.strip().split("|")

            if len(data) == 4 or len(data) == 5:
                if data[1] == username_cari:
                    ditemukan = True
                    nama_file_ditemukan = nama_file
                    data_ditemukan = data
                    break

        if ditemukan:
            break

    if ditemukan == False:
        print("Akun tidak ditemukan.")
        return

    print("\nAkun yang ditemukan:")
    print("Nama     :", data_ditemukan[0])
    print("Username :", data_ditemukan[1])
    print("Role     :", data_ditemukan[3])

    if data_ditemukan[3] == "Admin":
        print("Akun Admin tidak boleh dinonaktifkan melalui fitur ini.")
        return

    status = "Aktif"

    if len(data_ditemukan) == 5:
        status = data_ditemukan[4]

    if status == "Tidak Aktif":
        print("Akun sudah tidak aktif.")
        return

    konfirmasi = input("Yakin ingin menonaktifkan akun? (y/n): ").lower()

    if konfirmasi != "y":
        print("Penonaktifan akun dibatalkan.")
        return

    if len(data_ditemukan) == 4:
        data_ditemukan.append("Aktif")

    data_ditemukan[4] = "Tidak Aktif"

    file = open(nama_file_ditemukan, "r")
    isi = file.readlines()
    file.close()

    file = open(nama_file_ditemukan, "w")

    for pengguna in isi:
        data = pengguna.strip().split("|")

        if len(data) == 4 or len(data) == 5:
            if data[1] == username_cari:
                file.write("|".join(data_ditemukan) + "\n")
            else:
                file.write(pengguna)
        else:
            file.write(pengguna)

    file.close()

    catat_aktivitas(
        "data/admin_aktivitas.txt",
        nama_pengguna_aktif,
        "Menonaktifkan akun " + username_cari
    )

    print("Akun berhasil dinonaktifkan!")



def lihat_laporan():
    print("\n========== LAPORAN PENJUALAN SMK MART ==========")

    try:
        file = open("data/riwayat.txt", "r")
        isi = file.readlines()
        file.close()

        if len(isi) == 0:
            print("Belum ada transaksi penjualan.")
            return

        total_pendapatan = 0
        total_barang = 0

        print("-" * 90)
        print(f"{'Tanggal':<20}{'Kode':<10}{'Nama Barang':<22}{'Jumlah':>8}{'Subtotal':>15}")
        print("-" * 90)

        for transaksi in isi:
            data = transaksi.strip().split("|")

            if len(data) == 7:
                tanggal = data[0]
                kode = data[1]
                nama = data[2]
                jumlah = int(data[4])
                subtotal = int(data[5])

                total_barang = total_barang + jumlah
                total_pendapatan = total_pendapatan + subtotal

                print(
                    f"{tanggal:<20}{kode:<10}{nama:<22}"
                    f"{jumlah:>8}{subtotal:>15,}"
                )

        print("-" * 90)
        print("Total barang terjual :", total_barang)
        print(f"Total pendapatan     : Rp{total_pendapatan:,}")
        print("-" * 90)

    except FileNotFoundError:
        print("File data/riwayat.txt belum ditemukan.")

    except ValueError:
        print("Data transaksi tidak valid.")


def tambah_keranjang_kasir():
    print("\n========== TAMBAH BARANG KASIR ==========")

    try:
        with open("data/gudang.txt", "r") as file:
            isi = file.readlines()

        while True:
            kode_cari = input("\nMasukkan kode barang: ").strip().upper()

            if kode_cari == "":
                print("Kode barang tidak boleh kosong.")
                continue

            ditemukan = False

            for baris in isi:
                data = baris.strip().split("|")

                if len(data) == 6 and data[0].upper() == kode_cari and data[5] == "Aktif":
                    ditemukan = True

                    nama = data[1]
                    harga = int(data[2])
                    stok = int(data[3])

                    print("\n========== RINCIAN BARANG ==========")
                    print("Kode barang  :", kode_cari)
                    print("Nama barang  :", nama)
                    print(f"Harga        : Rp{harga:,}")
                    print("Stok tersedia:", stok)

                    barang_di_keranjang = None

                    for item in keranjang_kasir:
                        if item[0].upper() == kode_cari:
                            barang_di_keranjang = item
                            break

                    if barang_di_keranjang is not None:
                        jumlah_lama = barang_di_keranjang[3]

                        print("\nBarang sudah ada di keranjang.")
                        print("Jumlah sebelumnya:", jumlah_lama)

                        while True:
                            print("\n1. Ubah jumlah barang")
                            print("2. Tambahkan jumlah barang")
                            print("3. Kembali")

                            pilihan = input("Pilih menu: ").strip()

                            if pilihan == "1":
                                try:
                                    jumlah_baru = int(
                                        input("Masukkan jumlah baru: ")
                                    )

                                    if jumlah_baru < 0:
                                        print("Jumlah tidak boleh negatif.")
                                        continue

                                    if jumlah_baru == 0:
                                        konfirmasi = input(
                                            "Yakin ingin menghapus barang ini? (y/n): "
                                        ).strip().lower()

                                        if konfirmasi == "y":
                                            verifikasi = input(
                                                "Ketik ulang kode barang untuk konfirmasi: "
                                            ).strip().upper()

                                            if verifikasi == kode_cari:
                                                keranjang_kasir.remove(
                                                    barang_di_keranjang
                                                )

                                                catat_aktivitas(
                                                    "data/kasir_aktivitas.txt",
                                                    nama_pengguna_aktif,
                                                    "Menghapus " + nama +
                                                    " dari keranjang"
                                                )

                                                print("Barang berhasil dihapus!")

                                            else:
                                                print("Kode barang tidak cocok!")
                                                print("Penghapusan dibatalkan.")

                                        elif konfirmasi == "n":
                                            print("Penghapusan dibatalkan.")

                                        else:
                                            print("Pilihan konfirmasi tidak valid.")

                                        break

                                    if jumlah_baru > stok:
                                        print("Jumlah melebihi stok tersedia.")
                                        print("Stok tersedia:", stok)
                                        continue

                                    barang_di_keranjang[3] = jumlah_baru

                                    catat_aktivitas(
                                        "data/kasir_aktivitas.txt",
                                        nama_pengguna_aktif,
                                        "Mengubah jumlah " + nama +
                                        " menjadi " + str(jumlah_baru)
                                    )

                                    print("Jumlah barang berhasil diubah!")
                                    break

                                except ValueError:
                                    print("Masukkan angka bulat yang valid.")

                            elif pilihan == "2":
                                try:
                                    tambahan = int(
                                        input("Masukkan jumlah tambahan: ")
                                    )

                                    if tambahan <= 0:
                                        print("Jumlah harus lebih dari 0.")
                                        continue

                                    jumlah_baru = jumlah_lama + tambahan

                                    if jumlah_baru > stok:
                                        print("Jumlah melebihi stok tersedia.")
                                        print("Stok tersedia:", stok)
                                        continue

                                    barang_di_keranjang[3] = jumlah_baru

                                    catat_aktivitas(
                                        "data/kasir_aktivitas.txt",
                                        nama_pengguna_aktif,
                                        "Menambahkan jumlah " + nama +
                                        " menjadi " + str(jumlah_baru)
                                    )

                                    print("Jumlah barang berhasil ditambahkan!")
                                    break

                                except ValueError:
                                    print("Masukkan angka bulat yang valid.")

                            elif pilihan == "3":
                                break

                            else:
                                print("Pilihan tidak valid.")

                    else:
                        while True:
                            try:
                                jumlah = int(
                                    input("Masukkan jumlah: ")
                                )

                                if jumlah <= 0:
                                    print("Jumlah harus lebih dari 0.")
                                    continue

                                if jumlah > stok:
                                    print("Jumlah melebihi stok tersedia.")
                                    print("Stok tersedia:", stok)
                                    continue

                                keranjang_kasir.append(
                                    [kode_cari, nama, harga, jumlah]
                                )

                                catat_aktivitas(
                                    "data/kasir_aktivitas.txt",
                                    nama_pengguna_aktif,
                                    "Menambahkan " + nama +
                                    " sebanyak " + str(jumlah) +
                                    " ke keranjang"
                                )

                                print(
                                    "Barang berhasil ditambahkan "
                                    "ke keranjang Kasir!"
                                )
                                break

                            except ValueError:
                                print("Masukkan angka bulat yang valid.")

                    break

            if ditemukan == False:
                print("Kode barang tidak valid!")
                continue

            while True:
                tambah_lagi = input(
                    "\nApakah ingin menambahkan barang lagi? (y/n): "
                ).strip().lower()

                if tambah_lagi == "y":
                    break

                elif tambah_lagi == "n":
                    bayar(keranjang_kasir)
                    return

                else:
                    print("Masukkan pilihan y atau n.")

    except ValueError:
        print("Data barang di gudang tidak valid.")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")


def lihat_keranjang_kasir():
    print("\n========== KERANJANG KASIR ==========")

    if len(keranjang_kasir) == 0:
        print("Keranjang Kasir masih kosong.")
        return

    total = 0

    print("-" * 70)
    print(f"{'Kode':<12}{'Nama Barang':<25}{'Harga':>10}{'Jumlah':>8}{'Subtotal':>15}")
    print("-" * 70)

    for barang in keranjang_kasir:
        kode = barang[0]
        nama = barang[1]
        harga = barang[2]
        jumlah = barang[3]
        subtotal = harga * jumlah

        total = total + subtotal

        print(
            f"{kode:<12}{nama:<25}{harga:>10,}"
            f"{jumlah:>8}{subtotal:>15,}"
        )

    print("-" * 70)
    print(f"{'TOTAL BELANJA':<55}Rp{total:>12,}")
    print("-" * 70)


def lihat_stok():
    print("\n=== LAPORAN STOK BARANG ===")

    try:
        with open("data/gudang.txt", "r") as file:
            data_barang = file.readlines()

        if len(data_barang) == 0:
            print("Data barang masih kosong.")
            return

        print("-" * 85)
        print(
            f"{'Kode':<10} {'Nama Barang':<25} "
            f"{'Stok':<10} {'Min. Stok':<12} {'Status'}"
        )
        print("-" * 85)

        ada_peringatan = False

        for baris in data_barang:
            data = baris.strip().split("|")

            if len(data) != 6:
                print("Ada data barang yang formatnya tidak valid.")
                continue

            kode = data[0]
            nama = data[1]

            try:
                stok = int(data[3])
                min_stok = int(data[4])
            except ValueError:
                print(f"Stok barang {kode} tidak valid.")
                continue

            if stok < 0 or min_stok < 0:
                print(f"Data stok barang {kode} tidak valid.")
                continue

            if stok <= min_stok:
                status = "STOK MINIMUM!"
                ada_peringatan = True
            else:
                status = "Aman"

            print(
                f"{kode:<10} {nama:<25} "
                f"{stok:<10} {min_stok:<12} {status}"
            )

        print("-" * 85)

        print("\n=== PERINGATAN STOK MINIMUM ===")

        if ada_peringatan:
            for baris in data_barang:
                data = baris.strip().split("|")

                if len(data) != 5:
                    continue

                try:
                    stok = int(data[3])
                    min_stok = int(data[4])
                except ValueError:
                    continue

                if stok >= 0 and min_stok >= 0 and stok <= min_stok:
                    print(
                        f"PERINGATAN: {data[1]} ({data[0]}) "
                        f"tersedia {stok} barang, "
                        f"batas minimum {min_stok}."
                    )
        else:
            print("Semua stok barang berada di atas batas minimum.")

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")

    except OSError as e:
        print(f"Gagal membaca data stok: {e}")



def catat_barang_masuk(kode, nama, jumlah, stok_akhir):
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    try:
        with open("data/barang_masuk.txt", "a") as file:
            file.write(
                f"{tanggal}|{kode}|{nama}|"
                f"{jumlah}|{stok_akhir}\n"
            )

        print("Riwayat barang masuk berhasil dicatat.")

    except OSError as e:
        print(f"Gagal mencatat riwayat barang masuk: {e}")


def lihat_riwayat_barang_masuk():
    print("\n========== RIWAYAT BARANG MASUK ==========")

    try:
        with open("data/barang_masuk.txt", "r") as file:
            data_masuk = file.readlines()

        if len(data_masuk) == 0:
            print("Belum ada riwayat barang masuk.")
            return

        print("-" * 95)
        print(
            f"{'Tanggal':<21}{'Kode':<10}"
            f"{'Nama Barang':<25}{'Jumlah':>10}{'Stok Akhir':>15}"
        )
        print("-" * 95)

        for baris in data_masuk:
            data = baris.strip().split("|")

            if len(data) != 5:
                print("Ada catatan dengan format tidak valid.")
                continue

            tanggal = data[0]
            kode = data[1]
            nama = data[2]
            jumlah = data[3]
            stok_akhir = data[4]

            print(
                f"{tanggal:<21}{kode:<10}"
                f"{nama:<25}{jumlah:>10}{stok_akhir:>15}"
            )

        print("-" * 95)

    except FileNotFoundError:
        print("File data/barang_masuk.txt belum tersedia.")

    except OSError as e:
        print("Gagal membaca riwayat:", e)

def lihat_riwayat_barang_keluar():
    print("\n========== RIWAYAT BARANG KELUAR ==========")

    try:
        with open("data/barang_keluar.txt", "r") as file:
            data_barang = file.readlines()

        if len(data_barang) == 0:
            print("Belum ada riwayat barang keluar.")
            return

        print("-" * 110)
        print(
            f"{'Tanggal':<20} {'Kode':<10} {'Nama Barang':<22} "
            f"{'Jumlah':<10} {'Stok Akhir':<12} {'Alasan'}"
        )
        print("-" * 110)

        for baris in data_barang:
            data = baris.strip().split("|")

            if len(data) != 6:
                print("Ada data riwayat dengan format tidak valid.")
                continue

            tanggal = data[0]
            kode = data[1]
            nama = data[2]
            jumlah = data[3]
            stok_akhir = data[4]
            alasan = data[5]

            print(
                f"{tanggal:<20} {kode:<10} {nama:<22} "
                f"{jumlah:<10} {stok_akhir:<12} {alasan}"
            )

        print("-" * 110)

    except FileNotFoundError:
        print("File data/barang_keluar.txt belum tersedia.")
    except OSError as e:
        print("Gagal membaca riwayat barang keluar:", e)



def barang_keluar():
    print("\n========== BARANG KELUAR ==========")

    kode_cari = input("Masukkan kode barang: ").strip().upper()

    if kode_cari == "":
        print("Kode barang tidak boleh kosong.")
        return

    try:
        jumlah = int(input("Masukkan jumlah barang keluar: "))

        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return

    except ValueError:
        print("Jumlah harus berupa angka bulat.")
        return

    alasan = input("Alasan barang keluar: ").strip()

    if alasan == "":
        print("Alasan tidak boleh kosong.")
        return

    try:
        with open("data/gudang.txt", "r") as file:
            isi = file.readlines()

        daftar_barang = []
        ditemukan = False
        nama_barang = ""
        stok_baru = 0

        for baris in isi:
            data = baris.strip().split("|")

            if len(data) == 6 and data[0].upper() == kode_cari and data[5] == "Aktif":

                if ditemukan:
                    print("Kode barang terduplikasi.")
                    return

                try:
                    stok_lama = int(data[3])
                except ValueError:
                    print("Data stok barang tidak valid.")
                    return

                if stok_lama < 0:
                    print("Data stok barang tidak valid.")
                    return

                if jumlah > stok_lama:
                    print("Stok tidak mencukupi.")
                    print("Stok tersedia:", stok_lama)
                    return

                nama_barang = data[1]
                stok_baru = stok_lama - jumlah
                data[3] = str(stok_baru)
                ditemukan = True

                daftar_barang.append("|".join(data) + "\n")

            else:
                daftar_barang.append(baris)

        if not ditemukan:
            print("Barang aktif tidak ditemukan.")
            return

        with open("data/gudang.txt", "w") as file:
            file.writelines(daftar_barang)

        print("\nBarang keluar berhasil.")
        print("Nama barang :", nama_barang)
        print("Jumlah keluar:", jumlah)
        print("Stok sekarang:", stok_baru)

        catat_barang_keluar(
            kode_cari,
            nama_barang,
            jumlah,
            stok_baru,
            alasan
        )

        catat_aktivitas(
            "data/gudang_aktivitas.txt",
            nama_pengguna_aktif,
            "Barang keluar " + kode_cari +
            " - " + nama_barang +
            " sebanyak " + str(jumlah) +
            ". Alasan: " + alasan
        )

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")

    except OSError as e:
        print("Terjadi kesalahan file:", e)


def catat_barang_keluar(kode, nama, jumlah, stok_akhir, alasan):
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    try:
        with open("data/barang_keluar.txt", "a") as file:
            file.write(
                f"{tanggal}|{kode}|{nama}|{jumlah}|"
                f"{stok_akhir}|{alasan}\n"
            )

        print("Riwayat barang keluar berhasil dicatat.")

    except OSError as e:
        print("Gagal mencatat riwayat barang keluar:", e)


def laporan_aktivitas_gudang():
    print("\n========== LAPORAN AKTIVITAS GUDANG ==========")

    total_barang_masuk = 0
    total_barang_keluar = 0

    try:
        with open("data/barang_masuk.txt", "r") as file:
            data_masuk = file.readlines()

        for baris in data_masuk:
            data = baris.strip().split("|")

            if len(data) == 5:
                try:
                    total_barang_masuk += int(data[3])
                except ValueError:
                    continue

    except FileNotFoundError:
        data_masuk = []

    try:
        with open("data/barang_keluar.txt", "r") as file:
            data_keluar = file.readlines()

        for baris in data_keluar:
            data = baris.strip().split("|")

            if len(data) == 6:
                try:
                    total_barang_keluar += int(data[3])
                except ValueError:
                    continue

    except FileNotFoundError:
        data_keluar = []

    print("\n--- RINGKASAN AKTIVITAS ---")
    print("Total jumlah barang masuk :", total_barang_masuk)
    print("Total jumlah barang keluar:", total_barang_keluar)

    print("\n--- STOK BARANG SAAT INI ---")

    try:
        with open("data/gudang.txt", "r") as file:
            data_stok = file.readlines()

        if len(data_stok) == 0:
            print("Belum ada data barang.")

        else:
            print("-" * 65)
            print(
                f"{'Kode':<10} {'Nama Barang':<25} "
                f"{'Stok':<10} {'Min. Stok':<10}"
            )
            print("-" * 65)

            for baris in data_stok:
                data = baris.strip().split("|")

                if len(data) != 5:
                    continue

                try:
                    stok = int(data[3])
                    min_stok = int(data[4])
                except ValueError:
                    continue

                print(
                    f"{data[0]:<10} {data[1]:<25} "
                    f"{stok:<10} {min_stok:<10}"
                )

            print("-" * 65)

    except FileNotFoundError:
        print("File data/gudang.txt tidak ditemukan.")

    print("\n--- RIWAYAT BARANG MASUK ---")

    if len(data_masuk) == 0:
        print("Belum ada riwayat barang masuk.")
    else:
        for baris in data_masuk:
            data = baris.strip().split("|")

            if len(data) == 5:
                print(
                    f"Tanggal: {data[0]} | "
                    f"Barang: {data[2]} | "
                    f"Jumlah: {data[3]}"
                )

    print("\n--- RIWAYAT BARANG KELUAR ---")

    if len(data_keluar) == 0:
        print("Belum ada riwayat barang keluar.")
    else:
        for baris in data_keluar:
            data = baris.strip().split("|")

            if len(data) == 6:
                print(
                    f"Tanggal: {data[0]} | "
                    f"Barang: {data[2]} | "
                    f"Jumlah: {data[3]} | "
                    f"Alasan: {data[5]}"
                )

    print("\n========== LAPORAN SELESAI ==========")

def catat_aktivitas(nama_file, nama, aktivitas):
    tanggal = datetime.now().strftime("%d-%m-%Y")

    file = open(nama_file, "r")
    isi = file.read()
    file.close()

    file = open(nama_file, "a")

    if isi != "" and not isi.endswith("\n"):
        file.write("\n")

    file.write(tanggal + "|" + nama + "|" + aktivitas + "\n")

    file.close()


def aktifkan_akun():
    print("\n========== AKTIFKAN KEMBALI AKUN ==========")

    username_cari = input("Masukkan username: ").strip()

    if username_cari == "":
        print("Username tidak boleh kosong.")
        return

    daftar_file = [
        "data/admin.txt",
        "data/gudang_akun.txt",
        "data/kasir.txt"
    ]

    ditemukan = False
    nama_file_ditemukan = ""

    for nama_file in daftar_file:
        file = open(nama_file, "r")
        isi = file.readlines()
        file.close()

        for pengguna in isi:
            data = pengguna.strip().split("|")

            if len(data) == 5 and data[1] == username_cari:
                ditemukan = True
                nama_file_ditemukan = nama_file
                break

        if ditemukan:
            break

    if ditemukan == False:
        print("Akun tidak ditemukan atau belum memiliki status.")
        return

    if data[4] == "Aktif":
        print("Akun sudah aktif.")
        return

    print("\nAkun yang ditemukan:")
    print("Nama     :", data[0])
    print("Username :", data[1])
    print("Role     :", data[3])
    print("Status   :", data[4])

    konfirmasi = input(
        "Yakin ingin mengaktifkan akun ini? (y/n): "
    ).strip().lower()

    if konfirmasi != "y":
        print("Pengaktifan akun dibatalkan.")
        return

    file = open(nama_file_ditemukan, "r")
    isi = file.readlines()
    file.close()

    file = open(nama_file_ditemukan, "w")

    for pengguna in isi:
        data_baris = pengguna.strip().split("|")

        if len(data_baris) == 5 and data_baris[1] == username_cari:
            data_baris[4] = "Aktif"
            file.write("|".join(data_baris) + "\n")
        else:
            file.write(pengguna)

    file.close()

    catat_aktivitas(
        "data/admin_aktivitas.txt",
        nama_pengguna_aktif,
        "Mengaktifkan akun " + username_cari
    )

    print("Akun berhasil diaktifkan kembali!")


def lihat_semua_aktivitas():
    print("\n========== LAPORAN SELURUH AKTIVITAS ==========")

    daftar_file = [
        ("AKTIVITAS ADMIN", "data/admin_aktivitas.txt"),
        ("AKTIVITAS GUDANG", "data/gudang_aktivitas.txt"),
        ("AKTIVITAS KASIR", "data/kasir_aktivitas.txt")
    ]

    for judul, nama_file in daftar_file:
        print("\n" + "=" * 65)
        print(judul)
        print("=" * 65)

        try:
            with open(nama_file, "r") as file:
                isi = file.readlines()

            if len(isi) == 0:
                print("Belum ada aktivitas.")
                continue

            print("-" * 65)
            print(f"{'Tanggal':<15}{'Nama':<20}{'Aktivitas'}")
            print("-" * 65)

            for aktivitas in isi:
                data = aktivitas.strip().split("|")

                if len(data) == 3:
                    print(f"{data[0]:<15}{data[1]:<20}{data[2]}")
                else:
                    print(aktivitas.strip())

        except FileNotFoundError:
            print("File aktivitas tidak ditemukan.")

    print("\n" + "=" * 65)



print("===================================")
print("             SMK MART")
print("===================================")

while True:
    print("\nMENU UTAMA")
    print("1. Login")
    print("2. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        login()

    elif pilihan == "2":
        print("Terima kasih telah menggunakan SMK MART.")
        break

    else:
        print("Pilihan tidak valid.")

