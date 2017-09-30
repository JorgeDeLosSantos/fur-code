function T = mthtras(q)
% MTH de traslación

T = [1,0,0,q(1);
     0,1,0,q(2);
     0,0,1,q(3);
     0,0,0,1];
end