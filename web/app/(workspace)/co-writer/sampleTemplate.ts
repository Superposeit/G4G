const FENCE = "```";

export const CO_WRITER_SAMPLE_TEMPLATE = `# EducaT TutorRD Co-Writer

> EducaT TutorRD's built-in writing canvas for notes, reports, tutorials, and AI-assisted drafts.

### Features

- Support Standard Markdown / CommonMark / GFM for everyday writing
- Real-time preview for headings, tables, code, math, flowchart, and sequence diagrams
- AI editing workflows for rewrite, shorten, and expand
- HTML tag decoding for tags like <sub>, <sup>, <abbr>, and <mark>
- A practical starter draft for EducaT TutorRD product docs and learning content

## Table of Contents

[TOCM]

[TOC]

#EducaT TutorRD Mission
##EducaT TutorRD Product Surface
###EducaT TutorRD Learning Experience
####EducaT TutorRD Co-Writer
#####EducaT TutorRD Knowledge Layer
######EducaT TutorRD Agent Runtime

#EducaT TutorRD Docs [Project Overview](#educat-tutorrd-mission "Jump to project overview")
##EducaT TutorRD Authoring [Co-Writer Section](#educat-tutorrd-co-writer "Jump to co-writer section")
###EducaT TutorRD Research [Learning Note](#educat-tutorrd-learning-note "Jump to learning note")

## Headers (Underline)

EducaT TutorRD Learning Note
=============

EducaT TutorRD Study Outline
-------------

### Characters

----

~~Deprecated behavior~~ <s>Legacy formatting path</s>
*Italic* _Italic_
**Emphasis** __Emphasis__
***Emphasis Italic*** ___Emphasis Italic___

Superscript: X<sub>2</sub>, Subscript: O<sup>2</sup>

**Abbreviation(link HTML abbr tag)**

The <abbr title="Large Language Model">LLM</abbr> layer powers EducaT TutorRD while the <abbr title="Retrieval Augmented Generation">RAG</abbr> layer provides grounded knowledge support.

### Blockquotes

> EducaT TutorRD helps students turn questions into structured understanding.
>
> "Learn deeply, write clearly.", [EducaT TutorRD](#educat-tutorrd-co-writer)

### Links

[EducaT TutorRD Overview](#educat-tutorrd-mission)

[EducaT TutorRD Co-Writer](#educat-tutorrd-co-writer "co-writer section")

[EducaT TutorRD Runtime](#educat-tutorrd-agent-runtime)

[Reference link][educat-doc]

[educat-doc]: #educat-tutorrd-learning-note

### Code Blocks

#### Inline code

\`deeptutor chat --once "Summarize this section"\`

#### Code Blocks (Indented style)

    from deeptutor.runtime.orchestrator import ChatOrchestrator
    orchestrator = ChatOrchestrator()
    print("EducaT TutorRD is ready.")

#### Python

${FENCE}python
from deeptutor.runtime.orchestrator import ChatOrchestrator
from deeptutor.core.context import UnifiedContext


async def run_demo() -> str:
    orchestrator = ChatOrchestrator()
    context = UnifiedContext(
        user_query="Explain Newton's second law",
        capability="chat",
    )
    result = await orchestrator.run(context)
    return result.get("response", "")
${FENCE}

#### JSON config

${FENCE}json
{
  "app_name": "EducaT TutorRD",
  "default_capability": "chat",
  "enabled_tools": ["rag", "web_search", "code_execution", "reason"],
  "ui": {
    "co_writer_template": true
  }
}
${FENCE}

#### HTML code

${FENCE}html
<section class="educat-tutorrd-card">
  <h1>EducaT TutorRD</h1>
  <p>Write, revise, and organize learning content with AI.</p>
</section>
${FENCE}

### Images

![](/educat-tutorrd-logo-v3.svg)

> EducaT TutorRD brand mark used inside the co-writer template.

### Lists

- EducaT TutorRD Chat
- EducaT TutorRD Co-Writer
- EducaT TutorRD Research

1. Draft a concept note
2. Ask AI to refine it
3. Export the polished markdown

### Tables

Feature       | Description
------------- | -------------
Co-Writer     | Draft and refine Markdown content
Chat          | Ask questions and iterate ideas
Research      | Build structured multi-step reports

| Capability    | Primary Use Case                     |
| ------------- | ------------------------------------ |
| \`chat\`       | General tutoring and guidance        |
| \`deep_solve\` | Structured problem solving           |
| \`deep_question\` | Question generation and validation |

### Markdown extras

- [x] Draft an EducaT TutorRD product note
- [x] Add references and structure
- [ ] Polish the final explanation
  - [ ] Check headings
  - [ ] Check citations

### TeX (LaTeX)

$$ E=mc^2 $$

Inline $$E=mc^2$$ appears in physics notes, and Inline $$a^2+b^2=c^2$$ appears in geometry notes.

$$\(\sqrt{3x-1}+(1+x)^2\)$$

$$ \sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$

### FlowChart

${FENCE}flow
st=>start: Student asks a question
op=>operation: EducaT TutorRD analyzes intent
cond=>condition: Need deep workflow?
chat=>operation: Answer with chat capability
solve=>operation: Route to deep solve
e=>end: Return structured response

st->op->cond
cond(no)->chat
cond(yes)->solve
chat->e
solve->e
${FENCE}

### Sequence Diagram

${FENCE}seq
Student->EducaT TutorRD: Ask for help
EducaT TutorRD->KnowledgeBase: Load context
Note right of EducaT TutorRD: Collect memory\nand relevant knowledge
EducaT TutorRD-->Student: Return guided response
Student->>EducaT TutorRD: Request rewrite in co-writer
${FENCE}

### End
`;
