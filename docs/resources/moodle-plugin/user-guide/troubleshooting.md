---
id: mp-guide-troubleshooting
title: Troubleshooting
---

{% include moodle-guide-draft.html %}

## A student can't add a submission

The **Add submission** button only appears when all of the following are true:

- the comparative judgement assignment has been set up and is not hidden
- the **Allow submissions from** date and time has arrived
- if a **Cut-off date** has been set, it has not passed
- if it is a group assignment, then the student has been assigned to a group 


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


## Still stuck?

If you cannot solve a problem using this guide, there are two ways to get help.

**Report a technical issue on GitHub.** If you have a GitHub account, you can report bugs and other technical problems on the plugin's [GitHub issues page](https://github.com/ianjones/moodle-assignsubmission_comparativejudgement/issues). It is worth checking the existing issues first, in case someone has already reported the same problem.

**Email for advice.** If you do not use GitHub, or you would like advice on using the plugin, email [comparativejudgement@gmail.com](mailto:comparativejudgement@gmail.com).

Whichever you choose, it helps to include:

- what you were trying to do, what you expected to happen and what happened instead
- your Moodle version and the plugin version, if you know them
- the browser and device you were using
- a screenshot, with any student names or other personal information removed


{% include moodle-guide-nav.html %}
