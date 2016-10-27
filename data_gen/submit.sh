#!/usr/bin/env bash
#
# Script to prepare the output files for submission.
# By pairs, it tars them, encrypts them and sftps them

cd out

for csv in *.csv; do
    base="${csv%.*}"
    if [ ! -f "$base.json" ]; then
        echo "skipping unpaired file $csv"
    else
        tarfile="../prepared/$base.tar.gz"
        gpgfile="$tarfile.gpg"
        tar czf "$tarfile" "$base.csv" "$base.json"
        gpg --homedir ../../config/gpg --no-permission-warning -q -e -r sbac_data_provider@sbac.com -o "$gpgfile" "$tarfile"
        echo "submitting $gpgfile"
        ../submit.exp "$gpgfile"
        rm "$tarfile"
        sleep 2
    fi
done

cd ..
