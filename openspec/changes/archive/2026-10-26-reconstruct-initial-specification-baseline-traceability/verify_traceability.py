"""Reconstituer et vérifier les preuves documentaires, sans mutation Git."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess


LOT = Path(__file__).resolve().parent
ROOT = LOT.parents[3] if LOT.parent.name == "archive" else LOT.parents[2]
H0 = "1d96ece501606330b45c6819054ba6e581b824bd"
H1 = "b83f9de8827f94fe930972a6abf6663fca7a1c29"
EVOLUTION = "6ac22961c242a8da709ec1801b7021410d18b479"
BOOTSTRAP = "openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap"
ARCHIVE = "openspec/changes/archive/2026-09-16-consolidate-initial-specification-baseline"
CAPS = ("audit", "operations", "initial-application-bootstrap", "initial-administration")
DEPS = ("reference-composition", "installation-provisioning", "identity-assurance", "authorization", "secrets-providers")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*arguments: str) -> bytes:
    result = subprocess.run(
        ["/usr/bin/git", "-c", f"safe.directory={ROOT}", *arguments],
        cwd=ROOT, check=True, capture_output=True,
    )
    return result.stdout


def historical(ref: str, path: str) -> bytes:
    require(path.startswith(("openspec/specs/", BOOTSTRAP + "/", ARCHIVE + "/")), "Chemin historique hors périmètre.")
    require(path.endswith((".md", ".yaml")), "Format historique hors périmètre.")
    return git("show", f"{ref}:{path}")


def reflow(text: str) -> str:
    paragraphs = text.split("\n\n")
    return "\n\n".join(
        p if any(re.match(r"^(?:\s|#|[-*+] |[0-9]+\. |>|`|~)", line) for line in p.splitlines())
        else " ".join(p.splitlines())
        for p in paragraphs
    )


def parse(data: bytes) -> list[dict]:
    text = data.decode("utf-8", errors="strict")
    lines = text.splitlines(keepends=True)
    headings = []
    fenced = False
    parent = None
    for index, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        if fenced:
            continue
        if line.startswith("## "):
            headings.append((index, "SECTION", "", ""))
        elif line.startswith("### Requirement: "):
            parent = line[len("### Requirement: "):].strip()
            headings.append((index, "R", parent, ""))
        elif line.startswith("#### Scenario: "):
            require(parent is not None, "Scénario sans exigence parente.")
            headings.append((index, "S", parent, line[len("#### Scenario: "):].strip()))
    units = []
    for position, (start, kind, requirement, scenario) in enumerate(headings):
        if kind == "SECTION":
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = "".join(lines[start:end]).strip()
        units.append({"kind": kind, "requirement": requirement, "scenario": scenario,
                      "line": start + 1, "body": body})
    return units


def key(unit: dict) -> tuple[str, str, str]:
    return unit["kind"], unit["requirement"], unit["scenario"]


def inventory(ref: str) -> dict[str, bytes]:
    paths = git("ls-tree", "-r", "--name-only", ref, "--", "openspec/specs").decode().splitlines()
    return {p: historical(ref, p) for p in paths if re.fullmatch(r"openspec/specs/[^/]+/spec\.md", p)}


def count(files: dict[str, bytes]) -> dict:
    units = [u for data in files.values() for u in parse(data)]
    return {"capabilities": len(files), "requirements": sum(u["kind"] == "R" for u in units),
            "scenarios": sum(u["kind"] == "S" for u in units)}


def snapshot_digest(files: dict[str, bytes]) -> str:
    return sha(b"\n".join(p.encode() + b"\0" + b for p, b in sorted(files.items())))


def verify_preservation() -> dict:
    guard = json.loads((LOT / "preservation.json").read_text(encoding="utf-8"))
    for section in ("archives", "canonical_specs"):
        for relative, digest in guard[section].items():
            if section == "archives" and not relative.startswith(ARCHIVE + "/"):
                continue
            path = ROOT / relative
            require(not path.is_symlink() and path.resolve().is_relative_to(ROOT), "Source protégée liée ou hors racine.")
            require(path.is_file() and sha(path.read_bytes()) == digest, f"Source protégée modifiée : {relative}")
    archive_paths = {str(p.relative_to(ROOT)) for p in (ROOT / ARCHIVE).rglob("*") if p.is_file()}
    expected_archive = {p for p in guard["archives"] if p.startswith(ARCHIVE + "/")}
    require(archive_paths == expected_archive, "Inventaire de l'archive cible modifié.")
    canon_paths = {str(p.relative_to(ROOT)) for p in (ROOT / "openspec/specs").glob("*/spec.md")}
    require(canon_paths == set(guard["canonical_specs"]), "Inventaire canonique modifié.")
    return {"archive_files": len(archive_paths), "canonical_specs": len(canon_paths),
            "auxiliary_initial_files": len(guard["archives"]) - len(expected_archive),
            "auxiliary_worktree_not_used": True, "auxiliary_source_ref": H1}


def build() -> dict:
    preserved = verify_preservation()
    before, after = inventory(H0), inventory(H1)
    require(count(before) == {"capabilities": 74, "requirements": 287, "scenarios": 290}, "Inventaire H0 inattendu.")
    require(count(after) == {"capabilities": 76, "requirements": 300, "scenarios": 305}, "Inventaire H1 inattendu.")
    require(git("rev-parse", H1 + "^").decode().strip() == H0, "H0 n'est pas le parent direct de H1.")
    git("merge-base", "--is-ancestor", H1, "HEAD")
    for cap in DEPS:
        require(f"openspec/specs/{cap}/spec.md" in before and f"openspec/specs/{cap}/spec.md" in after,
                f"Dépendance historique absente : {cap}")
    stable = [p for p in before if before[p] == after.get(p)]
    require(len(stable) == 72, "Les 72 capacités stables ne sont plus identiques.")
    current_files = {str(p.relative_to(ROOT)): p.read_bytes()
                     for p in sorted((ROOT / "openspec/specs").glob("*/spec.md"))}
    records = []
    evolution_files = {}
    groups = defaultdict(lambda: Counter())
    for path, target in sorted(after.items()):
        cap = path.split("/")[2]
        old_units = parse(before[path]) if path in before else []
        delta_path = f"{BOOTSTRAP}/specs/{cap}/spec.md"
        delta_units = parse(historical(H1, delta_path)) if cap in CAPS else []
        old_index = {key(u): u for u in old_units}
        delta_index = {key(u): u for u in delta_units}
        target_units = parse(target)
        require(len({key(u) for u in target_units}) == len(target_units), f"Repère historique ambigu : {path}")
        require(set(old_index).isdisjoint(delta_index), f"Delta ajouté déjà présent : {path}")
        require({key(u) for u in target_units} == set(old_index) | set(delta_index), f"Résidu normatif inexpliqué : {path}")
        now = parse(current_files[path])
        for unit in target_units:
            previous = key(unit) in old_index
            origin = old_index[key(unit)] if previous else delta_index[key(unit)]
            source_path = path if previous else delta_path
            source_ref = H0 if previous else H1
            group = "stable-72" if path in stable else cap + ("-ancien" if previous else "-bootstrap")
            groups[group][unit["kind"]] += 1
            same = origin["body"] == unit["body"]
            equivalent = reflow(origin["body"]) == reflow(unit["body"])
            require(same or equivalent, f"Texte historique non conservé : {path} {key(unit)}")
            matches = [u for u in now if key(u) == key(unit)]
            status = "REPÈRE CONSERVÉ"
            if not matches and unit["kind"] == "S":
                matches = [u for u in now if u["kind"] == "S" and u["scenario"] == unit["scenario"]]
                status = "RATTACHEMENT MODIFIÉ"
                if not matches and cap == "initial-administration" and unit["scenario"] == "Opérateur initial vérifié":
                    matches = [u for u in now if u["kind"] == "S" and u["scenario"] == "Compte fonctionnel créé explicitement"]
                    status = "REMPLACEMENT CONSTATÉ"
            require(len(matches) == 1, f"Traçabilité courante absente ou ambiguë : {path} {key(unit)}")
            current = matches[0]
            evolution_proof = None
            if status != "REPÈRE CONSERVÉ":
                if path not in evolution_files:
                    evolution_files[path] = (
                        parse(historical(EVOLUTION + "^", path)),
                        parse(historical(EVOLUTION, path)),
                    )
                previous_evolution, next_evolution = evolution_files[path]
                original = [u for u in previous_evolution if key(u) == key(unit)]
                replacement = [u for u in next_evolution if key(u) == key(current)]
                require(len(original) == len(replacement) == 1,
                        f"Évolution Git non corrélée : {path} {key(unit)}")
                require(not any(key(u) == key(unit) for u in next_evolution),
                        f"Ancien rattachement encore présent après l'évolution : {path}")
                evolution_proof = {"ref": EVOLUTION, "path": path,
                                   "before_line": original[0]["line"], "after_line": replacement[0]["line"],
                                   "before_sha256": sha(original[0]["body"].encode()),
                                   "after_sha256": sha(replacement[0]["body"].encode()),
                                   "human_approval_proven": False}
            refs = sorted(set(re.findall(r"`([^`]+)`", origin["body"])) & {p.split("/")[2] for p in after})
            if not previous:
                refs = sorted(set(refs) | set(DEPS))
            records.append({"id": f"B{len(records)+1:04d}", "capability": cap,
                            "kind": unit["kind"], "requirement": unit["requirement"], "scenario": unit["scenario"],
                            "source": {"ref": source_ref, "path": source_path, "line": origin["line"], "sha256": sha(origin["body"].encode())},
                            "target": {"ref": H1, "path": path, "line": unit["line"], "sha256": sha(unit["body"].encode())},
                            "group": group, "historical_comparison": "IDENTIQUE" if same else "REPLIEMENT DE PROSE",
                            "dependencies_explicit": refs,
                            "current": {"path": path, "line": current["line"], "requirement": current["requirement"],
                                        "scenario": current["scenario"], "status": status,
                                        "body_unchanged": current["body"] == unit["body"],
                                        "sha256": sha(current["body"].encode()),
                                        "evolution_commit": EVOLUTION if status != "REPÈRE CONSERVÉ" else None,
                                        "evolution_proof": evolution_proof}})
    require(len(records) == 605, "La matrice ne couvre pas 605 éléments.")
    require(sum(r["historical_comparison"] != "IDENTIQUE" for r in records) == 2, "Repliements historiques inattendus.")
    current_counts = dict(Counter(r["current"]["status"] for r in records))
    require(current_counts == {"REPÈRE CONSERVÉ": 600, "RATTACHEMENT MODIFIÉ": 4, "REMPLACEMENT CONSTATÉ": 1}, "Évolutions courantes inattendues.")
    return {"schema_version": 1, "before_ref": H0, "after_ref": H1,
            "head_at_capture": json.loads((LOT / "preservation.json").read_text(encoding="utf-8"))["head_at_capture"],
            "before": count(before), "after": count(after), "current_inventory": count(current_files),
            "before_digest": snapshot_digest(before), "after_digest": snapshot_digest(after),
            "stable_files": stable, "groups": {k: dict(v) for k, v in sorted(groups.items())},
            "current_status_counts": current_counts, "preservation": preserved,
            "records": records}


def render(evidence: dict) -> str:
    lines = ["# Matrice de conservation reconstruite", "",
             "Cette matrice corrige la traçabilité dans le présent lot ; l'archive reste intacte.", "",
             f"H0 : `{H0}` ; H1 : `{H1}`. H0 est le parent direct de H1.",
             "Les repères B sont des repères d'audit, sans changement d'identifiant normatif.",
             "Les preuves complètes, chemins, lignes et empreintes brutes sont dans [evidence.json](evidence.json).", "",
             "## Réconciliation des totaux", "",
             "| Origine | Exigences | Scénarios |", "| --- | ---: | ---: |"]
    for name, values in evidence["groups"].items():
        lines.append(f"| {name} | {values.get('R', 0)} | {values.get('S', 0)} |")
    lines += ["| **Total** | **300** | **305** |", "",
              "Les dix exigences et dix scénarios omis sont les 5/5 anciens d'audit et les 5/5 anciens d'operations.",
              "Les capacités sont comptées par chemins distincts : 76, sans additionner deux fois audit et operations.", "",
              "## Convention de lecture", "",
              "Source H0 = canon avant ; source D = delta du bootstrap archivé dans H1.",
              "Pour chaque capacité, les lignes source/cible renvoient aux chemins indiqués ci-dessous.",
              "Les dépendances listées sont les références de capacités explicites du bloc et celles déclarées pour le bootstrap ; absence de référence ne vaut pas indépendance.",
              "Deux exigences portent un repliement de prose documenté, sans identité brute prétendue.",
              "La colonne courante décrit la présence d'un repère, pas l'identité de tout son comportement ni un accord humain.", ""]
    for cap in sorted({r["capability"] for r in evidence["records"]}):
        lines += [f"## {cap}", "", f"Canon H0/H1/courant : `openspec/specs/{cap}/spec.md`."]
        if cap in CAPS:
            lines.append(f"D : `{BOOTSTRAP}/specs/{cap}/spec.md`, dans H1.")
        lines += ["", "| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        for r in evidence["records"]:
            if r["capability"] != cap:
                continue
            label = r["requirement"] if r["kind"] == "R" else r["scenario"] + " — sous « " + r["requirement"] + " »"
            label = label.replace("|", "&#124;")
            src = "H0" if r["source"]["ref"] == H0 else "D"
            deps = ", ".join(r["dependencies_explicit"]) or "Aucune référence explicite dans le bloc"
            now = r["current"]
            current = now["status"] + f" L{now['line']}"
            if now["status"] != "REPÈRE CONSERVÉ":
                current += f" ; `{EVOLUTION[:12]}` ; voir VERIFICATIONS.md"
            lines.append(f"| {r['id']} | {r['kind']} : {label} | {src} L{r['source']['line']} | L{r['target']['line']} | {r['historical_comparison']} | {deps} | {current} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Générer uniquement les deux documents de preuve de ce lot.")
    args = parser.parse_args()
    evidence = build()
    serialized = json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    markdown = render(evidence)
    outputs = {"evidence.json": serialized, "conservation-matrix.md": markdown}
    for name, expected in outputs.items():
        path = LOT / name
        require(not path.is_symlink(), "Destination de preuve symbolique.")
        if args.write:
            path.write_text(expected, encoding="utf-8", newline="\n")
        else:
            require(path.read_text(encoding="utf-8") == expected, f"Preuve non reproductible : {name}")
    print(json.dumps({"status": "VALIDÉ", "historical_units": len(evidence["records"]),
                      "groups": evidence["groups"], "current": evidence["current_status_counts"],
                      "protected": evidence["preservation"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
