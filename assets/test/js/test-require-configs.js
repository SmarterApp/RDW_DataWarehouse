/*globals require */
require({
  paths : {
    // libraries
    cs: '3p/cs',
    'coffee-script': '3p/coffee-script',
    jquery: '../../js/3p/jquery-1.7.2.min',
    jqGrid: '../../js/3p/jquery.jqGrid.min',
    moment: '../../js/3p/moment.min',
    sourceJS: '../../js',
    text: '../../js/3p/text',
    mustache: '../../js/3p/mustache',
    templates: '../../js/templates',
    bootstrap: '../../js/3p/bootstrap.min',

    // modules
    EDWARE: '../src/modules/EDWARE',
    edwareUtil: '../src/modules/EDWARE.util',
    edwareDataProxy: '../src/modules/EDWARE.dataProxy',
    'EDWARE.comparingPopulations': '../src/modules/EDWARE.comparingPopulations',
    'EDWARE.studentList': '../src/modules/EDWARE.studentList',
    'EDWARE.individualStudent': '../src/modules/EDWARE.individualStudent',
    edwareFeedback: '../src/modules/EDWARE.feedback',
    edwareConstants: '../src/modules/EDWARE.constants',
    edwarePreferences: '../src/modules/EDWARE.preferences',
    edwareExport: '../src/modules/EDWARE.export',

    // widgets
    edwareGrid: '../src/widgets/grid/EDWARE.grid.tablegrid',
    edwareGridFormatters: '../src/widgets/grid/EDWARE.grid.formatters',
    edwareBreadcrumbs: '../src/widgets/breadcrumb/EDWARE.breadcrumbs',
    edwareHeader: '../src/widgets/header/EDWARE.header',
    edwareConfidenceLevelBar: '../src/widgets/confidenceLevelBar/EDWARE.confidenceBar',
    edwareLOSConfidenceLevelBar: '../src/widgets/losConfidenceLevelBar/EDWARE.losConfidenceBar',
    edwareClaimsBar: '../src/widgets/claimsBar/EDWARE.claimsBar',
    edwarePopulationBar: '../src/widgets/populationBar/EDWARE.populationBar',
    edwareFooter: '../src/widgets/footer/EDWARE.footer',
    edwareLoadingMask: '../src/widgets/loadingMask/EDWARE.loadingMask',
    edwareFilter: '../src/widgets/filter/EDWARE.filter',
    edwareDropdown: '../src/widgets/dropdown/EDWARE.dropdown',
    edwareGridStickyCompare: '../src/widgets/grid/EDWARE.grid.stickyCompare',
    edwareAsmtDropdown: '../src/widgets/asmtDropdown/EDWARE.asmtDropdown',
    edwareGridSorters: '../src/widgets/grid/EDWARE.grid.sorters',
    edwareDisclaimer: '../src/widgets/interimDisclaimer/EDWARE.disclaimer',
    edwareClientStorage: '../src/widgets/clientStorage/EDWARE.clientStorage',
    edwareLegend: '../src/widgets/footer/EDWARE.legend',
    edwareLanguageSelector: '../src/widgets/languageSelector/EDWARE.languageSelector',
    edwareDownload: '../src/widgets/download/EDWARE.download',
    edwareReportInfoBar: '../src/widgets/header/EDWARE.infoBar',
    edwareReportActionBar: '../src/widgets/header/EDWARE.actionBar',
    edwareHelpMenu: '../src/widgets/header/EDWARE.helpMenu',
    edwarePrint: '../src/widgets/print/EDWARE.print',

    // templates
    edwareBreadcrumbsTemplate: '../src/widgets/breadcrumb/template.html',
    edwareHeaderHtml: '../src/widgets/header/header.html',
    InfoBarTemplate: '../src/widgets/header/InfoBarTemplate.html',
    ActionBarTemplate: '../src/widgets/header/ActionBarTemplate.html',
    edwareFooterHtml: '../src/widgets/footer/template.html',
    edwareConfidenceLevelBarTemplate: '../src/widgets/confidenceLevelBar/template.html',
    edwareLOSConfidenceLevelBarTemplate: '../src/widgets/losConfidenceLevelBar/template.html',
    edwarePopulationBarTemplate: '../src/widgets/populationBar/template.html',
    edwareClaimsBarTemplate: '../src/widgets/claimsBar/template.html',
    edwareAssessmentDropdownViewSelectionTemplate: '../js/templates/assessment_dropdown_view_selection.html',
    edwareLOSHeaderConfidenceLevelBarTemplate: '../js/templates/LOS_header_perf_bar.html',
    edwareFilterTemplate: '../src/widgets/filter/template.html',
    CSVOptionsTemplate: '../src/widgets/download/CSVOptionsTemplate.html',
    DownloadMenuTemplate: '../src/widgets/download/DownloadMenuTemplate.html',
    AsmtDropdownTemplate: '../src/widgets/asmtDropdown/template.html',
    PrintTemplate: '../src/widgets/print/template.html',
    HelpMenuTemplate: '../src/widgets/header/helpMenuTemplate.html',
    ActionBarTemplate: '../src/widgets/header/ActionBarTemplate.html',
    headerTemplateHtml: '../src/widgets/header/template.html'
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
}, ['cs!test.EDWARE']);
