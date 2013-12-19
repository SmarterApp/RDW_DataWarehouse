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
    headerTemplate.find('.text_help').html labels.help
    headerTemplate.find('.text_feedback').html labels.feedback
    headerTemplate.find('.text_resources').html labels.resources
    userInfo = data.user_info


    # Add header to the page
    userName = edwareUtil.getUserName userInfo

    if userName
      headerTemplate.find('#user-settings #username').html userName
    header = $("#header").html headerTemplate
    dropdown_menu = header.find '.dropdown-menu'
    # Add language selector
    edwareLanguageSelector.create dropdown_menu, labels

    $('.text_logout').html labels.logout

    createHelp labels
    bindEvents()
    
    feedbackData = config.feedback
    role = edwareUtil.getRole userInfo
    uid = edwareUtil.getUid userInfo
    edwareUtil.renderFeedback $('#SurveryMonkeyModalBody'), role, uid, reportName, feedbackData

  createHelp = (labels) ->
    @helpMenu = edwareHelpMenu.create '.HelpMenuContainer',
      labels: labels

  bindEvents = ()->
    self = @
    # Popup will close if user clicks popup hide button
    $('#header #help').click ->
      self.helpMenu.show()
    $('#header #log_out_button').click ->
      window.open '/logout', 'iframe_logout'
    $('#header #feedback').click ->
      $('#SurveryMonkeyModal').modal 'show'
    $('#header #resources').click ->
      $('#ResourcesModal').modal 'show'
    $('#header .dropdown').mouseleave ->
      $(@).removeClass 'open'
  create: create
