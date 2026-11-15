"""Ideal Brayton cycle plots.

All design inputs are read from inputs.py when plot_brayton_cycle() is called.
Update T3 in inputs.py to change maximum cycle temperature.
"""
import numpy as np
import matplotlib.pyplot as plt
import inputs


def plot_brayton_cycle(save_path='brayton_cycle.png', show=True):
    """Draw P-v, T-s, efficiency, work, and back-work ratio plots.

    Assumes a constant-cp, ideal air-standard Brayton power cycle.
    All work quantities are specific (kJ/kg), NOT thrust.
    """
    T1 = inputs.T1
    P1 = inputs.P1
    rp0 = inputs.pressure_ratio
    T3 = inputs.T3
    cp = inputs.cp
    gamma = inputs.gamma

    if T1 <= 0 or T3 <= 0 or P1 <= 0 or cp <= 0 or gamma <= 1 or rp0 <= 1:
        raise ValueError('Temperatures, P1 and cp must be positive; gamma and pressure_ratio must exceed 1.')

    a = (gamma - 1.0) / gamma
    T2 = T1 * rp0**a
    if T3 <= T2:
        raise ValueError(f'T3 ({T3:.1f} K) must exceed compressor exit T2 ({T2:.1f} K).')

    P2 = P3 = P1 * rp0
    P4 = P1
    T4 = T3 / rp0**a
    R = cp * a

    def v(T, P):
        return R * np.asarray(T) / np.asarray(P)

    def s_rel(T, P):
        return cp * np.log(np.asarray(T) / T1) - R * np.log(np.asarray(P) / P1)

    # Four ideal processes
    p12 = np.linspace(P1, P2, 120)
    t12 = T1 * (p12 / P1)**a
    t23 = np.linspace(T2, T3, 120)
    p23 = np.full_like(t23, P2)
    p34 = np.linspace(P3, P4, 120)
    t34 = T3 * (p34 / P3)**a
    t41 = np.linspace(T4, T1, 120)
    p41 = np.full_like(t41, P1)

    paths = [(t12, p12, '1 → 2 Compression'),
             (t23, p23, '2 → 3 Heat addition'),
             (t34, p34, '3 → 4 Expansion'),
             (t41, p41, '4 → 1 Heat rejection')]
    stations = [(T1, P1), (T2, P2), (T3, P3), (T4, P4)]

    fig, axs = plt.subplots(3, 2, figsize=(14, 13), constrained_layout=True)
    ax_pv, ax_ts, ax_eta, ax_work, ax_bwr, ax_notes = axs.flat

    for T, P, label in paths:
        ax_pv.plot(v(T, P), P / 1000, lw=2.2, label=label)
        ax_ts.plot(s_rel(T, P) / 1000, T, lw=2.2, label=label)

    for i, (T, P) in enumerate(stations, 1):
        ax_pv.scatter(v(T, P), P / 1000, color='black', s=24, zorder=5)
        ax_ts.scatter(s_rel(T, P) / 1000, T, color='black', s=24, zorder=5)
        ax_pv.annotate(str(i), (v(T, P), P / 1000), xytext=(5, 7), textcoords='offset points')
        ax_ts.annotate(str(i), (s_rel(T, P) / 1000, T), xytext=(5, 7), textcoords='offset points')

    ax_pv.set(title='Ideal Brayton cycle: P–v', xlabel='Specific volume [m³/kg]', ylabel='Pressure [kPa]')
    ax_ts.set(title='Ideal Brayton cycle: T–s', xlabel='Relative entropy [kJ/(kg·K)]', ylabel='Temperature [K]')
    ax_pv.legend(fontsize=8)

    # Sweep pressure ratio over physically admissible positive-heat-input states.
    rp_limit = (T3 / T1)**(1 / a)
    rp_max = min(20.0, 0.98 * rp_limit)
    if rp_max <= 1.01:
        raise ValueError('No useful pressure-ratio sweep for this T3/T1 combination.')
    rp = np.linspace(1.001, max(rp_max, rp0 * 1.02), 350)
    rp = rp[rp < rp_limit]

    t2 = T1 * rp**a
    t4 = T3 / rp**a
    wc = cp * (t2 - T1) / 1000
    wt = cp * (T3 - t4) / 1000
    wnet = wt - wc
    eta = 100 * (1 - rp**(-a))
    bwr = 100 * wc / wt

    wc0 = cp * (T2 - T1) / 1000
    wt0 = cp * (T3 - T4) / 1000
    wnet0 = wt0 - wc0
    eta0 = 100 * (1 - rp0**(-a))
    bwr0 = 100 * wc0 / wt0
    rp_opt = (T3 / T1)**(1 / (2 * a))

    ax_eta.plot(rp, eta, lw=2, label='Thermal efficiency')
    ax_eta.scatter(rp0, eta0, color='black', zorder=5, label='Current design')
    ax_eta.set(title='Efficiency vs pressure ratio', xlabel='Pressure ratio', ylabel='Thermal efficiency [%]')
    ax_eta.legend(fontsize=8)

    ax_work.plot(rp, wc, lw=2, label='Compressor work (input)')
    ax_work.plot(rp, wt, lw=2, label='Turbine work (output)')
    ax_work.plot(rp, wnet, lw=2, label='Net work')
    ax_work.scatter([rp0] * 3, [wc0, wt0, wnet0], color='black', s=20, zorder=5)
    if 1 < rp_opt <= rp.max():
        ax_work.axvline(rp_opt, color='gray', ls='--', alpha=0.8,
                        label=f'Max net work at rp={rp_opt:.2f}')
    ax_work.set(title='Specific work vs pressure ratio', xlabel='Pressure ratio', ylabel='Specific work [kJ/kg]')
    ax_work.legend(fontsize=8)

    ax_bwr.plot(rp, bwr, lw=2.2, label='Back-work ratio')
    ax_bwr.scatter(rp0, bwr0, color='black', zorder=5,
                   label=f'Current design: {bwr0:.1f}%')
    ax_bwr.axhline(100, color='gray', linestyle='--', linewidth=1,
                   label='100%: turbine work = compressor work')
    ax_bwr.set(title='Back-work ratio vs pressure ratio', xlabel='Pressure ratio',
               ylabel='Back-work ratio [%]')
    ax_bwr.legend(fontsize=8)
    ax_bwr.set_ylim(bottom=0)

    ax_notes.axis('off')
    note = (f'CURRENT DESIGN POINT\n\n'
            f'T1 = {T1:.2f} K    P1 = {P1 / 1000:.2f} kPa\n'
            f'T3 = {T3:.1f} K     rp = {rp0:.2f}\n\n'
            f'Compressor exit T2 = {T2:.1f} K\n'
            f'Turbine exit T4 = {T4:.1f} K\n'
            f'Compressor work = {wc0:.1f} kJ/kg\n'
            f'Turbine work = {wt0:.1f} kJ/kg\n'
            f'Net work = {wnet0:.1f} kJ/kg\n'
            f'Thermal efficiency = {eta0:.2f}%\n'
            f'Back-work ratio = {bwr0:.2f}%\n\n'
            f'Max-net-work pressure ratio = {rp_opt:.2f}\n'
            f'Ideal constant-cp air-standard power cycle\n'
            f'Not a turbojet thrust prediction')
    ax_notes.text(0.05, 0.95, note, va='top', ha='left',
                  transform=ax_notes.transAxes, fontsize=11, linespacing=1.5,
                  family='monospace')

    for ax in (ax_pv, ax_ts, ax_eta, ax_work, ax_bwr):
        ax.grid(True, alpha=0.3)
    fig.suptitle(f'Ideal Brayton Cycle | rp = {rp0:.2f} | T3 = {T3:.0f} K', fontsize=15)
    if save_path is not None:
        fig.savefig(save_path, dpi=180, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


if __name__ == '__main__':
    plot_brayton_cycle()
