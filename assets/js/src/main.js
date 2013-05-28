require({
	paths: {
		'jquery.min' : '../../3p/jquery-1.7.2.min',
		jquery: '../../3p/jquery-loader',
		jqGrid: '../../3p/jquery.jqGrid.min',
		bootstrap: '../../3p/bootstrap.min',
		text: '../../3p/text',
		mustache: '../../3p/mustache',
		templates: '../../templates',
		edwareUtil: 'EDWARE.util',
		edwareDataProxy: 'EDWARE.dataProxy',
		edwareGrid: '../widgets/grid/EDWARE.grid.tablegrid',
		edwareGridFormatters: '../widgets/grid/EDWARE.grid.formatters',
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
		edwareLoadingMask: '../widgets/loadingMask/EDWARE.loadingMask',
		
		// Templates
		edwareBreadcrumbsTemplate: '../widgets/breadcrumb/template.html',
		edwareConfidenceLevelBarTemplate: '../widgets/confidenceLevelBar/template.html',
		edwareLOSConfidenceLevelBarTemplate: '../widgets/losConfidenceLevelBar/template.html',
		edwareLOSHeaderConfidenceLevelBarTemplate: '../../templates/LOS_header_perf_bar.html',
		edwarePopulationBarTemplate: '../widgets/populationBar/template.html',
		edwareClaimsBarTemplate: '../widgets/claimsBar/template.html',
		edwareAssessmentDropdownViewSelectionTemplate: '../../templates/assessment_dropdown_view_selection.html',
		edwareHeaderHtml: '../widgets/header/header.html',
		edwareFooterHtml: '../widgets/footer/template.html',
		edwareFeedbackHTML: '../../templates/feedback/feedback.html'
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