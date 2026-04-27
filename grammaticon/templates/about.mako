<%inherit file="home_comp.mako"/>

<h2>About the Grammaticon</h2>

<p>The Grammaticon is an evolving database of grammatical comparative concepts
with proposed definitions and links to typological features from typological
feature collections such as
${h.external_link('https://wals.info/', label='WALS')}
(World atlas of language structures, Haspelmath et al. 2005),
${h.external_link('https://grambank.clld.org/', label='Grambank')}
(Skirgård et al. 2023), and
${h.external_link('https://apics-online.info/', label='APiCS')}
(Atlas of Pidgin and Creole language structures, Michaelis et al. 2013).</p>

<p>It was inspired by the
${h.external_link('https://concepticon.clld.org', label='Concepticon')}
(List et al. 2016), a database of lexical comparative concepts, and it is hoped
that it will facilitate comparison of typological datasets in the future.  Such
comparison is often still limited by variable usage of grammatical terminology
and lack of clarity of definitions.  The Grammaticon provides not only links
between grammatical terms and typological features, but (for many of the
features) also discussion of how the grammatical terms relate to each other.</p>

<p>When the definition of a grammatical term contains other technical terms,
these are preceded by a symbol (°) in the definition and listed in the box on
the right-hand side of the detail page for the term (“defining concepts”).  This
box also lists the “derived terms”, as well as related typological features.</p>

<p>Definitions which are preliminary are enclosed in double square brackets
([[…]]).</p>

<h3>Frequently asked questions (FAQ)</h3>

<h4>Does the Grammaticon aim to contain the definitive list of all needed grammatical comparative-concept terms?</h4>

<p>Not at all – it primarily aims to provide clear and sharp definitions of
a wide range of terms that are already widely used as comparative concepts by
linguists.  The set of grammatical comparative-concept terms that one might need
is completely open-ended, just like the set of lexical concepts that one might
need for lexical comparison is open-ended.  Linguists create new concepts all
the time, any maybe it would be helpful if they created new terms as well (in
order to avoid proliferation of polysemy).</p>

<h4>Are there similar databases of grammatical terms elsewhere?</h4>

<p>Yes, there is a recently published
${h.external_link('https://comparative-concepts.github.io/cc-database/cc-database.html', label='database of comparative concepts by William Croft')}.
The Grammaticon systematically links to these definitions, as well as to
Wikipedia and SIL’s Glossary of Linguistic terms.  The Grammaticon offers one
perspective, without claiming that it is the only one.</p>

<h4>Why are the Grammaticon’s definitions sharp rather than prototype-based?</h4>

<p>It is true that the reality is often continuous, but scientists must impose
sharp boundaries in order to capture this continuity quantitatively.  Without
sharp concepts as units of measurement, precise quantification is not possible,
and all comparison remains vague.  Some scientific concepts may not be amenable
to sharp definitions, but technical terms of grammar should ultimately be
subject to quantitative evaluation and should therefore be defined with clear
boundaries.</p>

<h4>What is the value of strange definitions of familiar terms, such as the Grammaticon’s definition of “word” and “affix”?</h4>

<p>Linguists typically assume implicitly that their technical terms (including
even “word”) have a clear meaning, even though they often fail to provide
definitions.  But it is only when one provides an explicit definition that one
can see problems with approaches that leave definitions implicit.  It appears
that one of the reasons why linguists are often reluctant to provide definitions
is that they think of the terms as referring to natural-kinds concepts
(Haspelmath 2018), i.&thinsp;e. entities that exist in nature to be discovered
or fully elucidated by linguists.  It may be that “words” and “affixes” exist in
nature, but as long as we do not know whether they do, it is best to use these
terms as comparative concepts with clear definitions.</p>

<h4>How do these comparative-concept terms relate to language description?</h4>

