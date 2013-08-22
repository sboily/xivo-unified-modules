$(function() {

    var id=1;

    $(".icon").draggable({
        helper:'clone'
    });

    $("#ivr").droppable({
        accept: ".icon",
        drop: function( event, ui ) {

             var newState = $(ui.helper).clone()
                                        .removeClass("icon ui-draggable ui-draggable-dragging")
                                        .attr('id', 'window' + id)
                                        .addClass("dropped_icon")
                                        .addClass('window')
                                        .css('position','');
             $(this).append($(newState));

            if($(newState).hasClass("source"))
                _addEndpoints($(newState), ["RightMiddle"], []);


            if($(newState).hasClass("target"))
                _addEndpoints($(newState), [], ["LeftMiddle"]);

            if($(newState).hasClass("unique")) {
                $(".icon[action='" + $(newState).attr("action") + "']")
                                                .draggable({ disabled: true });
            }

            jsPlumb.draggable($(newState), {
                containment:"parent"
            });

            id++;    
        }
    });

    function delete_connection(conn) {
        jsPlumb.deleteEndpoint(conn.endpoints[0].elementId, conn.endpoints[0]);
        jsPlumb.deleteEndpoint(conn.endpoints[1].elementId, conn.endpoints[1]);
        jsPlumb.detach(conn);
    }

    function contextmenu(elementId) {
        $(this).contextmenu({
            menu: [
                {title: "Delete", cmd: "delete", uiIcon: "ui-icon-trash"},
                ],
            select: function(event, ui) {
                switch(ui.cmd) {
                    case 'delete':
                        var source_conns = jsPlumb.getConnections({
                                               source:elementId
                                           });
                        for(i = 0; i < source_conns.length; i++) {
                            delete_connection(source_conns[i]);
                        }
                        var target_conns = jsPlumb.getConnections({
                                               target:elementId
                                           });
                        for(i = 0; i < target_conns.length; i++) {
                            delete_connection(target_conns[i]);
                        }
                        if($("#" + elementId).hasClass("unique")) {
                            $(".icon[action='" + $("#" + elementId).attr("action") + "']")
                                                                   .draggable({ disabled: false });
                        }
                        jsPlumb.remove(elementId);
                        $("#" + elementId).remove();
                    break;
                }
            }
        });
    };

    jsPlumb.importDefaults({
        DragOptions : { cursor: 'pointer', zIndex:2000 },
        EndpointStyles : [{ fillStyle:'#225588' }, { fillStyle:'#558822' }],
        Endpoints : [ [ "Dot", { radius:3 } ], [ "Dot", { radius:3 } ]],
        ConnectionOverlays : [[ "Arrow", { location:1 } ],
    		              [ "Label", { location:0.1,
    				           id:"label",
    				           cssClass:"aLabel"
    		              }]
    		             ]
     });		

    var connectorPaintStyle = {
        lineWidth:4,
        strokeStyle:"#deea18",
        joinstyle:"round",
        outlineColor:"#eaedef",
        outlineWidth:2
    },

    connectorHoverStyle = {
        lineWidth:4,
        strokeStyle:"#5C96BC",
        outlineWidth:2,
        outlineColor:"white"
    },

    endpointHoverStyle = {fillStyle:"#5C96BC"},

    sourceEndpoint = {
        endpoint:"Dot",
        paintStyle:{ 
            strokeStyle:"#1e8151",
    	    fillStyle:"transparent",
    	    radius:7,
    	    lineWidth: 1
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

    targetEndpoint = {
        endpoint:"Dot",
        paintStyle:{ fillStyle:"#1e8151",radius:8 },
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

    jsPlumb.bind("contextmenu", function(endpoint) {
        contextmenu(endpoint.elementId);
    });

    jsPlumb.bind("endpointClick", function(endpoint) {
    });

    jsPlumb.bind("connection", function(connInfo, originalEvent) {
        init(connInfo.connection);
    });

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

});

// connect a few up
//jsPlumb.connect({uuids:["window2BottomCenter", "window3TopCenter"], editable:true});
//jsPlumb.connect({uuids:["window2LeftMiddle", "window4LeftMiddle"], editable:true});
//jsPlumb.connect({uuids:["window4TopCenter", "window4RightMiddle"], editable:true});
//jsPlumb.connect({uuids:["window3RightMiddle", "window2RightMiddle"], editable:true});
//jsPlumb.connect({uuids:["window4BottomCenter", "window1TopCenter"], editable:true});
//jsPlumb.connect({uuids:["window3BottomCenter", "window1BottomCenter"], editable:true});
