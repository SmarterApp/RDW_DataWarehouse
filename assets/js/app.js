require({
  paths: {
    cs: '3p/cs',
    'coffee-script': '3p/coffee-script',
    jquery: '3p/jquery-1.7.2.min',
    jqGrid: '3p/jquery.jqGrid.min',
    edwareUtil: 'EDWARE.util'
  }
});

require([
  'cs!widgets/EDWARE.grid.tablegrid'
], function (edwareGrid) {
	var columnData, columnItems;

	columnData = [
	  {
	    id: "1",
	    name: "some long test text",
	    teacher: "teacher1",
	    overall: "1403",
	    amount: "200.00",
	    tax: "10.00",
	    total: "210.00"
	  }, 
	  {
	    id: "2",
	    name: "test2",
	    teacher: "teacher2",
	    overall: "1200",
	    amount: "300.00",
	    tax: "20.00",
	    total: "320.00"
	  }, 
	  {
	    id: "3",
	    name: "test3",
	    teacher: "teacher3",
	    overall: "1100",
	    amount: "400.00",
	    tax: "30.00",
	    total: "430.00"
	  },
	  {
	    id: "4",
	    name: "some long test text",
	    teacher: "teacher4",
	    overall: "1435",
	    amount: "200.00",
	    tax: "10.00",
	    total: "210.00"
	  }, 
	  {
	    id: "5",
	    name: "test2",
	    teacher: "teacher5",
	    overall: "1502",
	    amount: "300.00",
	    tax: "20.00",
	    total: "320.00"
	  }, 
	  {
	    id: "6",
	    name: "test3",
	    teacher: "teacher6",
	    overall: "899",
	    amount: "400.00",
	    tax: "30.00",
	    total: "430.00"
	  }
	];
	
	columnItems = [
	    { name: "id", index: "id", width: 150, align: "center", sorttype: "int", hidden: true}, 
	    { name: "name", index: "name", width: 150, style: "ui-ellipsis" },
	    { name: "Math", items: [
		    { name: "teacher", index: "teacher", width: 150, resizable: false }, 
		    { name: "overall", index: "overall", width: 150, formatter: "number", align: "right", resizable: false } 
	    ]}, 
	    { name: "amount", index: "amount", width: 150, formatter: "number", align: "right", resizable: false }, 
	    { name: "tax", index: "tax", width: 150, formatter: "number", align: "right", resizable: false }, 
	    { name: "total", index: "total", width: 150, formatter: "number", align: "right", resizable: false }
	  ];
    
  edwareGrid.create("gridTable", columnItems, columnData);
});
