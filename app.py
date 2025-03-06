from flask import Flask, request, render_template, jsonify
from flask import Flask, request, render_template, jsonify
import numpy as np
import json
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from utils.pwm_scanner import scan_dna_sequence 
from utils.jaspar_api import fetch_pwm_from_jaspar, fetch_pfm_from_jaspar  
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_pwm', methods=['POST'])
def get_pwm():
    data = request.json
    tf_matrix_id = data.get('matrix_id', '')

    if not tf_matrix_id:
        return jsonify({'error': 'Missing transcription factor ID'}), 400

    pwm = fetch_pwm_from_jaspar(tf_matrix_id)
    if pwm is None:
        return jsonify({'error': 'Failed to fetch PWM'}), 500

    return jsonify({'pwm': pwm})

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.json
        print("Received JSON data:", data)  # Debugging

        dna_sequence = data.get('dna_sequence', '').strip().upper()
        tf_matrix_id = data.get('tf_matrix_id', '').strip()

        if not dna_sequence or not tf_matrix_id:
            print("Error: Missing DNA sequence or TF motif")  # Debugging
            return jsonify({'error': 'Missing DNA sequence or TF motif'}), 400

        pwm = fetch_pwm_from_jaspar(tf_matrix_id)
        if pwm is None:
            print("Error: Could not fetch PWM")  # Debugging
            return jsonify({'error': 'Could not fetch PWM'}), 500
        pfm = fetch_pfm_from_jaspar(tf_matrix_id)  

        if pfm is None:
            print("Error: Could not fetch PFM")  # Debugging
            return jsonify({'error': 'Could not fetch PFM'}), 500

        results = scan_dna_sequence(dna_sequence, pwm, pfm)
        binding_sites = results.get("binding_sites", [])
        scores = results.get("scores", [])

        # Generate interactive Plotly JSON data
        plot_data = generate_plotly_json(scores)

        # ✅ Pass PWM into highlight function
        highlighted_sequence = highlight_binding_sites(dna_sequence, binding_sites, pwm, pfm)

        return jsonify({
            'binding_sites': binding_sites,
            'scores': scores,
            'plot_data': plot_data,  # Send JSON plot data
            'highlighted_sequence': highlighted_sequence
        })

    except Exception as e:
        print("Unexpected error:", str(e))  # Debugging
        traceback.print_exc()  # Print full traceback
        return jsonify({'error': 'Internal server error'}), 500

def generate_plotly_json(scores):
    trace = go.Scatter(
        x=list(range(len(scores))),
        y=scores,
        mode='markers',
        line=dict(
            color='#00ff88',  # Neon green accent
            width=2.5,
            shape='spline',
            smoothing=1.3
        ),
        marker=dict(
            color='#00ff88',
            size=8,
            line=dict(width=1, color='#1a1a1a'),
            opacity=0.8
        ),
        name="Binding Score",
        hoverinfo="y+x",
        hovertemplate="<b>Position</b>: %{x}<br><b>Score</b>: %{y:.2f}<extra></extra>"
    )

    layout = go.Layout(
        title={
            'text': "Binding Score Distribution",
            'font': {'size': 20, 'family': "Arial", 'color': '#ffffff'}
        },
        xaxis=dict(
            title="Position in DNA Sequence",
            showgrid=False,
            titlefont=dict(size=14, family='Arial', color='#a0a0a0'),
            tickfont=dict(size=12, color='#ffffff'),
            linecolor='#3d3d3d',
            mirror=True
        ),
        yaxis=dict(
            title="Binding Score",
            showgrid=False,
            titlefont=dict(size=14, family='Arial', color='#a0a0a0'),
            tickfont=dict(size=12, color='#ffffff'),
            linecolor='#3d3d3d',
            mirror=True
        ),
        paper_bgcolor='rgba(30, 30, 30, 1)',
        plot_bgcolor='rgba(30, 30, 30, 1)',
        hoverlabel=dict(
            bgcolor='#1a1a1a',
            font_size=14,
            font_family="Arial",
            font_color='#00ff88'
        ),
        margin=dict(l=50, r=50, b=50, t=80),
        hovermode='x unified',
        showlegend=True,  # Enable legend to show trace names
        updatemenus=[  # Add interactive button
    
]
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(
        hoverdistance=100,
        spikedistance=1000,
        transition={'duration': 300}
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



def highlight_binding_sites(sequence, binding_sites, pwm, pfm):
    highlighted = list(sequence)
    
    if pwm is None or 'A' not in pwm:
        print("Error: Invalid PWM data")
        return sequence  

    motif_length = len(pwm['A'])

    for i in binding_sites:
        if i + motif_length <= len(sequence):
            subseq = sequence[i:i + motif_length]

            # Verify the sequence strictly follows the PFM motif
            is_valid = all(pfm[base][j] > 0.05 for j, base in enumerate(subseq) if base in pfm)

            if is_valid:
                for j in range(motif_length):
                    highlighted[i + j] = f"<span class='highlight'>{sequence[i + j]}</span>"

    return "".join(highlighted)


if __name__ == '__main__':
    app.run(debug=True)