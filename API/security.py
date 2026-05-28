import base64
import hashlib

import bcrypt


def _prehash(password: str) -> bytes:
    # SHA-256 → base64 keeps input to bcrypt at 44 bytes, safely under its 72-byte limit
    return base64.b64encode(hashlib.sha256(password.encode()).digest())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_prehash(password), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(_prehash(password), hashed.encode())
