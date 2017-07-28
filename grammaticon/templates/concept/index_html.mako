<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "concepts" %>
<%block name="title">Concepts</%block>

<h2>Concepts</h2>
${ctx.render()}