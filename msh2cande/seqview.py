import math
import numbers
from abc import abstractmethod


class SeqItemView:
    def __init__(self, key, seq):
        self.key = key
        self.seq = seq

    @property
    def value(self):
        return self.seq[self.key]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.seq!r}, {self.key!r})"

    def __str__(self):
        return f"{self.seq[self.key]!s}"

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        return self.value == other

    def __format__(self, format_spec):
        return self.value.__format__(format_spec)


class DelegatedInteger(numbers.Integral):
    @property
    @abstractmethod
    def value(self):
        return NotImplemented

    def __abs__(self):
        return abs(self.value)

    def __add__(self, other):
        return self.value + other

    def __ceil__(self):
        return math.ceil(self.value)

    def __eq__(self, other):
        return self.value == other

    def __floor__(self):
        return math.floor(self.value)

    def __floordiv__(self, other):
        return self.value // other

    def __int__(self):
        return int(self.value)

    def __le__(self, other):
        return self.value <= other

    def __lt__(self, other):
        return self.value < other

    def __mod__(self, other):
        return self.value % other

    def __mul__(self, other):
        return self.value * other

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __pow__(self, other):
        return self.value ** other

    def __radd__(self, other):
        return other + self.value

    def __rfloordiv__(self, other):
        return other // self.value

    def __rmod__(self, other):
        return other % self.value

    def __rmul__(self, other):
        return other * self.value

    def __round__(self, ndigits=None):
        return round(self.value, ndigits)

    def __rpow__(self, other):
        return other ** self.value

    def __rtruediv__(self, other):
        return other / self.value

    def __truediv__(self, other):
        return self.value / other

    def __trunc__(self):
        return math.trunc(self.value)

    def __and__(self, other):
        return self.value & other

    def __lshift__(self, other):
        return self.value << other

    def __invert__(self):
        return ~self.value

    def __or__(self, other):
        return self.value | other

    def __rand__(self, other):
        return other & self.value

    def __rlshift__(self, other):
        return other << self.value

    def __ror__(self, other):
        return other | self.value

    def __rrshift__(self, other):
        return other >> self.value

    def __rshift__(self, other):
        return self.value >> other

    def __rxor__(self, other):
        return other ^ self.value

    def __xor__(self, other):
        return self.value ^ other


class SeqNumberView(SeqItemView, DelegatedInteger):
    def __hash__(self):
        return hash(self.value)

    def __iadd__(self, other):
        self.seq[self.key] += other

    def __isub__(self, other):
        self.seq[self.key] -= other

    def __imul__(self, other):
        self.seq[self.key] *= other

    def __itruediv__(self, other):
        self.seq[self.key] /= other

    def __ifloordiv__(self, other):
        self.seq[self.key] //= other

    def __imod__(self, other):
        self.seq[self.key] %= other

    def __imatmul__(self, other):
        self.seq[self.key] @= other

    def __ipow__(self, other):
        self.seq[self.key] **= other