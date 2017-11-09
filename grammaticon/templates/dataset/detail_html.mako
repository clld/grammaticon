<%inherit file="../home_comp.mako"/>

<%block name="head">
    <script src="${request.static_url('grammaticon:static/sigmajs/sigma.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.parsers.json.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.layout.forceAtlas2.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.renderers.edgeLabels.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.plugins.animate.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.plugins.dragNodes.min.js')}"></script>
    <script src="${request.static_url('grammaticon:static/sigmajs/plugins/sigma.layout.noverlap.js')}"></script>

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

<div id="container"> </div>

<script>
sigma.parsers.json(
    '${request.route_url("relations")}',
    {
      container: 'container',
      settings: {
        defaultNodeColor: '#006400',
        labelSize: 'fixed',
        defaultEdgeType: 'arrow',
        edgeLabelSize: 'fixed',
        labelThreshold: 4,
        labelSizeRatio: 4,
        edgeLabelThreshold: 0.01,
        defaultLabelSize: 14,
          minArrowSize: 3,
        defaultEdgeLabelSize: 4,
        drawEdgeLabels: false,
        minEdgeSize: 2,
        maxEdgeSize: 3
      }
    },
    function(s) {
      for (var i=0,edge; edge=s.graph.edges()[i]; i++) {
        edge['color'] = '#222222';
        edge['arrow'] = 'target';
      }
      /*
      for (var i=0,node; node=s.graph.nodes()[i]; i++) {
        if (node['label'] == 'SIBLING') {
          node['color'] = '#DC143C';
          node['size'] = 1.5;
        }
      }
      */
      var noverlapListener = s.configNoverlap({
        nodeMargin: 10,
        scaleNodes: 10.05,
        gridSize: 1750,
        easing: 'quadraticInOut',
        duration: 500
      });
      // Bind the events:
      noverlapListener.bind('start stop interpolate', function(e) {
        console.log(e.type);
        if(e.type === 'start') {
          console.time('noverlap');
        }
        if(e.type === 'interpolate') {
          console.timeEnd('noverlap');
        }
      });
      s.startForceAtlas2();
      setTimeout(function() {s.killForceAtlas2();}, 1000);
      var dragListener = sigma.plugins.dragNodes(s, s.renderers[0]);
      dragListener.bind('startdrag', function(event) {
        console.log(event);
      });
      dragListener.bind('drag', function(event) {
        console.log(event);
      });
      dragListener.bind('drop', function(event) {
        console.log(event);
      });
      dragListener.bind('dragend', function(event) {
        console.log(event);
      });
    }
);
</script>
