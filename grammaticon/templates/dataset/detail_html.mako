<%inherit file="../home_comp.mako"/>

<%block name="head">
    <script src="${request.static_url('grammaticon:static/sigmajs/sigma.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.parsers.json.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.layout.forceAtlas2.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.renderers.edgeLabels.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.plugins.animate.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.plugins.dragNodes.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.layout.noverlap.min.js')}"></script>

    <style type="text/css">
        #container {
            max-width: 100%;
            height: 800px;
            margin: auto;
            margin-bottom: 1em;
        }
    </style>
</%block>


<h2>Welcome to grammaticon</h2>

<!--p class="lead">
    Abstract.
</p-->

<h4><a href="${req.route_url('concepts')}">Concepts</a></h4>
