import tkinter as tk               # Library untuk membuat GUI
from tkinter import ttk, messagebox # ttk = widget modern, messagebox = popup
from expense import Expense         # Import class Expense dari file expense.py
import datetime, calendar, locale, os # Modul bawaan Python untuk waktu, kalender, bahasa, dan file

# Gunakan bahasa Indonesia jika tersedia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
except:
    locale.setlocale(locale.LC_ALL, '')

# Daftar kategori pengeluaran
expense_categories = ["🍔 Makanan", "🏠 Rumah", "💼 Kebutuhan", "🎉 Hiburan", "🛍️ Belanja"]

# Budget bulanan tetap
budget = 2_000_000

# Fungsi ubah angka ke format Rupiah
def format_rupiah(amount):
    return f"Rp{locale.format_string('%d', amount, grouping=True)}"

# Fungsi tentukan nama file sesuai bulan & tahun
def get_expense_file_path():
    now = datetime.datetime.now()
    filename = f"pengeluaran_{now.year}_{now.month:02}.csv"
    return filename

# Fungsi hitung total per kategori
def get_total_by_category(category):
    path = get_expense_file_path()
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        expenses = [
            Expense(name, float(amount), cat)
            for name, amount, cat in (line.strip().split(",") for line in f)
        ]
    total = sum(e.amount for e in expenses if e.category == category)
    return total

# Fungsi simpan data pengeluaran ke file CSV
def save_expense(name, amount, category):
    try:
        amount = float(amount)  # Ubah input jadi angka
        path = get_expense_file_path()
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{name},{amount},{category}\n")  # Simpan data

        # Hitung total kategori terbaru
        total_cat = get_total_by_category(category)

        # Popup sukses
        messagebox.showinfo(
            "Berhasil",
            f"✅ Pengeluaran berhasil dicatat!\n\n"
            f"📝 Nama: {name}\n"
            f"💵 Jumlah: {format_rupiah(amount)}\n"
            f"📂 Kategori: {category}\n\n"
            f"➡️ Total {category} sekarang: {format_rupiah(total_cat)}"
        )

        # Tampilkan ringkasan + info transaksi terakhir di summary_text
        show_summary(name, amount, category, total_cat)

    except ValueError:
        messagebox.showerror("Error", "Jumlah pengeluaran harus berupa angka!")

# Fungsi tampilkan ringkasan pengeluaran
def show_summary(last_name=None, last_amount=None, last_category=None, last_total=None):
    path = get_expense_file_path()
    if not os.path.exists(path):
        messagebox.showinfo("Info", "Belum ada data pengeluaran bulan ini.")
        return

    # Baca semua pengeluaran
    with open(path, "r", encoding="utf-8") as f:
        expenses = [
            Expense(name, float(amount), category)
            for name, amount, category in (line.strip().split(",") for line in f)
        ]

    # Hitung total per kategori
    total_by_cat = {}
    for e in expenses:
        total_by_cat[e.category] = total_by_cat.get(e.category, 0) + e.amount

    # Hitung total bulanan
    total_spent = sum(e.amount for e in expenses)
    remaining = budget - total_spent

    # Hitung sisa hari
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_remaining = remaining / remaining_days if remaining_days > 0 else 0
    daily_plan = budget / days_in_month

    # Buat teks ringkasan
    summary = "📊 RINGKASAN PENGELUARAN\n"
    summary += "=" * 40 + "\n\n"

    summary += "📁 Total per Kategori:\n"
    for cat, total in total_by_cat.items():
        summary += f"  • {cat}: {format_rupiah(total)}\n"

    summary += f"\n💰 Total Bulanan: {format_rupiah(total_spent)}"
    summary += f"\n💡 Sisa Budget: {format_rupiah(remaining)}"
    summary += f"\n\n📅 Hari Ini: {now.strftime('%d %B %Y')}"
    summary += f"\n🗓️ Sisa Hari Bulan Ini: {remaining_days} hari"
    summary += f"\n\n📊 Budget Harian Awal: {format_rupiah(daily_plan)}"
    summary += f"\n✅ Budget Harian Tersisa: {format_rupiah(daily_remaining)}"

    # Tambahkan catatan transaksi terakhir
    if last_name and last_amount and last_category:
        summary += "\n\n📝 TRANSAKSI TERAKHIR\n"
        summary += "-" * 40 + "\n"
        summary += f"Nama: {last_name}\n"
        summary += f"Jumlah: {format_rupiah(last_amount)}\n"
        summary += f"Kategori: {last_category}\n"
        summary += f"➡️ Total {last_category}: {format_rupiah(last_total)}"

    # Tampilkan di kotak teks
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)

# ========== UI (Antarmuka) ==========
root = tk.Tk()
root.title("📊 Pemantau Pengeluaran Harian")

# Input nama pengeluaran
tk.Label(root, text="Nama Pengeluaran:").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1)

# Input jumlah uang
tk.Label(root, text="Jumlah (Rp):").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(root, width=30)
amount_entry.grid(row=1, column=1)

# Pilihan kategori
tk.Label(root, text="Kategori:").grid(row=2, column=0, sticky="w")
category_combo = ttk.Combobox(root, values=expense_categories, state="readonly", width=28)
category_combo.grid(row=2, column=1)
category_combo.current(0)

# Tombol simpan
tk.Button(
    root, text="Simpan Pengeluaran",
    command=lambda: save_expense(name_entry.get(), amount_entry.get(), category_combo.get())
).grid(row=3, column=0, columnspan=2, pady=10)

# Kotak teks ringkasan
summary_text = tk.Text(root, height=20, width=60)
summary_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Tombol lihat ringkasan
tk.Button(root, text="Lihat Ringkasan", command=show_summary).grid(row=5, column=0, columnspan=2, pady=10)

# Jalankan aplikasi
root.mainloop()
