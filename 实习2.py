import streamlit as st
import pandas as pd

st.title('长三角地区PM2.5监测数据')
url_data = "https://EcnuGISChaser.github.io/gis_development/data/csj_pm25.csv"
df = pd.read_csv(url_data,encoding="utf8")
 
with st.expander("显示原始数据"):
    st.dataframe(df) 

with st.form("my_form"):
    st.header("基于属性表达式查询记录")
    month = st.selectbox('选择一个月份', ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'])
    sign = st.selectbox('选择一个表达式', ['>','<'])
    number = st.text_input('请输入一个值',value=0)
    
    if st.form_submit_button('提交'):
        if sign == '>':
            exp = (df[month] > float(number))
        else:
            exp = (df[month] < float(number))
        
        st.header(f'共有{len(df[exp])}条记录')
        st.write(df[exp])
        
        df["lon"] = df["经度"]
        df["lat"] = df["纬度"]
        st.map(df[exp])

