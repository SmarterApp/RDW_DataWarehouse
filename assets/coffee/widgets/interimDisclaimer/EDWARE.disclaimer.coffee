define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  

  class EdwareDisclaimer
    
    constructor: (@content) ->
      @interimDisclaimerIcon = $('.interimDisclaimerIcon')
      @bindEvents()
      @

    displayPopover: ()->
      if this.hasLoaded()
        return
      self = this
      # make popup and make it stay
      @interimDisclaimerIcon.popover('show')
      setTimeout (->
        self.interimDisclaimerIcon.popover('hide')
      ), 10000
      # This will save that we've loaded it the first time
      @saveLoadedInfo()
      
    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      @interimDisclaimerIcon.popover
        html: true
        placement: "bottom"
        trigger: "hover"
        container: '#content'
        content: @content
      .on 'shown.bs.popover', ->
        offset = self.interimDisclaimerIcon.offset()
        popover = $('#content .popover')
        popover.css "left", offset.left + 17 - popover.width()
        # update arrow
        arrow = $(".arrow", popover)
        arrow.css "left", popover.width() - 10

    hasLoaded: () ->
      edwarePreferences.getInterimInfo()
    
    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()
    
    update: (asmtType) ->
      if asmtType is "Comprehensive Interim"
        @interimDisclaimerIcon.show()
      else
        @interimDisclaimerIcon.hide()
      @displayPopover()
        
  (($)->
    $.fn.edwareDisclaimer = (content) ->
      new EdwareDisclaimer(content)
  ) jQuery
