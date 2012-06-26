/*
 * File:        TableTools.js
 * Version:     2.0.3
 * Description: Tools and buttons for DataTables
 * Author:      Allan Jardine (www.sprymedia.co.uk)
 * Language:    Javascript
 * License:	    GPL v2 or BSD 3 point style
 * Project:	    DataTables
 * 
 * Copyright 2009-2012 Allan Jardine, all rights reserved.
 *
 * This source file is free software, under either the GPL v2 license or a
 * BSD style license, available at:
 *   http://datatables.net/license_gpl2
 *   http://datatables.net/license_bsd
 */

/* Global scope for TableTools */
var TableTools;

(function($, window, document) {

/** 
 * TableTools provides flexible buttons and other tools for a DataTables enhanced table
 * @class TableTools
 * @constructor
 * @param {Object} oDT DataTables instance
 * @param {Object} oOpts TableTools options
 * @param {String} oOpts.sSwfPath ZeroClipboard SWF path
 * @param {String} oOpts.sRowSelect Row selection options - 'none', 'single' or 'multi'
 * @param {Function} oOpts.fnPreRowSelect Callback function just prior to row selection
 * @param {Function} oOpts.fnRowSelected Callback function just after row selection
 * @param {Function} oOpts.fnRowDeselected Callback function when row is deselected
 * @param {Array} oOpts.aButtons List of buttons to be used
 */
TableTools = function( oDT, oOpts )
{
	/* Santiy check that we are a new instance */
	if ( !this.CLASS || this.CLASS != "TableTools" )
	{
		alert( "Warning: TableTools must be initialised with the keyword 'new'" );
	}
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public class variables
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
	
	/**
	 * @namespace Settings object which contains customisable information for TableTools instance
	 */
	this.s = {
		/**
		 * Store 'this' so the instance can be retreieved from the settings object
		 * @property that
		 * @type	 object
		 * @default  this
		 */
		"that": this,
		
		/** 
		 * DataTables settings objects
		 * @property dt
		 * @type	 object
		 * @default  null
		 */
		"dt": null,
		
		/**
		 * @namespace Print specific information
		 */
		"print": {
			/** 
			 * DataTables draw 'start' point before the printing display was shown
			 *  @property saveStart
			 *  @type	 int
			 *  @default  -1
		 	 */
		  "saveStart": -1,
			
			/** 
			 * DataTables draw 'length' point before the printing display was shown
			 *  @property saveLength
			 *  @type	 int
			 *  @default  -1
		 	 */
		  "saveLength": -1,
		
			/** 
			 * Page scrolling point before the printing display was shown so it can be restored
			 *  @property saveScroll
			 *  @type	 int
			 *  @default  -1
		 	 */
		  "saveScroll": -1,
		
			/** 
			 * Wrapped function to end the print display (to maintain scope)
			 *  @property funcEnd
		 	 *  @type	 Function
			 *  @default  function () {}
		 	 */
		  "funcEnd": function () {}
	  },
	
		/**
		 * A unique ID is assigned to each button in each instance
		 * @property buttonCounter
		 *  @type	 int
		 * @default  0
		 */
	  "buttonCounter": 0,
		
		/**
		 * @namespace Select rows specific information
		 */
		"select": {
			/**
			 * Select type - can be 'none', 'single' or 'multi'
			 * @property type
			 *  @type	 string
			 * @default  ""
			 */
			"type": "",
			
			/**
			 * Array of nodes which are currently selected
			 *  @property selected
			 *  @type	 array
			 *  @default  []
			 */
			"selected": [],
			
			/**
			 * Function to run before the selection can take place. Will cancel the select if the
			 * function returns false
			 *  @property preRowSelect
			 *  @type	 Function
			 *  @default  null
			 */
			"preRowSelect": null,
			
			/**
			 * Function to run when a row is selected
			 *  @property postSelected
			 *  @type	 Function
			 *  @default  null
			 */
			"postSelected": null,
			
			/**
			 * Function to run when a row is deselected
			 *  @property postDeselected
			 *  @type	 Function
			 *  @default  null
			 */
			"postDeselected": null,
			
			/**
			 * Indicate if all rows are selected (needed for server-side processing)
			 *  @property all
			 *  @type	 boolean
			 *  @default  false
			 */
			"all": false,
			
			/**
			 * Class name to add to selected TR nodes
			 *  @property selectedClass
			 *  @type	 String
			 *  @default  ""
			 */
			"selectedClass": ""
		},
		
		/**
		 * Store of the user input customisation object
		 *  @property custom
		 *  @type	 object
		 *  @default  {}
		 */
		"custom": {},
		
		/**
		 * SWF movie path
		 *  @property swfPath
		 *  @type	 string
		 *  @default  ""
		 */
		"swfPath": "",
		
		/**
		 * Default button set
		 *  @property buttonSet
		 *  @type	 array
		 *  @default  []
		 */
		"buttonSet": [],
		
		/**
		 * When there is more than one TableTools instance for a DataTable, there must be a 
		 * master which controls events (row selection etc)
		 *  @property master
		 *  @type	 boolean
		 *  @default  false
		 */
		"master": false
	};
	
	
	/**
	 * @namespace Common and useful DOM elements for the class instance
	 */
	this.dom = {
		/**
		 * DIV element that is create and all TableTools buttons (and their children) put into
		 *  @property container
		 *  @type	 node
		 *  @default  null
		 */
		"container": null,
		
		/**
		 * The table node to which TableTools will be applied
		 *  @property table
		 *  @type	 node
		 *  @default  null
		 */
		"table": null,
		
		/**
		 * @namespace Nodes used for the print display
		 */
		"print": {
			/**
			 * Nodes which have been removed from the display by setting them to display none
			 *  @property hidden
			 *  @type	 array
		 	 *  @default  []
			 */
		  "hidden": [],
			
			/**
			 * The information display saying tellng the user about the print display
			 *  @property message
			 *  @type	 node
		 	 *  @default  null
			 */
		  "message": null
	  },
		
		/**
		 * @namespace Nodes used for a collection display. This contains the currently used collection
		 */
		"collection": {
			/**
			 * The div wrapper containing the buttons in the collection (i.e. the menu)
			 *  @property collection
			 *  @type	 node
		 	 *  @default  null
			 */
			"collection": null,
			
			/**
			 * Background display to provide focus and capture events
			 *  @property background
			 *  @type	 node
		 	 *  @default  null
			 */
			"background": null
		}
	};
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public class methods
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
	
	/**
	 * Retreieve the settings object from an instance
	 *  @method fnSettings
	 *  @returns {object} TableTools settings object
	 */
	this.fnSettings = function () {
		return this.s;
	};
	
	
	/* Constructor logic */
	if ( typeof oOpts == 'undefined' )
	{
		oOpts = {};
	}
	
	this.s.dt = oDT.fnSettings();
	this._fnConstruct( oOpts );
	
	return this;
};



TableTools.prototype = {
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Public methods
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
	
	/**
	 * Retreieve the settings object from an instance
	 *  @method fnGetSelected
	 *  @returns {array} List of TR nodes which are currently selected
	 */
	"fnGetSelected": function ()
	{
		var masterS = this._fnGetMasterSettings();
		return masterS.select.selected;
	},


	/**
	 * Get the data source objects/arrays from DataTables for the selected rows (same as
	 * fnGetSelected followed by fnGetData on each row from the table)
	 *  @method fnGetSelectedData
	 *  @returns {array} Data from the TR nodes which are currently selected
	 */
	"fnGetSelectedData": function ()
	{
		var masterS = this._fnGetMasterSettings();
		var selected = masterS.select.selected;
		var out = [];

		for ( var i=0, iLen=selected.length ; i<iLen ; i++ )
		{
			out.push( this.s.dt.oInstance.fnGetData( selected[i] ) );
		}

		return out;
	},
	
	
	/**
	 * Check to see if a current row is selected or not
	 *  @method fnGetSelected
	 *  @param {Node} n TR node to check if it is currently selected or not
	 *  @returns {Boolean} true if select, false otherwise
	 */
	"fnIsSelected": function ( n )
	{
		var selected = this.fnGetSelected();
		for ( var i=0, iLen=selected.length ; i<iLen ; i++ )
		{
			if ( n == selected[i] )
			{
				return true;
			}
		}
		return false;
	},

	
	/**
	 * Select all rows in the table
	 *  @method  fnSelectAll
	 *  @returns void
	 */
	"fnSelectAll": function ()
	{
		var masterS = this._fnGetMasterSettings();
		masterS.that._fnRowSelectAll();
	},

	
	/**
	 * Deselect all rows in the table
	 *  @method  fnSelectNone
	 *  @returns void
	 */
	"fnSelectNone": function ()
	{
		var masterS = this._fnGetMasterSettings();
		masterS.that._fnRowDeselectAll();
	},

	
	/**
	 * Select an individual row
	 *  @method  fnSelect
	 *  @returns void
	 */
	"fnSelect": function ( n )
	{
		/* Check if the row is already selected */
		if ( !this.fnIsSelected( n ) )
		{
			if ( this.s.select.type == "single" )
			{
				this._fnRowSelectSingle( n );
			}
			else if ( this.s.select.type == "multi" )
			{
				this._fnRowSelectMulti( n );
			}
		}
	},

	
	/**
	 * Deselect an individual row
	 *  @method  fnDeselect
	 *  @returns void
	 */
	"fnDeselect": function ( n )
	{
		/* Check if the row is already deselected */
		if ( this.fnIsSelected( n ) )
		{
			if ( this.s.select.type == "single" )
			{
				this._fnRowSelectSingle( n );
			}
			else if ( this.s.select.type == "multi" )
			{
				this._fnRowSelectMulti( n );
			}
		}
	},
	
	
	/**
	 * Get the title of the document - useful for file names. The title is retrieved from either
	 * the configuration object's 'title' parameter, or the HTML document title
	 *  @method  fnGetTitle
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {String} Button title
	 */
	"fnGetTitle": function( oConfig )
	{
		var sTitle = "";
		if ( typeof oConfig.sTitle != 'undefined' && oConfig.sTitle !== "" ) {
			sTitle = oConfig.sTitle;
		} else {
			var anTitle = document.getElementsByTagName('title');
			if ( anTitle.length > 0 )
			{
				sTitle = anTitle[0].innerHTML;
			}
		}
		
		/* Strip characters which the OS will object to - checking for UTF8 support in the scripting
		 * engine
		 */
		if ( "\u00A1".toString().length < 4 ) {
			return sTitle.replace(/[^a-zA-Z0-9_\u00A1-\uFFFF\.,\-_ !\(\)]/g, "");
		} else {
			return sTitle.replace(/[^a-zA-Z0-9_\.,\-_ !\(\)]/g, "");
		}
	},
	
	
	/**
	 * Calculate a unity array with the column width by proportion for a set of columns to be
	 * included for a button. This is particularly useful for PDF creation, where we can use the
	 * column widths calculated by the browser to size the columns in the PDF.
	 *  @method  fnCalcColRations
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {Array} Unity array of column ratios
	 */
	"fnCalcColRatios": function ( oConfig )
	{
		var
			aoCols = this.s.dt.aoColumns,
			aColumnsInc = this._fnColumnTargets( oConfig.mColumns ),
			aColWidths = [],
			iWidth = 0, iTotal = 0, i, iLen;
		
		for ( i=0, iLen=aColumnsInc.length ; i<iLen ; i++ )
		{
			if ( aColumnsInc[i] )
			{
				iWidth = aoCols[i].nTh.offsetWidth;
				iTotal += iWidth;
				aColWidths.push( iWidth );
			}
		}
		
		for ( i=0, iLen=aColWidths.length ; i<iLen ; i++ )
		{
			aColWidths[i] = aColWidths[i] / iTotal;
		}
		
		return aColWidths.join('\t');
	},
	
	
	/**
	 * Get the information contained in a table as a string
	 *  @method  fnGetTableData
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {String} Table data as a string
	 */
	"fnGetTableData": function ( oConfig )
	{
		/* In future this could be used to get data from a plain HTML source as well as DataTables */
		if ( this.s.dt )
		{
			return this._fnGetDataTablesData( oConfig );
		}
	},
	
	
	/**
	 * Pass text to a flash button instance, which will be used on the button's click handler
	 *  @method  fnSetText
	 *  @param   {Object} clip Flash button object
	 *  @param   {String} text Text to set
	 *  @returns void
	 */
	"fnSetText": function ( clip, text )
	{
		this._fnFlashSetText( clip, text );
	},
	
	
	/**
	 * Resize the flash elements of the buttons attached to this TableTools instance - this is
	 * useful for when initialising TableTools when it is hidden (display:none) since sizes can't
	 * be calculated at that time.
	 *  @method  fnResizeButtons
	 *  @returns void
	 */
	"fnResizeButtons": function ()
	{
		for ( var cli in ZeroClipboard_TableTools.clients )
		{
			if ( cli )
			{
				var client = ZeroClipboard_TableTools.clients[cli];
				if ( typeof client.domElement != 'undefined' &&
					 client.domElement.parentNode == this.dom.container )
				{
					client.positionElement();
				}
			}
		}
	},
	
	
	/**
	 * Check to see if any of the ZeroClipboard client's attached need to be resized
	 *  @method  fnResizeRequired
	 *  @returns void
	 */
	"fnResizeRequired": function ()
	{
		for ( var cli in ZeroClipboard_TableTools.clients )
		{
			if ( cli )
			{
				var client = ZeroClipboard_TableTools.clients[cli];
				if ( typeof client.domElement != 'undefined' &&
					 client.domElement.parentNode == this.dom.container &&
					 client.sized === false )
				{
					return true;
				}
			}
		}
		return false;
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Private methods (they are of course public in JS, but recommended as private)
	 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
	
	/**
	 * Constructor logic
	 *  @method  _fnConstruct
	 *  @param   {Object} oOpts Same as TableTools constructor
	 *  @returns void
	 *  @private 
	 */
	"_fnConstruct": function ( oOpts )
	{
		var that = this;
		
		this._fnCustomiseSettings( oOpts );
		
		/* Container element */
		this.dom.container = document.createElement('div');
		this.dom.container.className = !this.s.dt.bJUI ? "DTTT_container" :
			"DTTT_container ui-buttonset ui-buttonset-multi";
		
		/* Row selection config */
		if ( this.s.select.type != 'none' )
		{
			this._fnRowSelectConfig();
		}
		
		/* Buttons */
		this._fnButtonDefinations( this.s.buttonSet, this.dom.container );
		
		/* Destructor - need to wipe the DOM for IE's garbage collector */
		this.s.dt.aoDestroyCallback.push( {
			"sName": "TableTools",
			"fn": function () {
				that.dom.container.innerHTML = "";
			}
		} );
	},
	
	
	/**
	 * Take the user defined settings and the default settings and combine them.
	 *  @method  _fnCustomiseSettings
	 *  @param   {Object} oOpts Same as TableTools constructor
	 *  @returns void
	 *  @private 
	 */
	"_fnCustomiseSettings": function ( oOpts )
	{
		/* Is this the master control instance or not? */
		if ( typeof this.s.dt._TableToolsInit == 'undefined' )
		{
			this.s.master = true;
			this.s.dt._TableToolsInit = true;
		}
		
		/* We can use the table node from comparisons to group controls */
		this.dom.table = this.s.dt.nTable;
		
		/* Clone the defaults and then the user options */
		this.s.custom = $.extend( {}, TableTools.DEFAULTS, oOpts );
		
		/* Flash file location */
		this.s.swfPath = this.s.custom.sSwfPath;
		if ( typeof ZeroClipboard_TableTools != 'undefined' )
		{
			ZeroClipboard_TableTools.moviePath = this.s.swfPath;
		}
		
		/* Table row selecting */
		this.s.select.type = this.s.custom.sRowSelect;
		this.s.select.preRowSelect = this.s.custom.fnPreRowSelect;
		this.s.select.postSelected = this.s.custom.fnRowSelected;
		this.s.select.postDeselected = this.s.custom.fnRowDeselected;
		this.s.select.selectedClass = this.s.custom.sSelectedClass;
		
		/* Button set */
		this.s.buttonSet = this.s.custom.aButtons;
	},
	
	
	/**
	 * Take the user input arrays and expand them to be fully defined, and then add them to a given
	 * DOM element
	 *  @method  _fnButtonDefinations
	 *  @param {array} buttonSet Set of user defined buttons
	 *  @param {node} wrapper Node to add the created buttons to
	 *  @returns void
	 *  @private 
	 */
	"_fnButtonDefinations": function ( buttonSet, wrapper )
	{
		var buttonDef;
		
		for ( var i=0, iLen=buttonSet.length ; i<iLen ; i++ )
		{
			if ( typeof buttonSet[i] == "string" )
			{
				if ( typeof TableTools.BUTTONS[ buttonSet[i] ] == 'undefined' )
				{
					alert( "TableTools: Warning - unknown button type: "+buttonSet[i] );
					continue;
				}
				buttonDef = $.extend( {}, TableTools.BUTTONS[ buttonSet[i] ], true );
			}
			else
			{
				if ( typeof TableTools.BUTTONS[ buttonSet[i].sExtends ] == 'undefined' )
				{
					alert( "TableTools: Warning - unknown button type: "+buttonSet[i].sExtends );
					continue;
				}
				var o = $.extend( {}, TableTools.BUTTONS[ buttonSet[i].sExtends ], true );
				buttonDef = $.extend( o, buttonSet[i], true );
			}
			
			if ( this.s.dt.bJUI )
			{
				buttonDef.sButtonClass += " ui-button ui-state-default";
				buttonDef.sButtonClassHover += " ui-state-hover";
			}
			else
			{
				buttonDef.sButtonClassHover += " DTTT_button_hover";
			}
			
			wrapper.appendChild( this._fnCreateButton( buttonDef ) );
		}
	},
	
	
	/**
	 * Create and configure a TableTools button
	 *  @method  _fnCreateButton
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns {Node} Button element
	 *  @private 
	 */
	"_fnCreateButton": function ( oConfig )
	{
	  var nButton = (oConfig.sAction == 'div') ?
	  	this._fnDivBase( oConfig ) : this._fnButtonBase( oConfig );
		
		if ( oConfig.sAction == "print" )
		{
			this._fnPrintConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction.match(/flash/) )
		{
			this._fnFlashConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "text" )
		{
			this._fnTextConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "div" )
		{
			this._fnTextConfig( nButton, oConfig );
		}
		else if ( oConfig.sAction == "collection" )
		{
			this._fnTextConfig( nButton, oConfig );
			this._fnCollectionConfig( nButton, oConfig );
		}
		
		return nButton;
	},
	
	
	/**
	 * Create the DOM needed for the button and apply some base properties. All buttons start here
	 *  @method  _fnButtonBase
	 *  @param   {o} oConfig Button configuration object
	 *  @returns {Node} DIV element for the button
	 *  @private 
	 */
	"_fnButtonBase": function ( o )
	{
		var
		  nButton = document.createElement('button'),
		  nSpan = document.createElement('span'),
			masterS = this._fnGetMasterSettings();
		
		nButton.className = "DTTT_button "+o.sButtonClass;
		nButton.setAttribute('id', "ToolTables_"+this.s.dt.sInstance+"_"+masterS.buttonCounter );
		nButton.appendChild( nSpan );
		nSpan.innerHTML = o.sButtonText;
		
		masterS.buttonCounter++;
		
		return nButton;
	},
	
	
	/**
	 * Create a DIV element to use for a non-button
	 *  @method  _fnDivBase
	 *  @param   {o} oConfig Button configuration object
	 *  @returns {Node} DIV element for the button
	 *  @private 
	 */
	"_fnDivBase": function ( o )
	{
		var
		  nDiv = document.createElement('div'),
			masterS = this._fnGetMasterSettings();
		
		nDiv.className = o.sButtonClass;
		nDiv.setAttribute('id', "ToolTables_"+this.s.dt.sInstance+"_"+masterS.buttonCounter );
		nDiv.innerHTML = o.sButtonText;

		if ( o.nContent !== null )
		{
			nDiv.appendChild( o.nContent );
		}
		
		masterS.buttonCounter++;
		
		return nDiv;
	},
	
	
	/**
	 * Get the settings object for the master instance. When more than one TableTools instance is
	 * assigned to a DataTable, only one of them can be the 'master' (for the select rows). As such,
	 * we will typically want to interact with that master for global properties.
	 *  @method  _fnGetMasterSettings
	 *  @returns {Object} TableTools settings object
	 *  @private 
	 */
	"_fnGetMasterSettings": function ()
	{
		if ( this.s.master )
		{
			return this.s;
		}
		else
		{
			/* Look for the master which has the same DT as this one */
			var instances = TableTools._aInstances;
			for ( var i=0, iLen=instances.length ; i<iLen ; i++ )
			{
				if ( this.dom.table == instances[i].s.dt.nTable )
				{
					return instances[i].s;
				}
			}
		}
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Button collection functions
	 */
	
	/**
	 * Create a collection button, when activated will present a drop downlist of other buttons
	 *  @param   {Node} nButton Button to use for the collection activation
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionConfig": function ( nButton, oConfig )
	{
		var nHidden = document.createElement('div');
		nHidden.style.display = "none";
		nHidden.className = !this.s.dt.bJUI ? "DTTT_collection" :
			"DTTT_collection ui-buttonset ui-buttonset-multi";
		oConfig._collection = nHidden;
		document.body.appendChild( nHidden );
		
		this._fnButtonDefinations( oConfig.aButtons, nHidden );
	},
	
	
	/**
	 * Show a button collection
	 *  @param   {Node} nButton Button to use for the collection
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionShow": function ( nButton, oConfig )
	{
		var
			that = this,
			oPos = $(nButton).offset(),
			nHidden = oConfig._collection,
			iDivX = oPos.left,
			iDivY = oPos.top + $(nButton).outerHeight(),
			iWinHeight = $(window).height(), iDocHeight = $(document).height(),
		 	iWinWidth = $(window).width(), iDocWidth = $(document).width();
		
		nHidden.style.position = "absolute";
		nHidden.style.left = iDivX+"px";
		nHidden.style.top = iDivY+"px";
		nHidden.style.display = "block";
		$(nHidden).css('opacity',0);
		
		var nBackground = document.createElement('div');
		nBackground.style.position = "absolute";
		nBackground.style.left = "0px";
		nBackground.style.top = "0px";
		nBackground.style.height = ((iWinHeight>iDocHeight)? iWinHeight : iDocHeight) +"px";
		nBackground.style.width = ((iWinWidth>iDocWidth)? iWinWidth : iDocWidth) +"px";
		nBackground.className = "DTTT_collection_background";
		$(nBackground).css('opacity',0);
		
		document.body.appendChild( nBackground );
		document.body.appendChild( nHidden );
		
		/* Visual corrections to try and keep the collection visible */
		var iDivWidth = $(nHidden).outerWidth();
		var iDivHeight = $(nHidden).outerHeight();
		
		if ( iDivX + iDivWidth > iDocWidth )
		{
			nHidden.style.left = (iDocWidth-iDivWidth)+"px";
		}
		
		if ( iDivY + iDivHeight > iDocHeight )
		{
			nHidden.style.top = (iDivY-iDivHeight-$(nButton).outerHeight())+"px";
		}
	
		this.dom.collection.collection = nHidden;
		this.dom.collection.background = nBackground;
		
		/* This results in a very small delay for the end user but it allows the animation to be
		 * much smoother. If you don't want the animation, then the setTimeout can be removed
		 */
		setTimeout( function () {
			$(nHidden).animate({"opacity": 1}, 500);
			$(nBackground).animate({"opacity": 0.25}, 500);
		}, 10 );
		
		/* Event handler to remove the collection display */
		$(nBackground).click( function () {
			that._fnCollectionHide.call( that, null, null );
		} );
	},
	
	
	/**
	 * Hide a button collection
	 *  @param   {Node} nButton Button to use for the collection
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private
	 */
	"_fnCollectionHide": function ( nButton, oConfig )
	{
		if ( oConfig !== null && oConfig.sExtends == 'collection' )
		{
			return;
		}
		
		if ( this.dom.collection.collection !== null )
		{
			$(this.dom.collection.collection).animate({"opacity": 0}, 500, function (e) {
				this.style.display = "none";
			} );
			
			$(this.dom.collection.background).animate({"opacity": 0}, 500, function (e) {
				this.parentNode.removeChild( this );
			} );
			
			this.dom.collection.collection = null;
			this.dom.collection.background = null;
		}
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Row selection functions
	 */
	
	/**
	 * Add event handlers to a table to allow for row selection
	 *  @method  _fnRowSelectConfig
	 *  @returns void
	 *  @private 
	 */
	"_fnRowSelectConfig": function ()
	{
		if ( this.s.master )
		{
			var
				that = this, 
				i, iLen, 
				aoOpenRows = this.s.dt.aoOpenRows;
			
			$(that.s.dt.nTable).addClass( 'DTTT_selectable' );
			
			$('tr', that.s.dt.nTBody).live( 'click', function(e) {
				/* Sub-table must be ignored (odd that the selector won't do this with >) */
				if ( this.parentNode != that.s.dt.nTBody )
				{
					return;
				}
				
				/* Check that we are actually working with a DataTables controlled row */
				var anTableRows = that.s.dt.oInstance.fnGetNodes();
				if ( $.inArray( this, anTableRows ) === -1 ) {
				    return;
				}
				
				/* User defined selection function */
				if ( that.s.select.preRowSelect !== null && !that.s.select.preRowSelect.call(that, e) )
				{
					return;
				}
				
				/* And go */
				if ( that.s.select.type == "single" )
				{
					that._fnRowSelectSingle.call( that, this );
				}
				else
				{
					that._fnRowSelectMulti.call( that, this );
				}
			} );
			
			/* Add a draw callback handler for when 'select' all is active and we are using server-side
			 * processing, so TableTools will automatically select the new rows for us
			 */
			that.s.dt.aoDrawCallback.push( {
				"fn": function () {
					if ( that.s.select.all && that.s.dt.oFeatures.bServerSide )
					{
						that.fnSelectAll();
					}
				},
				"sName": "TableTools_select"
			} );
		}
	},
	
	
	/**
	 * Select or deselect a row based on its current state when only one row is allowed to be
	 * selected at a time (i.e. if there is a row already selected, deselect it). If the selected
	 * row is the one being passed in, just deselect and take no further action.
	 *  @method  _fnRowSelectSingle
	 *  @param   {Node} nNode TR element which is being 'activated' in some way
	 *  @returns void
	 *  @private 
	 */
	"_fnRowSelectSingle": function ( nNode )
	{
		if ( this.s.master )
		{
			/* Do nothing on the DataTables 'empty' result set row */
			if ( $('td', nNode).hasClass(this.s.dt.oClasses.sRowEmpty) )
			{
				return;
			}
			
			if ( $(nNode).hasClass(this.s.select.selectedClass) )
			{
				this._fnRowDeselect( nNode );
			}
			else
			{
				if ( this.s.select.selected.length !== 0 )
				{
					this._fnRowDeselectAll();
				}
				
				this.s.select.selected.push( nNode );
				$(nNode).addClass( this.s.select.selectedClass );
				
				if ( this.s.select.postSelected !== null )
				{
					this.s.select.postSelected.call( this, nNode );
				}
			}
			
			TableTools._fnEventDispatch( this, 'select', nNode );
		}
	},
	
	
	/**
	 * Select or deselect a row based on its current state when multiple rows are allowed to be
	 * selected.
	 *  @method  _fnRowSelectMulti
	 *  @param   {Node} nNode TR element which is being 'activated' in some way
	 *  @returns void
	 *  @private 
	 */
	"_fnRowSelectMulti": function ( nNode )
	{
		if ( this.s.master )
		{
			/* Do nothing on the DataTables 'empty' result set row */
			if ( $('td', nNode).hasClass(this.s.dt.oClasses.sRowEmpty) )
			{
				return;
			}
			
			if ( $(nNode).hasClass(this.s.select.selectedClass) )
			{
				this._fnRowDeselect( nNode );
			}
			else
			{
				this.s.select.selected.push( nNode );
				$(nNode).addClass( this.s.select.selectedClass );
				
				if ( this.s.select.postSelected !== null )
				{
					this.s.select.postSelected.call( this, nNode );
				}
			}
			
			TableTools._fnEventDispatch( this, 'select', nNode );
		}
	},
	
	
	/**
	 * Select all TR elements in the table. Note that this function will still operate in 'single'
	 * select mode, which might not be what you desire (in which case, don't call this function!)
	 *  @method  _fnRowSelectAll
	 *  @returns void
	 *  @private 
	 */
	"_fnRowSelectAll": function ( )
	{
		if ( this.s.master )
		{
			var n;
			for ( var i=0, iLen=this.s.dt.aiDisplayMaster.length ; i<iLen ; i++ )
			{
				n = this.s.dt.aoData[ this.s.dt.aiDisplayMaster[i] ].nTr;
				
				if ( !$(n).hasClass(this.s.select.selectedClass) )
				{
					this.s.select.selected.push( n );
					$(n).addClass( this.s.select.selectedClass );
				}
			}

			if ( this.s.select.postSelected !== null )
			{
				this.s.select.postSelected.call( this, null );
			}
			
			this.s.select.all = true;
			TableTools._fnEventDispatch( this, 'select', null );
		}
	},
	
	
	/**
	 * Deselect all TR elements in the table. If nothing is currently selected, then no action is
	 * taken.
	 *  @method  _fnRowDeselectAll
	 *  @returns void
	 *  @private 
	 */
	"_fnRowDeselectAll": function ( )
	{
		if ( this.s.master )
		{
			for ( var i=this.s.select.selected.length-1 ; i>=0 ; i-- )
			{
				this._fnRowDeselect( i, false );
			}

			if ( this.s.select.postDeselected !== null )
			{
				this.s.select.postDeselected.call( this, null );
			}
			
			this.s.select.all = false;
			TableTools._fnEventDispatch( this, 'select', null );
		}
	},
	
	
	/**
	 * Deselect a single row, based on its index in the selected array, or a TR node (when the
	 * index is then computed)
	 *  @method  _fnRowDeselect
	 *  @param   {int|Node} i Node or index of node in selected array, which is to be deselected
	 *  @param   {bool} [action=true] Run the post deselected method or not
	 *  @returns void
	 *  @private 
	 */
	"_fnRowDeselect": function ( i, action )
	{
		if ( typeof i.nodeName != 'undefined' )
		{
			i = $.inArray( i, this.s.select.selected );
		}
		
		var nNode = this.s.select.selected[i];
		$(nNode).removeClass(this.s.select.selectedClass);
		this.s.select.selected.splice( i, 1 );
		
		if ( (typeof action == 'undefined' || action) && this.s.select.postDeselected !== null )
		{
			this.s.select.postDeselected.call( this, nNode );
		}
		
		this.s.select.all = false;
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Text button functions
	 */
	
	/**
	 * Configure a text based button for interaction events
	 *  @method  _fnTextConfig
	 *  @param   {Node} nButton Button element which is being considered
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnTextConfig": function ( nButton, oConfig )
	{
		var that = this;
		
		if ( oConfig.fnInit !== null )
		{
			oConfig.fnInit.call( this, nButton, oConfig );
		}
		
		if ( oConfig.sToolTip !== "" )
		{
			nButton.title = oConfig.sToolTip;
		}
		
		$(nButton).hover( function () {
			$(nButton).addClass(oConfig.sButtonClassHover );
			if ( oConfig.fnMouseover !== null )
			{
				oConfig.fnMouseover.call( this, nButton, oConfig, null );
			}
		}, function () {
			$(nButton).removeClass( oConfig.sButtonClassHover );
			if ( oConfig.fnMouseout !== null )
			{
				oConfig.fnMouseout.call( this, nButton, oConfig, null );
			}
		} );
		
		if ( oConfig.fnSelect !== null )
		{
			TableTools._fnEventListen( this, 'select', function (n) {
				oConfig.fnSelect.call( that, nButton, oConfig, n );
			} );
		}
		
		$(nButton).click( function (e) {
			e.preventDefault();
			
			if ( oConfig.fnClick !== null )
			{
				oConfig.fnClick.call( that, nButton, oConfig, null );
			}
			
			/* Provide a complete function to match the behaviour of the flash elements */
			if ( oConfig.fnComplete !== null )
			{
				oConfig.fnComplete.call( that, nButton, oConfig, null, null );
			}
			
			that._fnCollectionHide( nButton, oConfig );
		} );
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Flash button functions
	 */
	
	/**
	 * Configure a flash based button for interaction events
	 *  @method  _fnFlashConfig
	 *  @param   {Node} nButton Button element which is being considered
	 *  @param   {o} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashConfig": function ( nButton, oConfig )
	{
		var that = this;
		var flash = new ZeroClipboard_TableTools.Client();
		
		if ( oConfig.fnInit !== null )
		{
			oConfig.fnInit.call( this, nButton, oConfig );
		}
		
		flash.setHandCursor( true );
		
		if ( oConfig.sAction == "flash_save" )
		{
			flash.setAction( 'save' );
			flash.setCharSet( (oConfig.sCharSet=="utf16le") ? 'UTF16LE' : 'UTF8' );
			flash.setBomInc( oConfig.bBomInc );
			flash.setFileName( oConfig.sFileName.replace('*', this.fnGetTitle(oConfig)) );
		}
		else if ( oConfig.sAction == "flash_pdf" )
		{
			flash.setAction( 'pdf' );
			flash.setFileName( oConfig.sFileName.replace('*', this.fnGetTitle(oConfig)) );
		}
		else
		{
			flash.setAction( 'copy' );
		}
		
		flash.addEventListener('mouseOver', function(client) {
			$(nButton).addClass(oConfig.sButtonClassHover );
			
			if ( oConfig.fnMouseover !== null )
			{
				oConfig.fnMouseover.call( that, nButton, oConfig, flash );
			}
		} );
		
		flash.addEventListener('mouseOut', function(client) {
			$(nButton).removeClass( oConfig.sButtonClassHover );
			
			if ( oConfig.fnMouseout !== null )
			{
				oConfig.fnMouseout.call( that, nButton, oConfig, flash );
			}
		} );
		
		flash.addEventListener('mouseDown', function(client) {
			if ( oConfig.fnClick !== null )
			{
				oConfig.fnClick.call( that, nButton, oConfig, flash );
			}
		} );
		
		flash.addEventListener('complete', function (client, text) {
			if ( oConfig.fnComplete !== null )
			{
				oConfig.fnComplete.call( that, nButton, oConfig, flash, text );
			}
			that._fnCollectionHide( nButton, oConfig );
		} );
		
		this._fnFlashGlue( flash, nButton, oConfig.sToolTip );
	},
	
	
	/**
	 * Wait until the id is in the DOM before we "glue" the swf. Note that this function will call
	 * itself (using setTimeout) until it completes successfully
	 *  @method  _fnFlashGlue
	 *  @param   {Object} clip Zero clipboard object
	 *  @param   {Node} node node to glue swf to
	 *  @param   {String} text title of the flash movie
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashGlue": function ( flash, node, text )
	{
		var that = this;
		var id = node.getAttribute('id');
		
		if ( document.getElementById(id) )
		{
			flash.glue( node, text );
			
			/* Catch those who are using a TableTools 1 version of ZeroClipboard */
			if ( flash.domElement.parentNode != flash.div.parentNode && 
				   typeof that.__bZCWarning == 'undefined' )
			{
				that.s.dt.oApi._fnLog( this.s.dt, 0, "It looks like you are using the version of "+
					"ZeroClipboard which came with TableTools 1. Please update to use the version that "+
					"came with TableTools 2." );
				that.__bZCWarning = true;
			}
		}
		else
		{
			setTimeout( function () {
				that._fnFlashGlue( flash, node, text );
			}, 100 );
		}
	},
	
	
	/**
	 * Set the text for the flash clip to deal with
	 * 
	 * This function is required for large information sets. There is a limit on the 
	 * amount of data that can be transfered between Javascript and Flash in a single call, so
	 * we use this method to build up the text in Flash by sending over chunks. It is estimated
	 * that the data limit is around 64k, although it is undocuments, and appears to be different
	 * between different flash versions. We chunk at 8KiB.
	 *  @method  _fnFlashSetText
	 *  @param   {Object} clip the ZeroClipboard object
	 *  @param   {String} sData the data to be set
	 *  @returns void
	 *  @private 
	 */
	"_fnFlashSetText": function ( clip, sData )
	{
		var asData = this._fnChunkData( sData, 8192 );
		
		clip.clearText();
		for ( var i=0, iLen=asData.length ; i<iLen ; i++ )
		{
			clip.appendText( asData[i] );
		}
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Data retrieval functions
	 */
	
	/**
	 * Convert the mixed columns variable into a boolean array the same size as the columns, which
	 * indicates which columns we want to include
	 *  @method  _fnColumnTargets
	 *  @param   {String|Array} mColumns The columns to be included in data retreieval. If a string
	 *			 then it can take the value of "visible" or "hidden" (to include all visible or
	 *			 hidden columns respectively). Or an array of column indexes
	 *  @returns {Array} A boolean array the length of the columns of the table, which each value
	 *			 indicating if the column is to be included or not
	 *  @private 
	 */
	"_fnColumnTargets": function ( mColumns )
	{
		var aColumns = [];
		var dt = this.s.dt;
		
		if ( typeof mColumns == "object" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( false );
			}
			
			for ( i=0, iLen=mColumns.length ; i<iLen ; i++ )
			{
				aColumns[ mColumns[i] ] = true;
			}
		}
		else if ( mColumns == "visible" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bVisible ? true : false );
			}
		}
		else if ( mColumns == "hidden" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bVisible ? false : true );
			}
		}
		else if ( mColumns == "sortable" )
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( dt.aoColumns[i].bSortable ? true : false );
			}
		}
		else /* all */
		{
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				aColumns.push( true );
			}
		}
		
		return aColumns;
	},
	
	
	/**
	 * New line character(s) depend on the platforms
	 *  @method  method
	 *  @param   {Object} oConfig Button configuration object - only interested in oConfig.sNewLine
	 *  @returns {String} Newline character
	 */
	"_fnNewline": function ( oConfig )
	{
		if ( oConfig.sNewLine == "auto" )
		{
			return navigator.userAgent.match(/Windows/) ? "\r\n" : "\n";
		}
		else
		{
			return oConfig.sNewLine;
		}
	},
	
	
	/**
	 * Get data from DataTables' internals and format it for output
	 *  @method  _fnGetDataTablesData
	 *  @param   {Object} oConfig Button configuration object
	 *  @param   {String} oConfig.sFieldBoundary Field boundary for the data cells in the string
	 *  @param   {String} oConfig.sFieldSeperator Field seperator for the data cells
	 *  @param   {String} oConfig.sNewline New line options
	 *  @param   {Mixed} oConfig.mColumns Which columns should be included in the output
	 *  @param   {Boolean} oConfig.bHeader Include the header
	 *  @param   {Boolean} oConfig.bFooter Include the footer
	 *  @param   {Boolean} oConfig.bSelectedOnly Include only the selected rows in the output
	 *  @returns {String} Concatinated string of data
	 *  @private 
	 */
	"_fnGetDataTablesData": function ( oConfig )
	{
		var i, iLen, j, jLen;
		var aRow, aData=[], sLoopData='';
		var dt = this.s.dt;
		var regex = new RegExp(oConfig.sFieldBoundary, "g"); /* Do it here for speed */
		var aColumnsInc = this._fnColumnTargets( oConfig.mColumns );
		var bSelectedOnly = (typeof oConfig.bSelectedOnly != 'undefined') ? oConfig.bSelectedOnly : false;
		
		/*
		 * Header
		 */
		if ( oConfig.bHeader )
		{
			aRow = [];
			
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				if ( aColumnsInc[i] )
				{
					sLoopData = dt.aoColumns[i].sTitle.replace(/\n/g," ").replace( /<.*?>/g, "" ).replace(/^\s+|\s+$/g,"");
					sLoopData = this._fnHtmlDecode( sLoopData );
					
					aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
				}
			}

			aData.push( aRow.join(oConfig.sFieldSeperator) );
		}
		
		/*
		 * Body
		 */
		for ( j=0, jLen=dt.aiDisplay.length ; j<jLen ; j++ )
		{
			if ( this.s.select.type == "none" || !bSelectedOnly ||
				   (bSelectedOnly && $(dt.aoData[ dt.aiDisplay[j] ].nTr).hasClass( this.s.select.selectedClass )) ||
			     (bSelectedOnly && this.s.select.selected.length == 0) )
			{
				aRow = [];
				
				/* Columns */
				for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
				{
					if ( aColumnsInc[i] )
					{
						/* Convert to strings (with small optimisation) */
						var mTypeData = dt.oApi._fnGetCellData( dt, dt.aiDisplay[j], i, 'display' );
						if ( oConfig.fnCellRender )
						{
							sLoopData = oConfig.fnCellRender( mTypeData, i )+"";
						}
						else if ( typeof mTypeData == "string" )
						{
							/* Strip newlines, replace img tags with alt attr. and finally strip html... */
							sLoopData = mTypeData.replace(/\n/g," ");
							sLoopData =
							 	sLoopData.replace(/<img.*?\s+alt\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+)).*?>/gi,
							 		'$1$2$3');
							sLoopData = sLoopData.replace( /<.*?>/g, "" );
						}
						else
						{
							sLoopData = mTypeData+"";
						}
						
						/* Trim and clean the data */
						sLoopData = sLoopData.replace(/^\s+/, '').replace(/\s+$/, '');
						sLoopData = this._fnHtmlDecode( sLoopData );
						
						/* Bound it and add it to the total data */
						aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
					}
				}

				aData.push( aRow.join(oConfig.sFieldSeperator) );
			}
		}
		
		/*
		 * Footer
		 */
		if ( oConfig.bFooter && dt.nTFoot !== null )
		{
			aRow = [];
			
			for ( i=0, iLen=dt.aoColumns.length ; i<iLen ; i++ )
			{
				if ( aColumnsInc[i] && dt.aoColumns[i].nTf !== null )
				{
					sLoopData = dt.aoColumns[i].nTf.innerHTML.replace(/\n/g," ").replace( /<.*?>/g, "" );
					sLoopData = this._fnHtmlDecode( sLoopData );
					
					aRow.push( this._fnBoundData( sLoopData, oConfig.sFieldBoundary, regex ) );
				}
			}
			
			aData.push( aRow.join(oConfig.sFieldSeperator) );
		}
		
		_sLastData = aData.join( this._fnNewline(oConfig) );
		return _sLastData;
	},
	
	
	/**
	 * Wrap data up with a boundary string
	 *  @method  _fnBoundData
	 *  @param   {String} sData data to bound
	 *  @param   {String} sBoundary bounding char(s)
	 *  @param   {RegExp} regex search for the bounding chars - constructed outside for efficincy
	 *			 in the loop
	 *  @returns {String} bound data
	 *  @private 
	 */
	"_fnBoundData": function ( sData, sBoundary, regex )
	{
		if ( sBoundary === "" )
		{
			return sData;
		}
		else
		{
			return sBoundary + sData.replace(regex, sBoundary+sBoundary) + sBoundary;
		}
	},
	
	
	/**
	 * Break a string up into an array of smaller strings
	 *  @method  _fnChunkData
	 *  @param   {String} sData data to be broken up
	 *  @param   {Int} iSize chunk size
	 *  @returns {Array} String array of broken up text
	 *  @private 
	 */
	"_fnChunkData": function ( sData, iSize )
	{
		var asReturn = [];
		var iStrlen = sData.length;
		
		for ( var i=0 ; i<iStrlen ; i+=iSize )
		{
			if ( i+iSize < iStrlen )
			{
				asReturn.push( sData.substring( i, i+iSize ) );
			}
			else
			{
				asReturn.push( sData.substring( i, iStrlen ) );
			}
		}
		
		return asReturn;
	},
	
	
	/**
	 * Decode HTML entities
	 *  @method  _fnHtmlDecode
	 *  @param   {String} sData encoded string
	 *  @returns {String} decoded string
	 *  @private 
	 */
	"_fnHtmlDecode": function ( sData )
	{
		if ( sData.indexOf('&') == -1 )
		{
			return sData;
		}
		
		var 
			aData = this._fnChunkData( sData, 2048 ),
			n = document.createElement('div'),
			i, iLen, iIndex,
			sReturn = "", sInner;
		
		/* nodeValue has a limit in browsers - so we chunk the data into smaller segments to build
		 * up the string. Note that the 'trick' here is to remember than we might have split over
		 * an HTML entity, so we backtrack a little to make sure this doesn't happen
		 */
		for ( i=0, iLen=aData.length ; i<iLen ; i++ )
		{
			/* Magic number 8 is because no entity is longer then strlen 8 in ISO 8859-1 */
			iIndex = aData[i].lastIndexOf( '&' );
			if ( iIndex != -1 && aData[i].length >= 8 && iIndex > aData[i].length - 8 )
			{
				sInner = aData[i].substr( iIndex );
				aData[i] = aData[i].substr( 0, iIndex );
			}
			
			n.innerHTML = aData[i];
			sReturn += n.childNodes[0].nodeValue;
		}
		
		return sReturn;
	},
	
	
	
	/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
	 * Printing functions
	 */
	
	/**
	 * Configure a button for printing
	 *  @method  _fnPrintConfig
	 *  @param   {Node} nButton Button element which is being considered
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintConfig": function ( nButton, oConfig )
	{
	  var that = this;

		if ( oConfig.fnInit !== null )
		{
			oConfig.fnInit.call( this, nButton, oConfig );
		}
		
		if ( oConfig.sToolTip !== "" )
		{
			nButton.title = oConfig.sToolTip;
		}

	  $(nButton).hover( function () {
			$(nButton).addClass(oConfig.sButtonClassHover );
		}, function () {
			$(nButton).removeClass( oConfig.sButtonClassHover );
		} );
		
		if ( oConfig.fnSelect !== null )
		{
			TableTools._fnEventListen( this, 'select', function (n) {
				oConfig.fnSelect.call( that, nButton, oConfig, n );
			} );
		}
		
		$(nButton).click( function (e) {
			e.preventDefault();
			
			that._fnPrintStart.call( that, e, oConfig);
			
			if ( oConfig.fnClick !== null )
			{
				oConfig.fnClick.call( that, nButton, oConfig, null );
			}
			
			/* Provide a complete function to match the behaviour of the flash elements */
			if ( oConfig.fnComplete !== null )
			{
				oConfig.fnComplete.call( that, nButton, oConfig, null, null );
			}
			
			that._fnCollectionHide( nButton, oConfig );
		} );
	},
	
	/**
	 * Show print display
	 *  @method  _fnPrintStart
	 *  @param   {Event} e Event object
	 *  @param   {Object} oConfig Button configuration object
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintStart": function ( e, oConfig )
	{
	  var that = this;
	  var oSetDT = this.s.dt;
	  
		/* Parse through the DOM hiding everything that isn't needed for the table */
		this._fnPrintHideNodes( oSetDT.nTable );
		
		/* Show the whole table */
		this.s.print.saveStart = oSetDT._iDisplayStart;
		this.s.print.saveLength = oSetDT._iDisplayLength;

		if ( oConfig.bShowAll )
		{
			oSetDT._iDisplayStart = 0;
			oSetDT._iDisplayLength = -1;
			oSetDT.oApi._fnCalculateEnd( oSetDT );
			oSetDT.oApi._fnDraw( oSetDT );
		}
		
		/* Adjust the display for scrolling which might be done by DataTables */
		if ( oSetDT.oScroll.sX !== "" || oSetDT.oScroll.sY !== "" )
		{
			this._fnPrintScrollStart( oSetDT );
		}
		
		/* Remove the other DataTables feature nodes - but leave the table! and info div */
		var anFeature = oSetDT.aanFeatures;
		for ( var cFeature in anFeature )
		{
			if ( cFeature != 'i' && cFeature != 't' && cFeature.length == 1 )
			{
				for ( var i=0, iLen=anFeature[cFeature].length ; i<iLen ; i++ )
				{
					this.dom.print.hidden.push( {
						"node": anFeature[cFeature][i],
						"display": "block"
					} );
					anFeature[cFeature][i].style.display = "none";
				}
			}
		}
		
		/* Print class can be used for styling */
		$(document.body).addClass( 'DTTT_Print' );
	
		/* Add a node telling the user what is going on */
		if ( oConfig.sInfo !== "" )
		{
		  var nInfo = document.createElement( "div" );
		  nInfo.className = "DTTT_print_info";
		  nInfo.innerHTML = oConfig.sInfo;
		  document.body.appendChild( nInfo );
		  
		  setTimeout( function() {
		  	$(nInfo).fadeOut( "normal", function() {
		  		document.body.removeChild( nInfo );
		  	} );
		  }, 2000 );
		}
		
		/* Add a message at the top of the page */
		if ( oConfig.sMessage !== "" )
		{
			this.dom.print.message = document.createElement( "div" );
			this.dom.print.message.className = "DTTT_PrintMessage";
			this.dom.print.message.innerHTML = oConfig.sMessage;
			document.body.insertBefore( this.dom.print.message, document.body.childNodes[0] );
		}
		
		/* Cache the scrolling and the jump to the top of the t=page */
		this.s.print.saveScroll = $(window).scrollTop();
		window.scrollTo( 0, 0 );
		
		this.s.print.funcEnd = function(e) {
			that._fnPrintEnd.call( that, e ); 
		};
		$(document).bind( "keydown", null, this.s.print.funcEnd );
	},
	
	
	/**
	 * Printing is finished, resume normal display
	 *  @method  _fnPrintEnd
	 *  @param   {Event} e Event object
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintEnd": function ( e )
	{
		/* Only interested in the escape key */
		if ( e.keyCode == 27 )
		{
			e.preventDefault();
			
			var that = this;
			var oSetDT = this.s.dt;
			var oSetPrint = this.s.print;
			var oDomPrint = this.dom.print;
			
			/* Show all hidden nodes */
			this._fnPrintShowNodes();
			
			/* Restore DataTables' scrolling */
			if ( oSetDT.oScroll.sX !== "" || oSetDT.oScroll.sY !== "" )
			{
				this._fnPrintScrollEnd();
			}
			
			/* Restore the scroll */
			window.scrollTo( 0, oSetPrint.saveScroll );
			
			/* Drop the print message */
			if ( oDomPrint.message !== null )
			{
				document.body.removeChild( oDomPrint.message );
				oDomPrint.message = null;
			}
			
			/* Styling class */
			$(document.body).removeClass( 'DTTT_Print' );
			
			/* Restore the table length */
			oSetDT._iDisplayStart = oSetPrint.saveStart;
			oSetDT._iDisplayLength = oSetPrint.saveLength;
			oSetDT.oApi._fnCalculateEnd( oSetDT );
			oSetDT.oApi._fnDraw( oSetDT );
			
			$(document).unbind( "keydown", this.s.print.funcEnd );
			this.s.print.funcEnd = null;
		}
	},
	
	
	/**
	 * Take account of scrolling in DataTables by showing the full table
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintScrollStart": function ()
	{
		var 
			oSetDT = this.s.dt,
			nScrollHeadInner = oSetDT.nScrollHead.getElementsByTagName('div')[0],
			nScrollHeadTable = nScrollHeadInner.getElementsByTagName('table')[0],
			nScrollBody = oSetDT.nTable.parentNode;

		/* Copy the header in the thead in the body table, this way we show one single table when
		 * in print view. Note that this section of code is more or less verbatim from DT 1.7.0
		 */
		var nTheadSize = oSetDT.nTable.getElementsByTagName('thead');
		if ( nTheadSize.length > 0 )
		{
			oSetDT.nTable.removeChild( nTheadSize[0] );
		}
		
		if ( oSetDT.nTFoot !== null )
		{
			var nTfootSize = oSetDT.nTable.getElementsByTagName('tfoot');
			if ( nTfootSize.length > 0 )
			{
				oSetDT.nTable.removeChild( nTfootSize[0] );
			}
		}
		
		nTheadSize = oSetDT.nTHead.cloneNode(true);
		oSetDT.nTable.insertBefore( nTheadSize, oSetDT.nTable.childNodes[0] );
		
		if ( oSetDT.nTFoot !== null )
		{
			nTfootSize = oSetDT.nTFoot.cloneNode(true);
			oSetDT.nTable.insertBefore( nTfootSize, oSetDT.nTable.childNodes[1] );
		}
		
		/* Now adjust the table's viewport so we can actually see it */
		if ( oSetDT.oScroll.sX !== "" )
		{
			oSetDT.nTable.style.width = $(oSetDT.nTable).outerWidth()+"px";
			nScrollBody.style.width = $(oSetDT.nTable).outerWidth()+"px";
			nScrollBody.style.overflow = "visible";
		}
		
		if ( oSetDT.oScroll.sY !== "" )
		{
			nScrollBody.style.height = $(oSetDT.nTable).outerHeight()+"px";
			nScrollBody.style.overflow = "visible";
		}
	},
	
	
	/**
	 * Take account of scrolling in DataTables by showing the full table. Note that the redraw of
	 * the DataTable that we do will actually deal with the majority of the hardword here
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintScrollEnd": function ()
	{
		var 
			oSetDT = this.s.dt,
			nScrollBody = oSetDT.nTable.parentNode;
		
		if ( oSetDT.oScroll.sX !== "" )
		{
			nScrollBody.style.width = oSetDT.oApi._fnStringToCss( oSetDT.oScroll.sX );
			nScrollBody.style.overflow = "auto";
		}
		
		if ( oSetDT.oScroll.sY !== "" )
		{
			nScrollBody.style.height = oSetDT.oApi._fnStringToCss( oSetDT.oScroll.sY );
			nScrollBody.style.overflow = "auto";
		}
	},
	
	
	/**
	 * Resume the display of all TableTools hidden nodes
	 *  @method  _fnPrintShowNodes
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintShowNodes": function ( )
	{
	  var anHidden = this.dom.print.hidden;
	  
		for ( var i=0, iLen=anHidden.length ; i<iLen ; i++ )
		{
			anHidden[i].node.style.display = anHidden[i].display;
		}
		anHidden.splice( 0, anHidden.length );
	},
	
	
	/**
	 * Hide nodes which are not needed in order to display the table. Note that this function is
	 * recursive
	 *  @method  _fnPrintHideNodes
	 *  @param   {Node} nNode Element which should be showing in a 'print' display
	 *  @returns void
	 *  @private 
	 */
	"_fnPrintHideNodes": function ( nNode )
	{
	  var anHidden = this.dom.print.hidden;
	  
		var nParent = nNode.parentNode;
		var nChildren = nParent.childNodes;
		for ( var i=0, iLen=nChildren.length ; i<iLen ; i++ )
		{
			if ( nChildren[i] != nNode && nChildren[i].nodeType == 1 )
			{
				/* If our node is shown (don't want to show nodes which were previously hidden) */
				var sDisplay = $(nChildren[i]).css("display");
			 	if ( sDisplay != "none" )
				{
					/* Cache the node and it's previous state so we can restore it */
					anHidden.push( {
						"node": nChildren[i],
						"display": sDisplay
					} );
					nChildren[i].style.display = "none";
				}
			}
		}
		
		if ( nParent.nodeName != "BODY" )
		{
			this._fnPrintHideNodes( nParent );
		}
	}
};



