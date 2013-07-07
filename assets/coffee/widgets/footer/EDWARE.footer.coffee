define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareConfidenceLevelBar"
  "text!edwareFooterHtml"
  "text!edwareLegendTemplate"
], ($, Mustache, bootstrap, edwareConfidenceLevelBar, footerTemplate, legendTemplate) ->
                                           
  $.fn.generateFooter = (reportName, content, legend) ->
    self = this
    data = {}
    # keep these images to display legend on Cpop and LOS two reports
    if reportName is 'list_of_students'
      data['imageFileName'] = 'legend_ListofStudents.png'
    else if reportName is 'comparing_populations'
      data['imageFileName'] = 'legend_comparepop.png'
    
    data['report_info'] = content[reportName]
    # create legend
    # for the time being, we show legend in html format only on ISR
    if legend
      legend_info = createLegend legend
      data['legend_info'] = legend_info
   
    output = Mustache.to_html footerTemplate, data
      
    self.html output
    # show "Print" only on ISR
    if reportName isnt 'individual_student_report'
      $('#print').hide()
    createPopover()
    if legend
      # create performance bar in legend
      createConfidenceLevelBar(legend['subject'])
    
  createConfidenceLevelBar = (subject) ->
    # use mustache template to display the json data 
    # show 300px performance bar on html page
    output = edwareConfidenceLevelBar.create subject, 300
    $('#legendTemplate .losPerfBar').html(output)
    # show 640px performance bar on pdf
    output = edwareConfidenceLevelBar.create subject, 640
    $('#legendTemplate .confidenceLevel').html(output)
    
  createLegend = (legend) ->
    # create legend in html format from mustache template
    data = {}
    # create ALD intervals
    data['ALDs'] = createALDs legend['subject']
    # text from json file
    data['legendInfo'] = legend['legendInfo']
    # need assessment score and color to display legend consistently across all ISR
    data['asmtScore'] = legend['subject'].asmt_score
    data['scoreColor'] = legend['subject'].score_color
    Mustache.to_html legendTemplate, data

  createALDs = (items) ->
    # create intervals to display on ALD table
    ALDs = []
    intervals = items.cut_point_intervals
    i = 0
    while i < intervals.length
      interval = {}
      interval['color'] = intervals[i]['bg_color']
      interval['description'] = intervals[i]['name']
      start_score = if i == 0 then items.asmt_score_min else intervals[i-1]['interval']
      end_score = if i == intervals.length - 1 then items.asmt_score_max else (intervals[i]['interval'] - 1)
      interval['range'] = start_score + '-' + end_score
      ALDs.push interval
      i++
    ALDs
  
  create = (containerId) ->
    $(containerId).generateFooter
                
  hidePopover = (id) ->
    $(id).popover("hide")
   
  createPopover = ->
    
    # Survey monkey popup
    $("#feedback").popover
      html: true
      placement: "top"
      container: "footer"
      title: ->
          '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="feedback">Hide <img src="../images/hide_x.png"></img></i></a></div><div class="lead">Feedback</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".surveyMonkeyPopup").html()
        
    $("#legend").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="legend">Hide <img src="../images/hide_x.png"></img></i></a></div><div class="lead">Legend</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $("#footerLinks .legendPopup").html()
              
    $("#aboutReport").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="aboutReport">Hide <img src="../images/hide_x.png"></img></i></a></div><div class="lead">Report Info</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $("#footerLinks .aboutReportPopup").html()
        
    $("#help").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="help">Hide <img src="../images/hide_x.png"></img></i></a></div><div class="lead">Help</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".helpPopup").html()

    $("#print").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="print">Hide <img src="../images/hide_x.png"></img></i></a></div><div class="lead">Print Options</div>'
      template: '<div class="popover footerPopover printFooterPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".printPopup").html()
     
  # Make the footer button active when associate popup opens up
  $(document).on
    click: ->
      $("#footer .nav li a").not($(this)).removeClass("active")
      $(this).toggleClass("active")
    , "#footer .nav li a"
    
  
  # Popup will close if user clicks popup hide button
  $(document).on
    click: ->
      $("#"+$(this).data("id")).popover("hide")
      $("#footer .nav li a").removeClass("active")
     , ".hideButton a"

  $(document).on
    click: ->
      val=$('input[name=print_options]:checked').val()
      url=document.URL.replace("/assets/html/","/services/pdf/").replace(new RegExp("#.*"),"")
      url += '&pdf=true'
      if val is "gray"
        url += "&grayscale=true"
      $("#print").popover "hide"
      $("#footer .nav li a").removeClass("active")
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')
    , "#printButton"

  create: create
