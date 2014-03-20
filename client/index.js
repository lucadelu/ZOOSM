var mapPanel,map,park,listLayer,selectControl,user = null,passwd = null;

//function to show help panel
function help(){
  //panel 
  valore=1; //it is used by panel to load different help pages
  var cent_help = new Ext.Panel({
      region: 'center',
      width: 470,
      height: 395,
      id: 'cent_help',
      autoLoad: "help/1.html",
      autoScroll: true,
      collapsible: false,
      bodyStyle: 'padding:5px;'
  });
  
  //window containing panel
  var win_help = new Ext.Window({
    title: 'Aiuto',
    items: [cent_help],
    closable: true,
    width: 480,
    height: 400,
    layout: 'border',
    buttons: [{
      text: 'Previous',
      disabled: true,
      id: 'prev',
      //function to load previous help page
      handler: function(){
	valore = valore - 1
	//if valore==1 the button is disabled because it is the first help page
	if (valore==1){
	  this.disable()
	}
	if (valore<2){
	  Ext.getCmp('next').enable()
	}
	//change the content of help page
	Ext.getCmp('cent_help').body.load("help/"+valore+".html")
      }
    },{
       //function to load next help page     
      text: 'Next',
      id: 'next',
      handler: function(){
	valore = valore + 1
	if (valore>1){
	  Ext.getCmp('prev').enable()
	}
	if (valore==2){
	  this.disable()  
	}
	//change the content of help page
	Ext.getCmp('cent_help').body.load("help/"+valore+".html")
      }
    },{
      text: 'Close',
      handler: function(){
	win_help.hide();
      }
    }]
  });
  //show help window
  win_help.show();  
};

//function to show the login form
function login(){
  
  var loginPanel = new Ext.FormPanel({
    labelWidth: 75,
    frame:true,
    region: 'center',     
    bodyStyle:'padding:5px 5px 0',
    width: 240,
    height: 140,
    defaultType: 'textfield',
    items: [{
	fieldLabel: 'Username',
	name: 'user',
	allowBlank:false
    },{
	fieldLabel: 'Password',
        inputType: 'password',
	name: 'passwd',
	allowBlank:false
    }] 
  })
  //window containing panel
  var win_login = new Ext.Window({
    title: 'Login',
    items: [loginPanel],
    closable: true,
    width: 250,    
    height: 150,
    layout: 'border',
    buttons: [{
      text: 'Login',
      handler: function(){
	//set the user and password value
	user = loginPanel.form.getValues().user
	passwd = loginPanel.form.getValues().passwd
	win_login.hide();	
      }
    },{
      text: 'Close',
      handler: function(){
	win_login.hide();
      }
    }] 
  });  
  //show help window
  win_login.show();   
  
};
//function to logout
function logout(){
  user = null
  passwd = null
}

//function to upload data on OpenStreetMap database
function upload(){
  //check if some features are selected
  if (listLayer.length == 0)
//       return Ext.MessageBox.alert('Error',"No feature selected!")
      return Ext.MessageBox.show({ 
	   title: 'Error',
           msg: 'No feature selected',
           buttons: Ext.MessageBox.WARNING,
	   icon: Ext.MessageBox.WARNING
      })
  //check if user and passwd variable are setted
  if ( (user == null) || (passwd == null) )
//       return Ext.MessageBox.alert('Error',"Please, you should login with your OpenStreetMap account")
      return Ext.MessageBox.show({ 
	   title: 'Error',
           msg: 'Please, you should login with your OpenStreetMap account',
           buttons: Ext.MessageBox.WARNING,
	   icon: Ext.MessageBox.WARNING
      })      
  //create the geojson variable to write the features list
  var geoJSON = new OpenLayers.Format.GeoJSON({internalProjection: map.projection, externalProjection: map.displayProjection})
  geoJSONText = geoJSON.write(listLayer)
  console.log(geoJSONText)
  
  url="http://lucadelu.org/cgi-bin/zoo_loader.cgi"
//   url += encodeURIComponent(geoJSONText)
//   url += ";username="+user+";password"+passwd+"&RawDataOutput=output"

  //create the url for wps service
  var params = '<wps:Execute service="WPS" version="1.0.0" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0/../wpsExecute_request.xsd">';
  params += '<ows:Identifier>zoosm</ows:Identifier>';
  params += '<wps:DataInputs>';
  params += '<wps:Input>';
  params += '<ows:Identifier>username</ows:Identifier>';
  params += '<wps:Data>';
  params += '<wps:LiteralData>'+ user +'</wps:LiteralData>';
  params += '</wps:Data>';
  params += '</wps:Input>';
  params += '<wps:Input>';
  params += '<ows:Identifier>password</ows:Identifier>';
  params += '<wps:Data>';
  params += '<wps:LiteralData>'+ passwd +'</wps:LiteralData>';
  params += '</wps:Data>';
  params += '</wps:Input>';
  params += '<wps:Input>';
  params += '<ows:Identifier>inputvector</ows:Identifier>';
  params += '<wps:Data>';
  params += '<wps:ComplexData mimeType="application/json"> '+ geoJSONText +' </wps:ComplexData>';
  params += '</wps:Data>';
  params += '</wps:Input>';
  params += '</wps:DataInputs>';
  params += '<wps:ResponseForm>';
  params += '<wps:RawDataOutput>';
  params += '<ows:Identifier>output</ows:Identifier>';
  params += '</wps:RawDataOutput>';
  params += '</wps:ResponseForm>';
  params += '</wps:Execute>';  

  var request = new OpenLayers.Request.XMLHttpRequest();
  request.open('POST',url,true);
  request.setRequestHeader('Content-Type','text/xml');
  request.onreadystatechange = function() {
    if(request.readyState == OpenLayers.Request.XMLHttpRequest.DONE) {
      console.log(request.responseText)
    }
  }
  request.send(params);
}


