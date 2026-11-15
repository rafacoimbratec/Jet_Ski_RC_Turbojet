
# inputs.py

# ======================================
# ANALYSIS CONFIGURATION
# ======================================

ANALYSIS_PHASE = 2

# 1 - Ideal Air-Standard Brayton Cycle
# 2A - Ideal Open Turbojet Cycle
# 2B - Non-ideal open turbojet
# 3 - Propane-air cantera model
# 4 - Integrated performance assesment

SAVE_PLOTS = True
SHOW_PLOTS = True

# ======================================
# THERMODYNAMIC INPUTS
# ======================================

# Ambient conditions
T1 = 288.15        # K
P1 = 101325.0      # Pa

# Design parameters
pressure_ratio = 3.0
T3 = 1000.0        # K

# Constant air properties
cp = 1005.0        # J/(kg*K)
gamma = 1.4

# Component efficiencies
eta_c = 1.0
eta_t = 1.0
