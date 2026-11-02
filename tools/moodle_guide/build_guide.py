"""Build the Moodle plugin user guide pages from the Word draft.

Usage:
    python3 tools/moodle_guide/build_guide.py path/to/CJ_Guide.docx

Pages are matched to the Word document by its headings (see PAGES below), so
a re-edited draft can be rebuilt with the same command as long as the headings
keep their names. Every page under docs/resources/moodle-plugin/user-guide/
is regenerated, so edit the Word document rather than the generated pages.
"""
import json
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GUIDE = REPO / 'docs/resources/moodle-plugin/user-guide'
GUIDE_URL = '/resources/moodle-plugin/user-guide'
IMAGES = REPO / 'docs/images/moodle-plugin/user-guide'
IMAGES_URL = '/images/moodle-plugin/user-guide'
NAV_DATA = REPO / 'docs/_data/moodle_guide.yml'

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def w(tag):
    return '{%s}%s' % (W, tag)


# Screenshots get readable file names and alt text. Images not listed here
# (or mapped to None) are decorative arrows or review notes and are dropped.
IMAGE_NAMES = {
    'image1.png': ('assignment-buttons-with-do-comparison', 'The assignment page showing the Do comparison and management buttons'),
    'image2.png': ('assignment-buttons', 'The assignment page showing the management buttons'),
    'image3.png': None,
    'image4.png': ('grading-screenshot-1', 'Grading screenshot'),
    'image5.png': ('grading-screenshot-2', 'Grading screenshot'),
    'image6.png': ('student-add-submission', 'The student view with the Add submission button'),
    'image7.png': ('student-edit-remove-submission', 'The student view with buttons to edit or remove a submission'),
    'image8.png': ('student-do-comparison-button', 'The student view with the Do comparison button'),
    'image9.png': ('judging-instructions', 'Judging instructions shown at the top of the comparison page'),
    'image10.png': ('judging-pair', 'A pair of items to judge'),
    'image11.png': ('comment-boxes', 'Comment boxes and the Choose A / Choose B buttons'),
    'image12.png': ('next-pair', 'The next pair of items to judge'),
    'image13.png': ('edit-mode-add-content', 'Edit mode switched on, with the Add content menu open'),
    'image14.png': None,
    'image15.png': ('add-assignment', 'Choosing Assignment from the activity chooser'),
    'image16.png': ('icon-handwritten-work', 'Handwritten work'),
    'image17.png': ('icon-students-in-pairs', 'Students worked in pairs'),
    'image18.png': ('icon-formative', 'Formative assessment'),
    'image19.png': ('settings-name-description', 'Assignment name and description settings'),
    'image20.png': ('settings-activity-instructions', 'Activity instructions settings'),
    'image21.png': ('formative-availability', 'Availability settings for the formative example'),
    'image22.png': ('formative-submission-types', 'Submission type settings for the formative example'),
    'image23.png': ('formative-judging', 'Judging settings for the formative example'),
    'image24.png': ('settings-judges', 'Choosing which roles can judge'),
    'image25.png': ('settings-files', 'File settings'),
    'image26.png': ('settings-save', 'Saving the assignment settings'),
    'image27.png': ('hide-assignment', 'The assignment on the module page, with the menu to hide it'),
    'image28.png': ('manage-exemplars-tab', 'The Manage exemplars button'),
    'image29.png': ('add-exemplar-button', 'The Add exemplar button'),
    'image30.png': ('upload-exemplar', 'Uploading an exemplar'),
    'image31.png': ('exemplar-list', 'The list of uploaded exemplars'),
    'image32.png': ('test-student-view', 'Testing the assignment in the student view'),
    'image33.png': ('test-both-buttons', 'The Do comparison and Add submission buttons shown together while testing'),
    'image34.png': ('add-submission-upload', 'Uploading a submission'),
    'image35.png': ('icon-students-alone', 'Students worked alone'),
    'image36.png': ('icon-summative', 'Summative assessment'),
    'image37.png': ('summative-availability', 'Availability settings for the summative example'),
    'image38.png': ('summative-submission-types', 'Submission type settings for the summative example'),
    'image39.png': ('summative-judging', 'Judging settings for the summative example'),
    'image40.png': None,
    'image41.png': None,
}
ICONS = {'image16.png', 'image17.png', 'image18.png', 'image35.png', 'image36.png'}

