<%inherit file="home_comp.mako"/>
<%! from grammaticon import models %>

<h3>Downloads</h3>

<% dataset = request.db.query(models.GrammaticonDataset).one() %>

<p>You can download the latest release of the Grammaticon data
${h.external_link(f'https://doi.org/{dataset.zenodo_concept_doi}', label='on Zenodo')}.</p>

<p>You can find the the latest work-in-progress version
${h.external_link(dataset.repo, label='on Github')}.</p>
