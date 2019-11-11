// Include the headers needed for sequential model

//gSystem->Load("/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_thread.so");
//gSystem->Load("/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/liblwtnn.so");
//gSystem->Load("/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_system.so");
//gSystem->AddIncludePath("/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/include/eigen3");

//R__ADD_LIBRARY_PATH(path)
R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_thread.so);
R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/liblwtnn.so);
R__LOAD_LIBRARY(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/lib/libboost_system.so);
R__ADD_INCLUDE_PATH(/cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/include/eigen3);

#include "lwtnn/NNLayerConfig.hh"
#include "lwtnn/LightweightNeuralNetwork.hh"
#include "lwtnn/parse_json.hh"
#include "lwtnn/Stack.hh" 
#include <fstream> 
#include <iostream>
#include "TString.h"

using std::cout;
using std::endl;

/*
int main(int argc, char **argv){ 

   std::string input_json_file="";
   for (int i = 1; i < argc; ++i) {
    cout<<"Command line parameter "<<i<<" is "<<argv[i]<<endl;
    if (!strcmp(argv[i], "-input")){
      input_json_file =std::string(argv[i+1]);
      cout << " use input nn json file : " << input_json_file  << endl;
    }
   }
   if(input_json_file.empty()){
      cout << " use default nn json file : " << input_json_file  << endl;
      input_json_file = "../models/neural_net_sync.json";
    }
*/
lwt::LightweightNeuralNetwork *nn_instance;
void create_lwtnn(TString input_json_file, lwt::LightweightNeuralNetwork*& NN_instance );
void create_lwtnn(TString input_json_file, lwt::LightweightNeuralNetwork*& NN_instance){
   lwt::JSONConfig network_file;
   // Read in the network file
   cout << " load nn json file : " << input_json_file  << endl;
   std::string in_file_name(input_json_file);
   std::ifstream in_file(in_file_name);
   network_file = lwt::parse_json(in_file);
   // Create a new lwtn netowrk instance
   NN_instance = new lwt::LightweightNeuralNetwork(network_file.inputs, 
      network_file.layers, network_file.outputs);
}

void set_lwtnn_inputs(std::map<std::string,double>& Inputs);
void set_lwtnn_inputs(std::map<std::string,double>& Inputs){
   Inputs["jet3_pt"] = 115.83694;
   Inputs["jet3_eta"] = -1.8762726;
   Inputs["lep1_eta"] = -2.0628693;
   Inputs["jet2_pt"] = 127.26464;
   Inputs["jet1_E"] = 459.64105;
   Inputs["jet1_pt"] = 156.83456;
   Inputs["mT_lep1"] = 111.11824;
   Inputs["resTop_BDT"] = 0.9964719;
   Inputs["jet4_phi"] = -1.3943541;
   Inputs["lep2_conePt"] = 53.14766;
   Inputs["massL"] = 107.182755;
   Inputs["jet2_E"] = 246.63837;
   Inputs["jet1_phi"] = 0.2766842;
   Inputs["jet2_eta"] = -1.2781172;
   Inputs["jet3_E"] = 387.1906;
   Inputs["n_presel_jet"] = 6.0;
   Inputs["jet4_E"] = 56.71256;
   Inputs["lep1_charge"] = 1.0;
   Inputs["avg_dr_jet"] = 4.512807;
   Inputs["lep1_phi"] = 0.76473796;
   Inputs["mindr_lep2_jet"] = 1.6448803;
   Inputs["nBJetLoose"] = 3.0;
   Inputs["jet4_pt"] = 43.634937;
   Inputs["n_presel_mu"] = 1.0;
   Inputs["mindr_lep1_jet"] = 0.5866425;
   Inputs["lep1_conePt"] = 70.65949;
   Inputs["lep2_phi"] = 1.4254931;
   Inputs["jet2_phi"] = -2.4915662;
   Inputs["lep2_eta"] = -0.5601357;
   Inputs["mbb"] = 153.49431;
   Inputs["lep1_E"] = 275.43036;
   Inputs["jet4_eta"] = -0.7349299;
   Inputs["nBJetMedium"] = 2.0;
   Inputs["Hj_tagger_resTop"] = -0.38391635;
   Inputs["Dilep_pdgId"] = 2.0;
   Inputs["mT_lep2"] = 56.546318;
   Inputs["metLD"] = 102.46797;
   Inputs["jet3_phi"] = -2.2543252;
   Inputs["maxeta"] = 2.0628693;
   Inputs["n_presel_ele"] = 1.0;
   Inputs["jet1_eta"] = -1.7373651;
   Inputs["lep2_E"] = 61.70563;
};

