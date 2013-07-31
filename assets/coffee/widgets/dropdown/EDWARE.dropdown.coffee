define [
  "jquery"
  "mustache"
  "text!edwareDropdownTemplate"
], ($, Mustache, dropdownTemplate) ->

  # create dropdown menu for color bars
  class EdwareDropdownMenu
    
    constructor: (@dropdown, @config, @callback) ->
      this.initialize()
      this.menu = this.create()
      this.bindEvents()
      return this.menu

    initialize: () ->
      # get <div> object where dropdown menu will be appear
      this.asmtSubjectSort = $('#' + this.config['asmtSubject'] + "_sort")
    
    bindEvents: () ->
      self = this;
      $('input.inputColorBlock', this.menu).click (e) ->
        self.dropdown.resetDropdown()
        self.sort e.target
        self.dropdown.setCenter()

    sort: (sortItem) ->
      $this = $(sortItem)
      # check current selection
      $this.attr('checked', true)
      dropdown = $this.closest('div.dropdown')
      subject = dropdown.data('subject')
      # obtain selected color bar and set it to table header
      colorBar = $this.next().clone()
      #set the center of table header
      dropdownTitle = $('.dropdown_title', dropdown)
      dropdownTitle.html(colorBar)
      this.dropdown.callback subject

    create: () ->
      # create dropdown and set to the center of each colomn
      output = $(Mustache.to_html dropdownTemplate, this.config)
      # remove the last color bar
      output.find('li:nth-last-child(2)').remove()
      # set margin for color bar
      options = output.find('li')
      $.each options, (index, element) ->
        $('.colorBlock', element).eq(index).addClass('margin_right')
        # set index for sorting
        $('input', element).attr('data-index', index)
      output

  class EdwareDropdown
    
    constructor: (@dropdownSection, @customALDDropdown, @callback) ->
      this.menus = {}
      
    initialize: () ->
      # Hide the drop down if data is empty
      this.hideEmptyData()
      this.create()
      
    hideEmptyData: () ->
      for subject, asmtSubject of this.asmtSubjectsData
        if not this.hasData(subject) and this.hasMenu(subject)
          $(this.menus[subject]).remove()
          this.menus[subject] = undefined
    
    create: () ->
      for subject, asmtSubject of this.asmtSubjectsData
        if this.hasSubject(subject) and not this.hasMenu(subject)
          config = this.generateConfig(subject, asmtSubject)
          menu = new EdwareDropdownMenu(this, config)
          #cache generated dropdown menu
          this.menus[subject] = menu
          $(this.dropdownSection).append menu
          
    hasData: (subject) ->
      this.summaryData.results and this.summaryData.results[subject]

    hasSubject: (subject) ->
      this.colorsData[subject] isnt undefined
     
    hasMenu: (subject) ->
      this.menus[subject] isnt undefined

    generateConfig: (subject, asmtSubject) ->
      this.config = {}
      this.config['totalStudents'] = this.customALDDropdown.totalStudents
      this.config['selectSort'] = this.customALDDropdown.selectSort
      this.config['colors'] = this.colorsData[subject]
      this.config['asmtSubject'] = asmtSubject
      this.config
          
    setCenter: () ->
      self = this
      $(".dropdown").each (index, element) ->
        subject = $(element).data('subject')
        width = $('.dropdown_title', element).width()
        self.setCenterForDropdown(subject, width, element)
  
    setCenterForDropdown: (subject_name, width, targetElement) ->
      position = $('#' + subject_name + '_sort').parent().offset()
      parent_position = $('#' + subject_name + '_sort').closest('.gridHeight100').offset()
      position.left -= parent_position.left
      position.top -= parent_position.top
      position.left = position.left + $('#' + subject_name + '_sort').parent().width()/2-width/2
      $(targetElement).closest('.dropdown').css('margin-left', position.left).css('margin-top', position.top)

    resetAll: () ->
      # reset dropdown state
      this.resetDropdown()
      this.setCenter()

    resetDropdown: () ->
      # unselect radio button
      $('.inputColorBlock').attr('checked', false)
      $(".dropdown").removeClass('open')
      $('.dropdown_title').html this.config['selectSort']

    update: (@summaryData, @asmtSubjectsData, @colorsData) ->
      this.initialize()
      this.setCenter()
      
  #
  #    *  EDWARE Filter plugin
  #    *  @param filterHook - Panel config data
  #    *  @param filterTrigger - 
  #    *  @param callback - callback function, triggered by click event on apply button
  #    *  Example: $("#table1").edwareFilter(filterTrigger, callbackFunction)
  #  
  (($)->
    $.fn.edwareDropdown = (customALDDropdown, callback) ->
      new EdwareDropdown($(this), customALDDropdown, callback)
  ) jQuery
