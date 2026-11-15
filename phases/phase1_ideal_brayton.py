
# phases/phase1_ideal_brayton.py

from inputs import (
    T1, P1, pressure_ratio, T3,
    cp, gamma, SAVE_PLOTS, SHOW_PLOTS
)

from components.compressor import ideal_compressor
from components.turbine import ideal_turbine
from plots.brayton_plots import plot_brayton_cycle


def run_phase1():

    # 1 -> 2: Isentropic compression
    T2, P2, wc = ideal_compressor(
        T1, P1, pressure_ratio, cp, gamma
    )

    # 2 -> 3: Constant-pressure heat addition
    P3 = P2
    q_in = cp * (T3 - T2)

    if q_in <= 0:
        raise ValueError("T3 must exceed T2.")

    # 3 -> 4: Isentropic expansion
    P4 = P1
    T4, wt = ideal_turbine(
        T3, P3, P4, cp, gamma
    )

    # 4 -> 1: Constant-pressure heat rejection
    q_out = cp * (T4 - T1)

    # Cycle performance
    w_net = wt - wc
    eta_th = w_net / q_in
    bwr = wc / wt

    # Analytical checks
    exponent = (gamma - 1) / gamma
    eta_analytical = 1 - pressure_ratio**(-exponent)

    assert abs(eta_th - eta_analytical) < 1e-10
    assert abs(q_in - q_out - w_net) < 1e-6

    # Results
    print("\n--- Station Temperatures ---")
    for name, value in zip(
        ["T1", "T2", "T3", "T4"],
        [T1, T2, T3, T4]
    ):
        print(f"{name} = {value:.2f} K")

    print("\n--- Cycle Performance ---")
    print(f"Compressor work: {wc/1000:.2f} kJ/kg")
    print(f"Turbine work:    {wt/1000:.2f} kJ/kg")
    print(f"Net work:        {w_net/1000:.2f} kJ/kg")
    print(f"Heat input:      {q_in/1000:.2f} kJ/kg")
    print(f"Thermal efficiency: {eta_th*100:.2f}%")
    print(f"Back-work ratio:    {bwr*100:.2f}%")

    # Generate plots
    plot_brayton_cycle(
        save_path=(
            "brayton_cycle.png" if SAVE_PLOTS else None
        ),
        show=SHOW_PLOTS
    )

    return {
    "T1": T1,
    "T2": T2,
    "T3": T3,
    "T4": T4,
    "P1": P1,
    "P2": P2,
    "P3": P3,
    "P4": P4,
    "compressor_work": wc,
    "turbine_work": wt,
    "net_work": w_net,
    "heat_input": q_in,
    "thermal_efficiency": eta_th,
    "back_work_ratio": bwr
    }