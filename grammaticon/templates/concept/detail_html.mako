<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "concepts" %>
<%block name="title">Concept: ${ctx.name}</%block>
<%! from clld.db.models import common %>
<%! import grammaticon.models as m %>

<h2>Concept: ${ctx.name}</h2>

<%def name="sidebar()">
  <div class="well">
    % if ctx.parents:
    <h4>Defining concepts:</h4>
    <ul>
      % for c in ctx.parents:
      <li>${h.link(req, c)}</li>
      % endfor
    </ul>
    % endif

    % if ctx.children:
    <h4>Derived concepts:</h4>
    <ul>
      % for c in ctx.children:
      <li>${h.link(req, c)}</li>
      % endfor
    </ul>
    % endif
    <%
      features = list(request.db.query(m.Feature)
        .join(common.ValueSet)
        .join(common.Contribution)
        .join(m.Metafeature)
        .join(m.ConceptMetafeature)
        .filter(m.ConceptMetafeature.concept_pk == ctx.pk)
        .distinct())
    %>
    % if features:
    <h4>Related features:</h4>
    <ul>
      % for feature in features:
      <li>${h.link(req, feature)} (${h.link(req, feature.valueset.contribution)})</li>
      % endfor
    </ul>
    % endif
  </div>
</%def>


% if ctx.description or ctx.comments or ctx.wikipedia_counterpart or ctx.sil_counterpart or ctx.croft_counterpart or ctx.quotation or ctx.references:
<dl class="concept-properties">
  % if ctx.description:
  <dt>Description</dt>
  <dd>${ctx.description}</dd>
  % endif
  % if ctx.comments:
  <dt>Comments</dt>
  <dd>${ctx.comments}</dd>
  % endif
  % if ctx.croft_counterpart:
  <dt>Croft (2022)</dt>
  %   if ctx.croft_definition:
  <dd><strong>${ctx.croft_counterpart}</strong>: ${ctx.croft_definition}</dd>
  %   else:
  <dd><strong>${ctx.croft_counterpart}</strong></dd>
  %   endif
  % endif
  % if ctx.wikipedia_counterpart:
  <dt>Wikipedia</dt>
  %   if ctx.wikipedia_url:
  <dd>${h.external_link(ctx.wikipedia_url, label=ctx.wikipedia_counterpart)}</dd>
  %   else:
  <dd>${ctx.wikipedia_counterpart}</dd>
  %   endif
  % endif
  % if ctx.sil_counterpart:
  <dt>SIL dictionary</dt>
  %   if ctx.sil_url:
  <dd>${h.external_link(ctx.sil_url, label=ctx.sil_counterpart)}</dd>
  %   else:
  <dd>${ctx.sil_counterpart}</dd>
  %   endif
  % endif
  % if ctx.quotation:
  <dt>Quotation</dt>
  <dd>${ctx.quotation}</dd>
  % endif
  % if ctx.references:
  <dt>Sources</dt>
  <dd>${h.linked_references(request, ctx)|n}</dd>
  % endif
</dl>
% endif
