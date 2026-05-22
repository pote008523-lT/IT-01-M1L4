import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
import io
import warnings
warnings.filterwarnings('ignore')

# Set Streamlit page config
st.set_page_config(layout="wide", page_title="✨ Advanced Data Cleaning Workshop ✨")

# --- Custom CSS for a more unique look (Optional but adds flair) ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6; /* Light gray background */
        color: #333333;
    }
    .st-emotion-cache-zt5ig { /* Streamlit header */
        background-color: #264653; /* Dark teal */
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .css-1dp5atx.e1s3ed0e1 { /* Sidebar */
        background-color: #e9c46a; /* Earthy yellow */
        color: #333333;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #2a9d8f; /* Medium teal */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.7rem 1rem;
        font-size: 1rem;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #264653; /* Darker teal on hover */
        color: white;
    }
    .css-vk32pt.e1ewe7p86 { /* Subheader */
        color: #e76f51; /* Coral */
        font-size: 1.5rem;
        font-weight: bold;
    }
    .st-emotion-cache-16grpna { /* Markdown headers */
        color: #e76f51;
    }
    .st-emotion-cache-eq20f0.eczjsme4 { /* Main content text */
        color: #444444;
    }
</style>
""", unsafe_allow_html=True)


# --- Streamlit App Title ---
st.title("🐂✨ Data Cleaning Workshop App TaeTae ✨🐂")
st.markdown("---")
st.markdown("### ยินดีต้อนรับสู่แอปพลิเคชัน Data Cleaning สุดพิเศษ โดย TaeTae!")
st.info("💡 **คำแนะนำ:** อัปโหลดไฟล์ CSV ของคุณ (สำหรับโครงสร้าง `redbull_workshop_dirty.csv`) และเริ่มต้นกระบวนการทำความสะอาดข้อมูลได้เลย!")

# --- File Uploader ---
uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ CSV ของคุณ", type=["csv"]) # ช่องสำหรับอัปโหลดไฟล์ CSV

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    df = df_raw.copy()
    st.success("✅ อัปโหลดไฟล์สำเร็จ! เตรียมพร้อมสำหรับเวิร์คช็อปการทำความสะอาดข้อมูล")

    # Layout for raw data preview
    st.markdown("## 📊 ข้อมูลดิบของคุณ")
    with st.expander("แสดงตัวอย่างข้อมูลดิบ (5 แถวแรก)"):
        st.dataframe(df_raw.head())

    # --- Data Cleaning Steps (as functions) ---

    def perform_data_exploration(data):
        st.subheader("🔍 1. Data Exploration: เจาะลึกข้อมูลของคุณ")
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### ขนาดข้อมูล (Data Shape):")
            st.markdown(f"- **จำนวนแถว:** {data.shape[0]:,} แถว")
            st.markdown(f"- **จำนวนคอลัมน์:** {data.shape[1]} คอลัมน์")
        with col2:
            st.write("#### ข้อมูลทั่วไป (Data Info):")
            buffer = io.StringIO()
            data.info(buf=buffer)
            st.text(buffer.getvalue())

        with st.expander("📈 สถิติเชิงพรรณนา (Descriptive Statistics)"):
            st.dataframe(data.describe(include='all'))
        return data

    def handle_duplicate_data(data):
        st.subheader("👥 2. Duplicate Data: จัดการข้อมูลที่ซ้ำซ้อน")
        exact_dups = data.duplicated()
        exact_dup_count = exact_dups.sum()
        if exact_dup_count > 0:
            st.warning(f"⚠️ พบข้อมูลซ้ำ 100% จำนวน **{exact_dup_count:,} แถว**")
            with st.expander("ตัวอย่างแถวที่ซ้ำซ้อน"):
                st.dataframe(data[exact_dups])
            data = data.drop_duplicates()
            st.success(f"✅ ลบข้อมูลซ้ำสำเร็จ! ตอนนี้เหลือ **{len(data):,} แถว**")
        else:
            st.info("🎉 ไม่พบ Exact Duplicate ในชุดข้อมูลนี้")
        return data

    def handle_inconsistent_data(data):
        st.subheader("🔄 3. Inconsistent Data: แก้ไขข้อมูลที่ไม่สอดคล้องกัน")
        cat_cols = ['Region', 'Product_Variant', 'Channel']

        st.markdown("##### 📝 ก่อนแก้ไข Inconsistent Values (ค่า Unique สำหรับคอลัมน์ Categorical)")
        for col in cat_cols:
            unique_vals = data[col].unique()
            st.write(f"**📌 {col} ({len(unique_vals)} ค่า):**")
            st.code(unique_vals)

        st.markdown("##### ⚙️ กำลังดำเนินการแก้ไข Inconsistent Values...")

        # 1. Standardize Region Column
        data['Region'] = data['Region'].str.strip().str.lower()
        region_mapping = {
            'th-central': 'TH-Central', 'th central': 'TH-Central',
            'thailand central': 'TH-Central', 'thailand-central': 'TH-Central',
            'thailand': 'TH-Central',
            'usa-east': 'USA-East', 'us east': 'USA-East',
            'united states east': 'USA-East', 'u.s.a.': 'USA-East',
            'europe-eu': 'Europe-EU', 'eu': 'Europe-EU',
            'europe': 'Europe-EU', 'european union': 'Europe-EU',
            'asia-pacific': 'Asia-Pacific', 'asia-pac': 'Asia-Pacific',
            'apac': 'Asia-Pacific', 'asia pacific': 'Asia-Pacific'
        }
        data['Region'] = data['Region'].replace(region_mapping)
        data['Region'] = data['Region'].str.upper()

        # 2. Standardize Product_Variant Column
        data['Product_Variant'] = data['Product_Variant'].str.strip().str.lower()
        product_variant_mapping = {
            'original blue': 'Original Blue', 'original  blue': 'Original Blue',
            'krating daeng 250': 'Krating Daeng 250',
            'red edition': 'Red Edition',
            'sugarfree': 'Sugarfree', 'sugar free': 'Sugarfree',
            'sugarfree ': 'Sugarfree', 'sugar-free': 'Sugarfree',
            'tropical edition': 'Tropical Edition', 'tropical  edition': 'Tropical Edition',
            'tropical': 'Tropical Edition',
        }
        data['Product_Variant'] = data['Product_Variant'].replace(product_variant_mapping)

        # 3. Standardize Channel Column
        data['Channel'] = data['Channel'].str.strip().str.lower()
        channel_mapping = {
            'social media': 'Social Media', 'social_media': 'Social Media',
            'tv ad': 'TV Ad', 'tv ads': 'TV Ad',
            'tv advertisement': 'TV Ad', 'television ad': 'TV Ad',
            'in-store promo': 'In-store Promo',
            'f1 sponsorship': 'F1 Sponsorship',
            'extreme sports': 'Extreme Sports'
        }
        data['Channel'] = data['Channel'].replace(channel_mapping)
        data['Channel'] = data['Channel'].apply(lambda x: x.title() if isinstance(x, str) else x)

        # Convert Date to datetime
        data['Date'] = pd.to_datetime(data['Date'], format='mixed')

        st.success("✅ แก้ไข Inconsistent Values สำเร็จแล้ว!")
        st.markdown("##### 🟢 หลังแก้ไข Inconsistent Values (ค่า Unique สำหรับคอลัมน์ Categorical)")
        for col in cat_cols:
            unique_vals = data[col].unique()
            st.write(f"**📌 {col} ({len(unique_vals)} ค่า):**")
            st.code(unique_vals)
        return data

    def handle_missing_data(data):
        st.subheader("📭 4. Missing Data: เติมเต็มข้อมูลที่หายไป")
        missing_count = data.isnull().sum()
        total_missing = missing_count.sum()

        if total_missing > 0:
            st.markdown(f"##### 🔴 พบ Missing Values รวม **{total_missing:,} ค่า**")
            with st.expander("รายละเอียด Missing Values ก่อนแก้ไข"):
                st.dataframe(missing_count[missing_count > 0].reset_index().rename(columns={'index': 'Column', 0: 'Missing Count'}))

            # Fill Marketing_Spend with Median
            median_marketing = data['Marketing_Spend'].median()
            data['Marketing_Spend'] = data['Marketing_Spend'].fillna(median_marketing)
            st.info(f'✅ Marketing_Spend: เติมด้วย Median = **{median_marketing:,.2f}**')

            # Fill Customer_Score with Median
            median_score = data['Customer_Score'].median()
            data['Customer_Score'] = data['Customer_Score'].fillna(median_score)
            st.info(f'✅ Customer_Score: เติมด้วย Median = **{median_score}**')

            st.success("✅ แก้ไข Missing Values สำเร็จแล้ว!")
            st.markdown(f"##### 🟢 ตอนนี้มี Missing Values เหลือ: **{data.isnull().sum().sum()} ค่า** (ควรเป็น 0)")
        else:
            st.info("🎉 ไม่พบ Missing Data ในชุดข้อมูลนี้")
        return data

    def handle_noisy_data(data):
        st.subheader("📢 5. Noisy Data: กรองข้อมูลที่ผิดพลาดตาม Business Logic")
        st.markdown("##### 🕵️‍♀️ กำลังตรวจสอบ Business Logic...")
        neg_price = data[data['Unit_Price'] <= 0]
        neg_units = data[data['Units_Sold'] <= 0]
        neg_mkt = data[data['Marketing_Spend'] < 0]
        bad_score = data[(data['Customer_Score'] < 1) | (data['Customer_Score'] > 10)]

        found_noisy = False
        if not neg_price.empty:
            st.warning(f"❌ **Unit_Price ≤ 0** : พบ **{len(neg_price):,} แถว** (ราคาต้องเป็นบวก!)")
            found_noisy = True
        if not neg_units.empty:
            st.warning(f"❌ **Units_Sold ≤ 0** : พบ **{len(neg_units):,} แถว** (จำนวนที่ขายไม่ได้ติดลบ!)")
            found_noisy = True
        if not neg_mkt.empty:
            st.warning(f"❌ **Marketing_Spend < 0** : พบ **{len(neg_mkt):,} แถว** (งบการตลาดต้องไม่ติดลบ!)")
            found_noisy = True
        if not bad_score.empty:
            st.warning(f"❌ **Customer_Score ไม่ใช่ 1-10** : พบ **{len(bad_score):,} แถว** (คะแนนต้องอยู่ระหว่าง 1-10!)")
            found_noisy = True

        if found_noisy:
            initial_rows = len(data)
            data = data[data['Unit_Price'] > 0]
            data = data[data['Units_Sold'] > 0]
            data = data[data['Marketing_Spend'] >= 0]
            data = data[(data['Customer_Score'] >= 1) & (data['Customer_Score'] <= 10)]
            st.success(f"✅ แก้ไข Noisy Data สำเร็จ! ลบไป **{initial_rows - len(data):,} แถว**")
        else:
            st.info("🎉 ไม่พบ Noisy Data ที่ขัดแย้งกับ Business Logic")
        return data

    def perform_outlier_analysis(data):
        st.subheader("📐 6. Outlier Detection & Treatment: ตรวจจับและพิจารณา Outliers")
        st.markdown("##### 📊 ตรวจสอบ Outliers ด้วย Boxplot")

        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if 'Customer_Score' in numeric_cols:
            numeric_cols.remove('Customer_Score') # Handled in noisy data

        if numeric_cols:
            num_cols = len(numeric_cols)
            # Adjust columns per row based on number of numeric columns
            cols_per_row = 3 if num_cols >= 3 else num_cols
            rows_needed = (num_cols + cols_per_row - 1) // cols_per_row

            # Create a grid of plots
            st.markdown(f"กำลังแสดง Boxplot สำหรับคอลัมน์ตัวเลข {', '.join(numeric_cols)}:")
            for i in range(rows_needed):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i * cols_per_row + j
                    if idx < num_cols:
                        col_name = numeric_cols[idx]
                        with cols[j]:
                            fig, ax = plt.subplots(figsize=(6, 3)) # Smaller plots for grid
                            sns.boxplot(x=data[col_name], ax=ax, color='#2a9d8f') # Using a themed color
                            ax.set_title(f'Boxplot: {col_name}', fontsize=10)
                            ax.set_xlabel('') # Hide x-label to save space
                            st.pyplot(fig)
                            plt.close(fig)

            st.markdown("""
            **⚠️ ข้อควรระวังในการจัดการ Outliers:**
            ใน Workshop นี้ เราเลือกที่จะ **ไม่ปรับ Outliers** ด้วย `winsorize` โดยตรง เพื่อรักษาสะท้อนบริบททางธุรกิจของข้อมูลอย่างแท้จริง
            การตัดสินใจนี้สำคัญมาก! เพราะบางครั้ง Outliers อาจเป็นข้อมูลเชิงลึกที่มีค่า (เช่น ยอดขายสูงสุดเป็นประวัติการณ์)
            การจัดการ Outliers ควรพิจารณาจาก **Domain Knowledge** และ **เป้าหมายการวิเคราะห์** เป็นหลัก
            """)
        else:
            st.info("🎉 ไม่พบคอลัมน์ตัวเลขที่เหมาะสมสำหรับวิเคราะห์ Outliers")
        return data

    st.sidebar.header("⚙️ เลือกขั้นตอน Data Cleaning")
    st.sidebar.markdown("---")
    do_explore = st.sidebar.checkbox("1. Data Exploration", value=True)
    do_duplicates = st.sidebar.checkbox("2. Handle Duplicate Data", value=True)
    do_inconsistent = st.sidebar.checkbox("3. Handle Inconsistent Data", value=True)
    do_missing = st.sidebar.checkbox("4. Handle Missing Data", value=True)
    do_noisy = st.sidebar.checkbox("5. Handle Noisy Data", value=True)
    do_outlier = st.sidebar.checkbox("6. Outlier Detection", value=True)
    st.sidebar.markdown("---")

    st.markdown("---")

    if st.button("🚀 เริ่มต้นกระบวนการทำความสะอาดข้อมูล"):
        st.markdown("### 🧹 กำลังดำเนินการ Data Cleaning...")
        if do_explore:
            df = perform_data_exploration(df)
        if do_duplicates:
            df = handle_duplicate_data(df)
        if do_inconsistent:
            df = handle_inconsistent_data(df)
        if do_missing:
            df = handle_missing_data(df)
        if do_noisy:
            df = handle_noisy_data(df)
        if do_outlier:
            df = perform_outlier_analysis(df)

        st.markdown("---")
        st.subheader("✅ 7. Cleaned Data Summary: สรุปผลลัพธ์")
        col_summary1, col_summary2 = st.columns(2)
        with col_summary1:
            st.markdown(f"#### 📦 ก่อนทำความสะอาด:")
            st.markdown(f"- **จำนวนแถว:** {df_raw.shape[0]:,} แถว")
            st.markdown(f"- **จำนวนคอลัมน์:** {df_raw.shape[1]} คอลัมน์")
        with col_summary2:
            st.markdown(f"#### ✨ หลังทำความสะอาด:")
            st.markdown(f"- **จำนวนแถว:** {df.shape[0]:,} แถว")
            st.markdown(f"- **จำนวนคอลัมน์:** {df.shape[1]} คอลัมน์")

        st.markdown("### ✨ ข้อมูลที่ถูกทำความสะอาดแล้ว (5 แถวแรก)")
        st.dataframe(df.head())

        # --- Download Cleaned Data ---
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 ดาวน์โหลดข้อมูลที่ทำความสะอาดแล้ว (CSV)",
            data=csv_buffer,
            file_name="redbull_clean_enhanced.csv",
            mime="text/csv",
            help="คลิกเพื่อดาวน์โหลดชุดข้อมูลที่ผ่านการทำความสะอาด"
        )
else:
    st.info("⬆️ กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มต้นการทำความสะอาดข้อมูล")

st.markdown("---")
if st.button("🏠 กลับสู่หน้าหลัก"):
    st.switch_page("app.py")
