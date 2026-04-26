import streamlit as st
import pandas as pd
import math as m

def render_type(border=True, height="stretch", width="stretch"):
    """Renders filter type."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Filter Type")
        st.selectbox("Filter Type", ["FIR"], #, "IIR"], Not supported yet
                      key='f-type', label_visibility="hidden")

def render_options(border=True, height="stretch", width="stretch"):
    """Renders options selection."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Options")
        dm = st.session_state.get("design-method")
        if dm == "Window":
            # default values
            if "window-numtaps" not in st.session_state:
                st.session_state["window-numtaps"] = 29
            if "window-width" not in st.session_state:
                st.session_state["window-width"] = 0.0001
            if "window-window" not in st.session_state:
                st.session_state["window-window"] = 'hamming'
            if "window-pass_zero" not in st.session_state:
                st.session_state["window-pass_zero"] = False
            if "window-scale" not in st.session_state:
                st.session_state["window-scale"] = False
            if "window-fs" not in st.session_state:
                st.session_state["window-fs"] = 1000

            st.slider("Number of taps", min_value=1, max_value=128, value=29, step=1, key="window-numtaps",
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
                            step=int(10**(m.ceil(m.log10(st.session_state.get("window-fs"))/3))), value=1000, key="window-fs")
        elif dm == "Frequency Samping":
            pass
        elif dm == "Least Squares":
            pass
        elif dm == "Equiripple/Minimax":
            pass
        else:
            raise ValueError("Design Method not supported")

def render_dm(border=True, height="stretch", width="stretch"):
    """Renders design method."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Design Method")
        f_type = st.session_state.get("f-type")
        if f_type == "FIR":
            st.selectbox("Design Method",
                         ["Window"], #, "Frequency Sampling", "Least Squares", "Equiripple/Minimax"], Not Supported Yet
                         key="design-method",
                         label_visibility="hidden")
        elif f_type == "IIR":
            st.selectbox("Design Method",
                         [""],
                         key="design-method",
                         label_visibility="hidden")
        else:
            raise ValueError("Filter type can either be FIR or IIR")

def render_plot(plt, border=True, height="stretch", width="stretch"):
    """Renders Frequency Response using Plotly"""
    freq_rsp = plt
    with st.container(border=border, height=height, width=width):
        st.subheader("Frequency Response")
        freq_rsp.update()
        freq_rsp.render()

def render_plot_param(border=True, height="stretch", width="stretch"):
    """Renders Plot Parameters"""
    with st.container(border=border, height=height, width=width):
        st.subheader("Plot Parameters")
        st.slider("worN", min_value=512, max_value=2048, value=512, key='worN')
        st.selectbox("Magnitude Unit", ["RAW", "dB"], key='mag-unit')

def render_summary(border=True, height="stretch", width="stretch"):
    """Renders Summary."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Summary")

def render_taps(taps, border=True, height="stretch", width="stretch"):
    """Renders Taps"""
    with st.container(border=border, height=height, width=width):
        st.subheader("Coefficients")
        st.code(taps, "python", wrap_lines=True, height=300)

def render_taps_param(border=True, height="stretch", width="stretch"):
    """Renders Taps"""
    with st.container(border=border, height=height, width=width):
        st.subheader("Coef Format")
        taps_fmt = st.selectbox("Numerical Representation", ["float", "fixed", "csd", "raw"], key="taps-num_rep")
        if taps_fmt != "float":
            width = st.slider("Total Bits", min_value=1, max_value=128, value=16, key="taps-width")
            frac = st.slider("Fractional Bits", min_value=0, max_value=width, value=15, key="taps-frac")
            if taps_fmt in ["fixed", "raw"]:
                out_fmt = st.selectbox("Output Format", ["Dec", "Bin", "Hex"], key="taps-out_fmt")
            else:
                out_fmt = None
        
