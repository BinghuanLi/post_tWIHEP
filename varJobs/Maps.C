std::map<TString,std::map<Int_t, TString>> MapOfChannelMap={
    {"SubCat2l",{{0,"inclusive"},{1,"ee_neg"},{2,"ee_pos"},{3,"em_bl_neg"},{4,"em_bl_pos"},{5,"em_bt_neg"},{6,"em_bt_pos"},{7,"mm_bl_neg"},{8,"mm_bl_pos"},{9,"mm_bt_neg"},{10,"mm_bt_pos"}}},
    {"DNNCat",{{0,"inclusive"},{1,"ttHnode"},{2,"ttJnode"},{3,"ttWnode"},{4,"ttZnode"}}},
    {"DNNCat_option2",{{0,"inclusive"},{1,"ttHnode"},{2,"ttJnode"},{3,"ttWnode"},{4,"ttZnode"}}},
    {"DNNCat_option3",{{0,"inclusive"},{1,"ttHnode"},{2,"ttJnode"},{3,"ttWnode"},{4,"ttZnode"}}},
    {"DNNSubCat1_option1",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_ttJnode"},{5,"em_ttWnode"},{6,"em_ttZnode"},{7,"mm_ttHnode"},{8,"mm_ttJnode"},{9,"mm_ttWnode"},{10,"mm_ttZnode"}}},
    {"DNNSubCat1_option2",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_ttJnode"},{5,"em_ttWnode"},{6,"em_ttZnode"},{7,"mm_ttHnode"},{8,"mm_ttJnode"},{9,"mm_ttWnode"},{10,"mm_ttZnode"}}},
    {"DNNSubCat1_option3",{{1,"ee_neg"},{2,"ee_pos"},{3,"em_ttHnode"},{4,"em_ttJnode"},{5,"em_ttWnode"},{6,"em_ttZnode"},{7,"mm_ttHnode"},{8,"mm_ttJnode"},{9,"mm_ttWnode"},{10,"mm_ttZnode"}}},
    {"DNNSubCat2_option1",{{1,"ee_ttHnode"},{2,"ee_ttJnode"},{3,"ee_ttWnode"},{4,"ee_ttZnode"},{5,"em_ttHnode"},{6,"em_ttJnode"},{7,"em_ttWnode"},{8,"em_ttZnode"},{9,"mm_ttHnode"},{10,"mm_ttJnode"},{11,"mm_ttWnode"},{12,"mm_ttZnode"}}},
    {"DNNSubCat2_option2",{{1,"ee_ttHnode"},{2,"ee_ttJnode"},{3,"ee_ttWnode"},{4,"ee_ttZnode"},{5,"em_ttHnode"},{6,"em_ttJnode"},{7,"em_ttWnode"},{8,"em_ttZnode"},{9,"mm_ttHnode"},{10,"mm_ttJnode"},{11,"mm_ttWnode"},{12,"mm_ttZnode"}}},
    {"DNNSubCat2_option3",{{1,"ee_ttHnode"},{2,"ee_ttJnode"},{3,"ee_ttWnode"},{4,"ee_ttZnode"},{5,"em_ttHnode"},{6,"em_ttJnode"},{7,"em_ttWnode"},{8,"em_ttZnode"},{9,"mm_ttHnode"},{10,"mm_ttJnode"},{11,"mm_ttWnode"},{12,"mm_ttZnode"}}},
    // cut based on AMS2
    {"DNNAMS2Cat1_option1",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
    {"DNNAMS2Cat1_option2",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
    {"DNNAMS2Cat1_option3",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
    // cut based on AMS3
    {"DNNAMS3Cat1_option1",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
    {"DNNAMS3Cat1_option2",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
    {"DNNAMS3Cat1_option3",{{0,"inclusive"},{1,"loose_ttHnode"},{2,"tight_ttHnode"},{3,"ttJnode"},{4,"ttWnode"},{5,"ttZnode"}}},
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
