sudo add-apt-repository universe
sudo apt update
sudo apt install tesseract-ocr
uvicorn main:app --host 0.0.0.0 --port ${PORT} --forwarded-allow-ips '*'