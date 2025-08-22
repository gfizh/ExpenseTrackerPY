import tkinter as tk
from tkinter import ttk, messagebox
import datetime, os, locale, csv

# Gunakan lokal Indonesia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
except:
    locale.setlocale(locale.LC_ALL, '')

# ====== Variabel Global ======
budget = 600000  # contoh budget bulanan
expense_categories = [
    "🍔 Makanan & Jajan",
    "🎒 Alat Sekolah",
    "🚌 Transportasi",
    "🎮 Hiburan",
    "📱 Pulsa & Internet",
    "👕 Kebutuhan Pribadi",
    "🎁 Lainnya"
]

# ====== Helper ======
def format_rupiah(amount):
    return "Rp {:,}".format(int(amount)).replace(",", ".")

def get_expense_file_path():
    bulan = datetime.datetime.now().strftime("%Y-%m")
    return f"pengeluaran_{bulan}.csv"

# ====== Simpan Data ======
def save_expense(name, amount, category):
    path = get_expense_file_path()
    file_exists = os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:  # kalau file baru, kasih header
            writer.writerow(["Tanggal", "Nama", "Nominal", "Kategori"])
        writer.writerow([datetime.date.today(), name, amount, category])

    show_summary(last_name=name, last_amount=amount, last_category=category)

# ====== Tampilkan Ringkasan (Dashboard) ======
def show_summary(last_name=None, last_amount=None, last_category=None):
    for widget in summary_frame.winfo_children():
        widget.destroy()

    totals = {}
    total_all = 0
    path = get_expense_file_path()

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amount = int(row["Nominal"])
                    category = row["Kategori"]
                    totals[category] = totals.get(category, 0) + amount
                    total_all += amount
                except:
                    continue

    # === CARD 1: Ringkasan Bulanan ===
    card1 = tk.Frame(summary_frame, bg="#fef9c3", bd=2, relief="ridge", padx=10, pady=10)
    card1.pack(fill="x", pady=5)
    tk.Label(card1, text="💰 Ringkasan Bulanan", font=("Segoe UI", 12, "bold"), bg="#fef9c3").pack(anchor="w")
    tk.Label(card1, text=f"Total Pengeluaran: {format_rupiah(total_all)}", bg="#fef9c3").pack(anchor="w")
    tk.Label(card1, text=f"Budget: {format_rupiah(budget)}", bg="#fef9c3").pack(anchor="w")
    tk.Label(card1, text=f"Sisa Budget: {format_rupiah(budget - total_all)}", bg="#fef9c3").pack(anchor="w")

    # === CARD 2: Total per Kategori ===
    card2 = tk.Frame(summary_frame, bg="#dbeafe", bd=2, relief="ridge", padx=10, pady=10)
    card2.pack(fill="x", pady=5)
    tk.Label(card2, text="📊 Total per Kategori", font=("Segoe UI", 12, "bold"), bg="#dbeafe").pack(anchor="w")
    if totals:
        for cat, amt in totals.items():
            tk.Label(card2, text=f"{cat}: {format_rupiah(amt)}", bg="#dbeafe").pack(anchor="w")
    else:
        tk.Label(card2, text="Belum ada data.", bg="#dbeafe").pack(anchor="w")

    # === CARD 3: Transaksi Terakhir ===
    card3 = tk.Frame(summary_frame, bg="#fce7f3", bd=2, relief="ridge", padx=10, pady=10)
    card3.pack(fill="x", pady=5)
    tk.Label(card3, text="📝 Transaksi Terakhir", font=("Segoe UI", 12, "bold"), bg="#fce7f3").pack(anchor="w")
    if last_name:
        tk.Label(card3, text=f"{last_name} - {last_category} - {format_rupiah(last_amount)}", bg="#fce7f3").pack(anchor="w")
    else:
        tk.Label(card3, text="Belum ada transaksi terbaru.", bg="#fce7f3").pack(anchor="w")

# ====== Submit Form ======
def submit_expense():
    name = entry_name.get().strip()
    amount = entry_amount.get().strip()
    category = combo_category.get()

    if not name or not amount or not category:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")
        return
    try:
        amount = int(amount)
    except:
        messagebox.showerror("Error", "Nominal harus angka!")
        return

    save_expense(name, amount, category)
    entry_name.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

# ====== UI ======
root = tk.Tk()
root.title("📊 Tracker Keuangan Anak Sekolah")
root.geometry("500x600")
root.configure(bg="white")

title = tk.Label(root, text="📊 Tracker Keuangan", font=("Segoe UI", 16, "bold"), bg="white")
title.pack(pady=10)

form_frame = tk.Frame(root, bg="white")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Nama Pengeluaran:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(form_frame, width=30)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Nominal (Rp):", bg="white").grid(row=1, column=0, sticky="w", pady=5)
entry_amount = tk.Entry(form_frame, width=30)
entry_amount.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Kategori:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
combo_category = ttk.Combobox(form_frame, values=expense_categories, width=28, state="readonly")
combo_category.grid(row=2, column=1, pady=5)

btn_submit = tk.Button(root, text="Tambah Pengeluaran", command=submit_expense, bg="#4ade80", fg="black", font=("Segoe UI", 10, "bold"))
btn_submit.pack(pady=10)

summary_frame = tk.Frame(root, bg="white")
summary_frame.pack(fill="both", expand=True, padx=10, pady=10)

show_summary()
root.mainloop()
