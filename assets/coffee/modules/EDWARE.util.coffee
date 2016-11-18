###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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
      overall_ald: 305
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

  getErrorPage = ->
    "/assets/public/error.html"
    
  getUrlParams = ->
    params = {}
    decoded = decodeURIComponent(window.location.search).replace(/\+/g, ' ')
    decoded.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
      params[key] = value

    params

  isPublicReport = () ->
    params = getUrlParams()
    'isPublic' of params and params['isPublic'].toLowerCase() == "true"
  
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

  formatDate = (date) ->
    if not date
      return ""
    date = date.toString()
    return "#{date[0..3]}.#{date[4..5]}.#{date[6..]}"

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

  getTenantBrandingData = (metadata) ->
    return getTenantBranding(metadata, false, false)

  getTenantBrandingDataForPrint = (metadata, isGrayscale) ->
    return getTenantBranding(metadata, true, isGrayscale)

  getTenantBranding = (metadata, isPrint, isGrayscale) ->
    defaultLogo = '/assets/images/smarterHeader_logo.png'
    if isPrint
      defaultLogo = if isGrayscale then '/assets/images/smarter_printlogo_gray.png' else '/assets/images/smarter_printlogo.png'
    brandingData = {'tenantLogo': defaultLogo, 'tenantLabel': '', 'higherEdLink':''}
    if metadata and metadata.branding
      brandingData.tenantLogo = getAbsolutePathForBrandingResource metadata.branding.image if metadata.branding.image
      brandingData.tenantLabel = truncateContent metadata.branding.display, 50 if metadata.branding.display
      brandingData.higherEdLink = metadata.branding.higherEdLink
    return brandingData

  deepCopy = (object, maximumDepth, currentDepth) ->
    copy = undefined
    maximumDepth = if typeof maximumDepth == 'number' then maximumDepth else 10
    currentDepth = if typeof currentDepth == 'number' then currentDepth else 0
    if currentDepth >= maximumDepth
      throw new Error('Deep copy failed. Maximum recursive depth of ' + maximumDepth + ' exceeded')
    # Handle the 3 simple types, and null or undefined
    if object == null or typeof object != 'object' or object instanceof RegExp
      return object
    # Handle Date
    if object instanceof Date
      copy = new Date
      copy.setTime object.getTime()
      return copy
    # Handle Array
    if object instanceof Array
      copy = []
      i = 0
      length = object.length
      while i < length
        copy[i] = deepCopy(object[i], maximumDepth, currentDepth + 1)
        i++
      return copy
    # Handle Object
    if object instanceof Object
      copy = {}
      for property of object
        if object.hasOwnProperty(property)
          copy[property] = deepCopy(object[property], maximumDepth, currentDepth + 1)
      return copy
    throw new Error('Deep copy failed. Unsupported type "' + object.constructor.name + '"')
    return

  getConstants: getConstants
  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams
  isPublicReport: isPublicReport
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
  getTenantBrandingData: getTenantBrandingData
  getTenantBrandingDataForPrint: getTenantBrandingDataForPrint
  formatDate: formatDate
  getErrorPage: getErrorPage
  deepCopy: deepCopy
