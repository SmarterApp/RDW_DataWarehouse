define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  
  # TODO: put content in json and i18n
  DISCLAIMER_TEMPLATE =  
    '<div class="interimDisclaimerIcon">' +
    '<div class="interimDisclaimer hide">' +
     '1.      Tasks and items on interim tests are scored locally by teachers  This is a professional development opportunity for teachers that promotes understanding of scoring activity. Local scoring, however, is not subject to the rigorous controls used in summative assessment. Local results may show some variation.' +
     '2.      Interim assessment questions are not secure. They may be used for classroom discussion or in shorter, more targeted tests.  When this is the case, familiarity with test questions my affect student performance.' +
     '3.      If test questions are shared widely, item parameters may differ from those established in secure field testing. This affects the accuracy of interim scale scores.' +
     '</div>' +
     '</div>'
  class EdwareDisclaimer
    
    constructor: (@disclaimerSection) ->
      this.bindEvents()
      this
      
    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      $(document).on 'mouseenter', '.interimDisclaimerIcon', (e) ->
          e = $(this)
          e.popover
            html: true
            placement: "bottom"
            trigger: "manual"
            template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
            content: ->
              e.find(".interimDisclaimer").html() 
          .popover("show")
      $(document).on 'click', '.interimDisclaimerIcon', (e) ->
          e.preventDefault()
      $(document).on 'mouseleave', '.interimDisclaimerIcon', (e) ->
          e = $(this)
          e.popover("hide")

    # Call this to create the disclaimer icon
    create: () ->
      this.disclaimerSection.html DISCLAIMER_TEMPLATE
      if not this.hasLoaded()
        # TODO make popup and make it stay
        
        # This will save that we've loaded it the first time
        this.saveLoadedInfo()
   
    hasLoaded: () ->
      edwarePreferences.getInterimInfo()
    
    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()
        
  (($)->
    $.fn.edwareDisclaimer = () ->
      new EdwareDisclaimer($(this))
  ) jQuery
