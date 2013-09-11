define [
  "jquery"
  "mustache"
  "edwareUtil"
  "edwareLanguageSelector"
], ($, Mustache, edwareUtil, edwareLanguageSelector) ->

  HEADER_TEMPLATE = "<div id='logo'>" +
                    "<img src='../images/smarterHeader_logo.png' alt='logo' height='36' width='112'>" +
                    "</div>" +
                    "<div id='headerTitle'>Reporting Beta UAT - DRAFT SYSTEM</div>" + 
                    "<div class='topLinks'>" +
                    "<span id='language_selector'></span><span class='seperator'>|</span>" +
                    "<span id='headerUser' class='user'></span><span class='seperator'>|</span><span id='headerLogout'><a id='logout_button' href='/logout' target='iframe_logout'>Log Out</a></span>" +
                    "</div>" +
                    "<!--This iframe is used for logout redirect.  Do not remove it.-->" +
                    "<iframe frameborder='0' height='0px' width='0px' name='iframe_logout'></iframe>"


  create = (data, config, reportName) ->
    userInfo = data.user_info

    $("#header").html(HEADER_TEMPLATE)

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

  create: create