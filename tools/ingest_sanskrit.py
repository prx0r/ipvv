#!/usr/bin/env python3
"""tools/ingest_sanskrit.py — copy held Sanskrit e-texts into site/data/sanskrit/.

Sources (bytes stay upstream; we vendor plain-text copies with provenance):
  GRETIL mirror  /tmp/gretil-corpus            (CC BY-NC-SA 4.0)
  Mukhabodha R2 snapshot (extracted to /tmp/muk-sel) (CC BY-NC 4.0)
  deitybody corpus/stotra (already vendored cleans)

Writes site/data/sanskrit/<work-id>.txt with a provenance header, and prints
the JSON patch lines for works_*.json (sanskrit_file/source/licence).
Run: python3 tools/ingest_sanskrit.py
"""
from __future__ import annotations
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
GRETIL = Path("/tmp/gretil-corpus")
MUK = Path("/tmp/muk-sel/muktabodha-lib")
OUT = ROOT / "site/data/sanskrit"
OUT.mkdir(parents=True, exist_ok=True)

# (work-id, kind, source-path-relative, provenance-label)
JOBS = [
    # Abhinavagupta — GRETIL
    ("tantraloka", "gretil", "6_sastra/3_phil/sa_abhinavagupta-tantrAloka.txt", "GRETIL KSTS 1918-38 (Jayaratha Viveka ed.) · CC BY-NC-SA 4.0"),
    ("tantrasara", "gretil", "6_sastra/3_phil/sa_abhinavagupta-tantrasAra.txt", "GRETIL Nirnaya Sagara 1918 KSTS 17 · CC BY-NC-SA 4.0"),
    ("mvv", "gretil", "6_sastra/3_phil/sa_abhinavagupta-mAlinIzlokavArttika.txt", "GRETIL KSTS 32/Hanneder · CC BY-NC-SA 4.0"),
    ("paramarthasara", "gretil", "6_sastra/3_phil/sa_abhinavagupta-paramArthasAra.txt", "GRETIL KSTS 7 · CC BY-NC-SA 4.0"),
    ("ipv", "gretil", "6_sastra/3_phil/sa_abhinavagupta-IzvarapratyabhijJAvimarzinI.txt", "GRETIL (Iyer/Pandey ed.) · CC BY-NC-SA 4.0"),
    ("kramastotra", "gretil", "6_sastra/3_phil/sa_abhinavagupta-kramastotra.txt", "GRETIL · CC BY-NC-SA 4.0"),
    ("paryantapancasika", "gretil", "6_sastra/3_phil/sa_abhinavagupta-paryantapaJcAzikA.txt", "GRETIL · CC BY-NC-SA 4.0"),
    ("ghatakarpara", "gretil", "5_poetry/2_kavya/sa_ghaTakarparakAvya-comm.txt", "GRETIL (Parlier ed., Abhinavagupta vivrti) · CC BY-NC-SA 4.0"),
    ("dhvanyaloka", "gretil", "5_poetry/1_alam/sa_Anandavardhana-dhvanyAloka-comm.txt", "GRETIL (Locana embedded) · CC BY-NC-SA 4.0"),
    # Abhinavagupta — Mukhabodha (no GRETIL plain text)
    ("ptv-madhyama", "muk", "parAtrizikAvivRti-M00044-IAST.txt", "Mukhabodha M00044 · CC BY-NC 4.0"),
    ("ptv-laghu", "muk", "parAtrIzikAlaghuvRtti-M00042-IAST.txt", "Mukhabodha M00042 · CC BY-NC 4.0"),
    ("ptv-vivrti2", "muk", "parAtrizikAvivRtI-M00154-IAST.txt", "Mukhabodha M00154 · CC BY-NC 4.0"),
    ("ipvv-vol1", "muk", "IzvarapratyabhijJAvivRtivimarzinI Volume 1-M00020-IAST.txt", "Mukhabodha M00020 · CC BY-NC 4.0"),
    ("ipvv-vol2", "muk", "IzvarapratyabhijJAvivRtivimarzinI Volume 2-M00021-IAST.txt", "Mukhabodha M00021 · CC BY-NC 4.0"),
    ("ipvv-vol3", "muk", "IzvarapratyabhijJAvivRtivimarzinI Volume 3-M00022-IAST.txt", "Mukhabodha M00022 · CC BY-NC 4.0"),
    # Utpaladeva — GRETIL
    ("ipk", "gretil", "6_sastra/3_phil/sa_utpaladeva-IzvarapratyabhijJAkArikA-with-vRtti.txt", "GRETIL Kaul Shastri 1921/Torella · CC BY-NC-SA 4.0"),
    ("ajadapramatrsiddhi", "gretil", "6_sastra/3_phil/sa_utpaladeva-ajaDapramAtRsiddhi.txt", "GRETIL KSTS 34 · CC BY-NC-SA 4.0"),
    ("sivastotravali-u", "gretil", "4_rellit/saiva/sa_utpaladeva-zivastotrAvali.txt", "GRETIL (Bailly ed.) · CC BY-NC-SA 4.0"),
    # Utpaladeva — Mukhabodha
    ("isvarasiddhi", "muk", "Izvarasiddhi-M00023-IAST.txt", "Mukhabodha M00023 (KSTS 34) · CC BY-NC 4.0"),
    ("sambandhasiddhi", "muk", "sambandhasiddhi-M00080-IAST.txt", "Mukhabodha M00080 · CC BY-NC 4.0"),
    # Ksemaraja — GRETIL
    ("phrdaya", "gretil", "6_sastra/3_phil/sa_kSemarAja-pratyabhijJAhRdaya.txt", "GRETIL · CC BY-NC-SA 4.0"),
    ("spanda-root", "gretil", "6_sastra/3_phil/sa_vasugupta-spandakArikA.txt", "GRETIL · CC BY-NC-SA 4.0"),
    ("spanda-ksem", "gretil", "6_sastra/3_phil/sa_vasugupta-spandakArikA-comm.txt", "GRETIL (Ksemaraja comm., KSTS) · CC BY-NC-SA 4.0"),
    ("vbt-root", "gretil", "6_sastra/3_phil/sa_vijJAnabhairava.txt", "GRETIL · CC BY-NC-SA 4.0"),
    ("sivasutra-root", "gretil", "4_rellit/saiva/sa_zivasUtra-with-vArttika.txt", "GRETIL Kaul Shastri 1925 · CC BY-NC-SA 4.0"),
    ("stavacintamani", "gretil", "4_rellit/saiva/sa_bhaTTanArAyaNa-stavacintAmaNi.txt", "GRETIL KSTS X (Ksemaraja comm. per ed.) · CC BY-NC-SA 4.0"),
    ("natya-root", "gretil", "5_poetry/1_natya/sa_bharata-nATyazAstra-1-1618-303335-37.txt", "GRETIL (Bharata root; Bharati itself undigitized) · CC BY-NC-SA 4.0"),
    # Ksemaraja — Mukhabodha
    ("spandanirnaya", "muk", "spandanirNaya-M00163-IAST.txt", "Mukhabodha M00163 · CC BY-NC 4.0"),
    ("spandasandoha", "muk", "spandasandoha-M00084-IAST.txt", "Mukhabodha M00084 · CC BY-NC 4.0"),
    ("sivasutravimarsini", "muk", "zivasUtravimarzinI text version-M00349-IAST.txt", "Mukhabodha M00349 · CC BY-NC 4.0"),
    ("netratantra", "muk", "netratantra-M00038-IAST.txt", "Mukhabodha M00038 · CC BY-NC 4.0"),
    ("svacchandatantra", "muk", "svacchandatantra-M00091-IAST.txt", "Mukhabodha M00091 · CC BY-NC 4.0"),
    ("parapravesika", "muk", "parAprAvezikA-M00048-IAST.txt", "Mukhabodha M00048 · CC BY-NC 4.0"),
]

def main() -> None:
    got, miss = [], []
    for wid, kind, rel, prov in JOBS:
        src = (GRETIL if kind == "gretil" else MUK) / rel
        if not src.exists():
            miss.append(f"{wid} <- {rel}"); continue
        txt = src.read_text(encoding="utf-8", errors="replace")
        head = f"### Provenance: {prov}\n### Source file: {rel}\n### Vendored: site/data/sanskrit/{wid}.txt (research/education use; respect licence)\n\n"
        (OUT / f"{wid}.txt").write_text(head + txt, encoding="utf-8")
        got.append(wid)
    print(f"ingested {len(got)}, missing {len(miss)}")
    for m in miss: print("  MISS", m)
    print("ids:", " ".join(got))

if __name__ == "__main__":
    main()
