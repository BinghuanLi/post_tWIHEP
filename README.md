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

Scripts in directory "rootplJobs" are used to create rootplas. It takes the output of tWIHEPFramework as input. The script actually reconstruct variables and selections is "LegacyV2/Rootplas_LegacyAll.C".
1. Current Working Directory is BaseDir1, please copy rootplJobs/Datacard/\*.py to BaseDir1
2. makeHEPSubmit.py is the script to create HEP jobs at IHEP, change frameworkDir, inputBaseDir, outputBaseDir, executable of this script so the job will run frameworkDir/executable
3. ` python makeHEPSubmit.py` will create a script all.sh,
     `bash all.sh` to submit all jobs, after all jobs finishes, `python resubmitJobs.py` to check failed job, if any job failed, run `bash allMissingFiles.sh`,
     after this, run `python mergeCheck.py` to remove unnecessary files,
     finally, submit job script allSkim.sh, this will run script skimLegacyAll.py and varMerge.py, you need to change baseDir and frameworkDir in skimLegacyAll.py, the output will be in directory "Rootplas/"

datacard stuff
-----------------------
Scripts in directory "rootplJobs/LegacyV2/mvaTool" are used to create datacards. It takes the output of previous step as input. The script actually create variation template is "LegacyV2/mvaTool/mvaTool.C".

1. Create Template Variations
    * create working direcotry BaseDir2, please copy LegacyV2/mvaTool/\*.py to BaseDir2
    * change frameworkDir, inputBaseDir, outputBaseDir, inputBaseDir should be set to BaseDir1
    * `python makeVarHEPJob.py` will create a script all.sh, `bash all.sh` to submit all jobs.
       This will submit all the jobs to IHEP farm to create all the template needed for all the sub categories
       Each job runs mvaTool.C 

2. Use runCreateTemplate.py to create datacard, this script will call createDatacardRootFile.py and datacard_Template.py, key variables requires hardcode are:
    * "systs_ctcvcp" in runCreateTemplate.py and createDatacardRootFile.py is a list containing the kt kv variations, to run only SM, one should set it to [""]
    * "use_ctcvcp" in createDatacardRootFile.py is set to False for SM, to True for kt kv
    * "useData" in createDatacardRootFile.py is set to False for blinded, please note regions in list "ctrls" will be unblinded
    * "Categories" in runCreateTemplate.py is chosen to run different signal extraction strategy, "SVACat2l","SVACat3j" is for SVA, "DNNSubCat2_option1" is the DNN, "SubCat2l" is for BDT, these variables are category flags set in "Rootplas_LegacyAll.C"
    * "varPerCat" in runCreateTemplate.py is used to select discriminators.
    * "createROOT" in runCreateTemplate.py is set to True to run script createDatacardRootFile.py
    * "version" and "inputDir" in runCreateTemplate.py controls the output name and input path respectively

3. After hardcoding all above variables, `python runCreateTemplate.py` to create all datacards, now you have everything needed for combine fitting
     

combine jobs
----------------------
Scripts in directory "combJobs/LegacyV2/" are used to create combine fit jobs. It takes the output of previous step as input. Notice these scripts is able to run the SM fit and create ctcv cards, but not ready to run kt-kv fit.

1. assuming you have installed combineTool and Harvester in $CMSSWBASE/src, goes into $CMSSWBASE/src, `cmsenv` to setup environement, create and enters directory "datacard/test", here you will create jobs and datacards. please copy combJobs/LegacyV2/\*.py into "datacard/test"  

2. manipulate_datacards.py is used to combine all the datacards you produced before, you need to change following variables of this manipuldate_datacards.py:
    * "inputBaseDir" should be set to BaseDir2
    * "inputdirs" in function "makecards" should be modified to match the datacards created in previous step
    * "years", "makeCTCV_card"

3. `python manipulate_datacards.py` will create and combine all datacards, for example, for DNN, it will create x+1 (x = len(years)) set of cards, "ttH_2lss_0tau_runII" datacards combines the years you set in variable "years"

4. make_newComJobs.py will create jobs to run combine fit, options before function " prepareCshJob " ( around line 40) should be hardcoded, all of them are self-explaining. `python make_newComJobs.py` to create jobs, `bash all.sh` to submit all jobs. The output can be found in directory "XXXBIN/results"

5. plotLimit.py is a tool to collect limit result, you can use it to optimize #bin ( please set loopBin to true)
        
