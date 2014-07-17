#!/usr/bin/env bash

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
