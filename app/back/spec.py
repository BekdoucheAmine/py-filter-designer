import streamlit as st

class specs:
    def __init__(self, f):
        self.filter = f
    
    def get_mag_unit(self):
        return st.session_state.get("mag-unit")
    
    def get_worN(self):
        return st.session_state.get("worN")

    def get_fs(self):
        self.filter.set_function(st.session_state.get("design-method"))
        dm = st.session_state.get("design-method")
        if dm == "Window":
            return st.session_state.get("window-fs")
        elif dm == "Frequency Sampling":
            return st.session_state.get("freq_smp-fs")
        elif dm == "Least Squares":
            return st.session_state.get("lst_sq-fs")
        elif dm == "Equiripple/Minimax":
            return st.session_state.get("remez-fs")
    
    def get_taps(self):
        self.filter.set_function(st.session_state.get("design-method"))
        dm = st.session_state.get("design-method")
        if dm == "Window":
            use_width = st.session_state.get("window-width_checkbox")
            param = [
                st.session_state.get("window-numtaps"),
                st.session_state.get("window-df")["Frequencies"],
                st.session_state.get("window-width") if use_width else None,
                st.session_state.get("window-window"),
                st.session_state.get("window-pass_zero"),
                st.session_state.get("window-scale"),
                st.session_state.get("window-fs")
            ]
            self.filter.set_param(param)
            return self.filter.get_taps()
        elif dm == "Frequency Sampling":
            param = [
                st.session_state.get("freq_smp-numtaps"),
                st.session_state.get("freq_smp-freq"),
                st.session_state.get("freq_smp-gain"),
                st.session_state.get("freq_smp-nfreqs"),
                st.session_state.get("freq_smp-window"),
                st.session_state.get("freq_smp-antisymmetric"),
                st.session_state.get("freq_smp-fs")
            ]
            self.filter.set_param(param)
            return self.filter.get_taps()
        elif dm == "Least Squares":
            param = [
                st.session_state.get("lst_sq-numtaps"),
                st.session_state.get("lst_sq-bands"),
                st.session_state.get("lst_sq-desired"),
                st.session_state.get("lst_sq-weight"),
                st.session_state.get("lst_sq-fs")
            ]
            self.filter.set_param(param)
            return self.filter.get_taps()
        elif dm == "Equiripple/Minimax":
            param = [
                st.session_state.get("remez-numtaps"),
                st.session_state.get("remez-bands"),
                st.session_state.get("remez-desired"),
                st.session_state.get("remez-weight"),
                st.session_state.get("remez-type"),
                st.session_state.get("remez-maxiter"),
                st.session_state.get("remez-grid_density"),
                st.session_state.get("remez-fs")
            ]
            self.filter.set_param(param)
            return self.filter.get_taps()