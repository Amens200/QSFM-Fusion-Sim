#include <iostream>
#include <vector>
#include "QSFM_Scanner.cpp"  // Include scanner

// Mock ASIC outputs (from Verilog sim/export)
struct ASICOutput {
    uint32_t anomaly;
    uint32_t entropy;
    uint32_t hmac;
};

int main() {
    QSFM_Scanner scanner;
    std::vector<double> mag(100, 1e-9), grav(100, 5e-5);  // Mock data
    std::vector<std::pair<double, double>> locs(100, {0.1, 0.1});
    std::vector<std::string> manifests(100, "cargo: electronics 50kg");
    auto weights = scanner.ship_manifest_processor(manifests);

    // Simulate ASIC call (replace with real DPI/FPGA read)
    ASICOutput asic = {140, 450000, 0xABCDEF01};  // e.g., 140% anomaly, ~450k entropy

    double fused_anomaly = scanner.fuse_scan(mag, grav, locs, weights) + asic.anomaly / 100.0;
    double fused_entropy = scanner.entropy_predict({std::vector<double>(10, 0.5)}) + asic.entropy;

    std::cout << "Integrated Anomaly: " << fused_anomaly * 100 << "% - Threats neutralized!\n";
    scanner.log_audit("2025-08-07 12:00:00", fused_anomaly, fused_entropy, fused_anomaly * 80);
    return 0;
}