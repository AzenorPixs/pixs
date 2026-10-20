"""Vérifications documentaires C02 reproductibles ; aucune écriture ni accès aux secrets."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

_CHANGE = "add-core-postgres-services"

def verify(root: Path, checkpoint: Path | None) -> dict:
    root = root.resolve()
    change = root / "openspec/changes" / _CHANGE
    if not change.is_dir():
        candidates = tuple((root / "openspec/changes/archive").glob("????-??-??-" + _CHANGE))
        if len(candidates) != 1:
            raise ValueError("Archive C02 absente ou ambiguë")
        change = candidates[0]
    req = change / "requirements.md"
    text = req.read_text(encoding="utf-8")
    errors = []
    rows = []
    scenarios = {"R": 0, "T": 0}
    for line in text.splitlines():
        if not re.match(r"\| C02-[RT][0-9]{2} \|", line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        rid, source, references = cells[:3]
        rows.append(rid)
        match = re.search(r"\[([^\]]+)\]\(([^)#]+)#L([0-9]+)\)", source)
        if match is None:
            errors.append([rid, "REFERENCE_FORMAT"])
            continue
        target = (req.parent / match.group(2)).resolve()
        if not target.is_relative_to(root / "openspec/specs"):
            errors.append([rid, "REFERENCE_SCOPE"])
            continue
        lines = target.read_text(encoding="utf-8").splitlines()
        index = int(match.group(3)) - 1
        title = match.group(1).split("—", 1)[-1].strip()
        if not 0 <= index < len(lines) or lines[index] != "### Requirement: " + title:
            errors.append([rid, "REQUIREMENT_TITLE_LINE"])
            continue
        stop = next((j for j in range(index+1,len(lines)) if lines[j].startswith("### Requirement:")),len(lines))
        names = {s[len("#### Scenario: "):] for s in lines[index:stop] if s.startswith("#### Scenario: ")}
        wanted = [s.strip() for s in references.split(";") if s.strip()]
        scenarios[rid[4]] += len(wanted)
        for name in wanted:
            if name not in names:
                errors.append([rid, "SCENARIO_TITLE", name])
    hashes = re.findall(r"- \x60(openspec/specs/[^\x60]+)\x60 : \x60([0-9a-f]{64})\x60", text)
    for relative, digest in hashes:
        path = (root / relative).resolve()
        if not path.is_relative_to(root / "openspec/specs") or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append([relative, "CANON_HASH_DRIFT"])
    expected_rows = {"C02-R%02d" % n for n in range(1,19)} | {"C02-T%02d" % n for n in range(1,55)}
    if set(rows) != expected_rows or len(rows) != 72 or scenarios != {"R":24,"T":65} or len(hashes) != 18:
        errors.append(["MATRIX", "COUNTS_OR_ROWS"])
    checked = 0
    if checkpoint is not None:
        path = checkpoint.resolve()
        if not path.is_relative_to(root / "output/cismp") or path.name != "state.json":
            raise ValueError("Checkpoint hors périmètre")
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("change_id") != _CHANGE or state.get("project_root") != str(root):
            raise ValueError("Identité checkpoint divergente")
        expected = state.get("written_files")
        if type(expected) is not dict or not expected:
            raise ValueError("Empreintes attendues absentes")
        allowed_roots = (root / "src/pixs/core", root / "tests", change)
        documents = {root / f for f in ("PROJECT.md","TECHNICAL.md","README.md","BUILD.md","DEVOPS.md")}
        for relative, proof in expected.items():
            if type(relative) is not str or type(proof) is not dict:
                raise ValueError("Empreinte mal formée")
            current = proof.get("current_path",relative)
            target = (root / current).resolve()
            digest = proof.get("sha256")
            if type(digest) is not str or re.fullmatch(r"[0-9a-f]{64}",digest) is None:
                raise ValueError("Empreinte mal formée")
            if not any(target.is_relative_to(parent) for parent in allowed_roots) and target not in documents:
                errors.append([relative,"SOURCE_SCOPE"])
                continue
            if target.suffix not in (".py",".md",".toml") or any(p.startswith(".") for p in target.relative_to(root).parts):
                errors.append([relative,"SOURCE_SCOPE"])
                continue
            data = target.read_bytes()
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                errors.append([relative,"UTF8"])
            if b"\r" in data:
                errors.append([relative,"CRLF"])
            if hashlib.sha256(data).hexdigest() != digest:
                errors.append([relative,"SOURCE_HASH_DRIFT"])
            checked += 1
    return {"requirements":len(rows),"scenario_references":scenarios,"canonical_hashes":len(hashes),"written_files_checked":checked,"errors":errors,"ok":not errors}

def main() -> int:
    parser = argparse.ArgumentParser(description="Vérifications documentaires C02 sans effet")
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--checkpoint",type=Path)
    args = parser.parse_args()
    result = verify(args.root,args.checkpoint)
    print(json.dumps(result,sort_keys=True,ensure_ascii=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
