(function() {
  define(["jquery", "bootstrap", "mustache", "edwareDataProxy", "edwareConfidenceLevelBar", "text!templates/individualStudent_report/individual_student_template.html", "text!templates/individualStudent_report/claimsInfo.html", "edwareBreadcrumbs", "edwareUtil", "edwareFeedback", "edwareHeader"], function($, bootstrap, Mustache, edwareDataProxy, edwareConfidenceLevelBar, indivStudentReportTemplate, claimsInfoTemplate, edwareBreadcrumbs, edwareUtil, edwareFeedback, edwareHeader) {
    var claimScoreWeightArray, generateIndividualStudentReport, getContent;

    claimScoreWeightArray = {
      "MATH": ["40", "40", "20", "10"],
      "ELA": ["40", "30", "20", "10"]
    };
    generateIndividualStudentReport = function(params) {
      var content, options;

      content = {};
      getContent("../data/content.json", function(tempContent) {
        return content = tempContent;
      });
      options = {
        async: true,
        method: "POST",
        params: params
      };
      return edwareDataProxy.getDatafromSource("/data/individual_student_report", options, function(data) {
        var defaultColors;

        $("#legend").popover({
          html: true,
          placement: "top",
          container: "div",
          title: function() {
            return '<div class="pull-right"><button class="btn" id="close" type="button" onclick="$(&quot;#legend&quot;).popover(&quot;hide&quot;);">Hide</button></div><div class="lead">Legends</div>';
          },
          template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>',
          content: function() {
            return $(".legendPopup").html();
          }
        });
        $("#aboutReport").popover({
          html: true,
          placement: "top",
          container: "div",
          title: function() {
            return '<div class="pull-right"><button class="btn" id="close" type="button" onclick="$(&quot;#aboutReport&quot;).popover(&quot;hide&quot;);">Hide</button></div><div class="lead">About Report</div>';
          },
          template: '<div class="popover footerPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>',
          content: function() {
            return $(".aboutReportPopup").html();
          }
        });
        defaultColors = {};
        options = {
          async: false,
          method: "GET"
        };
        return edwareDataProxy.getDatafromSource("../data/color.json", options, function(defaultColors) {
          var barContainer, claim, contextData, grade, grade_asmt, i, item, items, j, output, partials, performance_level, role, uid;

          i = 0;
          while (i < data.items.length) {
            items = data.items[i];
            j = 0;
            while (j < items.cut_point_intervals.length) {
              if (!items.cut_point_intervals[j].bg_color) {
                $.extend(items.cut_point_intervals[j], defaultColors[j]);
              }
              j++;
            }
            items.count = i;
            items.content = content.content;
            performance_level = items.cut_point_intervals[items.asmt_perf_lvl - 1];
            items.score_color = performance_level.bg_color;
            items.score_text_color = performance_level.text_color;
            items.score_bg_color = performance_level.bg_color;
            items.score_name = performance_level.name;
            items.overall_ald = content.overall_ald[items.asmt_subject][items.asmt_perf_lvl];
            output = Mustache.render(content.psychometric_implications[items.asmt_subject], items);
            items.psychometric_implications = output;
            grade = content.policy_content[items.grade];
            if (items.grade === "11") {
              items.policy_content = grade[items.asmt_subject];
            } else if (items.grade === "3") {
              grade_asmt = grade[items.asmt_subject];
              items.policy_content = grade_asmt[items.asmt_perf_lvl];
            }
            if (items.claims.length < 4) {
              items.claim_box_width = "28%";
            }
            if (items.claims.length === 4) {
              items.claim_box_width = "20%";
            }
            j = 0;
            while (j < items.claims.length) {
              claim = items.claims[j];
              claim.assessmentUC = items.asmt_subject.toUpperCase();
              claim.claim_score_weight = claimScoreWeightArray[claim.assessmentUC][j];
              claim.desc = content.claims[items.asmt_subject][claim.indexer];
              j++;
            }
            i++;
          }
          contextData = data.context;
          $('#header').header();
          $('#breadcrumb').breadcrumbs(contextData);
          partials = {
            claimsInfo: claimsInfoTemplate
          };
          output = Mustache.to_html(indivStudentReportTemplate, data, partials);
          $("#individualStudentContent").html(output);
          i = 0;
          while (i < data.items.length) {
            item = data.items[i];
            barContainer = "#assessmentSection" + i + " .confidenceLevel";
            edwareConfidenceLevelBar.create(item, 640, barContainer);
            i++;
          }
          if (data.user_info) {
            $('#header .topLinks .user').html(edwareUtil.getUserName(data.user_info));
            role = edwareUtil.getRole(data.user_info);
            uid = edwareUtil.getUid(data.user_info);
            return edwareFeedback.renderFeedback(role, uid, "individual_student_report");
          }
        });
      });
    };
    getContent = function(configURL, callback) {
      var content, options;

      content = {};
      if (configURL === "undefined" || typeof configURL === "number" || typeof configURL === "function" || typeof configURL === "object") {
        return false;
      }
      options = {
        async: false,
        method: "GET"
      };
      return edwareDataProxy.getDatafromSource(configURL, options, function(data) {
        content = data;
        if (callback) {
          return callback(content);
        } else {
          return content;
        }
      });
    };
    return {
      generateIndividualStudentReport: generateIndividualStudentReport
    };
  });

}).call(this);
