import streamlit as st
from front.main import *

def main():
    st.set_page_config(page_title="Filter Designer", layout="wide")
    st.title("Filter Characteristics")
    st.markdown("")

    render_sidebar()

    m_col1, m_col2, m_col3 = st.columns(3, vertical_alignment="top")
    with m_col1:
        render_dm()
    with m_col2:
        render_options()
    with m_col3:
        render_graph_settings()

    render_plot()

if __name__ == "__main__":
    main()