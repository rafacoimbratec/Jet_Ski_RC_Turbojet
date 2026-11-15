"""Static specific thrust and target-equivalent airflow, air-standard model."""

def static_thrust_performance(V9, P9, Pa, rho9, target_thrust):
    if V9 <= 0 or rho9 <= 0 or target_thrust <= 0:
        raise ValueError('Exhaust speed, density and target thrust must be positive')
    specific_thrust = V9 + (P9 - Pa) / (rho9 * V9)
    if specific_thrust <= 0:
        raise ValueError('No positive specific thrust')
    mdot_air = target_thrust / specific_thrust
    A9 = mdot_air / (rho9 * V9)
    return {'specific_thrust': specific_thrust, 'target_thrust': target_thrust,
            'required_airflow': mdot_air, 'nozzle_exit_area': A9,
            'calculated_thrust': mdot_air * V9 + (P9 - Pa) * A9}
