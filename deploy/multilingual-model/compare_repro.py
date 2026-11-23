"""Compare two repro_check outputs: bitwise hash equality, max abs diff, min per-sentence cosine."""
import base64, json, sys
import numpy as np
a, b = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:3])
ea = np.frombuffer(base64.b64decode(a["_full_embedding_b64"]), dtype=np.float32).reshape(a["shape"])
eb = np.frombuffer(base64.b64decode(b["_full_embedding_b64"]), dtype=np.float32).reshape(b["shape"])
cos = (ea * eb).sum(1) / (np.linalg.norm(ea, axis=1) * np.linalg.norm(eb, axis=1))
print("bitwise identical:", a["embeddings_sha256_bitwise"] == b["embeddings_sha256_bitwise"])
print("max abs diff:", float(np.abs(ea - eb).max()))
print("min cosine:", float(cos.min()), " 1-min cosine:", float(1 - cos.min()))
print("within 1e-4 cosine:", bool((1 - cos).max() <= 1e-4))
