import numpy as np
import matplotlib.pyplot as plt

class SVM:
    def __init__(self,kernel='linear', learning_rate=0.001,lambda_param=0.01 ,epoch=1000, debug=False, verbose=False)-> None:
        '''
        Create by Peerasit Ployaram 6410451237
        '''
        
        self.kernel = kernel
        self.learningRate = learning_rate
        self.lambda_param = lambda_param
        self.epoch = epoch                # 1 epoch for n sample
        self.w = None                       # Weight

        self.debug = debug          # True / False
        self.gradient_round = 0     # Gradient step
        self.verbose = verbose

        # history for plot graph
        self.cost_function = []
        self.zero_one_loss = []


        if self.debug:
            print("-- Parameter --\nLearning Rate: {}\nLambda Param: {}\nN_Iters: {}\n---------------".format(self.learningRate, self.lambda_param, self.epoch))

    def bias(self, features):                                               # add b to w for not compute b
        n_samples = len(features)
        return np.concatenate( (np.ones((n_samples, 1)), features), axis=1 )    # [1 , x1, x2, ..., xn]


    def gradient(self, sample, label):
        slack = label * np.dot(self.w, sample)          # Slack higeloss

        n_feature = sample.shape[0]
        gradient = np.zeros(n_feature)                  # Set array w for feature + b

        if slack >= 1:                               # if >=1 yi * (w * xi)
            gradient = (self.lambda_param * self.w)

        else:                                        # if <1 1 - yi * (w * xi)
            gradient = (self.lambda_param * self.w) - (sample * label)
        
        self.gradient_round += 1    # Count round
        return gradient

    def fit(self, x_train, y_train):
        x_train = self.bias(x_train)       # Add b in w
        x_samples = x_train.shape[1]        # get Index of sample, sample
        self.w = np.zeros(x_samples)            # Set w size feature x

        for epoch in range(self.epoch):                             # Train Epoch round
            zr_oe_loss = 0
            for index, x_sample in enumerate(x_train):
                # Compute Gradient
                gradient = self.gradient(x_sample, y_train[index])  # Find gradient

                # Update Weight
                self.w -= self.learningRate * gradient              # Update new weight

                # Save History Loss
                predict = np.sign(np.dot(self.w, x_sample))
                if predict != y_train[index]:
                    zr_oe_loss += 1

            avr_gradient = sum(gradient) / len(x_sample)            # Find average gradient of array gradient

            cost_w = 1 / 2 * np.dot(self.w, self.w) + ( self.lambda_param * avr_gradient)   # Cal Cost(w) of regularization

            if self.verbose == True:
                print(cost_w)
            
            self.cost_function.append(cost_w)
            self.zero_one_loss.append(zr_oe_loss)
            
        if self.debug:
            print("Gradient {} steps.".format(self.gradient_round))



    def predict(self, test_features):
        test_features = self.bias(test_features)   # Add b to w
        buffer = []                                    # List for y predict

        for x_sample in test_features:                 # Predict from list
            predict = np.dot(self.w, x_sample)         # Predict
            if predict < 0:
                buffer.append(-1)
            elif predict > 0:
                buffer.append(1)
            else:
                buffer.append(0)
        return buffer     


    def score(self, x_test, y_test):        
        counter = 0                             # Counter correct
        predict = self.predict(x_test)          # Predict

        for index, sample_test in enumerate(predict):
            if sample_test == y_test[index]:            # If equal +1
                counter += 1
        return counter / len(x_test)                    # Return Accuracy 0 - 1
    

    def plot_cost(self):
        plt.figure(figsize=(10,5))
        plt.plot(self.cost_function)



    def plot_accuracy(self, x_train, y_train, x_test, y_test, epoch, verbose=False):
        test = []           # List predict
        train = []
        self.debug = False  # Set debug=False for no output

        for _ in epoch:     # Loop epoch round
            self.epoch = _  # Set epoch
            model = self.fit(x_train, y_train)
            predict_test = self.score(x_test, y_test)
            predict_train = self.score(x_train, y_train)
            if verbose:
                print("Epoch {}\nValidate Accruacy is: {}\nTrain Accuracy is: {}".format(_, predict_test, predict_train))

            test.append(predict_test)
            train.append(predict_train)


        # Plot graph
        plt.figure(figsize=(10,5))
        plt.title("Model accuracy")
        plt.plot(test, label="Validation", marker='o')
        plt.plot(train, label="Train", marker='x')
        plt.legend()
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xticks(np.arange(len(epoch)), epoch)
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy (0 - 1)')
        plt.show()



    def plot_lambda(self, x_train, y_train, x_test, y_test, lambda_param, epoch, verbose=False):
        train = []          # List predict
        validate = []

        self.debug = False

        for i in lambda_param:
            self.lambda_param = i
            self.epoch = epoch
            model = self.fit(x_train, y_train)

            validate_score = self.score(x_test, y_test)
            train_score = self.score(x_train, y_train)

            if verbose:
                print("Lambda {}\nValidate Accruacy is: {}\nTrain Accuracy is: {}".format(i, validate_score, train_score))

            train.append(train_score)
            validate.append(validate_score)

        # Plot graph
        plt.figure(figsize=(10,5))
        plt.title("Model accuracy [Epoch {}]".format(epoch))
        plt.plot(validate, label="Validation", marker='o')
        plt.plot(train, label="Train", marker='x')
        plt.legend()
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xticks(np.arange(len(lambda_param)), lambda_param)
        plt.xlabel('λ (Lambda)')
        plt.ylabel('Accuracy (0 - 1)')
        plt.show()  


    def plot_loss(self):
        plt.figure(figsize=(10,5))
        plt.title("SVM with Epoch[{}], λ[{}] Training Loss".format(self.epoch, self.lambda_param))
        plt.plot(self.zero_one_loss, label='Training Loss')     # Plot from history 0-1 loss
        plt.xlabel('Epochs')
        plt.legend()
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.ylabel('0 - 1 Loss')

        plt.show()