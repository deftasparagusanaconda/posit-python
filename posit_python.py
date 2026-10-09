from __future__ import annotations
from fractions import Fraction 
from itertools import islice
from math import ceil

two = Fraction(2)

def posit(n: int) -> type[Posit]:
    'create posit datatype of n bits (see https://posithub.org)'
    
    if not isinstance(n, int) or not (n > 1):
        raise ValueError(f'{n=} must be any integer greater than 1')

    n_ = n
    
    class Posit:
        f"""
        posit datatype of {n_} bits (see https://posithub.org)
        """
        n: int = n_
        NaR: object = object()
        
        def __init__(self, bitstring: str): 

            # ------------------
            # split into S R E F
            # ------------------
            
            it = iter(bitstring)
            
            self.S: str = next(it)      
            self.R: str = next(it)
            for bit in it:
                if bit != self.R[-1]:
                    break
                self.R += bit
            self.E: str = ''.join(islice(it, 2))
            self.F: str = ''.join(it)
            
            # -----------
            # calculate p
            # -----------
            
            self.k: int = len(self.R)
            self.m: int = len(self.F)
            
            self.f: Fraction = Fraction(int(self.F or '0', base=2), 2 ** self.m)
            self.s: int = int(self.S)
            self.r: int = self.k - 1 if int(self.R[0]) else -self.k
            self.e: int = int(self.E.ljust(2, '0'), base=2)
            
            self.p: Fraction | Posit.NaR = (
                (   Posit.NaR
                    if self.S == '1'
                    else Fraction(0))
                if all(bit == '0' for bit in bitstring[1:])
                else ((1 - 3 * self.s) + self.f) * two ** ((1 - 2 * self.s) * (4 * self.r + self.e + self.s)))

            # fix bitfield indexing
            self.R: str = self.R[::-1]
            self.E: str = self.E[::-1]
            self.F: str = self.F[::-1]
            self.bits: str = bitstring[::-1]

            # -------------------------------
            # dyadic rational form K * 2 ** M
            # -------------------------------
            
            if isinstance(self.p, Fraction):
                self.K = self.p.numerator
                self.M = 1 - self.p.denominator.bit_length()

                while self.K != 0 and self.K % 2 == 0:
                    self.K //= 2
                    self.M += 1
            
            #assert self % Posit.minPos == 0
        
        def as_bitstring(self) -> str:
            return self.bits[::-1]
        
        def __str__(self) -> str:
            'print the posit in decimal'
            return str(self.p)
        
    # Posit.NaR     = Posit.from_bits('abc')
    # Posit.zero    = Posit.from_bits('0' * n)
    # Posit.minPos  = Posit(two ** (-4 * n + 8))
    # Posit.maxPos  = 1 / Posit.minPos
    # Posit.pIntMax = Posit.(ceil(two ** (4 * (n - 3) // 5)))
    
    return Posit
