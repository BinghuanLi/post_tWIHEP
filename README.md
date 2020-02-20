post tWIHEPFrameworks scripts
==================================

Introduction
------------------------
1. This repo contains scripts making rootplas, create datacards and run combine fit
2. This repo contains a lot of hardcoding scripts, each task requires hardcode works to create htcondor jobs 

Setting up the code 
------------------------
Downloading the project from github
```bash
git clone git@github.com:BinghuanLi/post_tWIHEP.git
```

IHEP use htcondor job management system. IHEP implemented a toolkit HepJob, which helps users to manage their jobs. There are customizations in HepJob for the IHEP cluster. We should use HepJob instead of the native HTCondor commands unless there are some specific requirements. This [guide][user_guide] introduce you the IHEP computing system including job management systems.

Setting up the HEP environment
```
export PATH=$PATH:/afs/ihep.ac.cn/soft/common/sysgroup/hep_job/bin/
```
[user_guide]:http://afsapply.ihep.ac.cn/cchelp/en/local-cluster/jobs/HTCondor/

CombineTool and Harvester are used to perform statistics analysis. Please following the link [here][combine] and [here][harvester] to set up this two packages. Please install them on lxslc7 under CMSSW_10_2_X.

[combine]:[http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#introduction]
[harvester]:[http://cms-analysis.github.io/CombineHarvester/index.html#getting-started]


rootplJobs
-------------------------

Scripts in directory "rootplJobs" are used to create rootplas. It takes the output of tWIHEPFramework as input.
1. Current Working Directory is BaseDir, please copy rootplJobs/Datacard/*.py to BaseDir
2. makeHEPSubmit.py is the script to create HEP jobs at IHEP, change frameworkDir, inputBaseDir, outputBaseDir, executable of this script so the job will run frameworkDir/executable
3. ` python makeHEPSubmit.py` will create a script all.sh,
     `bash all.sh` to submit all jobs, after all jobs finishes, `python resubmitJobs.py` to check failed job, if any job failed, run `bash allMissingFiles.sh`,
     after this, run `python mergeCheck.py` to remove unnecessary files,
     finally, submit job script allSkim.sh, this will run script skimLegacyAll.py and varMerge.py, you need to change baseDir and frameworkDir in skimLegacyAll.py, the output will be in directory "Rootplas/"

datacard stuff
-----------------------

    scripts used to prepare datacards

    Step 1:
        Create Template Variations
        Current Working Direcotry is BaseDir, please copy LegacyV2/mvaTool/*.py to BaseDir
        change frameworkDir, inputBaseDir, outputBaseDir
        <python makeVarHEPJob.py>
        this command will create a script all.sh, directory Output
        <bash all.sh>
        this will submit all the jobs to IHEP farm to create all the template needed for all the sub categories
        each job runs mvaTool.C 

    Step 2 :
        create datacard
        In datacard_Template.py createDatacardRootFile.py, you can tune the processes and nuisances
        <python runCreateTemplate.py> to create the template


    now you have everything needed for combine fitting

combine jobs
----------------------
  
    Here are the scripts used for submit combine fitting jobs
    goes into CMSSW/src/
    cmsenv
    create a directory "test"(for example)
    cd test/
    copy combJobs/LegacyV2/*.py .
    manipulate_datacards.py is used to combine all the datacards you produced before, you need to change the input path of this manipuldate_datacards.py
    python <make_newComJobs.py>
    this will create jobs for the fits
    <bash all.sh>
    this will submit all the combine fitting job to IHEP farm

    <plotLimit.py> is a tool to collect limit result, you can use it to optimize #bin
        
