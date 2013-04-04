(function() {
  define(["jquery", "bootstrap", "edwareDataProxy", "edwareGrid", "edwareBreadcrumbs", "edwareUtil", "edwareFeedback", "edwareHeader"], function($, bootstrap, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareFeedback, edwareHeader) {
    var addApostropheS, appendColor, appendColorToData, createPopulationGrid, formatSummaryData, getColumnConfig, getOverallSummaryName, getPopulationData, getReportTitle, getReportType;

    createPopulationGrid = function(params) {
      return getPopulationData("/data/comparing_populations", params, function(populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info) {
        var defaultColors, options;

        defaultColors = {};
        options = {
          async: false,
          method: "GET"
        };
        return edwareDataProxy.getDatafromSource("../data/color.json", options, function(defaultColors) {
          return getColumnConfig("../data/comparingPopulations.json", function(gridConfig, customViews) {
            var reportTitle, reportType, role, summaryRowName, uid;

            reportType = getReportType(params);
            if (populationData.length > 0) {
              populationData = appendColorToData(populationData, asmtSubjectsData, colorsData, defaultColors);
              summaryData = appendColorToData(summaryData, asmtSubjectsData, colorsData, defaultColors);
              gridConfig[0].name = customViews[reportType].name;
              gridConfig[0].options.linkUrl = customViews[reportType].link;
              gridConfig[0].options.id_name = customViews[reportType].id_name;
              $('#header').header();
              $('#breadcrumb').breadcrumbs(breadcrumbsData);
              reportTitle = getReportTitle(breadcrumbsData, reportType);
              $('#content h2').html(reportTitle);
              summaryRowName = getOverallSummaryName(breadcrumbsData, reportType);
              summaryData = formatSummaryData(summaryData, summaryRowName);
            }
            edwareGrid.create("gridTable", gridConfig, populationData, summaryData);
            if (user_info) {
              $('#header .topLinks .user').html(edwareUtil.getUserName(user_info));
              role = edwareUtil.getRole(user_info);
              uid = edwareUtil.getUid(user_info);
              edwareFeedback.renderFeedback(role, uid, "comparing_populations_" + reportType);
            }
            return $(document).on({
              mouseenter: function() {
                var e;

                e = $(this);
                return e.popover({
                  html: true,
                  placement: "top",
                  template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>',
                  content: function() {
                    return e.find(".progressBar_tooltip").html();
                  }
                }).popover("show");
              },
              mouseleave: function() {
                var e;

                e = $(this);
                return e.popover("hide");
              }
            }, ".progress");
          });
        });
      });
    };
    getPopulationData = function(sourceURL, params, callback) {
      var dataArray, options;

      dataArray = [];
      if (sourceURL === "undefined" || typeof sourceURL === "number" || typeof sourceURL === "function" || typeof sourceURL === "object") {
        return false;
      }
      options = {
        async: true,
        method: "POST",
        params: params
      };
      return edwareDataProxy.getDatafromSource(sourceURL, options, function(data) {
        var asmtSubjectsData, breadcrumbsData, colorsData, populationData, summaryData, user_info;

        populationData = data.records;
        summaryData = data.summary;
        asmtSubjectsData = data.subjects;
        colorsData = data.colors;
        breadcrumbsData = data.context;
        user_info = data.user_info;
        if (callback) {
          return callback(populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info);
        } else {
          return dataArray(populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info);
        }
      });
    };
    getColumnConfig = function(configURL, callback) {
      var dataArray, options;

      dataArray = [];
      if (configURL === "undefined" || typeof configURL === "number" || typeof configURL === "function" || typeof configURL === "object") {
        return false;
      }
      options = {
        async: false,
        method: "GET"
      };
      return edwareDataProxy.getDatafromSource(configURL, options, function(data) {
        var comparePopCfgs, schoolColumnCfgs;

        schoolColumnCfgs = data.grid;
        comparePopCfgs = data.customViews;
        if (callback) {
          return callback(schoolColumnCfgs, comparePopCfgs);
        } else {
          return dataArray(schoolColumnCfgs, comparePopCfgs);
        }
      });
    };
    appendColorToData = function(data, asmtSubjectsData, colorsData, defaultColors) {
      var j, k;

      for (k in asmtSubjectsData) {
        j = 0;
        while (j < data.length) {
          data[j]['results'][k].intervals = appendColor(data[j]['results'][k].intervals, colorsData[k], defaultColors);
          j++;
        }
      }
      return data;
    };
    appendColor = function(intervals, colorsData, defaultColors) {
      var element, i, len;

      i = 0;
      len = intervals.length;
      while (i < len) {
        element = intervals[i];
        if (colorsData && colorsData[i]) {
          element.color = colorsData[i];
        } else {
          element.color = defaultColors[i];
        }
        if (element.percentage > 9) {
          element.showPercentage = true;
        } else {
          element.showPercentage = false;
        }
        i++;
      }
      return intervals;
    };
    formatSummaryData = function(summaryData, summaryRowName) {
      var data, k, name;

      data = {};
      summaryData = summaryData[0];
      for (k in summaryData.results) {
        name = 'results.' + k + '.total';
        data[name] = summaryData.results[k].total;
      }
      data['subtitle'] = 'Reference Point';
      data['header'] = true;
      data['results'] = summaryData.results;
      data['name'] = summaryRowName;
      return data;
    };
    getReportTitle = function(breadcrumbsData, reportType) {
      var data;

      if (reportType === 'state') {
        data = addApostropheS(breadcrumbsData.items[0].name) + ' Districts';
      } else if (reportType === 'district') {
        data = addApostropheS(breadcrumbsData.items[1].name) + ' Schools';
      } else if (reportType === 'school') {
        data = addApostropheS(breadcrumbsData.items[2].name) + ' Grades';
      }
      return 'Comparing ' + data + ' on Math & ELA';
    };
    getOverallSummaryName = function(breadcrumbsData, reportType) {
      var data;

      if (reportType === 'state') {
        data = breadcrumbsData.items[0].name + ' District';
      } else if (reportType === 'district') {
        data = breadcrumbsData.items[1].name + ' School';
      } else if (reportType === 'school') {
        data = breadcrumbsData.items[2].name + ' Grade';
      }
      return 'Overall ' + data + ' Summary';
    };
    addApostropheS = function(word) {
      if (word.substr(word.length - 1) === "s") {
        word = word + "'";
      } else {
        word = word + "'s";
      }
      return word;
    };
    getReportType = function(params) {
      var reportType;

      if (params['schoolGuid']) {
        reportType = 'school';
      } else if (params['districtGuid']) {
        reportType = 'district';
      } else if (params['stateCode']) {
        reportType = 'state';
      }
      return reportType;
    };
    return {
      createPopulationGrid: createPopulationGrid
    };
  });

}).call(this);
