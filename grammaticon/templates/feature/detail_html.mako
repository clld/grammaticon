<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "features" %>
<%block name="title">Feature: ${ctx.name}</%block>
<%! import grammaticon.models as m %>

<%def name="sidebar()">
  <div class="well">
    <h4>${_('Contribution')}</h4>
    ${h.link(req, ctx.contribution)}
    <%
      concepts = list(
        request.db.query(m.Concept)
        .join(m.ConceptFeature)
        .filter(m.ConceptFeature.feature_pk == ctx.pk)
        .distinct())
    %>
    % if concepts:
      <h4>Related Grammaticon concepts</h4>
    <ul>
      % for concept in concepts:
      <li>${h.link(req, concept)}</li>
      % endfor
    </ul>
    % endif
  </div>
</%def>

<h2>Feature: ${ctx.name}</h2>

%if ctx.url or ctx.description or ctx.comment:
<dl>
  %if ctx.url:
  <dt>Feature URL:</dt>
  <dd>${h.external_link(ctx.url)}</dd>
  %endif
  %if ctx.description:
  <dt>Description</dt>
  <dd>${u.md(ctx.description)|n}</dd>
  %endif
  %if ctx.comment:
  <dt>Relation to Grammaticon concepts</dt>
  <dd>${u.md(ctx.comment)|n}</dd>
  %endif
</dl>
%endif
