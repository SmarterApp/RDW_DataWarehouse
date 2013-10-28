define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  

  class EdwareDisclaimer
    
    constructor: (@disclaimerSection, @content) ->
      this.initialize()
      this.bindEvents()
      this.displayPopover()
      this

    displayPopover: ()->
      if this.hasLoaded()
        return
      # make popup and make it stay
      this.icon.mouseenter()
      setTimeout ()->
        $('.interimDisclaimerPopover').fadeOut(150)
      , 10000
      # This will save that we've loaded it the first time
      this.saveLoadedInfo()
      
    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      this.icon.popover
        html: true
        placement: "bottom"
        trigger: "manual"
        container: '#interimDisclaimerPopover'
        content: self.content
      .mouseenter ()->
        # move popover
        $(this).popover 'show'
        self.setPosition()
      .mouseleave ()->
        $(this).popover "hide"

    setPosition: ()->
      offset = this.icon.offset()
      popover = $('#interimDisclaimerPopover .popover')
      popover.css "left", offset.left + 17 - popover.width()

      # update arrow
      arrow = $(".arrow", popover)
      arrow.css "left", popover.width() - 10

    # Call this to create the disclaimer icon
    initialize: () ->
      interimDisclaimerIcon = $('<div class="interimDisclaimerIcon"></div>')
      this.disclaimerSection.append interimDisclaimerIcon
      this.icon = $('.interimDisclaimerIcon')
      this.container = $('.disclaimerInfo')
   
    hasLoaded: () ->
      edwarePreferences.getInterimInfo()
    
    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()
    
    update: (asmtType) ->
      if asmtType is "Comprehensive Interim"
        this.disclaimerSection.show()
      else
        this.disclaimerSection.hide()
        
  (($)->
    $.fn.edwareDisclaimer = (content) ->
      new EdwareDisclaimer($(this), content)
  ) jQuery
