import streamlit as st
import sqlite3
import os
from datetime import datetime
from predictor import get_response

st.set_page_config(page_title='IT Support Chatbot', page_icon='🤖', layout='wide')

st.markdown("""
<style>
.chat-user {
    background: #1e3a5f; color: white; padding: 12px 16px;
    border-radius: 18px 18px 4px 18px; margin: 6px 0;
    text-align: right; max-width: 70%; margin-left: auto;
}
.chat-bot {
    background: #f0f4ff; color: #111; padding: 12px 16px;
    border-radius: 18px 18px 18px 4px; margin: 6px 0;
    max-width: 75%;
}
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('data/query_log.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS query_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_query TEXT,
        predicted_category TEXT,
        sop_recommended TEXT
    )''')
    conn.commit()
    conn.close()

def log_query(query, category, sop):
    conn = sqlite3.connect('data/query_log.db')
    conn.execute('INSERT INTO query_log VALUES (NULL,?,?,?,?)',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), query, category, sop))
    conn.commit()
    conn.close()

init_db()

if 'messages' not in st.session_state:
    st.session_state.messages = [{
        'role': 'bot',
        'content': 'Hello! I am your IT Support Assistant. Type your IT issue and I will help you fix it.',
        'category': '', 'steps': [], 'sop': ''
    }]

col1, col2 = st.columns([4, 1])
with col1:
    st.title('🤖 IT Support Chatbot')
    st.caption('Wipro IT Support | BITS Pilani Project | Aditya Jaiswal')
with col2:
    st.metric('Queries', (len(st.session_state.messages) - 1) // 2)

st.divider()

for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',
                    unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>',
                        unsafe_allow_html=True)
            if msg.get('category'):
                st.info(f'Issue Category: {msg["category"]}')
            if msg.get('steps'):
                with st.expander('View Troubleshooting Steps', expanded=True):
                    for i, step in enumerate(msg['steps'], 1):
                        if step:
                            st.write(f'{i}. {step}')
            if msg.get('sop'):
                sop_path = f'sops/{msg["sop"]}'
                if os.path.exists(sop_path):
                    with open(sop_path, 'rb') as f:
                        st.download_button(f'Download SOP: {msg["sop"]}', f,
                                           file_name=msg['sop'])
                else:
                    st.info(f'Recommended SOP: {msg["sop"]}')

st.divider()
user_input = st.chat_input('Type your IT issue here...')

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    category, answer, steps, sop = get_response(user_input)
    log_query(user_input, category, sop)
    st.session_state.messages.append({
        'role': 'bot', 'content': answer,
        'category': category, 'steps': steps, 'sop': sop
    })
    st.rerun()