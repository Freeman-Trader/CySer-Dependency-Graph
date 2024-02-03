# CySer Dependency Graph Project
## By: Douglas Takada and Freeman Trader
### Mentor: Tashi Stirewal

For the program to work, run pip install igraph on your system and then run python AST.py

added ASTnode visiter
increase readability via functions
group loose code together

Nodes
- classes
- functions
    - asynch
    - def asynch
- loose statements
    - global statements

Edges
- Child-Parent edges
- Calling edges (different because it could refer to code outside of the program)
    - Later down the line, trashing edges that call for system defined functions while keeping user defined functions