# Each page: path, id, title, then the Word sections it is built from.
# Section keys are Heading 1 / Heading 2 texts, lower-cased with numbering
# removed; 'intro' is everything before the first heading. A section listed as
# ('key', False) keeps its body but not its heading.
PAGES = [
    ('getting-started.md', 'mp-guide-getting-started', 'Getting started', [('setting up a cj assignment in moodle', False)]),
    ('settings/index.md', 'mp-guide-settings', 'Assignment settings', []),
    ('settings/availability.md', 'mp-guide-availability', 'Availability settings', [('availability', False)]),
    ('settings/submission-types.md', 'mp-guide-submission-types', 'Submission types and comparisons', [('submission types', False, 'types')]),
    ('settings/judging.md', 'mp-guide-judging', 'Judging settings', [('submission types', False, 'judging')]),
    ('settings/files.md', 'mp-guide-files', 'File settings', [('submission types', False, 'files')]),
    ('settings/grade.md', 'mp-guide-grade', 'Grade settings', [('grade', False)]),
    ('settings/other-moodle-settings.md', 'mp-guide-other-settings', 'Other Moodle assignment settings',
     ['feedback types', 'submission settings', 'group submission settings', 'notifications']),
    ('managing/index.md', 'mp-guide-managing', 'Managing the assignment', [('managing the cj assignment', False)]),
    ('managing/exemplars.md', 'mp-guide-exemplars', 'Manage exemplars', [('manage exemplars', False)]),
    ('managing/do-comparison.md', 'mp-guide-do-comparison', 'Do comparison', [('do comparison', False)]),
    ('managing/judges.md', 'mp-guide-judges', 'Manage judges', [('manage judges', False)]),
    ('managing/comparison-comments.md', 'mp-guide-comments', 'Comparison comments', [('comparison comments', False)]),
    ('managing/submissions.md', 'mp-guide-submissions', 'Manage submissions', [('manage submissions', False)]),
    ('managing/comparisons.md', 'mp-guide-comparisons', 'Manage comparisons', [('manage comparisons', False)]),
    ('managing/reminder-emails.md', 'mp-guide-reminder-emails', 'Manage comparison request emails', [('manage comparison request emails', False)]),
    ('grading.md', 'mp-guide-grading', 'Grading and judgement data', [('grading and judgement data', False)]),
    ('student-view.md', 'mp-guide-student-view', 'The student perspective', [('the student perspective', False), 'what they will see']),
    ('worked-examples/index.md', 'mp-guide-worked-examples', 'Worked examples', [('worked examples', False), 'initial steps']),
    ('worked-examples/formative.md', 'mp-guide-formative', 'Worked example: formative use', [('formative use', False)]),
    ('worked-examples/summative.md', 'mp-guide-summative', 'Worked example: summative use', [('summative use', False)]),
    ('troubleshooting.md', 'mp-guide-troubleshooting', 'Troubleshooting', []),
    ('videos.md', 'mp-guide-videos', 'Videos', []),
]

# The Submission Types section holds four tables; these intro sentences mark
# where each of its pages starts.
SUBMISSION_SPLITS = [
    ('types', None),
    ('judging', 'Next you will have options regarding who judges'),
    ('files', 'Next you will have options regarding the items uploaded'),
]

