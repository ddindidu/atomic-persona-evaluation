# 🎭 Atomic Persona Evaluation

> Official code & data for **“Spotting Out-of-Character Behavior: Atomic-Level Evaluation of Persona Fidelity in Open-Ended Generation”** (Findings of ACL 2025). [[arXiv](https://www.arxiv.org/pdf/2506.19352)]   
> We introduce **ACC<sub>atom</sub>**, **IC<sub>atom</sub>**, and **RC<sub>atom</sub>** – three complementary metrics that diagnose how well a generated response respects each *atomic* persona statement rather than a coarse, one-shot persona summary.


# Overview
This project provides persona assignment and evaluation prompts to assess how well persona fragments—LLM-generated statements containing a specific character—match a target persona. Leveraging principles from atomic design and prompt engineering, the toolkit helps developers analyze and refine persona content systematically using LLM APIs (e.g., GPT).


# Installation
**1. Clone this repo**
```
git clone https://github.com/ddindidu/atomic-persona-evaluation.git
cd atomic-persona-evaluation
```
**2. Install dependencies (Conda)**
```
conda env create -f env.yml          # creates env "atomeval"
conda activate atomeval
```

# Usage
## 1. Generate persona statements

## 2. Run Evaluation

