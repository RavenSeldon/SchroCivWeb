# Back-Translation Review of the Localized Tale Pages

The eight localized Tale landing pages (`src/content/tale-locales.json`) were written by Claude, an AI, from the site's own English wording. No native speaker has read them.

As a substitute check, two further model instances were given the eight locales **cold** — the text only, no English source, no explanation of what it was for — and asked to back-translate every field literally and flag anything a native reader would mark. The point of withholding the English is that a reviewer who knows the intended meaning tends to read it back into the text.

**This document is the first pass's report, and it describes the text as it stood before correction.** Where it flags something, that something has since been changed; the report is kept unedited as the record of what was found.

## Corrections applied on 2026-10-05

From the first pass:

| Locale | Field | Was | Now |
| --- | --- | --- | --- |
| de | title, h1 | Mit Mühe zu den Sternen ("barely making it to the stars") | Durch Mühsal zu den Sternen |
| de | p2 | die öffentlich dokumentierte Faktenlage ("the publicly documented facts") | die öffentlich zugänglichen Unterlagen |
| zh-Hans | p4 | "人类" ("humankind") glossed as 人类操作者 | "人" |
| ru | p2 | то есть в 8,4 % (dangling "that is, in 8.4%") | что составляет 8,4 % |
| ru | p3 | обращает ту же проверку на… (calque) | применяет ту же проверку к… |
| fr, es, pt, de, ru | p6 | the downloads called articles / essays / papers, colliding with the 24 press articles named in p2 | one research-paper term per language |
| pt | p2 | 8,4% | 8,4 % |
| fr | lede | comma before *et* | removed |
| zh-Hans | description | 顿号 (、) joining a quantity to a predicate | ，|

From the second pass, which read only the sentences the first pass had changed:

| Locale | Field | Was | Now |
| --- | --- | --- | --- |
| pt | p2 | Encontra desvio estabelecido… (finite verb, no subject, no clitic — broken) | Encontraram-se desvios estabelecidos… |
| pt | p6 | artigos de pesquisa (calque) | artigos científicos |
| de | title, h1 | Mit Anstrengung zu den Sternen (reads as physical strain) | Durch Mühsal zu den Sternen |
| de | p2 | wie getreu | wie genau |
| de | p2 | Eine belegte Abweichung zeigt sich in 7 von 83 bewertbaren Beobachtungen (one deviation in seven places) | Belegte Abweichungen fanden sich in 7 von 83 auswertbaren Beobachtungen |
| ru | p2 | Установленное расхождение обнаружено (tautology, singular) | Установленные расхождения обнаружены |
| ru | p3 | рабочим записям | рабочим материалам |
| fr | p6 | les téléchargements (the act of downloading) | les fichiers à télécharger |

**Not applied, and why:** the second pass also proposed softening *Audit* to *Prüfung* in German, adding a classifier before the Latin-script product names in Russian, italicising English work titles in French, and dropping the enumeration in the last paragraph of every page. These are style preferences, and the project's English terms are deliberate. The circularity in "the human is the human operator" is in the English canon and was kept.

**What both passes agreed on:** every figure is identical across all eight locales — 23 chapters, 24 press articles, July 2026, drift established in 7 of 83 assessable observations, 8.4 %, four tiers of vocabulary — and 7/83 rounds to 8.4 % correctly in each. Decimal marks follow local convention.

---

# Cold-Reading Back-Translation and Flag Report

Eight locales, read without reference to any source text. Back-translations are literal: they render what the words say, not what they were probably meant to say. Flags list what a native reader would mark.

---

## fr (Français)

**Literal back-translation**

title
: The Translator's Tale: With effort, up to the stars

description
: French summary of The Translator's Tale: 23 illustrated chapters on the Claim Transmission Atlas and the women and the men who carried it. Narrative in English. *(«celles et ceux» is the inclusive feminine+masculine doublet)*

h1
: With effort, up to the stars

lede
: A history of the Claim Transmission Atlas, and of the people who carried it