/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Static variables
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**
 * Store of all instances that have been created of TableTools, so one can look up other (when
 * there is need of a master)
 *  @property _aInstances
 *  @type	 Array
 *  @default  []
 *  @private
 */
TableTools._aInstances = [];


/**
 * Store of all listeners and their callback functions
 *  @property _aListeners
 *  @type	 Array
 *  @default  []
 */
TableTools._aListeners = [];



/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Static methods
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**
 * Get an array of all the master instances
 *  @method  fnGetMasters
 *  @returns {Array} List of master TableTools instances
 *  @static
 */
TableTools.fnGetMasters = function ()
{
	var a = [];
	for ( var i=0, iLen=TableTools._aInstances.length ; i<iLen ; i++ )
	{
		if ( TableTools._aInstances[i].s.master )
		{
			a.push( TableTools._aInstances[i] );
		}
	}
	return a;
};

/**
 * Get the master instance for a table node (or id if a string is given)
 *  @method  fnGetInstance
 *  @returns {Object} ID of table OR table node, for which we want the TableTools instance
 *  @static
 */
TableTools.fnGetInstance = function ( node )
{
	if ( typeof node != 'object' )
	{
		node = document.getElementById(node);
	}
	
	for ( var i=0, iLen=TableTools._aInstances.length ; i<iLen ; i++ )
	{
		if ( TableTools._aInstances[i].s.master && TableTools._aInstances[i].dom.table == node )
		{
			return TableTools._aInstances[i];
		}
	}
	return null;
};


