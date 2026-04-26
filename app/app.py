import streamlit as st
from back.filter import filter
from back.spec import specs
from back.tap import taps
from front.main import *
from front.plot import plotter

def main():
    st.set_page_config(page_title="Filter Designer", layout="wide")
    st.title("Filter Characteristics")
    st.markdown("")

    col1, col2, col3 = st.columns((1,3,1))

    sidebar = st.sidebar
    
    f = filter()
    spec = specs(f)
    plt = plotter(spec)
    coef = taps(spec)
    
    with sidebar:
        render_type(border=False, width="content")
        render_dm(border=False, width="content")

    with col1:
        render_options(height="content")
    with col3:
        render_plot_param(height="content")
        render_taps_param(height="content")
        render_taps(coef.get_taps(), height="content")
    with col2:
        render_plot(plt)

if __name__ == "__main__":
    main()