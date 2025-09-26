import streamlit as st
from datetime import date
import pandas as pd

# ===== ตั้งค่าหน้า =====
st.set_page_config(page_title="ฟอร์มใบสั่งงาน IK", page_icon="📄", layout="centered")

# ===== Header =====
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h1 style="color:#2E86C1;">📄 ใบสั่งงาน</h1>
        <h2 style="color:#117A65;">บริษัท อินะบาตะ ไทย จำกัด</h2>
        <hr style="margin-top:20px; margin-bottom:20px;">
    </div>
    """,
    unsafe_allow_html=True
)

# ===== Layout หลัก (สองคอลัมน์) =====
left_col, right_col = st.columns([1, 2])

# ===== Left: Checklist =====
with left_col:
    st.subheader("☑ รายการ")

    checklist_options = [
        "ส่งของ/เอกสาร/ตัวอย่าง",
        "รับของ/เอกสาร/ตัวอย่าง",
        "เซ็นรับใบกำกับภาษี รับสำเนากลับ 2 ใบ",
        "เซ็นรับใบกำกับภาษีและวางบิล รับต้นฉบับใบวางบิล และสำเนาใบกำกับภาษีกลับ 1 ใบ",
        "วางบิล รับต้นฉบับใบวางบิลกลับ",
        "รับเช็ค ________ ใบ",
        "อื่นๆ ________________________"
    ]

    selected_checklist = []
    for item in checklist_options:
        if st.checkbox(item):
            selected_checklist.append(item)

# ===== Right: ข้อมูลฟอร์ม =====
with right_col:
    st.subheader("📝 ข้อมูลฟอร์ม")

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

# ===== หมายเหตุ =====
remark = st.text_area("📝 หมายเหตุ / Remark")

# ===== ปุ่ม Submit =====
if st.button("✅ บันทึกข้อมูล"):
    st.success("บันทึกข้อมูลเรียบร้อย ✅")

    st.write("### == ฟอร์มใบสั่งงาน ==")
    st.write("มอบหมายให้:", assigned_to)
    st.write("วันที่สั่งงาน:", order_date)
    st.write("เวลา:", time)
    st.write("ติดต่อ:", contact)
    st.write("บริษัท:", company)
    st.write("แผนก:", department)
    st.write("ที่อยู่:", address)
    st.write("โทร:", phone)
    st.write("ผู้สั่งงาน:", ordered_by)
    st.write("ผู้รับ:", receiver)
    st.write("วันที่ (รับงาน):", receive_date)

    st.write("### == Checklist ที่เลือก ==")
    for item in selected_checklist:
        st.write("✔", item)

    st.write("### == หมายเหตุ ==")
    st.write(remark)
