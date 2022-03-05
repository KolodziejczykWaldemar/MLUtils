#include <Python.h>

#define INSERT_COST 1
#define DELETE_COST 1
#define REPLACE_COST 2


int MinEditDistance(char *source, char *target){
     
    // Initialize temporal replace cost to the replace cost that is passed into this function                  
    int tempReplaceCost = REPLACE_COST;
    
    int candidateEditDistInsert;
    int candidateEditDistDelete;
    int candidateEditDistReplace;
    
    int currentEditDist;
    int minEditDistance;
              
              
    // Initialize cost table with dimensions (sourceLength+1,targetLength+1)                  
    int sourceLength = strlen(source);
    int targetLength = strlen(target);
    int costTable[sourceLength + 1][targetLength + 1];
    costTable[0][0] = 0;

    // Fill in column 0, from row 1 till the end
    for (int row=1; row<sourceLength + 1; row++){
    	costTable[row][0] = costTable[row - 1][0] + DELETE_COST;
    }

    // Fill in row 0, from column 1 till the end
    for (int col=1; col<targetLength + 1; col++){
    	costTable[0][col] = costTable[0][col - 1] + INSERT_COST;
    }
        

    // Loop through row 1 till the end
    for (int row=1; row<sourceLength + 1; row++){
    	
    	// Loop through column 1 till the end
        for (int col=1; col<targetLength + 1; col++){

            // Check if source character at the previous row matches the target character at the
            // previous column and set the replacement cost to 0 if source and target are the same
            if (source[row - 1] == target[col - 1]){
                tempReplaceCost = 0;
            }
            else {
            	tempReplaceCost = REPLACE_COST;
            }

          
            // Update the cost at row, col based on previous entries in the cost table
            candidateEditDistInsert = costTable[row][col - 1] + INSERT_COST;
            candidateEditDistDelete = costTable[row - 1][col] + DELETE_COST;
            candidateEditDistReplace = costTable[row - 1][col - 1] + tempReplaceCost;
    	    
    	    if (candidateEditDistInsert < candidateEditDistDelete &&
    	    	  candidateEditDistInsert < candidateEditDistReplace){
   		currentEditDist = candidateEditDistInsert;	
    	    }
    	    else if (candidateEditDistDelete < candidateEditDistInsert && 
    	    	    candidateEditDistDelete < candidateEditDistReplace){
    	    	currentEditDist = candidateEditDistDelete;
    	    }
    	    else {
    	    	currentEditDist = candidateEditDistReplace;
    	    }
    	    
    	    costTable[row][col] = currentEditDist;
    
    	}
    }

    // Return the minimum edit distance as the cost found at the last indices of table
    minEditDistance = costTable[sourceLength][targetLength];
    return minEditDistance;
}



static PyObject *method_min_edit_dist(PyObject *self, PyObject *args) {
    char *source, *target = NULL;
    int minEditDist = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ss", &source, &target)) {
        return NULL;
    }
    
    minEditDist = MinEditDistance(source, target);

    return PyLong_FromLong(minEditDist);
}

static PyMethodDef medMethods[] = {
    {"min_edit_dist", method_min_edit_dist, METH_VARARGS, "Python interface for fast calculation of minimum edit distance"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef medModule = {
    PyModuleDef_HEAD_INIT,
    "med",
    "Python interface for fast calculation of minimum edit distance",
    -1,
    medMethods
};


PyMODINIT_FUNC PyInit_med(void) {
    /* Assign module value */
    PyObject *module = PyModule_Create(&medModule);
    return module;
}
