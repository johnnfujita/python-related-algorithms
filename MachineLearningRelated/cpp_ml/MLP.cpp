#include "MLP.h"

double frand() {
    return (2.0*(double)rand() / RAND_MAX) - 1.0;
}

Perceptron::Perceptron(int inputs, double bias) {
    this->bias = bias;
    weights.resize(inputs+1);
    generate(weights.begin(), weights.end(), frand);
}

double Perceptron::run(vector<double> x) {
    x.push_back(bias);
    double sum = inner_product(x.begin(), x.end(), weights.begin(), (double)0.0);
    return sigmoid(sum);
}

void Perceptron::set_weights(vector<double> w_init) {
    weights = w_init;
}

double Perceptron::sigmoid(double x) {
    return 1.0 /(1.0 + exp(-x));
}


MultiLayerPerceptron::MultiLayerPerceptron(vector<int> layers, double bias, double eta) {
    this->layers = layers;
    this->bias = bias;
    this->eta = eta;

    // multilayer perceptron

    for (int i = 0; i < layers.size(); i++) {
        values.push_back(vector<double>(layers[i],0.0));
        d.push_back(vector<double>(layers[i], 0.0));
        network.push_back(vector<Perceptron>());
        if (i > 0) // input layer
            for (int j = 0; j < layers[i]; j++)
                network[i].push_back(Perceptron(layers[i-1], bias));
    }
}

void MultiLayerPerceptron::set_weights(vector<vector<vector<double> > > w_init) {
    for (int i = 0; i < w_init.size(); i++) {
        for (int j = 0; j < w_init[i].size(); j++) 
            network[i+1][j].set_weights(w_init[i][j]); // skip first
    }
}

void MultiLayerPerceptron::print_weights() {
    cout << endl;
    for (int i = 1; i < network.size(); i++) {
        for (int j = 0; j < layers[i]; j++) {
            cout << "Layer " << i+1 << " Neuron " << j << ": ";
            for (auto &it: network[i][j].weights)
                cout << it << "  ";
            cout << endl;
        } 
    }
    cout << endl;
}

vector <double> MultiLayerPerceptron::run(vector<double> x) {
    values[0] = x;
    for (int i = 1; i < network.size(); i++)
        for (int j = 0; j < layers[i]; j++)
            values[i][j] = network[i][j].run(values[i-1]); // forward prop of the champions
    return values.back();
}

double MultiLayerPerceptron::bp(vector<double> x, vector<double> y) {
    
    // Forward Propagate
    vector<double> outputs = run(x);

    // Calculate the MSE
    vector<double> error;
    double MSE = 0.0;
    for (int i = 0; i < y.size(); i++) {
        error.push_back(y[i] - outputs[i]);
        MSE += error[i] * error[i];
    }
    MSE /= layers.back();

    //Calculate the output error terms
    for (int i = 0; i < outputs.size(); i++) {
        d.back()[i] = outputs[i] * (1 - outputs[i]) * (error[i]);
    }
    
    // Calculate the erro term of each unit on each layer
    // take network_size - 2 is taking out outputs and inputs
    for (int i = network.size() - 2; i > 0; i--) {
        for (int h = 0; h < network[i].size(); h++) {
            double forward_error = 0.0;
            // layers i+1 is cause you need to start from the previous to the last layer, and it is starting from the previous to that one;
            for (int k = 0; k < layers[i+1]; k++) {
                forward_error += network[i+1][k].weights[h] * d[i+1][k];
            d[i][h] = values[i][h] * (1-values[i][h]) * forward_error;
            }
        }
    }

    // Calculate deltas and update weights
    for (int i = 1; i < network.size(); i++) {
        for (int j = 0; j < layers[i]; j++) {
            for (int k = 0; k < layers[i-1]+1; k++){
                double delta;
                if (k==layers[i-1]) {
                    delta = eta * d[i][j] * bias;
                }
                else {
                    delta = eta * d[i][j] * values[i-1][k];
                }
                network[i][j].weights[k] += delta;
            }
        }
    }
    return MSE;
}