import streamlit as st

st.set_page_config(page_title="MyApp", layout="wide")

st.title("🏠 หน้าหลัก ")
st.write("### Boot Camp: Data Science and Machine Learning")
st.info("7 Day Intensive Hands-on Workshop")
st.write("Kritsana")
st.write("##### Day 1: การจัดการข้อมูลพื้นฐานและโครงสร้างข้อมูลด้วย Python")

# if st.button("🏠 กลับหน้าหลัก "):
   # st.switch_page("app.py")

if st.button("💰ระบบคำนวณส่วนลดตามยอดซื้อ"):
    st.switch_page("pages/app1_discount_calc.py")
elif st.button("✨การทำความสะอาดข้อมูล"):
    st.switch_page("pages/clean_app_Taev2.py")
elif st.button("📂เครื่องมือทำความสะอาดข้อมูลลูกค้า"):
    st.switch_page("pages/clean_customers.py")