# Cross-references in the Word text that become links on the web.
CROSS_REFS = [
    ('(see Settings above)', f'(see [Submission types and comparisons]({GUIDE_URL}/settings/submission-types.html))'),
    ('in the Settings', f'in the [judging settings]({GUIDE_URL}/settings/judging.html)'),
    ('settings (see Section 1)', f'settings (see [Submission types and comparisons]({GUIDE_URL}/settings/submission-types.html))'),
    ('(see Section 1)', f'(see [Submission types and comparisons]({GUIDE_URL}/settings/submission-types.html))'),
    ('see Column headings subsection below', 'see the table below'),
    ('see Grades and judgement data subsection', f'see [Grading and judgement data]({GUIDE_URL}/grading.html)'),
    ('(see Calculate scores below)', f'(see [Calculate scores]({GUIDE_URL}/grading.html))'),
    ('Core settings are included in Section 1 of this document.', f'Core settings are covered in [Assignment settings]({GUIDE_URL}/settings/).'),
    ('see the Formative Use worked example', f'see the [formative worked example]({GUIDE_URL}/worked-examples/formative.html)'),
    ('see this user guide.', 'see this user guide. **[To do: add link]**'),
    ('Next you will have options regarding who judges and when:', 'In the same part of the settings there are options for who judges and when:'),
    ('Next you will have options regarding the items uploaded for judgement:', 'In the same part of the settings there are options for the items uploaded for judgement:'),
]
PLACEHOLDERS = {
    'Add text here to explain this screenshot': '> **To do:** add text to explain this screenshot.',
    '**xx:** *xx.*': '> **To do:** placeholder note ("xx: xx") to be written.',
    'This section is still being edited and finalised': '> **To do:** this section is still being edited and finalised.',
}


# ---------------------------------------------------------------- docx reading

def read_docx(path, workdir):
    with zipfile.ZipFile(path) as z:
        z.extractall(workdir)
    d = Path(workdir)
    rels = {r.get('Id'): r.get('Target') for r in ET.parse(d / 'word/_rels/document.xml.rels').getroot()}
    numfmt = {}
    numbering = d / 'word/numbering.xml'
    if numbering.exists():
        root = ET.parse(numbering).getroot()
        abstract = {}
        for an in root.findall(w('abstractNum')):
            abstract[an.get(w('abstractNumId'))] = {
                lvl.get(w('ilvl')): (lvl.find(w('numFmt')).get(w('val')) if lvl.find(w('numFmt')) is not None else 'bullet')
                for lvl in an.findall(w('lvl'))}
        for n in root.findall(w('num')):
            numfmt[n.get(w('numId'))] = abstract.get(n.find(w('abstractNumId')).get(w('val')), {})

    def inline(el):
        """Paragraph text as Markdown; same-format runs are merged first."""
        segs = []

        def walk(node, href=None):
            for c in node:
                if c.tag in (w('del'), w('moveFrom')):
                    continue
                if c.tag == w('hyperlink'):
                    rid = c.get('{%s}id' % R)
                    walk(c, rels.get(rid) if rid else None)
                elif c.tag == w('r'):
                    rpr = c.find(w('rPr'))

                    def on(t):
                        e = rpr.find(w(t)) if rpr is not None else None
                        return e is not None and e.get(w('val')) not in ('0', 'false')
                    b, i = on('b'), on('i')
                    for x in c.iter():
                        if x.tag == w('t'):
                            segs.append([x.text or '', b, i, href])
                        elif x.tag == w('tab'):
                            segs.append([' ', b, i, href])
                        elif x.tag == w('br'):
                            segs.append(['\n', False, False, None])
                        elif x.tag == '{%s}blip' % A:
                            segs.append(('IMG', Path(rels[x.get('{%s}embed' % R)]).name))
                elif c.tag in (w('ins'), w('smartTag'), w('sdt'), w('sdtContent'), w('fldSimple'), w('moveTo')):
                    walk(c, href)
        walk(el)

        merged = []
        for sg in segs:
            if (merged and sg[0] != 'IMG' and merged[-1][0] != 'IMG'
                    and (merged[-1][1:] == sg[1:] or (not sg[0].strip() and merged[-1][3] == sg[3]))):
                merged[-1][0] += sg[0]
            else:
                merged.append(list(sg) if sg[0] != 'IMG' else sg)

        out, images, k = [], [], 0
        while k < len(merged):
            sg = merged[k]
            if sg[0] == 'IMG':
                images.append(sg[1])
                k += 1
                continue
            href = sg[3]
            if href:
                group = []
                while k < len(merged) and merged[k][0] != 'IMG' and merged[k][3] == href:
                    group.append(merged[k][0])
                    k += 1
                text = ''.join(group).strip()
                href = re.sub(r'[?&]_gl=.*$', '', href)
                out.append(f' <{text}> ' if text.startswith('http') else f' [{text}]({href}) ')
                continue
            t, b, i, _ = sg
            core = t.strip()
            if core:
                lead, trail = t[:len(t) - len(t.lstrip())], t[len(t.rstrip()):]
                if b or i:
                    # Keep stray punctuation outside the emphasis markers.
                    m = re.match(r'^([.,;:]*)\s*(.*?)$', core)
                    punct, core = m.group(1), m.group(2)
                    lead = punct + (' ' if punct else '') + lead
                core = f'**{core}**' if b and core else f'*{core}*' if i and core else core
                t = lead + core + trail
            out.append(t)
            k += 1
        text = re.sub(r'[  ]{2,}', ' ', ''.join(out)).strip()
        text = re.sub(r' ([.,;:])(?=\s|$)', r'\1', text.replace('. .', '.'))
        return text, images

    def para(p):
        ppr = p.find(w('pPr'))
        style, lst = '', None
        if ppr is not None:
            st = ppr.find(w('pStyle'))
            style = st.get(w('val')) if st is not None else ''
            np_ = ppr.find(w('numPr'))
            if np_ is not None and np_.find(w('numId')) is not None:
                nid = np_.find(w('numId')).get(w('val'))
                lvl = np_.find(w('ilvl')).get(w('val')) if np_.find(w('ilvl')) is not None else '0'
                if nid != '0':
                    lst = (numfmt.get(nid, {}).get(lvl, 'bullet'), int(lvl))
        text, images = inline(p)
        return {'k': 'p', 'style': style, 'list': lst, 'text': text, 'images': images}

    blocks = []
    body = ET.parse(d / 'word/document.xml').getroot().find(w('body'))
    for el in body:
        if el.tag == w('p'):
            blocks.append(para(el))
        elif el.tag == w('tbl'):
            rows = []
            for tr in el.findall(w('tr')):
                cells = []
                for tc in tr.findall(w('tc')):
                    parts = [para(p)['text'] for p in tc.iter(w('p'))]
                    cells.append('<br>'.join(x for x in parts if x))
                rows.append(cells)
            blocks.append({'k': 'tbl', 'rows': rows})
    return d, blocks