/**
 * Add a listener for a specific event
 *  @method  _fnEventListen
 *  @param   {Object} that Scope of the listening function (i.e. 'this' in the caller)
 *  @param   {String} type Event type
 *  @param   {Function} fn Function
 *  @returns void
 *  @private
 *  @static
 */
TableTools._fnEventListen = function ( that, type, fn )
{
	TableTools._aListeners.push( {
		"that": that,
		"type": type,
		"fn": fn
	} );
};
	

/**
 * An event has occured - look up every listener and fire it off. We check that the event we are
 * going to fire is attached to the same table (using the table node as reference) before firing
 *  @method  _fnEventDispatch
 *  @param   {Object} that Scope of the listening function (i.e. 'this' in the caller)
 *  @param   {String} type Event type
 *  @param   {Node} node Element that the event occured on (may be null)
 *  @returns void
 *  @private
 *  @static
 */
TableTools._fnEventDispatch = function ( that, type, node )
{
	var listeners = TableTools._aListeners;
	for ( var i=0, iLen=listeners.length ; i<iLen ; i++ )
	{
		if ( that.dom.table == listeners[i].that.dom.table && listeners[i].type == type )
		{
			listeners[i].fn( node );
		}
	}
};






/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Constants
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */


/**
 * @namespace Default button configurations
 */
