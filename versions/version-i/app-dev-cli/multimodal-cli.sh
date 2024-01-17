python -m venv env
source env/bin/activate
pip install -U -r requirements.txt -q
python multimodal-cli.py

rm -rf env
