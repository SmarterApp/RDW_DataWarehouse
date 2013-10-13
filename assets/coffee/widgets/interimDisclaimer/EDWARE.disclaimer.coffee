define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  
  DISCLAIMER_TEMPLATE =  
    '<div class="interimDisclaimerIcon">' +
      '<div class="interimDisclaimer hide">{{{content}}}</div>' +
    '</div>'

  DISCLAIMER_POPOVER_TEMPLATE = '<div class="popover interimDisclaimerPopover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
  
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
        this.popover.fadeOut(150) if this.popover
      , 3000
      # This will save that we've loaded it the first time
      this.saveLoadedInfo()
      
    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      this.icon.popover
        html: true
        placement: "bottom"
        trigger: "manual"
        template: DISCLAIMER_POPOVER_TEMPLATE
        content: ->
          $(this).find(".interimDisclaimer").html()
      .mouseenter ()->
        $(this).popover('show')
        popover = $('.interimDisclaimerPopover').remove()
        self.icon.append popover
      .mouseleave ()->
        $(this).popover('hide')

    # Call this to create the disclaimer icon
    initialize: () ->
      output = Mustache.to_html DISCLAIMER_TEMPLATE, {'content': this.content}
      this.disclaimerSection.html output
      this.icon = $('.interimDisclaimerIcon')
      this.popover = $('.interimDisclaimerPopover')
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
