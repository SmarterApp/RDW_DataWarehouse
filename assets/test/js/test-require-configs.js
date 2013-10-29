/*globals require */
var baseConfigs = {
  paths : {
    // libraries
    'coffee-script': '../../js/3p/coffee-script',
    jquery: '../../js/3p/jquery-1.7.2.min',
    jqGrid: '../../js/3p/jquery.jqGrid.min',
    sourceJS: '../../js',
    text: '../../js/3p/text',
    mustache: '../../js/3p/mustache',
    templates: '../../js/templates',
    bootstrap: '../../js/3p/bootstrap.min',

    // modules
    EDWARE: '../../js/src/modules/EDWARE',
    edwareUtil: '../../js/src/modules/EDWARE.util',
    edwareDataProxy: '../../js/src/modules/EDWARE.dataProxy',
    'EDWARE.comparingPopulations': '../../js/src/modules/EDWARE.comparingPopulations',
    'EDWARE.studentList': '../../js/src/modules/EDWARE.studentList',
    'EDWARE.individualStudent': '../../js/src/modules/EDWARE.individualStudent',
    edwareFeedback: '../../js/src/modules/EDWARE.feedback',
    edwareConstants: '../../js/src/modules/EDWARE.constants',
    edwarePreferences: '../../js/src/modules/EDWARE.preferences',
    edwareExport: '../../js/src/modules/EDWARE.export',

    // widgets
    edwareGrid: '../../js/src/widgets/grid/EDWARE.grid.tablegrid',
    edwareGridFormatters: '../../js/src/widgets/grid/EDWARE.grid.formatters',
    edwareBreadcrumbs: '../../js/src/widgets/breadcrumb/EDWARE.breadcrumbs',
    edwareHeader: '../../js/src/widgets/header/EDWARE.header',
    edwareConfidenceLevelBar: '../../js/src/widgets/confidenceLevelBar/EDWARE.confidenceBar',
    edwareLOSConfidenceLevelBar: '../../js/src/widgets/losConfidenceLevelBar/EDWARE.losConfidenceBar',
    edwareClaimsBar: '../../js/src/widgets/claimsBar/EDWARE.claimsBar',
    edwarePopulationBar: '../../js/src/widgets/populationBar/EDWARE.populationBar',
    edwareFooter: '../../js/src/widgets/footer/EDWARE.footer',
    edwareLoadingMask: '../../js/src/widgets/loadingMask/EDWARE.loadingMask',
    edwareFilter: '../../js/src/widgets/filter/EDWARE.filter',
    edwareDropdown: '../../js/src/widgets/dropdown/EDWARE.dropdown',
    edwareGridStickyCompare: '../../js/src/widgets/grid/EDWARE.grid.stickyCompare',
    edwareAsmtDropdown: '../../js/src/widgets/asmtDropdown/EDWARE.asmtDropdown',
    edwareGridSorters: '../../js/src/widgets/grid/EDWARE.grid.sorters',
    edwareDisclaimer: '../../js/src/widgets/interimDisclaimer/EDWARE.disclaimer',
    edwareClientStorage: '../../js/src/widgets/clientStorage/EDWARE.clientStorage',
    edwareLegend: '../../js/src/widgets/footer/EDWARE.legend',
    edwareLanguageSelector: '../../js/src/widgets/languageSelector/EDWARE.languageSelector',

    // templates
    edwareBreadcrumbsTemplate: '../../js/src/widgets/breadcrumb/template.html',
    edwareHeaderHtml: '../../js/src/widgets/header/header.html',
    edwareFooterHtml: '../../js/src/widgets/footer/template.html',
    edwareConfidenceLevelBarTemplate: '../../js/src/widgets/confidenceLevelBar/template.html',
    edwareLOSConfidenceLevelBarTemplate: '../../js/src/widgets/losConfidenceLevelBar/template.html',
    edwarePopulationBarTemplate: '../../js/src/widgets/populationBar/template.html',
    edwareClaimsBarTemplate: '../../js/src/widgets/claimsBar/template.html',
    edwareAssessmentDropdownViewSelectionTemplate: '../../js/templates/assessment_dropdown_view_selection.html',
    edwareLOSHeaderConfidenceLevelBarTemplate: '../../js/templates/LOS_header_perf_bar.html',
    edwareFilterTemplate: '../../js/src/widgets/filter/template.html'

  },
  shim: {
    'jqGrid': {
      //These script dependencies should be loaded before loading
      //jqGrid
      deps: ['jquery'],
      exports: 'jqGrid'
    }
  }
};

require.config(baseConfigs);
