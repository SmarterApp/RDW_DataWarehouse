/*globals require */
var baseConfigs = {
	paths : {	
	    cs: '../../js/3p/cs',
	    'coffee-script': '../../js/3p/coffee-script',
	    jquery: '../../js/3p/jquery-1.7.2.min',
	    jqGrid: '../../js/3p/jquery.jqGrid.min',
	    sourceJS: '../../js',
	    text: '../../js/3p/text',
		mustache: '../../js/3p/mustache',
		templates: '../../js/templates',
		bootstrap: '../../js/3p/bootstrap.min',
		
	    EDWARE: '../../js/src/modules/EDWARE',
	    edwareUtil: '../../js/src/modules/EDWARE.util',
	    edwareDataProxy: '../../js/src/modules/EDWARE.dataProxy',
	    edwareGrid: '../../js/src/widgets/grid/EDWARE.grid.tablegrid',
	    edwareGridFormatters: '../../js/src/widgets/grid/EDWARE.grid.formatters',
	    edwareStudentList: '../../js/src/modules/EDWARE.studentList',
	    edwareIndividualStudent: '../../js/src/modules/EDWARE.individualStudent',
	    edwareBreadcrumbs: '../../js/src/widgets/breadcrumb/EDWARE.breadcrumbs',
	    edwareHeader: '../../js/src/widgets/header/EDWARE.header',
		edwareConfidenceLevelBar: '../../js/src/widgets/confidenceLevelBar/EDWARE.confidenceBar',
		edwareLOSConfidenceLevelBar: '../../js/src/widgets/losConfidenceLevelBar/EDWARE.losConfidenceBar',
		edwarePopulationBar: '../../js/src/widgets/populationBar/EDWARE.populationBar',
		edwareComparingPopulations: '../../js/src/modules/EDWARE.comparingPopulations',
		edwareFeedback: '../../js/src/modules/EDWARE.feedback',
		edwareFooter: '../../js/src/widgets/footer/EDWARE.footer',
	    
	    edwareBreadcrumbsTemplate: '../../js/src/widgets/breadcrumb/template.html',
	    edwareHeaderHtml: '../../js/src/widgets/header/header.html',
	    edwareFooterHtml: '../../js/src/widgets/footer/template.html',
		edwareConfidenceLevelBarTemplate: '../../js/src/widgets/confidenceLevelBar/template.html',
		edwareLOSConfidenceLevelBarTemplate: '../../js/src/widgets/losConfidenceLevelBar/template.html',
		edwarePopulationBarTemplate: '../../js/src/widgets/populationBar/template.html',
		edwareAssessmentDropdownViewSelectionTemplate: '../../js/templates/assessment_dropdown_view_selection.html',
		edwareLOSHeaderConfidenceLevelBarTemplate: '../../js/templates/LOS_header_perf_bar.html'
		
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

function getTestFile() {
	var scriptTags = document.getElementsByTagName("script"), i, testfile = [], fileName;

	for( i = 0; i < scriptTags.length; i++) {
		fileName = scriptTags[i].getAttribute("data-testfile");
		if(fileName) {
			testfile.push(fileName);
		}
	}

	return testfile;
}

require(getTestFile());