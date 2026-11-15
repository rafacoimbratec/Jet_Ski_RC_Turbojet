"""Phase 2A: ideal static open turbojet, air-standard steady flow."""
from inputs import T1, P1, pressure_ratio, T3, cp, gamma, SAVE_PLOTS, SHOW_PLOTS
from components.compressor import ideal_turbojet_compressor
from components.combustor import ideal_heat_addition
from components.turbine import ideal_turbojet_turbine
from components.nozzle import ideal_convergent_nozzle
from components.propulsion import static_thrust_performance
from plots.turbojet_plots import plot_turbojet_cycle


def solve_phase2(Tt2, Pt2, rp, Tt4, cp_air, gamma_air, target_thrust=70.0):
    """Pure calculation without plotting, suitable for sensitivities and tests."""
    compressor = ideal_turbojet_compressor(Tt2, Pt2, rp, cp_air, gamma_air)
    combustor = ideal_heat_addition(compressor['Tt3'], compressor['Pt3'], Tt4, cp_air)
    turbine = ideal_turbojet_turbine(combustor['Tt4'], combustor['Pt4'], compressor['wc'], cp_air, gamma_air)
    nozzle = ideal_convergent_nozzle(turbine['Tt5'], turbine['Pt5'], Pt2, cp_air, gamma_air)
    propulsion = static_thrust_performance(nozzle['V9'], nozzle['P9'], Pt2,
                                           nozzle['rho9'], target_thrust)
    assert abs(turbine['wt'] - compressor['wc']) < 1e-6
    assert abs(propulsion['calculated_thrust'] - target_thrust) < 1e-6
    results = {
        'phase': 2,
        'stations': {
            '2 - Compressor inlet': (Tt2, Pt2),
            '3 - Compressor exit': (compressor['Tt3'], compressor['Pt3']),
            '4 - Turbine inlet': (combustor['Tt4'], combustor['Pt4']),
            '5 - Turbine exit': (turbine['Tt5'], turbine['Pt5']),
        },
        'T9': nozzle['T9'], 'P9': nozzle['P9'],
        'wc': compressor['wc'], 'wt': turbine['wt'], 'q_in': combustor['q_in'],
        'Pt5': turbine['Pt5'], 'Tt5': turbine['Tt5'],
        'nozzle_choked': nozzle['choked'], 'exit_velocity': nozzle['V9'],
        'specific_thrust': propulsion['specific_thrust'],
        'target_thrust': target_thrust, 'required_airflow': propulsion['required_airflow'],
        'nozzle_exit_area': propulsion['nozzle_exit_area'],
        'critical_ratio': nozzle['critical_ratio'],
        'nozzle_pressure_ratio': nozzle['NPR'],
        'Tt2': Tt2, 'Pt2': Pt2, 'Tt3': compressor['Tt3'], 'Pt3': compressor['Pt3'],
        'Tt4': combustor['Tt4'], 'Pt4': combustor['Pt4'],
        'cp': cp_air, 'gamma': gamma_air, 'pressure_ratio': rp,
    }
    return results


def run_phase2():
    results = solve_phase2(T1, P1, pressure_ratio, T3, cp, gamma)
    print('\n====== PHASE 2: IDEAL OPEN TURBOJET ======')
    print('\n--- Thermodynamic stations (total, except station 9) ---')
    for name, (T, P) in results['stations'].items():
        print(f'{name}: Tt = {T:.2f} K, Pt = {P/1000:.2f} kPa')
    print(f"9 - Nozzle exit (static): T = {results['T9']:.2f} K, P = {results['P9']/1000:.2f} kPa")
    print('\n--- Energy balance ---')
    print(f"Heat input: {results['q_in']/1000:.2f} kJ/kg")
    print(f"Compressor work: {results['wc']/1000:.2f} kJ/kg")
    print(f"Turbine work: {results['wt']/1000:.2f} kJ/kg")
    print('\n--- Nozzle ---')
    print(f"Nozzle pressure ratio: {results['nozzle_pressure_ratio']:.3f}")
    print(f"Critical pressure ratio: {results['critical_ratio']:.3f}")
    print(f"Choked: {results['nozzle_choked']}")
    print(f"Exit velocity: {results['exit_velocity']:.2f} m/s")
    print('\n--- Propulsion performance (ideal target-equivalent estimates) ---')
    print(f"Specific thrust: {results['specific_thrust']:.2f} N/(kg/s)")
    print(f"Target thrust: {results['target_thrust']:.2f} N")
    print(f"Required airflow: {results['required_airflow']:.4f} kg/s")
    print(f"Nozzle exit area: {results['nozzle_exit_area']*1e4:.2f} cm²")
    plot_turbojet_cycle(results,
                       save_path='turbojet_cycle.png' if SAVE_PLOTS else None,
                       show=SHOW_PLOTS)
    return results
