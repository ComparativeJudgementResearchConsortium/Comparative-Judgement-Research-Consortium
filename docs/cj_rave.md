---
id: cj_rave
title: CJ RAVE Dataset
---

## Overview

The CJ RAVE (Research Agenda Voting Exercise) dataset was collected at a special meeting of the Comparative Judgement Research Consortium held in Loughborough in May 2026. Twenty-two researchers in the comparative judgement community judged pairs of research questions, indicating which question they considered higher priority for advancing the field.

The study comprised 114 research questions spanning topics such as judge reliability, model diagnostics, pair allocation strategies, AI integration, and psychometric foundations. Participants made 1198 pairwise comparisons in total. Rankings were estimated using a Bayesian Bradley-Terry model.

## Human Judgement Data

[Download CJRC2026_RAVE.csv](https://github.com/codingWithAndy/Comparative-Judgement-Research-Consortium/blob/main/comparison_data/CJRC2026_RAVE.csv)

Each row represents one pairwise comparison made by one participant. Participant identifiers have been anonymised (P01-P22).

| Column | Description |
|--------|-------------|
| `participant_id` | Anonymous participant identifier (P01-P22) |
| `choice_id1` | Numeric ID of the first item presented |
| `choice_id2` | Numeric ID of the second item presented |
| `winner_id` | Numeric ID of the item selected as higher priority |
| `choice1_text` | Full text of item 1 |
| `choice2_text` | Full text of item 2 |

## LLM Data

[Download CJRC2026_RAVE_llm.csv](https://github.com/codingWithAndy/Comparative-Judgement-Research-Consortium/blob/main/comparison_data/CJRC2026_RAVE_llm.csv)

In addition to human judgements, all 6441 unique pairs (114 items x 113 / 2) were submitted to GPT-5.1 via the Azure API Management gateway. Of these, 6119 received a parseable response; the remaining 322 were marked invalid and excluded from this file. The model was run at temperature 0.0 with the following system prompt:

> *You are an expert in comparative judgement research methods. Which of these two research questions would most advance the theory or application of comparative judgement. Only answer with either A or B*

Each pair was presented as a user message in the form:

```
A: <question text>
B: <question text>
```

The model response ("A" or "B") was parsed to identify the winning item. All pairs were completed in a single run. The `participant_id` column contains the model identifier (`gpt-5.1`). The column schema is identical to the human judgement file.

## Analysis Code

[Download fit_bt_split_halves.R](https://github.com/codingWithAndy/Comparative-Judgement-Research-Consortium/blob/main/fit_bt_split_halves.R)

This R script fits a Bayesian Bradley-Terry model to the RAVE comparison data using the `speedyBBT` package and performs a split-halves reliability analysis (200 random splits of judges). It produces:

- Posterior median quality estimates with 95% credible intervals for all 114 research questions
- A ranked list of the questions
- Split-halves reliability correlations summarising inter-judge agreement

## Top 10 Research Questions

The 10 highest-priority research questions as estimated by the Bayesian Bradley-Terry model from the human data, ranked by posterior median score:

| Rank | Score | Question |
|------|-------|----------|
| 1 | 2.067 | What's the best way of generalising from data on judgements made by a sample of judges to judgements made by a population of judges? |
| 2 | 2.039 | What are the best strategies for structuring a data collection that exposes individual raters to repeated pairs and/or sets of pairs that can reveal intransitivity and instability, in order to assess the reliability of individual raters and distinguish variation within rater from variation across raters? |
| 3 | 1.663 | How do we tell the difference between judges who are providing no information versus judges who have a different opinion to the rest of the group? |
| 4 | 1.607 | How does cognitive load affect pairwise comparisons? Is there a threshold in the amount of information being processed beyond which comparison becomes harder than absolute judgement? If so, how can it be approximated? |
| 5 | 1.501 | What are best approaches to developing CJs so that they yield reliable and valid scores when assessing individual differences? How to create optimal CJ designs that minimise the assessment length and complexity of CJ blocks but maximise reliability and construct validity? How to incorporate response time and other process data in CJ designs? How to balance desirability matching and latent attribute recovery? |
| 6 | 1.271 | Reliability = consensus? Researchers sometimes use reliability measures (SSR/SHR) as an indicator of consensus between the judges about some construct. Is this a valid inference? |
| 7 | 1.191 | How should we evaluate goodness-of-fit for comparative judgement models, and what diagnostics are most informative for people using them? |
| 8 | 1.187 | What potential wider applications of CJ should be a focus for research (e.g. peer review of funding applications, driver training, sentencing decisions, recruitment, resource prioritisation)? |
| 9 | 1.114 | Humans are often better at pairwise comparison than absolute scoring — is this still true when AI is the assessor? |
| 10 | 1.073 | How do we best control for particular aspects of representations (e.g. length)? Can we factor these out of the CJ scores? |