TableTools.BUTTONS = {
	"csv": {
		"sAction": "flash_save",
		"sCharSet": "utf8",
		"bBomInc": false,
		"sFileName": "*.csv",
		"sFieldBoundary": '"',
		"sFieldSeperator": ",",
		"sNewLine": "auto",
		"sTitle": "",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_csv",
		"sButtonClassHover": "DTTT_button_csv_hover",
		"sButtonText": "CSV",
		"mColumns": "all", /* "all", "visible", "hidden" or array of column integers */
		"bHeader": true,
		"bFooter": true,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		},
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"xls": {
		"sAction": "flash_save",
		"sCharSet": "utf16le",
		"bBomInc": true,
		"sFileName": "*.csv",
		"sFieldBoundary": "",
		"sFieldSeperator": "\t",
		"sNewLine": "auto",
		"sTitle": "",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_xls",
		"sButtonClassHover": "DTTT_button_xls_hover",
		"sButtonText": "Excel",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		},
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"copy": {
		"sAction": "flash_copy",
		"sFieldBoundary": "",
		"sFieldSeperator": "\t",
		"sNewLine": "auto",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_copy",
		"sButtonClassHover": "DTTT_button_copy_hover",
		"sButtonText": "Copy",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, this.fnGetTableData(oConfig) );
		},
		"fnSelect": null,
		"fnComplete": function(nButton, oConfig, flash, text) {
			var
				lines = text.split('\n').length,
				len = this.s.dt.nTFoot === null ? lines-1 : lines-2,
				plural = (len==1) ? "" : "s";
			alert( 'Copied '+len+' row'+plural+' to the clipboard' );
		},
		"fnInit": null,
		"fnCellRender": null
	},
	"pdf": {
		"sAction": "flash_pdf",
		"sFieldBoundary": "",
		"sFieldSeperator": "\t",
		"sNewLine": "\n",
		"sFileName": "*.pdf",
		"sToolTip": "",
		"sTitle": "",
		"sButtonClass": "DTTT_button_pdf",
		"sButtonClassHover": "DTTT_button_pdf_hover",
		"sButtonText": "PDF",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": false,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"sPdfOrientation": "portrait",
		"sPdfSize": "A4",
		"sPdfMessage": "",
		"fnClick": function( nButton, oConfig, flash ) {
			this.fnSetText( flash, 
				"title:"+ this.fnGetTitle(oConfig) +"\n"+
				"message:"+ oConfig.sPdfMessage +"\n"+
				"colWidth:"+ this.fnCalcColRatios(oConfig) +"\n"+
				"orientation:"+ oConfig.sPdfOrientation +"\n"+
				"size:"+ oConfig.sPdfSize +"\n"+
				"--/TableToolsOpts--\n" +
				this.fnGetTableData(oConfig)
			);
		},
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"print": {
		"sAction": "print",
		"sInfo": "<h6>Print view</h6><p>Please use your browser's print function to "+
		  "print this table. Press escape when finished.",
		"sMessage": "",
		"bShowAll": true,
		"sToolTip": "View print view",
		"sButtonClass": "DTTT_button_print",
		"sButtonClassHover": "DTTT_button_print_hover",
		"sButtonText": "Print",
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": null,
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"text": {
		"sAction": "text",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Text button",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": null,
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"select": {
		"sAction": "text",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Select button",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": null,
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length !== 0 ) {
				$(nButton).removeClass('DTTT_disabled');
			} else {
				$(nButton).addClass('DTTT_disabled');
			}
		},
		"fnComplete": null,
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass('DTTT_disabled');
		},
		"fnCellRender": null
	},
	"select_single": {
		"sAction": "text",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Select button",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": null,
		"fnSelect": function( nButton, oConfig ) {
			var iSelected = this.fnGetSelected().length;
			if ( iSelected == 1 ) {
				$(nButton).removeClass('DTTT_disabled');
			} else {
				$(nButton).addClass('DTTT_disabled');
			}
		},
		"fnComplete": null,
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass('DTTT_disabled');
		},
		"fnCellRender": null
	},
	"select_all": {
		"sAction": "text",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Select all",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig ) {
			this.fnSelectAll();
		},
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length == this.s.dt.fnRecordsDisplay() ) {
				$(nButton).addClass('DTTT_disabled');
			} else {
				$(nButton).removeClass('DTTT_disabled');
			}
		},
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	},
	"select_none": {
		"sAction": "text",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Deselect all",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig ) {
			this.fnSelectNone();
		},
		"fnSelect": function( nButton, oConfig ) {
			if ( this.fnGetSelected().length !== 0 ) {
				$(nButton).removeClass('DTTT_disabled');
			} else {
				$(nButton).addClass('DTTT_disabled');
			}
		},
		"fnComplete": null,
		"fnInit": function( nButton, oConfig ) {
			$(nButton).addClass('DTTT_disabled');
		},
		"fnCellRender": null
	},
	"ajax": {
		"sAction": "text",
		"sFieldBoundary": "",
		"sFieldSeperator": "\t",
		"sNewLine": "\n",
		"sAjaxUrl": "/xhr.php",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_text",
		"sButtonClassHover": "DTTT_button_text_hover",
		"sButtonText": "Ajax button",
		"mColumns": "all",
		"bHeader": true,
		"bFooter": true,
		"bSelectedOnly": false,
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig ) {
			var sData = this.fnGetTableData(oConfig);
			$.ajax( {
				"url": oConfig.sAjaxUrl,
				"data": [
					{ "name": "tableData", "value": sData }
				],
				"success": oConfig.fnAjaxComplete,
				"dataType": "json",
				"type": "POST", 
				"cache": false,
				"error": function () {
					alert( "Error detected when sending table data to server" );
				}
			} );
		},
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnAjaxComplete": function( json ) {
			alert( 'Ajax complete' );
		},
		"fnCellRender": null
	},
	"div": {
		"sAction": "div",
		"sToolTip": "",
		"sButtonClass": "DTTT_nonbutton",
		"sButtonClassHover": "",
		"sButtonText": "Text button",
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": null,
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"nContent": null,
		"fnCellRender": null
	},
	"collection": {
		"sAction": "collection",
		"sToolTip": "",
		"sButtonClass": "DTTT_button_collection",
		"sButtonClassHover": "DTTT_button_collection_hover",
		"sButtonText": "Collection",
		"fnMouseover": null,
		"fnMouseout": null,
		"fnClick": function( nButton, oConfig ) {
			this._fnCollectionShow(nButton, oConfig);
		},
		"fnSelect": null,
		"fnComplete": null,
		"fnInit": null,
		"fnCellRender": null
	}
};
/*
 *  on* callback parameters:
 *  	1. node - button element
 *  	2. object - configuration object for this button
 *  	3. object - ZeroClipboard reference (flash button only)
 *  	4. string - Returned string from Flash (flash button only - and only on 'complete')
 */


