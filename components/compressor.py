"""Ideal compressor functions shared by Phase 1 and Phase 2."""

def ideal_compressor(T1, P1, pressure_ratio, cp, gamma):
    """Phase 1-compatible return tuple: (outlet T, outlet P, specific work)."""
    if min(T1, P1, cp) <= 0 or pressure_ratio <= 1 or gamma <= 1:
        raise ValueError('Invalid compressor inputs')
    P2 = P1 * pressure_ratio
    T2 = T1 * pressure_ratio ** ((gamma - 1) / gamma)
    return T2, P2, cp * (T2 - T1)


def ideal_turbojet_compressor(Tt2, Pt2, pressure_ratio, cp, gamma):
    """Station 2->3, total quantities, constant cp/gamma."""
    Tt3, Pt3, wc = ideal_compressor(Tt2, Pt2, pressure_ratio, cp, gamma)
    return {'Tt3': Tt3, 'Pt3': Pt3, 'wc': wc}
