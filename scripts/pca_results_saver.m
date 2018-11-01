path='../res/ACE17K/TransE/3/';

types=[{'paper'},{'author'},{'field'},{'venue'},{'institute'}];
for n=1:5
    type=char(types(n));
    embedding=load([path,type,'Vector.data']);
    [~,data,latent,~]=princomp(embedding);
    [x,y]=size(data);
    fid=fopen([path,type,'PCA.data'],'w');
    for i=1:x
        for j=1:y-1
            fprintf(fid,'%g\t',data(i,j)*latent(j));
        end
        fprintf(fid,'%g\n',data(i,y)*latent(j));
    end
    fclose(fid);
end