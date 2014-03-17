
	//初始化
	var tablename;
	var tables=[];
	$("#dbTables>li>a").each(function (){
		tables.push($(this).html())
	})

	//绑定表名的点击
	function bindItem(){
		$(".table_node").click(function(){
			tablename = $(this).html();
			$("#board_table_name").html(tablename)
			var cParent = $("#result_col")
	    	cParent.empty()
	    	var parent = $("#result_col_value")
	    	parent.empty()
		})
	}
	bindItem();

	//绑定筛选框
	$("#search_filter").keyup(function() {
		var tbKeyword = $(this).val();
		$("#dbTables").empty();
		for (var i = 0; i < tables.length; i++) {
			if (tables[i].toUpperCase().indexOf(tbKeyword.toUpperCase())>=0) {
				var temp = $('<li><a class="table_node" href="#">'+tables[i]+'</a></li>')
				$("#dbTables").append(temp);
			}; 
		};
		bindItem();
	})

	//绑定查询按钮 go
	$("#go").click(function(){
		var query = $("#query").val();
		$.post("query",{tableName:tablename,condition:query},function(result){
	    	data = $.parseJSON(result)
	    	head = data.k
	    	value = data.v
	    	//process k
	    	var cParent = $("#result_col")
	    	cParent.empty()
	    	for (var i = 0; i < head.length; i++) {
	    		var th = $("<th>"+head[i]+"</th>")
	    		cParent.append(th)
	    	}
	    	//process v
	    	var parent = $("#result_col_value")
	    	parent.empty()
	    	for (var i = 0; i < value.length; i++) {
	    		var tr = $("<tr></tr>")
	    		var arr = value[i]
	    		for(var j = 0; j < arr.length; j++){
	    			var col = arr[j]
	    			var td = $("<td>"+col+"</td>")
	    			tr.append(td)
	    		}
	    		parent.append(tr)
	    	}
	  	});
	})

