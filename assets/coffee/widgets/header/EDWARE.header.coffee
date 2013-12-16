define [
  "jquery"
  "mustache"
  "edwareUtil"
  "edwareLanguageSelector"
  "edwareHelpMenu"
  "text!headerTemplateHtml"
], ($, Mustache, edwareUtil, edwareLanguageSelector, edwareHelpMenu, headerTemplateHtml) ->



  create = (data, config, reportName) ->
    labels = config.labels
    headerTemplate = $(headerTemplateHtml)
    headerTemplate.find('#help').append labels.help
    headerTemplate.find('#feedback').append labels.feedback
    headerTemplate.find('#resources').append labels.resources
    header = $("#header").append headerTemplate
    dropdown_menu = header.find('.dropdown-menu')
    # Add language selector
    edwareLanguageSelector.create dropdown_menu, labels
    log_out = $('<li class="divider"></li><div style="text-align:center;"><button type="button" class="btn btn-primary">'+labels.logout+'</button></div>')
    dropdown_menu.append log_out
    createHelp(labels)
    bindEvents()
    userInfo = data.user_info


    # Add header to the page
    userName = edwareUtil.getUserName userInfo

    if userName
      $('#header .topLinks .user').html userName
    
    feedbackData = config.feedback
    role = edwareUtil.getRole userInfo
    uid = edwareUtil.getUid userInfo
    # TODO might need to move this part to footer
    edwareUtil.renderFeedback(role, uid, reportName, feedbackData)
  createHelp = (labels) ->
    @helpMenu = edwareHelpMenu.create '.HelpMenuContainer',
      labels: labels

  bindEvents = ()->
    self = @
    # Popup will close if user clicks popup hide button
    $('#header #help').click () ->
      self.helpMenu.show()

  create: create
