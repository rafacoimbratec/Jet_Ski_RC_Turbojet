"""Phase 2A ideal, static, air-standard turbojet visualizations.

Requires numpy and matplotlib. All sweep curves use the SAME assumptions
as phase2_open_turbojet.py (constant cp/gamma; ideal components; zero fuel mass;
ideal convergent nozzle with pressure thrust when choked).
"""
from pathlib import Path
from components.compressor import ideal_turbojet_compressor
from components.combustor import ideal_heat_addition
from components.turbine import ideal_turbojet_turbine
from components.nozzle import ideal_convergent_nozzle
from components.propulsion import static_thrust_performance

import matplotlib.pyplot as plt
import numpy as np


def _ideal_point(T_in, P_ambient, rp, T_t4, cp, gamma):
    """Sensitivity point using the same reusable component models as the solver."""
    try:
        c = ideal_turbojet_compressor(T_in, P_ambient, rp, cp, gamma)
        b = ideal_heat_addition(c['Tt3'], c['Pt3'], T_t4, cp)
        t = ideal_turbojet_turbine(b['Tt4'], b['Pt4'], c['wc'], cp, gamma)
        n = ideal_convergent_nozzle(t['Tt5'], t['Pt5'], P_ambient, cp, gamma)
        p = static_thrust_performance(n['V9'], n['P9'], P_ambient, n['rho9'], 70.0)
    except (ValueError, ZeroDivisionError):
        return None
    return {'Tt3': c['Tt3'], 'Tt5': t['Tt5'], 'Pt5': t['Pt5'],
            'NPR': n['NPR'], 'critical_ratio': n['critical_ratio'],
            'choked': n['choked'], 'specific_thrust': p['specific_thrust']}


