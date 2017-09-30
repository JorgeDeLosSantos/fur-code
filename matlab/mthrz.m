function X = mthrz(theta)
% MTH de rotación alrededor de Z

X = [cos(theta), -sin(theta), 0, 0;
      sin(theta), cos(theta), 0, 0;
      0, 0, 1, 0;
      0, 0, 0, 1];
end