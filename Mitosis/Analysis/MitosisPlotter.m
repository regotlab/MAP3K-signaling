
%MedIntensityCyt = zeros(1,1200);
for i = 20:21
    folder = strcat(fname,string(i),'Registration\')
    data = load(strcat(folder,'cpDataTrackedMitosis.mat'))
    data = data.data
    MdataI = data.cytoring.MedianIntensity(:,:,1);
    ax = data.Mitosis.MotherDaughter1Daughter2Frame;
    frames = ax(:,4) ;
    Daughter1 = ax(:,2);
    Daughter2 = ax(:,3);
    Mother = ax(:,1);
    
    for j = 1:length(Mother)
        M1 = MdataI(Mother(j),1:(frames(j)-1));
        M2 = MdataI(Daughter1(j),frames(j):end);
        M3 = MdataI(Daughter2(j),frames(j):end);
        %zfill
        mvec1 = zeros(1,1200);
        mvec2 = zeros(1,1200);
        valLen = 600 + length(M2)
        valLm = 601-length(M1)
        mvec1(601:valLen) = M2;
        mvec2(601:valLen) = M3;
        mvec1(valLm:600) = M1;
        mvec2(valLm:600) = M1;
        MedIntensityCyt = [MedIntensityCyt;mvec1;mvec2];
    end
end

MedIntensityCyt = MedIntensityCyt(2:end,:)