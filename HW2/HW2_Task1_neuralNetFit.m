load x(1).csv;
load y(1).csv;
load z(1).csv;

input = [x_1_;y_1_];

trainFcn = 'trainbr';

hiddenLayerSize = 10;

net = fitnet(hiddenLayerSize,trainFcn);

net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

[net,tr] = train(net,input,z_1_);

output = net(input);

msetTrn = tr.best_perf
mseval = tr.best_vperf
msetst = tr.best_tperf

brNeuralNet = net;
save brNeuralNet3