p1
: Twenty-three illustrated chapters, written in English. The Translator's Tale forms the third instalment of Schrödinger's Civilization, alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 press articles devoted to the OpenAI–Hugging Face incident of July 2026: it examines with what fidelity the press transmitted the public dossier. An established drift appears therein in 7 of the 83 evaluable observations, that is 8.4%.

p3
: The Minded-Language Audit applies the same examination to the production register of the project itself: four levels of vocabulary, a publication boundary, and the limits of what a lexical audit can establish.

p4
: In the narrative, the "Workers" are work roles entrusted to the AI, and "the human" is the human operator. As the prologue says: poetry must be preserved, but the facts more fiercely still.

p5
: The English title, "The Translator's Tale; or, Schrödinger's Cat's Tail", plays on tale (conte) and tail (queue), as a wink to Schrödinger's cat.

p6
: This page is a summary in French. The chapters, the articles and the downloads are in English.

cta_prologue
: Begin with the prologue (in English) →

cta_index
: Index of chapters (in English)

cta_home
: The Schrödinger's Civilization project

languages
: This page in other languages

alt
: Human silhouette under the Milky Way

**Flags**

- **Typography is exemplary and should be left alone.** Every colon is preceded by U+202F NARROW NO-BREAK SPACE, every « » carries the same narrow space inside, and "8,4 %" has it before the percent sign. This is correct French typesetting done properly, which is rare.
- **`h1` / `title` — "Avec effort".** Grammatical, but in ordinary French *avec effort* means "laboriously, with difficulty", not "through striving". As a headline it reads flat and slightly translated. Idiomatic: *À force d'efforts, jusqu'aux étoiles* or *Par l'effort, vers les étoiles*.
- **`lede` — stray comma.** "du Claim Transmission Atlas, et des personnes" — a comma before *et* joining two coordinate complements is not standard French punctuation. No other locale has it. Delete it.
- **`p2` — "préenregistré" is a false-friend trap.** It is the correct open-science term (*préenregistrement* of a protocol), but the dominant everyday sense of *préenregistré* is "pre-recorded". A French reader may parse "un audit préenregistré" as "a pre-recorded audit" on first pass. Safer: "un audit dont le protocole a été préenregistré".
- **`description` — three *et* in one breath** ("sur le Claim Transmission Atlas et celles et ceux qui…"), and the inclusive doublet here does not match the plain "des personnes" of the `lede`. Two fields a reader sees side by side in search results use two different strategies.
- **`p4` — "rôles de travail"** is a calque of "work roles". Every locale carries the same calque, so it presumably comes from the source; in French, "des fonctions confiées à l'IA" is more natural.
- Participle agreement in "l'ont porté" (referring to *le Claim Transmission Atlas*, masc. sg.) is correct in both `description` and `lede`. "le troisième volet" is good idiomatic French.

---

## es (Español)

**Literal back-translation**

title
: The Translator's Tale: With effort, toward the stars

description
: Spanish summary of The Translator's Tale: 23 illustrated chapters about the Claim Transmission Atlas and those who saw it through. Narrative in English.

h1
: With effort, toward the stars

lede
: A history of the Claim Transmission Atlas and of the people who saw it through

p1
: Twenty-three illustrated chapters, written in English. The Translator's Tale is the third part of Schrödinger's Civilization, alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 press articles about the OpenAI and Hugging Face incident of July 2026: it examines with what fidelity the press transmitted the public record. It detects an established deviation in 7 of 83 evaluable observations, that is, 8.4%.

p3
: The Minded-Language Audit applies that same examination to the project's own production record: four levels of vocabulary, a publication boundary and the limits of what a lexical audit can establish.

p4
: In the narrative, the "Workers" are work functions assigned to the AI and "the human" is the human operator. As the prologue says: poetry must be preserved, but the facts with more fierceness still.

p5
: The English title, "The Translator's Tale; or, Schrödinger's Cat's Tail", plays with tale (cuento) and tail (cola), in a nod to Schrödinger's cat.

p6
: This page is a summary in Spanish. The chapters, the articles and the downloads are in English.

cta_prologue
: Start with the prologue (in English) →

cta_index
: Index of chapters (in English)

cta_home
: The Schrödinger's Civilization project

languages
: This page in other languages

