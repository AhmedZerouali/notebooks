import pandas as pd
import datetime
import re
import numpy as np
from datetime import datetime




dependencies=pd.read_csv('./Dep_Ver_13M.csv', sep=',', dtype=object, index_col=None)
dependencies.rename(columns = {'Project':'package','Project_Number':'number','Dependency':'dependency','Dependency_Version':'dependency_version'}, inplace=True)
dependencies=dependencies.loc[:,['package','number','dependency','dependency_version']]

#f=open('lag_data.csv','w')
tmp_package=''
with open('./versions_15June17.csv') as lines:
	for index, line in enumerate(lines):
		line=line.strip('\n')
		row=line.split(',')
		package=row[0]
		version=row[1]
		deps=''
		if package != tmp_package:
			tmp=dependencies.query('package=="'+package+'"')
			tmp_package=package
		for dependency in tmp.query('number=="'+version+'"').values:
			entry=dependency[2]+':'+dependency[3]
			deps=deps+entry+','
		#f.write(line+',"'+deps+'"\n')
		print(line+',"'+deps+'"\n')
#f.close()

