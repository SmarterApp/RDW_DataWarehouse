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

#global define
define [
  "jquery"
], ($) ->
  
  $(document).ready ->
    count = 0
    $("form").submit ->
      if $("#inputEmail").val() is ""
        $("#inputEmail").closest(".control-group").addClass "error"
        count++
      else 
        $("#inputEmail").closest(".control-group").removeClass "error"
        
      if $("#inputPassword").val() is ""
        $("#inputPassword").closest(".control-group").addClass "error"
        count++
      else
        $("#inputPassword").closest(".control-group").removeClass "error"
        
      return false if count > 0
      
      location.href = "/assets/html/studentList.html?districtId=4&schoolId=3&asmtGrade=1"
      false
