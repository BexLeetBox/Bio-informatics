import requests
import numpy as np
JASPAR_API_URL = "https://jaspar.elixir.no/api/v1/matrix/"

def fetch_pwm_from_jaspar(matrix_id):
    """
    Fetches a PWM motif from JASPAR given the matrix ID.
    
    Args:
        matrix_id (str): The JASPAR matrix ID (e.g., "MA0004.1").
    
    Returns:
        dict: A dictionary containing the PWM if successful, otherwise None.
    """
    url = f"https://jaspar.elixir.no/api/v1/matrix/{matrix_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pfm = data.get("pfm", {})

        print(f"Retrieved PFM for {matrix_id}: {pfm}")  # Debugging

        # Convert PFM to probabilities (normalize each column)
        pwm = {}
        total_counts = np.array(list(pfm.values())).sum(axis=0) + 1e-9  # Avoid division by zero
        for base, counts in pfm.items():
            pwm[base] = np.array(counts) / total_counts  # Normalize instead of log transform

        print(f"Converted PWM (Probability-based) for {matrix_id}: {pwm}")  # Debugging
        return pwm
    else:
        print(f"Error fetching PWM for {matrix_id}: {response.status_code}")
        return None
