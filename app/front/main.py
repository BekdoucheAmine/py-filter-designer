import streamlit as st
import pandas as pd
import math as m

def render_type(border=True, height="stretch", width="stretch"):
    """Renders filter type."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Filter Type")
        st.selectbox("Filter Type", ["FIR"], #, "IIR"], Not supported yet
                      key='f-type', label_visibility="hidden")

def __render_options_window_selection():
    """
    """
    window = st.selectbox("Window", ["hamming", "barthann", "bartlett", "blackman",
                                     "blackmanharris", "bohman", "boxcar", "chebwin",
                                     "cosine", "dpss", "exponential", "flattop",
                                     "gaussian", "general cosine", "general gaussian", "general hamming",
                                     "hann", "kaiser", "kaiser bessel derived", "lanczos",
                                     "nuttall", "parzen", "taylor", "triangle",
                                     "tukey"], key="window")
    if window == "chebwin":
        st.number_input("Attenuation (dB)", key="window-chebwin_attenuation")
    elif window == "dpss":
        st.slider("Standardized half bandwidth", min_value=0.00001, max_value=st.session_state.get("numtaps")/2-0.0001, key="window-dpss_nw")
    elif window == "exponential":
        st.number_input("Tau", value=60, key="window-exponential_tau")
    elif window == "gaussian":
        st.number_input("Standard Deviation", value=10, key="window-gaussian_std")
    elif window == "general cosine":
        updated_df = st.data_editor(pd.DataFrame({"Weighted Coefficients": [0.36, 0.49, 0.14, 0.01]}), num_rows="dynamic",
                    column_config={
                        "Weighted Coefficients": st.column_config.NumberColumn(
                            "Weighted Coefficients",
                            help="Sequence of weighting coefficients. This uses the convention of being centered on the origin, so these will typically all be positive numbers, not alternating sign.",
                            min_value=0,
                            max_value=1.0,
                            format="plain",
                        )},
                    hide_index=True,
                    key="window-general_cosine_coef",
                    )
        st.session_state["window-general_cosine_coef_df"] = updated_df
    elif window == "general gaussian":
        st.slider("Shape Parameter", min_value=0.0, value=0.5, max_value=1.0, key="window-general_gaussian_p")
        st.number_input("Standard Deviation", value=10, key="window-general_gaussian_std")
    elif window == "general hamming":
        st.slider("Window Coefficient", min_value=0.0, value=0.5, max_value=1.0, key="window-general_hamming_alpha")
    elif window in ["kaiser bessel derived", "kaiser"]:
        st.slider("Shape Parameter", min_value=0.0, value=0.5, max_value=1.0, key="window-kaiser_beta")
    elif window == "taylor":
        st.number_input("Adjacent Side-lobes", key="window-taylor_nbar")
        st.number_input("Suppression Level (dB)", key="window-taylor_sll")
        st.checkbox("Normalize", value=True, key="window-taylor_norm")
    elif window == "tukey":
        st.slider("Shape Parameter", min_value=0.0, value=0.5, max_value=1.0, key="window-tukey_alpha")

def _render_options_firwin():
    """

    """
    # default values
    if "firwin-numtaps" not in st.session_state:
        st.session_state["firwin-numtaps"] = 29
    if "firwin-width" not in st.session_state:
        st.session_state["firwin-width"] = 0.0001
    if "firwin-window" not in st.session_state:
        st.session_state["firwin-window"] = 'hamming'
    if "firwin-pass_zero" not in st.session_state:
        st.session_state["firwin-pass_zero"] = False
    if "firwin-scale" not in st.session_state:
        st.session_state["firwin-scale"] = False
    if "firwin-fs" not in st.session_state:
        st.session_state["firwin-fs"] = 1000

    numtaps = st.slider("Number of taps", min_value=1, max_value=128, value=29, step=1, key="firwin-numtaps",
                        help= "Length of the filter (number of coefficients, i.e., the filter order + 1)"+\
                        ". numtaps must be odd if a passband includes the Nyquist frequency.")
    st.session_state["numtaps"] = numtaps

    updated_df = st.data_editor(pd.DataFrame({"Frequencies": [100.0, 200.0, 300.0, 400.0]}), num_rows="dynamic",
                    column_config={
                        "Frequencies": st.column_config.NumberColumn(
                            "Frequency (Hz)",
                            help="Must be between 0 and Nyquist, and strictly increasing.",
                            min_value=0.0001,
                            max_value=st.session_state.get("firwin-fs")/2-0.0001,
                            format="engineering",
                        )},
                    hide_index=True,
                    key="firwin-cutoff",
                    )
    st.session_state["firwin-df"] = updated_df

    st.checkbox("Transition Width", value=False, key='firwin-width_checkbox')
    st.slider("Transition Width",
                min_value=0.0001,
                max_value=st.session_state.get("firwin-fs")/2-0.0001,
                value=0.0001,
                disabled=not st.session_state.get("firwin-width_checkbox"),
                key="firwin-width",
                label_visibility="hidden")
    
    __render_options_window_selection()
    
    st.checkbox("Pass Zero (DC)", value=False, key='firwin-pass_zero')
    st.checkbox("Scale Coefficients", value=False, key='firwin-scale')
    st.number_input("Sample Frequency",
                    step=int(10**(m.ceil(m.log10(st.session_state.get("firwin-fs"))/3))), value=1000, key="firwin-fs")

def _render_options_firwin2():
    """

    """
    # default values
    if "firwin2-numtaps" not in st.session_state:
        st.session_state["firwin2-numtaps"] = 29
    if "firwin2-window" not in st.session_state:
        st.session_state["firwin2-window"] = 'hamming'
    if "firwin2-fs" not in st.session_state:
        st.session_state["firwin2-fs"] = 1000

    numtaps = st.slider("Number of taps", min_value=1, max_value=128, value=29, step=1, key="firwin2-numtaps",
                        help= "Length of the filter (number of coefficients, i.e., the filter order + 1)"+\
                        ". numtaps must be odd if a passband includes the Nyquist frequency.")
    st.session_state["numtaps"] = numtaps
    
    updated_df = st.data_editor(pd.DataFrame({"Frequencies": [0.0, 200.0, 400.0, 500.0]}), num_rows="dynamic",
                    column_config={
                        "Frequencies": st.column_config.NumberColumn(
                            "Frequency (Hz)",
                            help="Must be between 0 and Nyquist, and strictly increasing.",
                            min_value=0.0001,
                            max_value=st.session_state.get("firwin2-fs")/2-0.0001,
                            format="engineering",
                        )},
                    hide_index=True,
                    key="firwin2-freq",
                    )
    st.session_state["firwin2-freq_df"] = updated_df
    
    updated_df = st.data_editor(pd.DataFrame({"Gains": [1.0, 0.5, 0.1, 0.0]}), num_rows="dynamic",
                    column_config={
                        "Gains": st.column_config.NumberColumn(
                            "Gain (raw)",
                            format="engineering",
                        )},
                    hide_index=True,
                    key="firwin2-gain",
                    )
    st.session_state["firwin2-gain_df"] = updated_df

    st.slider("Interpolation Size", min_value=st.session_state.get("firwin2-numtaps")+1,
            value=st.session_state.get("firwin2-numtaps")+1, max_value=1000, step=1, key="firwin2-nfreqs")
    
    window = st.checkbox("Use Window", value=False, key='firwin2-enable_window')

    if window:
        __render_options_window_selection()
    
    st.checkbox("Anti-symmetric", value=False, key='firwin2-asym')

    st.number_input("Sample Frequency",
                    step=int(10**(m.ceil(m.log10(st.session_state.get("firwin2-fs"))/3))), value=1000, key="firwin2-fs")

def render_options(border=True, height="stretch", width="stretch"):
    """Renders options selection."""
    with st.container(border=border, height=height, width=width):
        st.subheader("Options")
        dm = st.session_state.get("design-method")
        if dm == "Window":
            _render_options_firwin()
        elif dm == "Frequency Sampling":
            _render_options_firwin2()
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
                         ["Window", "Frequency Sampling"], #, "Least Squares", "Equiripple/Minimax"], Not Supported Yet
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
        
