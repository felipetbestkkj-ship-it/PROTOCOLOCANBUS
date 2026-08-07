from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "AGENTS.md",
    "PROJECT_STATE.md",
    "ROADMAP.md",
    "EVIDENCE_INDEX.md",
    "DECISIONS.md",
    "LEARNINGS.md",
]

missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    print("FAIL: arquivos obrigatórios ausentes:")
    for name in missing:
        print(f"- {name}")
    sys.exit(1)

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
state = (ROOT / "PROJECT_STATE.md").read_text(encoding="utf-8")

checks = {
    "repo oficial no AGENTS": "felipetbestkkj-ship-it/PROTOCOLOCANBUS" in agents,
    "autonomia por bloco": "Autonomia por bloco" in agents,
    "Guardrails": "Codex Engineering Guardrails" in agents,
    "próximo bloco no estado": "Próximo bloco" in state,
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    print("FAIL: contrato mínimo de governança incompleto:")
    for label in failed:
        print(f"- {label}")
    sys.exit(1)

print("PASS: fundação de governança presente e coerente.")
