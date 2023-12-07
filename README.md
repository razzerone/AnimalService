# Animal service

## Local use

### Environment variables
You should set up environment variables (see `.env.example`)

### Keys
Generate rs256 keys (requires openssl)
```shell
cd rs256
bash gen_keys.sh
```

### Python venv
Create and activate virtual environment 
```shell
python -m venv venv
source ./venv/bon/activate
```
Install dependencies
```shell
pip install --upgrade -r requirements.txt
```

### Run
Run application
```shell
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Docker compose
Fill `.env` file (see `.env.example`), then run
```shell
docker compose up -d
```