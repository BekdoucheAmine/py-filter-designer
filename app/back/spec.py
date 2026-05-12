import streamlit as st

class specs:
    def __init__(self, f):
        self.filter = f
    
    def get_mag_unit(self):
        return st.session_state.get("mag-unit")
    
    def get_worN(self):
        return st.session_state.get("worN")

    def get_dm(self):
        """
        """
        return st.session_state.get("design-method")

    def get_fs(self):
        dm = self.get_dm()

        if dm == "Window":
            return st.session_state.get("firwin-fs")
        elif dm == "Frequency Sampling":
            return st.session_state.get("firwin2-fs")
        elif dm == "Least Squares":
            return st.session_state.get("lst_sq-fs")
        elif dm == "Equiripple/Minimax":
            return st.session_state.get("remez-fs")
    
    def update_filter(self):
        self.filter.set_function(self.get_dm())

    def __get_window_selection_param(self):
        """

        """
        window = st.session_state.get("window")
        if window == "chebwin":
            return (window, st.session_state.get("window-chebwin_attenuation"))
        elif window == "dpss":
            return (window, st.session_state.get("window-dpss_nw"))
        elif window == "exponential":
            return (window,
                    None,
                    st.session_state.get("window-exponential_tau"))
        elif window == "gaussian":
            return (window, st.session_state.get("window-gaussian_std"))
        elif window == "general cosine":
            return (window,
                    st.session_state.get("window-general_cosine_coef_df")["Weighted Coefficients"])
        elif window == "general gaussian":
            return (window,
                    st.session_state.get("window-general_gaussian_p"),
                    st.session_state.get("window-general_gaussian_std"))
        elif window == "general hamming":
            return (window, st.session_state.get("window-general_hamming_alpha"))
        elif window in ["kaiser bessel derived", "kaiser"]:
            return (window, st.session_state.get("window-kaiser_beta"))
        elif window == "taylor":
            return (window,
                    st.session_state.get("window-taylor_nbar"),
                    st.session_state.get("window-taylor_sll"),
                    st.session_state.get("window-taylor_norm"))
        elif window == "tukey":
            return (window, st.session_state.get("window-tukey_alpha"))
        else:
            return window

    def _get_firwin_params(self):
        """

        """
        use_width = st.session_state.get("firwin-width_checkbox")
        
        return [
            st.session_state.get("firwin-numtaps"),
            st.session_state.get("firwin-df")["Frequencies"],
            st.session_state.get("firwin-width") if use_width else None,
            self.__get_window_selection_param(),
            st.session_state.get("firwin-pass_zero"),
            st.session_state.get("firwin-scale"),
            st.session_state.get("firwin-fs")]

    def _get_firwin2_params(self):
        """

        """
        use_win = st.session_state.get("firwin2-enable_window")
        return [
            st.session_state.get("firwin2-numtaps"),
            st.session_state.get("firwin2-freq_df")["Frequencies"],
            st.session_state.get("firwin2-gain_df")["Gains"],
            st.session_state.get("firwin2-nfreqs"),
            self.__get_window_selection_param() if use_win else None,
            st.session_state.get("firwin2-asym"),
            st.session_state.get("firwin2-fs")]
    
    def get_params(self):
        """

        """
        param = [] # TODO: remove this and replace with direct return
        dm = self.get_dm()
        if dm == "Window":
            return self._get_firwin_params()
        elif dm == "Frequency Sampling":
            return self._get_firwin2_params()
        elif dm == "Least Squares":
            param.extend([
                st.session_state.get("lst_sq-numtaps"),
                st.session_state.get("lst_sq-bands"),
                st.session_state.get("lst_sq-desired"),
                st.session_state.get("lst_sq-weight"),
                st.session_state.get("lst_sq-fs")
            ])
        elif dm == "Equiripple/Minimax":
            param.extend([st.session_state.get("remez-numtaps"),
                st.session_state.get("remez-bands"),
                st.session_state.get("remez-desired"),
                st.session_state.get("remez-weight"),
                st.session_state.get("remez-type"),
                st.session_state.get("remez-maxiter"),
                st.session_state.get("remez-grid_density"),
                st.session_state.get("remez-fs")
            ]) 

    def get_taps(self):
        """

        """
        self.update_filter()
        param = self.get_params()
        self.filter.set_param(param)
        return self.filter.get_taps()