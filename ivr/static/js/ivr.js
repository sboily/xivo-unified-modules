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
                add_endpoint(id, "source");

            if($(newStep).hasClass("target"))
                add_endpoint(id, "target");

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
            case 'prompts':
                prompts(element);
            break;
        }
    }

    wait4digits = function(element) {
        element.bind("dblclick", function() {
            $('#wait4digits').dialog({title: 'Prompt for digits properties ...'});
        });
    }

    prompts = function(element) {
        element.bind("dblclick", function() {
            $('#prompts').dialog({title: 'Fill prompt name ...'});
        });
    }

    delete_connection = function(conn) {
        jsPlumb.deleteEndpoint(conn.endpoints[0].elementId, conn.endpoints[0]);
        jsPlumb.deleteEndpoint(conn.endpoints[1].elementId, conn.endpoints[1]);
        jsPlumb.detach(conn);
    }

    save_ivr = function() {
        var connection = Object();
        var elems = $('#ivr').find('div[class*="window"]');
        var c = 0;

        elems.each(function() {
            var e = $(this);
            var my_id = e.attr('id');
            var my_action = e.attr('action');
            var conns_source = jsPlumb.getConnections({source:my_id});
            var conns_target = jsPlumb.getConnections({target:my_id});

            connection[c] = Object();
            connection[c].id = my_id;
            connection[c].action = my_action;

            if (conns_source.length == 1) {
                connection[c].source_sourceid = conns_source[0].sourceId;
                connection[c].source_targetid = conns_source[0].targetId;
            }

            if (conns_target.length == 1) {
                connection[c].target_sourceid = conns_target[0].sourceId;
                connection[c].target_targetid = conns_target[0].targetId;
            }

            c++;
        });

        connection.length = connection.length;
        console.log(connection);

        $('#dialog').text(JSON.stringify(connection));
        $('#dialog').dialog({title: 'Saving ...'});

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(connection),
            dataType: 'json',
            url: '/ivr/save',
            success: function (e) {
                console.log(e);
            }
        });
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

    add_endpoint = function(id, type) {
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
