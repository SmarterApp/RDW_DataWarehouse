define [
  "jquery"
  "mustache"
  "edwareUtil"
  "edwareLanguageSelector"
  "edwareHelpMenu"
  "text!headerTemplateHtml"
], ($, Mustache, edwareUtil, edwareLanguageSelector, edwareHelpMenu, headerTemplateHtml) ->



  create = (data, config, reportName) ->
    #output = Mustache.render(HEADER_TEMPLATE, config)
    $("#header").html(headerTemplateHtml)
    labels = config.labels
    createHelp(labels)
    bindEvents()
    userInfo = data.user_info


    # Add header to the page
    userName = edwareUtil.getUserName userInfo

    if userName
      $('#header .topLinks .user').html userName
    
    # Add language selector
    edwareLanguageSelector.create $('#language_selector')

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
