<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
  <div style="text-align: center; margin: 1em 5em 1em 5em;">
    <img
      src="${request.static_url('grammaticon:static/grammaticon-logo.png')}"
      alt="Grammaticon logo"
      style="width: 13em;"
      />
  </div>

  <%util:well title="Cite">
    ${h.newline2br(h.text_citation(request, ctx))|n}
    % if ctx.doi:
    <p>
      <a href="https://doi.org/${ctx.doi}">
        <img src="https://zenodo.org/badge/DOI/${ctx.doi}.svg" alt="DOI">
      </a>
    </p>
    % endif
    ${h.cite_button(request, ctx)}
  </%util:well>

  <%util:well title="Version">
    <p>
      <a href="https://${req.dataset.domain}">${req.dataset.domain}</a>
      serves the latest released version of data curated at
      ${h.external_link(req.dataset.repo)}.
      % if ctx.zenodo_concept_doi:
      Older released versions are accessible via DOI
      <a href="https://doi.org/${ctx.zenodo_concept_doi}">
        <img src="https://zenodo.org/badge/DOI/${ctx.zenodo_concept_doi}.svg" alt="DOI">
      </a>
      on Zenodo as well.
      % endif
    </p>
  </%util:well>

</%def>

<h2>Welcome to the Grammaticon</h2>

<p>The Grammaticon is a collection of grammatical comparative concept terms with
definitions and links to other resources and comparative data collections such
as WALS (The World Atlas of Language Structures) and Grambank.</p>

<p>Version 1.0 is an early-release version that is still in some ways
incomplete. The plan is to update and expand it regularly.</p>

<h3>Concepts</h3>

<p>The Grammaticon contains several hundred English grammatical concept terms, with
(retro-)definitions by Martin Haspelmath, and links to corresponding terms in
the English Wikipedia, the SIL Glossary of Linguistic Terms, and Croft’s
Comparative Concepts Database
(${h.external_link('https://comparative-concepts.github.io/cc-database/cc-database.html')};
originally in the online appendix of Croft (2022).</p>

<p>In the definitions, a superscript circle (°) marks terms which are defined
elsewhere in the Grammaticon (“defining concepts”). Each concept page also shows
the “derived concepts” (which are defined with reference to it), as well as
“related features”.
[[Some concepts have preliminary definitions, enclosed in double square
brackets.]]</p>

<h3>Features</h3>

<p>The Grammaticon links hundreds of cross-linguistic datasets to the concept
terms, from a range of cross-linguistic dataset collections such as WALS,
Grambank and CrossGram. Each dataset is characterized by a “feature” (or
“parameter”), on which there is information for a wide range of languages
(dozens, and often hundreds). Each feature page offfers a definition of the
feature, usually copied from the database, and sometimes with comments
(“Relation to Grammaticon concepts”) on how exactly the feature’s definition
relates to the Grammaticon concepts.</p>

<h3>Collections</h3>

<p>The “Collections” page lists the collections from which the features are taken,
with brief descriptions. In addition to larger collections such as WALS,
Grambank and APiCS, there are also smaller collections, e.g. contributions from
CrossGram.</p>

<p>For most of the collections, not all features are included, because the
Grammaticon focuses on grammatical type features, and some of the collections
also include lexical features and/or cognate features.</p>
