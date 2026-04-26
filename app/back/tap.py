import numpy as np
import streamlit as st

class taps():
    def __init__(self, s):
        self.specs = s

    def get_taps(self):
        """
            desc: Get filter coefficient (to copy and implement elsewhere)
            in:
                num_rep: float, fixed, csd, raw (str)
                out_fmt: dec, bin, hex (str)
                width: number of bits (int) defaults to 32
                frac: number of fractional bits (int) < width defaults to 16
            out:
                taps: list in desired format (int or str)
        """
        num_rep = st.session_state.get("taps-num_rep")
        if num_rep == "float":
            return self.get_float()
        elif num_rep == "fixed":
            out_fmt = st.session_state.get("taps-out_fmt")
            width = st.session_state.get("taps-width")
            frac = st.session_state.get("taps-frac")
            taps = self.get_fixed(out_fmt, width, frac)
        elif num_rep == "csd":
            width = st.session_state.get("taps-width")
            frac = st.session_state.get("taps-frac")
            taps = self.get_csd(width, frac)
        elif num_rep == "raw":
            out_fmt = st.session_state.get("taps-out_fmt")
            width = st.session_state.get("taps-width")
            frac = st.session_state.get("taps-frac")
            taps = self.get_raw(out_fmt, width, frac)
        else:
            raise ValueError("Numerical representations are limit to float, fixed, csd, raw")
        return taps
    
    def get_float(self):
        float_taps = []
        for tap in self.specs.get_taps():
            float_taps.append(float(tap))
        return float_taps
    def get_fixed(self, out_fmt, width, frac):
        """
            desc: convert taps to fixed point format
            in:
                out_fmt: dec, bin, hex (str)
                width: number of bits (int)
                frac: number of fractional bits (int) < width
            out:
                taps: list in desired format (int or str)
        """
        fix_taps = []
        mask = (1 << width) - 1 
        for tap in self.specs.get_taps():
            ival = int(round(tap * (2**frac)))
            if ival > (1 << (width - 1)) - 1 or ival < -(1 << (width - 1)):
                ValueError("Conversion overflow, set a higher width")

            if out_fmt == "dec":
                fix_taps.append(ival)
            elif out_fmt == "bin":
                fix_taps.append(np.binary_repr(ival, width=width))
            elif out_fmt == "hex":
                hex_width = (width + 3) // 4
                fix_taps.append(format(ival & mask, f'0{hex_width}x')) 
        return fix_taps
    def to_csd(self, n, width):

        res = ""
        temp_n = n
        for _ in range(width):
            if temp_n % 2 == 0:
                digit = "0"
                temp_n //= 2
            else:
                # If next bit is also 1, this is a sequence; use -1
                if (temp_n // 2) % 2 == 1:
                    digit = "-"
                    temp_n = (temp_n + 1) // 2
                else:
                    digit = "+"
                    temp_n //= 2
            res = digit + res
        return res
    def get_csd(self, width, frac):
        """
            desc: Converts taps to Canonical Signed Digit strings.
            in:
                out_fmt: dec, bin, hex (str)
                width: number of bits (int)
                frac: number of fractional bits (int) < width
            out:
                taps: list in desired format (int or str)
        """
        csd_taps = []
        for tap in self.specs.get_taps():
            n = int(round(tap * (2**frac)))
            is_negative = n < 0
            temp_n = abs(n)
            csd_tap = self.to_csd(temp_n, width)
            if is_negative:
                csd_tap = csd_tap.replace('+', '_').replace('-', '+').replace('_', '-')
            csd_taps.append(csd_tap)
        return csd_taps

    def get_raw(self, out_fmt, width):
        """
            desc: Scales coefficients to the maximum possible range for a given bit-width.
            in:
                out_fmt: dec, bin, hex (str)
                width: number of bits (int) defaults to 32
            out:
                taps: list in desired format (int or str)
        """
        taps = self.specs.get_taps()
        max_tap = max(abs(t) for t in taps)
        max_int = (1 << (width - 1)) - 1 
        scale_factor = max_int / max_tap
        
        raw_taps = []
        mask = (1 << width) - 1
        
        for tap in taps:
            ival = int(round(tap * scale_factor))
            if out_fmt == "dec":
                raw_taps.append(ival)
            elif out_fmt == "bin":
                raw_taps.append(np.binary_repr(ival, width=width))
            elif out_fmt == "hex":
                hex_width = (width + 3) // 4
                raw_taps.append(format(ival & mask, f'0{hex_width}x'))       
        return raw_taps