---
id: moodle-plugin-technical
title: Moodle Plugin Technical Information
---

Technical information about the [Moodle Comparative Judgement plugin](https://marketplace.moodle.com/plugins/assignsubmission_comparativejudgement), including how to install it, will be added here.

## Pair selection

The pairs are generated on the fly as each user requests to do a judgement. The criteria for prioritising the next pair a user sees are, in order:

1. the number of times the user has seen this exact pair
2. the number of times anyone has seen this exact pair
3. the number of times the user has seen either, and then each, of the submissions
4. the number of times anyone has seen either, and then each, of the submissions
5. a random factor (when the plugin's automated tests are running, submission user IDs are used instead so the results are repeatable)

[Back to the Moodle Plugin page](/resources/moodle-plugin/)
