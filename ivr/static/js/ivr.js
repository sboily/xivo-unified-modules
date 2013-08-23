$(function() {

    var id=1;

    $(".icon").draggable({
        helper:'clone'
    });

    $("#ivr").droppable({
        accept: ".icon",
        drop: function( event, ui ) {

             var newStep = $(ui.helper).clone()
                                        .removeClass("icon ui-draggable ui-draggable-dragging")
                                        .attr('id', 'window' + id)
                                        .addClass("dropped_icon")
                                        .addClass('window')
                                        .css('position','');
             $(newStep).append("<div class='endpoint' id='" + 'ep_' + id + "'></div>");
             $(this).append($(newStep));

            if($(newStep).hasClass("source"))
                _addEndpoints(id, "source");

            if($(newStep).hasClass("target"))
                _addEndpoints(id, "target");

            if($(newStep).hasClass("unique")) {
                $(".icon[action='" + $(newStep).attr("action") + "']")
                                                .draggable({ disabled: true });
            }

            jsPlumb.draggable(jsPlumb.getSelector('#window' + id), {
                containment:"parent"
            });

            catch_action('window' + id);
            id++;    
        }
    });

    catch_action = function(step) {
        element = $('#' + step)
        action = element.attr("action");

        $('#' + step).bind("contextmenu", function() {
            contextmenu(step);
        });

        switch(action) {
            case 'wait4digits':
                wait4digits(element);
            break;
        }
    }

    wait4digits = function(element) {
        element.bind("dblclick", function() {
            $('#wait4digits').dialog({title: 'Prompt for digits properties ...'});
        });
    }

    delete_connection = function(conn) {
        jsPlumb.deleteEndpoint(conn.endpoints[0].elementId, conn.endpoints[0]);
        jsPlumb.deleteEndpoint(conn.endpoints[1].elementId, conn.endpoints[1]);
        jsPlumb.detach(conn);
    }

    save_ivr = function() {
        var conns = jsPlumb.getConnections();
        var connection = Object();

        for(i = 0; i < conns.length; i++) {
            sourceid = conns[i].sourceId;
            targetid = conns[i].targetId;

            connection[i] = Object();
            connection[i].sourceid = sourceid;
            connection[i].targetid = targetid;
        }

        connection.length = conns.length;

        $('#dialog').text(JSON.stringify(connection));
        $('#dialog').dialog({title: 'Saving ...'});
    }

    contextmenu = function(elementId) {
        console.log(elementId);
        $(document).contextmenu({
            delegate: ".window",
            preventSelect: true,
            taphold: true,
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


    init = function(connection) {
        connection.getOverlay("label").setLabel(connection.sourceId.substring(6) + "-" + connection.targetId.substring(6));
        connection.bind("editCompleted", function(o) {
    	    if (typeof console != "undefined")
    	        console.log("connection edited. path is now ", o.path);
    	});
    };			

    _addEndpoints = function(id, type) {
        switch(type) {
            case 'source':
                jsPlumb.makeSource('ep_' + id, {
		    parent:"window" + id,
		    anchor:"Continuous",
                    connector:[ "Flowchart", {  } ],
		    connectorStyle:{ strokeStyle:"#5c96bc", lineWidth:2, outlineColor:"transparent", outlineWidth:4 },
		    maxConnections:1,
		    onMaxConnections:function(info, e) {
		        alert("Maximum connections (" + info.maxConnections + ") reached");
		    }
	        });
                break;
            case 'target':
                jsPlumb.makeTarget('window' + id, {
                    connector:[ "Flowchart", {  } ],
		    anchor:"Continuous",
                    maxConnections:-1
		});
            break;
        }
    };

    jsPlumb.importDefaults({
        Endpoint : ["Dot", {radius:2}],
        HoverPaintStyle : {strokeStyle:"#1e8151", lineWidth:2 },
        ConnectionOverlays : [[ "Arrow", { location:1,
                                           id:"arrow",
                                           length:14,
                                           foldback:0.8
                                         }],
                              [ "Label", { label:"Connexion",
                                           id:"label",
                                           cssClass:"aLabel" }]
                             ]
    });

    $(".save").click(function() {
        save_ivr();
    });

    jsPlumb.bind("endpointClick", function(endpoint, originalEvent) {
        console.log("endpointclick" + endpoint);
    });

    jsPlumb.bind("jsPlumbConnection", function(info, originalEvent) {
        console.log("jsPlumbConnection" + info);
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
