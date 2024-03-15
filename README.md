#Text Indentification in Images

AIM: The objective is to identify text in images. Train data is broken up into smaller images for each individual image. 
The trained network is then fed the test images, and predictions are made for any text present in the input image.

APPROACH: ALGORITHM APPROACH:

	1. By comparing two letters pixel by pixel, the weighted sum is calculated.
 
	2. Higher weights are provided and vice versa when there is a match.
 
	3. The final average of the weighted total is calculated, and the letter that is predicted by the majority of matching pixels is the result.
	
ALGORITHM FOR VARIABLE ELIMINATION:

	1. A text file used to calculate and record first transition probabilities is called dict transition.
 
	2. Determine value for each character as the next step.
 
	3. Variables are eliminated by calculating the character count as a whole.
 

VERTIBRI ALGORITHM APPROACH:

	1. Calculate the transition probability.
 
	2. The number of columns in the matrix is equal to the number of letters in the test data
 
	3. Probabilities determined by matching pixels to pixels are placed in the first column of the matrix.
 
	4. The previous corresponding value and transition probabilities are used to determine the next emission probabilities.
 

The final stage involves going backward to identify the letter that corresponds to the one where the value is highest. Return the string.

#References:;
1. https://www.cis.upenn.edu/~cis2620/notes/Example-Viterbi-DNA.pdf
2. https://medium.com/analytics-vidhya/viterbi-algorithm-for-prediction-with-hmm-part-3-of-the-hmm-series-6466ce2f5dc6
3. http://www.cim.mcgill.ca/~latorres/Viterbi/va_alg.htm
