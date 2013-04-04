(function() {
  define(["jquery", "bootstrap", "mustache", "edwareDataProxy", "edwareGrid", "edwareBreadcrumbs", "text!edwareAssessmentDropdownViewSelectionTemplate", "edwareFeedback", "edwareUtil", "edwareHeader"], function($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareAssessmentDropdownViewSelectionTemplate, edwareFeedback, edwareUtil, edwareHeader) {
    var assessmentsData, createAssessmentViewSelectDropDown, createStudentGrid, formatAssessmentsData, getStudentData, getStudentsConfig, renderStudentGrid, studentsConfig, subjectsData;

    assessmentsData = {};
    studentsConfig = {};
    subjectsData = {};
    createStudentGrid = function(params) {
      var options;

      options = {
        async: false,
        method: "GET"
      };
      return edwareDataProxy.getDatafromSource("../data/color.json", options, function(defaultColors) {
        return getStudentData("/data/list_of_students", params, defaultColors, function(assessmentsData, contextData, subjectsData, claimsData, userData) {
          $("#school_name").html(contextData.items[2].name);
          return getStudentsConfig("../data/student.json", function(callback_studentsConfig) {
            var combinedData, defaultView, output, role, uid;

            studentsConfig = callback_studentsConfig;
            if (assessmentsData['ALL'].length > 0) {
              combinedData = subjectsData;
              combinedData.claims = claimsData;
              output = Mustache.render(JSON.stringify(studentsConfig), combinedData);
              studentsConfig = JSON.parse(output);
            }
            defaultView = createAssessmentViewSelectDropDown(studentsConfig.customViews);
            $('#header').header();
            $('#breadcrumb').breadcrumbs(contextData);
            renderStudentGrid(defaultView);
            if (userData) {
              $('#header .topLinks .user').html(edwareUtil.getUserName(userData));
              role = edwareUtil.getRole(userData);
              uid = edwareUtil.getUid(userData);
              return edwareFeedback.renderFeedback(role, uid, "list_of_students");
            }
          });
        });
      });
    };
    renderStudentGrid = function(viewName) {
      var dataName;

      $("#gbox_gridTable").remove();
      $("#content").append("<table id='gridTable'></table>");
      edwareUtil.displayErrorMessage("");
      dataName = viewName.toUpperCase();
      if (!(dataName in assessmentsData)) {
        dataName = 'ALL';
      }
      edwareGrid.create("gridTable", studentsConfig[viewName], assessmentsData[dataName]);
      return $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(5), .ui-jqgrid tr.jqgrow td:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(5)').css("border-right", "solid 1px #B1B1B1");
    };
    getStudentData = function(sourceURL, params, defaultColors, callback) {
      var assessmentArray, options;

      assessmentArray = [];
      if (sourceURL === "undefined" || typeof sourceURL === "number" || typeof sourceURL === "function" || typeof sourceURL === "object") {
        return false;
      }
      options = {
        async: true,
        method: "POST",
        params: params
      };
      return edwareDataProxy.getDatafromSource(sourceURL, options, function(data) {
        var claimsData, contextData, cutPointsData, items, j, key, userData;

        assessmentsData = data.assessments;
        contextData = data.context;
        subjectsData = data.subjects;
        claimsData = data.metadata.claims;
        cutPointsData = data.metadata.cutpoints;
        userData = data.user_info;
        for (key in cutPointsData) {
          items = cutPointsData[key];
          j = 0;
          while (j < items.cut_point_intervals.length) {
            if (!items.cut_point_intervals[j].bg_color) {
              $.extend(items.cut_point_intervals[j], defaultColors[j]);
            }
            j++;
          }
        }
        formatAssessmentsData(cutPointsData);
        if (callback) {
          return callback(assessmentsData, contextData, subjectsData, claimsData, userData);
        } else {
          return assessmentArray(assessmentsData, contextData, subjectsData, claimsData, userData);
        }
      });
    };
    getStudentsConfig = function(configURL, callback) {
      var options, studentColumnCfgs;

      studentColumnCfgs = {};
      if (configURL === "undefined" || typeof configURL === "number" || typeof configURL === "function" || typeof configURL === "object") {
        return false;
      }
      options = {
        async: false,
        method: "GET"
      };
      return edwareDataProxy.getDatafromSource(configURL, options, function(data) {
        if (callback) {
          return callback(data);
        } else {
          return data;
        }
      });
    };
    createAssessmentViewSelectDropDown = function(customViewsData) {
      var defaultView, items, key, output, value;

      items = [];
      for (key in customViewsData) {
        value = customViewsData[key];
        items.push({
          'key': key,
          'value': value
        });
      }
      output = Mustache.to_html(edwareAssessmentDropdownViewSelectionTemplate, {
        'items': items
      });
      $("#content #select_measure").append(output);
      $(document).on({
        click: function(e) {
          var viewName;

          e.preventDefault();
          viewName = $(this).attr("id");
          $("#select_measure_current_view").html($('#' + viewName).text());
          renderStudentGrid(viewName);
          if (viewName === "Math_ELA") {
            return $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(5), .ui-jqgrid tr.jqgrow td:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(5)').css("border-right", "solid 1px #b1b1b1");
          } else {
            $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(5), .ui-jqgrid tr.jqgrow td:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(5)').css("border-right", "solid 1px #d0d0d0");
            return $('.ui-jqgrid tr.jqgrow td:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(5)').css("border-right", "solid 1px #E2E2E2");
          }
        }
      }, ".viewOptions");
      defaultView = items[0].key;
      $("#select_measure_current_view").html($('#' + defaultView).text());
      return defaultView;
    };
    formatAssessmentsData = function(assessmentCutpoints) {
      var allAssessments, assessment, cutpoint, key, row, value, _i, _len, _ref;

      allAssessments = {
        'ALL': assessmentsData
      };
      for (key in subjectsData) {
        value = subjectsData[key];
        allAssessments[value.toUpperCase()] = [];
      }
      _ref = allAssessments["ALL"];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        row = _ref[_i];
        assessment = row['assessments'];
        for (key in subjectsData) {
          value = subjectsData[key];
          if (key in assessment) {
            cutpoint = assessmentCutpoints[key];
            $.extend(assessment[key], cutpoint);
            assessment[key].score_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl - 1].bg_color;
            allAssessments[value.toUpperCase()].push(row);
          }
        }
      }
      return assessmentsData = allAssessments;
    };
    return {
      createStudentGrid: createStudentGrid
    };
  });

}).call(this);
