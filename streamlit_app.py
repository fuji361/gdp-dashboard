import streamlit as st
import pandas as pd
import numpy as np

st.title('ログ解析プロトタイプ')

# ダミーデータの作成
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['404 Error', '500 Error', '200 OK']
)

# グラフの表示
st.line_chart(chart_data)

# 表の表示
st.subheader('詳細ログデータ（サンプル）')
st.dataframe(chart_data)