alt
: Human silhouette under the Milky Way

**Flags**

This is the cleanest of the eight. Nothing here is an error; both items below are cosmetic.

- **`p2` — "8,4 %" uses an ordinary space (U+0020).** The RAE prescribes a fixed/non-breaking space so the figure cannot wrap away from the sign. The French locale got this right with U+202F; Spanish should at least use U+00A0.
- **`p1` — asymmetric coordination.** "junto al Minded-Language Audit y el Claim Transmission Atlas" mixes *al* and *el*. Either "junto al A y al B" or "junto a A y B".
- "sacar adelante", "prerregistrada" (correct double-r after the prefix), "fiereza", and the « » quotes are all correct and natural. Publishable as-is.

---

## pt (Português)

**Literal back-translation**

title
: The Translator's Tale: With effort, toward the stars

description
: Portuguese summary of The Translator's Tale: 23 illustrated chapters about the Claim Transmission Atlas and the people who carried it forward. Narrative in English.

h1
: With effort, toward the stars

lede
: A history of the Claim Transmission Atlas and of the people who carried it forward

p1
: Twenty-three illustrated chapters, written in English. The Translator's Tale is the third part of Schrödinger's Civilization, alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 press articles about the OpenAI–Hugging Face incident of July 2026: it examines with what fidelity the press transmitted the public record. It finds established deviation in 7 of 83 evaluable observations, that is, 8.4%.

p3
: The Minded-Language Audit turns the same examination toward the project's own production record: four levels of vocabulary, a publication boundary and the limits of what a lexical audit can establish.

p4
: In the narrative, the "Workers" are work functions assigned to the AI and "the human" is the human operator. As the prologue says: poetry must be preserved, but the facts with even more ferocity.

p5
: The English title, "The Translator's Tale; or, Schrödinger's Cat's Tail", plays with tale (conto) and tail (cauda), in an allusion to Schrödinger's cat.

p6
: This page is a summary in Portuguese. The chapters, the articles and the downloads are in English.

cta_prologue
: Begin with the prologue (in English) →

cta_index
: Index of chapters (in English)

cta_home
: The Schrödinger's Civilization project

languages
: This page in other languages

alt
: Human silhouette under the Milky Way

**Flags**

- **`p2` — "8,4%" is the only European locale with no space before the percent sign.** fr, es, de and ru all have one. Portuguese norm wants the space too. Fix for both correctness and cross-locale consistency.
- **`p2` — "Encontra desvio estabelecido" drops the article.** Bare "desvio" reads telegraphic/headline-ish against the measured register of the rest. "Encontra um desvio estabelecido" or "Encontra desvios estabelecidos".
- **`p3` — "volta o mesmo exame para"** is a loose calque of "turns the same examination on". Natural Portuguese: "dirige o mesmo exame ao" or "aplica o mesmo exame ao".
- **Variety is consistently pt-BR** — *registro*, *fatos*, *pré-registrada*, *downloads*, “ ” quotes. Internally consistent, which is good; but a pt-PT audience would expect *registo*, *factos*, and « ». Decide which market this serves.
- Nothing grammatically wrong. Hyphenation ("pré-registrada") and the en dash in "OpenAI–Hugging Face" are correct.

---

## de (Deutsch)

**Literal back-translation**

title
: The Translator's Narrative: With difficulty / only just, to the stars

description
: German summary of The Translator's Narrative: 23 illustrated chapters about the Claim Transmission Atlas and the people behind it. Narrated in English.

h1
: With difficulty / only just, to the stars

lede
: A history of the Claim Transmission Atlas and of the people who carried it

p1
: Twenty-three illustrated chapters, written in English. The Translator's Narrative is the third part of Schrödinger's Civilization, alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 press articles about the incident at OpenAI and Hugging Face in July 2026: it examines how faithfully the press reproduced the publicly documented state of the facts. An evidenced deviation shows up in 7 of 83 assessable observations, that is 8.4%.

p3
: The Minded-Language Audit directs the same scrutiny at the project's own production documentation: four levels of vocabulary, a publication boundary and the limits of what a lexical audit can show.

