#!/usr/bin/env python

from UserDict import UserDict

# User convenient functions
def q(expr):
    """ Convenient function for quoting """
    return ['quote',expr]

# Context
class Context(UserDict):
    def __init__(self, parent=None):
        UserDict.__init__(self)
        self.parent = parent

default_context = Context()

# Predefined functions

## Decorators
def in_context(context, *names):
    """ put into a context """
    def wrapper(func):
        if len(names)==0:
            context[func.__name__]=func
        else:
            for name in names:
                context[name] = func
        return func
    return wrapper

def dc(*names):
    """ put into default context"""
    return in_context(default_context, *names)

def call_by_name(func):
    func.call_by_name=True
    return func

## Functions

# meta
@dc("eval")
def _eval(context, expr):
    if isinstance(expr, str):
        cur_context = context
        while cur_context is not None:
            if expr in cur_context:
                return cur_context[expr]
            else:
                cur_context = cur_context.parent
        raise KeyError(expr)
    elif isinstance(expr, list):
        first, rest = expr[0], expr[1:]
        func = _eval(context, first)
        if getattr(func,"call_by_name",False)==False:
            evrest = [_eval(context, e) for e in rest]
        else:
            evrest = rest
        # print "DEBUG: calling %s"%func
        # print "       in context %s"%context
        # print "       with args %s"%rest
        # print "       evaluated args %s"%evrest
        return func(context, *evrest)
    else:
        return expr

@dc()
@call_by_name
def quote(context, expr):
    return expr

# binding

@dc("set")
def _set(context, key, value):
    context[key]=value
    return value

@dc()
@call_by_name
def setq(context, key, value):
    context[key]=_eval(context,value)
    return value

@dc()
@call_by_name
def let(context, bindings, expr):
    new_context = Context(context)

    for k,v in bindings:
        evv = _eval(new_context, v)
        new_context[k] = evv

    return _eval(new_context, expr)

class LambdaExpression(object):
    def __init__(self, defining_context, params, expr):
        self.defining_context = defining_context
        self.params = params
        self.expr = expr

    def __call__(self, calling_context, *args):
        new_context = Context(self.defining_context)

        for k,v in zip(self.params, args):
            new_context[k] = v

        return _eval(new_context, self.expr)

@dc("lambda")
@call_by_name
def _lambda(defining_context, params, expr):
    return LambdaExpression(defining_context, params, expr)

# IO

@dc("print")
def _print(context, expr):
    print expr
    return None

@dc("read")
def _read(context):
    return input()

# Control Flow

@dc()
@call_by_name
def begin(context, *exprs):
    rv = None
    for expr in exprs:
        rv = _eval(context, expr)
    return rv

@dc()
@call_by_name
def dowhile(context, *exprs):
    while True:
        rv = begin(context, *exprs)
        if rv==False:
            return rv

@dc()
@call_by_name
def loop(context, *exprs):
    while True:
        begin(context, *exprs)

@dc("if")
@call_by_name
def _if(context, condition, iftrue, iffalse=None):
    if _eval(context, condition):
        return _eval(context, iftrue)
    else:
        return _eval(context, iffalse)

@dc()
@call_by_name
def cond(context, *exprs):
    for condition, value in exprs:
        if _eval(context, condition):
            return _eval(context, value)
    return None


# Constants

default_context['otherwise']=True
default_context['t']=True
default_context['nil']=False

otherwise = True

# Arithmetic

@dc("+")
def add(context, *exprs):
    return sum(exprs)

@dc("-")
def sub(context, expr1, expr2):
    return expr1-expr2

@dc("*")
def time(context, expr1, expr2):
    return expr1*expr2

@dc("/")
def divide(context, expr1, expr2):
    return expr1/expr2

@dc("%")
def mod(context, expr1, expr2):
    return expr1%expr2

# Relational

@dc("==")
def equal(context, expr1, expr2):
    return expr1==expr2

@dc("!=")
def not_equal(context, expr1, expr2):
    return expr1!=expr2

@dc("<")
def less_than(context, expr1, expr2):
    return expr1<expr2

@dc(">")
def greater_than(context, expr1, expr2):
    return expr1>expr2

@dc("<=")
def less_equal(context, expr1, expr2):
    return expr1<=expr2

@dc(">=")
def greater_equal(context, expr1, expr2):
    return expr1>=expr2

# Logical
@dc("and")
def _and(context, *exprs):
    return all(*exprs)

@dc("or")
def _or(context, *exprs):
    return any(*exprs)

@dc("not")
def _not(context, expr):
    return not expr

# High-order Functions

@dc("filter")
def _filter(context, predicate, lst):
    return filter(lambda elem: predicate(context, elem), lst)

@dc("map")
def _map(context, func, lst):
    return map(lambda elem: func(context, elem), lst)

@dc("reduce")
def _reduce(context, func, lst):
    return reduce(lambda lhs,rhs: func(context, lhs, rhs), lst)

@dc()
def partition(context, predicate, lst):
    return [_filter(context, predicate, lst),
            _filter(context, lambda ctx,x: not predicate(ctx,x), lst)]

# List Processing

@dc()
def apply(context, func, args):
    return func(context, *args)

@dc("list")
def _list(context, *elems):
    return list(elems)

@dc()
def cons(context, first, rest):
    return [first]+rest

@dc("first","car","head")
def first(context, lst):
    return lst[0]

@dc("rest","cdr","tail")
def rest(context, lst):
    return lst[1:]

@dc()
def null(context, lst):
    return len(lst)==0

@dc()
def concat(context, lists):
    result_list = []
    for lst in lists:
        result_list.extend(lst)
    return result_list

@dc()
def append(context, *lists):
    return concat(context, lists)

# Evaluator

class PLispEvaluator(object):
    def __init__(self):
        self.context = Context(default_context)

    def evaluate(self, expr):
        return _eval(self.context, expr)

if __name__=='__main__':
    import sys
    if len(sys.argv)>1:
        prog = open(sys.argv[1]).read()
    else:
        prog = sys.stdin.read()
    evaluator = PLispEvaluator()
    evaluator.evaluate(eval(prog))
