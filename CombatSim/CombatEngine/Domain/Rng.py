"""Swappable random number generator for the combat engine.

Uses Python's random module (Mersenne Twister) by default.
"""

import random as _py_random


class Rng:
    """Singleton RNG with swappable backend.

    Usage
    -----
    >>> Rng.randint(1, 100)   # inclusive integer
    >>> Rng.random()          # float in [0, 1)
    """

    _backend = "python"
    randint = staticmethod(_py_random.randint)
    random = staticmethod(_py_random.random)

    @classmethod
    def use_python(cls) -> None:
        """Use Python's random (Mersenne Twister) — default, already active."""
        cls._backend = "python"
        cls.randint = staticmethod(_py_random.randint)
        cls.random = staticmethod(_py_random.random)

    @classmethod
    def use_c(cls) -> None:
        """Switch to C libc rand() via ctypes — LCG, faster in some workloads."""
        import ctypes as _ct
        import ctypes
        _libc = _ct.CDLL("libc.so.6")
        _libc.rand.restype = _ct.c_int
        _RAND_MAX = 0x7FFFFFFF

        def _c_randint(lo: int, hi: int) -> int:
            return (_libc.rand() % (hi - lo + 1)) + lo

        def _c_random() -> float:
            return (_libc.rand() & _RAND_MAX) / (_RAND_MAX + 1.0)

        cls._backend = "c"
        cls.randint = staticmethod(_c_randint)
        cls.random = staticmethod(_c_random)


# Module-level aliases for test patching
random = Rng.random
randint = Rng.randint
