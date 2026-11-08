# Bike Sharing Data Analysis

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Venv
```bash
python -m venv main-ds
```

Aktifkan environment:

Windows:
```bash
main-ds\Scripts\activate
```

macOS/Linux:
```bash
source main-ds/bin/activate
```

Instal dependencies:
```bash
pip install -r requirements.txt
```

## Setup Environment - Pipenv
```bash
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```