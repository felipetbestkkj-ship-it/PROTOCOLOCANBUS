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
    "docs/BRANCH_POLICY.md",
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
branch_policy = (ROOT / "docs/BRANCH_POLICY.md").read_text(encoding="utf-8")
learning_skill = (ROOT / "skills/reusable-engineering-learning/SKILL.md").read_text(encoding="utf-8")
learnings = (ROOT / "LEARNINGS.md").read_text(encoding="utf-8")
decisions = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")

checks = {
    "repo oficial no AGENTS": "felipetbestkkj-ship-it/PROTOCOLOCANBUS" in agents,
    "autonomia por bloco": "Autonomia por bloco" in agents,
    "Guardrails obrigatório": "Codex Engineering Guardrails" in agents,
    "preflight obrigatório": "Preflight obrigatório" in agents,
    "Notion primeiro no preflight": "ler no Notion a Central Oficial, o Estado Oficial e o bloco ativo/planejado" in agents,
    "GitHub Connector explícito": "GitHub Connector" in agents,
    "remote-first explícito": "Operação remote-first" in agents,
    "branch por risco no AGENTS": "Branches — decisão por risco com autorização explícita" in agents,
    "main como padrão": "`main` é o padrão. Branch é ferramenta de isolamento de risco" in agents,
    "branch continua exigindo autorização": "não cria nem usa a branch automaticamente" in agents,
    "autonomia preservada após autorização": "não pedir microautorizações a cada commit ou teste" in agents,
    "branch policy canônica": "Branch é uma ferramenta de isolamento de risco" in branch_policy,
    "gate de benefício": "## Gate de benefício" in branch_policy,
    "autorização obrigatória no branch policy": "Criar ou usar qualquer branch diferente de `main` exige autorização clara e explícita do proprietário" in branch_policy,
    "main + uma temporária como padrão autorizado": "uma branch temporária autorizada" in branch_policy,
    "anti-vies de branch": "## Regra anti-viés" in branch_policy,
    "workflows explica risco": "Branch só faz sentido quando isola um risco real" in workflows_doc,
    "workflows preserva autorização": "não cria nem usa a branch sem autorização clara e explícita do proprietário" in workflows_doc,
    "workflows preserva autonomia": "não surgem microautorizações novas" in workflows_doc,
    "main única no estado atual": "`main` é a única linha técnica ativa" in state,
    "decisão D-011 atual": "D-011 — Main única durante a fase de descoberta" in decisions,
    "decisão D-012 permanente": "D-012 — Branch somente por benefício de isolamento + autorização explícita" in decisions,
    "aprendizado L-003 atualizado": "Paralelismo não justifica branch durante descoberta" in learnings,
    "política remota presente": "estado remoto como fonte oficial" in remote,
    "remote policy branch por risco": "## Política de branches por risco" in remote,
    "remote policy preserva autorização": "criar ou usar qualquer branch diferente de `main` continua exigindo autorização clara e explícita do proprietário" in remote,
    "remote policy preserva autonomia": "commits, testes, correções e documentação" in remote,
    "workflow humano documentado": "📱 GERAR APK PARA INSTALAR" in workflows_doc,
    "apk autoexplicativo": "INSTALAR-ESTE-APK_" in workflows_doc,
    "workflow governança autoexplicativo": "✅ VERIFICAR SE O PROJETO ESTÁ ORGANIZADO" in workflow,
    "workflow aceita branch temporária nomeada": "work/*|lab/*" in workflow,
    "workflow não finge validar Notion": "este workflow não consegue provar a autorização do proprietário no Notion" in workflow,
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

print("PASS: governança, branch por risco com autorização, autonomia, Guardrails, operação remota, workflows, skills e aprendizado estão amarrados.")