<p>Each language has its own unique categories (Haspelmath 2020), so descriptive
work must normally work with language-particular categories, defined in terms of
language-particular notions.  By contrast, the Grammaticon’s terms are
comparative concepts, which are defined in the same way for all languages
(Haspelmath 2018).  Thus, they are not directly suitable for language
description/analysis, and many of the definitions come from typological work.
However, language description can often be inspired by the general concepts
defined by typologists, and language-particular descriptions are more
transparent if they use similar terms.</p>

<h4>Are all of the definitions given in the Grammaticon “retro-definitions”?</h4>

<p>Most of them are retro-definitions, i.&thinsp;e. definitions of well-known
terms that have been provided retroactively (Haspelmath 2021).  Most well-known
terms have spread among linguists via salient exemplars, rather than via
definitions, and the Grammaticon aims to provide clear (retro-)definitions for
them.  However, the Grammaticon also contains a number of neologisms which seem
helpful, such as “numerative”, “hyparctic clause”, and “duonominal clause”.</p>

<h3>References</h3>

<ul>
<li>Haspelmath, Martin. 2018. How comparative concepts and descriptive
  linguistic categories are different. In Van Olmen, Daniël &amp; Mortelmans,
  Tanja &amp; Brisard, Frank (eds.), <em>Aspects of linguistic variation:
  Studies in honor of Johan van der Auwera</em>, 83–113. Berlin: De Gruyter
  Mouton.
  (${h.external_link('https://doi.org/10.1515/9783110607963-004', label='doi:10.1515/9783110607963-004')})
  (${h.external_link('https://zenodo.org/record/3519206')})</li>
<li>Haspelmath, Martin. 2020. The structural uniqueness of languages and the
  value of comparison for description. <em>Asian Languages and Linguistics</em>
  1(2). 346–366.
  (DOI: ${h.external_link('https://doi.org/10.1075/alal.20032.has', label='10.1075/alal.20032.has')})</li>
<li>Haspelmath, Martin. 2021. Towards standardization of morphosyntactic
  terminology for general linguistics. In Alfieri, Luca &amp; Arcodia, Giorgio
  Francesco &amp; Ramat, Paolo (eds.), <em>Linguistic categories, language
  description and linguistic typology</em>, 35–57. Amsterdam: Benjamins.
  (DOI: ${h.external_link('https://chooser.crossref.org/?doi=10.1075%2Ftsl.132.02has', label='10.1075/tsl.132.02has')},
  ${h.external_link('https://ling.auf.net/lingbuzz/005489')})</li>
<li>Haspelmath, Martin &amp; Dryer, Matthew &amp; Gil, David &amp; Comrie,
  Bernard (eds.). 2005. <em>The world atlas of language structures.</em>
  Oxford: Oxford University Press.
  (${h.external_link('https://wals.info/')})</li>
<li>List, Johann-Mattis &amp; Cysouw, Michael &amp; Forkel, Robert. 2016.
  Concepticon: A resource for the linking of concept lists. <em>Proceedings of
  the Tenth International Conference on Language Resources and Evaluation
  (LREC’16)</em>, 2393–2400.</li>
<li>Michaelis, Susanne Maria &amp; Maurer, Philippe &amp; Haspelmath, Martin
  &amp; Huber, Magnus (eds.). 2013. <em>Atlas of pidgin and creole language
  structures.</em> Oxford: Oxford University Press.
  (${h.external_link('https://apics-online.info/')})</li>
<li>Skirgård, Hedvig &amp; Haynie, Hannah J. &amp; Blasi, Damián E. &amp;
  Hammarström, Harald &amp; Collins, Jeremy &amp; Latarche, Jay J. &amp; Lesage,
  Jakob et al. 2023. Grambank reveals the importance of genealogical constraints
  on linguistic diversity and highlights the impact of language loss. <em>Science
  Advances</em> 9(16). eadg6175.
  (DOI: ${h.external_link('https://doi.org/10.1126/sciadv.adg6175', label='10.1126/sciadv.adg6175')})</li>
</ul>