/**
 * @namespace TableTools default settings for initialisation
 */
TableTools.DEFAULTS = {
	"sSwfPath":        "media/swf/copy_csv_xls_pdf.swf",
	"sRowSelect":      "none",
	"sSelectedClass":  "DTTT_selected",
	"fnPreRowSelect":  null,
	"fnRowSelected":   null,
	"fnRowDeselected": null,
	"aButtons":        [ "copy", "csv", "xls", "pdf", "print" ]
};


/**
 * Name of this class
 *  @constant CLASS
 *  @type	 String
 *  @default  TableTools
 */
TableTools.prototype.CLASS = "TableTools";


/**
 * TableTools version
 *  @constant  VERSION
 *  @type	  String
 *  @default   2.0.3.dev
 */
TableTools.VERSION = "2.0.3";
TableTools.prototype.VERSION = TableTools.VERSION;




/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Initialisation
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/*
 * Register a new feature with DataTables
 */
if ( typeof $.fn.dataTable == "function" &&
	 typeof $.fn.dataTableExt.fnVersionCheck == "function" &&
	 $.fn.dataTableExt.fnVersionCheck('1.8.2') )
{
	$.fn.dataTableExt.aoFeatures.push( {
		"fnInit": function( oDTSettings ) {
			var oOpts = typeof oDTSettings.oInit.oTableTools != 'undefined' ? 
				oDTSettings.oInit.oTableTools : {};
			
			var oTT = new TableTools( oDTSettings.oInstance, oOpts );
			TableTools._aInstances.push( oTT );
			
			return oTT.dom.container;
		},
		"cFeature": "T",
		"sFeature": "TableTools"
	} );
}
else
{
	alert( "Warning: TableTools 2 requires DataTables 1.8.2 or newer - www.datatables.net/download");
}

})(jQuery, window, document);

