from scipy.signal import firwin, firwin2, firls, remez

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
            self.f = firwin
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
