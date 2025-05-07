# Handy Utilities with Streamlit

> Collection Of Utilities For Daily Life Hacks

## Usage

### Use Online

https://handy-utils.streamlit.app

### Install Locally

```bash
git clone https://github.com/hoishing/handy-utils.git
cd handy-utils
uv sync  # install dependencies with uv
source .venv/bin/activate
streamlit run main.py
```

- add `.streamlit/secrets.toml` (optional)
- api key fields in the app will be auto-filled after adding the secret file

```ini
GEMINI_API_KEY = "gemini-api-key"
GROQ_API_KEY = "groq-api-key"
MISTRAL_API_KEY = "mistral-api-key"
```

## Questions?

Open a [github issue] or ping me on [LinkedIn]

[github issue]: https://github.com/hoishing/handy-utils/issues
[LinkedIn]: https://www.linkedin.com/in/kng2
