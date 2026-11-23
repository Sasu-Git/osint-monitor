"""Measure RSS delta of loading the model + encoding 256 short texts, torch threads=2 (CPU)."""
import os, sys, time, json, ctypes
os.environ.setdefault("HF_HUB_OFFLINE", "1")
import torch
torch.set_num_threads(2)
from sentence_transformers import SentenceTransformer
def rss():
    """Current resident set (MiB), stdlib only: Windows working set via ctypes, Linux via /proc."""
    if sys.platform == "win32":
        from ctypes import wintypes
        class C(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                (n, ctypes.c_size_t) for n in ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                 "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                 "PagefileUsage", "PeakPagefileUsage")]
        c = C(); c.cb = ctypes.sizeof(c)
        k = ctypes.WinDLL("kernel32", use_last_error=True); p = ctypes.WinDLL("psapi", use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        p.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(C), wintypes.DWORD]
        p.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(c), c.cb)
        return c.WorkingSetSize / 2**20
    for l in open("/proc/self/status"):
        if l.startswith("VmRSS"): return int(l.split()[1]) / 1024
base = rss()
t0 = time.perf_counter()
m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                        revision="e8f8c211226b894fcb81acc59f3b34ba3efd5f42", device="cpu")
load_s = time.perf_counter() - t0; after_load = rss()
base_texts = ["Government forces shelled the northern district overnight, officials said.",
              "El presidente anuncio nuevas sanciones contra el sector energetico.",
              "Il governo ha convocato un vertice di emergenza sulla crisi.",
              "Oil prices jumped after the strike on a refinery.",
              "Protesters gathered outside parliament demanding early elections."]
texts = [f"{base_texts[i % 5]} #{i}" for i in range(256)]
m.encode(texts[:8], show_progress_bar=False)  # warmup
w = rss(); peak = w; times = []
for _ in range(5):
    t = time.perf_counter(); m.encode(texts, batch_size=32, show_progress_bar=False)
    times.append(time.perf_counter() - t); peak = max(peak, rss())
best = min(times)
print(json.dumps({"rss_baseline_mb": round(base), "rss_after_load_mb": round(after_load),
  "load_delta_mb": round(after_load - base), "rss_after_encode_peak_mb": round(peak),
  "total_delta_mb": round(peak - base), "load_seconds": round(load_s, 1),
  "encode256_best_s": round(best, 2), "encode256_median_s": round(sorted(times)[2], 2),
  "texts_per_s_best": round(256 / best, 1), "threads": 2, "batch_size": 32}, indent=1))
