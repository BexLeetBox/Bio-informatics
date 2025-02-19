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


def score_pwm(sequence, pwm):
    pwm_length = len(pwm['A'])  # Assume PWM length is consistent
    scores = []
    sequence = sequence.upper()  # Convert to uppercase to avoid key errors

    if len(sequence) < pwm_length:
        print(f"Warning: Sequence too short for PWM scanning: {sequence}")
        return []

    for i in range(len(sequence) - pwm_length + 1):
        subseq = sequence[i:i + pwm_length]

        # Compute PWM score for this position
        score = sum(pwm[base][j] if base in pwm else 0 for j, base in enumerate(subseq))
        scores.append(score)  # Append scores correctly

    return scores


def scan_dna_sequence(dna_sequence, pwm):
    """
    Scans a single DNA sequence for transcription factor binding sites.

    Args:
        dna_sequence (str): The input DNA sequence.
        pwm (dict): The PWM dictionary.

    Returns:
        dict: A dictionary containing binding sites and scores.
    """
    motif_length = len(pwm['A'])
    dna_sequence = dna_sequence.upper().strip()  # Ensure proper formatting

    if len(dna_sequence) < motif_length:
        print(f"Warning: Sequence too short for motif scanning: {dna_sequence}")
        return {'binding_sites': [], 'scores': []}

    scores = score_pwm(dna_sequence, pwm)

    if not scores:  # Prevent empty mean calculations
        print(f"Warning: No valid scores found for sequence {dna_sequence}")
        return {'binding_sites': [], 'scores': []}

    # Dynamically adjust the threshold
    threshold = np.mean(scores) + 2 * np.std(scores)

    # Find binding sites
    binding_sites = [i for i, score in enumerate(scores) if score > threshold]

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



