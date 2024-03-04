mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
ebableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml