# MAP3K-signaling
Systematic Analysis of the MAPK Signaling Network Reveals MAP3K Driven Control of Cell Fate

within the matlab (MAP3Kinductions.mat) structure are 42 different conditions (each cell line is treated with either media, Dox (for inductions), or DoxBat (to determine cell-autonomous v. non-cell-autonomous signaling features)

within the matlab (inputs.mat) structure are 14 different conditions (WT or ADAM17ko cells were treated with specified signaling inputs and imaged every 5 minutes)

Within each main condition are several fields. The most important fields here are BSCorrp38Act (which is used to look at p38 activity), BSCorrERKAct (to look at ERK Activity) and BSCorrJNKAct (to look at JNK activity). within these structures each row represents a single cell and each column represents the subsequent timepoints. (taken using 5 min imaging intervals)
