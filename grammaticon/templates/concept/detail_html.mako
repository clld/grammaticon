<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "concepts" %>
<%block name="title">Concept: ${ctx.name}</%block>


<h2>Concept: ${ctx.name}</h2>
<p>
    ${ctx.description}
</p>
<dt>
    % for o in ['GOLD', 'ISOCAT']:
        % if getattr(ctx, o + '_counterpart'):
            <dt>${o}</dt>
            <dd>
                ${h.external_link(getattr(ctx, o + '_URL'), label=getattr(ctx, o + '_counterpart'))}
                % if getattr(ctx, o + '_comments'):
                    (${getattr(ctx, o + '_comments')})
                % endif
            </dd>
        % endif
    % endfor
</dt>

% if ctx.metafeature_assocs:
    <h4>Related metafeatures:</h4>
    <ul>
        % for ca in ctx.metafeature_assocs:
            <li>${h.link(req, ca.metafeature)}</li>
        % endfor
    </ul>
% endif

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
