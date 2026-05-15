---
id: cj_rave
title: CJ RAVE Dataset
---

## Overview

The CJ RAVE (Research Agenda Voting Exercise) dataset was collected at a special meeting of the Comparative Judgement Research Consortium held in Belgium in May 2026. Twenty-two researchers in the comparative judgement community judged pairs of research questions, indicating which question they considered higher priority for advancing the field.

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

In addition to human judgements, all 6441 unique pairs (114 items x 113 / 2) were submitted to GPT-5.1 via the Azure API Management gateway. Of these, 6119 received a parseable response; the remaining 322 were marked invalid and excluded from this file. The model was given the following system prompt:

> *Which of these two research questions would most advance comparative judgement?*

The two research questions were presented as options A and B. The model response ("A" or "B") was parsed to identify the winning item. All pairs were completed in a single run. The `participant_id` column contains the model identifier (`gpt-5.1`). The column schema is identical to the human judgement file.

## Top Research Questions

The 20 highest-priority research questions as estimated by the Bayesian Bradley-Terry model, displayed in random order:

1. What is the 'unit of measurement' in CJ, and to what extent should we expect it to be invariant across CJ studies that make comparisons of the same construct? When simulating judgement data from a CJ study, what principles should we use to set the standard deviation (or other distributional parameters) of theta?
2. What are best approaches to developing CJs so that they yield reliable and valid scores when assessing individual differences? How to create optimal CJ designs that minimise the assessment length and complexity of CJ blocks but maximise reliability and construct validity? How to incorporate response time and other process data in CJ designs? How to balance desirability matching and latent attribute recovery?
3. What are the best strategies for structuring a data collection that exposes individual raters to repeated pairs and/or sets of pairs that can reveal intransitivity and instability, in order to assess the reliability of individual raters and distinguish variation within rater from variation across raters?
4. How do we best control for particular aspects of representations (e.g. length)? Can we factor these out of the CJ scores?
5. How does cognitive load affect pairwise comparisons? Is there a threshold in the amount of information being processed beyond which comparison becomes harder than absolute judgement? If so, how can it be approximated?
6. What's the best way of generalising from data on judgements made by a sample of judges to judgements made by a population of judges?
7. What makes a 'good' prompt for CJ sessions?
8. How do comparative judgement methods scale to large numbers of items or sparse comparison designs?
9. What potential wider applications of CJ should be a focus for research (e.g. peer review of funding applications, driver training, sentencing decisions, recruitment, resource prioritisation)?
10. How should we evaluate goodness-of-fit for comparative judgement models, and what diagnostics are most informative for people using them?
11. What is the optimal way to do pair selection for CJ?
12. Humans are often better at pairwise comparison than absolute scoring  is this still true when AI is the assessor?
13. What falsifiable claims about reality are embodied in the set of CJ scores that a set of objects receives post-Bradley-Terry analysis? How can/should these claims be tested and falsified?
14. Reliability = consensus? Researchers sometimes use reliability measures (SSR/SHR) as an indicator of consensus between the judges about some construct. Is this a valid inference?
15. How can we measure and account for heterogeneity among judges in comparative judgement?
16. How can we assess and improve the external validity of comparative judgment tasks, i.e., the degree to which the CJ task elicits the preferences/beliefs that drive judges' behaviour/choices in other contexts?
17. When overall inter-rater reliability is low but higher reliability is observed within subsets of judges, what latent factors explain this pattern in collected pairwise judgements? Additionally, can we statistically identify these subsets of agreement, rather than through manual inspection?
18. How do we tell the difference between judges who are providing no information versus judges who have a different opinion to the rest of the group?
19. What does crowdsourcing reveal about the behaviour of comparative judgement as the number of judges increases, particularly regarding convergence with expert-panel outcomes and the distinctive role of experts?
20. How can the near-unlimited capacity/throughput of AI be harnessed? What might LLM training/fine-tuning be able to offer? Will results be well-adapted to CJ or to specific subject material? How can this be done in a framework which allows understanding of how various flavours of AI compare to each other and to human/expert judgement?

