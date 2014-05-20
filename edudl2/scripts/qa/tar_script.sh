#! /bin/bash
cd <dir path to files to be tar and gpg>
mkdir tar_dir
cp *.json tar_dir
cp *.csv tar_dir
cd tar_dir
IFS=$'\n'
for file in `ls *`
do
    d=`echo $file | tr " " _`
    mv "$file" $d
    echo $d
done
for filename in `ls *.json`
do
	echo ${filename#*COMPREHENSIVE_}
	substr=${filename#*COMPREHENSIVE_}
	final_substr=${substr%.*}
	echo $final_substr
	for csv_file in `ls *.csv`
	do
		if [[ $csv_file =~ $final_substr ]];then echo $csv_file;
			csv=${csv_file%.*}
			echo $csv
			tar -cvzf $csv.tar.gz --disable-copyfile $csv_file $filename
			echo sbac udl2 | gpg --armor --local-user ca_user@ca.com --recipient sbac_data_provider@sbac.com --encrypt --passphrase-fd 0 --sign $csv.tar.gz
			mv $csv.tar.gz.asc $csv.tar.gz.gpg
		fi
	done
done


	
	