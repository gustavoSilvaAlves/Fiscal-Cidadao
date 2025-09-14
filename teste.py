import requests
import base64

API_URL = "http://localhost:8080"
API_KEY = "chave_secreta_teste"
instance_id = "10761057-1bf5-47c2-9c14-7419a158cfe2"

headers = {
    "apikey": API_KEY
}

# Pegar o QR code
resp = requests.get(f"{API_URL}/manager/instance/{instance_id}/qrcode", headers=headers)
data = resp.json()

if "qrcode" in data:
    qr_base64 = data["qrcode"]
    # Salvar como imagem
    with open("whatsapp_qr.png", "wb") as f:
        f.write(base64.b64decode(qr_base64))
    print("QR code salvo como whatsapp_qr.png")
else:
    print(data)
