import requests
import numpy as np
import json
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


def fetch_pfm_from_jaspar(tf_matrix_id):
    """
    Fetches the Position Frequency Matrix (PFM) from JASPAR for a given transcription factor matrix ID.
    """
    jaspar_url = f"https://jaspar.genereg.net/api/v1/matrix/{tf_matrix_id}/"

    try:
        response = requests.get(jaspar_url)
        response.raise_for_status()  # Raise error for bad requests
        
        data = response.json()
        print(f"Full response from JASPAR for {tf_matrix_id}: {json.dumps(data, indent=2)}")  # Debugging

        if "pfm" not in data:
            print("Error: PFM data not found in JASPAR response.")
            return None

        pfm_matrix = data["pfm"]

        # Check if the matrix is in an expected dictionary format
        if not isinstance(pfm_matrix, dict):
            print(f"Unexpected PFM structure: {pfm_matrix}")
            return None

        pfm = {
            'A': pfm_matrix.get('A', []),
            'C': pfm_matrix.get('C', []),
            'G': pfm_matrix.get('G', []),
            'T': pfm_matrix.get('T', [])
        }

        return pfm

    except requests.exceptions.RequestException as e:
        print(f"Error fetching PFM from JASPAR: {e}")
        return None