p4
: In the narrative the "Workers" are AI work roles, and "the human" is the human operator. As the prologue puts it: poetry must be preserved, the facts however even more resolutely.

p5
: The English title "The Translator's Tale; or, Schrödinger's Cat's Tail" plays with tale (Erzählung) and tail (Schwanz) – an allusion to Schrödinger's cat.

p6
: This page is a summary in German. The chapters, the essays and the downloads are in English.

cta_prologue
: Begin with the prologue (in English) →

cta_index
: Chapter overview (in English)

cta_home
: The Schrödinger's Civilization project

languages
: This page in other languages

alt
: Human silhouette under the Milky Way

**Flags**

This is the weakest locale and the only one with errors I would call blocking.

- **BLOCKING — `title` / `h1`: "Mit Mühe zu den Sternen".** *Mit Mühe* in German means "with difficulty", "barely", "only just" — *er schaffte es mit Mühe* = "he only just managed it". The German headline therefore reads **"barely making it to the stars"**, which inverts the striving sense every other locale carries. Replace with *Mit Anstrengung zu den Sternen*, *Durch Mühsal zu den Sternen*, or the established Latin *Per aspera ad astra*.
- **BLOCKING — `p2`: "die öffentlich dokumentierte Faktenlage".** Literally "the publicly documented state of the facts". Every other locale says *the public record* (dossier public / registro público / registro público / публичные сведения / 公的な記録 / 공개 기록 / 公开记录). On a page whose entire subject is whether the press transmitted a record faithfully, calling that record a *Faktenlage* takes an evidential position the German text is not entitled to and the other seven locales do not take. Use *die öffentlich zugänglichen Unterlagen* or *den öffentlichen Aktenbestand*.
- **`description` vs `lede` — internal inconsistency.** "die Menschen dahinter" ("the people behind it") loses the "carried it" sense that the `lede` keeps ("die Menschen, die ihn getragen haben"). These two fields appear together in a search result.
- **`p3` — Grenze/Grenzen echo.** "eine Publikationsgrenze und die Grenzen dessen, was…" — the same root twice in eight words. Also "zeigen kann" is weaker than the *establish* that fr/es/pt use for the same clause.
- **`p4` — "der menschliche Operator".** *Operator* exists in German for industrial-plant and reactor operators, but applied to a person running an AI writing pipeline it reads as an untranslated calque. *Der Mensch an der Steuerung* or *der menschliche Bediener* is plainer.
- **`p4` — "entschiedener" ("more resolutely")** softens the "fiercely" the other locales keep (fr *plus farouchement*, es *con más fiereza*, pt *com ainda mais ferocidade*).
- **`p6` — "die Aufsätze" ("the essays")** where fr/es/pt/ru say "articles" and ja/ko/zh say "academic papers". See the cross-locale section.
- Noun capitalisation, „ " quotes, the en dash in p5, and "8,4 %" spacing are all correct. Gender assignment is internally consistent and defensible (*der* Atlas masc., *das* Audit neut.), and the dative "dem … und dem …" in p1 works for both.

---

## ru (Русский)

**Literal back-translation**

title
: The Translator's Tale: With effort — to the stars

description
: Summary of "The Translator's Tale" in Russian: 23 illustrated chapters about the Claim Transmission Atlas and the people who led this work. The text is in English.

h1
: With effort — to the stars

lede
: The history of the Claim Transmission Atlas and of the people who led this work

p1
: Twenty-three illustrated chapters, written in the English language. "The Translator's Tale" is the third part of the Schrödinger's Civilization project, alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 press publications about the incident involving OpenAI and Hugging Face in July 2026: it checks how accurately the press conveyed the public information. An established discrepancy was found in 7 of 83 observations suitable for evaluation, that is, in 8.4%.

p3
: The Minded-Language Audit turns the same check onto the project's own working archive: four levels of lexis, a publication boundary, and the limits of what a lexical audit is able to show.

p4
: In the tale, "Workers" are work roles performed by the AI, and "the human" is the human operator. As it is said in the prologue: poetry must be preserved, but the facts — even more resolutely.

