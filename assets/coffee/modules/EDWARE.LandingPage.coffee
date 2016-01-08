require [
  'jquery'
  'bootstrap'
  'mustache'
  'edwareDataProxy'
  'edwareModal'
  'text!templates/LandingPage.html'
  'edwareLanguageSelector'
  'edwareEvents'
], ($, bootstrap, Mustache, edwareDataProxy, edwareModal, landingPageTemplate, edwareLanguageSelector, edwareEvents) ->

  edwareDataProxy.getDataForLandingPage().done (data) ->
    output = Mustache.to_html landingPageTemplate, data
    $('body').html output
    #Add language selector
    edwareLanguageSelector.create $('.languageMenu'), data
    #bind events
    $('.btn-login').click ()->
      window.location.href = window.location.protocol + "//" + window.location.host + "/assets/html/index.html"
    $('.languageDropdown').click ()->
      $this = $(this)
      $this.toggleClass('show')
      $this.find('.divider').toggleClass('open')
      # toggle icon color
      $this.find('.edware-icon-globe-blue').toggleClass('edware-icon-globe-grayscale')
      $this.find('.edware-icon-downarrow-blue').toggleClass('edware-icon-downarrow-grayscale')

      $('.languageDropdown').focuslost ->
        $this = $(this)
        # collpase language dropdown menu if it's expanded
        $this.click() if $this.hasClass("show")
