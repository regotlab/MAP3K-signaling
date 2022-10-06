

function makeMultiOnAll2(totalnum,fpath)

kmax = str2num(totalnum)

str12 = strcat(fpath,'\Pos')

folder = strcat(str12,string(10),'Registration\')
data = load(strcat(folder,'cpDataTracked.mat'));
data = data.data;

imList = data.nuclei.imageSetNames;

[yes,where] = ismember({'h2b'},imList)
if yes == 0
    [yes,where] = ismember({'Far-red'},imList)
end
if yes == 0
    [yes,where] = ismember({'H2B'},imList)
end
if yes == 0
    [yes,where] = ismember({'DAPI'},imList)
end
if yes == 0
    [yes,where] = ismember({'Nuc'},imList)
end
if yes == 0
    [yes,where] = ismember({'Far red'},imList)
end
if yes == 0
    [yes,where] = ismember({'red'},imList)
end
if yes == 0
    [yes,where] = ismember({'Red'},imList)
end
if yes == 0
    [yes,where] = ismember({'Nuclei'},imList)
end

for k = 10:kmax
    folder = strcat(str12,string(k),'Registration\')
    data = load(strcat(folder,'cpDataTracked.mat'));
    data = data.data;
    
area = data.nuclei.Area;
int1 = data.nuclei.StdIntensity(:,:,where);

[r c] = size(area);


fid1 = fopen(strcat(folder,'MitosisClassifier.ts'),'w')
%fid2 = fopen('Level2.ts','w')



m1 = zeros(135,20,25);
t = zeros(1,135);

vv = [] ;




str1 = '@problemName MitosisMean3\n';
str2 = '@timeStamps false\n';
str3=  '@classLabel true 0 1 \n';
str4= '@univariate false\n';
str5 = '\n';
str6 = '@data\n';

fprintf(fid1,str1);fprintf(fid1,str2);fprintf(fid1,str3);fprintf(fid1,str4);
fprintf(fid1,str5);fprintf(fid1,str6);

for i = 1:r
    a1 = area(i,:);
    i1 = int1(i,:);
    
    [outI,outA,outD] = mitProcessor(a1,i1);
    
    if nnz(outA) > 10
    
        outD(isnan(outD)) = 0;
        areaStr = sprintf('%.5f,',outA); areaStr = areaStr(1:end-1);
        iStr = sprintf('%.5f,',outI); iStr = iStr(1:end-1);
        dStr = sprintf('%.5f,',outD); dStr = dStr(1:end-1);


        
        areaStr = strcat(areaStr,':',iStr,':',dStr,':0\n');
        fprintf(fid1,areaStr);
        
    end
    
    
end
end
end


function [outI,outA,outD] = mitProcessor(area1,i1)
k2 =  [3.0000 2.0000 1.0000 0.5000 1.0000 2.0000 3.0000];
k3 = [3.0000 2.0000 1.0000 0.5000 1.0000 1.0000 1.0000];
SE = strel('line',3,0);

aMean = mean(area1(area1~=0));
areaRawNorm = area1./aMean;
areaClosed = imclose(areaRawNorm,SE);
areaFilt = imfilter(areaClosed,k2,'replicate');

aMean2 = mean(areaFilt(areaFilt~=0));
outA = areaFilt./aMean2;

iMean = mean(i1(i1~=0));
iRawNorm = i1./iMean;
iFilt = imfilter(iRawNorm,k3,'replicate');
iMean2 = mean(iFilt(iFilt~=0));
outI = iFilt./iMean2;

outD = outI./outA;
end