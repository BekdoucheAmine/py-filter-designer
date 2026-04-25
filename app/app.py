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
        render_type()
        render_dm()

    with col1:
        render_options()
    with col3:
        render_plot_param()
        render_taps_param()
        render_taps(coef.get_taps())
    with col2:
        render_plot(plt)

if __name__ == "__main__":
    main()