def section_key(text):
    text = re.sub(r'^\d+\)\s*', '', text.strip())
    return re.sub(r'\s+', ' ', text).lower()


def split_sections(blocks):
    """Group blocks under their Heading 1 / Heading 2, keyed by heading text."""
    sections = {'intro': []}
    current = 'intro'
    for b in blocks:
        if b['k'] == 'p' and b['style'] in ('Heading1', 'Heading2') and b['text']:
            current = section_key(b['text'])
            sections[current] = []
            continue
        if b['k'] == 'p' and b['style'] in ('Heading1', 'Heading2', 'Title', 'TOC1', 'TOC2'):
            continue
        sections[current].append(b)
    return sections


# ------------------------------------------------------------------ rendering

used_images = set()


def image_md(name, indent=''):
    info = IMAGE_NAMES.get(name, (Path(name).stem, 'Screenshot'))
    if info is None:
        return None
    used_images.add(name)
    slug, alt = info
    if name in ICONS:
        return f'{indent}<img src="{IMAGES_URL}/{slug}.png" alt="{alt}" width="140" />'
    return f'{indent}![{alt}]({IMAGES_URL}/{slug}.png)'


def table_md(rows):
    def clean(c):
        return c.replace('|', '\\|').strip()
    head = [re.sub(r'\*\*\s*\*\*', ' ', clean(c)).replace('**', '') for c in rows[0]]
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in rows[1:]:
        lines.append('| ' + ' | '.join(clean(c) for c in r) + ' |')
    return '\n'.join(lines)


def note_md(text):
    """One-cell tables in the draft are user notes; render them as callouts."""
    if text in PLACEHOLDERS:
        return PLACEHOLDERS[text]
    m = re.match(r'\*\*User [Nn]ote:\*\*\s*(.*)', text, re.S)
    if m:
        body = m.group(1).replace('**', '\u0000').replace('*', '').replace('\u0000', '**').strip()
        body = body[0].upper() + body[1:]
        return f'> **Note:** {body}'
    return f'> {text}'


