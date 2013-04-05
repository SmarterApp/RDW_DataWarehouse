define [
  "jquery"
  "mustache"
  "bootstrap"
  "text!edwareFooterHtml"
], ($, Mustache, bootstrap, footerTemplate) ->
  $.fn.generateFooter = (reportName) ->
    self = this
    imageData = {}
    if reportName is 'individual_student_report'
      imageData['imageFileName'] = 'legend_IndivStudent.png'
    else if reportName is 'list_of_students'
      imageData['imageFileName'] = 'legend_ListofStudents.png'
    else if reportName is 'comparing_populations'
      imageData['imageFileName'] = 'legend_comparepop.png'
   
    output = Mustache.to_html footerTemplate, imageData
      
    self.html output
    createPopover()

  create = (containerId) ->
    $(containerId).generateFooter
                
  
  createPopover = ->
    $("#legend").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right"><ul class="nav"><li><a class="pull-right" href="#" id="close" onclick="$(&quot;#legend&quot;).popover(&quot;hide&quot;);">Hide <img src="../images/hide_x.png"></img></i></a></li></ul></div><div class="lead">Legend</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".legendPopup").html()
              
    $("#aboutReport").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right"><ul class="nav"><li><a class="pull-right" href="#" id="close" onclick="$(&quot;#aboutReport&quot;).popover(&quot;hide&quot;);">Hide <img src="../images/hide_x.png"></img></i></a></li></ul></div><div class="lead">Report Info</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        $(".aboutReportPopup").html()
        
    $("#help").popover
      html: true
      placement: "top"
      container: "div"
      title: ->
        '<div class="pull-right"><ul class="nav"><li><a class="pull-right" href="#" id="close" onclick="$(&quot;#help&quot;).popover(&quot;hide&quot;);">Hide <img src="../images/hide_x.png"></img></i></a></li></ul></div><div class="lead">Help</div>'
      template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
      content: ->
        '<p>Send your inquiries to our <a href="mailto:SmarterBalancedReporting@wgen.net?subject=Smarter Balanced Reporting: Help Inquiries">System Administrator</a>, and be sure to include your userid in the body of the email.</p><p>You should receive a response within 2 business days.</p>'

  create: create
