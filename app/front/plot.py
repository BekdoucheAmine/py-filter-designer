from plotly import graph_objects as go
from scipy.signal import *
import numpy as np
import streamlit as st

class plotter:
    """
        instead of a single huge function to plot the frequency graph its done using this class
    """
    def __init__(self, specs, pad=8):
        self.fig = go.Figure()
        self.specs = specs
        self.pad = pad
    def __calc_freq_rsp(self):
        """
            uses the given specs to provide frequency response of the filter
        """
        w, h = freqz(self.specs.get_taps(),
                               worN=self.specs.get_worN(),
                               fs=self.specs.get_fs())
        self.w = w
        self.h = np.abs(h)
        self.mag_db = 20 * np.log10(self.h)   
    def __add_line_marker(self, x0, y0, x1, y1, txt):
        """
            x0, y0, x1, y1: coordinates, line will be drawn from point 0 to point 1
            txt: string, txt will be placed on (x0,x1)/2 | y0+self.pad
        """
        # add line
        self.fig.add_shape(
            type="line",
            x0=x0, y0=y0,
            x1=x1, y1=y1,
            line=dict(color="black", dash="dash", width=1)
        )
        # add text
        self.fig.add_annotation(
            x=(x0+x1)/2, y=y0,
            text=txt,
            yshift=self.pad,
            showarrow=False,
            font=dict(color="black")
        )
    def __add_rect_marker(self, x0, y0, x1, y1, color, txt):
        """
           x0, y0, x1, y1: coordinates, rectangle will be drawn from point 0 to point 1
           color: fill color for the rectangle
           txt: string, txt will be placed in the center of the the rectangle
        """
        self.fig.add_shape(
            type="rect",
            x0=x0, y0=y0,
            x1=x1, y1=y1,
            fillcolor=color,
            opacity=0.1,
            line_width=0,
            layer="below"
        )

        self.fig.add_annotation(
            x=(x0+x1)/2, y=(y0+y1)/2,
            text=txt,
            showarrow=False,
            font=dict(color="black")
        )
    def _add_region_marker(self):
        """
            f0, f1: frequency
            a0, a1: magnitude 
            txt: tuple->(freq-txt,mag-txt,reg-txt) string values
            color: fill color (string)
            mode: "lowpass", "highpass", "bandpass", "bandstop"
        """
        dm = self.specs.get_dm()
        param = self.specs.get_params()

        if dm == "Window":
            freqs = list(param[1]) # band frequencies
            width = param[2] # transition width
            pass_zero = param[4] # pass zero
            
            # magnitude regions
            apass = np.max(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.max(self.h)
            astop = np.max(self.mag_db)-6 if self.specs.get_mag_unit()=="dB" else np.max(self.h)*0.25
            amin = np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h)
            if pass_zero:
                freqs.insert(0, np.min(self.w))
            else:
                self.__add_line_marker(np.min(self.w), astop,
                                    freqs[0], astop,
                                    "Astop")
                self.__add_line_marker(np.min(self.w), amin,
                                    freqs[0], amin,
                                    "")
                self.__add_rect_marker(np.min(self.w), astop,
                                    freqs[0], amin,
                                    "red",
                                    "")
            for i in range(len(freqs)):
                if i < len(freqs)-1:
                    if i%2 == 0:
                        self.__add_line_marker(freqs[i], apass,
                                            freqs[i+1], apass,
                                            "Apass")
                        self.__add_line_marker(freqs[i], astop,
                                            freqs[i+1], astop,
                                            "")
                        self.__add_rect_marker(freqs[i], apass,
                                            freqs[i+1], astop,
                                            "green",
                                            "")
                    if i%2 == 1:
                        self.__add_line_marker(freqs[i], astop,
                                            freqs[i+1], astop,
                                            "Astop")
                        self.__add_line_marker(freqs[i], amin,
                                            freqs[i+1], amin,
                                            "")
                        self.__add_rect_marker(freqs[i], astop,
                                            freqs[i+1], amin,
                                            "red",
                                            "")
                else:
                    if i%2 == 0:
                        self.__add_line_marker(freqs[i], apass,
                                            np.max(self.w), apass,
                                            "Apass")
                        self.__add_line_marker(freqs[i], astop,
                                            np.max(self.w), astop, "")
                        self.__add_rect_marker(freqs[i], apass,
                                            np.max(self.w), astop,
                                            "green",
                                            "")
                    if i%2 == 1:
                        self.__add_line_marker(freqs[i], astop,
                                            np.max(self.w), astop,
                                            "Astop")
                        self.__add_line_marker(freqs[i], amin,
                                            np.max(self.w), amin,
                                            "")
                        self.__add_rect_marker(freqs[i], astop,
                                            np.max(self.w), amin,
                                            "red",
                                            "")
    def _add_freq_response(self):
        """
            add frequency response trace to the figure (self.fig)
        """
        self.fig.add_trace(go.Scatter(
            x=self.w, 
            y=self.mag_db if self.specs.get_mag_unit()=="dB" else self.h, 
            mode='lines',
            name='Frequency Response',
            line=dict(color='blue', width=2))
        )
    def update(self):
        # remove all traces
        self.fig.data = []
        self.fig.layout.shapes = []
        self.fig.layout.annotations = []
        # recalculate frequency response
        self.__calc_freq_rsp()
        # add frequency response trace
        self._add_freq_response()
        # add annotations
        self._add_region_marker()
    def render(self):
        st.plotly_chart(self.fig, height="stretch", width="stretch")