exports.predictLoanRepayment = async (req, res) => {
  try {
    if (!req.body || Object.keys(req.body).length === 0) {
      return res.status(400).json({ error: 'Missing required financial/personal data in request body' });
    }

    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(req.body)
    });

    if (!response.ok) {
      const errData = await response.text();
      return res.status(response.status).json({ error: 'ML Service Error', details: errData });
    }

    const mlData = await response.json();

    // Use CatBoost as the primary model
    const primaryProbability = mlData.catboost.probability;

    let decision = "REJECT";
    let risk_level = "HIGH RISK";

    if (primaryProbability > 0.85) {
      decision = "APPROVE";
      risk_level = "LOW RISK";
    } else if (primaryProbability >= 0.6) {
      decision = "REVIEW";
      risk_level = "MEDIUM RISK";
    }

    const finalResponse = {
      decision,
      probability: primaryProbability,
      risk_level,
      model_outputs: mlData
    };

    res.json(finalResponse);
  } catch (error) {
    res.status(500).json({ error: 'Failed to process loan prediction', details: error.message });
  }
};
