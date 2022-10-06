hold on
pv2 = zeros(9,52)
for i = 1:11
    cv = (cytVals(i,1))
    pv = cv./nucVals(i,:)
    plot(xv52,pv)
    pv2(i,:) = pv
end