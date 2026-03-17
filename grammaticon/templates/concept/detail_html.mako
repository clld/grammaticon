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
      features = list(
        request.db.query(m.Feature)
        .join(m.ConceptFeature)
        .filter(m.ConceptFeature.concept_pk == ctx.pk)
        .outerjoin(common.Contribution)
        .distinct())
    %>
    % if features:
    <h4>Related features:</h4>
    <ul>
      % for feature in features:
      <li>
        ${h.link(req, feature)}
        % if feature.contribution:
        (${h.link(req, feature.contribution)})
        % endif
      </li>
      % endfor
    </ul>
    % endif
  </div>
</%def>


% if ctx.description or ctx.comments or ctx.wikipedia_counterpart or ctx.sil_counterpart or ctx.croft_counterpart or ctx.quotation or ctx.references:
<dl class="concept-properties">
  % if ctx.description:
  <dt>Definition</dt>
  <dd>${ctx.description}</dd>
  % endif
  % if ctx.comments:
  <dt>Comments</dt>
  <dd>${ctx.comments}</dd>
  % endif
  % if ctx.croft_counterpart:
  <dt>Croft's comparative concept</dt>
  <dd>
    <strong>${h.external_link(ctx.croft_url, label=ctx.croft_counterpart) if ctx.croft_url else ctx.croft_counterpart}</strong>${':' if ctx.croft_definition else ''}
    % if ctx.croft_definition:
    ${ctx.croft_definition}
    % endif
  </dd>
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
  <dt>SIL Glossary</dt>
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
