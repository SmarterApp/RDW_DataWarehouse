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
