# Create virtual environment
python -m venv env
source env/bin/activate

pip install -U -r requirements.txt -q

# Run app-cli.py
python app-cli.py

# Remove virtual environment
rm -rf env
