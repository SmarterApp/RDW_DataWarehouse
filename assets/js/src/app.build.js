({
  appDir: ".",
  baseUrl: ".",
  dir : "build",
  preserveLicenseComments: true,
  optimize: 'uglify',
  modules: [
    {
      name : "modules/EDWARE.comparingPopulationsReport"
    },
    {
      name : "modules/EDWARE.individualStudentReport"
    },
    {
      name : "modules/EDWARE.studentListReport"
    },
    {
      name: "modules/EDWARE.stateMap"
    }]
})
