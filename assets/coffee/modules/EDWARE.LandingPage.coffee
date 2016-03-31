###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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
