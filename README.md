# Phishing URL Detector

A machine learning web app that checks whether a URL looks safe or suspicious.

**Live demo:** [add your Streamlit link here]

## How it works
- Turns each URL into 13 numeric features (length, dots, hyphens, digits, "@" symbol, IP address, HTTPS, suspicious words, and more)
- A Random Forest model trained on 100,000 URLs from the Kaggle Malicious URLs dataset classifies it as safe or suspicious
- A trusted-domain allowlist and an "uncertain" zone reduce false alarms

## Results
- Accuracy: 92.5% on 20,000 unseen URLs

## Tech
Python, pandas, scikit-learn, Streamlit

## Run locally
```
pip install -r requirements.txt
python train.py
python -m streamlit run app.py
```

The dataset is not included. Download it from Kaggle ("Malicious URLs dataset" by Manu Siddhartha) and place `malicious_phish.csv` in the project folder.

## Limitations
The model only looks at the text of a URL, not the website's reputation, so some safe links with long or complex addresses may be flagged. This is an educational project, not a replacement for real security tools.