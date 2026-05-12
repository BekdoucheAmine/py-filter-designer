from scipy.signal import firwin, firwin2, firls, remez, kaiser_atten, kaiser_beta
from scipy.signal._arraytools import _validate_fs
from scipy.signal.windows import get_window, general_cosine
from scipy._lib._array_api import array_namespace, xp_size, xp_default_dtype
import scipy._lib.array_api_extra as xpx

class filter:
    """
    """
    def __init__(self):
        """
        """
        self.f_name = None
        self.f = None
        self.param = None
    def set_function(self, f_name):
        """
        """
        self.f_name = f_name
        if f_name == "Window":
            self.f = self._firwin
        elif f_name == "Frequency Sampling":
            self.f = firwin2
        elif f_name == "Least Squares":
            self.f = firls
        elif f_name == "Equiripple/Minimax":
            self.f = remez
        else:
            raise ValueError("Function not supported at the moment")
    def set_param(self, param):
        """
        """
        if self.f_name == "Window":
            self.param = {
                "numtaps": param[0],
                "cutoff": param[1],
                "width": param[2],
                "window": param[3],
                "pass_zero": param[4],
                "scale": param[5],
                "fs": param[6]
            }
        elif self.f_name == "Frequency Sampling":
            self.param = {
                "numtaps": param[0],
                "freq": param[1],
                "gain": param[2],
                "nfreq": param[3],
                "window": param[4],
                "antisymmetric": param[5],
                "fs": param[6]
            }
        elif self.f_name == "Least Squares":
            self.param = {
                "numtaps": param[0],
                "bands": param[1],
                "desired": param[2],
                "weight": param[3],
                "fs": param[4]
            }
        elif self.f_name == "Equiripple/Minimax":
            self.param = {
                "numtaps": param[0],
                "bands": param[1],
                "desired": param[2],
                "weight": param[3],
                "type": param[4],
                "maxiter": param[5],
                "grid_density": param[6],
                "fs": param[7]
            }   
    def _firwin(self, numtaps, cutoff, *, width=None, window='hamming', pass_zero=True, scale=True, fs=None):
        """
            this is a local copy of firwin that fixes the issue of general cosine
        """
        # NB: scipy's version of array_namespace returns `np_compat` for int or floats
        xp = array_namespace(cutoff)

        # The major enhancements to this function added in November 2010 were
        # developed by Tom Krauss (see ticket #902).
        fs = _validate_fs(fs, allow_none=True)
        fs = 2 if fs is None else fs

        nyq = 0.5 * fs

        cutoff = xp.asarray(cutoff, dtype=xp_default_dtype(xp))
        cutoff = xpx.atleast_nd(cutoff, ndim=1, xp=xp) / float(nyq)

        # Check for invalid input.
        if cutoff.ndim > 1:
            raise ValueError("The cutoff argument must be at most "
                            "one-dimensional.")
        if xp_size(cutoff) == 0:
            raise ValueError("At least one cutoff frequency must be given.")
        if xp.min(cutoff) <= 0 or xp.max(cutoff) >= 1:
            raise ValueError("Invalid cutoff frequency: frequencies must be "
                            "greater than 0 and less than fs/2.")
        if xp.any(cutoff[1:] - cutoff[:-1] <= 0):
            raise ValueError("Invalid cutoff frequencies: the frequencies "
                            "must be strictly increasing.")

        if width is not None:
            # A width was given.  Find the beta parameter of the Kaiser window
            # and set `window`.  This overrides the value of `window` passed in.
            atten = kaiser_atten(numtaps, float(width) / nyq)
            beta = kaiser_beta(atten)
            window = ('kaiser', beta)

        if pass_zero in ('bandstop', 'lowpass'):
            if pass_zero == 'lowpass':
                if xp_size(cutoff) != 1:
                    raise ValueError('cutoff must have one element if '
                                    f'pass_zero=="lowpass", got {cutoff.shape}')
            elif xp_size(cutoff) <= 1:
                raise ValueError('cutoff must have at least two elements if '
                                f'pass_zero=="bandstop", got {cutoff.shape}')
            pass_zero = True
        elif pass_zero in ('bandpass', 'highpass'):
            if pass_zero == 'highpass':
                if xp_size(cutoff) != 1:
                    raise ValueError('cutoff must have one element if '
                                    f'pass_zero=="highpass", got {cutoff.shape}')
            elif xp_size(cutoff) <= 1:
                raise ValueError('cutoff must have at least two elements if '
                                f'pass_zero=="bandpass", got {cutoff.shape}')
            pass_zero = False
        elif not (pass_zero is True or pass_zero is False):
            raise ValueError(f"Parameter {pass_zero=} not in (True, False, 'bandpass', " +
                            "'lowpass', 'highpass', 'bandstop')")

        pass_nyquist = (xp_size(cutoff) % 2 == 0) == pass_zero
        if pass_nyquist and numtaps % 2 == 0:
            raise ValueError("A filter with an even number of coefficients must "
                            "have zero response at the Nyquist frequency.")

        # Insert 0 and/or 1 at the ends of cutoff so that the length of cutoff
        # is even, and each pair in cutoff corresponds to passband.
        cutoff = xp.concat((xp.zeros(int(pass_zero)), cutoff, xp.ones(int(pass_nyquist))))


        # `bands` is a 2-D array; each row gives the left and right edges of
        # a passband.
        bands = xp.reshape(cutoff, (-1, 2))

        # Build up the coefficients.
        alpha = 0.5 * (numtaps - 1)
        m = xp.arange(0, numtaps, dtype=cutoff.dtype) - alpha
        h = 0
        for j in range(bands.shape[0]):
            left, right = bands[j, 0], bands[j, 1]
            h += right * xpx.sinc(right * m, xp=xp)
            h -= left * xpx.sinc(left * m, xp=xp)

        # Get and apply the window function.
        if window[0] == "general cosine":
            win = general_cosine(numtaps, window[1], sym=True)
        else:
            win = get_window(window, numtaps, fftbins=False, xp=xp)
        h *= win

        # Now handle scaling if desired.
        if scale:
            # Get the first passband.
            left, right = bands[0, ...]
            if left == 0:
                scale_frequency = 0.0
            elif right == 1:
                scale_frequency = 1.0
            else:
                scale_frequency = 0.5 * (left + right)
            c = xp.cos(xp.pi * m * scale_frequency)
            s = xp.sum(h * c)
            h /= s

        return h
    def get_taps(self):
        """
        """
        if self.f_name == "Window":
            return self.f(self.param["numtaps"],
                          self.param["cutoff"],
                          width=self.param["width"],
                          window=self.param["window"],
                          pass_zero=self.param["pass_zero"],
                          scale=self.param["scale"],
                          fs=self.param["fs"])
        elif self.f_name == "Frequency Sampling":
            return self.f(self.param["numtaps"],
                          self.param["freq"],
                          self.param["gain"],
                          self.param["nfreqs"],
                          self.param["window"],
                          self.param["antisymmetric"],
                          self.param["fs"])
        elif self.f_name == "Least Squares":
            return self.f(self.param["numtaps"],
                          self.param["bands"],
                          self.param["desired"],
                          self.param["weight"],
                          self.param["fs"])
        elif self.f_name == "Equiripple/Minimax":
            return self.f(self.param["numtaps"],
                          self.param["bands"],
                          self.param["desired"],
                          self.param["weight"],
                          self.param["type"],
                          self.param["maxiter"],
                          self.param["grid_density"],
                          self.param["fs"])
