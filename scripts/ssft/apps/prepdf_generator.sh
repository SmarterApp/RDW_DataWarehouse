#!/bin/bash

__run(){
    cd "$EDWARE_WORKSPACE"
    echo  "
import time
from pyramid.paster import get_app, setup_logging
from smarter.trigger.pre_pdf_generator import *
app = get_app('$EDWARE_INI_HOME/$EDWARE_INI_SMARTER')
time.sleep(20)
setup_logging('$EDWARE_INI_HOME/$EDWARE_INI_SMARTER')
settings = app.registry._settings
results = prepdf_task(settings)
" > pre-pdf.py
    python3.3 pre-pdf.py >> "$EDWARE_LOG_PREPDF" 2>&1
    rm pre-pdf.py
}
