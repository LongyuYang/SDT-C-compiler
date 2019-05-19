# SDT-C-compiler
This is a simple C compiler based on syntax-directed translation(SDT) using top-down LL(1). The syntax analysis and the semantic analysis are executed simultaneously.
## Requirements
- Python 3.6
- PyQt 5.11
## Example
Click the `Open File` button to choose a source file, and then click the `Execute SDT` button to conduct the syntax-directed translation. The intermediate code will be saved to `InterCode.txt`. To generate MIPS code, click the `Generate MIPS` button and the MIPS code will be saved to `MIPS.asm`.
![Alt text](https://github.com/ynuy1998/SDT-C-compiler/raw/master/ExamplePhoto/compiler.png)
