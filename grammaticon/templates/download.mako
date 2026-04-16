<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>
<%! from grammaticon import models %>

<h3>Downloads</h3>

<% dataset = next(request.db.execute(request.db.query(models.GrammaticonDataset)))[0] %>

<p>You can download the latest release of the Grammaticon data
${h.external_link(f'https://doi.org/{dataset.zenodo_concept_doi}', label='on Zenodo')}.</p>

<p>You can find the the latest work-in-progress version
${h.external_link(dataset.repo, label='on Github')}.</p>
