import customtkinter as ctk
from datetime import date

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ฟอร์มใบสั่งงาน IK บริษัท อินะบาตะ ไทย จำกัด")
app.geometry("1000x800")

# ===== Header =====
header = ctk.CTkLabel(
    app,
    text="📄 ใบสั่งงาน",
    font=ctk.CTkFont(size=28, weight="bold")
)
header.pack(pady=15)

# ===== Main Frame (แนวนอน) =====
main_frame = ctk.CTkFrame(app, corner_radius=12)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

main_frame.grid_columnconfigure(0, weight=1, uniform="col")
main_frame.grid_columnconfigure(1, weight=2, uniform="col")

# ===== Left: Checklist =====
left_frame = ctk.CTkFrame(main_frame, corner_radius=12)
left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

ctk.CTkLabel(
    left_frame,
    text="☑ รายการ",
    font=ctk.CTkFont(size=18, weight="bold")
).pack(anchor="w", pady=(10, 15), padx=10)

checkbox_texts = [
    "ส่งของ/เอกสาร/ตัวอย่าง",
    "รับของ/เอกสาร/ตัวอย่าง",
    "เซ็นรับใบกำกับภาษี รับสำเนากลับ 2 ใบ",
    "เซ็นรับใบกำกับภาษีและวางบิล\nรับต้นฉบับใบวางบิล และสำเนาใบกำกับภาษีกลับ 1 ใบ",
    "วางบิล รับต้นฉบับใบวางบิลกลับ",
    "รับเช็ค ________ ใบ",
    "อื่นๆ ________________________"
]

checkbox_vars = []
for text in checkbox_texts:
    var = ctk.BooleanVar()
    cb = ctk.CTkCheckBox(left_frame, text=text, variable=var, font=ctk.CTkFont(size=14))
    cb.pack(anchor="w", pady=5, padx=15)
    checkbox_vars.append((var, text))

# ===== Right: ข้อมูลฟอร์ม =====
right_frame = ctk.CTkFrame(main_frame, corner_radius=12)
right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

entry_fields = {}

def create_row(label, default=""):
    row = ctk.CTkFrame(right_frame)
    row.pack(fill="x", pady=6, padx=10)
    ctk.CTkLabel(row, text=label, width=120, anchor="w").pack(side="left", padx=(0, 10))
    entry = ctk.CTkEntry(row, placeholder_text=label)
    entry.insert(0, default)
    entry.pack(side="left", fill="x", expand=True)
    entry_fields[label] = entry

create_row("มอบหมายให้", "DRIVER TXE")
create_row("วันที่สั่งงาน", date.today().strftime("%d.%m.%Y"))
create_row("เวลา", "")
create_row("ติดต่อ", "")
create_row("บริษัท", "STI PRECISION")
create_row("แผนก", "")
create_row("ที่อยู่", "")
create_row("โทร", "")
create_row("ผู้สั่งงาน", "SIRAPAT")
create_row("ผู้รับ", "")
create_row("วันที่ (รับงาน)", "28.08.2027")

# ===== หมายเหตุ =====
remark_frame = ctk.CTkFrame(app, corner_radius=12)
remark_frame.pack(fill="both", expand=False, padx=20, pady=(5, 10))

ctk.CTkLabel(
    remark_frame,
    text="📝 หมายเหตุ / Remark",
    font=ctk.CTkFont(size=16, weight="bold")
).pack(anchor="w", pady=(8, 5), padx=10)

entry_remark = ctk.CTkTextbox(remark_frame, height=100)
entry_remark.pack(padx=15, pady=(0, 10), fill="x")

# ===== Submit Button =====
def submit_form():
    print("== ฟอร์มใบสั่งงาน ==")
    for label, entry in entry_fields.items():
        print(f"{label}: {entry.get()}")
    print("== Checklist ที่เลือก ==")
    for var, text in checkbox_vars:
        if var.get():
            print("✔", text)
    print("== หมายเหตุ ==")
    print(entry_remark.get("1.0", "end").strip())

submit_btn = ctk.CTkButton(
    app,
    text="✅ บันทึกข้อมูล",
    font=ctk.CTkFont(size=16, weight="bold"),
    command=submit_form,
    height=40,
    corner_radius=10
)
submit_btn.pack(pady=20)

app.mainloop()
