#!/bin/bash
echo "Building QSFM - Let's fuse those threats!"
# Verilog: Mock synthesis (use real tool like iverilog QSFM_ASIC_Fusion.v -o asic.vvp)
iverilog QSFM_ASIC_Fusion.v -o asic.vvp && vvp asic.vvp
# C++: Compile scanner and integration
g++ -o qsfm_scanner QSFM_Scanner.cpp -std=c++17
g++ -o qsfm_integrator QSFM_Integration.cpp -std=c++17
# Python: Install deps and run sim/main
pip install numpy scipy qutip scikit-learn flask sqlite3
python QSFM_FusionSimulation.py
python QSFM_Main.py
echo "Build complete - Anomaly-free zone achieved!"