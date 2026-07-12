# Bank Marketing Streamlit Demo

## Files required

- `app.py`
- `requirements.txt`
- `best_bank_marketing_model.pkl`

Place the trained model file in the same folder as `app.py`.

## Test locally

Open Command Prompt in this folder and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `best_bank_marketing_model.pkl`.
3. Sign in to Streamlit Community Cloud.
4. Choose **Create app**.
5. Select your GitHub repository.
6. Set the main file path to `app.py`.
7. Deploy the app.
8. Copy the public URL and insert it into Section 9 of the project report.

## Suggested report wording

> A Streamlit-based web demonstration was developed to allow users to enter customer and campaign information and receive a prediction of whether the customer is likely to subscribe to a term deposit. The deployed demo is available at: [INSERT PUBLIC STREAMLIT LINK].
