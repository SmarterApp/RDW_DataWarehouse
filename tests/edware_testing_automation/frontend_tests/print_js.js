/*
(c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
below.

Education agencies that are members of the Smarter Balanced Assessment
Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
display, distribute, perform and create derivative works of the software
included in the Reporting Platform, including the source code to such software.
This license includes the right to grant sublicenses by such consortium members
to third party vendors solely for the purpose of performing services on behalf
of such consortium member educational agencies.

*/

(function pretendToBeAPrinter() {
    //For looking up if something is in the media list
    function hasMedia(list, media) {
        if (!list) return false;

        var i = list.length;
        while (i--) {
            if (list[i] === media) {
                return true;
            }
        }
        return false;
    }

    //Loop though all stylesheets
    for (var styleSheetNo = 0; styleSheetNo < document.styleSheets.length; styleSheetNo++) {
        //Current stylesheet
        var styleSheet = document.styleSheets[styleSheetNo];

        //Output debug information
        console.info("Stylesheet #" + styleSheetNo + ":");
        console.log(styleSheet);

        //First, check if any media queries have been defined on the <style> / <link> tag

        //Disable screen-only sheets
        if (hasMedia(styleSheet.media, "screen") && !hasMedia(styleSheet.media, "print")) {
            styleSheet.disabled = true;
        }

        //Display "print" stylesheets
        if (!hasMedia(styleSheet.media, "screen") && hasMedia(styleSheet.media, "print")) {
            //Add "screen" media to show on screen
            styleSheet.media.appendMedium("screen");
        }

        //Get the CSS rules in a cross-browser compatible way
        var rules = styleSheet.rules || styleSheet.cssRules;

        //Handle cases where styleSheet.rules is null
        if (!rules) {
            continue;
        }

        //Second, loop through all the rules in a stylesheet
        for (var ruleNo = 0; ruleNo < rules.length; ruleNo++) {
            //Current rule
            var rule = rules[ruleNo];

            //Hide screen-only rules
            if (hasMedia(rule.media, "screen") && !hasMedia(rule.media, "print")) {
                //Rule.disabled doesn't work here, so we remove the "screen" rule and add the "print" rule so it isn't shown
                console.info('Rule.media:');
                console.log(rule.media);
                rule.media.appendMedium(':not(screen)');
                rule.media.deleteMedium('screen');
                console.info('Rule.media after tampering:');
                console.log(rule.media)
            }

            //Display "print" rules
            if (!hasMedia(rule.media, "screen") && hasMedia(rule.media, "print")) {
                //Add "screen" media to show on screen
                rule.media.appendMedium("screen");
            }
        }
    }
})();
window.onbeforeprint();
