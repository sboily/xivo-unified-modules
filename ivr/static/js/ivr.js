var f = 8;
function addState() {
//$('html').dblclick(function(e) {
    var obj = new Date();
    var newState = $('<div>').attr('id', 'window' + f).addClass('window').appendTo('#ivr');
    var title = $('<p>').text('Window ' + f);

    //newState.css({
    //   'top': e.pageY,
    //   'left': e.pageX
    //});

    _addEndpoints('window' + f, ["TopCenter", "BottomCenter"], ["LeftMiddle", "RightMiddle"]);			
    jsPlumb.draggable($(newState), {
        containment:"parent"
    });

    newState.append(title);
    $('#ivr').append(newState);

    f++;    
//});  
};

jsPlumb.importDefaults({
    DragOptions : { cursor: 'pointer', zIndex:2000 },
    EndpointStyles : [{ fillStyle:'#225588' }, { fillStyle:'#558822' }],
    Endpoints : [ [ "Dot", {radius:7} ], [ "Dot", { radius:11 } ]],
    ConnectionOverlays : [[ "Arrow", { location:1 } ],
    		      [ "Label", { location:0.1,
    				   id:"label",
    				   cssClass:"aLabel"
    		      }]
    		     ]
});		

// this is the paint style for the connecting lines..
var connectorPaintStyle = {
    lineWidth:4,
    strokeStyle:"#deea18",
    joinstyle:"round",
    outlineColor:"#eaedef",
    outlineWidth:2
    },

// .. and this is the hover style. 
connectorHoverStyle = {
    lineWidth:4,
    strokeStyle:"#5C96BC",
    outlineWidth:2,
    outlineColor:"white"
    },

endpointHoverStyle = {fillStyle:"#5C96BC"},

// the definition of source endpoints (the small blue ones)
sourceEndpoint = {
    endpoint:"Dot",
    paintStyle:{ 
    	strokeStyle:"#1e8151",
    	fillStyle:"transparent",
    	radius:7,
    	lineWidth:2 
    },				
    isSource:true,
    connector:[ "Flowchart", { stub:[40, 60], gap:10, cornerRadius:5, alwaysRespectStubs:true } ],								                
    connectorStyle:connectorPaintStyle,
    hoverPaintStyle:endpointHoverStyle,
    connectorHoverStyle:connectorHoverStyle,
    dragOptions:{},
    overlays:[[ "Label", { location:[0.5, 1.5], 
                           label:"Out",
                           cssClass:"endpointSourceLabel"}]
             ]
    },

// the definition of target endpoints (will appear when the user drags a connection) 
targetEndpoint = {
    endpoint:"Dot",					
    paintStyle:{ fillStyle:"#1e8151",radius:11 },
    hoverPaintStyle:endpointHoverStyle,
    maxConnections:-1,
    dropOptions:{ hoverClass:"hover", activeClass:"active" },
    isTarget:true,			
   overlays:[["Label", { location:[0.5, -0.5],
                          label:"In", 
                          cssClass:"endpointTargetLabel" }]
             ]
    },			

init = function(connection) {
    connection.getOverlay("label").setLabel(connection.sourceId.substring(6) + "-" + connection.targetId.substring(6));
    connection.bind("editCompleted", function(o) {
    	if (typeof console != "undefined")
    		console.log("connection edited. path is now ", o.path);
    	});
};			

 _addEndpoints = function(toId, sourceAnchors, targetAnchors) {
    for (var i = 0; i < sourceAnchors.length; i++) {
    	var sourceUUID = toId + sourceAnchors[i];
    	jsPlumb.addEndpoint(toId, sourceEndpoint, { anchor:sourceAnchors[i], uuid:sourceUUID });						
    	}
    for (var j = 0; j < targetAnchors.length; j++) {
    	var targetUUID = toId + targetAnchors[j];
    	jsPlumb.addEndpoint(toId, targetEndpoint, { anchor:targetAnchors[j], uuid:targetUUID });						
    	}
    };

// listen for new connections; initialise them the same way we initialise the connections at startup.
jsPlumb.bind("connection", function(connInfo, originalEvent) { 
    init(connInfo.connection);
});			

// listen for clicks on connections, and offer to delete connections on click.
jsPlumb.bind("click", function(conn, originalEvent) {
    if (confirm("Delete connection from " + conn.sourceId + " to " + conn.targetId + "?"))
    	jsPlumb.detach(conn); 
});	
    
jsPlumb.bind("connectionDrag", function(connection) {
    console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
});		
    
jsPlumb.bind("connectionDragStop", function(connection) {
    console.log("connection " + connection.id + " was dragged");
});

jsPlumb.bind("ready", function() {
    _addEndpoints($(".window"), ["TopCenter", "BottomCenter"], ["LeftMiddle", "RightMiddle"]);			
    jsPlumb.draggable($(".window"), {
        containment:"parent"
    });
});

// connect a few up
//jsPlumb.connect({uuids:["window2BottomCenter", "window3TopCenter"], editable:true});
//jsPlumb.connect({uuids:["window2LeftMiddle", "window4LeftMiddle"], editable:true});
//jsPlumb.connect({uuids:["window4TopCenter", "window4RightMiddle"], editable:true});
//jsPlumb.connect({uuids:["window3RightMiddle", "window2RightMiddle"], editable:true});
//jsPlumb.connect({uuids:["window4BottomCenter", "window1TopCenter"], editable:true});
//jsPlumb.connect({uuids:["window3BottomCenter", "window1BottomCenter"], editable:true});
