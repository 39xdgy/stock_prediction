class day_info:

    def __init__(self, high, low, open, close):
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.DI = (high + low + (2*close))/4
        self.EMA12 = None
        self.EMA26 = None
        self.DIF = None
        self.MACD = None
        self.OSC = None
        self.OSCS = None
        self.RSI6 = None
        self.RSI12 = None
        self.RSI_diff = None
        self.RSV = None
        self.K = None
        self.D = None
        self.J = None

    def set_EMA12(self, EMA12):
        self.EMA12 = EMA12

    def set_EMA26(self, EMA26):
        self.EMA26 = EMA26

    def set_DIF(self, DIF):
        self.DIF = DIF

    def set_MACD(self, MACD):
        self.MACD = MACD

    def set_OSC(self, OSC):
        self.OSC = OSC

    def set_OSCS(self, OSCS):
        self.OSCS = OSCS

    def set_RSI6(self, RSI6):
        self.RSI6 = RSI6

    def set_RSI12(self, RSI12):
        self.RSI12 = RSI12

    def set_RSI_diff(self, RSI_diff):
        self.RSI_diff = RSI_diff
    def set_RSV(self, RSV):
        self.RSV = RSV

    def set_K(self, K):
        self.K = K

    def set_D(self, D):
        self.D = D

    def set_J(self, J):
        self.J = J

    def get_all_flag(self):
        return [self.EMA12, self.EMA26,
                self.DIF, self.MACD,
                self.OSC, self.OSCS,
                self.RSI6, self.RSI12, self.RSI_diff, 
                self.RSV, self.K, self.D, self.J]