/*
* File:        jquery.dataTables.columnFilter.js
* Version:     1.4.7.
* Author:      Jovan Popovic
*
* Copyright 2011-2012 Jovan Popovic, all rights reserved.
*
* This source file is free software, under either the GPL v2 license or a
* BSD style license, as supplied with this software.
*
* This source file is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
* or FITNESS FOR A PARTICULAR PURPOSE.
*
* Parameters:"
* @sPlaceHolder                 String      Place where inline filtering function should be placed ("tfoot", "thead:before", "thead:after"). Default is "tfoot"
* @sRangeSeparator              String      Separator that will be used when range values are sent to the server-side. Default value is "~".
* @sRangeFormat                 string      Default format of the From ... to ... range inputs. Default is From {from} to {to}
* @aoColumns                    Array       Array of the filter settings that will be applied on the columns
*/
(function ($) {


    $.fn.columnFilter = function (options) {

        var asInitVals, i, label, th;

        //var sTableId = "table";
        var sRangeFormat = "From {from} to {to}";
        //Array of the functions that will override sSearch_ parameters
        var afnSearch_ = new Array();
        var aiCustomSearch_Indexes = new Array();

        var oFunctionTimeout = null;

        var fnOnFiltered = function () { };

        function _fnGetColumnValues(oSettings, iColumn, bUnique, bFiltered, bIgnoreEmpty) {
            ///<summary>
            ///Return values in the column
            ///</summary>
            ///<param name="oSettings" type="Object">DataTables settings</param>
            ///<param name="iColumn" type="int">Id of the column</param>
            ///<param name="bUnique" type="bool">Return only distinct values</param>
            ///<param name="bFiltered" type="bool">Return values only from the filtered rows</param>
            ///<param name="bIgnoreEmpty" type="bool">Ignore empty cells</param>

            // check that we have a column id
            if (typeof iColumn == "undefined") return new Array();

            // by default we only wany unique data
            if (typeof bUnique == "undefined") bUnique = true;

            // by default we do want to only look at filtered data
            if (typeof bFiltered == "undefined") bFiltered = true;

            // by default we do not wany to include empty values
            if (typeof bIgnoreEmpty == "undefined") bIgnoreEmpty = true;

            // list of rows which we're going to loop through
            var aiRows;

            // use only filtered rows
            if (bFiltered == true) aiRows = oSettings.aiDisplay;
            // use all rows
            else aiRows = oSettings.aiDisplayMaster; // all row numbers

            // set up data array
            var asResultData = new Array();

            for (var i = 0, c = aiRows.length; i < c; i++) {
                iRow = aiRows[i];
                var aData = oTable.fnGetData(iRow);
                var sValue = aData[iColumn];

                // ignore empty values?
                if (bIgnoreEmpty == true && sValue.length == 0) continue;

                // ignore unique values?
                else if (bUnique == true && jQuery.inArray(sValue, asResultData) > -1) continue;

                // else push the value onto the result data array
                else asResultData.push(sValue);
            }

            return asResultData.sort();
        }

        function _fnColumnIndex(iColumnIndex) {
            if (properties.bUseColVis)
                return iColumnIndex;
            else
                return oTable.fnSettings().oApi._fnVisibleToColumnIndex(oTable.fnSettings(), iColumnIndex);
            //return iColumnIndex;
            //return oTable.fnSettings().oApi._fnColumnIndexToVisible(oTable.fnSettings(), iColumnIndex);
        }

        function fnCreateInput(oTable, regex, smart, bIsNumber, iFilterLength, iMaxLenght) {
            var sCSSClass = "text_filter";
            if (bIsNumber)
                sCSSClass = "number_filter";

            label = label.replace(/(^\s*)|(\s*$)/g, "");
            var currentFilter = oTable.fnSettings().aoPreSearchCols[i].sSearch;
            var search_init = 'search_init ';
            var inputvalue = label;
            if (currentFilter != '' && currentFilter != '^') {
                if (bIsNumber && currentFilter.charAt(0) == '^')
                    inputvalue = currentFilter.substr(1); //ignore trailing ^
                else
                    inputvalue = currentFilter;
                search_init = '';
            }

            var input = $('<input type="text" class="' + search_init + sCSSClass + '" value="' + inputvalue + '"/>');
            if (iMaxLenght != undefined && iMaxLenght != -1) {
                input.attr('maxlength', iMaxLenght);
            }
            th.html(input);
            if (bIsNumber)
                th.wrapInner('<span class="filter_column filter_number" />');
            else
                th.wrapInner('<span class="filter_column filter_text" />');

            asInitVals[i] = label;
            var index = i;

            if (bIsNumber && !oTable.fnSettings().oFeatures.bServerSide) {
                input.keyup(function () {
                    /* Filter on the column all numbers that starts with the entered value */
                    oTable.fnFilter('^' + this.value, _fnColumnIndex(index), true, false); //Issue 37
                    fnOnFiltered();
                });
            } else {
                input.keyup(function () {
                    if (oTable.fnSettings().oFeatures.bServerSide && iFilterLength != 0) {
                        //If filter length is set in the server-side processing mode
                        //Check has the user entered at least iFilterLength new characters

                        var currentFilter = oTable.fnSettings().aoPreSearchCols[index].sSearch;
                        var iLastFilterLength = $(this).data("dt-iLastFilterLength");
                        if (typeof iLastFilterLength == "undefined")
                            iLastFilterLength = 0;
                        var iCurrentFilterLength = this.value.length;
                        if (Math.abs(iCurrentFilterLength - iLastFilterLength) < iFilterLength
                        //&& currentFilter.length == 0 //Why this?
					        ) {
                            //Cancel the filtering
                            return;
                        }
                        else {
                            //Remember the current filter length
                            $(this).data("dt-iLastFilterLength", iCurrentFilterLength);
                        }
                    }
                    /* Filter on the column (the index) of this element */
                    oTable.fnFilter(this.value, _fnColumnIndex(index), regex, smart); //Issue 37
                    fnOnFiltered();
                });
            }

            input.focus(function () {
                if ($(this).hasClass("search_init")) {
                    $(this).removeClass("search_init");
                    this.value = "";
                }
            });
            input.blur(function () {
                if (this.value == "") {
                    $(this).addClass("search_init");
                    this.value = asInitVals[index];
                }
            });
        }

        function fnCreateRangeInput(oTable) {

            th.html(_fnRangeLabelPart(0));
            var sFromId = oTable.attr("id") + '_range_from_' + i;
            var from = $('<input type="text" class="number_range_filter" id="' + sFromId + '" rel="' + i + '"/>');
            th.append(from);
            th.append(_fnRangeLabelPart(1));
            var sToId = oTable.attr("id") + '_range_to_' + i;
            var to = $('<input type="text" class="number_range_filter" id="' + sToId + '" rel="' + i + '"/>');
            th.append(to);
            th.append(_fnRangeLabelPart(2));
            th.wrapInner('<span class="filterColumn filter_number_range" />');
            var index = i;
            aiCustomSearch_Indexes.push(i);



            //------------start range filtering function


            /* 	Custom filtering function which will filter data in column four between two values
            *	Author: 	Allan Jardine, Modified by Jovan Popovic
            */
            //$.fn.dataTableExt.afnFiltering.push(
            oTable.dataTableExt.afnFiltering.push(
	        function (oSettings, aData, iDataIndex) {
	            if (oTable.attr("id") != oSettings.sTableId)
	                return true;
	            // Try to handle missing nodes more gracefully
	            if (document.getElementById(sFromId) == null)
	                return true;
	            var iMin = document.getElementById(sFromId).value * 1;
	            var iMax = document.getElementById(sToId).value * 1;
	            var iValue = aData[_fnColumnIndex(index)] == "-" ? 0 : aData[_fnColumnIndex(index)] * 1;
	            if (iMin == "" && iMax == "") {
	                return true;
	            }
	            else if (iMin == "" && iValue <= iMax) {
	                return true;
	            }
	            else if (iMin <= iValue && "" == iMax) {
	                return true;
	            }
	            else if (iMin <= iValue && iValue <= iMax) {
	                return true;
	            }
	            return false;
	        }
        );
            //------------end range filtering function



            $('#' + sFromId + ',#' + sToId, th).keyup(function () {

                var iMin = document.getElementById(sFromId).value * 1;
                var iMax = document.getElementById(sToId).value * 1;
                if (iMin != 0 && iMax != 0 && iMin > iMax)
                    return;

                oTable.fnDraw();
                fnOnFiltered();
            });


        }


        function fnCreateDateRangeInput(oTable) {
            th.html(_fnRangeLabelPart(0));
            var sFromId = oTable.attr("id") + '_range_from_' + i;
            var from = $('<input type="text" class="date_range_filter" id="' + sFromId + '" rel="' + i + '"/>');
            from.datepicker();
            th.append(from);
            th.append(_fnRangeLabelPart(1));
            var sToId = oTable.attr("id") + '_range_to_' + i;
            var to = $('<input type="text" class="date_range_filter" id="' + sToId + '" rel="' + i + '"/>');
            th.append(to);
            th.append(_fnRangeLabelPart(2));
            th.wrapInner('<span class="filterColumn filter_date_range" />');
            to.datepicker();
            var index = i;
            aiCustomSearch_Indexes.push(i);


            //------------start date range filtering function

            //$.fn.dataTableExt.afnFiltering.push(
            oTable.dataTableExt.afnFiltering.push(
	        function (oSettings, aData, iDataIndex) {
	            if (oTable.attr("id") != oSettings.sTableId)
	                return true;

	            var dStartDate = from.datepicker("getDate");

	            var dEndDate = to.datepicker("getDate");

	            if (dStartDate == null && dEndDate == null) {
	                return true;
	            }

	            var dCellDate = null;
	            try {
	                if (aData[_fnColumnIndex(index)] == null || aData[_fnColumnIndex(index)] == "")
	                    return false;
	                dCellDate = $.datepicker.parseDate($.datepicker.regional[""].dateFormat, aData[_fnColumnIndex(index)]);
	            } catch (ex) {
	                return false;
	            }
	            if (dCellDate == null)
	                return false;


	            if (dStartDate == null && dCellDate <= dEndDate) {
	                return true;
	            }
	            else if (dStartDate <= dCellDate && dEndDate == null) {
	                return true;
	            }
	            else if (dStartDate <= dCellDate && dCellDate <= dEndDate) {
	                return true;
	            }
	            return false;
	        }
        );
            //------------end date range filtering function

            $('#' + sFromId + ',#' + sToId, th).change(function () {
                oTable.fnDraw();
                fnOnFiltered();
            });


        }

        function fnCreateColumnSelect(oTable, aData, iColumn, nTh, sLabel, bRegex) {
            if (aData == null)
                aData = _fnGetColumnValues(oTable.fnSettings(), iColumn, true, false, true);
            var index = iColumn;
            var currentFilter = oTable.fnSettings().aoPreSearchCols[i].sSearch;

            var r = '<select class="search_init select_filter"><option value="" class="search_init">' + sLabel + '</option>';
            var j = 0;
            var iLen = aData.length;
            for (j = 0; j < iLen; j++) {
                if (typeof (aData[j]) != 'object') {
                    var selected = '';
                    if (escape(aData[j]) == currentFilter) selected = 'selected '
                    r += '<option ' + selected + ' value="' + escape(aData[j]) + '">' + aData[j] + '</option>';
                }
                else {
                    var selected = '';
                    if (bRegex) {
                        //Do not escape values if they are explicitely set to avoid escaping special characters in the regexp
                        if (aData[j].value == currentFilter) selected = 'selected ';
                        r += '<option ' + selected + 'value="' + aData[j].value + '">' + aData[j].label + '</option>';
                    } else {
                        if (escape(aData[j].value) == currentFilter) selected = 'selected ';
                        r += '<option ' + selected + 'value="' + escape(aData[j].value) + '">' + aData[j].label + '</option>';
                    }
                }
            }

            var select = $(r + '</select>');
            nTh.html(select);
            nTh.wrapInner('<span class="filterColumn filter_select" />');
            select.change(function () {
                //var val = $(this).val();
                if ($(this).val() != "") {
                    $(this).removeClass("search_init");
                } else {
                    $(this).addClass("search_init");
                }
                if (bRegex)
                    oTable.fnFilter($(this).val(), iColumn, bRegex); //Issue 41
                else
                    oTable.fnFilter(unescape($(this).val()), iColumn); //Issue 25
                fnOnFiltered();
            });
        }

        function fnCreateSelect(oTable, aData, bRegex) {
            var oSettings = oTable.fnSettings();
            if (aData == null && oSettings.sAjaxSource != "" && !oSettings.oFeatures.bServerSide) {
                // Add a function to the draw callback, which will check for the Ajax data having
                // been loaded. Use a closure for the individual column elements that are used to
                // built the column filter, since 'i' and 'th' (etc) are locally "global".
                oSettings.aoDrawCallback.push({
                    "fn": (function (iColumn, nTh, sLabel) {
                        return function () {
                            // Only rebuild the select on the second draw - i.e. when the Ajax
                            // data has been loaded.
                            if (oSettings.iDraw == 2 && oSettings.sAjaxSource != null && oSettings.sAjaxSource != "" && !oSettings.oFeatures.bServerSide) {
                                return fnCreateColumnSelect(oTable, null, _fnColumnIndex(iColumn), nTh, sLabel, bRegex); //Issue 37
                            }
                        };
                    })(i, th, label),
                    "sName": "column_filter_" + i
                });
            }
            // Regardless of the Ajax state, build the select on first pass
            fnCreateColumnSelect(oTable, aData, _fnColumnIndex(i), th, label, bRegex); //Issue 37

        }

        function fnCreateCheckbox(oTable, aData) {

            if (aData == null)
                aData = _fnGetColumnValues(oTable.fnSettings(), i, true, true, true);
            var index = i;

            var r = '', j, iLen = aData.length;

            //clean the string
            var localLabel = label.replace('%', 'Perc').replace("&", "AND").replace("$", "DOL").replace("£", "STERL").replace("@", "AT").replace(/\s/g, "_");
            localLabel = localLabel.replace(/[^a-zA-Z 0-9]+/g, '');
            //clean the string

            //button label override
            if (properties.sFilterButtonText != null || properties.sFilterButtonText != undefined) {
                labelBtn = properties.sFilterButtonText;
            } else {
                labelBtn = label;
            }

            var relativeDivWidthToggleSize = 10;
            var numRow = 12; //numero di checkbox per colonna
            var numCol = Math.floor(iLen / numRow);
            if (iLen % numRow > 0) {
                numCol = numCol + 1;
            };

            //count how many column should be generated and split the div size
            var divWidth = 100 / numCol - 2;

            var divWidthToggle = relativeDivWidthToggleSize * numCol;

            if (numCol == 1) {
                divWidth = 20;
            }

            var divRowDef = '<div style="float:left; min-width: ' + divWidth + '%; " >';
            var divClose = '</div>';

            var uniqueId = oTable.attr("id") + localLabel;
            var buttonId = "chkBtnOpen" + uniqueId;
            var checkToggleDiv = uniqueId + "-flt-toggle";
            r += '<button id="' + buttonId + '" class="checkbox_filter" > ' + labelBtn + '</button>'; //filter button witch open dialog
            r += '<div id="' + checkToggleDiv + '" '
            	+ 'title="' + label + '" '
            	+ 'class="toggle-check ui-widget-content ui-corner-all"  style="width: ' + (divWidthToggle) + '%; " >'; //dialog div
            //r+= '<div align="center" style="margin-top: 5px; "> <button id="'+buttonId+'Reset" class="checkbox_filter" > reset </button> </div>'; //reset button and its div
            r += divRowDef;

            for (j = 0; j < iLen; j++) {

                //if last check close div
                if (j % numRow == 0 && j != 0) {
                    r += divClose + divRowDef;
                }

                //check button
                r += '<input class="search_init checkbox_filter" type="checkbox" id= "' + aData[j] + '" name= "' + localLabel + '" value="' + aData[j] + '" >' + aData[j] + '<br/>';

                var checkbox = $(r);
                th.html(checkbox);
                th.wrapInner('<span class="filterColumn filter_checkbox" />');
                //on every checkbox selection
                checkbox.change(function () {

                    var search = '';
                    var or = '|'; //var for select checks in 'or' into the regex
                    var resSize = $('input:checkbox[name="' + localLabel + '"]:checked').size();
                    $('input:checkbox[name="' + localLabel + '"]:checked').each(function (index) {

                        //search = search + ' ' + $(this).val();
                        //concatenation for selected checks in or
                        if ((index == 0 && resSize == 1)
                				|| (index != 0 && index == resSize - 1)) {
                            or = '';
                        }
                        //trim
                        search = search.replace(/^\s+|\s+$/g, "");
                        search = search + $(this).val() + or;
                        or = '|';

                    });

                    for (var jj = 0; jj < iLen; jj++) {
                        if (search != "") {
                            $('#' + aData[jj]).removeClass("search_init");
                        } else {
                            $('#' + aData[jj]).addClass("search_init");
                        }
                    }

                    //execute search
                    oTable.fnFilter(search, index, true, false);
                    fnOnFiltered();
                });
            }

            //filter button
            $('#' + buttonId).button();
            //dialog
            $('#' + checkToggleDiv).dialog({
                //height: 140,
                autoOpen: false,
                //show: "blind",
                hide: "blind",
                buttons: [{
                    text: "Reset",
                    click: function () {
                        //$('#'+buttonId).removeClass("filter_selected"); //LM remove border if filter selected
                        $('input:checkbox[name="' + localLabel + '"]:checked').each(function (index3) {
                            $(this).attr('checked', false);
                            $(this).addClass("search_init");
                        });
                        oTable.fnFilter('', index, true, false);
                        fnOnFiltered();
                        return false;
                    }
                },
							{
							    text: "Close",
							    click: function () { $(this).dialog("close"); }
							}
						]
            });


            $('#' + buttonId).click(function () {

                $('#' + checkToggleDiv).dialog('open');
                var target = $(this);
                $('#' + checkToggleDiv).dialog("widget").position({ my: 'top',
                    at: 'bottom',
                    of: target
                });

                return false;
            });

            var fnOnFilteredCurrent = fnOnFiltered;

            fnOnFiltered = function () {
                var target = $('#' + buttonId);
                $('#' + checkToggleDiv).dialog("widget").position({ my: 'top',
                    at: 'bottom',
                    of: target
                });
                fnOnFilteredCurrent();
            };
            //reset
            /*
            $('#'+buttonId+"Reset").button();
            $('#'+buttonId+"Reset").click(function(){
            $('#'+buttonId).removeClass("filter_selected"); //LM remove border if filter selected
            $('input:checkbox[name="'+localLabel+'"]:checked').each(function(index3) {
            $(this).attr('checked', false);
            $(this).addClass("search_init");
            });
            oTable.fnFilter('', index, true, false);
            return false;
            });
            */
        }




        function _fnRangeLabelPart(iPlace) {
            switch (iPlace) {
                case 0:
                    return sRangeFormat.substring(0, sRangeFormat.indexOf("{from}"));
                case 1:
                    return sRangeFormat.substring(sRangeFormat.indexOf("{from}") + 6, sRangeFormat.indexOf("{to}"));
                default:
                    return sRangeFormat.substring(sRangeFormat.indexOf("{to}") + 4);
            }
        }




        oTable = this;

        var defaults = {
            sPlaceHolder: "foot",
            sRangeSeparator: "~",
            iFilteringDelay: 500,
            aoColumns: null,
            sRangeFormat: "From {from} to {to}"
        };

        properties = $.extend(defaults, options);

        return this.each(function () {

            if (!oTable.fnSettings().oFeatures.bFilter)
                return;
            asInitVals = new Array();

            aoFilterCells = oTable.fnSettings().aoFooter[0];

            var oHost = oTable.fnSettings().nTFoot; //Before fix for ColVis
            var sFilterRow = "tr"; //Before fix for ColVis

            if (properties.sPlaceHolder == "head:after") {
                var tr = $("tr:first", oTable.fnSettings().nTHead).detach();
                //tr.appendTo($(oTable.fnSettings().nTHead));
                if (oTable.fnSettings().bSortCellsTop) {
                    tr.prependTo($(oTable.fnSettings().nTHead));
                    //tr.appendTo($("thead", oTable));
                    aoFilterCells = oTable.fnSettings().aoHeader[1];
                }
                else {
                    tr.appendTo($(oTable.fnSettings().nTHead));
                    //tr.prependTo($("thead", oTable));
                    aoFilterCells = oTable.fnSettings().aoHeader[0];
                }

                sFilterRow = "tr:last";
                oHost = oTable.fnSettings().nTHead;

            } else if (properties.sPlaceHolder == "head:before") {

                if (oTable.fnSettings().bSortCellsTop) {
                    var tr = $("tr:first", oTable.fnSettings().nTHead).detach();
                    tr.appendTo($(oTable.fnSettings().nTHead));
                    aoFilterCells = oTable.fnSettings().aoHeader[1];
                } else {
                    aoFilterCells = oTable.fnSettings().aoHeader[0];
                }
                /*else {
                //tr.prependTo($("thead", oTable));
                sFilterRow = "tr:first";
                }*/

                sFilterRow = "tr:first";

                oHost = oTable.fnSettings().nTHead;


            }

            //$(sFilterRow + " th", oHost).each(function (index) {//bug with ColVis
            $(aoFilterCells).each(function (index) {//fix for ColVis
                i = index;
                var aoColumn = { type: "text",
                    bRegex: false,
                    bSmart: true,
                    iMaxLenght: -1,
                    iFilterLength: 0
                };
                if (properties.aoColumns != null) {
                    if (properties.aoColumns.length < i || properties.aoColumns[i] == null)
                        return;
                    aoColumn = properties.aoColumns[i];
                }
                //label = $(this).text(); //Before fix for ColVis
                label = $($(this)[0].cell).text(); //Fix for ColVis
                if (aoColumn.sSelector == null) {
                    //th = $($(this)[0]);//Before fix for ColVis
                    th = $($(this)[0].cell); //Fix for ColVis
                }
                else {
                    th = $(aoColumn.sSelector);
                    if (th.length == 0)
                        th = $($(this)[0].cell);
                }

                if (aoColumn != null) {
                    if (aoColumn.sRangeFormat != null)
                        sRangeFormat = aoColumn.sRangeFormat;
                    else
                        sRangeFormat = properties.sRangeFormat;
                    switch (aoColumn.type) {
                        case "null":
                            break;
                        case "number":
                            fnCreateInput(oTable, true, false, true, aoColumn.iFilterLength, aoColumn.iMaxLenght);
                            break;
                        case "select":
                            if (aoColumn.bRegex != true)
                                aoColumn.bRegex = false;
                            fnCreateSelect(oTable, aoColumn.values, aoColumn.bRegex);
                            break;
                        case "number-range":
                            fnCreateRangeInput(oTable);
                            break;
                        case "date-range":
                            fnCreateDateRangeInput(oTable);
                            break;
                        case "checkbox":
                            fnCreateCheckbox(oTable, aoColumn.values);
                            break;
                        case "text":
                        default:
                            bRegex = (aoColumn.bRegex == null ? false : aoColumn.bRegex);
                            bSmart = (aoColumn.bSmart == null ? false : aoColumn.bSmart);
                            fnCreateInput(oTable, bRegex, bSmart, false, aoColumn.iFilterLength, aoColumn.iMaxLenght);
                            break;

                    }
                }
            });

            for (j = 0; j < aiCustomSearch_Indexes.length; j++) {
                //var index = aiCustomSearch_Indexes[j];
                var fnSearch_ = function () {
                    var id = oTable.attr("id");
                    return $("#" + id + "_range_from_" + aiCustomSearch_Indexes[j]).val() + properties.sRangeSeparator + $("#" + id + "_range_to_" + aiCustomSearch_Indexes[j]).val()
                }
                afnSearch_.push(fnSearch_);
            }

            if (oTable.fnSettings().oFeatures.bServerSide) {

                var fnServerDataOriginal = oTable.fnSettings().fnServerData;

                oTable.fnSettings().fnServerData = function (sSource, aoData, fnCallback) {

                    for (j = 0; j < aiCustomSearch_Indexes.length; j++) {
                        var index = aiCustomSearch_Indexes[j];

                        for (k = 0; k < aoData.length; k++) {
                            if (aoData[k].name == "sSearch_" + index)
                                aoData[k].value = afnSearch_[j]();
                        }
                    }
                    aoData.push({ "name": "sRangeSeparator", "value": properties.sRangeSeparator });

                    if (fnServerDataOriginal != null) {
                        try {
                            fnServerDataOriginal(sSource, aoData, fnCallback, oTable.fnSettings()); //TODO: See Issue 18
                        } catch (ex) {
                            fnServerDataOriginal(sSource, aoData, fnCallback);
                        }
                    }
                    else {
                        $.getJSON(sSource, aoData, function (json) {
                            fnCallback(json)
                        });
                    }
                };

            }

        });

    };




})(jQuery);

