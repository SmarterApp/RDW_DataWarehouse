#!/bin/bash --
#xform_type_bool.sh
#takes a minute...
grep -rl '|t|' ./ | xargs sed -i 's/|t|/|1|/g'
grep -rl '|f|' ./ | xargs sed -i 's/|f|/|0|/g'
