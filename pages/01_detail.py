import streamlit as st
import pandas as pd

st.set_page_config(page_title="詳細ログ検索", layout="wide")
st.title("🔍 詳細ログ検索・フィルタリング")

# 本来はS3や共通のキャッシュから読み込みますが、一旦デモ用
if 'df' not in st.session_state:
    # 前のページで作ったデータがない場合は空のDFを作成（検証用）
    st.warning("メインページでデータをロードしてください。")
    st.stop()

df = st.session_state['df']

# --- フィルタエリア ---
st.sidebar.header("検索フィルタ")
selected_levels = st.sidebar.multiselect("ログレベル", options=df['level'].unique(), default=df['level'].unique())
search_keyword = st.sidebar.text_input("メッセージ検索")

# フィルタリング実行
filtered_df = df[df['level'].isin(selected_levels)]
if search_keyword:
    filtered_df = filtered_df[filtered_df['message'].str.contains(search_keyword, case=False)]

# --- メイン表示 ---
st.subheader(f"該当件数: {len(filtered_df)} 件")

# 詳細テーブル
# column_config を使うと、日時の表示形式なども細かく制御できます
st.dataframe(filtered_df, use_container_width=True)

# --- 選択したログの詳細表示 ---
st.divider()
st.subheader("📝 選択ログの詳細確認")
selected_row = st.selectbox("詳細を見たい行を選択してください", filtered_df.index)

if selected_row is not None:
    st.json(filtered_df.loc[selected_row].to_dict())