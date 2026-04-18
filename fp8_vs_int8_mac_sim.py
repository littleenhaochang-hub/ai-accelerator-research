import math

def simulate_fp8_vs_int8():
    # Hardware synthesis estimates (relative silicon area in um^2)
    # INT8 MAC: 8-bit integer multiplier + 32-bit integer accumulator
    int8_mul_area = 300
    int8_acc_area = 150
    int8_total_area = int8_mul_area + int8_acc_area

    # FP8 (E4M3) MAC: 4-bit exp adder, 4x4 mantissa multiplier, alignment shifter, FP accumulator
    fp8_mul_area = 120  # smaller mantissa multiplier
    fp8_exp_add_area = 50
    fp8_align_area = 180
    fp8_acc_area = 350
    fp8_total_area = fp8_mul_area + fp8_exp_add_area + fp8_align_area + fp8_acc_area

    area_ratio = fp8_total_area / int8_total_area

    # Energy per MAC (relative pJ)
    int8_energy_pj = 0.20
    fp8_energy_pj = 0.35

    print("--- FP8 (E4M3) vs INT8 MAC Hardware Simulation ---")
    print(f"INT8 MAC Area: {int8_total_area} um^2 | Energy: {int8_energy_pj} pJ")
    print(f"FP8 MAC Area: {fp8_total_area} um^2 | Energy: {fp8_energy_pj} pJ")
    print(f"FP8 Area Overhead: {area_ratio:.2f}x")
    print(f"FP8 Energy Overhead: {fp8_energy_pj/int8_energy_pj:.2f}x")
    print("Conclusion: FP8 offers better dynamic range without block-wise scaling factors, but costs 55%+ more silicon area and 75% more power due to mantissa alignment shifters. Unsuitable for Extreme Edge without block-shared exponents (Microscaling).")

if __name__ == "__main__":
    simulate_fp8_vs_int8()
