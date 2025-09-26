import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
from fpdf import FPDF

# ===== ตั้งค่าหน้า =====
st.set_page_config(page_title="ฟอร์มใบสั่งงาน IK", page_icon="📄", layout="centered")

# ===== Header =====
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h1 style="color:#2E86C1;">📋 ฟอร์มใบสั่งงาน</h1>
        <h2 style="color:#117A65;">บริษัท อินะบาตะ ไทย จำกัด</h2>
        <hr style="margin-top:20px; margin-bottom:20px;">
    </div>
    """,
    unsafe_allow_html=True
)

# ===== DB Setup =====
conn = sqlite3.connect("work_orders.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS work_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assigned_to TEXT,
    order_date TEXT,
    time TEXT,
    contact TEXT,
    company TEXT,
    department TEXT,
    address TEXT,
    phone TEXT,
    ordered_by TEXT,
    receiver TEXT,
    receive_date TEXT,
    checklist TEXT,
    remark TEXT
)
""")
conn.commit()

# ===== ฟอร์มกรอกข้อมูล =====
with st.form("work_order_form", clear_on_submit=True):
    assigned_to = st.text_input("มอบหมายให้", "DRIVER TXE")
    order_date = st.date_input("วันที่สั่งงาน", date.today())
    time = st.text_input("เวลา")
    contact = st.text_input("ติดต่อ")
    company = st.text_input("บริษัท", "STI PRECISION")
    department = st.text_input("แผนก")
    address = st.text_area("ที่อยู่")
    phone = st.text_input("โทร")
    ordered_by = st.text_input("ผู้สั่งงาน", "SIRAPAT")
    receiver = st.text_input("ผู้รับ")
    receive_date = st.date_input("วันที่ (รับงาน)", date.today())

    st.markdown("### ☑ รายการ")
    checklist_options = [
        "ส่งของ/เอกสาร/ตัวอย่าง",
        "รับของ/เอกสาร/ตัวอย่าง",
        "เซ็นรับใบกำกับภาษี รับสำเนากลับ 2 ใบ",
        "เซ็นรับใบกำกับภาษีและวางบิล รับต้นฉบับใบวางบิล และสำเนาใบกำกับภาษีกลับ 1 ใบ",
        "วางบิล รับต้นฉบับใบวางบิลกลับ",
        "รับเช็ค ________ ใบ",
        "อื่นๆ ________________________"
    ]
    checklist = st.multiselect("เลือก Checklist", checklist_options)

    remark = st.text_area("📝 หมายเหตุ / Remark")

    submitted = st.form_submit_button("✅ บันทึกข้อมูล")
    if submitted:
        c.execute("""
        INSERT INTO work_orders (
            assigned_to, order_date, time, contact, company, department,
            address, phone, ordered_by, receiver, receive_date, checklist, remark
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assigned_to, str(order_date), time, contact, company, department,
            address, phone, ordered_by, receiver, str(receive_date),
            ", ".join(checklist), remark
        ))
        conn.commit()
        st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว!")

# ===== ดึงข้อมูลทั้งหมด =====
st.markdown("---")
st.subheader("📑 ข้อมูลที่บันทึกไว้")

df = pd.read_sql_query("SELECT * FROM work_orders ORDER BY id DESC", conn)
st.dataframe(df, use_container_width=True)

# ===== ฟังก์ชันสร้าง PDF =====
def generate_pdf(row):
    pdf = FPDF()
    pdf.add_page()

    # ✅ ฟอนต์ไทย (ต้องมีไฟล์ THSarabunNew.ttf ในโฟลเดอร์เดียวกัน)
    pdf.add_font("THSarabunNew", "", "THSarabunNew.ttf", uni=True)
    pdf.set_font("THSarabunNew", "", 16)

    # หัวเรื่อง
    pdf.set_font("THSarabunNew", "B", 20)
    pdf.cell(0, 15, "📋 ใบสั่งงาน", ln=True, align="C")
    pdf.ln(5)

    # วาดตาราง
    pdf.set_font("THSarabunNew", "", 16)
    col_width = 50
    row_height = 10

    for key, value in row.items():
        pdf.cell(col_width, row_height, str(key), border=1)
        pdf.multi_cell(0, row_height, str(value), border=1)

    # ✅ คืนค่า bytes (ไม่ต้อง encode)
    return pdf.output(dest="S").encode("latin-1")

# ===== ปุ่มพิมพ์ / ดาวน์โหลด PDF =====
if not df.empty:
    latest_row = df.iloc[0]
    pdf_file = generate_pdf(latest_row)

    st.download_button(
        label="🖨️ พิมพ์ / ดาวน์โหลด PDF",
        data=pdf_file,
        file_name="work_order.pdf",
        mime="application/pdf"
    )