def render(blocks):
    out = []
    in_steps = False  # inside a numbered list: indent follow-on content
    pending_icons = []

    def flush_icons():
        if pending_icons:
            out.append(' '.join(pending_icons))
            pending_icons.clear()

    for b in blocks:
        if b['k'] == 'tbl':
            flush_icons()
            if len(b['rows']) == 1 and len(b['rows'][0]) == 1:
                md = note_md(b['rows'][0][0])
                out.append(('   ' + md.replace('\n', '\n   ')) if in_steps else md)
            else:
                out.append(table_md(b['rows']))
            continue
        text, lst = b['text'], b['list']
        for name in b['images']:
            if name in ICONS:
                pending_icons.append(image_md(name))
        if text in PLACEHOLDERS:
            out.append(PLACEHOLDERS[text])
            continue
        if text.startswith('// '):
            out.append('```\n' + text + '\n```')
            continue
        if text:
            flush_icons()
            if lst and lst[0] == 'decimal':
                in_steps = True
                out.append(f'1. {text}')
            elif lst and in_steps:
                out.append(f'   - {text}')
            elif lst and lst[1] > 0:
                out.append(f'   - {text}')
            elif lst:
                out.append(f'- {text}')
            else:
                out.append(('   ' if in_steps else '') + text)
        for name in b['images']:
            if name not in ICONS:
                md = image_md(name, '   ' if in_steps else '')
                if md:
                    out.append(md)
    flush_icons()

    # Join with blank lines, but keep runs of bullet items tight.
    def indent(line):
        return len(line) - len(line.lstrip())
    md = ''
    for i, line in enumerate(out):
        if i and re.match(r'\s*- ', line) and re.match(r'\s*- ', out[i - 1]) and indent(line) == indent(out[i - 1]):
            md += '\n' + line
        else:
            md += ('\n\n' if md else '') + line
    for old, new in CROSS_REFS:
        md = md.replace(old, new)
    return md


def submission_part(blocks, part):
    starts = []
    for name, marker in SUBMISSION_SPLITS:
        idx = 0 if marker is None else next(i for i, b in enumerate(blocks) if b['k'] == 'p' and b['text'].startswith(marker))
        starts.append((name, idx))
    for n, (name, idx) in enumerate(starts):
        if name == part:
            end = starts[n + 1][1] if n + 1 < len(starts) else len(blocks)
            return blocks[idx:end]
    raise KeyError(part)


# --------------------------------------------------------- hand-written pages

def page_intro(rel):
    """Short linking text for pages that are not taken straight from the draft."""
    u = GUIDE_URL
    if rel == 'settings/index.md':
        return f"""A comparative judgement assignment is a standard Moodle assignment with the Comparative judgement submission type switched on. These pages go through the settings you will need to consider.

## Comparative judgement settings

- [Availability]({u}/settings/availability.html): when students can submit work to be judged
- [Submission types and comparisons]({u}/settings/submission-types.html): switching on comparative judgement and setting how many comparisons are needed
- [Judging]({u}/settings/judging.html): who judges, when judging starts and the instructions judges see
- [Files]({u}/settings/files.html): the number, size and type of files students upload
- [Grade]({u}/settings/grade.html): how grades are recorded

## Standard Moodle settings

- [Other Moodle assignment settings]({u}/settings/other-moodle-settings.html): feedback, submission, group and notification settings, which work the same as in any Moodle assignment

> **To do:** add a summary table of recommended settings for formative and summative use."""
    if rel == 'troubleshooting.md':
        return f"""## The Do comparison button is missing

The **Do comparison** button only appears when all of the following are true:

- the comparative judgement assignment has been set up and is not hidden
- there are at least 2 exemplars or submissions uploaded, not including the judge's own work
- the number of comparisons required is greater than 0 (see [Submission types and comparisons]({u}/settings/submission-types.html))
- the judge has a role that was given judging rights (see [Judging settings]({u}/settings/judging.html))
- the start date for comparisons has been left blank, or has passed

If you still cannot see the button after exemplars or submissions have been uploaded, try selecting all roles in the **Judges** box and try again.

When testing in student mode, check in the settings which user groups you have given permission to judge, and what date judging is scheduled to start.

See also [Do comparison]({u}/managing/do-comparison.html)."""
    if rel == 'videos.md':
        return """Short how-to videos for the plugin will be listed here. Each video will also appear on the page of the guide that covers the same task.

> **To do:** add videos as they are recorded."""
    return ''


