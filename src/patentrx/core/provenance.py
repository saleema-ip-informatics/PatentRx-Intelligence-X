"""Local source file integrity metadata, not expert attestation."""
import hashlib
from pathlib import Path


def source_fingerprint(path: str) -> dict:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    return {"filename": p.name, "bytes": p.stat().st_size,
            "sha256": digest.hexdigest(), "expert_verified": False}
