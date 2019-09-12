#!/bin/bash

while read alphabet; do

	# mkdir $alphabet
	#rm $alphabet/easy_ones.csv
	#grep ^$alphabet ../lab/icsr2018/easy_one_2.csv > $alphabet/easy_ones_2.csv
	# grep ^$alphabet ../lab/icsr2018/versions_15June17.csv > $alphabet/versions_15June17.csv
	# sed -i '1s/^/package,version,date\n/' $alphabet/versions_15June17.csv
	#cp ../lab/icsr2018/get_right_version.py $alphabet/get_right_version.py

	#cd $alphabet/
	#python3 get_right_version.py &
	#cd ..

	# grep ^$alphabet ../lab/icsr2018/dependencies_versions_15June17.csv > $alphabet/dependencies_versions_15June17.csv
	# grep ^$alphabet ../lab/icsr2018/vers_17.csv > $alphabet/vers_17.csv

	# sed -i '1s/^/Project Name,Version Number,Dependency Name,Dependency Kind,Dependency Requirements,Published Package\n/' $alphabet/dependencies_versions_15June17.csv

	# cp ../lab/icsr2018/get_technical_lag.py $alphabet/get_technical_lag.py

	# cd $alphabet/
	# python3 get_technical_lag.py &
	# cd ..

	cat $alphabet/lag_data.csv >> ../lag_all_data.csv


done<alphabets2