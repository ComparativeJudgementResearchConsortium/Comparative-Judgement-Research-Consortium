---
id: mp-guide-grading
title: Grading and judgement data
---

{% include moodle-guide-draft.html %}

Three buttons appear at the bottom of the [Manage submissions](/resources/moodle-plugin/user-guide/managing/submissions.html) page once some judgements have been completed:

| Button | Explanation |
|---|---|
| **Calculate scores** | Uses the comparisons made so far to calculate a score for each exemplar or submission. It will also calculate a reliability figure that will be displayed just above the **Calculate scores** button. This reliability figure is what is known as [Scale Separation Reliability](https://journals.sagepub.com/doi/10.1177/0146621617748321) and should be greater than 0.7 before you can be confident in your scores. If this figure is lower than 0.7 then add more judgements. Usually 10 judgements per submission is more than adequate. |
| **Raw comparison data** | For advanced users, you can download the comparisons made and calculate your own scores offline. Guidance on processing comparative judgement decisions offline is coming soon on the CJRC website. |
| **Copy grades to gradebook** | Click once all comparisons are complete to copy the grades to the Moodle gradebook. |

Note that if you set the option to Enable comparison comments, there is an extra step to distribute the comments to students. On the “Comparison comments” page, press the button at the bottom of the table, Import comments. This copies across all comments received on a student's submission into the “Feedback comments” field.

## Student scores

Once you have clicked **Calculate scores**, the table on the Manage submissions page shows how each exemplar and submission fared in the comparisons.

![The Manage submissions table showing wins, losses and scores for each submission](/images/moodle-plugin/user-guide/grading-screenshot-1.png)

Each row is one exemplar or submission. Click **View** to see the work itself. The **Comparisons received** column tells you how many times the item has been judged, and **Time spent** and **Median time spent** show how long judges spent on the comparisons involving it. The **First comparison** and **Last comparison** dates show when it was first and most recently judged.

**Wins** is the number of times the item was chosen as the better of the pair, and **Losses** is the number of times the other item was chosen. For example, in the screenshot above, submission 4059735 won 26 of its 32 comparisons, while submission 4059729 won only 4 of its 34.

The **Score** is calculated from all the comparisons using a statistical model (the Bradley-Terry model). It is not simply the proportion of wins: the model also takes into account the strength of the items each one was compared against, so a win against strong work counts for more than a win against weak work. Scores are placed on a scale of 0 to 100, centred on around 65, with most scores falling between about 35 and 95. A higher score means the work was judged to be of higher quality. Click a column heading to sort the table, for example by **Score** to see the rank order of the work.

Untick **Include in grading** to exclude an exemplar or submission. All comparisons involving it are then left out the next time you click **Calculate scores**. Exemplars are never copied to the gradebook, even when they are included in grading.

## Grade boundaries

A common concern about comparative judgement is the assumption that grades must be normative rather than criterion-based; that is, that a student judged amongst a high-achieving cohort will get a lower score than if they were judged amongst a low-achieving cohort. In fact this concern is unwarranted. The scores from a comparative judgement exercise can be used for criterion-based grading just like a set of scores from traditional marking. To do this we anchor the scores to an external reference that serves as the grade boundaries. We offer three methods for doing so.

### Grade boundary exemplars at the moderation stage

Grading can be done at the moderation stage, after the students have completed their peer judgements. Before you start your moderating judgements, add an [exemplar](/resources/moodle-plugin/user-guide/managing/exemplars.html) for each grade boundary. For example, if students are to receive a grade between 1 and 5, you would add an exemplar that reads “Grade boundary 1/2”, another that reads “Grade boundary 2/3”, and so on.

When you do your moderating judgements, these grade boundary exemplars appear occasionally amongst the students' work. For each pair, decide whether the student's work is above or below that grade boundary.

![A comparison between a Grade boundary 3/4 exemplar and a student's submission](/images/moodle-plugin/user-guide/grade34comp.png)

The outcome is a rank order of the students' work with the grade boundaries fitted in between. Each student's grade is given by the boundaries their work falls between.

![A rank order of student work with grade boundary exemplars placed between the submissions](/images/moodle-plugin/user-guide/grade_rank_order.png)

### Grade boundary scripts

A related method can be used if you already have pieces of student work that represent the grade boundaries. These boundary scripts can be taken from previous cohorts, or identified by independently marking a handful of the current scripts. For example, in a [study of secondary statistics in New Zealand](https://doi.org/10.1007/s40841-020-00163-3), six boundary scripts published by the national qualifications authority to exemplify levels of achievement were added to the students' work. The comparative judgement process placed all six in the correct order, from lowest to highest grade.

Add the boundary scripts as [exemplars](/resources/moodle-plugin/user-guide/managing/exemplars.html). With this method the boundary scripts can be included before the students make their judgements, or added at the moderation stage. After you click **Calculate scores**, the position of the boundary scripts in the rank order shows where the grade boundaries fall.

![Scores in rank order, with the boundary scripts from a previous cohort highlighted](/images/moodle-plugin/user-guide/grading-screenshot-2.png)

### Breaks in the scores

Alternatively, you can create grade boundaries by scrutinising the scores arising from the comparative judgement. This method is described in a [study of secondary science](https://doi.org/10.1080/0969594X.2014.978839), in which teachers applied grade boundaries to the scaled rank order of their students' test responses.

1. Decide how many grades you need.
2. Sort the submissions by score and look at the rank order, ideally as a chart of scores like the one below. Look for natural breaks, where there is a noticeable jump in score between neighbouring pieces of work.
3. Starting at one end of the scale, propose a boundary at a break.
4. Read the work either side of the proposed boundary and adjust the boundary up or down by one or two pieces of work if needed.
5. Repeat for each of the remaining boundaries.

![Scores in rank order with grade boundaries drawn at breaks in the scores](/images/moodle-plugin/user-guide/grade_scale_breaks.png)

Once the boundaries are agreed, you can also write a short description of the work within each grade, drawing on the work itself. In the science study these level descriptors were given to students along with their grade.

{% include moodle-guide-nav.html %}
