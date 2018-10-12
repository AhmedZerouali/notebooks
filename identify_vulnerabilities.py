################# IDENTIFY VULNERABIITIES #################

import pandas as pd
import json as js
import codecs
import apt_pkg
apt_pkg.init_system()

# These are packages installed in debian:stretch
packages=pd.read_csv('./data/stertch_packages.csv', index_col=None, sep=';') 


def parse_json_vuls():
    # download it from https://security-tracker.debian.org/tracker/data/json
    vulnerabilities=js.load(codecs.open('data/vuls_15April.json', 'r', 'utf-8'))
    return vulnerabilities

def final_vuls(tracked_packages):
    
    vulnerabilities=parse_json_vuls()    
    
    columns=['source','source_version','urgency','status','fixed_version','debianbug','release','cve']
    df=pd.DataFrame(columns=columns)
    
    sorted_packages=packages[['source','source_version','release_snapshot']].drop_duplicates()
    
    for index, raw in enumerate(sorted_packages.iterrows()): ######## iterate over the sources (docker)
        source=raw[1]['source']
        source_version=raw[1]['source_version']
        release=raw[1]['release_snapshot']
        try:
            vuls=vulnerabilities[source] ###### check if the source has any vulnerabilities
        except:
            continue
        for cve in vuls:  ###### for each vulnerability
            if not cve.startswith('CVE'):
                continue
            v=vulnerabilities[source][cve]
            try:
                status=v['releases'][release]['status']  ###### check only the release of source
                urgency=v['releases'][release]['urgency'] ###### check only the release of source
                
                try:
                    debianbug=str(v['debianbug'])
                except:
                    debianbug="undefined"
                    
                if status == "open" or status=="undetermined": ###### if the vulnerability is still OPEN
                    fixed="undefined"
                    vul=[source,source_version,urgency,status,fixed,debianbug,release,cve]
                    df.loc[len(df)] = vul
                else: ###### if the vulnerability is RESOLVED
                    fixed=v['releases'][release]["fixed_version"]
                    if apt_pkg.version_compare(source_version,fixed) < 0: #### Compare between the used source and fixed one (dates comparison)
                        vul=[source,source_version,urgency,status,fixed,debianbug,release,cve]
                        df.loc[len(df)] = vul
            except:
                pass
    return df

#### MERGE FOUND VULNERABILITIES WITH INSTALLED PACKAGES
def merge_vuls(packages):
    vuls=final_vuls(packages)            ### GET VULNERABILITIES
    # Here we merge vulnerabilities with community outdated packages
    docker_vuls=(
        packages.
        set_index(['source','source_version'])
        [['date','package','version']].
        merge(vuls.
              set_index(['source','source_version']),
              left_index=True, 
              right_index=True, 
              how='left').dropna().reset_index().drop_duplicates()
    )
    return docker_vuls


docker_vulnerabilities=merge_vuls(packages)
print(docker_vulnerabilities.head())