p5
: The English title "The Translator's Tale; or, Schrödinger's Cat's Tail" plays on the consonance of tale (повесть) and tail (хвост) — a reference to Schrödinger's cat.

p6
: This page is a summary in the Russian language. The chapters, the articles and the files for download are in English.

cta_prologue
: Start from the prologue (in English) →

cta_index
: Table of contents (in English)

cta_home
: The Schrödinger's Civilization project

languages
: This page in other languages

alt
: Silhouette of a person under the Milky Way

**Flags**

- **`p2` — "то есть в 8,4 %" is dangling.** "that is, in 8.4%" — in 8.4% of *what*? Russian needs "то есть в 8,4 % случаев" or, cleaner, "что составляет 8,4 %". This wart sits on the sentence carrying the page's headline statistic.
- **`p3` — "обращает ту же проверку на…" is a calque** of English "turns the same examination on". Russian idiom is "применяет ту же проверку к…" or "направляет ту же проверку на…". As written it reads translated.
- **`p3` — "рабочий архив проекта" ("the project's working archive")** names a different object from the "production record" of the other seven locales. If the audited thing is a production log, "производственный журнал проекта" or "рабочие записи проекта".
- **`p2` — "публичные сведения" ("public information")** is vaguer than "public record"; "общедоступные материалы" or "публичный протокол" is closer.
- **`title` / `h1` — "С усилием"** is grammatical but stiff as a headline. Russian already has the ready-made phrase for exactly this: "Через тернии — к звёздам".
- **`p1` — inconsistent title marking.** "«Повесть переводчика»" takes guillemets while "Minded-Language Audit" and "Claim Transmission Atlas" sit bare in the same sentence. Defensible (Latin script often goes unquoted), but pick a rule and hold it.
- **`p2` — "8,4 %" uses an ordinary space**; a non-breaking space is the typographic norm.
- **ё is used consistently and correctly** throughout — звёздам, ещё, Шрёдингера, Млечным Путём. « » are the correct quote marks and are used consistently. Case government and the instrumental in the alt text are all correct.

---

## ja (日本語)

**Literal back-translation**

title
: The Translator's Story: Piling up effort, to the stars

description
: Japanese summary of "The Translator's Story". 23 illustrated chapters in all, depicting the Claim Transmission Atlas and the people who shouldered that work. The main text is in English.

h1
: Piling up effort, to the stars

lede
: The history of the Claim Transmission Atlas and the people who shouldered it

p1
: This is a story of 23 illustrated chapters, written in English. "The Translator's Story" corresponds to the third part of Schrödinger's Civilization, standing alongside the Minded-Language Audit and the Claim Transmission Atlas.

p2
: The Claim Transmission Atlas is a pre-registration-type audit covering 24 articles that reported the OpenAI · Hugging Face incident of July 2026, verifying how faithfully the reporting conveyed the public record. A confirmed deviation was found in 7 (8.4%) of the 83 evaluable observations.

p3
: The Minded-Language Audit turns the same verification toward the project's own work record. Namely: four stages of vocabulary, the boundary of publication, and the limits of what a vocabulary audit can show.

p4
: The "Workers" in the story refer to the AI's work roles, and "the human" refers to the human operator. To borrow the words of the prologue: poetry must be protected, but the facts must be protected even more strongly.

p5
: The English title "The Translator's Tale; or, Schrödinger's Cat's Tail" is wordplay crossing tale (物語) with tail (しっぽ), in reference to Schrödinger's cat.

p6
: This page is a summary in Japanese. The chapters, the papers and the downloads are all in English.

cta_prologue
: Read from the prologue (English) →

cta_index
: List of chapters (English)

cta_home
: Project Schrödinger's Civilization

languages
: Other language versions of this page

alt
: Silhouette of a person beneath the Milky Way

**Flags**

Nothing here is an error. The punctuation is correct throughout — fullwidth ：, 、, 。, fullwidth parentheses, halfwidth digits and %, no space around numerals, spaces around Latin words. All of that is standard practice. The flags below are naturalness, not correctness.