std::map<std::string,double> evaluate_lwtnn(lwt::LightweightNeuralNetwork* NN_instance, const std::map<std::string,double> Inputs, std::vector<TString> variables);
std::map<std::string,double> evaluate_lwtnn(lwt::LightweightNeuralNetwork* NN_instance ,const std::map<std::string,double> Inputs, std::vector<TString> variables){
   std::map<std::string,double> outputs;
   std::map<std::string,double> inputs;
   inputs = Inputs;
   for (auto& in_var:inputs){
    auto it = std::find(variables.begin(), variables.end(), in_var.first);
    if (it == variables.end()){
        inputs.erase(in_var.first);
    }
   }
   auto out_vals = NN_instance->compute(inputs);
   for (const auto& out: out_vals){
     double output_value = out.second;
     std::cout<< " NN " << out.first << " = " << output_value << std::endl;
   }
   outputs = out_vals;
   return outputs;
};

int evaluation_lwtnn(TString input_json_file){ 
   // Define some variables, often in a header file
   float output_value;
   // The map for the variables
   std::map<std::string,double> inputs;
   create_lwtnn(input_json_file, nn_instance);
   /*
   lwt::JSONConfig network_file;
   // The actual NN instance
   lwt::LightweightNeuralNetwork *nn_instance;
   // Read in the network file
   //std::string in_file_name("../models/neural_net_sync.json");
   cout << " load nn json file : " << input_json_file  << endl;
   std::string in_file_name(input_json_file);
   std::ifstream in_file(in_file_name);
   network_file = lwt::parse_json(in_file);
   // Create a new lwtn netowrk instance
   nn_instance = new lwt::LightweightNeuralNetwork(network_file.inputs, 
        network_file.layers, network_file.outputs);
   */
   // Set the variables used in training
   // Calculate the output value of the NN based on the inputs given
   std::map<std::string,double>outputs;
   set_lwtnn_inputs(inputs);
   std::vector<TString> variables={"jet3_pt","jet3_eta","lep1_eta","jet2_pt","jet1_E","jet1_pt","mT_lep1","resTop_BDT","jet4_phi","lep2_conePt","massL","jet2_E","jet1_phi","jet2_eta","jet3_E","n_presel_jet","jet4_E","lep1_charge","avg_dr_jet","lep1_phi","mindr_lep2_jet","nBJetLoose","jet4_pt","n_presel_mu","mindr_lep1_jet","lep1_conePt","lep2_phi","jet2_phi","lep2_eta","mbb","lep1_E","jet4_eta","nBJetMedium","Hj_tagger_resTop","Dilep_pdgId","mT_lep2","metLD","jet3_phi","maxeta","n_presel_ele","jet1_eta","lep2_E"};
   outputs =  evaluate_lwtnn( nn_instance, inputs, variables);
   
   //set_lwtnn_inputs(std::map<std::string,double>& inputs);
   //auto out_vals = nn_instance->compute(inputs);
   for (const auto& out: outputs) {
     output_value = out.second;
     std::cout<<"NN " << out.first << " = " << output_value << std::endl;
   }
   // Eye candy
   return 0;
}

