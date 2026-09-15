# advisor-skills

Ten skills for advisory and knowledge work. Install: `claude plugin install advisor-skills@bwfnx`. Each skill also works as a Codex skill (every folder carries `agents/openai.yaml`).

| Skill | Use it when |
|---|---|
| `sbir-proposal-review` | A federal SBIR/STTR or grant proposal needs a pre-submission review. |
| `sbdc-funding-match-packet` | A client needs matched to grants, loans, and programs, as a packet. |
| `wiki-interview` | A wiki has gaps and you want a structured 20-question interview to fill them. |
| `teardown` | A workflow, process, or plan should be torn down (ESIA) before improving it. |
| `build-verification-audit` | An agent says a build is done and you want proof before believing it. |
| `durable-learning-protocol` | A task is wrapping up and reusable insights should be saved. Ships `scripts/learnings.py`. |
| `ai-analyst-agent` | You need a bias-resistant analytical judgment under uncertainty. |
| `transcript-to-wiki-pipeline` | Training transcripts should be processed into wiki articles. Ships `scripts/scan_pipeline.py`. |
| `cos` | "What am I behind on?" — one Now, one Next, everything else parked. Reads `TASKS.md`. |
| `email-followups` | You're avoiding replies. Finds what's owed, drafts them, never sends. |

Placeholders like `{{WORKSPACE_ROOT}}` and `{{CRM}}` mean "your workspace root" and "your CRM"; replace them or leave them and the skill will ask.
