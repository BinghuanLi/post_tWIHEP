combine -M GoodnessOfFit --algo saturated --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 1e-1 -s -1 -D data_obs --fixedSignalStrength 1 data_cardTTCRMu2017_ws.root -n data_obs
combine -M GoodnessOfFit --algo saturated --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 1e-1 -s -1 -D data_obs --fixedSignalStrength 1 -t 300 --toysFrequentist data_cardTTCRMu2017_ws.root -n toys300