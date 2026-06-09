import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard', page_icon='📊', layout='wide')
st.title('📊 IT Support Chatbot — Dashboard')

def load_data():
    conn = sqlite3.connect('data/query_log.db')
    try:
        df = pd.read_sql('SELECT * FROM query_log', conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

df = load_data()

if len(df) == 0:
    st.warning('No data yet. Use the chatbot first.')
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric('Total Queries', len(df))
col2.metric('Issue Types', df['predicted_category'].nunique())
col3.metric('SOPs Given', df['sop_recommended'].notna().sum())

st.divider()

col_a, col_b = st.columns(2)
with col_a:
    st.subheader('Queries by Issue Type')
    counts = df['predicted_category'].value_counts().reset_index()
    counts.columns = ['Category', 'Count']
    fig = px.bar(counts, x='Category', y='Count',
                 color='Count', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader('Category Split')
    fig2 = px.pie(counts, names='Category', values='Count')
    st.plotly_chart(fig2, use_container_width=True)

st.subheader('All Queries')
st.dataframe(
    df[['timestamp','user_query','predicted_category','sop_recommended']
    ].sort_values('timestamp', ascending=False),
    use_container_width=True
)