define [
  'jquery'
  'mustache'
], ($, Mustache) ->
  #
  # * EDWARE util
  # * Handles constants, reusable or common methods required by other EDWARE javascript files
  #

  #global $ window

  constants =
      overall_ald: 275
      psychometric_characterLimits: 256
      policyContent_characterLimits: 256
      claims_characterLimits: 140

  getConstants = (value) ->
    constants[value]

  displayNoResultsMessage = ->
    displayErrorMessage "There is no data available for your request."

  displayErrorMessage = (error) ->

    if error isnt ""
      $("#errorMessage").show().html(error)
    else
      $("#errorMessage").hide()

  getUrlParams = ->
    params = {}
    decoded = decodeURIComponent(window.location.search).replace(/\+/g, ' ')
    decoded.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
      params[key] = value

    params

  # Given an user_info object, return the one role of that user from the list
  getRole = (userInfo) ->
    # roles is a list, for beta, we can assume we only have 1 role
    userInfo._User__info.roles[0].toUpperCase()

  # Given an user_info object, return the first and last name of the user
  getUserName = (userInfo) ->
    userInfo._User__info.name.firstName + ' ' + userInfo._User__info.name.lastName

  # Given an user_info object, return the uid
  getUid = (userInfo) ->
    userInfo._User__info.uid

  # Given an user_info object, return the uid
  getGuid = (userInfo) ->
    userInfo._User__info.guid

  # Given an user_info object, return the state_code
  getUserStateCode = (userInfo) ->
    userInfo._User__info.stateCode

  getDisplayBreadcrumbsHome = (userInfo) ->
    userInfo._User__info.displayHome

  format_full_name_reverse = (first_name, middle_name, last_name) ->
    if (middle_name && middle_name.length > 0)
        middle_init = middle_name[0] + '.'
    else
        middle_init = ''
    return "#{last_name}, #{first_name} #{middle_init}".replace '  ', ' '

  # truncate the content and add ellipsis "..." if content is more than character limits
  truncateContent = (content, characterLimits)->
    if content.length > characterLimits
      content = content.substr(0, characterLimits)

      # ignore characters after the last word
      content = content.substr(0, content.lastIndexOf(' ') + 1) + "..."

    content

  # Set the popup position to left, right, top, bottom
  popupPlacement = (element, popupWidth, popupHeight)->
    isWithinBounds = (elementPosition) ->
        boundTop < elementPosition.top and boundLeft < elementPosition.left and boundRight > (elementPosition.left + actualWidth) and boundBottom > (elementPosition.top + actualHeight)

    $element = $(element)
    pos = $.extend({}, $element.offset(),
      width: element.offsetWidth
      height: element.offsetHeight
    )
    actualWidth = popupWidth
    actualHeight = popupHeight
    boundTop = $(document).scrollTop()
    boundLeft = $(document).scrollLeft()
    boundRight = boundLeft + $(window).width()
    boundBottom = boundTop + $(window).height()
    elementAbove =
      top: pos.top - actualHeight
      left: pos.left + pos.width / 2 - actualWidth / 2

    elementBelow =
      top: pos.top + pos.height
      left: pos.left + pos.width / 2 - actualWidth / 2

    elementLeft =
      top: pos.top + pos.height / 2 - actualHeight / 2
      left: pos.left - actualWidth

    elementRight =
      top: pos.top + pos.height / 2 - actualHeight / 2
      left: pos.left + pos.width

    above = isWithinBounds(elementAbove)
    below = isWithinBounds(elementBelow)
    left = isWithinBounds(elementLeft)
    right = isWithinBounds(elementRight)
    if above
      "top"
    else
      if below
        "bottom"
      else
        if left
          "left"
        else
          if right
            "right"
          else
            "left"

  showGrayScale = ->
    $('head').append("<link rel='stylesheet' type='text/css' href='../css/grayscale.css' />");

  showPdfCSS = ->
    $('head').append("<link rel='stylesheet' type='text/css' href='../css/pdf.css' />");

  # Add comma as thousand separator to numbers
  # Return 0 if parameter is undefined
  formatNumber = (num) ->
    if num then num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") else 0

  reRenderBody = (labels) ->
    body = $('body').html()
    output = Mustache.to_html body, {
        labels: labels
    }
    $('body').html output

  escapeCSV = (value) ->
    if typeof(value) is 'string'
      # escape double quote
      return '"' + value + '"'
    else if typeof(value) is 'number'
      return '"' + value + '"'
    else if $.isArray(value)
      for item in value
        escapeCSV item
    else
      value

  getBaseURL = ->
    window.location.protocol + "//" + window.location.host

  getAcademicYears = (years)->
    return if not years
    for year in years
      "display": toDisplay(year),
      "value": year

   toDisplay = (year)->
    (year - 1) + " - " + year

  deepFind = (obj, path) ->
    paths = path.split('.')

    for currentPath in paths
      return obj if not obj
      obj = obj[currentPath]

    return obj

  getAbsolutePathForBrandingResource = (path) ->
    # If it starts with \, then it's some abs path
    if /^\/.+\..+/.test path
      return path
    else
      return '/assets/images/branding/' + path

  getTenantLevelBrandingData = (metadata) ->
    brandingData = {'tenantLogo': '/assets/images/smarterHeader_logo.png', 'tenantLabel': ''}
    if metadata and metadata.branding
      brandingData.tenantLogo = getAbsolutePathForBrandingResource metadata.branding.image if metadata.branding.image
      brandingData.tenantLabel = truncateContent metadata.branding.display, 50 if metadata.branding.display
    return brandingData

  getTenantLevelBrandingDataForPrint = (metadata, isGrayscale) ->
    brandingData = {'tenantLogo': '/assets/images/smarter_printlogo.png', 'tenantLabel': '', 'tenantLogoHeight': '47', 'tenantLogoWideth': '150'}
    if metadata and metadata.branding
      brandingData.tenantLogo = getAbsolutePathForBrandingResource metadata.branding.image if metadata.branding.image
      brandingData.tenantLabel = truncateContent metadata.branding.display, 50 if metadata.branding.display
      brandingData.tenantLogoHeight = '' if metadata.branding.image
      brandingData.tenantLogoWidth = '' if metadata.branding.image
    else if isGrayscale
        brandingData.tenantLogo = "../images/smarter_printlogo_gray.png"
    return brandingData

  getConstants: getConstants
  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams
  getRole: getRole
  getUserName: getUserName
  getUid: getUid
  getGuid: getGuid
  getUserStateCode: getUserStateCode
  getDisplayBreadcrumbsHome: getDisplayBreadcrumbsHome
  truncateContent: truncateContent
  popupPlacement: popupPlacement
  format_full_name_reverse: format_full_name_reverse
  showGrayScale : showGrayScale
  showPdfCSS : showPdfCSS
  formatNumber: formatNumber
  displayNoResultsMessage: displayNoResultsMessage
  reRenderBody: reRenderBody
  escapeCSV: escapeCSV
  getBaseURL: getBaseURL
  getAcademicYears: getAcademicYears
  deepFind: deepFind
  getTenantLevelBrandingData: getTenantLevelBrandingData
  getTenantLevelBrandingDataForPrint: getTenantLevelBrandingDataForPrint
