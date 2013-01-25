define [
  'jquery'
  'jqGrid'
  'gridLocaleEn'
], ($, jqGrid, gridLocaleEn) ->
  console.log 'app name is edware'
  
  $(document).ready ->
  "use strict"
  mydata = [
    id: "1"
    invdate: "2007-10-01"
    name: "some long test text"
    note: "note"
    amount: "200.00"
    tax: "10.00"
    closed: true
    ship_via: "TN"
    total: "210.00"
  ,
    id: "2"
    invdate: "2007-10-02"
    name: "test2"
    note: "note2"
    amount: "300.00"
    tax: "20.00"
    closed: false
    ship_via: "FE"
    total: "320.00"
  ,
    id: "3"
    invdate: "2007-09-01"
    name: "test3"
    note: "note3"
    amount: "400.00"
    tax: "30.00"
    closed: false
    ship_via: "FE"
    total: "430.00"
  ,
    id: "4"
    invdate: "2007-10-04"
    name: "test4"
    note: "note4"
    amount: "200.00"
    tax: "10.00"
    closed: true
    ship_via: "TN"
    total: "210.00"
  ,
    id: "5"
    invdate: "2007-10-31"
    name: "test5"
    note: "note5"
    amount: "300.00"
    tax: "20.00"
    closed: false
    ship_via: "FE"
    total: "320.00"
  ,
    id: "6"
    invdate: "2007-09-06"
    name: "test6"
    note: "note6"
    amount: "400.00"
    tax: "30.00"
    closed: false
    ship_via: "FE"
    total: "430.00"
  ,
    id: "7"
    invdate: "2007-10-04"
    name: "test7"
    note: "note7"
    amount: "200.00"
    tax: "10.00"
    closed: true
    ship_via: "TN"
    total: "210.00"
  ,
    id: "8"
    invdate: "2007-10-03"
    name: "test8"
    note: "note8"
    amount: "300.00"
    tax: "20.00"
    closed: false
    ship_via: "FE"
    total: "320.00"
  ,
    id: "9"
    invdate: "2007-09-01"
    name: "test9"
    note: "note9"
    amount: "400.00"
    tax: "30.00"
    closed: false
    ship_via: "TN"
    total: "430.00"
  ,
    id: "10"
    invdate: "2007-09-08"
    name: "test10"
    note: "note10"
    amount: "500.00"
    tax: "30.00"
    closed: true
    ship_via: "TN"
    total: "530.00"
  ,
    id: "11"
    invdate: "2007-09-08"
    name: "test11"
    note: "note11"
    amount: "500.00"
    tax: "30.00"
    closed: false
    ship_via: "FE"
    total: "530.00"
  ,
    id: "12"
    invdate: "2007-09-10"
    name: "test12"
    note: "note12"
    amount: "500.00"
    tax: "30.00"
    closed: false
    ship_via: "FE"
    total: "530.00"
  ]
  grid = $("#list")
  grid.jqGrid
    datatype: "local"
    data: mydata
    colNames: ["Inv No", "Date", "Client", "Amount", "Tax", "Total", "Closed", "Shipped via", "Notes"]
    colModel: [
      name: "id"
      index: "id"
      width: 70
      align: "center"
      sorttype: "int"
      hidden: true
    ,
      name: "invdate"
      index: "invdate"
      width: 80
      align: "center"
      sorttype: "date"
      formatter: "date"
      formatoptions:
        newformat: "m/d/Y"

      datefmt: "m/d/Y"
      resizable: false
    ,
      name: "name"
      index: "name"
      width: 90
      style: "ui-ellipsis"
    ,
      name: "amount"
      index: "amount"
      width: 70
      formatter: "number"
      align: "right"
      resizable: false
    ,
      name: "tax"
      index: "tax"
      width: 50
      formatter: "number"
      align: "right"
      resizable: false
    ,
      name: "total"
      index: "total"
      width: 60
      formatter: "number"
      align: "right"
      resizable: false
    ,
      name: "closed"
      index: "closed"
      width: 60
      align: "center"
      formatter: "checkbox"
      edittype: "checkbox"
      editoptions:
        value: "Yes:No"
        defaultValue: "Yes"
    ,
      name: "ship_via"
      index: "ship_via"
      width: 90
      align: "center"
      formatter: "select"
      edittype: "select"
      editoptions:
        value: "FE:FedEx;TN:TNT;IN:Intim"
        defaultValue: "Intime"
    ,
      name: "note"
      index: "note"
      width: 70
      sortable: false
    ]
    rowNum: 10
    rowList: [5, 10, 20]
    pager: "#pager"
    altRows: true
    altclass: "myAltRowClass"
    gridview: true
    rownumbers: true
    sortname: "invdate"
    viewrecords: true
    sortorder: "desc"
    caption: "Just simple local grid"
    height: "100%"
