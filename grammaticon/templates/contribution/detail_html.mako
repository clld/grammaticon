<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Contribution')}: ${ctx.name}</%block>
<%! import grammaticon.models as m %>

<h2>${_('Contribution')} ${ctx.name}</h2>

%if ctx.url:
<p><strong>URL:</strong> ${h.external_link(ctx.url)}</p>
%endif

${util.data()}

<% dt = request.get_datatable('features', m.Feature, contribution=ctx) %>
% if dt:
<div>
  ${dt.render()}
</div>
% endif