def page_outro(rel):
    """Links to sub-pages, added after the draft text on section index pages."""
    u = GUIDE_URL
    if rel == 'managing/index.md':
        return f"""The buttons are covered on these pages:

- [Do comparison]({u}/managing/do-comparison.html)
- [Manage exemplars]({u}/managing/exemplars.html)
- [Manage judges]({u}/managing/judges.html)
- [Comparison comments]({u}/managing/comparison-comments.html)
- [Manage submissions]({u}/managing/submissions.html)
- [Manage comparisons]({u}/managing/comparisons.html)
- [Manage comparison request emails]({u}/managing/reminder-emails.html)"""
    if rel == 'worked-examples/index.md':
        return f"""## The examples

- [Formative use]({u}/worked-examples/formative.html): students worked in pairs on a learning activity
- [Summative use]({u}/worked-examples/summative.html): students worked alone on a graded assessment"""
    return ''


def guide_index(sections):
    u = GUIDE_URL
    intro = sections.get('intro', [])
    first = next((b['text'] for b in intro if b['k'] == 'p' and b['text'] and not b['text'].startswith('**')), '')
    return f"""{first}

## Contents

- [Getting started]({u}/getting-started.html): creating a comparative judgement assignment in Moodle
- [Assignment settings]({u}/settings/): availability, submission types, judging, files, grade and other Moodle settings
- [Managing the assignment]({u}/managing/): exemplars, doing comparisons, and managing judges, submissions, comparisons and reminder emails
- [Grading and judgement data]({u}/grading.html): calculating scores, downloading data and copying grades to the gradebook
- [The student perspective]({u}/student-view.html): preparing students and what they will see
- [Worked examples]({u}/worked-examples/): formative and summative examples from a Foundation Maths course
- [Troubleshooting]({u}/troubleshooting.html)
- [Videos]({u}/videos.html)

Technical details, including how pairs are selected, are on the [technical information](/resources/moodle-plugin/technical.html) page."""


# ------------------------------------------------------------------ building

def write_page(rel, page_id, title, body):
    path = GUIDE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'---\nid: {page_id}\ntitle: {title}\n---\n\n'
        '{% include moodle-guide-draft.html %}\n\n'
        f'{body.strip()}\n\n'
        '{% include moodle-guide-nav.html %}\n')


def page_url(rel):
    rel = rel[:-len('index.md')] if rel.endswith('index.md') else rel[:-3] + '.html'
    return f'{GUIDE_URL}/{rel}'


def main(docx):
    with tempfile.TemporaryDirectory() as tmp:
        d, blocks = read_docx(docx, tmp)
        sections = split_sections(blocks)

        if GUIDE.exists():
            shutil.rmtree(GUIDE)
        if IMAGES.exists():
            shutil.rmtree(IMAGES)
        GUIDE.mkdir(parents=True)

        write_page('index.md', 'moodle-plugin-user-guide', 'Moodle Plugin User Guide', guide_index(sections))
        for rel, page_id, title, parts in PAGES:
            chunks = [page_intro(rel)]
            for part in parts:
                key, keep_heading, sub = (part, True, None) if isinstance(part, str) else (part + (None,))[:3]
                body = sections[key]
                if sub:
                    body = submission_part(body, sub)
                md = render(body)
                if keep_heading:
                    md = f'## {key[0].upper()}{key[1:]}\n\n{md}'
                chunks.append(md)
            chunks.append(page_outro(rel))
            write_page(rel, page_id, title, '\n\n'.join(c for c in chunks if c))

        IMAGES.mkdir(parents=True)
        for name in sorted(used_images):
            shutil.copy(d / 'word/media' / name, IMAGES / f'{IMAGE_NAMES[name][0]}.png')

    nav = [('Contents', f'{GUIDE_URL}/')] + [(t, page_url(r)) for r, _, t, _ in PAGES]
    NAV_DATA.parent.mkdir(parents=True, exist_ok=True)
    NAV_DATA.write_text('# Page order for the Moodle plugin user guide (generated by tools/moodle_guide/build_guide.py)\n'
                        + ''.join(f'- title: {json.dumps(t)}\n  url: {u}\n' for t, u in nav))
    print(f'Wrote {len(PAGES) + 1} pages and {len(used_images)} images')


if __name__ == '__main__':
    main(sys.argv[1])
