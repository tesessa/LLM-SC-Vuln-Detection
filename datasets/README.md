# 📁 Datasets

This folder contains curated datasets used in our smart contract vulnerability detection framework.

  ### 📂 `weaknessCodeSnippets/`
  
  This subfolder contains JSONL-formatted code samples derived from the [SmartBugs-Wild](https://github.com/smartbugs/smartbugs) dataset. The data includes both positive and negative code snippets intended for fine-tuning and evaluating our LLM-based detection models.
  
  #### 📄 `weakness_sniffer_gemini.jsonl`
  
  - ~22,000 **positive** examples (snippets containing known weakness patterns)
  - ~2,000 **negative** examples (clean or safe snippets)
  - Formatted in prompt/completion style for LLM ingestion (on Google Cloud for VertexAI)

---

> All data was curated, filtered, and token-normalized to maximize training quality and minimize noise.
