"# DEEP_Q_LEARNING_TETRIS_GAME" 

. link paper: https://dione.lib.unipi.gr/xmlui/bitstream/handle/unipi/13891/Thesis___Big_Data___Analytics__Ioannis_Tsirovasilis_.pdf?sequence=1&isAllowed=y


. link introduction: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/


. library:

    -torch 2.4.0
    
    -numpy 1.26.4
    
    -pygame 2.6.0


. Input Layer: The input layer accepting the state representation.

. Hidden Layer 1: The first hidden layer consists of 64 neurons and uses the ReLU activation function.

. Hidden Layer 2: The second hidden layer consists of 64 neurons and uses the ReLU activation function.

. Hidden Layer 3: The first hidden layer consists of 64 neurons and uses the ReLU activation function.

. Hidden Layer 4: The second hidden layer consists of 64 neurons and uses the ReLU activation function.

. Output Layer: The output layers consists of 1 neuron which represents the expected reward given the input state. The activation function is linear.

. Loss Function: Mean Squared Error is used as loss function.

. Optimizer: Adam optimizer is used.

. Learning Rate: Learning rate is set to 0.001.


. run: 

    -python test.py (with bach_duong_best + max_score.pth is model of best score and anh_quang.pth is model of final score)

. train:

    -python train.py
