define [
  'jquery'
  'mustache'
  'edwareUtil'
  'edwareSessionStorage'
  'text!edwareStickyCompareTemplate'
], ($, Mustache, edwareUtil, edwareSessionStorage, edwareStickyCompareTemplate) ->
  
  class EdwareGridStickyCompare
    
    constructor: (@reportType, @orgName, @displayType, @params, @callback) ->
      this.initialize()
      
    initialize: () ->
      this.storage = edwareSessionStorage.stickyCompStorage
      this.selectedRows = this.getSelectedRows()
      this.bindEvents()
      this.createButtonBar()

    update: () ->
      # show and hide appropriate buttons
      # Hide buttons based on whether any selection is already made
      this.selectedRows = this.getSelectedRows()
      if this.selectedRows.length > 0
        this.showCompareEnabledButtons()
      else
        this.hideCompareSection()
        
    # All events related to grid filtering of rows
    bindEvents: () ->
      self = this  
      # checkboxes in each row
      $(document).on 'click', '.stickyCheckbox', () ->
        self.resetCompareRowControls()
        if not $(this).is(':checked')
          $(this).siblings("label").text(self.displayText)
          $(this).siblings("label").removeClass "stickyCompareLabelChecked"
          $(this).siblings("label").addClass "stickyCompareLabel"
        else
          $(this).siblings("label").addClass "stickyCompareLabelChecked"
          $(this).siblings("label").removeClass "stickyCompareLabel"
  
      # Binds to compare button in summary row
      $(document).on 'click', '#stickyCompare-btn', () ->
        self.selectedRows = []
        $('.stickyCheckbox:checked').each () ->
          value = String($(this).data('value'))
          self.selectedRows.push value
        if self.selectedRows.length > 0
          self.updateSelection()
          self.showCompareEnabledButtons()
      
      # Deselect Button in summary row
      $(document).on 'click', '#stickyDeselect-btn', () ->
        self.selectedRows = []
        $('.stickyCheckbox').attr('checked', false)  
        self.resetCompareRowControls()
        $('.stickyCheckbox').siblings("label").text(self.displayText)
      
      # Show all district button
      $(document).on 'click', '#stickyShowAll-btn', () ->
        self.selectedRows = []
        self.updateSelection()
      
      # Remove button on each row in grid 
      $(document).on 'click', '.stickyCompareRemove', () ->
        value = String($(this).data('value'))
        index = self.selectedRows.indexOf(value)
        self.selectedRows.splice(index, 1) if index > -1
        self.updateSelection()
        
    getSelectedRows: () ->
      # TODO more elegent way?
      data = this.getDataFromStorage()[this.reportType]
      if not data then data = {}
      data = data[this.getOrgId()]
      if not data then data = []
      data

    updateSelection: () ->
      this.saveSelectedRowsToStorage()
      # calls a callback function (render grid)
      this.callback()

   # Update session storage for selected rows
    saveSelectedRowsToStorage: () ->
      if this.reportType in ['state', 'district']
        data = this.getDataFromStorage()
        reportData = data[this.reportType]
        reportData = {} if not reportData
        reportData[this.getOrgId()] = this.selectedRows
        data[this.reportType] = reportData
        this.storage.save data
   
    getDataFromStorage: () ->
      data = JSON.parse(this.storage.load())
      if not data then data = {}
      data
      
    getOrgId: () ->
      if this.params['districtGuid']
        id  = this.params['districtGuid']
      else if this.params['stateCode']
        id  = this.params['stateCode']
      id
      
    # Reset Grid rows checkbox and button text
    resetCompareRowControls: () ->
      count = $('.stickyCheckbox:checked').length
      text =  "Compare"
      if count > 0
        text  += " " + count + " " + this.displayType
        this.showCompareSelectedButtons()
        if count > 1
          text += "s"
      else
        # Hide all buttons
        this.hideCompareSection()
      $('.stickyCheckbox:checked').siblings("label").text(text)
      $('#stickyCompare-btn').text(text)
    
    createButtonBar: () ->
      output = Mustache.to_html edwareStickyCompareTemplate, {}
      $('#stickyCompareSection').html output
      this.hideCompareSection()
   
    hideCompareSection: () ->
      $('#stickyCompareSection').hide()
    
    showCompareSection: () ->
      $('#stickyCompareSection').show()

    showCompareSelectedButtons: () ->
      this.showCompareSection()
      $('#compareSelectedActions').show()
      $('#compareEnabledActions').hide()
    
    showCompareEnabledButtons: () ->
      this.showCompareSection()
      $('#stickyShowAll-btn').text("Show All " + this.displayType + "s")
      count = this.selectedRows.length
      text = "Comparing " + String(count) + " " + this.orgName + " " + this.displayType
      text += "s" if count > 1
      $('#stickyEnabledDescription').text(text)
      $('#compareSelectedActions').hide()
      $('#compareEnabledActions').show()
  
  
  EdwareGridStickyCompare:EdwareGridStickyCompare