/*
 * Jeditable - jQuery in place edit plugin
 *
 * Copyright (c) 2006-2009 Mika Tuupola, Dylan Verheul
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.appelsiini.net/projects/jeditable
 *
 * Based on editable by Dylan Verheul <dylan_at_dyve.net>:
 *    http://www.dyve.net/jquery/?editable
 *
 */

/**
  * Version 1.7.1
  *
  * ** means there is basic unit tests for this parameter.
  *
  * @name  Jeditable
  * @type  jQuery
  * @param String  target             (POST) URL or function to send edited content to **
  * @param Hash    options            additional options
  * @param String  options[method]    method to use to send edited content (POST or PUT) **
  * @param Function options[callback] Function to run after submitting edited content **
  * @param String  options[name]      POST parameter name of edited content
  * @param String  options[id]        POST parameter name of edited div id
  * @param Hash    options[submitdata] Extra parameters to send when submitting edited content.
  * @param String  options[type]      text, textarea or select (or any 3rd party input type) **
  * @param Integer options[rows]      number of rows if using textarea **
  * @param Integer options[cols]      number of columns if using textarea **
  * @param Mixed   options[height]    'auto', 'none' or height in pixels **
  * @param Mixed   options[width]     'auto', 'none' or width in pixels **
  * @param String  options[loadurl]   URL to fetch input content before editing **
  * @param String  options[loadtype]  Request type for load url. Should be GET or POST.
  * @param String  options[loadtext]  Text to display while loading external content.
  * @param Mixed   options[loaddata]  Extra parameters to pass when fetching content before editing.
  * @param Mixed   options[data]      Or content given as paramameter. String or function.**
  * @param String  options[indicator] indicator html to show when saving
  * @param String  options[tooltip]   optional tooltip text via title attribute **
  * @param String  options[event]     jQuery event such as 'click' of 'dblclick' **
  * @param String  options[submit]    submit button value, empty means no button **
  * @param String  options[cancel]    cancel button value, empty means no button **
  * @param String  options[cssclass]  CSS class to apply to input form. 'inherit' to copy from parent. **
  * @param String  options[style]     Style to apply to input form 'inherit' to copy from parent. **
  * @param String  options[select]    true or false, when true text is highlighted ??
  * @param String  options[placeholder] Placeholder text or html to insert when element is empty. **
  * @param String  options[onblur]    'cancel', 'submit', 'ignore' or function ??
  *
  * @param Function options[onsubmit] function(settings, original) { ... } called before submit
  * @param Function options[onreset]  function(settings, original) { ... } called before reset
  * @param Function options[onerror]  function(settings, original, xhr) { ... } called on error
  *
  * @param Hash    options[ajaxoptions]  jQuery Ajax options. See docs.jquery.com.
  *
  */

