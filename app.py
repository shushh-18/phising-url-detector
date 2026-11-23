from urllib.parse import urlparse

import joblib
import pandas as pd
import streamlit as st

from features import extract_features

st.set_page_config(page_title="Phishing URL Detector", page_icon="🛡️")

# Well-known domains that are treated as trusted
TRUSTED = {
    "google.com", "claude.ai", "anthropic.com", "github.com",
    "wikipedia.org", "youtube.com", "microsoft.com", "apple.com",
    "linkedin.com", "kaggle.com",
}


def is_trusted(url):
    full = url if "://" in url else "http://" + url
    host = urlparse(full).netloc.lower().split(":")[0]
    return any(host == d or host.endswith("." + d) for d in TRUSTED)


@st.cache_resource
def load_model():
    data = joblib.load("model.joblib")
    return data["model"], data["columns"]


model, columns = load_model()

st.title("🛡️ Phishing URL Detector")
st.write(
    "Paste a link to check whether it looks safe or suspicious. "
    "The model is a Random Forest trained on about 100,000 URLs."
)

url = st.text_input("Enter a URL", placeholder="http://example.com/login")

if st.button("Check URL"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        features = pd.DataFrame([extract_features(url)])[columns]
        prob = model.predict_proba(features)[0][1]

        if is_trusted(url):
            st.success("✅ Trusted domain (on the allowlist)")
        elif prob >= 0.65:
            st.error(f"⚠️ Suspicious ({prob:.0%} risk score)")
        elif prob >= 0.35:
            st.warning(f"🤔 Uncertain ({prob:.0%} risk score). Check it carefully.")
        else:
            st.success(f"✅ Looks safe ({prob:.0%} risk score)")

        with st.expander("See the features the model used"):
            st.dataframe(features.T.rename(columns={0: "value"}))
#(python -m streamlit run app.py)
st.caption("Educational project. Not a replacement for real security tools.")