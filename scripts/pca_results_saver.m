% path='../res/ACE17K/TransE_advanced/1/';
path='../res/ACE17K/WTransE_test/1/';

types=[{'paper'},{'author'},{'field'},{'venue'},{'institute'}];
mkdir(path,'pca');
for n=1:5
    type=char(types(n));
    embedding=load([path,type,'Vector.data']);
    [coeff,data,latent,~]=princomp(embedding);
    [x,y]=size(data);
    fid=fopen([path,'pca/',type,'PCA.data'],'w');
    for i=1:x
        for j=1:y-1
            fprintf(fid,'%g\t',data(i,j)*latent(j));
        end
        fprintf(fid,'%g\n',data(i,y)*latent(y));
    end
    fclose(fid);
    fid=fopen([path,'pca/',type,'Coeff.data'],'w');
    for i=1:y
        for j=1:y-1
            fprintf(fid,'%g\t',coeff(i,j));
        end
        fprintf(fid,'%g\n',coeff(i,y));
    end
    fclose(fid);
    fid=fopen([path,'pca/',type,'Latent.data'],'w');
    for i=1:y-1
        fprintf(fid,'%g\t',latent(i));
    end
    fprintf(fid,'%g\t',latent(y));
    fclose(fid);
end