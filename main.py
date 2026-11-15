
# main.py

from inputs import ANALYSIS_PHASE

from phases.phase1_ideal_brayton import run_phase1
from phases.phase2_open_turbojet import run_phase2


def main():

    print("\n====== JET ENGINE THERMODYNAMIC ANALYSIS ======")

    if ANALYSIS_PHASE == 1:
        print("\nPhase 1: Ideal Brayton Cycle")
        run_phase1()

    elif ANALYSIS_PHASE == 2:
        print("\nPhase 2: Open Turbojet Cycle")
        run_phase2()

    else:
        raise ValueError(
            f"Invalid analysis phase: {ANALYSIS_PHASE}"
        )


if __name__ == "__main__":
    main()
