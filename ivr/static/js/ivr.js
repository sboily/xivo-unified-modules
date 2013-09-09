$(function() {

    var id=1;
    var node_config = Object();
    var ivr_name_edit = false;
    var sUsrAg = navigator.userAgent;

    if (sUsrAg.indexOf("Firefox") == -1) 
        alert("Only the latest firefox is supported with this module !");

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
        var comment = false;

        my_node = icon.clone()
                      .attr('id', name)
                      .removeClass("icon ui-draggable ui-draggable-dragging")
                      .addClass("dropped_icon node")
                      .css(styles);

        if (my_node.attr('action') == 'comment') {
            my_node.find("img").remove();
            my_node.append("<textarea id='textarea-comment'></textarea>")
                   .addClass("comment");
            my_node.find("#textarea-comment").attr("cols", 50)
                                             .attr("rows", 6)
                                             .attr("placeholder", "Add comment here !")
                                             .css("resize", "none");
            comment = true;
        }

        my_node.append("<i class='btn-icon-only icon-remove node-icon-action-remove'>");
        if (node_config[my_node.attr("action")])
            my_node.append("<i class='btn-icon-only icon-wrench node-icon-action-wrench'>");

        my_node.append("<div class='endpoint' id='" + 'ep_' + id + "'></div>");
        if (comment == true) {
            my_node.find(".endpoint").css("display", "none");
        }
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
            containment:"parent",
            grid: [ 10,10 ] 
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
        my_element = $('#' + node);
        my_node_close = $('#' + node + ' .node-icon-action-remove');
        my_node_action = my_element.attr("action");
        my_node_config = {};
        my_node_input = [];

        my_node_close.bind("click", function() {
            if (confirm("Delete node " + node + "?"))
                delete_node(node);
        });

        try {
            $.each(node_config[my_node_action]["config"], function (i) {
                attribute = node_config[my_node_action]["config"][i];
                my_node_input.push(attribute);
            });

            var my_node_config = { title: node_config[my_node_action].title,
                                   width: node_config[my_node_action].width,
                                   height: node_config[my_node_action].height,
                                   name: my_node_action,
                                   input: my_node_input
                                 }
        } catch(e) {
            console.log("This node hasn't configuration : " + node);
            return false;
        }

        if (my_node_config)
            edit_node_config(my_element, my_node_config, node);
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

    whattruefalse = function(conn) {
        $("#on_what_true_false").dialog({
            bgiframe: true,
            modal: true,
            width: 300,
            height: 200,
            title: 'On action true/false ...',
            buttons : {'Cancel' : function() {
                            $(this).dialog('close');
                      },
                       'Save' : function() {
                            conn.addOverlay(["Label", { location:0.1,
                                                        id:"action",
                                                        cssClass:"aLabel",
                                                        label : $(this).find("#my_action option:selected").val()
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
            width: 380,
            height: 250,
            title: 'Please enter name ...',
            buttons : {'Cancel' : function() {
                            $(this).dialog('close');
                      },
                       'Save' : function() {
                            $('#ivr').attr('name', $(this).find("input[name='name']").val());
                            $('#ivr').attr('context', $(this).find("input[name='context']").val());
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

    edit_node_config = function(element, my_node_config, node) {
        my_node_edit = $('#' + node + ' .node-icon-action-wrench');

        my_node_edit.bind("click", function() {

            $.each(my_node_config.input, function(index, value) {
                $('#' + my_node_config.name + " :input[name='" + value + "']").val(element.attr(value));
            });

            $("#" + my_node_config.name).dialog({
                bgiframe: true,
                modal: true,
                width: my_node_config.width,
                height: my_node_config.height,
                title: my_node_config.name + ' properties ...',
                buttons : { 'Cancel' : function() {
                                $(this).dialog('close');
                                       },
                            'Save' : function() {
                                element.attr("config", my_node_config.name);
                                $.each(my_node_config.input, function(index, value) {
                                    element.attr(value, $("#" + my_node_config.name).find(":input[name='" + value + "']").val());
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
        var is_edit = false;
        var old_name = false;

        if ($('#ivr').attr('name') != undefined) {
            ivr_name = $('#ivr').attr('name');
            old_name = $('#ivr').attr('old-name');
            is_edit = true;
        } else {
            whatname();
            return false;
        }

        context = $('#ivr').attr('context');

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

            if (connection.getOverlay('action'))
                action = connection.getOverlay('action').getLabel();
            else
                action = null

            connections.push({
                connectionId: connection.id,
                sourceId: connection.sourceId,
                targetId: connection.targetId,
                digitId: digit,
                action: action
            });
        });

        j = JSON.stringify({ 'name': ivr_name,
                             'context' : context,
                             'old_name' : old_name,
                             'is_edit' : is_edit,
                             'nodes' : nodes,
                             'connections' : connections
                           });

        $('#dialog').text('Ivr ' + ivr_name + ' has been saved !');
        $('#dialog').dialog({ title: 'Saving ...',
                              width: 300,
                              height: 100,
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
                if (e.action == 'add')
                    window.location = "/ivr/edit/" + e.id;
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
            action = value.action;
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

            if (action != null) {
                c.addOverlay(["Label", { location:0.1,
                                         id:"action",
                                         cssClass:"aLabel",
                                         label : action
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

    delete_node = function(node) {
        var source_conns = jsPlumb.getConnections({source:node});

        for(i = 0; i < source_conns.length; i++) {
            delete_connection(source_conns[i]);
        }

        var target_conns = jsPlumb.getConnections({target:node});

        for(i = 0; i < target_conns.length; i++) {
             delete_connection(target_conns[i]);
        }

        if ($("#" + node).hasClass("unique")) {
            $(".icon[action='" + $("#" + node).attr("action") + "']")
                                              .draggable({ disabled: false });
        }

        jsPlumb.remove(node);
        $("#" + node).remove();
    }

    contextmenu = function(node) {
        $(document).contextmenu({
            delegate: "#ivr",
            preventSelect: true,
            taphold: true,
        });
    };

    endpoint_max_conn = function(elem, type) {
        switch(type) {
            case 'source':
                maxconn = $("#" + elem).attr('maxconnsource')
                break;
            case 'target':
                maxconn = $("#" + elem).attr('maxconntarget')
                break;
            default:
                maxconn = 1;
        }

        if (maxconn != undefined)
            return maxconn;
        else
            return 1
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
	            maxConnections: endpoint_max_conn(elem, 'source'),
		    onMaxConnections:function(info, e) {
		        alert("Maximum connections source (" + info.maxConnections + ") reached");
		    }
                }

                jsPlumb.makeSource('ep_' + id, endpointOptions);
                break;
            case 'target':
                endpointOptions = {
                    isTarget:true,
                    connector:[ "Flowchart", {  } ],
		    anchor:"Continuous",
                    maxConnections: endpoint_max_conn(elem, 'target'),
		    onMaxConnections:function(info, e) {
		        alert("Maximum connections target (" + info.maxConnections + ") reached");
                    }
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

        if($('#' + my_source).attr('action') == "gotoif") {
            whattruefalse(my_conn);
        }

        if($('#' + my_source).attr('action') == "gotoiftime") {
            whattruefalse(my_conn);
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

    $("#ivr").bind("contextmenu", function() {
            contextmenu(node);
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

    $("#ivr_name").bind("click", function() {
        if (!ivr_name_edit) {
            old_name = $('#ivr').attr('name');
            context = $('#ivr').attr('context');
            $("#ivr_name p").replaceWith("<p>New name ? : <input type='text' placeholder='Press enter to save ...'></input></p>");
            ivr_name_edit = true;
            $("#ivr_name p").keypress(function(event) {
                if (event.keyCode == 13) {
                    new_name = $("#ivr_name input").val();
                    if (new_name) {
                        $('#ivr').attr('name', new_name);
                        $('#ivr').attr('old-name', old_name);
                        ivr_save();
                        $("#ivr_name p").replaceWith("<p>Name : " + new_name + " (" + context + ")</p>");
                    } else {
                        $("#ivr_name p").replaceWith("<p>Name : " + old_name + " (" + context + ")</p>");
                    }
                    ivr_name_edit = false;
                }
            });
        }
    });

});