- **`lede` — 歴史.** 歴史 is "history" in the chronicle/academic sense. For a 23-chapter illustrated narrative, 物語 or 記録 reads better; 歴史 makes it sound like a scholarly history *of* the Atlas rather than the story of making it.
- **`p1` — tangled modifier.** "Minded-Language Audit と Claim Transmission Atlas と並ぶ Schrödinger's Civilization の第三部にあたります" stacks a と…と並ぶ relative clause in front of a long Latin title; hard to parse. Recast: 「…は Schrödinger's Civilization の第三部で、Minded-Language Audit、Claim Transmission Atlas と並びます」.
- **`p2` — 「83件の観察」.** 観察 is the *act* of observing. As a countable data point Japanese wants 観察項目, 観測, or 観察事例. (Same issue in ko and zh.)
- **`p2` — 「OpenAI・Hugging Face インシデント」.** The nakaguro can be read as fusing the two into one compound name rather than meaning "and". 「OpenAI と Hugging Face をめぐるインシデント」 is unambiguous.
- **`p4` — repetition.** 守らなければならない appears twice in one sentence and the whole thing closes with 「…ということです」, which is wordier and flatter than the terse aphorism the other locales carry.
- **`p3` — 「語彙の四つの段階」** → 「語彙の四段階」 is tighter. The sentence also switches from verb-final to a 体言止め list glued on with です, which is slightly awkward.
- **`alt` — 「天の川の下の人のシルエット」** chains three の. 「天の川の下に立つ人のシルエット」 reads better.

---

## ko (한국어)

**Literal back-translation**

title
: The Translator's Story: With effort, toward the stars

description
: Korean summary of "The Translator's Story". 23 chapters including illustrations, covering the Claim Transmission Atlas and the people who led that work. The main text is in English.

h1
: With effort, toward the stars

lede
: The history of the Claim Transmission Atlas and the people who led that work

p1
: This is a story of 23 chapters including illustrations, written in English. "The Translator's Story", together with the Minded-Language Audit and the Claim Transmission Atlas, forms the third part of Schrödinger's Civilization.

p2
: The Claim Transmission Atlas is a pre-registered audit of 24 articles covering the OpenAI–Hugging Face incident of July 2026, examining how faithfully the press conveyed the public record. A confirmed departure was found in 7 (8.4%) of the 83 evaluable observations.

p3
: The Minded-Language Audit applies the same examination to the project's own work record. Namely, four stages of vocabulary, the boundary of disclosure, and the limits of what a vocabulary audit can bring to light.

p4
: The 'Workers' in the story are work roles taken on by the AI, and 'the human' is the human operator. As the prologue says, poetry must be protected, but the facts must be protected still more firmly.

p5
: The English title "The Translator's Tale; or, Schrödinger's Cat's Tail" is a pun weaving together tale (이야기) and tail (꼬리), calling to mind Schrödinger's cat.

p6
: This page is a Korean summary. The chapters, the papers and the download files are all in English.

cta_prologue
: Read from the prologue (English) →

cta_index
: Chapter list (English)

cta_home
: The Schrödinger's Civilization project

languages
: Other languages of this page

alt
: Silhouette of a person under the Milky Way

**Flags**

- **Three quoting systems on one page.** 「 」 in `description` and `p1`, ‘ ’ in `p4`, “ ” in `p5`. Pick one. Current Korean orthography prefers 《 》/〈 〉 or plain quotation marks for titles; 「 」 is permitted but reads Japanese-influenced on a Korean page, and mixing all three in five fields looks careless.
- **`description` / `p1` — "삽화 포함 23개 장".** A noun stack, and 23개 장 double-counts: 장 is itself a counter, so this is "23 pieces of chapter". Natural: "삽화를 실은 23개 장" or simply "전 23장".
- **`p1` — four modifiers before the head noun.** "영어로 쓰인 삽화 포함 23개 장의 이야기입니다" is a pile-up. Split into two clauses.
- **`p2` — "사전 등록 감사"** is an unmarked noun chain; "사전 등록된 감사" or "사전 등록 방식의 감사" is clearer. 감사 is also ambiguous out of context (gratitude / inspection / audit) — "감사(audit)" on first use would help.
- **`p2` — "관찰 83건".** As in ja and zh, 관찰 is the *act* of observing; the countable unit is 관찰 항목.
- **`p2` — "이탈"** for the audit finding reads as "departure from a route". Depending on what the Atlas actually measures, 편차 or 왜곡 may be closer.
- **`h1` — "노력으로, 별을 향해"** ends on the connective 향해 and so feels unfinished as a standalone headline. "노력으로 별을 향하여" or "노력 끝에 별까지".
- **Particle attachment to the English proper nouns is correct throughout** — Atlas는 / Atlas와 / Audit은 / Civilization의, all with no stray space. Halfwidth parentheses, the colon in the title, and the spacing before → are all correct Korean practice. No spacing errors found.

