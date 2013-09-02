$(function() {

    var id=1;
    var node_config = Object();

    $.each($('.nodes_config').children('.node_config'), function( index ) {
        node_config[this.id] = Object();
        node_config[this.id].title = $(this).attr('title');
        node_config[this.id].height = $(this).attr('height');
        node_config[this.id].width = $(this).attr('width');
        my_node_config = node_config[this.id].config = Object()
        $.each($('#' + this.id + " :input"), function(i) {
            my_node_config[i] = $(this).attr('name');
        });
    });

    add_node = function(icon, name, styles) {
        my_node = icon.clone()
                      .attr('id', name)
                      .removeClass("icon ui-draggable ui-draggable-dragging")
                      .addClass("dropped_icon node")
                      .css(styles);

        my_node.append("<div class='endpoint' id='" + 'ep_' + id + "'></div>");
        $("#ivr").append(my_node);

        if (my_node.hasClass("source"))
            add_endpoint(name, "source");

        if (my_node.hasClass("target"))
            add_endpoint(name, "target");

        if (my_node.hasClass("unique")) {
            $(".icon[action='" + my_node.attr("action") + "']")
                                        .draggable({ disabled: true });
        }

        jsPlumb.draggable(jsPlumb.getSelector('#' + name), {
            containment:"parent"
        });

        catch_action(name);

        id++;    
    }

    add_popover = function(name) {
        my_node = $('#' + name);
        my_desc = my_node.attr("description");

        if (my_desc.length == 0) {
            my_node.popover("destroy");
            return true;
        }

        if(my_desc != undefined)
            my_desc = '<i class="icon-comment"></i> ' + my_desc;
        else
            my_desc = '<i class="icon-comment"></i> No information';

        my_node.popover({ placement: 'top',
                          trigger: 'hover',
                          animation: true,
                          html: true,
                          delay: { show: 0, hide: 100 },
                          title: name
                        });

        my_node.data('popover').options.content = my_desc;
    }

    catch_action = function(node) {
        element = $('#' + node)
        action = element.attr("action");
        config = {};
        input = [];

        element.bind("contextmenu", function() {
            contextmenu(node);
        });

        try {
            $.each(node_config[action]["config"], function (i) {
                attribute = node_config[action]["config"][i];
                input.push(attribute);
            });

            config = { title: node_config[action].title,
                       width: node_config[action].width,
                       height: node_config[action].height,
                       name: action,
                       input: input
                     }

        } catch(e) {
            console.log("This node hasn't configuration : " + node);
        }

        if (config)
            edit_node_config(element, config);
    }

    whatdigit = function(conn) {
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
                            conn.addOverlay(["Label", { location:0.1,
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

    delete_connection = function(conn) {
        jsPlumb.deleteEndpoint(conn.endpoints[0].elementId, conn.endpoints[0]);
        jsPlumb.deleteEndpoint(conn.endpoints[1].elementId, conn.endpoints[1]);
        jsPlumb.detach(conn);
    }

    edit_node_config = function(element, config) {
        element.bind("dblclick", function() {

            $.each(config.input, function(index, value) {
                $('#' + config.name + " :input[name='" + value + "']").val(element.attr(value));
            });

            $("#" + config.name).dialog({
                bgiframe: true,
                modal: true,
                width: config.width,
                height: config.height,
                title: config.name + ' properties ...',
                buttons : { 'Cancel' : function() {
                                $(this).dialog('close');
                                       },
                            'Save' : function() {
                                element.attr("config", config.name);
                                $.each(config.input, function(index, value) {
                                    element.attr(value, $("#" + config.name).find(":input[name='" + value + "']").val());
                                });

                                ivr_save();
                                add_popover(element[0].id);

                                $(this).dialog('close');
                                     }
                          }
            });
        });
    }

    set_node_config = function(value) {
        node = value.id;
        config = value.config;
        $.each(config, function(index, value) {
            $('#' + node).attr(index, value);
        });
    }

    get_node_config = function(node) {
        my_elem = $("#" + node);
        elem = my_elem.attr("config");
        var config = Object();

        try {
            $.each(node_config[elem]["config"], function (i) {
                attribute = node_config[elem]["config"][i];
                config[attribute] = my_elem.attr(attribute);
            });
        } catch(e) {
            console.log("This node hasn't configuration : " + node);
        }

        return config;
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

        var nodes = []
        $("#ivr .node").each(function (idx, elem) {
            var $elem = $(elem);
            nodes.push({
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
                             'nodes' : nodes,
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

            if (value.config) {
                $('#' + value.id).attr('config', value.action);
                set_node_config(value);
            }

            if ($('#' + value.id).attr('description')) {
                add_popover(value.id);
            }

        });

        $.each(connections, function(index, value) {
            digit = value.digitId;
            my_label = value.sourceId.substring(4) + "-" + value.targetId.substring(4);
            c = jsPlumb.connect({ 'source' : value.sourceId,
                                  'target': value.targetId,
                                });

            c.removeOverlay("label");

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

    $(".icon").draggable({
        helper:'clone'
    });

    if ($("#ivr").attr("action") == "edit") {
        name = $("#ivr").attr("name");
        ivr_load(name);
    }

    jsPlumb.bind("connection", function(conn) {
        my_conn = conn.connection;
        my_source = conn.sourceId;
        my_target = conn.targetId;

        if(my_source == my_target) {
            console.log ("source and target ids are same !");
            jsPlumb.detach(my_conn);
        }

        my_conn.removeOverlay("label");

        if($('#' + my_source).attr('action') == "wait4digits") {
            whatdigit(my_conn);
        }
    });

    jsPlumb.bind("click", function(conn) {
        if (confirm("Delete connection from " + conn.sourceId + " to " + conn.targetId + "?"))
    	    jsPlumb.detach(conn);
    });

    jsPlumb.bind("connectionDrag", function(conn) {
        console.log("connection " + conn.id + " is being dragged.");
    });
    
    jsPlumb.bind("connectionDragStop", function(conn) {
        console.log("connection " + conn.id + " was dragged");
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

});
