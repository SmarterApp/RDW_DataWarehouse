define [
  'jquery'
  'mustache'
  'edwareUtil'
  'edwareSessionStorage'
  'text!edwareStickyCompareTemplate'
], ($, Mustache, edwareUtil, edwareSessionStorage, edwareStickyCompareTemplate) ->
  
  class EdwareGridStickyCompare
    
    constructor: (@callback) ->
      this.initialize()
      this
      
    initialize: () ->
      this.storage = edwareSessionStorage.stickyCompStorage
      this.bindEvents()
      this.createButtonBar()
      this.selectedRows = []

    # Sets information when we know what type of report it is, etc.
    # compareMode is set to false since we know that the html is reloaded
    setReportInfo: (@reportType, @orgName, @displayType, @params) ->
      this.compareMode = false
      
    update: () ->
      # Hide buttons based on whether any selection is already made
      # Only perform when compare mode is active
      if this.compareMode
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
          $(this).siblings("label").text("Compare")
          $(this).siblings("label").removeClass "stickyCompareLabelChecked"
          $(this).siblings("label").addClass "stickyCompareLabel"
          self.removeCurrentRow this
        else
          $(this).siblings("label").addClass "stickyCompareLabelChecked"
          $(this).siblings("label").removeClass "stickyCompareLabel"
          self.addCurrentRow this
  
      # Binds to compare button in summary row
      $(document).on 'click', '#stickyCompare-btn', () ->
        self.compareMode = true
        self.updateSelection() if self.selectedRows.length > 0
      
      # Deselect Button in summary row
      $(document).on 'click', '#stickyDeselect-btn', () ->
        self.selectedRows = []
        $('.stickyCheckbox').attr('checked', false)  
        $('.stickyCheckbox').siblings("label").text("Compare")
        self.resetCompareRowControls()
      
      # Show all district button
      $(document).on 'click', '#stickyShowAll-btn', () ->
        self.selectedRows = []
        self.updateSelection()
      
      # Remove button on each row in grid 
      $(document).on 'click', '.stickyCompareRemove', () ->
        self.removeCurrentRow this
        self.updateSelection()
    
    # Given a row in the grid, add its value to selectedRows
    addCurrentRow: (row) ->
      value = this.getCurrentRowValue row
      this.selectedRows.push value
    
    # Given a row in the grid, remove its value from selectedRows
    removeCurrentRow: (row) ->
      value = this.getCurrentRowValue row
      index = this.selectedRows.indexOf(value)
      this.selectedRows.splice(index, 1) if index > -1
    
    # Returns the value of a row
    getCurrentRowValue: (row) ->
      String($(row).data('value'))
    
    getSelectedRows: () ->
      # When this gets called, it means we should read from storage
      # Set the mode based on whether any rows are returned
      # Gets the rows selected for the current report view
      this.selectedRows = this.getDataForReport()
      this.compareMode = false
      if this.selectedRows.length > 0
        this.compareMode = true
      this.selectedRows
    
    getDataForReport: () ->
      # Gets the rows selected for the current report view
      data = this.getDataFromStorage()[this.reportType] || {}
      data[this.getOrgId()] || []
    
    # Saves to storage
    # Reset compare mode depending on whether any rows are selected
    updateSelection: () ->
      this.saveSelectedRowsToStorage()
      if this.selectedRows.length is 0 and this.compareMode
        this.compareMode = false
        this.hideCompareSection()
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
      this.updateDisplayText count
      if count > 0
        this.showCompareSelectedButtons()
      else
        # Hide all buttons
        this.hideCompareSection()
      $('.stickyCheckbox:checked').siblings("label").text(this.displayText)
      $('#stickyCompare-btn').text(this.displayText)

    updateDisplayText: (count) ->
      this.displayText = "Compare"
      if count > 0
        this.displayText  += " " + count + " " + this.displayType
        if count > 1
          this.displayText += "s"

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
