---
id: mp-guide-troubleshooting
title: Troubleshooting
---

{% include moodle-guide-draft.html %}

## The Do comparison button is missing

The **Do comparison** button only appears when all of the following are true:

- the comparative judgement assignment has been set up and is not hidden
- there are at least 2 exemplars or submissions uploaded, not including the judge's own work
- the number of comparisons required is greater than 0 (see [Submission types and comparisons](/resources/moodle-plugin/user-guide/settings/submission-types.html))
- the judge has a role that was given judging rights (see [Judging settings](/resources/moodle-plugin/user-guide/settings/judging.html))
- the start date for comparisons has been left blank, or has passed
- either you have checked the box "**Allow judge to make comparisons while their submission is editable**" (in the **Submission types** settings), or the submission is no longer editable
  - the submission will no longer be editable if the submission and cut off deadlines have passed or if you selected "Yes" in the **Submission settings** against the option **Require students to click the submit button**

If you still cannot see the button after exemplars or submissions have been uploaded, try selecting all roles in the **Judges** box and try again.

When testing in student mode, check in the settings which user groups you have given permission to judge, and what date judging is scheduled to start.

See also [Do comparison](/resources/moodle-plugin/user-guide/managing/do-comparison.html).

{% include moodle-guide-nav.html %}
