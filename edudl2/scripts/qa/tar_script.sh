#! /bin/bash
# get work dir from shell argument list or default value
if [ -n "$1" ]
then
    work_dir=$1
else
    work_dir=~/Downloads/test/
fi

# exit if work_dir doesn't exist
echo "work dir is " $work_dir
if [[ ! -d $work_dir ]]; then
   echo "please specify working directory because $work_dir doesn't exist"
   exit 1
fi

cd $work_dir
asmt_types=(COMPREHENSIVE_ SUMMATIVE_) # separate by " "
mkdir tar_dir
cp *.json tar_dir
cp *.csv tar_dir
cd tar_dir
IFS=$'\n'

####
# list all csv and json files and normalized file name to use '_' instead of ' '
####

for file in `ls *.csv *.json`
do
    normalized_file_name=`echo $file | tr " " _`
    mv "$file" $normalized_file_name
    echo "replace file name to " $normalized_file_name
done

##
# loop through all json, find related csv, tar and gpg them for landig zone format
#
##
for asmt_type in ${asmt_types[*]}
    do
    # find all json file
    for json_file in `ls *${asmt_type}*.json`
    do
        echo "json file for ${asmt_type}: " ${json_file}
        json_grade=`echo ${json_file}|cut -d _ -f 6`
        echo "json_grade" $json_grade
        echo "guid with extension " ${json_file#*${asmt_type}}
        substr=${json_file#*${asmt_type}}
        guid=${substr%.*}
        echo "guid " $guid
        for csv_file in `ls *${asmt_type}*.csv`
        do
            csv_grade=`echo ${csv_file}|cut -d _ -f 5`
            echo "csv grade " $csv_grade
            if [[ $csv_file =~ $guid ]] && [[ $csv_grade == $json_grade ]] ;then
                echo "csv file" $csv_file;
                csv=${csv_file%.*}
                echo "csv " $csv
                tar -cvzf $csv.tar.gz --disable-copyfile $csv_file $json_file
                echo sbac udl2 | gpg --armor --local-user ca_user@ca.com --recipient sbac_data_provider@sbac.com --encrypt --passphrase-fd 0 --sign $csv.tar.gz
                mv $csv.tar.gz.asc $csv.tar.gz.gpg
            fi
        done
    done
done
mkdir gz_dir
mkdir gpg_dir
cp *.gz gz_dir
cp *.gpg gpg_dir

