% path='../../res/ACE17K/TransE_advanced/1/';
path='../../res/ACE17K/WTransE_test/3/';

fid=fopen('../../data/ACE17K/info/venueInfo.data','r');
index=textscan(fid,'%s\t%s\t%s\t%s\t%s');
fclose(fid);
embedding=load([path,'venueVector.data']);
% [coeff,data,~,~,~,~]=pca(embedding);
[coeff,data,latent,~]=princomp(embedding);
scatter(data(:,1),data(:,2),'Marker','.');

colorArray=[22.8,46.55,74.96,102.52,159.79,184.8,210.93,282.47,315.13,338];
for i=1:68
    text(data(i,1),data(i,2),[' ',deblank(index{3}{i})],'Color',hsv2rgb(colorArray(index{5}{i}-47)/360,1,1));
end