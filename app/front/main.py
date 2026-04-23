import streamlit as st
import pandas as pd
import math as m
from front.plot import plotter
from back.spec import specs

def render_sidebar():
    """Renders Side Bar"""
    with st.sidebar:
        st.title("")
        st.markdown("")
        st.selectbox("Filter Type", ["FIR", "IIR"], key='f-type')

def render_options(border=True):
    """Renders options selection."""
    with st.container(border=border):
        st.subheader("Options")
        dm = st.session_state.get("design-method")
        if dm == "Window":
            # default values
            if "window-numtaps" not in st.session_state:
                st.session_state["window-numtaps"] = 9
            if "window-width" not in st.session_state:
                st.session_state["window-width"] = None
            if "window-window" not in st.session_state:
                st.session_state["window-window"] = 'hamming'
            if "window-pass_zero" not in st.session_state:
                st.session_state["window-pass_zero"] = True
            if "window-scale" not in st.session_state:
                st.session_state["window-scale"] = False
            if "window-fs" not in st.session_state:
                st.session_state["window-fs"] = 1000

            st.slider("Number of taps", min_value=1, max_value=128, value=9, step=1, key="window-numtaps",
                      help= "Length of the filter (number of coefficients, i.e., the filter order + 1)"+\
                            ". numtaps must be odd if a passband includes the Nyquist frequency.")

            updated_df = st.data_editor(pd.DataFrame({"Frequencies": [100.0, 200.0, 300.0, 400.0]}), num_rows="dynamic",
                           column_config={
                                "Frequencies": st.column_config.NumberColumn(
                                    "Frequency (Hz)",
                                    help="Must be between 0 and Nyquist, and strictly increasing.",
                                    min_value=0.0001,
                                    max_value=st.session_state.get("window-fs")-0.0001,
                                    format="engineering",
                                )},
                            hide_index=True,
                            key="window-cutoff",
                            )
            st.session_state["window-df"] = updated_df

            st.checkbox("Transition Width", value=False, key='window-width_checkbox')
            st.slider("Transition Width",
                      min_value=0.0001,
                      max_value=st.session_state.get("window-fs")/2-0.0001,
                      value=0.0001,
                      disabled=not st.session_state.get("window-width_checkbox"),
                      key="window-width",
                      label_visibility="hidden")
    
            st.checkbox("Pass Zero (DC)", value=False, key='window-pass_zero')
            st.checkbox("Scale Coefficients", value=False, key='window-scale')
            st.number_input("Sample Frequency",
                            step=int(10**(m.ceil(m.log10(st.session_state.get("window-fs"))/3))), value=1000)
        elif dm == "Frequency Samping":
            pass
        elif dm == "Least Squares":
            pass
        elif dm == "Equiripple/Minimax":
            pass
        else:
            raise ValueError("Design Method not supported")

def render_dm(border=True):
    """Renders design method."""
    with st.container(border=border):
        st.subheader("Design Method")
        f_type = st.session_state.get("f-type")
        if f_type == "FIR":
            st.selectbox("Design Method",
                         ["Window", "Frequency Sampling", "Least Squares", "Equiripple/Minimax"],
                         key="design-method",
                         label_visibility="hidden")
        elif f_type == "IIR":
            st.selectbox("Design Method",
                         [""],
                         key="design-method",
                         label_visibility="hidden")
        else:
            raise ValueError("Filter type can either be FIR or IIR")

def render_plot(border=True):
    """Renders Frequency Response using Plotly"""
    s = specs()
    freq_rsp = plotter(s)
    with st.container(border=border):
        st.subheader("Frequency Response")
        freq_rsp.update()
        freq_rsp.render()

def render_graph_settings(border=True):
    """Renders Graph Settings"""
    st.slider("worN", min_value=512, max_value=2048, value=512, key='worN')
    st.selectbox("Magnitude Unit", ["RAW", "dB"], key='mag-unit')

def render_summary(border=True):
    """Renders Summary."""
    with st.container(border=border):
        st.subheader("Summary")
