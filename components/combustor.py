"""Air-standard heat addition, not fuel combustion chemistry."""

def ideal_heat_addition(Tt3, Pt3, Tt4, cp):
    """Station 3->4: constant-total-pressure heat addition."""
    if min(Tt3, Pt3, Tt4, cp) <= 0 or Tt4 <= Tt3:
        raise ValueError('Heat addition requires Tt4 > Tt3 and positive states')
    return {'Tt4': Tt4, 'Pt4': Pt3, 'q_in': cp * (Tt4 - Tt3)}
