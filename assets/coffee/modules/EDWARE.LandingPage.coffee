require [
  'jquery'
  'bootstrap'
  'mustache'
  'edwareDataProxy'
  'edwareModal'
  'edwareHelpMenu'
  'text!templates/LandingPage.html'
  'edwareLanguageSelector'
], ($, bootstrap, Mustache, edwareDataProxy, edwareModal, edwareHelpMenu, landingPageTemplate, edwareLanguageSelector) ->

  edwareDataProxy.getDataForLandingPage().done (data) ->
    output = Mustache.to_html landingPageTemplate, data
    $('body').html output
    helpMenu = edwareHelpMenu.create '.helpMenuContainer', data
    #Add language selector
    edwareLanguageSelector.create $('.languageMenu'), data
    #bind events
    $('.helpMenu a').click (e)->
      target = $(this).attr('href')
      helpMenu.show target
    $('.btn-login').click ()->
      window.location.href = window.location.protocol + "//" + window.location.host + "/assets/html/index.html"
    $('.languageDropdown').click ()->
      $this = $(this)
      $this.toggleClass('show')
      $this.find('.divider').toggleClass('open')
      # toggle icon color
      $this.find('.edware-icon-globe-blue').toggleClass('edware-icon-globe-grayscale')
      $this.find('.edware-icon-downarrow-blue').toggleClass('edware-icon-downarrow-grayscale')
