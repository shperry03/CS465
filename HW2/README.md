# HW2

HW2 contains the script, network, predicted z values, and the arguments behind my decisions to use the architecture that I used for Homework 2.

## Usage

To use the network, you can use the script which will allow you to load 3 files explicitly named x.csv, y.csv, and z.csv.
The model (brNeuralNet.mat) has already been trained on data and the script loads the model and runs it on the 3 files provided, then outputs a csv file of the z-predicted values for the files given. 

The model has already been trained and can be used on other csv files but the script will need to be changed accordingly.

## Model

The brNeuralNetwork model that I have included in the file is based on the Bayesian Regularization in MatLab. It uses 7 hidden layer nodes and has a split of 85% training and 15% testing. The best performance I got from this model is:
  Training: 2.07E+10
  Testing: 7.45E+09
as taken from the table below. 

From all the testing I did, the Bayesian Regularization(BR) model performed better than other architecture (Levenberg-Marquardt (LM) and Scaled Conjugate Gradient (SCG)). To begin with, I read the MatLab documents and it says, "For noisy or small problems, Bayesian Regularization (trainbr) can obtain a better solution, at the cost of taking longer". With that in mind, I began by training networks using the BR architecture and tested several different layers with different starting points. The best I generated was a model based on the 7 Hidden node layout. I then began testing the others. 

The SCG gave the worst outputs and the errors were always generally pretty large. I continued testing different nodes with the SCG architecture and it didn't seem to fit with the data we were using. Better models existed and the model overfitting was an issue moving into higher nodes.

The LM architecture was better than the SCG but still performed worse overall than the BR architecture. In the LM architecture, it seemed that overfitting was much more apparent earlier on than the other 2. The performances were generally clustered around eachother relative to increasing/decreasing nodes, but increasing nodes caused the overfitting to be much more prevalent in the error histograms and MSEs.

The BR architecture was the best performing architecture. As a whole, I believe it modeled the data much better and the fits were much tighter. The architectures in between each run were pretty different, so I took the best network from the ones I ran. After comparing all architectures, I believe I chose the best model from the ones I have run and produced. 

## Table
| Algorithm                 | Hidden Nodes | Restarts | Best Run Training MSE | Best Run Validation MSE | Best Run Test MSE | Why Thrown away?                                                                           |
| ------------------------- | ------------ | -------- | --------------------- | ----------------------- | ----------------- | ------------------------------------------------------------------------------------------ |
| Levenberg-Marquardt       | 7            | 3        | 3.00E+10              | 1.99E+10                | 3.19E+10          | problem with underfitting and there were better models available                           |
|                           | 10           | 3        | 5.07E+10              | 1.30E+11                | 1.27E+11          | better models available, BR better for problem                                             |
|                           | 12           | 3        | 4.15E+09              | 2.25E+11                | 1.45E+11          | overfitting on this example, others were not good fits                                     |
|                           | 15           | 3        | 1.40E+10              | 1.02E+11                | 5.10E+10          | the problem isn't perfectly modeled here and better models exist                           |
|                           | 20           | 3        | 1.82E+09              | 1.15E+12                | 3.79E+11          | Overfitting was apparent in all versions of this one                                       |
| Scaled Conjugate Gradient | 5            | 3        | 4.41E+10              | 2.46E+10                | 8.29E+10          | Doesn't fit the data, all over the place with runs, got lucky on this one                  |
|                           | 7            | 3        | 6.70E+10              | 3.52E+11                | 3.44E+11          | Didn't fit data, same as 5 nodes                                                           |
|                           | 10           | 3        | 2.11E+10              | 6.54E+10                | 1.58E+11          | Better models available, generally pretty all over the place, some errors were much larger |
|                           | 12           | 3        | 1.02E+11              | 1.24E+11                | 3.45E+11          | Worse than 10 nodes and bettermodels available                                             |
|                           | 15           | 3        | 8.88E+10              | 2.03E+11                | 1.69E+12          | large variation in test and train error, over training on training data                    |
| Bayesian Regularization   | 5            | 5        | 2.24E+10              | N/A                     | 1.93E+10          | More accurate models available, some models underfit based on error histogram              |
|                           | 7            | 10       | 2.07E+10              | N/A                     | 7.45E+09          | USED                                                                                       |
|                           | 10           | 8        | 6.64E+09              | N/A                     | 1.02E+11          | Model can be overtrained but the 7 node model generally performed better                   |
|                           | 12           | 5        | 7.25E+09              | N/A                     | 2.45E+10          | slight overfitting, larger variation in training and test                                  |
|                           | 15           | 5        | 8.19E+09              | N/A                     | 1.67E+10          | better performing models, larger variations in training and test                           |
|                           | 20           | 3        | 4.81E+09              | N/A                     | 8.20E+10          | Too large variation between training and test, overfitting                                 |


  
  
  
## Citations
[MATLAB](https://www.mathworks.com/help/deeplearning/gs/fit-data-with-a-neural-network.html)
