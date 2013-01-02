Smarter Balanced Project
========================

Here is to store Smarter Balanced Project code. 

I (Eugene Jen) think this one is where web front end and application should be stored. Since we want to build a platform
that can be reused by other project. So it seems like client specific product is the web.

But we may need to move platform related code to other part in repository if we want them to be reused.
/lib is for that. But I need to think how do we deal with Framework or other resuable code in system. 

Let's deal the problem when we meet it.

***

(updated by Eugene Jen on Jan 2nd, 2013, please contact ejen@wgen.net for any error) 

to run the project without virtualenv,

1. make sure you have pyramid installed and all dependency.
2. check out the code.
3. cd to smarter directory
4. run "python3 setup.py develop" on OS X or "python.exe setup.py develop" on your windows box.
   setup will patch up all missed depency with latest python packages
5. pserve development.ini to run the server
6. set up your Aptana by Import -> Select -> Existing Projects into Workspace 
7. Select root directory to be where you check out the code plus under "edware/smarter"
   You should see tthe projects files smarter
8. I don't think you need to copy projects into workspace. Also we need to see how do we do this when
   we start git branch. For the moment. just copy. And I will check how working sets works in Aptana. Or 
   You can inform me for you experience so I play around working sets.
9. Click finish to import project
10. Please open the project properties to make sure PyDev -- Interpreter/Grammar are set to 3.0, and interpreter is
    set to your python3 interpreter for the moment. When we start to use virtualenv to lockd down python. We will move
    to use the virtualenv python. This set up is project based, so your python setting is only effective in current project.
11. [To be verified] I need to test how the python path works inside pyramid. otherwise we will need to add /edware/lib into
    PyDev's PYTHONPATH to make common library code in project searchable for Python interpreters.
12. [To be verified] I need to check how do we integrated coffeescript.
13. In Aptana's PyDev - PYTHONPATH, in "string subsitution variables" add variable "pyramid_run" to be the pserve in your system (on windows, it will be pserve-python.py).
    (please refer the document here in wiki, <https://confluence.wgenhq.net/display/CS/Installation+of+Python+3%2C+related+packages%2C+Pyramid+and+Edware+Developer+Environment>, this is pyramid specific to enable Apatan Pyramid IDE integration, if you can do everything with EDITOR and command line, you can skip those steps)
14. In project's runtime configuration in Apatan, create a new runtime conf like smarter, then make sure project smarter is selected wth main module being set as "${pyramid_run}" and Arguments to be "development.ini" to run dev version from inside Aptana.
15. [to be continued] I need to make sure unit test configuratio works. Currently this is broken under Apatan.
 
Please notify Eugene for any error in this document.

***


