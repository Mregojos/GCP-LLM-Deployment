python -m venv env
source env/bin/activate
pip install -U -r requirements.txt -q
py multimodal-cli.py

rm -rf env
