
	//初始化
	var tablename;
	var tables=[];
	var querytype='where';

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
	//绑定查询表结构
	$("#show_create").hover(function(){
		$.post("showCreate",{tableName:tablename},function(result){
			str = $.parseJSON(result)
			var content = "<div style='width:600px'>" + str[0] +"</div>";
			content = content.replace(tablename+',','')
			content =content.replace(/\n/g,'<br>')
			$('#show_create').attr("data-original-title",content)
			$('#show_create').tooltip({html:true,trigger:'hover'})
		})
	})
	//绑定查询方式按钮
	$(".query_type").click(function(){
		$("#query_type").html($(this).html()+"<span class='caret'></span>");
		if ($(this).html() == "完整sql") {
			querytype='full';
			$("#query").attr("placeholder",'输入完整sql语句')
		};
		if ($(this).html() == "where条件") {
			querytype='where';
			$("#query").attr("placeholder","查询条件，可以不输(全匹配)' ,输入举例：'id=1';'id=1 and name='abc'")
		};
		
	})

	//绑定查询框
	$("#query").keyup(function(e){
		if (e.keyCode == 13) {
			$("#go").click();
		};
	})

	//绑定查询按钮 go
	$("#go").click(function(){
		var query = $("#query").val();
		queryWhere(query,null);
		
	})

	function queryWhere(query,orderCondition){
		$.post("query",{tableName:tablename,condition:query,queryType:querytype,orderCondition:orderCondition},function(result){
	    	data = $.parseJSON(result)
	    	head = data.k
	    	value = data.v
	    	//process k
	    	var cParent = $("#result_col")
	    	cParent.empty()
	    	for (var i = 0; i < head.length; i++) {
	    		var th = $("<th data="+head[i]+">"+head[i]+ "<br><span><span style='font-size:5px;cursor: pointer;' class='glyphicon glyphicon-chevron-up order-up'></span><span style='font-size:5px;cursor: pointer;' class='glyphicon glyphicon-chevron-down order-down'></span></span></th>")
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
	    	bindOrderClick();
	  	});
	}

	function bindOrderClick(){
		var query = $("#query").val();
		$(".order-up").click(function(){
			var col = $(this).parent().parent().attr('data')
			queryWhere(query,col + ' asc');
		});	
		$(".order-down").click(function(){
			var col = $(this).parent().parent().attr('data')
			queryWhere(query,col + ' desc');
		});	

	}