---

## zh-hans (简体中文)

**Literal back-translation**

title
: The Translator's Story: Through effort, at last reaching the stars

description
: Chinese summary of "The Translator's Story": 23 chapters in total, furnished with illustrations, telling of the Claim Transmission Atlas and the people who drove this work forward. The main text is in English.

h1
: Through effort, at last reaching the stars

lede
: The history of the Claim Transmission Atlas and of the people who drove it forward

p1
: This is a 23-chapter story written in English and furnished with illustrations. "The Translator's Story", together with the Minded-Language Audit and the Claim Transmission Atlas, constitutes the third part of Schrödinger's Civilization.

p2
: The Claim Transmission Atlas is a pre-registered audit that examined 24 news articles reporting the OpenAI and Hugging Face incident of July 2026, testing to what degree the press faithfully conveyed the public record. Among 83 evaluable observations, 7 (8.4%) were confirmed to contain drift.

p3
: The Minded-Language Audit turns the same scrutiny onto the project's own work record: four tiers of wording, one line of publication, and the limit of what an audit at the lexical level can explain.

p4
: The "Workers" in the story refer to the work roles undertaken by artificial intelligence; "humankind" refers to the human operator. As the preface says: the poetic must be preserved, while the facts must be held to still more firmly.

p5
: The English title "The Translator's Tale; or, Schrödinger's Cat's Tail" makes use of the near-homophony of tale (故事) and tail (尾巴), echoing "Schrödinger's cat".

p6
: This page is a Chinese summary. The chapters, papers and download files are all in English.

cta_prologue
: Start reading from the prologue (English) →

cta_index
: Chapter contents (English)

cta_home
: The Schrödinger's Civilization project

languages
: Other language versions of this page

alt
: A human figure beneath the Milky Way

**Flags**

- **BLOCKING — `p4`: 「“人类”指人类操作者」.** 人类 means "humankind / the human species", not "the human" as an individual. The sentence reads "'Humankind' refers to the human operator", which is both wrong in sense and circular — it glosses a term with the same word plus a noun. Should be 「“人”指人类操作者」, or whatever single-person term the story actually uses. Note that every other locale's equivalent gloss works because the quoted term and the gloss differ in grade; here they do not.
- **`description` — misused 顿号.** 「共 23 章、配有插图，讲述…」 uses 、 to join a quantity statement to a predicate. 顿号 is for coordinate items of the same kind. Use a comma: 「共 23 章，配有插图，讲述…」. (The 顿号 in `p1`, 「以英文写成、配有插图的」, is fine — those are genuinely parallel attributives.)
- **`lede` — 的 pile-up.** 「Claim Transmission Atlas 及推动它的人们的历史」 has two 的 in four characters. Recast: 「Claim Transmission Atlas 及其推动者的故事」.
- **`p2` — spaced dates.** 「2026 年 7 月」. Pangu spacing is applied consistently to Latin words and numerals everywhere on the page, which is defensible as a house style, but spacing *inside* a Chinese date is unusual; most Chinese typesetting writes 2026年7月.
- **`p3` — 「一条发表的界线」.** 界线 takes the measure word 道, not 条, and 「发表的界线」 wants to be 「发表界线」 or 「可发表的边界」.
- **`p2` — 「83 项可评估的观察」.** As in ja and ko, 观察 is the act of observing; the countable unit is 观察项 or 观测值.
- **`p2` — 「偏移」** reads as a physical or numeric shift. For a fidelity audit, 偏差 or 失真 may be the better word.
- **`alt` — 「人影」** means an indistinct figure or shadow of a person. The precise word for silhouette is 剪影.
- **`h1` 「历经努力，终抵群星」 is the strongest headline of the eight** — genuinely idiomatic, with a real rhythm. Fullwidth colon, commas and parentheses are all correct; the decimal point in 8.4% is correct for Chinese.

