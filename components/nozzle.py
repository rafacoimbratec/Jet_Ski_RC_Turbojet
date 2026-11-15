"""Ideal convergent nozzle for a static air-standard turbojet."""
import math


def ideal_convergent_nozzle(Tt5, Pt5, Pa, cp, gamma):
    """Station 5->9. Choked nozzle exits at M=1 with pressure thrust."""
    if min(Tt5, Pt5, Pa, cp) <= 0 or gamma <= 1:
        raise ValueError('Invalid nozzle inputs')
    if Pt5 <= Pa:
        raise ValueError('Nozzle inlet total pressure must exceed ambient pressure')
    k = (gamma - 1) / gamma
    R = cp * k
    critical_ratio = ((gamma + 1) / 2)**(gamma / (gamma - 1))
    NPR = Pt5 / Pa
    choked = NPR >= critical_ratio
    P9 = Pt5 / critical_ratio if choked else Pa
    T9 = Tt5 * (P9 / Pt5)**k
    V9 = math.sqrt(max(0, 2 * cp * (Tt5 - T9)))
    rho9 = P9 / (R * T9)
    return {'P9': P9, 'T9': T9, 'V9': V9, 'rho9': rho9,
            'choked': choked, 'critical_ratio': critical_ratio, 'NPR': NPR}
