define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareUtil"
  "edwareLanguageSelector"
  "edwareHelpMenu"
  "text!headerTemplateHtml"
  "edwareEvents"
  "edwareModal"
], ($, Bootstrap, Mustache, edwareUtil, edwareLanguageSelector, edwareHelpMenu, headerTemplateHtml, edwareEvents, edwareModal) ->

  create = (data, config, isPublic) ->
    labels = config.labels
    # Get tenant level branding information
    templateData = edwareUtil.getTenantBrandingData data.metadata
    templateData.isPublic = isPublic ?= false
    if isPublic
      params = edwareUtil.getUrlParams()
      templateData.stateCode = params['stateCode']
    headerTemplateHtml = Mustache.to_html headerTemplateHtml, templateData
    headerTemplate = $(headerTemplateHtml)
    # Add labels
    headerTemplate.find('.text_hi').html labels.hi
    if isPublic
      text = labels.info
    else
      text = labels.help
    headerTemplate.find('.text_help').html text
    userInfo = data.user_info
    # Add header to the page
    userName = edwareUtil.getUserName userInfo if userInfo
    if userName
      headerTemplate.find('#user-settings #username').html userName
    header = $("#header").html headerTemplate
    # Add language selector
    edwareLanguageSelector.create $('#languageSelector', header), labels
    $('.text_logout').html labels.logout
    createHelp(labels, isPublic)
    bindEvents()
    role = edwareUtil.getRole userInfo if userInfo
    uid = edwareUtil.getUid userInfo if userInfo

  createHelp = (labels, isPublic) ->
    @helpMenu = edwareHelpMenu.create '.HelpMenuContainer', isPublic,
      labels: labels

  bindEvents = ()->
    self = @
    # Popup will close if user clicks popup hide button
    $('#header #help').click ->
      self.helpMenu.show()
    $('#header #log_out_button').click ->
      window.open '/logout', 'iframe_logout'
    $('#header #resources').click ->
      $('#ResourcesModal').edwareModal()
    $('#header .dropdown').mouseleave ->
      $(this).removeClass 'open'

  create: create
