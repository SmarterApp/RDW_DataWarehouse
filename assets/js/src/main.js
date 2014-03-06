require({
  // version
  urlArgs: 'v1',
  baseUrl: '../js/src/',
  paths: {
    // globals
    jquery: '../3p/jquery-1.7.2.min',
    jqGrid: '../3p/jquery.jqGrid.min',
    bootstrap: '../3p/bootstrap.min',
    text: '../3p/text',
    mustache: '../3p/mustache',
    moment: '../3p/moment.min',
    templates: '../templates',
    usmap: '../3p/usmap/jquery.usmap',
    raphael: '../3p/usmap/raphael',

    // modules
    'Edware.LandingPage': 'modules/Edware.LandingPage',
    'Edware.ComparingPopulationsReport': 'modules/Edware.comparingPopulationsReport',
    'Edware.StudentListReport': 'modules/Edware.studentListReport',
    'Edware.IndividualStudentReport': 'modules/Edware.individualStudentReport',
    'Edware.StateMap': 'modules/Edware.stateMap',

    edwareUtil: 'modules/EDWARE.util',
    edwareConstants: 'modules/EDWARE.constants',
    edwareDataProxy: 'modules/EDWARE.dataProxy',
    edwareGrid: 'widgets/grid/EDWARE.grid.tablegrid',
    edwareGridFormatters: 'widgets/grid/EDWARE.grid.formatters',
    edwareStudentList: 'modules/EDWARE.studentList',
    edwareIndividualStudent: 'modules/EDWARE.individualStudent',
    edwareComparingPopulations: 'modules/EDWARE.comparingPopulations',
    edwareBreadcrumbs: 'widgets/breadcrumb/EDWARE.breadcrumbs',
    edwareHeader: 'widgets/header/EDWARE.header',
    edwareConfidenceLevelBar: 'widgets/confidenceLevelBar/EDWARE.confidenceBar',
    edwareLOSConfidenceLevelBar: 'widgets/losConfidenceLevelBar/EDWARE.losConfidenceBar',
    edwareClaimsBar: 'widgets/claimsBar/EDWARE.claimsBar',
    edwarePopulationBar: 'widgets/populationBar/EDWARE.populationBar',
    edwareFeedback: 'modules/EDWARE.feedback',
    edwareLegend: 'widgets/legend/EDWARE.legend',
    edwareLoadingMask: 'widgets/loadingMask/EDWARE.loadingMask',
    edwareFilter: 'widgets/filter/EDWARE.filter',
    edwareClientStorage: 'widgets/clientStorage/EDWARE.clientStorage',
    edwareLanguageSelector: 'widgets/languageSelector/EDWARE.languageSelector',
    edwareGridStickyCompare: 'widgets/grid/EDWARE.grid.stickyCompare',
    edwareAsmtDropdown: 'widgets/asmtDropdown/EDWARE.asmtDropdown',
    edwarePreferences: 'modules/EDWARE.preferences',
    edwareDisclaimer: 'widgets/interimDisclaimer/EDWARE.disclaimer',
    edwareExport: 'modules/EDWARE.export',
    edwareDownload: 'widgets/download/EDWARE.download',
    edwareReportInfoBar: 'widgets/header/EDWARE.infoBar',
    edwareReportActionBar: 'widgets/header/EDWARE.actionBar',
    edwareHelpMenu: 'widgets/header/EDWARE.helpMenu',
    edwarePrint: 'widgets/print/EDWARE.print',
    edwareRedirect: 'modules/EDWARE.stateViewRedirect',
    edwarePopover: 'widgets/popover/EDWARE.popover',

    // widgets

    // templates
    edwareBreadcrumbsTemplate: 'widgets/breadcrumb/template.html',
    edwareConfidenceLevelBarTemplate: 'widgets/confidenceLevelBar/template.html',
    edwareLOSConfidenceLevelBarTemplate: 'widgets/losConfidenceLevelBar/template.html',
    edwareLOSHeaderConfidenceLevelBarTemplate: '../templates/LOS_header_perf_bar.html',
    edwarePopulationBarTemplate: 'widgets/populationBar/template.html',
    edwareClaimsBarTemplate: 'widgets/claimsBar/template.html',
    edwareAssessmentDropdownViewSelectionTemplate: '../templates/assessment_dropdown_view_selection.html',
    ISRTemplate: 'widgets/legend/ISRTemplate.html',
    CPopTemplate: 'widgets/legend/CPopTemplate.html',
    LOSTemplate: 'widgets/legend/LOSTemplate.html',
    edwareHeaderHtml: 'widgets/header/header.html',
    InfoBarTemplate: 'widgets/header/InfoBarTemplate.html',
    ActionBarTemplate: 'widgets/header/ActionBarTemplate.html',
    edwareFilterTemplate: 'widgets/filter/template.html',
    edwareDropdownTemplate: 'widgets/dropdown/template.html',
    edwareStickyCompareTemplate: 'widgets/grid/stickyCompare.template.html',
    edwareFormatterTemplate: 'widgets/grid/FormatterTemplate.html',
    CSVOptionsTemplate: 'widgets/download/CSVOptionsTemplate.html',
    DownloadMenuTemplate: 'widgets/download/DownloadMenuTemplate.html',
    AsmtDropdownTemplate: 'widgets/asmtDropdown/template.html',
    PrintTemplate: 'widgets/print/template.html',
    HelpMenuTemplate: 'widgets/header/helpMenuTemplate.html',
    headerTemplateHtml: 'widgets/header/template.html'
  },
  shim: {
    'jqGrid': {
      //These script dependencies should be loaded before loading
      //jqGrid
      deps: ['jquery'],
      exports: 'jqGrid'
    },
    'bootstrap': {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    'usmap': {
      deps: ['jquery', 'raphael'],
      exports: 'usmap'
    },
  }
});

(function(){
  //setup google analytics
  (function(i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] ||
      function() {
	(i[r].q = i[r].q || []).push(arguments)
      }, i[r].l = 1 * new Date();
    a = s.createElement(o), m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
  })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

  ga('create', 'UA-43067000-1', 'edwdc.net');
  ga('send', 'pageview', {
    'page':  window.location.pathname,
    'location': window.location.protocol + "://" + window.location.host + window.location.pathname,
    'title': document.title});
}).call(this);
