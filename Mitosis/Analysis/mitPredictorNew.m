function [data,data2] = mitPredictorNew(totalNumPos,folder)

tn = str2num(totalNumPos);
for k = 1:tn
    folder2 = strcat(folder,'\Pos',string(k),'Registration\')
    data = load(strcat(folder2,'cpDataTracked.mat'));
    data = data.data;
    MitosisClassified = load(strcat(folder2,'MitosisClassified.csv'));
    frameGuesses = load(strcat(folder2,'GuessedFrames.csv'));

%interpretClassifiedChunks
MitosisTraces = frameGuesses(:,1);
MitosisTraces = MitosisTraces + 1;
MitosisFrames = frameGuesses(:,2);
%chunks = load('ChunksClassified.csv')
%chunks = e00;


%[rx cx] = size(chunks)

totalCount = sum(MitosisTraces)

%predictions = zeros(totalCount,csize)

% for z = 1:totalCount
%     spoint = (z-1)*csize + 1
%     epoint = spoint + csize - 1
%     predictions(z,:) = chunks(spoint:epoint)
% end

%data = load('cpDataTracked.mat')
%data = data.data
[r c] = size(data.nuclei.Area);
area = data.nuclei.Area;
h2b = data.nuclei.StdIntensity(:,:,2);
t = zeros(totalCount,1);
choicesScore10 = [];
finalEvents = [];
newCellCount = r+1;
count2 = 1;

for i = 1:r
      if ismember(i,MitosisTraces)
          a1 = area(i,:);
          i1 = h2b(i,:);
          %[av,av2] = slidingChunks(vec1,1);
          %[gx1,gx2] = guesser2(vec1,a1,i1);
          [rx,rr] = ismember(i,MitosisTraces);
          count2 = count2+1;
          t(i) = MitosisFrames(rr);
          id = i;
          fr = MitosisFrames(rr);
          id;
          fr;
           [~,~,choice] = scoringX(id,fr,data);
            mv1 = [data.nuclei.Area(id,choice(1,2)),data.nuclei.StdIntensity(id,choice(1,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(1,2),2)\data.nuclei.Area(id,choice(1,2))),data.nuclei.UpperQuartileIntensity(id,choice(1,2),2)*1000,20];
            mv2 = [data.nuclei.Area(id,choice(2,2)),data.nuclei.StdIntensity(id,choice(2,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(2,2),2)\data.nuclei.Area(id,choice(2,2))),data.nuclei.UpperQuartileIntensity(id,choice(2,2),2)*1000,20];
            mv3 = [data.nuclei.Area(id,choice(3,2)),data.nuclei.StdIntensity(id,choice(3,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(3,2),2)\data.nuclei.Area(id,choice(3,2))),data.nuclei.UpperQuartileIntensity(id,choice(3,2),2)*1000,20];

            tv1 = [data.nuclei.Area(choice(1,1),choice(1,2)),data.nuclei.StdIntensity(choice(1,1),choice(1,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(1,1),choice(1,2),2)\data.nuclei.Area(choice(1,1),choice(1,2))),data.nuclei.UpperQuartileIntensity(choice(1,1),choice(1,2),2)*1000,choice(1,5)];
            tv2 = [data.nuclei.Area(choice(2,1),choice(2,2)),data.nuclei.StdIntensity(choice(2,1),choice(2,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(2,1),choice(2,2),2)\data.nuclei.Area(choice(2,1),choice(2,2))),data.nuclei.UpperQuartileIntensity(choice(2,1),choice(2,2),2)*1000,choice(2,5)];
            tv3 = [data.nuclei.Area(choice(3,1),choice(3,2)),data.nuclei.StdIntensity(choice(3,1),choice(3,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(3,1),choice(3,2),2)\data.nuclei.Area(choice(3,1),choice(3,2))),data.nuclei.UpperQuartileIntensity(choice(3,1),choice(3,2),2)*1000,choice(3,5)];

            
            s1 = ssim(tv1,mv1);
            s2 = ssim(tv2,mv2);
            s3 = ssim(tv3,mv3);

            svec = [s1 s2 s3];
            [a idx] = max(svec);
            flag = 0;

            if a < 0.85
               %[~,choice] = scoringFunc2(id,fr,data);
                %mv1 = [data.nuclei.Area(id,choice(1,2)),data.nuclei.StdIntensity(id,choice(1,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(1,2),2)\data.nuclei.Area(id,choice(1,2))),data.nuclei.UpperQuartileIntensity(id,choice(1,2),2)*1000,20];
                %mv2 = [data.nuclei.Area(id,choice(2,2)),data.nuclei.StdIntensity(id,choice(2,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(2,2),2)\data.nuclei.Area(id,choice(2,2))),data.nuclei.UpperQuartileIntensity(id,choice(2,2),2)*1000,20];
                %mv3 = [data.nuclei.Area(id,choice(3,2)),data.nuclei.StdIntensity(id,choice(3,2),2)*1000,(1000*data.nuclei.StdIntensity(id,choice(3,2),2)\data.nuclei.Area(id,choice(3,2))),data.nuclei.UpperQuartileIntensity(id,choice(3,2),2)*1000,20];

                %tv1 = [data.nuclei.Area(choice(1,1),choice(1,2)),data.nuclei.StdIntensity(choice(1,1),choice(1,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(1,1),choice(1,2),2)\data.nuclei.Area(choice(1,1),choice(1,2))),data.nuclei.UpperQuartileIntensity(choice(1,1),choice(1,2),2)*1000,choice(1,5)];
                %tv2 = [data.nuclei.Area(choice(2,1),choice(2,2)),data.nuclei.StdIntensity(choice(2,1),choice(2,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(2,1),choice(2,2),2)\data.nuclei.Area(choice(2,1),choice(2,2))),data.nuclei.UpperQuartileIntensity(choice(2,1),choice(2,2),2)*1000,choice(2,5)];
                %tv3 = [data.nuclei.Area(choice(3,1),choice(3,2)),data.nuclei.StdIntensity(choice(3,1),choice(3,2),2)*1000,(1000*data.nuclei.StdIntensity(choice(3,1),choice(3,2),2)\data.nuclei.Area(choice(3,1),choice(3,2))),data.nuclei.UpperQuartileIntensity(choice(3,1),choice(3,2),2)*1000,choice(3,5)];

                s1 = ssim(tv1,mv1);
                s2 = ssim(tv2,mv2);
                s3 = ssim(tv3,mv3);

                %svec = [s1 s2 s3]

                %[a idx] = max(svec);
                flag =0;
            end
            choice(idx,:)
            svec(idx)
            if flag == 0
                choicesScore10 = [choicesScore10; choice(idx,:) svec(idx)];
            elseif flag == 1
                choicesScore10 = [choicesScore10; choice(idx,:)];
            end
            if a > 0.85
                fevent = [i, choice(idx,1), newCellCount, choice(idx,2)];
                newCellCount = newCellCount + 1;
                finalEvents = [finalEvents;fevent];
            end
      end
end

% for k = 1:totalCount
%     choicesScore10
%     
% end
                
data2 = choice;
data = mitStructure(data,finalEvents);
save(strcat(folder2,'cpDataTrackedMitosis.mat'),'data')

end
end

function [arr,coord,minset] = scoringX(id,fr,data)
    SE = strel('line',3,0);
    arr = [];
    coord = [];
    minset = zeros(3,5);
    [r c] = size(data.nuclei.Area);
    coord1 = [id id 0 0 0]
    for i = id:r
        a1 = imopen(data.nuclei.Area(i,:),SE);
        x = find(a1,1,'first');
        if abs(x-fr) < 6
            arr = [arr, i];
            coord1 = [i, x, data.nuclei.x(i,x), data.nuclei.y(i,x)];
            dx = coord1(3) - data.nuclei.x(id,x);
            dy = coord1(4) - data.nuclei.y(id,x);
            dist2 = sqrt(dx^2 + dy^2);
            coord1 = [coord1, dist2];
            coord = [coord; coord1]
        end
    end
    if length(coord) == 0
        coord = ones(3,5);
    end
    %[a, l] = min(coord(:,5));
    
    [r c] = size(coord1);
    if r<3
        coord = [coord; coord1];
        coord = [coord; coord1];
    end
    [val idx] = sort(coord(:,5),'ascend','MissingPlacement','last');
    minset(1,:) = coord(idx(1),:);
    minset(2,:) = coord(idx(2),:);
    minset(3,:) = coord(idx(3),:);
end

function [dataOut] = mitStructure(data,events2)


Mitosis = struct
[revents2 cevents2 ] = size(events2)
if revents2 > 0
    predID = events2(:,1);
    predDaughter1 = events2(:,2);
    predDaughter2 = events2(:,3);
    predFrame = events2(:,4);
    Mitosis.MotherDaughter1Daughter2Frame = [predID, predDaughter1, predDaughter2, predFrame];
    xc = 1;


    [r c] = size(data.nuclei.Area);

    for i = 1:r

        if ismember(i,predID)
            [a b] = ismember(i,predID);

            lcalc = c - predFrame(b);

            data.nuclei.Area(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Area(i,predFrame(b)+1:end,:);
            data.nuclei.Area(i,predFrame(b)+1:end,:) = 0;


            data.nuclei.BoundingBoxArea(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.BoundingBoxArea(i,predFrame(b)+1:end,:);
            data.nuclei.BoundingBoxArea(i,predFrame(b)+1:end,:) = 0;


            data.nuclei.Compactness(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Compactness(i,predFrame(b)+1:end,:);
            data.nuclei.Compactness(i,predFrame(b)+1:end,:) = 0;

            data.nuclei.Eccentricity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Eccentricity(i,predFrame(b)+1:end,:);
            data.nuclei.Eccentricity(i,predFrame(b)+1:end,:) = 0;

            data.nuclei.EulerNumber(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.EulerNumber(i,predFrame(b)+1:end,:);
            data.nuclei.EulerNumber(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.Extent(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Extent(i,predFrame(b)+1:end,:);
            data.nuclei.Extent(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.FormFactor(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.FormFactor(i,predFrame(b)+1:end,:);
            data.nuclei.FormFactor(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.IntegratedIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.IntegratedIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.IntegratedIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.IntegratedIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.IntegratedIntensityEdge(i,predFrame(b)+1:end,:);
            data.nuclei.IntegratedIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.LowerQuartileIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.LowerQuartileIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.LowerQuartileIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MADIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MADIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.MADIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MajorAxisLength(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MajorAxisLength(i,predFrame(b)+1:end,:);
            data.nuclei.MajorAxisLength(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MassDisplacement(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MassDisplacement(i,predFrame(b)+1:end,:);
            data.nuclei.MassDisplacement(i,predFrame(b)+1:end,:) = 0;


            data.nuclei.MaxFeretDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MaxFeretDiameter(i,predFrame(b)+1:end,:);
            data.nuclei.MaxFeretDiameter(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MaxIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MaxIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.MaxIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MaxIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MaxIntensityEdge(i,predFrame(b)+1:end,:);
            data.nuclei.MaxIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MaximumRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MaximumRadius(i,predFrame(b)+1:end,:);
            data.nuclei.MaximumRadius(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MeanIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MeanIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.MeanIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MeanIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MeanIntensityEdge(i,predFrame(b)+1:end,:);
            data.nuclei.MeanIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MeanRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MeanRadius(i,predFrame(b)+1:end,:);
            data.nuclei.MeanRadius(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MedianIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MedianIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.MedianIntensity(i,predFrame(b)+1:end,:) = 0;

            data.nuclei.MedianIntensityRatio(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MedianIntensityRatio(i,predFrame(b)+1:end,:);
            data.nuclei.MedianIntensityRatio(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MedianRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MedianRadius(i,predFrame(b)+1:end,:);
            data.nuclei.MedianRadius(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MinFeretDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MinFeretDiameter(i,predFrame(b)+1:end,:);
            data.nuclei.MinFeretDiameter(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MinIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MinIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.MinIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MinIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MinIntensityEdge(i,predFrame(b)+1:end,:);
            data.nuclei.MinIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.MinorAxisLength(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.MinorAxisLength(i,predFrame(b)+1:end,:);
            data.nuclei.MinorAxisLength(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.Orientation(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Orientation(i,predFrame(b)+1:end,:);
            data.nuclei.Orientation(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.Perimeter(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Perimeter(i,predFrame(b)+1:end,:);
            data.nuclei.Perimeter(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.Solidity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.Solidity(i,predFrame(b)+1:end,:);
            data.nuclei.Solidity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.StdIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.StdIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.StdIntensity(i,predFrame(b)+1:end,:) = 0;

            data.nuclei.StdIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.StdIntensityEdge(i,predFrame(b)+1:end,:);
            data.nuclei.StdIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.UpperQuartileIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.UpperQuartileIntensity(i,predFrame(b)+1:end,:);
            data.nuclei.UpperQuartileIntensity(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.label(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.label(i,predFrame(b)+1:end,:);
            data.nuclei.label(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.x(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.x(i,predFrame(b)+1:end,:);
            data.nuclei.x(i,predFrame(b)+1:end,:) = 0;
            data.nuclei.y(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.y(i,predFrame(b)+1:end,:);
            data.nuclei.y(i,predFrame(b)+1:end,:) = 0;


                    data.cytoring.Area(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Area(i,predFrame(b)+1:end,:);
            data.cytoring.Area(i,predFrame(b)+1:end,:) = 0;

            data.cytoring.BoundingBoxArea(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.BoundingBoxArea(i,predFrame(b)+1:end,:);
            data.cytoring.BoundingBoxArea(i,predFrame(b)+1:end,:) = 0;

                    data.cytoring.EquivalentDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.EquivalentDiameter(i,predFrame(b)+1:end,:);
            data.cytoring.EquivalentDiameter(i,predFrame(b)+1:end,:) = 0;

                    data.cytoring.BoundingBoxMaximum_X(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.BoundingBoxMaximum_X(i,predFrame(b)+1:end,:);
            data.cytoring.BoundingBoxMaximum_X(i,predFrame(b)+1:end,:) = 0;

                    data.cytoring.BoundingBoxMaximum_Y(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.BoundingBoxMaximum_Y(i,predFrame(b)+1:end,:);
            data.cytoring.BoundingBoxMaximum_Y(i,predFrame(b)+1:end,:) = 0;

                    data.cytoring.BoundingBoxMinimum_Y(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.BoundingBoxMinimum_Y(i,predFrame(b)+1:end,:);
            data.cytoring.BoundingBoxMinimum_Y(i,predFrame(b)+1:end,:) = 0;

                    data.cytoring.BoundingBoxMinimum_X(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.BoundingBoxMinimum_X(i,predFrame(b)+1:end,:);
            data.cytoring.BoundingBoxMinimum_X(i,predFrame(b)+1:end,:) = 0;


            data.nuclei.EquivalentDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.EquivalentDiameter(i,predFrame(b)+1:end,:);
            data.nuclei.EquivalentDiameter(i,predFrame(b)+1:end,:) = 0;

                    data.nuclei.BoundingBoxMaximum_X(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.BoundingBoxMaximum_X(i,predFrame(b)+1:end,:);
            data.nuclei.BoundingBoxMaximum_X(i,predFrame(b)+1:end,:) = 0;

                    data.nuclei.BoundingBoxMaximum_Y(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.BoundingBoxMaximum_Y(i,predFrame(b)+1:end,:);
            data.nuclei.BoundingBoxMaximum_Y(i,predFrame(b)+1:end,:) = 0;

                    data.nuclei.BoundingBoxMinimum_Y(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.BoundingBoxMinimum_Y(i,predFrame(b)+1:end,:);
            data.nuclei.BoundingBoxMinimum_Y(i,predFrame(b)+1:end,:) = 0;

                    data.nuclei.BoundingBoxMinimum_X(predDaughter2(xc),predFrame(b)+1:end,:) = data.nuclei.BoundingBoxMinimum_X(i,predFrame(b)+1:end,:);
            data.nuclei.BoundingBoxMinimum_X(i,predFrame(b)+1:end,:) = 0;

            data.cytoring.Compactness(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Compactness(i,predFrame(b)+1:end,:);
            data.cytoring.Compactness(i,predFrame(b)+1:end,:) = 0;

            data.cytoring.Eccentricity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Eccentricity(i,predFrame(b)+1:end,:);
            data.cytoring.Eccentricity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.EulerNumber(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.EulerNumber(i,predFrame(b)+1:end,:);
            data.cytoring.EulerNumber(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.Extent(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Extent(i,predFrame(b)+1:end,:);
            data.cytoring.Extent(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.FormFactor(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.FormFactor(i,predFrame(b)+1:end,:);
            data.cytoring.FormFactor(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.IntegratedIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.IntegratedIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.IntegratedIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.IntegratedIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.IntegratedIntensityEdge(i,predFrame(b)+1:end,:);
            data.cytoring.IntegratedIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.LowerQuartileIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.LowerQuartileIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.LowerQuartileIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MADIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MADIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.MADIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MajorAxisLength(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MajorAxisLength(i,predFrame(b)+1:end,:);
            data.cytoring.MajorAxisLength(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MassDisplacement(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MassDisplacement(i,predFrame(b)+1:end,:);
            data.cytoring.MassDisplacement(i,predFrame(b)+1:end,:) = 0;


            data.cytoring.MaxFeretDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MaxFeretDiameter(i,predFrame(b)+1:end,:);
            data.cytoring.MaxFeretDiameter(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MaxIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MaxIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.MaxIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MaxIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MaxIntensityEdge(i,predFrame(b)+1:end,:);
            data.cytoring.MaxIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MaximumRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MaximumRadius(i,predFrame(b)+1:end,:);
            data.cytoring.MaximumRadius(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MeanIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MeanIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.MeanIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MeanIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MeanIntensityEdge(i,predFrame(b)+1:end,:);
            data.cytoring.MeanIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MeanRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MeanRadius(i,predFrame(b)+1:end,:);
            data.cytoring.MeanRadius(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MedianIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MedianIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.MedianIntensity(i,predFrame(b)+1:end,:) = 0;


            data.cytoring.MedianRadius(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MedianRadius(i,predFrame(b)+1:end,:);
            data.cytoring.MedianRadius(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MinFeretDiameter(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MinFeretDiameter(i,predFrame(b)+1:end,:);
            data.cytoring.MinFeretDiameter(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MinIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MinIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.MinIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MinIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MinIntensityEdge(i,predFrame(b)+1:end,:);
            data.cytoring.MinIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.MinorAxisLength(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.MinorAxisLength(i,predFrame(b)+1:end,:);
            data.cytoring.MinorAxisLength(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.Orientation(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Orientation(i,predFrame(b)+1:end,:);
            data.cytoring.Orientation(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.Perimeter(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Perimeter(i,predFrame(b)+1:end,:);
            data.cytoring.Perimeter(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.Solidity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.Solidity(i,predFrame(b)+1:end,:);
            data.cytoring.Solidity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.StdIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.StdIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.StdIntensity(i,predFrame(b)+1:end,:) = 0;

            data.cytoring.StdIntensityEdge(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.StdIntensityEdge(i,predFrame(b)+1:end,:);
            data.cytoring.StdIntensityEdge(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.UpperQuartileIntensity(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.UpperQuartileIntensity(i,predFrame(b)+1:end,:);
            data.cytoring.UpperQuartileIntensity(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.label(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.label(i,predFrame(b)+1:end,:);
            data.cytoring.label(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.x(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.x(i,predFrame(b)+1:end,:);
            data.cytoring.x(i,predFrame(b)+1:end,:) = 0;
            data.cytoring.y(predDaughter2(xc),predFrame(b)+1:end,:) = data.cytoring.y(i,predFrame(b)+1:end,:);
            data.cytoring.y(i,predFrame(b)+1:end,:) = 0;
            xc = xc + 1;


        end
    end



end
dataOut = data;
dataOut.Mitosis = Mitosis;
end