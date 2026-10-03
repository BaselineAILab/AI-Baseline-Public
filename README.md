# AI Baseline Public

This repository hosts public AI Baseline artifacts, examples, and reference workflows. It is intended as a lightweight distribution point for materials that help users evaluate or integrate with AI Baseline products, including packaged assistant integrations, notebooks, and generated sample outputs.

The contents of this repository may change over time as additional examples and public artifacts are released.

## Repository Contents

| Path | Description |
| --- | --- |
| `Claude/ai-baseline.mcpb` | Archived MCPB 0.1.3 Desktop extension retained for compatibility reproduction. |
| `Claude/ai-baseline-skill.zip` | Maintained remote MCP skill for evidence-backed answers with inline document citations. |
| `Notebooks/financial_research_pipeline.ipynb` | Example text-to-research notebook that extracts investment themes from source text, queries AI Baseline, and produces a grounded investment note. |
| `Notebooks/investment_note.pdf` | Historical example output; it does not demonstrate the current citation workflow. |
| `Notebooks/.env.example` | Environment variable template for local API credentials used by the notebook. |

## Claude remote MCP skill

The maintained `Claude/ai-baseline-skill.zip` uses the configured remote MCP
connection's `get_corpus_overview` and `retrieve_evidence_context` tools. Set up the
connection URL provided for your company/base, enable it for the conversation and
install the skill using your client's instructions. Configure authentication in the
connection setup; never paste an API key into chat.

The model generates answers from retrieved evidence and provider instructions.
For each claim it follows the contributing citation IDs, resolves source metadata
through the registry, and copies supplied URLs verbatim into ordinary inline
Markdown citations. Multiple contributing sources or passages retain separate links.
Missing links must be stated honestly; source summaries are not verified quotations.

On a citation-enabled deployment, links open the complete retained document at the
verified sentence, passage or chunk without a separate browser sign-in. Anyone
holding a link can read its bound document until the stored expiry: 30 minutes by
default, operator configurable. Clicks do not renew access; expired links require
fresh authorized retrieval. Expiry does not retract previously delivered text.
No Sources panel, MCP App, extra rendering call or dashboard is required.

The MCPB 0.1.3 extension is an unchanged historical artifact. Its original
instructions do not qualify the maintained remote citation experience. The skill
is built from the corresponding source in the InfoWeaver repository; do not edit
ZIP contents directly. Public deployment availability requires separate acceptance.

## Notebook Example

The `Notebooks` directory contains a self-contained research workflow that:

1. Loads a text or Markdown source file.
2. Extracts investment-relevant themes.
3. Retrieves supporting evidence from AI Baseline.
4. Generates a grounded research note using an OpenRouter-hosted model.
5. Exports the result as Markdown and, when PDF dependencies are available, PDF.

To run the notebook locally:

```bash
cd Notebooks
cp .env.example .env
```

Then add local values for:

```bash
OPENROUTER_API_KEY=
AI_BASELINE_API_KEY=
```

Open `financial_research_pipeline.ipynb` in Jupyter or another compatible notebook environment and run the cells from top to bottom. The notebook installs missing Python packages when configured to do so, and writes run artifacts under `Notebooks/ai_baseline_research_output/`.

The answer-stage compaction preserves provider instructions and notices, complete
evidence entries and their citation records, and all source metadata needed by
retained entries. Entries that cannot fit are omitted whole with an explicit notice.
Offline regression checks do not run the notebook or make model/API calls:

```bash
python3 tests/test_notebook_citations.py
```

The retained example PDF is archival. Generate a new answer through your authorized
connection to obtain fresh links; do not reuse URLs from saved output after expiry.

## Credentials

Credentials are intentionally not included in this repository. Keep real API keys in local environment variables or local `.env` files only. The provided `.env.example` file is a template and should not contain secrets.

## Intended Audience

This repository is for users, partners, and evaluators who need public AI Baseline examples or packaged integration artifacts. It is not the primary product source tree for AI Baseline services.

## Support

For AI Baseline documentation and support resources, visit:

- https://www.ai-baseline.com
- https://docs.ai-baseline.com

## License

No license file is currently included in this repository. Unless a license is added, all rights are reserved by AI Baseline.
