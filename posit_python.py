from fractions import Fraction 
from itertools import islice
from typing import Any

def posit(n: int) -> type[Posit]:
    'create a posit datatype of n bits (see https://posithub.org)'
    
    if not isinstance(n, int) or not (n > 1):
        raise ValueError(f'{n=} must be any integer greater than 1')
    
    class Posit:
        f"""
        posit datatype of {n} bits (see https://posithub.org)
        """
        _es = 2
        
        def __init__(self, value: float | bytes | Any):
            if isinstance(value, bytes):
                it = iter(bits)
                
                self.sign_bits = next(it)
                
                self.regime_bits = next(it)
                for bit in it:
                    self.regime_bits += bit
                    if bit != self.regime_bits[0]:
                        break
                
                self.exponent_bits = ''.join(islice(it, _es))
                self.fraction_bits = ''.join(it)

                return
            
            
        
        
        def __str__(self):
            'print the posit in decimal'
            return 'idk'
    
    return Posit


    'create a posit datatype of n bits (see https://posithub.org)'