(function($) {

    $.fn.editable = function(target, options) {

        if ('disable' == target) {
            $(this).data('disabled.editable', true);
            return;
        }
        if ('enable' == target) {
            $(this).data('disabled.editable', false);
            return;
        }
        if ('destroy' == target) {
            $(this)
                .unbind($(this).data('event.editable'))
                .removeData('disabled.editable')
                .removeData('event.editable');
            return;
        }

        var settings = $.extend({}, $.fn.editable.defaults, {target:target}, options);

        /* setup some functions */
        var plugin   = $.editable.types[settings.type].plugin || function() { };
        var submit   = $.editable.types[settings.type].submit || function() { };
        var buttons  = $.editable.types[settings.type].buttons
                    || $.editable.types['defaults'].buttons;
        var content  = $.editable.types[settings.type].content
                    || $.editable.types['defaults'].content;
        var element  = $.editable.types[settings.type].element
                    || $.editable.types['defaults'].element;
        var reset    = $.editable.types[settings.type].reset
                    || $.editable.types['defaults'].reset;
        var callback = settings.callback || function() { };
        var onedit   = settings.onedit   || function() { };
        var onsubmit = settings.onsubmit || function() { };
        var onreset  = settings.onreset  || function() { };
        var onerror  = settings.onerror  || reset;

        /* show tooltip */
        if (settings.tooltip) {
            $(this).attr('title', settings.tooltip);
        }

        settings.autowidth  = 'auto' == settings.width;
        settings.autoheight = 'auto' == settings.height;

        return this.each(function() {

            /* save this to self because this changes when scope changes */
            var self = this;

            /* inlined block elements lose their width and height after first edit */
            /* save them for later use as workaround */
            var savedwidth  = $(self).width();
            var savedheight = $(self).height();

            /* save so it can be later used by $.editable('destroy') */
            $(this).data('event.editable', settings.event);

            /* if element is empty add something clickable (if requested) */
            if (!$.trim($(this).html())) {
                $(this).html(settings.placeholder);
            }

            $(this).bind(settings.event, function(e) {

                /* abort if disabled for this element */
                if (true === $(this).data('disabled.editable')) {
                    return;
                }

                /* prevent throwing an exeption if edit field is clicked again */
                if (self.editing) {
                    return;
                }

                /* abort if onedit hook returns false */
                if (false === onedit.apply(this, [settings, self])) {
                   return;
                }

                /* prevent default action and bubbling */
                e.preventDefault();
                e.stopPropagation();

                /* remove tooltip */
                if (settings.tooltip) {
                    $(self).removeAttr('title');
                }

                /* figure out how wide and tall we are, saved width and height */
                /* are workaround for http://dev.jquery.com/ticket/2190 */
                if (0 == $(self).width()) {
                    //$(self).css('visibility', 'hidden');
                    settings.width  = savedwidth;
                    settings.height = savedheight;
                } else {
                    if (settings.width != 'none') {
                        settings.width =
                            settings.autowidth ? $(self).width()  : settings.width;
                    }
                    if (settings.height != 'none') {
                        settings.height =
                            settings.autoheight ? $(self).height() : settings.height;
                    }
                }
                //$(this).css('visibility', '');

                /* remove placeholder text, replace is here because of IE */
                if ($(this).html().toLowerCase().replace(/(;|")/g, '') ==
                    settings.placeholder.toLowerCase().replace(/(;|")/g, '')) {
                        $(this).html('');
                }

                self.editing    = true;
                self.revert     = $(self).html();
                $(self).html('');

                /* create the form object */
                var form = $('<form />');

                /* apply css or style or both */
                if (settings.cssclass) {
                    if ('inherit' == settings.cssclass) {
                        form.attr('class', $(self).attr('class'));
                    } else {
                        form.attr('class', settings.cssclass);
                    }
                }

                if (settings.style) {
                    if ('inherit' == settings.style) {
                        form.attr('style', $(self).attr('style'));
                        /* IE needs the second line or display wont be inherited */
                        form.css('display', $(self).css('display'));
                    } else {
                        form.attr('style', settings.style);
                    }
                }

                /* add main input element to form and store it in input */
                var input = element.apply(form, [settings, self]);

                /* set input content via POST, GET, given data or existing value */
                var input_content;

                if (settings.loadurl) {
                    var t = setTimeout(function() {
                        input.disabled = true;
                        content.apply(form, [settings.loadtext, settings, self]);
                    }, 100);

                    var loaddata = {};
                    loaddata[settings.id] = self.id;
                    if ($.isFunction(settings.loaddata)) {
                        $.extend(loaddata, settings.loaddata.apply(self, [self.revert, settings]));
                    } else {
                        $.extend(loaddata, settings.loaddata);
                    }
                    $.ajax({
                       type : settings.loadtype,
                       url  : settings.loadurl,
                       data : loaddata,
                       async : false,
                       success: function(result) {
                          window.clearTimeout(t);
                          input_content = result;
                          input.disabled = false;
                       }
                    });
                } else if (settings.data) {
                    input_content = settings.data;
                    if ($.isFunction(settings.data)) {
                        input_content = settings.data.apply(self, [self.revert, settings]);
                    }
                } else {
                    input_content = self.revert;
                }
                content.apply(form, [input_content, settings, self]);

                input.attr('name', settings.name);

                /* add buttons to the form */
                buttons.apply(form, [settings, self]);

                /* add created form to self */
                $(self).append(form);

                /* attach 3rd party plugin if requested */
                plugin.apply(form, [settings, self]);

                /* focus to first visible form element */
                $(':input:visible:enabled:first', form).focus();

                /* highlight input contents when requested */
                if (settings.select) {
                    input.select();
                }

                /* discard changes if pressing esc */
                input.keydown(function(e) {
                    if (e.keyCode == 27) {
                        e.preventDefault();
                        //self.reset();
                        reset.apply(form, [settings, self]);
                    }
                });

                /* discard, submit or nothing with changes when clicking outside */
                /* do nothing is usable when navigating with tab */
                var t;
                if ('cancel' == settings.onblur) {
                    input.blur(function(e) {
                        /* prevent canceling if submit was clicked */
                        t = setTimeout(function() {
                            reset.apply(form, [settings, self]);
                        }, 500);
                    });
                } else if ('submit' == settings.onblur) {
                    input.blur(function(e) {
                        /* prevent double submit if submit was clicked */
                        t = setTimeout(function() {
                            form.submit();
                        }, 200);
                    });
                } else if ($.isFunction(settings.onblur)) {
                    input.blur(function(e) {
                        settings.onblur.apply(self, [input.val(), settings]);
                    });
                } else {
                    input.blur(function(e) {
                      /* TODO: maybe something here */
                    });
                }

                form.submit(function(e) {

                    if (t) {
                        clearTimeout(t);
                    }

                    /* do no submit */
                    e.preventDefault();

                    /* call before submit hook. */
                    /* if it returns false abort submitting */
                    if (false !== onsubmit.apply(form, [settings, self])) {
                        /* custom inputs call before submit hook. */
                        /* if it returns false abort submitting */
                        if (false !== submit.apply(form, [settings, self])) {

                          /* check if given target is function */
                          if ($.isFunction(settings.target)) {
                              var str = settings.target.apply(self, [input.val(), settings]);
                              $(self).html(str);
                              self.editing = false;
                              callback.apply(self, [self.innerHTML, settings]);
                              /* TODO: this is not dry */
                              if (!$.trim($(self).html())) {
                                  $(self).html(settings.placeholder);
                              }
                          } else {
                              /* add edited content and id of edited element to POST */
                              var submitdata = {};
                              submitdata[settings.name] = input.val();
                              submitdata[settings.id] = self.id;
                              /* add extra data to be POST:ed */
                              if ($.isFunction(settings.submitdata)) {
                                  $.extend(submitdata, settings.submitdata.apply(self, [self.revert, settings]));
                              } else {
                                  $.extend(submitdata, settings.submitdata);
                              }

                              /* quick and dirty PUT support */
                              if ('PUT' == settings.method) {
                                  submitdata['_method'] = 'put';
                              }

                              /* show the saving indicator */
                              $(self).html(settings.indicator);

                              /* defaults for ajaxoptions */
                              var ajaxoptions = {
                                  type    : 'POST',
                                  data    : submitdata,
                                  dataType: 'html',
                                  url     : settings.target,
                                  success : function(result, status) {
                                      if (ajaxoptions.dataType == 'html') {
                                        $(self).html(result);
                                      }
                                      self.editing = false;
                                      callback.apply(self, [result, settings]);
                                      if (!$.trim($(self).html())) {
                                          $(self).html(settings.placeholder);
                                      }
                                  },
                                  error   : function(xhr, status, error) {
                                      onerror.apply(form, [settings, self, xhr]);
                                  }
                              };

                              /* override with what is given in settings.ajaxoptions */
                              $.extend(ajaxoptions, settings.ajaxoptions);
                              $.ajax(ajaxoptions);

                            }
                        }
                    }

                    /* show tooltip again */
                    $(self).attr('title', settings.tooltip);

                    return false;
                });
            });

            /* privileged methods */
            this.reset = function(form) {
                /* prevent calling reset twice when blurring */
                if (this.editing) {
                    /* before reset hook, if it returns false abort reseting */
                    if (false !== onreset.apply(form, [settings, self])) {
                        $(self).html(self.revert);
                        self.editing   = false;
                        if (!$.trim($(self).html())) {
                            $(self).html(settings.placeholder);
                        }
                        /* show tooltip again */
                        if (settings.tooltip) {
                            $(self).attr('title', settings.tooltip);
                        }
                    }
                }
            };
        });

    };


    $.editable = {
        types: {
            defaults: {
                element : function(settings, original) {
                    var input = $('<input type="hidden"></input>');
                    $(this).append(input);
                    return(input);
                },
                content : function(string, settings, original) {
                    $(':input:first', this).val(string);
                },
                reset : function(settings, original) {
                  original.reset(this);
                },
                buttons : function(settings, original) {
                    var form = this;
                    if (settings.submit) {
                        /* if given html string use that */
                        if (settings.submit.match(/>$/)) {
                            var submit = $(settings.submit).click(function() {
                                if (submit.attr("type") != "submit") {
                                    form.submit();
                                }
                            });
                        /* otherwise use button with given string as text */
                        } else {
                            var submit = $('<button type="submit" />');
                            submit.html(settings.submit);
                        }
                        $(this).append(submit);
                    }
                    if (settings.cancel) {
                        /* if given html string use that */
                        if (settings.cancel.match(/>$/)) {
                            var cancel = $(settings.cancel);
                        /* otherwise use button with given string as text */
                        } else {
                            var cancel = $('<button type="cancel" />');
                            cancel.html(settings.cancel);
                        }
                        $(this).append(cancel);

                        $(cancel).click(function(event) {
                            //original.reset();
                            if ($.isFunction($.editable.types[settings.type].reset)) {
                                var reset = $.editable.types[settings.type].reset;
                            } else {
                                var reset = $.editable.types['defaults'].reset;
                            }
                            reset.apply(form, [settings, original]);
                            return false;
                        });
                    }
                }
            },
            text: {
                element : function(settings, original) {
                    var input = $('<input />');
                    if (settings.width  != 'none') { input.width(settings.width);  }
                    if (settings.height != 'none') { input.height(settings.height); }
                    /* https://bugzilla.mozilla.org/show_bug.cgi?id=236791 */
                    //input[0].setAttribute('autocomplete','off');
                    input.attr('autocomplete','off');
                    $(this).append(input);
                    return(input);
                }
            },
            textarea: {
                element : function(settings, original) {
                    var textarea = $('<textarea />');
                    if (settings.rows) {
                        textarea.attr('rows', settings.rows);
                    } else if (settings.height != "none") {
                        textarea.height(settings.height);
                    }
                    if (settings.cols) {
                        textarea.attr('cols', settings.cols);
                    } else if (settings.width != "none") {
                        textarea.width(settings.width);
                    }
                    $(this).append(textarea);
                    return(textarea);
                }
            },
            select: {
               element : function(settings, original) {
                    var select = $('<select />');
                    $(this).append(select);
                    return(select);
                },
                content : function(data, settings, original) {
                    /* If it is string assume it is json. */
                    if (String == data.constructor) {
                        eval ('var json = ' + data);
                    } else {
                    /* Otherwise assume it is a hash already. */
                        var json = data;
                    }
                    for (var key in json) {
                        if (!json.hasOwnProperty(key)) {
                            continue;
                        }
                        if ('selected' == key) {
                            continue;
                        }
                        var option = $('<option />').val(key).append(json[key]);
                        $('select', this).append(option);
                    }
                    /* Loop option again to set selected. IE needed this... */
                    $('select', this).children().each(function() {
                        if ($(this).val() == json['selected'] ||
                            $(this).text() == $.trim(original.revert)) {
                                $(this).attr('selected', 'selected');
                        }
                    });
                }
            }
        },

        /* Add new input type */
        addInputType: function(name, input) {
            $.editable.types[name] = input;
        }
    };

    // publicly accessible defaults
    $.fn.editable.defaults = {
        name       : 'value',
        id         : 'id',
        type       : 'text',
        width      : 'auto',
        height     : 'auto',
        event      : 'click.editable',
        onblur     : 'cancel',
        loadtype   : 'GET',
        loadtext   : 'Loading...',
        placeholder: 'Click to edit',
        loaddata   : {},
        submitdata : {},
        ajaxoptions: {}
    };

})(jQuery);
