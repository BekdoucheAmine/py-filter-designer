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
            x0=x0, y0=y0+self.pad,
            x1=x1, y1=y1+self.pad,
            line=dict(color="black", dash="dash", width=1)
        )
        # add text
        self.fig.add_annotation(
            x=(x0+x1)/2, y=y0+self.pad,
            text=txt,
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
    def __add_freq_marker(self, f, txt):
        """
            f: frequency, draws a vertical line at this magnitude
            txt: string, placed at the top of the vertical line
        """
        self.__add_line_marker(f, np.max(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.max(self.h),
                               f, np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                               txt)    
    def __add_mag_marker(self, a, f0, f1, txt):
        """
            a: magnitude, draws a horizontal line from f0,f1 at this magnitude
            f0: start frequency
            f1: stop frequency
            txt: string, placed at the center of the line with vertical pads
        """
        self.__add_line_marker(f0, a,
                               f1, a,
                               txt)       
    def _add_region_marker(self, f0, f1, a0, a1, mode):
        """
            f0, f1: frequency
            a0, a1: magnitude 
            txt: tuple->(freq-txt,mag-txt,reg-txt) string values
            color: fill color (string)
            mode: "lowpass", "highpass", "bandpass", "bandstop"
        """
        if mode == "lowpass":
            # pass region
            self._add_freq_marker(f0, "Fpass")
            self._add_mag_marker(a0/2.0, np.min(self.w), f0, "Apass")
            self._add_mag_marker(-a0/2.0, np.min(self.w), f0, "")
            self.__add_rect_marker(np.min(self.w), a0/2.0,
                                   f0, -a0/2.0,
                                   "green",
                                   "")
            # stop region
            self._add_freq_marker(f1, "Fstop")
            self._add_mag_marker(a1, f1, np.max(self.w), "Astop")
            self.__add_rect_marker(f1, a1,
                                   np.max(self.w), np.max(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.max(self.h),
                                   "red",
                                   "")
        elif mode == "highpass":
            # stop region
            self._add_freq_marker(f0, "Fstop")
            self._add_mag_marker(a0, np.min(self.w), f0, "Astop")
            self.__add_rect_marker(np.min(self.w), np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                                   f0, a0,
                                   "red",
                                   "")
            # pass region
            self._add_freq_marker(f1, "Fpass")
            self._add_mag_marker(a1/2.0, "Apass")
            self._add_mag_marker(-a1/2.0, "")
            self.__add_rect_marker(f1, a1/2.0,
                                   np.max(self.w), -a1/2.0,
                                   "green",
                                   "")
        elif mode == "bandpass":
            # pass region
            self._add_freq_marker(f0[0]-f0[1]/2.0, "Fpass")
            self._add_freq_marker(f0[0]+f0[1]/2.0, "")
            self._add_mag_marker(a0/2.0, f0[0]-f0[1]/2.0, f0[0]+f0[1]/2.0, "Apass")
            self._add_mag_marker(-a0/2.0, f0[0]-f0[1]/2.0, f0[0]+f0[1]/2.0, "")
            self.__add_rect_marker(f0[0]-f0[1]/2.0, a0/2.0,
                                   f0[0]+f0[1]/2.0, -a0/2.0,
                                   "green",
                                   "")
            # stop region
            self._add_freq_marker(f1[0], "Fstop")
            self._add_freq_marker(f1[1], "")
            self._add_mag_marker(a1, np.min(self.w), f1[0], "Astop")
            self._add_mag_marker(a1, f1[1], np.max(self.w), "")
            self.__add_rect_marker(np.min(self.w), a1,
                                   f1[0], np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                                   "red",
                                   "")
            self.__add_rect_marker(f1[0], a1,
                                   np.max(self.w), np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                                   "red",
                                   "")
            
        elif mode == "bandstop":
            # stop region
            self._add_freq_marker(f0[0]-f0[1]/2.0, "Fstop")
            self._add_freq_marker(f0[0]+f0[1]/2.0, "")
            self._add_mag_marker(a0/2.0, f0[0]-f0[1]/2.0, f0[0]+f0[1]/2.0, "Astop")
            self._add_mag_marker(-a0/2.0, f0[0]-f0[1]/2.0, f0[0]+f0[1]/2.0, "")
            self.__add_rect_marker(f0[0]-f0[1]/2.0, a0/2.0,
                                   f0[0]+f0[1]/2.0, -a0/2.0,
                                   "red",
                                   "")
            
            # pass region
            self._add_freq_marker(f1[0], "Fpass")
            self._add_freq_marker(f1[1], "")
            self._add_mag_marker(a1, np.min(self.w), f1[0], "Apass")
            self._add_mag_marker(a1, f1[1], np.max(self.w), "")
            self.__add_rect_marker(np.min(self.w), a1,
                                   f1[0], np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                                   "green",
                                   "")
            self.__add_rect_marker(f1[0], a1,
                                   np.max(self.w), np.min(self.mag_db) if self.specs.get_mag_unit()=="dB" else np.min(self.h),
                                   "green",
                                   "")
        else:
            raise ValueError("mode is a Literal, hence value can either be 'lowpass', 'highpass', 'bandpass', 'band_stop'")  
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
        # recalculate frequency response
        self.__calc_freq_rsp()
        # add frequency response trace
        self._add_freq_response()
        # add annotations
        # self._add_region_marker(self.specs.get_f0(),
        #                         self.specs.get_f1(),
        #                         self.specs.get_a0(),
        #                         self.specs.get_a1(),
        #                         self.specs.get_resp_type())
    def render(self):
        st.plotly_chart(self.fig)