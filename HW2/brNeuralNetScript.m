load brNeuralNet.mat;
load x.csv;
load y.csv;
load z.csv;

input = [x;y];

output = brNeuralNet(input);

writematrix(output,'z-predicted.csv')