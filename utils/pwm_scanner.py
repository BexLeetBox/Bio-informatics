import numpy as np
import os

def load_pwm(motif_name):
    pwm_file = f"data/jaspar_motifs/{motif_name}.txt"
    if not os.path.exists(pwm_file):
        raise ValueError(f"PWM file not found: {pwm_file}")
    
    pwm = {}
    with open(pwm_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue
            base, *values = line.strip().split()
            pwm[base] = np.array([float(v) for v in values])

    return pwm


def score_pwm(sequence, pwm, pfm, penalty_factor=2.0):
    pwm_length = len(pwm['A'])  
    scores = []
    sequence = sequence.upper()

    if len(sequence) < pwm_length:
        print(f"Warning: Sequence too short for PWM scanning: {sequence}")
        return []

    for i in range(len(sequence) - pwm_length + 1):
        subseq = sequence[i:i + pwm_length]

        score = 0
        for j, base in enumerate(subseq):
            if base in pwm:
                pwm_score = pwm[base][j]
                pfm_frequency = pfm[base][j]  # Extract the raw PFM frequency
                
                # Apply penalty if the nucleotide is rare at this position
                if pfm_frequency < 0.05:  # If the frequency is below 5% in JASPAR
                    pwm_score -= penalty_factor * abs(pwm_score)  # Apply penalty
                
                score += pwm_score

        scores.append(score)

    return scores



def scan_dna_sequence(dna_sequence, pwm, pfm):
    motif_length = len(pwm['A'])
    dna_sequence = dna_sequence.upper().strip()

    if len(dna_sequence) < motif_length:
        print(f"Warning: Sequence too short for motif scanning: {dna_sequence}")
        return {'binding_sites': [], 'scores': []}

    scores = score_pwm(dna_sequence, pwm, pfm)

    if not scores:
        print(f"Warning: No valid scores found for sequence {dna_sequence}")
        return {'binding_sites': [], 'scores': []}

    threshold = np.mean(scores) + 3.4 * np.std(scores)

    binding_sites = []
    for i, score in enumerate(scores):
        subseq = dna_sequence[i:i + motif_length]

        # Ensure no forbidden nucleotides are present
        is_valid = all(pfm[base][j] > 0.05 for j, base in enumerate(subseq) if base in pfm)
        
        if score > threshold and is_valid:
            binding_sites.append(i)

    return {
        'binding_sites': binding_sites,
        'scores': scores
    }

 

def convert_pfm_to_pwm(pfm):
    background_prob = 0.25  
    pwm = {}

    for base, counts in pfm.items():
        total_counts = np.sum(counts) + 1  # Add pseudocount
        pwm[base] = list(np.log2((np.array(counts) + 1) / total_counts / background_prob))  # Convert to list

    return pwm



