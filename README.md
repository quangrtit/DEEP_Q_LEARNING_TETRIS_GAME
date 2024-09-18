"# DEEP_Q_LEARNING_TETRIS_GAME" 
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/quangrtit/DEEP_Q_LEARNING_TETRIS_GAME.git
git push -u origin main

link paper: https://dione.lib.unipi.gr/xmlui/bitstream/handle/unipi/13891/Thesis___Big_Data___Analytics__Ioannis_Tsirovasilis_.pdf?sequence=1&isAllowed=y

• Input Layer: The input layer accepting the state representation.
• Hidden Layer 1: The first hidden layer consists of 32 neurons and uses the ReLU
activation function.
• Hidden Layer 2: The second hidden layer consists of 64 neurons and uses the
ReLU activation function.
• Hidden Layer 3: The first hidden layer consists of 64 neurons and uses the ReLU
activation function.
• Hidden Layer 4: The second hidden layer consists of 32 neurons and uses the
ReLU activation function.
• Output Layer: The output layers consists of 1 neuron which represents the expected reward given the input state. The activation function is linear.
• Loss Function: Mean Squared Error is used as loss function.
• Optimizer: Adam optimizer is used.
• Learning Rate: Learning rate is set to 0.001.