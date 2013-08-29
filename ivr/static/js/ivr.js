$(function() {

    var id=1;

    add_node = function(icon, name, styles) {
        my_node = icon.clone()
                      .attr('id', name)
                      .removeClass("icon ui-draggable ui-draggable-dragging")
                      .addClass("dropped_icon node")
                      .css(styles);

        my_node.append("<div class='endpoint' id='" + 'ep_' + id + "'></div>");
        $("#ivr").append(my_node);

        if(my_node.hasClass("source"))
            add_endpoint(name, "source");

        if(my_node.hasClass("target"))
            add_endpoint(name, "target");

        if(my_node.hasClass("unique")) {
            $(".icon[action='" + my_node.attr("action") + "']")
                                           .draggable({ disabled: true });
        }

        jsPlumb.draggable(jsPlumb.getSelector('#' + name), {
             containment:"parent"
        });

        catch_action(name);

        id++;    
    }

    catch_action = function(node) {
        element = $('#' + node)
        action = element.attr("action");

        element.bind("contextmenu", function() {
            contextmenu(node);
        });

        switch(action) {
            case 'wait4digits':
                wait4digits(element);
            break;
            case 'prompts':
                prompts(element);
            break;
            case 'execute':
                execute(element);
            break;
        }
    }

    wait4digits = function(element) {
        element.bind("dblclick", function() {
            $('#wait4digits').dialog({
                title: 'Prompt for digits properties ...',
                bgiframe: true,
                modal: true,
                width: 600,
                height: 400,
                buttons : {'Cancel' : function() {
                                          $(this).dialog('close');
                                      },
                           'Save' : function() {
                              element.attr("config", "wait4digits");
                              element.attr("wait_prompt_path", $(this).find("input[name='wait_prompt_path']").val());
                              element.attr("wait_expected_digits", $(this).find("input[name='wait_expected_digits']").val());
                              element.attr("min_digits", $(this).find("input[name='min_digits']").val());
                              element.attr("max_digits", $(this).find("input[name='max_digits']").val());
                              element.attr("retries", $(this).find("input[name='retries']").val());
                              element.attr("retry_timeout", $(this).find("input[name='retry_timeout']").val());

                              $(this).dialog('close');
                                    }
                          }
            });
        });
    }


    whatdigit = function(info) {
        $("#on_what_digit").dialog({
            bgiframe: true,
            modal: true,
            width: 300,
            height: 200,
            title: 'On Digit Press...',
            buttons : {'Cancel' : function() {
                            $(this).dialog('close');
                      },
                       'Save' : function() {
                            info.connection.addOverlay(["Label", { location:0.1,
                                                                   id:"digit",
                                                                   cssClass:"aLabel",
                                                                   label : $(this).find("input[name='digit']").val()
                                                                 }
                                                       ]);
                            $(this).dialog('close');
                                }
                      }
        });
    }

    whatname = function() {
        $("#on_what_name").dialog({
            bgiframe: true,
            modal: true,
            width: 300,
            height: 200,
            title: 'Please enter name ...',
            buttons : {'Cancel' : function() {
                            $(this).dialog('close');
                      },
                       'Save' : function() {
                            $('#ivr').attr('name', $(this).find("input[name='name']").val());
                            $(this).dialog('close');
                            ivr_save();
                                }
                      }
        });
    }

    prompts = function(element) {
        element.bind("dblclick", function() {
            $("#prompts").dialog({
                bgiframe: true,
                modal: true,
                width: 500,
                height: 270,
                title: 'Prompt properties ...',
                buttons : { 'Cancel' : function() {
                                $(this).dialog('close');
                                       },
                            'Save' : function() {
                                element.attr("config", "prompts");
                                element.attr("prompt_path", $(this).find("input[name='prompt_path']").val());
                                element.attr("escape_digits", $(this).find("input[name='escape_digits']").val());

                                $(this).dialog('close');
                                     }
                          }
            });
        });
    }

    execute = function(element) {
        element.bind("dblclick", function() {
            $("#execute").dialog({
                bgiframe: true,
                modal: true,
                width: 500,
                height: 270,
                title: 'Execute properties ...',
                buttons : { 'Cancel' : function() {
                                $(this).dialog('close');
                                       },
                            'Save' : function() {
                                element.attr("config", "execute");
                                element.attr("application", $(this).find("input[name='application']").val());
                                element.attr("arguments", $(this).find("input[name='arguments']").val());

                                $(this).dialog('close');
                                     }
                          }
            });
        });
    }

    delete_connection = function(conn) {
        jsPlumb.deleteEndpoint(conn.endpoints[0].elementId, conn.endpoints[0]);
        jsPlumb.deleteEndpoint(conn.endpoints[1].elementId, conn.endpoints[1]);
        jsPlumb.detach(conn);
    }


    get_node_config = function(node) {
        my_elem = $("#" + node);
        elem = my_elem.attr("config");
        var config = Object();

        switch(elem) {
            case 'wait4digits':
                config.wait_prompt_path = my_elem.attr('wait_prompt_path');
                config.wait_expected_digits = my_elem.attr('wait_expected_digits');
                config.min_digits = my_elem.attr('min_digits');
                config.max_digits = my_elem.attr('max_digits');
                config.retries = my_elem.attr('retries');
                config.retry_timeout = my_elem.attr('retry_timeout');
                return config;
            break;

            case 'prompts':
                config.prompt_path = my_elem.attr('prompt_path');
                config.escape_digits = my_elem.attr('escape_digits');
                return config;
            break;

            case 'execute':
                config.application = my_elem.attr('application');
                config.arguments = my_elem.attr('arguments');
                return config;
            break;

        }
    }

    ivr_save = function() {
        var elems = $('#ivr').find('div[class*="node"]');

        if ($('#ivr').attr('name') != undefined) {
            ivr_name = $('#ivr').attr('name');
        } else {
            whatname();
            return false;
        }

        if (elems.length == 0) {
            alert('Please add elements before saving ...');
            return false;
        }

        var blocks = []
        $("#ivr .node").each(function (idx, elem) {
            var $elem = $(elem);
            blocks.push({
                id: $elem.attr('id'),
                action: $elem.attr('action'),
                positionX: parseInt($elem.css("left"), 10),
                positionY: parseInt($elem.css("top"), 10),
                config: get_node_config($elem.attr('id'))
            });
        });

        var connections = [];
        $.each(jsPlumb.getConnections(), function (idx, connection) {
            if (connection.getOverlay('digit'))
                digit = connection.getOverlay('digit').getLabel();
            else
                digit = null
            connections.push({
                connectionId: connection.id,
                sourceId: connection.sourceId,
                targetId: connection.targetId,
                digitId: digit
            });
        });

        j = JSON.stringify({ 'name': ivr_name,
                             'blocks' : blocks,
                             'connections' : connections
                           });

        $('#dialog').text('Ivr ' + ivr_name + ' has been saved !');
        $('#dialog').dialog({ title: 'Saving ...',
                              hide: {effect: "fadeOut", duration: 500},
                              open: function(event, ui) {
                                        setTimeout(function(){
                                            $('#dialog').dialog('close');                
                                        }, 300);
                                    }
        });

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: j,
            dataType: 'json',
            url: '/ivr/save',
            success: function (e) {
                console.log(e);
            }
        });
    }

    ivr_load = function(name) {
        nodes = $.parseJSON($("#nodes").attr("data"));
        connections = $.parseJSON($("#connections").attr("data"));

        $.each(nodes, function(index, value) {
            id = value.id.toString().substr(4);
            styles = { position: "absolute",
                       top: value.positionY +"px",
                       left: value.positionX + "px"
                     };
            icon = $(".icon[action='"+ value.action +"']");

            add_node(icon, value.id, styles);

            console.log(value.config);

        });

        $.each(connections, function(index, value) {
            digit = value.digitId;
            my_label = value.sourceId.substring(4) + "-" + value.targetId.substring(4);
            c = jsPlumb.connect({ 'source' : value.sourceId,
                                  'target': value.targetId,
                                });

            label = c.getOverlay("label");
            label.setLabel(my_label);
            if (digit != null) {
                c.addOverlay(["Label", { location:0.1,
                                         id:"digit",
                                         cssClass:"aLabel",
                                         label : digit
                                       }
                             ]);
            }
        });

        id++;
    }

    ivr_reset = function() {
        $("#reset").dialog({
             bgiframe: true,
             modal: true,
             width: 300,
             height: 200,
             title: 'Confirm reset ...',
             buttons : { 'Cancel' : function() {
                                        $(this).dialog('close');
                                    },
                         'Reset' : function() {
                                       jsPlumb.deleteEveryEndpoint();
                                       $(".dropped_icon").remove();
                                       $(".icon").draggable('enable');
                                       id=1;
                                       $(this).dialog('close');
                                   }
             }
        });
    }

    contextmenu = function(elementId) {
        $(document).contextmenu({
            delegate: ".node",
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
        connection.getOverlay("label").setLabel(connection.sourceId.substring(4) + "-" + connection.targetId.substring(4));
        connection.bind("editCompleted", function(o) {
    	    if (typeof console != "undefined")
    	        console.log("connection edited. path is now ", o.path);
    	});
    };

    endpoint_max_conn = function(elem) {
        switch(elem) {
            case 'wait4digits':
                maxconn = -1;
                break;
            default:
                maxconn = 1;
        }

        return maxconn;
    }

    add_endpoint = function(name, type) {
        elem = $("#" + name).attr("action");

        switch(type) {
            case 'source':
                endpointOptions = {
		    parent:name,
                    isSource:true,
	            anchor:"Continuous",
                    connector:[ "Flowchart", {  } ],
                    connectorStyle:{ strokeStyle:"#5c96bc", lineWidth:2, outlineColor:"transparent", outlineWidth:4 },
	            maxConnections: endpoint_max_conn(elem),
		    onMaxConnections:function(info, e) {
		        alert("Maximum connections (" + info.maxConnections + ") reached");
		    }
                }

                jsPlumb.makeSource('ep_' + id, endpointOptions);
                break;
            case 'target':
                endpointOptions = {
                    isTarget:true,
                    connector:[ "Flowchart", {  } ],
		    anchor:"Continuous",
                    maxConnections:-1
                }

                jsPlumb.makeTarget(name, endpointOptions);
                break;
        }
    };

    jsPlumb.importDefaults({
        Endpoint : ["Dot", {radius:2}],
        ConnectionsDetachable:false,
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


    jsPlumb.bind("endpointClick", function(endpoint, originalEvent) {
        console.log("endpointclick" + endpoint);
    });

    jsPlumb.bind("connection", function(connInfo, originalEvent) {

        if(connInfo.connection.sourceId == connInfo.connection.targetId) {
            console.log ("source and target ids are same");
            jsPlumb.detach(connInfo.connection);
        }

        init(connInfo.connection);

        if($('#' + connInfo.connection.sourceId).attr('action') == "wait4digits") {
            current_connection = connInfo.connection;
            whatdigit(connInfo);
        }
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

    $(".icon").draggable({
        helper:'clone'
    });

    $(".save").click(function() {
        ivr_save();
    });

    $(".reset").click(function() {
        ivr_reset();
    });

    $("#ivr").droppable({
        accept: ".icon",
        drop: function(event, ui) { 
                  add_node(ui.helper, 'node' + id, {position: '' });
              }
    });

    if ($("#ivr").attr("action") == "edit") {
        name = $("#ivr").attr("name");
        ivr_load(name);
    }

});
