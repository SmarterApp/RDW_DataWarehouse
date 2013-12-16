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
    # Add labels
    headerTemplate.find('#help').append labels.help
    headerTemplate.find('#feedback').append labels.feedback
    headerTemplate.find('#resources').append labels.resources
    userInfo = data.user_info


    # Add header to the page
    userName = edwareUtil.getUserName userInfo

    if userName
      headerTemplate.find('#user-settings #username').html userName
    header = $("#header").append headerTemplate
    dropdown_menu = header.find('.dropdown-menu')
    # Add language selector
    edwareLanguageSelector.create dropdown_menu, labels

    $('#log_out_button').html labels.logout

    createHelp(labels)
    bindEvents()
    
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
    $('#log_out_button').click () ->
      window.open '/logout', 'iframe_logout'

  create: create
