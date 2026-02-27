import streamlit as st
import pandas as pd

st.set_page_config(page_title="GDP詳細ページ", layout="wide")
st.title("🌍 GDP詳細ページ")

# データ読み込み
@st.cache_data
def load_data():
    return pd.read_csv('data/gdp_data.csv')

df = load_data()

# --- フィルタエリア ---
st.sidebar.header("検索フィルタ")
search_keyword = st.sidebar.text_input("国名・指標名で検索")
year_range = st.sidebar.slider("年範囲を選択", 1960, 2022, (2000, 2022))

# 検索・フィルタ処理
filtered = df.copy()

if search_keyword:
    filtered = filtered[
        filtered['Country Name'].str.contains(search_keyword, case=False, na=False) |
        filtered['Indicator Name'].str.contains(search_keyword, case=False, na=False)
    ]
year_cols = [str(y) for y in range(year_range[0], year_range[1]+1)]

display_cols = ['Country Name', 'Country Code', 'Indicator Name'] + year_cols
filtered = filtered[display_cols]

# --- メイン表示 ---
st.subheader(f"該当件数: {len(filtered)} 件")
st.dataframe(filtered, use_container_width=True)