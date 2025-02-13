from utils.pwm_scanner import convert_pfm_to_pwm, scan_dna_sequence
from app import highlight_binding_sites
# Example PFM from JASPAR
pfm = {
    'A': [4, 19, 0, 0, 0, 0],
    'C': [16, 0, 20, 0, 0, 0],
    'G': [0, 1, 0, 20, 0, 20],
    'T': [0, 0, 0, 0, 20, 0]
}

# Convert to PWM
pwm = convert_pfm_to_pwm(pfm)

# Example sequences
sequences = ["TGCACGTGAC", "GACGTGACC", "TACGTGATT"]

# Scan sequences
results = scan_dna_sequence(sequences, pwm)

# Print results
for res in results:
    print(f"\nOriginal Sequence: {res['sequence']}")
    print(f"Binding Sites: {res['binding_sites']}")
    print(f"Scores: {res['scores']}")
    print(f"Highlighted: {highlight_binding_sites(res['sequence'], res['binding_sites'])}")
