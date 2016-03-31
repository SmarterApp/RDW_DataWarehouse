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
  "mustache"
  "edwareDataProxy"
  "text!HelpMenuTemplate"
], ($, Mustache, edwareDataProxy, HelpMenuTemplate) ->
  class EdwareHelpMenu

    constructor: (@container, @isPublic, @config) ->
      self = this
      @HelpMenuModal = "#HelpMenuModal"
      edwareDataProxy.getDataForHelpContent().done (data) ->
        self.data = data
        self.initialize()
        self.bindEvents()

    initialize: () ->
      output = Mustache.to_html HelpMenuTemplate, {
          labels: @config.labels
          helpContent: @data
          isPublic: @isPublic
      } 
      $(@container).html(output)

    bindEvents: () ->
      self = this
      tabs = $('#helpMenuTab')
      # stop from triggering modal show event, such that last focused
      # element won't be reset
      tabs.find('a').on 'show', (e) ->
        e.stopPropagation()
      # show selected tab
      tabs.find('a').click (e) ->
        e.preventDefault()
        $this = $(this)
        self.setActiveTabId $this.attr('href')
        $this.tab 'show'
      # show tab when menu modal dropdown, if any
      $(@HelpMenuModal).on 'shown', ->
        if self.activeTab
          target = tabs.find("a[href='" + self.activeTab + "']")
        else
          target = tabs.find("a:first")
        target.tab 'show'
      $(window).resize (e) ->
        self.setModalSize()

    setActiveTabId: (tabId) ->
      @activeTab = tabId

    show: (tabId) ->
      @setActiveTabId tabId if tabId
      $(@HelpMenuModal).edwareModal()
      this.setModalSize()
    
    setModalSize: () ->
      # Adjust the modal height based on window height
      windowHeight = $(window).height()
      # This is an approximate height for content area in help modal
      if !@isPublic
        height = windowHeight - 210
        if height < 0
          height = 1
        $(@HelpMenuModal).css('height', height + 80 + 'px')
        content = $(@HelpMenuModal + ' .tab-content')
        content.css('height', height + 'px')
        content.css('max-height', height - 35 + 'px')

  create = (container, isPublic, config) ->
    new EdwareHelpMenu(container, isPublic, config)

  EdwareHelpMenu: EdwareHelpMenu
  create: create
