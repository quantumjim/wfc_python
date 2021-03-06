# Quantum Wave Function Collapse Algorithm

This is substantially [ikarth/wfc_python](https://github.com/ikarth/wfc_python), which is itself an implementation of [mxgmn/WaveFunctionCollapse](https://github.com/mxgmn/WaveFunctionCollapse) in Python.

The main difference to these, and to to all other implementations of the Wave Function Collapse algorithm, is that there are actual real life quantum wave functions being collapsed in this one, thanks to IBM's [Qiskit](https://qiskit.org).

If you want to know what was changed, check out the file 'model.py'. All lines changed have a comment including the word 'quantum'.

An example of running a job is in [run_wfc.ipynb](https://github.com/quantumjim/wfc_python/blob/master/run_wfc.ipynb). The arguments of the relevant function take the same form as those in the [samples.xml](https://github.com/mxgmn/WaveFunctionCollapse/blob/master/samples.xml) file of the original implementation.
