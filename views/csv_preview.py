"""CSV 预览（纯本地，不依赖 API）"""
import streamlit as st
import pandas as pd
import theme

theme.apply()
theme.page_header("CSV 预览", "上传表格，自动展示内容、统计与图表。完全本地运行，无需联网")

uploaded = st.file_uploader("选择 CSV 文件", type=["csv"])

if uploaded is not None:
    try:
        try:
            df = pd.read_csv(uploaded)
        except UnicodeDecodeError:
            uploaded.seek(0)
            df = pd.read_csv(uploaded, encoding="gbk")

        st.markdown("##### 数据预览（前 100 行）")
        st.dataframe(df.head(100), use_container_width=True)

        st.markdown("##### 基本信息")
        c1, c2, c3 = st.columns(3)
        c1.metric("行数", df.shape[0])
        c2.metric("列数", df.shape[1])
        c3.metric("缺失值总数", int(df.isna().sum().sum()))

        st.markdown("##### 各列说明")
        info = pd.DataFrame({
            "列名": df.columns,
            "类型": [str(t) for t in df.dtypes],
            "非空数量": [int(df[c].notna().sum()) for c in df.columns],
            "唯一值数量": [int(df[c].nunique()) for c in df.columns],
        })
        st.dataframe(info, use_container_width=True)

        num_df = df.select_dtypes(include="number")
        if not num_df.empty:
            st.markdown("##### 数值列统计")
            st.dataframe(num_df.describe().T, use_container_width=True)

            st.markdown("##### 快速图表")
            col = st.selectbox("选择一个数值列绘图", list(num_df.columns))
            kind = st.radio("图表类型", ["柱状图", "折线图"], horizontal=True)
            data = num_df[col].head(50)
            if kind == "柱状图":
                st.bar_chart(data, color="#1E3A5F")
            else:
                st.line_chart(data, color="#1E3A5F")
        else:
            st.info("没有检测到数值列，跳过图表。")
    except Exception as e:
        st.error(f"读取失败：{e}")
else:
    st.info("还没有文件。可以先用任意一个 CSV 试试，例如导出一份 Excel 表格为 CSV。")
