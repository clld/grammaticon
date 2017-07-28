<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Metafeature: ${ctx.name}</%block>

<%def name="sidebar()">
    <%util:well title="Related concepts">
        <ul>
            % for ca in ctx.concept_assocs:
                <li>${h.link(req, ca.concept)}</li>
            % endfor
        </ul>
    </%util:well>
</%def>


<h2>Metafeature: ${ctx.name}</h2>

<h3>Features</h3>
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
