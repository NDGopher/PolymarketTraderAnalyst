from __future__ import annotations

import base64
import time
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from suspension_lab.config import WS_PATH


def load_private_key(path: str | Path):
    pem = Path(path).read_bytes()
    return serialization.load_pem_private_key(pem, password=None)


def sign_message(private_key, message: str) -> str:
    sig = private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(sig).decode("utf-8")


def auth_headers(api_key_id: str, private_key, method: str, path: str) -> dict[str, str]:
    ts = str(int(time.time() * 1000))
    clean_path = path.split("?", 1)[0]
    signature = sign_message(private_key, ts + method.upper() + clean_path)
    return {
        "KALSHI-ACCESS-KEY": api_key_id,
        "KALSHI-ACCESS-SIGNATURE": signature,
        "KALSHI-ACCESS-TIMESTAMP": ts,
    }


def ws_auth_headers(api_key_id: str, private_key) -> dict[str, str]:
    return auth_headers(api_key_id, private_key, "GET", WS_PATH)
