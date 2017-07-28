<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "values" %>
<%block name="title">Feature: ${ctx.name}</%block>

<%def name="sidebar()">
    <%util:well title="Featurelist">
        ${h.link(req, ctx.valueset.contribution)}<br/>
        by ${h.linked_contributors(req, ctx.valueset.contribution)}
    </%util:well>
</%def>


<h2>Feature: ${ctx.name}</h2>
<div>${u.md(ctx.description)|n}</div>
