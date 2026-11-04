---
id: mp-guide-summative
title: Worked example - summative use
---

{% include moodle-guide-draft.html %}

<img src="/images/moodle-plugin/user-guide/icon-handwritten-work.png" alt="Handwritten work" width="140" /> <img src="/images/moodle-plugin/user-guide/icon-students-alone.png" alt="Students worked alone" width="140" /> <img src="/images/moodle-plugin/user-guide/icon-summative.png" alt="Summative assessment" width="140" />

As we repeated a formative assessment (from a choice of three) as a summative assessment, much of the assignment setup shown here is very similar to the formative example, but with a few key differences around when students can judge, how many judgements they must do and why we might include some exemplar submissions. 

1. Give your assignment a title and describe what is expected overall.

   ![Assignment name and description settings](/images/moodle-plugin/user-guide/settings-name-description.png)

1. Give instructions on creating the items to be judged. There is also the option to upload additional files such as reference materials, but in this case we have not.

   ![Activity instructions settings](/images/moodle-plugin/user-guide/settings-activity-instructions.png)

1. Set the dates during which the items to be judged must be created. We opened submissions for one hour only during class time so we could ensure the items were created in exam conditions. The cut off for submissions in this case is the same as the main deadline.

   ![Availability settings for the summative example](/images/moodle-plugin/user-guide/summative-availability.png)

1. Set your submission types and the number of comparisons required. **You must select comparative judgement**.

   ![Submission type settings for the summative example](/images/moodle-plugin/user-guide/summative-submission-types.png)

   - We have chosen file submissions as we want the students to upload jpegs of handwritten work.
   - We have allowed comparison of pairs of exemplars, as we want to seed some marked examples from the previous year to use as indicators of grade boundaries, and we want them to be treated the same as new items.
   - We have enabled repeat comparisons. This means the same items can be judged against each other more than once, however the way pairs are generated means repeats should be minimal.
   - We have set a minimum of 10 comparisons per judge. As we are using peer judging, there are as many judges as items, so a relatively small number of judgements per person is enough to create a valid and reliable set of scores. 10 comparisons approximates to each individual submission being judged 20 times.
   - We have also set the maximum number of judgements to 10 so that we know precisely how many judgements each student will make. For a summative assessment this is more important. After the students have completed all of their judgements, we then go back into the settings and adjust this number upwards to enable the teacher to do a greater number of judgements, equal at least to the class size. This gives confidence that the teacher has reviewed most of the work as an expert judge, while still being quicker than traditional rubric marking.
   - As this is graded work, we set a minimum number of 10 comparisons per submission. We should easily reach this as the students are comparing 20 items each (10 paired comparisons) and the teacher is also doing judgements
   - We have enabled comparison comments as that could provide some useful additional feedback for the students.

1. Set a start date for comparisons and write instructions for your judges.

   ![Judging settings for the summative example](/images/moodle-plugin/user-guide/summative-judging.png)

   - We wanted comparisons to be done in a specific class-based session, immediately after item submission closed, so we set a start date and time to reflect that.
   - As this is an assessment we want to prevent comparisons on submissions that are still editable.
   - For our judge intro we described the judgement criteria (choose the best description) and gave instructions regarding comments.

1. Choose who can judge. The options available will be set by your institution. Hold down the ctrl key to select multiple options.

   ![Choosing which roles can judge](/images/moodle-plugin/user-guide/settings-judges.png)

1. Select the number and type of files to be uploaded.

   ![File settings](/images/moodle-plugin/user-guide/settings-files.png)

   - We restricted to 1 file, max 10MB, which is the general recommendation for most comparative judgement submissions.
   - Ideally all students should use the same file type. We therefore chose to limit them to .jpeg / .jpg uploads.

1. Check standard institutional assignment settings then save and return to module. Core settings are covered in [Assignment settings](/resources/moodle-plugin/user-guide/settings/). Additional settings guidance can be found here: <https://docs.moodle.org/502/en/Assignment_settings>

   ![Saving the assignment settings](/images/moodle-plugin/user-guide/settings-save.png)

1. Click onto the assignment title. Note we hid the assignment from students while setting it up, which is an option when you click the 3 dots on the right-hand side.

   ![The assignment on the module page, with the menu to hide it](/images/moodle-plugin/user-guide/hide-assignment.png)

1. Add exemplars (if you are using them) by first clicking the ‘Manage Exemplars’ tab, then ‘Add Exemplar’

   ![The Manage exemplars button](/images/moodle-plugin/user-guide/manage-exemplars-tab.png)

   ![The Add exemplar button](/images/moodle-plugin/user-guide/add-exemplar-button.png)

1. Upload exemplars one at a time; this can be done via ‘drag and drop’. Give each a title that links to their filename as this will help you if you need do checks or make changes later. It is not currently possible to bulk upload.

   ![Uploading an exemplar](/images/moodle-plugin/user-guide/upload-exemplar.png)

1. Test what your students can see. We briefly made the assignment visible again on the module page and temporarily adjusted the assignment dates in the settings to make submission and judging live, so that they could be checked.

   ![Testing the assignment in the student view](/images/moodle-plugin/user-guide/test-student-view.png)

   As we altered all availability dates for test purposes, we can see both the **Do comparison** and **Add submission** buttons.

   ![The Do comparison and Add submission buttons shown together while testing](/images/moodle-plugin/user-guide/test-both-buttons.png)

   If the **Do comparison** button is missing when you test in student mode, check in the settings:

   - Which user groups have you given permission to judge?
   - What date is judging currently scheduled to start?

   In our case judging is delayed so the student will actually only see the **Add submission** button when they first open the assignment.

   ![The student view with the Add submission button](/images/moodle-plugin/user-guide/student-add-submission.png)

   If you click **Add submission**, you can then drag and drop a new file. Unlike exemplars, a title is not required.

   ![Uploading a submission](/images/moodle-plugin/user-guide/add-submission-upload.png)

   The option to edit the submission will only be available until the submission deadline.

   ![The student view with buttons to edit or remove a submission](/images/moodle-plugin/user-guide/student-edit-remove-submission.png)

   If you have made the judging live you will also see the Do comparison button.

   ![The student view with the Do comparison button](/images/moodle-plugin/user-guide/student-do-comparison-button.png)

   When run normally though, judging will only become available after the submission deadline, and editing will disappear at that point.

   > **Note:** For screenshots of paired items, see the [formative worked example](/resources/moodle-plugin/user-guide/worked-examples/formative.html).

   As this was a summative assessment, students completed their judging alone.

{% include moodle-guide-nav.html %}
