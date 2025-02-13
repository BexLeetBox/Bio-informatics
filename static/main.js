async function fetchPWM() {
    let tfMatrixID = document.getElementById("tf_matrix_id").value;
    if (!tfMatrixID) {
        alert("Please enter a JASPAR matrix ID!");
        return;
    }

    let response = await fetch("/get_pwm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matrix_id: tfMatrixID })
    });

    let result = await response.json();
    if (result.error) {
        document.getElementById("pwm_output").innerText = "Error fetching PWM!";
    } else {
        document.getElementById("pwm_output").innerText = JSON.stringify(result.pwm, null, 2);
    }
}



async function scanSequence() {
    let dnaSequence = document.getElementById("dna_sequence").value.trim();
    let tfMatrixID = document.getElementById("tf_matrix_id").value.trim();

    if (!dnaSequence || !tfMatrixID) {
        alert("Please enter a DNA sequence and a JASPAR Matrix ID!");
        return;
    }

    let requestData = {
        dna_sequence: dnaSequence,
        tf_matrix_id: tfMatrixID
    };

    console.log("Sending request:", requestData);

    let response = await fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    });

    let result = await response.json();
    console.log("Response received:", result);

    if (result.error) {
        document.getElementById("scan_output").innerText = "Error: " + result.error;
        return;
    }

    // Display highlighted sequence
    document.getElementById("highlighted_sequence").innerHTML = result.highlighted_sequence;

    // Render the interactive Plotly graph
    let plotData = JSON.parse(result.plot_data);
    Plotly.newPlot("plotly-graph", plotData.data, plotData.layout);

    // Show raw JSON output for debugging
    document.getElementById("scan_output").innerText = JSON.stringify(result, null, 2);
}


