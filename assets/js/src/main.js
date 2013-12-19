require({
  // version
  urlArgs: 'v1',
  paths: {
    jquery: '../../3p/jquery-1.7.2.min',
    jqGrid: '../../3p/jquery.jqGrid.min',
    bootstrap: '../../3p/bootstrap.min',
    text: '../../3p/text',
    mustache: '../../3p/mustache',
    moment: '../../3p/moment.min',
    templates: '../../templates',
    edwareUtil: 'EDWARE.util',
    edwareConstants: 'EDWARE.constants',
    edwareDataProxy: 'EDWARE.dataProxy',
    edwareGrid: '../widgets/grid/EDWARE.grid.tablegrid',
    edwareGridFormatters: '../widgets/grid/EDWARE.grid.formatters',
    edwareGridSorters: '../widgets/grid/EDWARE.grid.sorters',
    edwareStudentList: 'EDWARE.studentList',
    edwareIndividualStudent: 'EDWARE.individualStudent',
    edwareComparingPopulations: 'EDWARE.comparingPopulations',
    edwareBreadcrumbs: '../widgets/breadcrumb/EDWARE.breadcrumbs',
    edwareHeader: '../widgets/header/EDWARE.header',
    edwareConfidenceLevelBar: '../widgets/confidenceLevelBar/EDWARE.confidenceBar',
    edwareLOSConfidenceLevelBar: '../widgets/losConfidenceLevelBar/EDWARE.losConfidenceBar',
    edwareClaimsBar: '../widgets/claimsBar/EDWARE.claimsBar',
    edwarePopulationBar: '../widgets/populationBar/EDWARE.populationBar',
    edwareFeedback: 'EDWARE.feedback',
    edwareFooter: '../widgets/footer/EDWARE.footer',
    edwareLegend: '../widgets/footer/EDWARE.legend',
    edwareLoadingMask: '../widgets/loadingMask/EDWARE.loadingMask',
    edwareFilter: '../widgets/filter/EDWARE.filter',
    edwareDropdown: '../widgets/dropdown/EDWARE.dropdown',
    edwareClientStorage: '../widgets/clientStorage/EDWARE.clientStorage',
    edwareLanguageSelector: '../widgets/languageSelector/EDWARE.languageSelector',
    edwareGridStickyCompare: '../widgets/grid/EDWARE.grid.stickyCompare',
    edwareAsmtDropdown: '../widgets/asmtDropdown/EDWARE.asmtDropdown',
    edwarePreferences: 'EDWARE.preferences',
    edwareDisclaimer: '../widgets/interimDisclaimer/EDWARE.disclaimer',
    edwareExport: 'EDWARE.export',
    edwareDownload: '../widgets/download/EDWARE.download',
    edwareReportInfoBar: '../widgets/header/EDWARE.infoBar',
    edwareReportActionBar: '../widgets/header/EDWARE.actionBar',
    edwareHelpMenu: '../widgets/header/EDWARE.helpMenu',
    edwarePrint: '../widgets/print/EDWARE.print',

    // Templates
    edwareBreadcrumbsTemplate: '../widgets/breadcrumb/template.html',
    edwareConfidenceLevelBarTemplate: '../widgets/confidenceLevelBar/template.html',
    edwareLOSConfidenceLevelBarTemplate: '../widgets/losConfidenceLevelBar/template.html',
    edwareLOSHeaderConfidenceLevelBarTemplate: '../../templates/LOS_header_perf_bar.html',
    edwarePopulationBarTemplate: '../widgets/populationBar/template.html',
    edwareClaimsBarTemplate: '../widgets/claimsBar/template.html',
    edwareAssessmentDropdownViewSelectionTemplate: '../../templates/assessment_dropdown_view_selection.html',
    ISRTemplate: '../widgets/footer/ISRTemplate.html',
    CPopTemplate: '../widgets/footer/CPopTemplate.html',
    LOSTemplate: '../widgets/footer/LOSTemplate.html',
    edwareHeaderHtml: '../widgets/header/header.html',
    InfoBarTemplate: '../widgets/header/InfoBarTemplate.html',
    ActionBarTemplate: '../widgets/header/ActionBarTemplate.html',
    edwareFooterHtml: '../widgets/footer/template.html',
    edwareFilterTemplate: '../widgets/filter/template.html',
    edwareDropdownTemplate: '../widgets/dropdown/template.html',
    edwareStickyCompareTemplate: '../widgets/grid/stickyCompare.template.html',
    edwareFormatterTemplate: '../widgets/grid/FormatterTemplate.html',
    CSVOptionsTemplate: '../widgets/download/CSVOptionsTemplate.html',
    DownloadMenuTemplate: '../widgets/download/DownloadMenuTemplate.html',
    AsmtDropdownTemplate: '../widgets/asmtDropdown/template.html',
    PrintTemplate: '../widgets/print/template.html',
    HelpMenuTemplate: '../widgets/header/helpMenuTemplate.html',
    headerTemplateHtml: '../widgets/header/template.html'
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
    }
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
