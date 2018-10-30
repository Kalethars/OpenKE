path='../../res/ACE17K/TransE/3/';

fid=fopen([path,'venue_index.txt'],'r');
index=textscan(fid,'%s\t%s\t%s\t%s\t%s');
fclose(fid);
embedding=load([path,'venue_data.txt']);
data=tsne(embedding,[],2,68,30);
scatter(data(:,1),data(:,2),'Marker','.');
for i=1:68
    text(data(i,1),data(i,2),[' ',deblank(index{3}{i})],'Color',hsv2rgb(1/10*(index{5}{i}-48),1,1));
end