def plot_turbojet_cycle(results, *, save_path=None, show=True):
    """Create the Phase 2A seven-panel turbojet dashboard.

    Parameters
    ----------
    results : dict
        Output of phases.phase2_open_turbojet.run_phase2().
    save_path : str or Path or None
        PNG/PDF destination, or None to avoid saving.
    show : bool
        Display the figure (requires a GUI Matplotlib backend).

    Returns
    -------
    matplotlib.figure.Figure
        The figure; it is closed if ``show=False``.
    """
    # Import here so there is no need to pass basic settings twice.
    from inputs import T1, P1, pressure_ratio, T3, cp, gamma

    if results.get('phase') != 2:
        raise ValueError('This plotting function expects Phase 2 results.')

    current = _ideal_point(T1, P1, pressure_ratio, T3, cp, gamma)
    if current is None:
        raise ValueError('Invalid or infeasible current Phase 2 inputs.')

    stations = results['stations']  # insertion order: 2, 3, 4, 5
    station_names = ['2', '3', '4', '5', '9']
    total_t = [value[0] for value in stations.values()] + [results['T9']]
    total_p = [value[1] / 1000 for value in stations.values()] + [results['P9'] / 1000]
    # Note: station 9 quantities are STATIC, not stagnation conditions.

    fig, axs = plt.subplots(4, 2, figsize=(14, 17), constrained_layout=True)
    ax_t, ax_p, ax_rp, ax_temp, ax_pt5, ax_npr, ax_ts, ax_note = axs.flat

    ax_t.plot(station_names[:4], total_t[:4], 'o-', linewidth=2, label='Total temperature (2–5)')
    ax_t.scatter(['9'], [total_t[4]], marker='s', s=55, label='Exit static temperature (9)')
    ax_t.set(title='Temperature across engine', xlabel='Station', ylabel='Temperature [K]')
    ax_t.legend(fontsize=8)

    ax_p.plot(station_names[:4], total_p[:4], 'o-', linewidth=2, label='Total pressure (2–5)')
    ax_p.scatter(['9'], [total_p[4]], marker='s', s=55, label='Exit static pressure (9)')
    ax_p.axhline(P1 / 1000, linestyle=':', color='gray', label='Ambient pressure')
    ax_p.set(title='Pressure across engine', xlabel='Station', ylabel='Pressure [kPa]')
    ax_p.legend(fontsize=8)

    # Pressure ratio sweep, with invalid states represented by NaN.
    rp_values = np.linspace(1.01, max(12.0, pressure_ratio * 1.4), 350)
    rp_points = [_ideal_point(T1, P1, p, T3, cp, gamma) for p in rp_values]
    def quantity(points, key, scale=1.0):
        return np.array([np.nan if point is None else point[key] / scale for point in points])

    ax_rp.plot(rp_values, quantity(rp_points, 'specific_thrust'), lw=2)
    ax_rp.scatter([pressure_ratio], [current['specific_thrust']], color='black', s=35, zorder=5, label='Current design')
    ax_rp.set(title='Specific thrust vs compressor pressure ratio', xlabel='Compressor pressure ratio', ylabel='Specific thrust [N / (kg/s)]')
    ax_rp.legend(fontsize=8)

    # Temperature sweep includes values below the current Tt4 if meaningful.
    t_min = max(T1 * pressure_ratio**((gamma - 1) / gamma) + 1, min(600.0, T3 * 0.8))
    t_max = max(1600.0, T3 * 1.2, t_min + 200)
    temp_values = np.linspace(t_min, t_max, 350)
    temp_points = [_ideal_point(T1, P1, pressure_ratio, t, cp, gamma) for t in temp_values]
    ax_temp.plot(temp_values, quantity(temp_points, 'specific_thrust'), lw=2)
    ax_temp.scatter([T3], [current['specific_thrust']], color='black', s=35, zorder=5, label='Current design')
    ax_temp.set(title='Specific thrust vs maximum temperature', xlabel='Turbine inlet total temperature, Tt4 [K]', ylabel='Specific thrust [N / (kg/s)]')
    ax_temp.legend(fontsize=8)

    ax_pt5.plot(rp_values, quantity(rp_points, 'Pt5', 1000.0), lw=2)
    ax_pt5.axhline(P1 / 1000, linestyle=':', color='gray', label='Ambient pressure')
    ax_pt5.scatter([pressure_ratio], [current['Pt5'] / 1000], color='black', s=35, zorder=5, label='Current design')
    ax_pt5.set(title='Turbine exit total pressure', xlabel='Compressor pressure ratio', ylabel='Pt5 [kPa]')
    ax_pt5.legend(fontsize=8)

    ax_npr.plot(rp_values, quantity(rp_points, 'NPR'), lw=2, label='Pt5 / ambient pressure')
    ax_npr.axhline(current['critical_ratio'], linestyle='--', label='Convergent nozzle choking threshold')
    ax_npr.scatter([pressure_ratio], [current['NPR']], color='black', s=35, zorder=5, label='Current design')
    ax_npr.set(title='Nozzle pressure ratio and choking', xlabel='Compressor pressure ratio', ylabel='Total-to-ambient pressure ratio')
    ax_npr.legend(fontsize=8)

    # OPEN-CYCLE T-s PATH: total states (2, 3, 4, 5) and STATIC state (9).
    # There is no 9->2 heat-rejection leg: fresh air enters and exhaust leaves.
    # s is relative to station 2, not absolute entropy.
    # Isentropic nozzle implies static exit entropy s9 equals total inlet entropy s5.
    exponent = (gamma - 1.0) / gamma
    R = cp * exponent
    station_2, station_3, station_4, station_5 = list(stations.values())
    def rel_s(T, P):
        return (cp * np.log(np.asarray(T) / T1)
                - R * np.log(np.asarray(P) / P1)) / 1000.0

    # 2->3 isentropic compression
    p23 = np.linspace(station_2[1], station_3[1], 100)
    t23 = station_2[0] * (p23 / station_2[1])**exponent
    # 3->4 constant-total-pressure heat addition
    t34 = np.linspace(station_3[0], station_4[0], 100)
    p34 = np.full_like(t34, station_3[1])
    # 4->5 isentropic turbine expansion
    p45 = np.linspace(station_4[1], station_5[1], 100)
    t45 = station_4[0] * (p45 / station_4[1])**exponent
    # 5->9 isentropic nozzle expansion (total state to static state)
    p59 = np.linspace(station_5[1], results['P9'], 100)
    t59 = station_5[0] * (p59 / station_5[1])**exponent

    for tt, pp, label in [
        (t23, p23, '2→3 Compressor'),
        (t34, p34, '3→4 Heat addition'),
        (t45, p45, '4→5 Turbine'),
        (t59, p59, '5→9 Nozzle'),
    ]:
        ax_ts.plot(rel_s(tt, pp), tt, linewidth=2, label=label)
    for num, (tt, pp) in zip(('2','3','4','5','9'),
                             [*stations.values(), (results['T9'], results['P9'])]):
        x = float(rel_s(tt, pp))
        ax_ts.scatter([x], [tt], color='black', s=20, zorder=5)
        ax_ts.annotate(num, (x, tt), xytext=(7, 6), textcoords='offset points')
    ax_ts.set(title='Open-cycle T–s (relative entropy)',
              xlabel='Relative specific entropy [kJ/(kg·K)]',
              ylabel='Temperature [K]')
    ax_ts.legend(fontsize=8)

    ax_note.axis('off')
    ax_note.text(0.05, 0.88, 'Model interpretation', fontsize=13,
                 fontweight='bold', transform=ax_note.transAxes)
    ax_note.text(0.05, 0.72,
                 '• Stations 2–5: total T and P\n'
                 '• Station 9: static exit T and P\n'
                 '• The T–s path is OPEN (no 9→2 closure)\n'
                 '• 5→9: ideal conversion of enthalpy into velocity\n'
                 '• Phase 2A: air-standard, no fuel mass\n'
                 '• 70 N airflow is target-equivalent, not predicted',
                 va='top', fontsize=10, linespacing=1.8,
                 transform=ax_note.transAxes)

    for ax in axs.flat:
        ax.grid(alpha=0.25)
    fig.suptitle(f'Phase 2A — Ideal Open Turbojet | rp={pressure_ratio:.2f} | Tt4={T3:.0f} K', fontsize=15)
    fig.text(0.5, 0.002, 'Ideal, static air-standard model: no fuel mass, component losses or real combustion. Nozzle is convergent.', ha='center', fontsize=9)

    if save_path is not None:
        target = Path(save_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(target, dpi=180, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
