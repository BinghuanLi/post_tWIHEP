python make_obsCombJobs.py --float -1 --era 2018 --outDir obs_results  
python make_obsCombJobs.py --float 1 --noRate --outDir impact_ttH_results  --impact 
python make_obsCombJobs.py --float 0 --noRate --outDir impact_tH_results  --impact 
python make_obsCombJobs.py --float 1 --noRate --era 2018 --outDir shapes_results --shapes
python make_obsCombJobs.py --float 1 --noRate --outDir likeli_ttH_results  --scan
python make_obsCombJobs.py --float 0 --noRate --outDir likeli_tH_results  --scan 
python make_obsCombJobs.py --float 1 --noRate --outDir GOF_results  --GOF

python make_obsCombJobs.py --float 1 --BreakDown --noRate --outDir ttH_breakdown_results  --POI r_ttH
python make_obsCombJobs.py --float 1 --BreakDown --noRate --outDir tH_breakdown_results  --POI r_tH
python make_obsCombJobs.py --float 1 --BreakDown --noRate --outDir ttW_breakdown_results  --POI r_ttW
