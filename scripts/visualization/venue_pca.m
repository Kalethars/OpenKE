% method='WTransH_test';
method='TransE_detailed';
order='6';
path=['../../res/ACE17K/',method,'/',order,'/'];

fid=fopen('../../data/ACE17K/info/venueInfo.data','r');
index=textscan(fid,'%s\t%s\t%s\t%s\t%s');
fclose(fid);
embedding=load([path,'venueVector.data']);
% [coeff,data,~,~,~,~]=pca(embedding);
[coeff,data,latent,~]=princomp(embedding);

colorArray=[22.8,46.55,74.96,102.52,159.79,184.8,210.93,282.47,315.13,338];
fid=fopen(['./data/',method,'_venue.data'],'w');
for i=1:68
    color=hsv2rgb(colorArray(index{5}{i}-47)/360,1,1);
    fprintf(fid,'%f\t%f\t%s\t%f\t%f\t%f\n',data(i,1),data(i,2),index{3}{i},color(1),color(2),color(3));
end
fclose(fid);

scatter(data(:,1),data(:,2),'Marker','.');

for i=1:68
    text(data(i,1),data(i,2),[' ',deblank(index{3}{i})],'Color',hsv2rgb(colorArray(index{5}{i}-47)/360,1,1));
end