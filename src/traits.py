class Traits:
    def __init__(self):
        self._S = 1
        self._I = 0
        self._R = 0
    @property
    def s(self):
        return self._S
    @property
    def i(self):
        return self._I
    @property
    def r(self):
        return self._R

    def infect(self,rate: float):
        moved = self._S * rate
        self._S -= moved
        self._I += moved
        self._check()
    def recover(self,rate: float):
        moved = self._I * rate
        self._I -= moved
        self._R += moved
        self._check()
    def _check(self):
        total = self._S + self._I + self._R
        if abs(total - 1.0) < 1e-6 :
            self._S /= total
            self._I /= total
            self._R /= total
            return
        else:
            raise ValueError(f"Traits invariant broken: S={self._S} I={self._I} R={self._R} total={total}")
