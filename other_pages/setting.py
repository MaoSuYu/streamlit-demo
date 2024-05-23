import streamlit as st

st.set_page_config(page_title="Chat with LLM", page_icon=":smiley:", layout="wide")

conn = st.connection('mysql', type='sql')

# Perform query.
df_chat_info = conn.query("""SELECT
	tci.*,
	wui.`name`,
	wui.nick_name 
FROM
	tb_chat_info AS tci
	LEFT JOIN wechat_user_info AS wui ON tci.user_id = wui.wechat_user_id 
ORDER BY
	tci.create_time DESC""", ttl=600)
st.data_editor(data=df_chat_info)

chat_id = st.text_input(placeholder='search by chat_id', label="Chat ID")
if st.button(label="Search", key="search button"):
    if chat_id:
        df_chat = conn.query(f"""SELECT * from tb_chat where chat_id='{chat_id}';""", ttl=600)
        st.data_editor(data=df_chat)

chat_line_chart=conn.query(f"""SELECT 
    DATE(`create_time`) AS date,
    COUNT(*) AS total
FROM 
    `tb_chat_info`
WHERE 
    `create_time` >= DATE_FORMAT(CURDATE() ,'%Y-%m-01') 
    AND `create_time` < DATE_FORMAT(DATE_ADD(CURDATE() ,INTERVAL 1 MONTH) ,'%Y-%m-01')
GROUP BY 
    DATE(`create_time`)
ORDER BY 
    date;""", ttl=600)
st.line_chart(chat_line_chart)

"""""
    mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
    because it conflicts with mysql (which contains client libraries).
    
    If you need to have mysql-client first in your PATH, run:
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
    
    For compilers to find mysql-client you may need to set:
    export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
    
    For pkg-config to find mysql-client you may need to set:
    export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
"""""