---

## Cross-Locale Consistency

### Figures — fully consistent

Every factual figure is identical in all eight locales. Verified by extraction, not by eye:

| Figure | fr | es | pt | de | ru | ja | ko | zh |
|---|---|---|---|---|---|---|---|---|
| Chapters | 23 | 23 | 23 | 23 | 23 | 23 | 23 | 23 |
| Press articles audited | 24 | 24 | 24 | 24 | 24 | 24 | 24 | 24 |
| Incident date | July 2026 | July 2026 | July 2026 | July 2026 | July 2026 | 2026年7月 | 2026년 7월 | 2026 年 7 月 |
| Drift found | 7 of 83 | 7 of 83 | 7 of 83 | 7 of 83 | 7 of 83 | 83件中7件 | 83건 중 7건 | 83 项中 7 项 |
| Percentage | 8,4 % | 8,4 % | 8,4% | 8,4 % | 8,4 % | 8.4% | 8.4% | 8.4% |
| Vocabulary levels | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Publication boundaries | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Part number in series | 3rd | 3rd | 3rd | 3rd | 3rd | 第三部 | 세 번째 | 第三部分 |

**No locale differs on any figure.** 7/83 = 8.434%, so 8.4% is a correct rounding everywhere. Decimal marks follow local convention correctly (comma in fr/es/pt/de/ru, point in ja/ko/zh). The only numeric-presentation deviation is **pt omitting the space before %**, where the other four European locales include it.

The European locales spell out "twenty-three" in `p1` and use "23" in `description`; the CJK locales use digits in both. That is a convention difference, not an inconsistency.

### Terminology — not consistent, and some of it is substantive

These are not figures, but they are facts the page asserts, and readers of different languages are currently told different things.

1. **What was audited (`p2`).** fr *le dossier public*, es *el registro público*, pt *o registro público*, ja 公的な記録, ko 공개 기록, zh 公开记录 — all "the public record". But **de says *die öffentlich dokumentierte Faktenlage*** ("the publicly documented state of the facts") and **ru says *публичные сведения*** ("public information"). German in particular asserts facticity on a page about whether facts were transmitted faithfully.
2. **What the Minded-Language Audit examines (`p3`).** Seven locales say some form of "the project's production/work record". **ru says *рабочий архив* ("working archive")** — a different object.
3. **What the audit can do (`p3`).** fr *établir*, es *establecer*, pt *estabelecer* = "establish". de *zeigen*, ru *показать*, ja 示せる, ko 밝힐 수 있는, zh 说明 = "show / reveal / explain". "Establish" is the evidential term; "show" is weaker. Readers get two different epistemic claims about the audit's reach.
4. **What the downloads are (`p6`).** fr *les articles*, es *los artículos*, pt *os artigos*, ru *статьи* = "articles". **de *die Aufsätze* = "essays". ja 論文, ko 논문, zh 论文 = "academic papers".** Three different kinds of document. Worse, `p2` has already used "articles" to mean the 24 *press* articles under audit, so a reader of the French or Spanish page may take `p6` to mean the press articles are downloadable. Settle on one term per concept and propagate it.
5. **Headline register.** zh 历经努力 and ja 努力を重ねて are idiomatic. es *Con esfuerzo* and pt *Com esforço* are fine. fr *Avec effort*, ru *С усилием* and ko 노력으로 are stiff. **de *Mit Mühe* is wrong** — it means "barely".
6. **Quote marks for "Workers".** fr « » (with narrow spaces), es « », pt “ ”, de „ ", ru « », ja 「 」, zh “ ” — all correct for their language. **ko uses ‘ ’ here but “ ” in `p5` and 「 」 in `description`** — the only locale that is internally inconsistent.
