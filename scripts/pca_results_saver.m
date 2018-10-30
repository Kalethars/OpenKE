path='../../res/ACE17K/TransE/3/';

embedding=load([path,'venue_data.txt']);
[~,data,latent,~]=princomp(embedding);
[x,y]=size(data);
fid=fopen([path,'venue_pca.txt'],'w');
for i=1:x
    for j=1:y-1
        fprintf(fid,'%g\t',data(i,j)*latent(j));
    end
    fprintf(fid,'%g\n',data(i,y)*latent(j));
end
fclose(fid);

% embedding=load('inst_data.txt');
% [~,data,latent,~]=princomp(embedding);
% [x,y]=size(data);
% fid=fopen('PCA_Inst.txt','w');
% for i=1:x
%     for j=1:y-1
%         fprintf(fid,'%g\t',data(i,j)*latent(j));
%     end
%     fprintf(fid,'%g\n',data(i,y)*latent(j));
% end
% fclose(fid);
% 
% embedding=load('paper_data.txt');
% [~,data,latent,~]=princomp(embedding);
% [x,y]=size(data);
% fid=fopen('PCA_Paper.txt','w');
% for i=1:x
%     for j=1:y-1
%         fprintf(fid,'%g\t',data(i,j)*latent(j));
%     end
%     fprintf(fid,'%g\n',data(i,y)*latent(j));
% end
% fclose(fid);
% 
% embedding=load('author_data.txt');
% [~,data,latent,~]=princomp(embedding);
% [x,y]=size(data);
% fid=fopen('PCA_Author.txt','w');
% for i=1:x
%     for j=1:y-1
%         fprintf(fid,'%g\t',data(i,j)*latent(j));
%     end
%     fprintf(fid,'%g\n',data(i,y)*latent(j));
% end
% fclose(fid);
% 
% embedding=load('field_data.txt');
% [~,data,latent,~]=princomp(embedding);
% [x,y]=size(data);
% fid=fopen('PCA_Field.txt','w');
% for i=1:x
%     for j=1:y-1
%         fprintf(fid,'%g\t',data(i,j)*latent(j));
%     end
%     fprintf(fid,'%g\n',data(i,y)*latent(j));
% end
% fclose(fid);
% 
% embedding=load('venue_data.txt');
% [~,data,latent,~]=princomp(embedding);
% [x,y]=size(data);
% fid=fopen('PCA_Venue.txt','w');
% for i=1:x
%     for j=1:y-1
%         fprintf(fid,'%g\t',data(i,j)*latent(j));
%     end
%     fprintf(fid,'%g\n',data(i,y)*latent(j));
% end
% fclose(fid);