//   var request = new OpenLayers.Request.XMLHttpRequest();
//   request.open('GET',url,true);
//   request.onreadystatechange = function() {
//     if(request.readyState == OpenLayers.Request.XMLHttpRequest.DONE) {
// //       var GeoJSON = new OpenLayers.Format.GeoJSON();
//       console.log(request.responseText);
//       return Ext.MessageBox.show({ 
// 	   title: 'Output',
//            msg: request.responseText,
//            buttons: Ext.MessageBox.WARNING,
// 	   icon: Ext.MessageBox.WARNING
//       })
// //       hover.removeFeatures(hover.features);
// //       hover.addFeatures(features);
//     }
//   }
//   request.send();

  
//   listLayer = []
//   selectControl.unselectAll()
  
// };
//function to unselect all features
function unselect(){
  selectControl.unselectAll()
};

//main function
Ext.onReady(function() {
  OpenLayers.ProxyHost = "/cgi-bin/proxy.cgi?url=";
  Ext.QuickTips.init();
               
  //MAP#####################################################################
  //options for map
  var options = {
    controls:[
//       new OpenLayers.Control.OverviewMap(),
      new OpenLayers.Control.Permalink(),
      new OpenLayers.Control.MousePosition(),
      new OpenLayers.Control.ZoomBox(),
      new OpenLayers.Control.Attribution(),
      new OpenLayers.Control.Navigation(),
      new OpenLayers.Control.ScaleLine()
    ],
    displayProjection: new OpenLayers.Projection("EPSG:4326"),
    projection: new OpenLayers.Projection("EPSG:900913"),
    units: "m"
  };
  //start map
  map = new OpenLayers.Map(options);
  //add selected feature to feature list
  function onFeatureSelect(feature) {
      listLayer.push(feature);
  }
  //remove feature from layer list
  function onFeatureUnselect(feature) {
      for (var i = 0; i < listLayer.length; ++i) {
// 	console.log(feature.id)
// 	console.log(listLayer[i].id)
	if (listLayer[i].id == feature.id) {
	  listLayer.splice(i,1);
	  break;
	}
      }
  }  
  
  //BASE LAYER##############################################################
  //osm layer
  var osm = new OpenLayers.Layer.OSM();
  map.addLayer(osm);

  //OVERLAY LAYER###########################################################
  //set the listlayer variable to empty list
  listLayer = []
  //piemonte parks
  layer1 = new OpenLayers.Layer.GML("Piemonte Parks","data/parchi.json",{
    format: OpenLayers.Format.GeoJSON,
    projection: map.displayProjection,
    styleMap: new OpenLayers.StyleMap({
	'default': new OpenLayers.Style({
	    'fillColor': "ffffff",
	    'fillOpacity': "0.0",
	    'strokeColor':  "000000",
	    'strokeWidth':  "1"
	}),
	'select': new OpenLayers.Style({
	    'fillColor': "ffffff",
	    'fillOpacity': "0.0",
	    'strokeColor':  "ffff00",
	    'strokeWidth':  "2.0"
	}),	
    })
  })
  map.addLayer(layer1);   

  //add event on park layer
  layer1.events.on({
      "featureselected": function(e) {
	  onFeatureSelect(e.feature);
      },
      "featureunselected": function(e) {
	  onFeatureUnselect(e.feature);
      },
      "visibilitychanged": function() {
	  console.log(layer1.getExtent())
	  if (layer1.getVisibility()==true) {
	      gridPanel.reconfigure(storelayer1,collayer1);
	      listLayer = [];
	  }
      }
  });    
  
  //STORES FOR LAYERS, THE NAME IS store + layer_name ########################
  //store for park layer
  var storelayer1 = new GeoExt.data.FeatureStore({
    fields: [
        {name: "CODICE", type: "string"},
        {name: "ENTE", type: "string"},
        {name: "LOCALITA", type: "string"}/*,
        {name: "number_fac", type: "int", defaultValue: 0}*/
    ],
    layer: layer1
  });
  var collayer1 =  new Ext.grid.ColumnModel({
    columns: [
      {header: "Codice", dataIndex: "CODICE", width: 10},
      {header: "Ente", dataIndex: "ENTE", width: 10},
      {header: "Località", dataIndex: "LOCALITA", width: 35}/*,
      {
	  xtype: "numbercolumn",
	  header: "# of Facilities",
	  dataIndex: "number_fac",
	  format: "1,000",
	  align: "right",
	  width: 55
      }*/
    ]
  });
  ///END LAYERS ##############################
  
  //GRID TO SHOW THE STORE OF SELECTED LAYER ################################
  var gridPanel = new Ext.grid.GridPanel({
    title: "Attributes of features",
    region: "center",
    viewConfig: {forceFit: true},
    store: storelayer1,
    sm: new GeoExt.grid.FeatureSelectionModel(),
    cm: collayer1
  });  

  //create select control for all layers
  selectControl = new OpenLayers.Control.SelectFeature(
      layer1,
      {
	  toggle: true, hover: false, multiple: true
      }
  );
  map.addControl(selectControl);

  //TOOLBAR###################################################################
  //list for the toolbar
  var toolbar = [], action;

  // ZoomToMaxExtent control, a "button" control
  action = new GeoExt.Action({
      control: new OpenLayers.Control.ZoomToMaxExtent(),
      map: map,
      text: "Zoom extent",
      tooltip: "Zoom to max extent",
      group: "move",
  });
  toolbar.push(action);
  
  // ZoomBox control, a "button" control
  action = new GeoExt.Action({
      control: new OpenLayers.Control.ZoomIn(),
      map: map,
      text: "Zoom in",
      tooltip: "Zoom in",
      group: "move"
  });
  toolbar.push(action);

  // ZoomOut control, a "button" control
  action = new GeoExt.Action({
      control: new OpenLayers.Control.ZoomOut(),
      map: map,
      text: "Zoom out",
      tooltip: "Zoom out",
      group: "move"    
  });
  toolbar.push(action);
  toolbar.push("-");
  
  //control to select featuures
  action = new GeoExt.Action({
    map: map,
    control: selectControl,
    text: "Select features",			     
    tooltip: "Select feature to upload",
    enableToggle: true,
    group: "info",
//     iconCls: "infobox",
    pressed: false
  }); 
  
  toolbar.push(action);
  //control to unselect all feature
  action = new Ext.Button({
    handler: unselect,
    text: "Unselect features",			     
    tooltip: "Unselect all features"
//     enableToggle: true,
  });
  toolbar.push(action);
  //control for upload function
  action = new Ext.Button({
    handler: upload,
    text: "Upload",			     
    tooltip: "Upload selected feature in OSM"
  }); 
  toolbar.push(action);
  
  toolbar.push("-");  
  
//   // STORE per combobox e search##########################
//   var place = new OpenLayers.Layer.Vector("Località trentino");
//   var store_place = new GeoExt.data.FeatureStore({
//       layer: place,
//       fields: [
// 	  {name: 'osm_id', type: 'number'},    
// 	  {name: 'name', type: 'string'},
//       ],
//       proxy: new GeoExt.data.ProtocolProxy({
// 	  protocol: new OpenLayers.Protocol.HTTP({
// 	      url: "place_id.json",
// 	      format: new OpenLayers.Format.GeoJSON()
// 	  })
//       }),
//       autoLoad: true     
//   });  
//   // fine store########################################
//   // COMBOBOX ##################################
//   var comboPlace = new Ext.form.ComboBox({
//         store: store_place,
//         displayField:'name',
// 	valueField: 'osm_id',
//         typeAhead: true,
//         mode: 'local',
// 	id: 'comboplace',
//         forceSelection: true,
//         triggerAction: 'all',
//         emptyText:'Seleziona località...',
//         selectOnFocus:true,
// // 	tpl: 'E’ possibile selezionare la località di interesse dal menu a tendina. Oppure inserire il nome della località',
// 	listeners: {
// 	  'select':function(comboPlace) {
//  	      var rec = store_place.query('osm_id',comboPlace.getValue());
//  	      var lonCenter = rec.items[0].data.feature.geometry.x;
//  	      var latCenter = rec.items[0].data.feature.geometry.y;
// 	      var p = new Proj4js.Point(lonCenter,latCenter);
// 	      Proj4js.transform(sourceEPSG, destEPSG, p);
// 	      map.setCenter(new OpenLayers.LonLat(p.x, p.y), 9); 
// 	  } 
// 	}
//   });
//   
//   toolbar.push(comboPlace);
//   toolbar.push("-");

  //control for show help function  
  var action = new Ext.Action({
      text: 'Help',
      handler: function(){
	  help();
      },
      tooltip: "Show help panel"     
  });
  toolbar.push(action);    
  toolbar.push("-");  
  //control for show help function  
  var action = new Ext.Action({
      text: 'Login',
      handler: function(){
	  login();
      },
      tooltip: "Login with the user and password of your OpenStreetMap account"    
  });
  toolbar.push(action);    
  
  //control for show help function  
  var action = new Ext.Action({
      text: 'Logout',
      handler: function(){
	  logout();
      },
      tooltip: "Logout"
  }); 
  toolbar.push(action);    
  
  //MAPPANEL with map and toolbar##################
  var mapPanel = new GeoExt.MapPanel({
    region: "center",
    id: "mappanel",
    map: map,
    layers: map.layers,
//     extent: map.maxExtent,
    zoom: 1,
    tbar: toolbar
  });

  //LAYER LIST #####################################################à
  // create our own layer node UI class, using the TreeNodeUIEventMixin
  var LayerNodeUI = Ext.extend(GeoExt.tree.LayerNodeUI, new GeoExt.tree.TreeNodeUIEventMixin());
  
  var treeConfig = new OpenLayers.Format.JSON().write([{
        expanded: false,    
        nodeType: "gx_baselayercontainer"
    }, {
        nodeType: "gx_overlaylayercontainer",
        expanded: true,
        // render the nodes inside this container with a radio button,
        // and assign them the group "foo".
/*	plugins: [
	    new GeoExt.plugins.TreeNodeRadioButton({
	      listeners: {
		  "radiochange": function(node) {
		      alert(node.text + "'s radio button was clicked.");
		  }
	      }
	    })
	],*/	
        loader: {
            baseAttrs: {
                radioGroup: "overlay",
                uiProvider: "layernodeui"
            }
        }
    }
  ],true)
  
  var layerList = new Ext.tree.TreePanel({
        border: true,
	id: 'layertree',
        title: "Layer",
        width: 280,
        split: true,
        collapsible: true,
        collapseMode: "mini",
        autoScroll: true,
        loader: new Ext.tree.TreeLoader({
            // applyLoader has to be set to false to not interfer with loaders
            // of nodes further down the tree hierarchy
            applyLoader: false,
            uiProviders: {
                "layernodeui": LayerNodeUI
            }
        }),
        root: {
            nodeType: "async",
            // the children property of an Ext.tree.AsyncTreeNode is used to
            // provide an initial set of layer nodes. We use the treeConfig
            // from above, that we created with OpenLayers.Format.JSON.write.
            children: Ext.decode(treeConfig)
        },
        rootVisible: false,
        lines: true
    });
 
  //PANEL FOR INFO AND CREDITS##############################################
  var ricoPanel = new Ext.Panel({
    title: "Informations",
    width: 290,
    autoScroll: true,   
    bodyStyle: 'padding:3px;',
    contentEl: 'ricoPanel'
  });
  
  //TOOL PANEL IN THE LEFT OF MAPPANEL#######################################
  var toolPanel = new Ext.Panel({
    region:"east",
    title: 'ZOOSM client<br />Import data into OSM project',
    margins:'2 2 2 0',
    contentEl: "toolPanel",
    split:true,
    width: 300,
    layout:'accordion',
    items: [layerList, gridPanel, ricoPanel]
  });
  
  //PRINCIPAL VIEW##########################################################
  //contain mapPanel e toolPanel
  new Ext.Viewport({
      layout: "border",
      items: [mapPanel,toolPanel]
  });
  mapPanel = Ext.getCmp("mappanel"); 
       
});