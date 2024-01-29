def hi():
    print('Hi')

def bye():
    hi()
    print('Bye')

bye()
hi()


#Module
#├── FunctionDef: hi
#│   └── body
#│       └── Expr
#│           └── Call
#│               ├── func: Name (id: print)
#│               └── args
#│                   └── Constant (value: 'Hi')
#├── FunctionDef: bye
#│   └── body
#│       ├── Expr
#│       │   └── Call
#│       │       └── func: Name (id: hi)
#│       └── Expr
#│           └── Call
#│               ├── func: Name (id: print)
#│               └── args
#│                   └── Constant (value: 'Bye')
#├── Expr
#│   └── Call
#│       └── func: Name (id: bye)
#└── Expr
#    └── Call
#        └── func: Name (id: hi)