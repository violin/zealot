(function($){
	var _loadingMask = null;
    var _loadingPb = null;

    window.Util = function() {

    }

    Util._$showLoading = function( _notShowMask ){
        
	    var __initLoading = function(){
	    	_loadingHtml ='<div id="loadingMask" class="loading-mask" style="z-index: 10001;"></div><div id="loadingPb" class="ui-loading f-cb" style="z-index: 10002;"></div> ';
		    $("body").append(_loadingHtml);
		    _loadingMask = $("#loadingMask");
		    _loadingPb = $("#loadingPb");
	    };

	    if(!_loadingMask)
	      __initLoading();
	    //显示内容
	    _notShowMask = _notShowMask || false;

	    //显示节点
	    if(!!_notShowMask){
	      $(_loadingMask).hide();
	    }
	    $(_loadingPb).show();
    };

    Util._$hideLoading = function(  ){
	    $(_loadingMask).hide();
	    $(_loadingPb).hide();
    };

    Util._$showToast = function( _type , _mes ){
        
    };
})( jQuery );