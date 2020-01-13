std::map<TString,std::map<Int_t, TString>> MapOfChannelMap={
    {"SubCat2l",{{0,"inclusive"},{1,"ee_neg"},{2,"ee_pos"},{3,"em_bl_neg"},{4,"em_bl_pos"},{5,"em_bt_neg"},{6,"em_bt_pos"},{7,"mm_bl_neg"},{8,"mm_bl_pos"},{9,"mm_bt_neg"},{10,"mm_bt_pos"}}},
    {"DNNCat",{{0,"inclusive"},{1,"ttHnode"},{2,"Restnode"},{3,"ttWnode"},{4,"tHQnode"}}},
    {"DNNCat_option2",{{0,"inclusive"},{1,"ttHnode"},{2,"Restnode"},{3,"ttWnode"},{4,"tHQnode"}}},
    {"DNNCat_option3",{{0,"inclusive"},{1,"ttHnode"},{2,"Restnode"},{3,"ttWnode"},{4,"tHQnode"}}},
    {"DNNSubCat1_option1",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_Restnode"},{5,"em_ttWnode"},{6,"em_tHQnode"},{7,"mm_ttHnode"},{8,"mm_Restnode"},{9,"mm_ttWnode"},{10,"mm_tHQnode"}}},
    {"DNNSubCat1_option2",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_Restnode"},{5,"em_ttWnode"},{6,"em_tHQnode"},{7,"mm_ttHnode"},{8,"mm_Restnode"},{9,"mm_ttWnode"},{10,"mm_tHQnode"}}},
    {"DNNSubCat1_option3",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_Restnode"},{5,"em_ttWnode"},{6,"em_tHQnode"},{7,"mm_ttHnode"},{8,"mm_Restnode"},{9,"mm_ttWnode"},{10,"mm_tHQnode"}}},
    {"DNNSubCat2_option1",{{1,"ee_ttHnode"},{2,"ee_Restnode"},{3,"ee_ttWnode"},{4,"ee_tHQnode"},{5,"em_ttHnode"},{6,"em_Restnode"},{7,"em_ttWnode"},{8,"em_tHQnode"},{9,"mm_ttHnode"},{10,"mm_Restnode"},{11,"mm_ttWnode"},{12,"mm_tHQnode"}}},
    {"DNNSubCat2_option2",{{1,"ee_ttHnode"},{2,"ee_Restnode"},{3,"ee_ttWnode"},{4,"ee_tHQnode"},{5,"em_ttHnode"},{6,"em_Restnode"},{7,"em_ttWnode"},{8,"em_tHQnode"},{9,"mm_ttHnode"},{10,"mm_Restnode"},{11,"mm_ttWnode"},{12,"mm_tHQnode"}}},
    {"DNNSubCat2_option3",{{1,"ee_ttHnode"},{2,"ee_Restnode"},{3,"ee_ttWnode"},{4,"ee_tHQnode"},{5,"em_ttHnode"},{6,"em_Restnode"},{7,"em_ttWnode"},{8,"em_tHQnode"},{9,"mm_ttHnode"},{10,"mm_Restnode"},{11,"mm_ttWnode"},{12,"mm_tHQnode"}}},
    // cut based on AMS2
    {"DNNAMS2Cat1_option1",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    {"DNNAMS2Cat1_option2",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    {"DNNAMS2Cat1_option3",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    // cut based on AMS3
    {"DNNAMS3Cat1_option1",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    {"DNNAMS3Cat1_option2",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    {"DNNAMS3Cat1_option3",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"Restnode"},{4,"ttWnode"},{5,"tHQnode"}}},
    };

// Bin Maps  
std::map<TString, std::map<TString, Int_t>> BinMap = {
    // pre-Xmas Bin number
    //{"DNNSubCat2_option1",{{"ee_ttHnode",5},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},{"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},{"mm_ttHnode",13},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}}},
    // Post-Xmas Bin number
    //{"DNNSubCat2_option2",{{"ee_ttHnode",4},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",3},{"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},{"mm_ttHnode",11},{"mm_Restnode",13},{"mm_ttWnode",19},{"mm_tHQnode",7}}},
    // used Bin number
    {"DNNSubCat2_option1",{{"ee_ttHnode",5},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},{"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},{"mm_ttHnode",13},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}}},
    {"DNNSubCat2_option2",{{"ee_ttHnode",5},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},{"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},{"mm_ttHnode",13},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}}},
};
  
    // Cuts on DNN_maxval according to AMS
std::map<TString,std::map<TString, Double_t>> AMS_MapOfCuts={
    {"DNNAMS2Cat1_option1",{{"ttHnode_SigRegion",0.41},{"ttHnode_ttWctrl",0.32}}},
    {"DNNAMS2Cat1_option2",{{"ttHnode_SigRegion",0.45},{"ttHnode_ttWctrl",0.4}}},
    {"DNNAMS2Cat1_option3",{{"ttHnode_SigRegion",0.45},{"ttHnode_ttWctrl",0.4}}},
    {"DNNAMS3Cat1_option1",{{"ttHnode_SigRegion",0.47},{"ttHnode_ttWctrl",0.32}}},
    {"DNNAMS3Cat1_option2",{{"ttHnode_SigRegion",0.49},{"ttHnode_ttWctrl",0.4}}},
    {"DNNAMS3Cat1_option3",{{"ttHnode_SigRegion",0.45},{"ttHnode_ttWctrl",-1}}},
};
std::map<int,std::vector<TString>> Variation_Map={
    //{2016,{"JERUp","JERDown","MetShiftUp","MetShiftDown","JESUp_FlavorQCD","JESDown_FlavorQCD","JESUp_RelativeSample_2016","JESDown_RelativeSample_2016"}},
    //{2017,{"JERUp","JERDown","MetShiftUp","MetShiftDown","JESUp_FlavorQCD","JESDown_FlavorQCD","JESUp_RelativeSample_2017","JESDown_RelativeSample_2017"}},
    //{2018,{"JERUp","JERDown","MetShiftUp","MetShiftDown","JESUp_FlavorQCD","JESDown_FlavorQCD","JESUp_RelativeSample_2018","JESDown_RelativeSample_2018"}},
    {2016,{}},
    {2017,{}},
    {2018,{}},
};
std::map<TString,int> IDOfReWeight={
    {"kt_m3_kv_1",1},
    {"kt_m2_kv_1",2},
    {"kt_m1p5_kv_1",3},
    {"kt_m1p25_kv_1",4},
    {"kt_m0p75_kv_1",5},
    {"kt_m0p5_kv_1",6},
    {"kt_m0p25_kv_1",7},
    {"kt_0_kv_1",8},
    {"kt_0p25_kv_1",9},
    {"kt_0p5_kv_1",10},
    {"kt_0p75_kv_1",11},
    {"kt_1_kv_1",12}, // standard model
    {"kt_1p25_kv_1",13},
    {"kt_1p5_kv_1",14},
    {"kt_2_kv_1",15},
    {"kt_3_kv_1",16},
    {"kt_m2_kv_1p5",18},
    {"kt_m1p5_kv_1p5",19},
    {"kt_m1p25_kv_1p5",20},
    {"kt_m1_kv_1p5",21},
    {"kt_m0p5_kv_1p5",23},
    {"kt_m0p25_kv_1p5",24},
    {"kt_0p25_kv_1p5",26},
    {"kt_0p5_kv_1p5",27},
    {"kt_1_kv_1p5",29},
    {"kt_1p25_kv_1p5",30},
    {"kt_2_kv_1p5",32},
    {"kt_m3_kv_0p5",34},
    {"kt_m2_kv_0p5",35},
    {"kt_m1p25_kv_0p5",37},
    {"kt_1p25_kv_0p5",47},
    {"kt_2_kv_0p5",49},
    {"kt_3_kv_0p5",50},
    {"cosa_m0p9",51},
    {"cosa_m0p8",52},
    {"cosa_m0p7",53},
    {"cosa_m0p6",54},
    {"cosa_m0p5",55},
    {"cosa_m0p4",56},
    {"cosa_m0p3",57},
    {"cosa_m0p2",58},
    {"cosa_m0p1",59},
    {"cosa_mp0001",60},// -0.0001, 
    {"cosa_0p1",61},
    {"cosa_0p2",62},
    {"cosa_0p3",63},
    {"cosa_0p4",64},
    {"cosa_0p5",65},
    {"cosa_0p6",66},
    {"cosa_0p7",67},
    {"cosa_0p8",68},
    {"cosa_0p9",69}
};
