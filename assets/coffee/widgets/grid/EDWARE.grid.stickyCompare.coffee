define [
  'jquery'
  'edwareUtil'
  'edwareSessionStorage'
], ($, edwareUtil, edwareSessionStorage) ->
  
  class EdwareGridStickyCompare
    
    constructor: (@reportType, @params, @callback) ->
      this.initialize()
      
    initialize: () ->
      this.storage = edwareSessionStorage.stickyCompStorage
      this.selectedRows = this.getSelectedRows()
      this.bindEvents()

    reset: () ->
      this.bindEvents()
      this.hideButtons()
        
    # All events related to grid filtering of rows
    bindEvents: () ->
      self = this  
      # checkboxes in each row
      $('.stickyCheckbox').click () ->
        text = self.resetCompareRowControls()
        if not $(this).is(':checked')
          $(this).siblings("label").text(text)
          $(this).siblings("label").removeClass "stickyCompareLabelChecked"
          $(this).siblings("label").addClass "stickyCompareLabel"
        else
          $(this).siblings("label").addClass "stickyCompareLabelChecked"
          $(this).siblings("label").removeClass "stickyCompareLabel"
  
      # Binds to compare button in summary row
      $('#stickyCompare').click () ->
        self.selectedRows = []
        $('.stickyCheckbox:checked').each () ->
          value = String($(this).data('value'))
          self.selectedRows.push value
        if self.selectedRows.length > 0
          self.updateSelection() 
      
      # Deselect Button in summary row
      $('#stickyDeselectAllRows').click () ->
        self.selectedRows = []
        $('.stickyCheckbox').attr('checked', false)  
        text = self.resetCompareRowControls()
        $('.stickyCheckbox').siblings("label").text(text)
      
      # Show all district button
      $('#stickyShowAll').click () ->
        self.selectedRows = []
        self.updateSelection()
      
      # Remove button on rows 
      $('.stickyCompareRemove').click () ->
        value = String($(this).data('value'))
        index = self.selectedRows.indexOf(value)
        self.selectedRows.splice(index, 1) if index > -1
        self.updateSelection()
        
    hideButtons: () ->
      # Hide buttons
      $('#stickyCompare').hide()
      $('#stickyDeselectAllRows').hide()
 
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
      text = "Compare"
      count = $('.stickyCheckbox:checked').length
      if count > 0
        # Show button
        $('#stickyCompare').show()
        $('#stickyDeselectAllRows').show()
        if this.reportType is "state" then orgType = "District" else orgType = "School"
        text += " " + count + " " + orgType
        if count > 1
          text += "s"
      else
        $('#stickyCompare').hide()
        $('#stickyDeselectAllRows').hide()
      $('.stickyCheckbox:checked').siblings("label").text(text)
      $('#stickyCompare').text(text)
      text
  
  EdwareGridStickyCompare:EdwareGridStickyCompare
