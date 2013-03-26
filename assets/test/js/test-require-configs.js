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
		
	    EDWARE: '../../js/EDWARE',
	    edwareUtil: '../../js/EDWARE.util',
	    edwareDataProxy: '../../js/EDWARE.dataProxy',
	    edwareGrid: '../../js/widgets/grid/EDWARE.grid.tablegrid',
	    edwareGridFormatters: '../../js/widgets/grid/EDWARE.grid.formatters',
	    edwareStudentList: '../../js/EDWARE.studentList',
	    edwareIndividualStudent: '../../js/EDWARE.individualStudent',
	    edwareBreadcrumbs: '../../js/widgets/breadcrumb/EDWARE.breadcrumbs',
		edwareConfidenceLevelBar: '../../js/widgets/confidenceLevelBar/EDWARE.confidenceBar',
		edwarePopulationBar: '../../js/widgets/populationBar/EDWARE.populationBar',
		edwareComparingPopulations: '../../js/EDWARE.comparingPopulations',
		edwareFeedback: '../../js/EDWARE.feedback',
	    
	    edwareBreadcrumbsTemplate: '../../js/widgets/breadcrumb/template.html',
		edwareConfidenceLevelBarTemplate: '../../js/widgets/confidenceLevelBar/template.html',
		edwarePopulationBarTemplate: '../../js/widgets/populationBar/template.html',
		edwareAssessmentDropdownViewSelectionTemplate: '../../js/templates/assessment_dropdown_view_selection.html'
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