import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. ページ設定
st.set_page_config(page_title="ログ解析デモ", layout="wide")
st.title("🛡️ ログ解析ダッシュボード（プロトタイプ）")

# 2. 調査用ダミーデータの作成
@st.cache_data
def load_dummy_data():
    dates = [datetime.now() - timedelta(hours=i) for i in range(100)]
    data = pd.DataFrame({
        '日時': dates,
        'ステータス': np.random.choice(['200', '404', '500'], 100),
        'メッセージ': np.random.choice(['OK', 'Not Found', 'Internal Server Error'], 100),
        'IPアドレス': [f"192.168.1.{i}" for i in range(100)]
    })
    return data

df = load_dummy_data()

# 3. サイドバー：フィルタリング機能
st.sidebar.header("フィルタ設定")
# 期間指定
start_date = st.sidebar.date_input("開始日", datetime.now() - timedelta(days=7))
end_date = st.sidebar.date_input("終了日", datetime.now())
# ステータスフィルタ
status_filter = st.sidebar.multiselect("ステータスコード", options=['200', '404', '500'], default=['404', '500'])

# データの絞り込み（擬似）
filtered_df = df[df['ステータス'].isin(status_filter)]

# 4. トップ画面：エラー件数グラフ（時系列推移）
st.subheader("📈 エラー発生件数の時系列推移")
# 時系列用に集計
chart_data = filtered_df.resample('H', on='日時').count()['ステータス']
st.line_chart(chart_data)

# 5. 詳細画面：ログ検索＋フィルタ
st.divider()
st.subheader("🔍 詳細ログ検索")

# 検索窓
search_query = st.text_input("キーワード検索 (メッセージやIPなど)")
if search_query:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_query)).any(axis=1)]

# 詳細表示（データフレーム）
st.dataframe(filtered_df, use_container_width=True)

# ログ詳細（st.expander + st.json の組み合わせ例）
if not filtered_df.empty:
    with st.expander("選択したログのJSON全文を確認"):
        st.json(filtered_df.iloc[0].to_dict())