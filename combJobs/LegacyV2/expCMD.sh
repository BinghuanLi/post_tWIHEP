python make_expCombJobs.py --float -1 --era 2018 --outDir exp_results  
python make_expCombJobs.py --float 1 --noRate --outDir impact_ttH_exp_results  --impact 
python make_expCombJobs.py --float 0 --noRate --outDir impact_tH_exp_results  --impact 
python make_expCombJobs.py --float 1 --noRate --era 2018 --outDir shapes_exp_results --shapes
python make_expCombJobs.py --float 1 --noRate --outDir likeli_ttH_exp_results  --scan
python make_expCombJobs.py --float 0 --noRate --outDir likeli_tH_exp_results  --scan 
python make_expCombJobs.py --float 1 --noRate --outDir GOF_exp_results  --GOF

python make_expCombJobs.py --float 1 --BreakDown --noRate --outDir ttH_breakdown_exp_results  --POI r_ttH
python make_expCombJobs.py --float 1 --BreakDown --noRate --outDir tH_breakdown_exp_results  --POI r_tH
python make_expCombJobs.py --float 1 --BreakDown --noRate --outDir ttW_breakdown_exp_results  --POI r_ttW
