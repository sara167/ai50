At first, I experimented with the following setup: 
1. A convolutional layer, 32 filters using a 3x3 kernel, with relu activation 
2. Max-pooling layer, using 2x2 pool size
3. Dropout 20% 
4. A convolutional layer, 96 filters using a 3x3 kernel, with relu activation 
5. Max-pooling layer, using 2x2 pool size
6. Dropout 20% 
7. flatten
8. hidden layer, 128 units, with relu activation 
9. Dropout 30% 
10. output with units equal to the number of categories, and softmax activation
The resulting model was accurate by 81.31%.
    
I then experimented with changing the relu activation function to sigmoid. The other parameters and order remained unchanged. 
The resulting model was accurate by 98.77%.