import tkinter as tk
from tkinter import ttk, messagebox
from expense import Expense
import datetime, calendar, locale, os

# Gunakan lokal Indonesia jika tersedia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
except:
    locale.setlocale(locale.LC_ALL, '')

# Kategori
expense_categories = ["🍔 Makanan", "🏠 Rumah", "💼 Pekerjaan", "🎉 Hiburan", "🛍️ Belanja"]

# Budget tetap
budget = 2_000_000

# Format Rupiah
def format_rupiah(amount):
    return f"Rp{locale.format_string('%d', amount, grouping=True)}"

# Dapatkan path file sesuai bulan dan tahun
def get_expense_file_path():
    now = datetime.datetime.now()
    filename = f"pengeluaran_{now.year}_{now.month:02}.csv"
    return filename

# Simpan pengeluaran
def save_expense(name, amount, category):
    try:
        amount = float(amount)
        path = get_expense_file_path()
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{name},{amount},{category}\n")
        messagebox.showinfo("Berhasil", f"Pengeluaran {name} disimpan!")
        show_summary()
    except ValueError:
        messagebox.showerror("Error", "Jumlah pengeluaran harus berupa angka!")

# Tampilkan ringkasan
def show_summary():
    path = get_expense_file_path()
    if not os.path.exists(path):
        messagebox.showinfo("Info", "Belum ada data pengeluaran bulan ini.")
        return

    with open(path, "r", encoding="utf-8") as f:
        expenses = [
            Expense(name, float(amount), category)
            for name, amount, category in (line.strip().split(",") for line in f)
        ]

    total_by_cat = {}
    for e in expenses:
        total_by_cat[e.category] = total_by_cat.get(e.category, 0) + e.amount

    total_spent = sum(e.amount for e in expenses)
    remaining = budget - total_spent

    # ALERT jika dana habis
    if remaining <= 0:
        messagebox.showwarning("⚠️ Budget Habis", "⚠️ Dana bulanan telah habis!")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_remaining = remaining / remaining_days if remaining_days > 0 else 0
    daily_plan = budget / days_in_month

    summary = "\n📁 Total per Kategori:\n"
    for cat, total in total_by_cat.items():
        summary += f"  {cat}: {format_rupiah(total)}\n"
    summary += f"\n💰 Total Bulanan: {format_rupiah(total_spent)}"
    summary += f"\n💡 Sisa Budget: {format_rupiah(remaining)}"
    summary += f"\n\n📅 Hari Ini: {now.strftime('%d %B %Y')}"
    summary += f"\nSisa Hari Bulan Ini: {remaining_days} hari"
    summary += f"\n\n📊 Budget Harian Awal: {format_rupiah(daily_plan)}"
    summary += f"\n✅ Budget Harian Tersisa: {format_rupiah(daily_remaining)}"

    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)

# ========== UI ========== #
root = tk.Tk()
root.title("📊 Pemantau Pengeluaran Harian")

# Form input
tk.Label(root, text="Nama Pengeluaran:").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Jumlah (Rp):").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(root, width=30)
amount_entry.grid(row=1, column=1)

tk.Label(root, text="Kategori:").grid(row=2, column=0, sticky="w")
category_combo = ttk.Combobox(root, values=expense_categories, state="readonly", width=28)
category_combo.grid(row=2, column=1)
category_combo.current(0)

tk.Button(root, text="Simpan Pengeluaran", command=lambda: save_expense(name_entry.get(), amount_entry.get(), category_combo.get())).grid(row=3, column=0, columnspan=2, pady=10)

# Summary
summary_text = tk.Text(root, height=15, width=60)
summary_text.grid(row=4, column=0, columnspan=2)

tk.Button(root, text="Lihat Ringkasan", command=show_summary).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
