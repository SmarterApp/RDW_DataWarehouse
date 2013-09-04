define [
  "jquery"
  "mustache"
  "edwareUtil"
], ($, Mustache, edwareUtil) ->

  HEADER_TEMPLATE = "<div id='logo'>" +
                    "<img src='../images/smarterHeader_logo.png' alt='logo' height='36' width='112'>" +
                    "</div>" +
                    "<div id='headerTitle'>Reporting Beta UAT - DRAFT SYSTEM</div>" + 
                    "<div class='topLinks'>" +
                    "<span id='headerUser' class='user'>{{userName}}</span><span class='seperator'>|</span><span id='headerLogout'><a id='logout_button' href='/logout' target='iframe_logout'>Log Out</a></span>" +
                    "</div>" +
                    "<!--This iframe is used for logout redirect.  Do not remove it.-->" +
                    "<iframe frameborder='0' height='0px' width='0px' name='iframe_logout'></iframe>"


  create = (data, config, reportType) ->
    userInfo = data.user_info
    # Add header to the page
    params =
      userName: edwareUtil.getUserName userInfo

    output = Mustache.to_html(HEADER_TEMPLATE, params)
    $("#header").html(output)

    feedbackData = config.feedback
    role = edwareUtil.getRole userInfo
    uid = edwareUtil.getUid userInfo
    # TODO might need to move this part to footer
    edwareUtil.renderFeedback(role, uid, "comparing_populations_" + reportType, feedbackData)

  create: create