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
    "REMOTE_OPERATION_POLICY.md",
    "WORKFLOWS.md",
    "SKILLS_INDEX.md",
    "docs/LEARNING_SYSTEM.md",
    "skills/reusable-engineering-learning/SKILL.md",
    "skills/artifact-forensics/SKILL.md",
    "skills/android-apk-differential-triage/SKILL.md",
    "skills/runtime-static-correlation/SKILL.md",
    "skills/cross-source-state-reconciliation/SKILL.md",
    "skills/can-frame-differential-analysis/SKILL.md",
    "skills/evidence-narrowing/SKILL.md",
]

missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    print("FAIL: arquivos obrigatórios ausentes:")
    for name in missing:
        print(f"- {name}")
    sys.exit(1)

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
state = (ROOT / "PROJECT_STATE.md").read_text(encoding="utf-8")
remote = (ROOT / "REMOTE_OPERATION_POLICY.md").read_text(encoding="utf-8")
workflows_doc = (ROOT / "WORKFLOWS.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/governance.yml").read_text(encoding="utf-8")
skills_index = (ROOT / "SKILLS_INDEX.md").read_text(encoding="utf-8")
learning_system = (ROOT / "docs/LEARNING_SYSTEM.md").read_text(encoding="utf-8")
learning_skill = (ROOT / "skills/reusable-engineering-learning/SKILL.md").read_text(encoding="utf-8")

checks = {
    "repo oficial no AGENTS": "felipetbestkkj-ship-it/PROTOCOLOCANBUS" in agents,
    "autonomia por bloco": "Autonomia por bloco" in agents,
    "Guardrails obrigatório": "Codex Engineering Guardrails" in agents,
    "preflight obrigatório": "Preflight obrigatório" in agents,
    "bloqueio sem tríade": "GitHub Connector não puderem ser usados" in agents,
    "registro de modo Guardrails": "modo Guardrails efetivamente carregado" in agents,
    "Notion primeiro no preflight": "ler no Notion a Central Oficial, o Estado Oficial e o bloco ativo/planejado" in agents,
    "GitHub Connector explícito": "GitHub Connector" in agents,
    "remote-first explícito": "Operação remote-first" in agents,
    "limite de três branches": "Máximo de **3 branches remotas ativas" in agents,
    "branch work padronizada": "work/f<fase>-<objetivo-curto>" in agents,
    "branch lab padronizada": "lab/f<fase>-<pergunta-curta>" in agents,
    "sem develop por padrão": "Não existe `develop` por padrão" in agents,
    "política remota presente": "estado remoto como fonte oficial" in remote,
    "ordem Notion Guardrails GitHub": "Notion" in remote and "Codex Engineering Guardrails" in remote and "GitHub Connector" in remote,
    "workflow humano documentado": "📱 GERAR APK PARA INSTALAR" in workflows_doc,
    "apk autoexplicativo": "INSTALAR-ESTE-APK_" in workflows_doc,
    "workflow governança autoexplicativo": "✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO" in workflow,
    "checagem remota de branches": "Branches remotas ativas" in workflow,
    "próximo bloco no estado": "Próximo bloco" in state,
    "índice de skills no contrato": "SKILLS_INDEX.md" in agents,
    "skills não bloqueantes": "ausência/inaplicabilidade de skill **não bloqueia**" in agents.lower(),
    "seleção autônoma de skill": "selecionar autonomamente apenas as skills relevantes" in agents,
    "learning distiller no fechamento": "Learning Distiller" in agents,
    "catálogo contém skill de aprendizado": "reusable-engineering-learning" in skills_index,
    "catálogo contém narrowing": "evidence-narrowing" in skills_index,
    "promoção controlada": "Gate de promoção para skill" in learning_system,
    "sem transcript como aprendizado": "não copiar o histórico completo do chat" in learning_skill.lower(),
}

failed = [label for label, ok in checks.items() if not ok]
if failed:
    print("FAIL: contrato mínimo de governança incompleto:")
    for label in failed:
        print(f"- {label}")
    sys.exit(1)

print("PASS: governança, Guardrails, operação remota, branches, workflows, skills e aprendizado estão amarrados.")
