"""Ideal turbine models for the power cycle and the turbojet."""

def ideal_turbine(T3, P3, P4, cp, gamma):
    """Existing Phase 1 interface: prescribed exit pressure."""
    if min(T3, P3, P4, cp) <= 0 or P4 >= P3 or gamma <= 1:
        raise ValueError('Invalid ideal turbine conditions')
    T4 = T3 * (P4 / P3)**((gamma - 1) / gamma)
    return T4, cp * (T3 - T4)


def ideal_turbojet_turbine(Tt4, Pt4, compressor_work, cp, gamma):
    """Station 4->5: ideal turbine supplying compressor work per kg of air."""
    if min(Tt4, Pt4, cp) <= 0 or gamma <= 1 or compressor_work < 0:
        raise ValueError('Invalid turbine inputs')
    wt = compressor_work
    Tt5 = Tt4 - wt / cp
    if Tt5 <= 0:
        raise ValueError('Turbine cannot supply the specified work')
    Pt5 = Pt4 * (Tt5 / Tt4)**(gamma / (gamma - 1))
    return {'Tt5': Tt5, 'Pt5': Pt5, 'wt': wt}
