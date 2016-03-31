#!/usr/bin/env bash
# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.


if [ -z $1 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

# utility script to tar and encrypt test files
for filename in $(ls $1/*.csv); do
    f="${filename%.*}"
    dir=$(dirname $f)
    base=$(basename $f)
    tar -czf "${f}.tar.gz" -C $dir --disable-copyfile "${base}.csv" "${base}.json" 2>&1 1>/dev/null
    echo "successfully compressed file $f"
    # Bellow cmd will ask for passphrase, enter: sbac udl2
    # TODO: need to do some validation of generated tar files
    gpg --armor --local-user ca_user@ca.com --recipient sbac_data_provider@sbac.com --encrypt --sign --passphrase "sbac udl2" ${f}.tar.gz
done

for ascname in $(ls $1/*.asc); do
    mv $ascname "${ascname%.*}.gpg"
done
