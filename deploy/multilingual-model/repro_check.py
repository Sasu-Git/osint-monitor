"""Reproducibility check: encode fixed multilingual sentences, emit hash + first-5 dims (1e-5).
Run on laptop now, on VM after install, then compare with compare_repro.py.
  HF_HUB_OFFLINE=1 python repro_check.py --out repro-<host>.json
"""
import argparse, hashlib, json, platform, sys, os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

REPO_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
REVISION = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
SENTENCES = [
 ("en", "The ceasefire talks collapsed after overnight missile strikes."),
 ("en", "Central bank raises interest rates to curb inflation."),
 ("en", "Earthquake of magnitude 6.1 strikes off the coast."),
 ("es", "Las conversaciones de alto el fuego fracasaron tras los ataques con misiles."),
 ("es", "El banco central sube los tipos de interes para frenar la inflacion."),
 ("es", "Un terremoto de magnitud 6,1 sacude la costa."),
 ("it", "I colloqui sul cessate il fuoco sono falliti dopo gli attacchi missilistici notturni."),
 ("it", "La banca centrale alza i tassi di interesse per frenare l'inflazione."),
 ("it", "Un terremoto di magnitudo 6,1 colpisce la costa."),
 ("fr", "Les negociations de cessez-le-feu ont echoue apres les frappes de missiles nocturnes."),
 ("fr", "La banque centrale releve ses taux d'interet pour freiner l'inflation."),
 ("de", "Die Waffenstillstandsgespraeche scheiterten nach naechtlichen Raketenangriffen."),
 ("de", "Die Zentralbank erhoeht die Zinsen, um die Inflation zu daempfen."),
 ("uk", "Переговори про припинення вогню провалилися після нічних ракетних ударів."),
 ("uk", "Центральний банк підвищує відсоткові ставки для стримування інфляції."),
 ("ru", "Переговоры о прекращении огня провалились после ночных ракетных ударов."),
 ("ru", "Центральный банк повышает процентные ставки для сдерживания инфляции."),
 ("ar", "انهارت محادثات وقف إطلاق النار بعد الضربات الصاروخية الليلية."),
 ("ar", "البنك المركزي يرفع أسعار الفائدة لكبح التضخم."),
 ("ar", "زلزال بقوة 6.1 درجة يضرب الساحل."),
]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    ap.add_argument("--threads", type=int, default=2)
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    m = SentenceTransformer(REPO_ID, revision=REVISION, device="cpu")
    emb = m.encode([s for _, s in SENTENCES], batch_size=20, convert_to_numpy=True,
                   normalize_embeddings=False, show_progress_bar=False).astype(np.float32)
    assert emb.shape == (len(SENTENCES), 384), emb.shape
    ehash = hashlib.sha256(np.ascontiguousarray(emb).tobytes()).hexdigest()
    rounded_hash = hashlib.sha256(np.round(emb, 4).astype(np.float32).tobytes()).hexdigest()
    n = emb / np.linalg.norm(emb, axis=1, keepdims=True)
    out = {
      "model": REPO_ID, "revision": REVISION,
      "env": {"python": platform.python_version(), "platform": platform.platform(),
              "machine": platform.machine(), "torch": torch.__version__,
              "threads": a.threads, "sentence_transformers": __import__("sentence_transformers").__version__,
              "numpy": np.__version__},
      "dtype": "float32", "shape": list(emb.shape),
      "embeddings_sha256_bitwise": ehash,
      "embeddings_sha256_rounded_1e-4": rounded_hash,
      "sentences": [{"lang": l, "text": t, "first5": [round(float(x), 5) for x in emb[i][:5]]}
                    for i, (l, t) in enumerate(SENTENCES)],
      "full_embeddings_float32_hex_sample_row0": emb[0][:8].tobytes().hex(),
      "_full_embedding_b64": __import__("base64").b64encode(emb.tobytes()).decode(),
    }
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("bitwise sha256:", ehash)

main()
