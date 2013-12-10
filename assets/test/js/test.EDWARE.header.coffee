define ["jquery", "edwareReportInfoBar", "edwareReportActionBar", "edwareHelpMenu"], ($, edwareReportInfoBar, edwareReportActionBar, edwareHelpMenu) ->

  ReportInfoBar = edwareReportInfoBar.ReportInfoBar

  ReportActionBar = edwareReportActionBar.ReportActionBar

  HelpMenu = edwareHelpMenu.EdwareHelpMenu

  infoBarConfig = {
    title: "Test Title"
  }

  actionBarConfig = {
    colorsData: {subject1:{colors:[{bg_color:"#DD514C",text_color:"#ffffff",end_gradient_bg_color:"#C43C35",start_gradient_bg_color:"#EE5F5B"},{bg_color:"#e4c904",text_color:"#000",end_gradient_bg_color:"#eed909",start_gradient_bg_color:"#e3c703"},{bg_color:"#6aa506",text_color:"#ffffff",end_gradient_bg_color:"#65b92c",start_gradient_bg_color:"#3d9913"},{bg_color:"#237ccb",text_color:"#ffffff",end_gradient_bg_color:"#3a98d1",start_gradient_bg_color:"#2078ca"}],min_cell_size:2}, subject2:{colors:[{bg_color:"#DD514C",text_color:"#ffffff",end_gradient_bg_color:"#C43C35",start_gradient_bg_color:"#EE5F5B"},{bg_color:"#e4c904",text_color:"#000",end_gradient_bg_color:"#eed909",start_gradient_bg_color:"#e3c703"},{bg_color:"#6aa506",text_color:"#ffffff",end_gradient_bg_color:"#65b92c",start_gradient_bg_color:"#3d9913"},{bg_color:"#237ccb",text_color:"#ffffff",end_gradient_bg_color:"#3a98d1",start_gradient_bg_color:"#2078ca"}],min_cell_size:2}},
    legendInfo: {sample_intervals:{asmt_score:1789,asmt_score_interval:65,asmt_score_max:2400,asmt_score_max_range:441,asmt_score_min:1200,asmt_score_min_range:263,asmt_score_pos:402.5,asmt_score_range_max:2027,asmt_score_range_min:1907,score_color:"#e4c904",cut_point_intervals:[{asmt_cut_point:107,bg_color:"#DD514C",end_gradient_bg_color:"#C43C35",interval:1400,name:"Minimal Understanding",start_gradient_bg_color:"#EE5F5B",text_color:"#FFFFFF"},{asmt_cut_point:213,bg_color:"#e4c904",end_gradient_bg_color:"#eed909",interval:1800,name:"Partial Understanding",start_gradient_bg_color:"#e3c703",text_color:"#000"},{asmt_cut_point:160,bg_color:"#6aa506",end_gradient_bg_color:"#65b92c",interval:"2100",name:"Adequate Understanding",start_gradient_bg_color:"#3d9913",text_color:"#FFFFFF"},{asmt_cut_point:160,bg_color:"#237ccb",end_gradient_bg_color:"#3a98d1",interval:2400,name:"Thorough Understanding",start_gradient_bg_color:"#2078ca",text_color:"#FFFFFF"}],intervals:[{color:{bg_color:"#DD514C",end_gradient_bg_color:"#C43C35",start_gradient_bg_color:"#EE5F5B",text_color:"#ffffff"},count:27,level:1,percentage:27,showPercentage:true},{color:{bg_color:"#e4c904",start_gradient_bg_color:"#e3c703",end_gradient_bg_color:"#eed909",text_color:"#000"},count:33,level:2,percentage:33,showPercentage:true},{color:{bg_color:"#6aa506",start_gradient_bg_color:"#3d9913",end_gradient_bg_color:"#65b92c",text_color:"#FFFFFF"},count:34,level:3,percentage:34,showPercentage:true},{color:{bg_color:"#237ccb",start_gradient_bg_color:"#2078ca",end_gradient_bg_color:"#3a98d1",text_color:"#FFFFFF"},count:6,level:4,percentage:6,showPercentage:true}]},indicator:"8,345",desc1:"Percentage of population",desc2:"Total Students",desc3:"The width of a colored segment is proportional to the number of students in that segment.",notes:["Rollover/Tap bar for breakdown of population numbers","Percentages are rounded to the nearest whole number. Therefore, small percentages may be reported as '0'."]}
  }

  helpMenuConfig = {}
  
  module "EDWARE.header",
    setup: ->
      $("body").append "<div id='infoBarContainer'></div>"
      $("body").append "<div id='actionBarContainer'></div>"
      $("body").append "<div id='helpMenu'></div>"

    teardown: ->
      $('#infoBarContainer').remove()
      $('#actionBarContainer').remove()
      $('#helpMenu').remove()

  test "Test ReportInfoBar class", ->
    ok ReportInfoBar, "should have a ReportInfoBar class"
    equal typeof(ReportInfoBar), "function", "ReportInfoBar should be a class"

  test "Test initiate ReportInfoBar class", ->
    infoBar = new ReportInfoBar '#infoBarContainer', infoBarConfig
    ok infoBar, "ReportInfoBar should be able to initiate an object"

  test "Test create function", ->
    infoBar = edwareReportInfoBar.create '#infoBarContainer', infoBarConfig
    ok infoBar, "EdwareReportInfoBar.create function should be able to initiate an object"

  test "Test download icon click event", ->
    infoBar = new ReportInfoBar '#infoBarContainer', infoBarConfig
    $('.downloadIcon').click()
    ok $('.modal-backdrop')[0], "Clicking download icon should display download menu on body element"

  test "Test ReportActionBar class", ->
    ok ReportActionBar, "should have a ReportActionBar class"
    equal typeof(ReportActionBar), "function", "ReportActionBar should be a class"

  test "Test initiate ReportInfoBar class", ->
    actionBar = new ReportActionBar '#actionBarContainer', actionBarConfig
    ok actionBar, "ReportInfoBar should be able to initiate an object"

  test "Test create function", ->
    actionBar = edwareReportActionBar.create '#actionBarContainer', actionBarConfig
    ok actionBar, "edwareReportActionBar.create function should be able to initiate an object"

  test "Test action bar items", ->
    actionBar = edwareReportActionBar.create '#actionBarContainer', actionBarConfig
    ok $('li.legendItem')[0], "Action bar should contain legend item"
    ok $('li.alignmentItem')[0], "Action bar should contain alignment item"
    ok $('li.sortItem')[0], "Action bar should contain sort item"
    ok $('li.filterItem')[0], "Action bar should contain filter item"
    ok $('li.printItem')[0], "Action bar should contain print item"

  test "Test action bar events", ->
    actionBar = edwareReportActionBar.create '#actionBarContainer', actionBarConfig
    $legendItem = $('li.legendItem')
    $legendItem.trigger 'click'
    ok $legendItem.hasClass('active'), 'Legend item should be highlighted'
    $legendItem.trigger 'mouseleave'
    ok not $legendItem.hasClass('active'), 'Legend item should not be highlighted after hovering out'
    $print = $('span.printLabel').trigger 'click'
    ok $('.modal-backdrop')[0], 'Clicking print label should display print popover'

  test "Test HelpMenu class", ->
    ok HelpMenu, "should have a HelpMenu class"
    equal typeof(HelpMenu), "function", "HelpMenu should be a class"
    equal typeof(edwareHelpMenu.create), "function", "HelpMenu should contain a create function"

  test "Test create a HelpMenu instance", ->
    helpMenu = edwareHelpMenu.create '#helpMenu', helpMenuConfig
    ok helpMenu, 'Should instantiate a HelpMenu object'
    helpMenu.show()
    ok $('.modal-backdrop')[0], 'Showing help menu should set up a backdrop'

  test "Test switching tabs", ->
    helpMenu = edwareHelpMenu.create '#helpMenu', helpMenuConfig
    helpMenu.show()
    $('a[href="#userGuide"]').click()
    ok $('div#userGuide').hasClass('active'), 'Should switch current active tab to clicked one'