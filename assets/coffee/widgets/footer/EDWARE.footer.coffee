define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareConfidenceLevelBar"
  "edwareClientStorage"
  "text!edwareFooterHtml"
  "edwareLegend"
  "edwarePreferences"
], ($, Mustache, bootstrap, edwareConfidenceLevelBar, edwareClientStorage, footerTemplate, edwareLegend, edwarePreferences) ->
  
  $.fn.generateFooter = (reportName, content, legend, labels) ->
    this.html Mustache.to_html footerTemplate, {
      'report_info': content,
      'labels': labels
    }
    # show "Print" only on ISR
    if reportName isnt 'individual_student_report'
      $('#print').hide()
    if reportName isnt 'list_of_students'
      $('#export').hide()
    createPopover(labels)
    # create legend
    $('.legendPopup').createLegend(reportName, legend)
  
  createConfidenceLevelBar = (subject) ->
    # use mustache template to display the json data 
    # show 300px performance bar on html page
    output = edwareConfidenceLevelBar.create subject, 300
    $('#legendTemplate .losPerfBar').html(output)
    # show 640px performance bar on pdf
    output = edwareConfidenceLevelBar.create subject, 640
    $('#legendTemplate .confidenceLevel').html(output)
                
  hidePopover = (id) ->
    $(id).popover("hide")
   
  createPopover =(labels) ->
    
    # Survey monkey popup
    $("#feedback").popover
      html: true
      placement: "top"
      container: 'body'
      title: ->
          '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="feedback">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead">'+labels.feedback+'</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".surveyMonkeyPopup").html()
        
    $("#legend").popover
      html: true
      placement: "top"
      container: 'body'
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="legend">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead">'+labels.legend+'</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $("#footerLinks .legendPopup").html()
              
    $("#aboutReport").popover
      html: true
      placement: "top"
      container: 'body'      
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="aboutReport">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead">'+labels.report_info+'</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $("#footerLinks .aboutReportPopup").html()
        
    $("#help").popover
      html: true
      placement: "top"
      container: 'body'
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="help">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead">'+labels.help+'</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".helpPopup").html()

    $("#print").popover
      html: true
      placement: "top"
      container: 'body'
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="print">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead">'+labels.print_options+'</div>'
      template: '<div class="popover footerPopover printFooterPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".printPopup").html()
   
    # TODO:  export is temporary placed in the footer.  If it's permanent, we need to update template.html for hiding another popovers
    $("#export").popover
      html: true
      placement: "top"
      title: ->
        '<div class="pull-right hideButton"><a class="pull-right" href="#" id="close" data-id="export">'+labels.hide+' <img src="../images/hide_x.png"></img></i></a></div><div class="lead"> Export</div>'
      template: '<div class="popover footerPopover exportFooterPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".exportPopup").html()
     
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
      asmtType = $('#selectedAsmtType').text()
      url=document.URL.replace("indivStudentReport","print")
      url += '&pdf=true'
      if val is "gray"
        url += "&grayscale=true"
      if asmtType
         url += "&asmtType=" + encodeURI asmtType
      url += "&lang=" + edwarePreference.getSelectedLanguage()
      $("#print").popover "hide"
      $("#footer .nav li a").removeClass("active")
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')
    , "#printButton"

  # Export Button
  $(document).on
    click: ->
      val=$('input[name=export_options]:checked').val()
      # We need to read the params in session storage, remove edwareSessionStorage when this code gets moved from footer
      params = JSON.parse edwareClientStorage.filterStorage.load()
      url = window.location.protocol + "//" + window.location.host + "/data/list_of_students_csv?" + $.param(params, true) + "&content-type=text/csv"
      $("#export").popover "hide"
      $("#footer .nav li a").removeClass("active")
      
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')
    , "#exportButton"

  create = (reportName, colorsData, config) ->
      labels = config.labels
      reportInfo = config.reportInfo
      legendInfo = config.legendInfo
      # Generate footer
      $('#footer').generateFooter(reportName, reportInfo, {
        'legendInfo': legendInfo,
        'subject': (()->
            # merge default color data into sample intervals data
            for color, i in colorsData.subject1 || colorsData.subject2
              legendInfo.sample_intervals.intervals[i].color = color
            legendInfo.sample_intervals
          )()
      }, labels)


  create: create
