import unittest
import plisp
from plisp import q

class TestPLispEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = plisp.PLispEvaluator()

    def tearDown(self):
        del self.evaluator

    # convenient methods

    def eval(self, expr):
        return self.evaluator.evaluate(expr)

    def assertEvalTo(self, expr, result):
        self.assertEqual(self.eval(expr), result)


    # test cases:

    def test_atom(self):
        self.assertEvalTo(5, 5)
        self.assertEvalTo(3.14, 3.14)
        self.assertEvalTo(u"hello world!", u"hello world!")
        self.assertEvalTo((1,2,3),(1,2,3))

    def test_symbol(self):
        self.assertEvalTo("+", plisp.add)
        self.assertEvalTo("-", plisp.sub)
        self.assertEvalTo("*", plisp.time)
        self.assertEvalTo("/", plisp.divide)
        self.assertEvalTo("%", plisp.mod)
        self.assertEvalTo("==", plisp.equal)
        self.assertEvalTo("!=", plisp.not_equal)

    def test_func(self):
        self.assertEvalTo(['+', 3, ['-', 9, 7]], 3+(9-7))
        self.assertEvalTo(['+', ["*", 1, 2], ["*",3,4]], 1*2+3*4)
        self.assertEvalTo(['quote', "abc"], "abc")
        self.assertEvalTo(q([1,2,3]), [1,2,3])

    def test_set(self):
        self.eval(['set', q('blah'), 42])
        self.assertEvalTo("blah", 42)

        self.eval(['set', q('eight'), ["+", 3, 5]])
        self.assertEvalTo("eight", 8)

    def test_setq(self):
        self.eval(['setq', 'blah', 42])
        self.assertEvalTo("blah", 42)

        self.eval(['setq', 'eight', ["+", 3, 5]])
        self.assertEvalTo("eight", 8)

    def test_let(self):
        self.assertEvalTo(['let',
            [["x", ["+",3,5]]],
            ['+', 'x', 10]
            ], 18)

        self.assertEvalTo(['let',
            [
                ["x", ["+", 3, 5]],
                ["y", ["-", 10, 6]],
                ],
            ['*', 'x', 'y'],
            ], 32)

        self.assertEvalTo(['let',
            [
                ['x', 3],
                ['y', ['+', 'x', 5]],
                ],
            ['*', 'x', 'y'],
            ], 24)

    def test_lambda(self):
        self.assertEvalTo([['lambda', ['x'], ['+', 'x', 1]], 9], 10)

        self.assertEvalTo([['lambda', ['x','y'], ['+', 'x', 'y',1]], 9,10],
                20)

        self.eval(['setq', 'square', ['lambda', ['x'], ['*', 'x', 'x']]])
        self.assertEvalTo(['square', 9], 81)

        self.eval(['setq', 'square-sum', ['lambda', ['x','y'],
            ['+', ['square','x'], ['square','y']]
            ]])
        self.assertEvalTo(['square-sum', 3, 4], 25)

        self.eval(['setq', 'a', 9])
        self.assertEvalTo(['square-sum', 3, 'a'], 90)

    def test_let_lambda(self):
        self.eval(['setq', 'plus2', ['let',
            [['increment',2]],
            ['lambda', ['x'], ['+', 'x', 'increment']]
            ]])
        self.assertEvalTo(['plus2', 8], 10)

    def test_control_flow(self):
        self.assertEvalTo(['begin', ['setq','yyyy',9], 2, 'yyyy'], 9)
        self.eval(['dowhile',
            ['setq','yyyy',['+', 'yyyy', 1]],
            ['!=',['%','yyyy',7],0]
            ])
        self.assertEvalTo('yyyy',14)

        self.assertEvalTo(['if', ['==',3,3], 42], 42)
        self.assertEvalTo(['if', ['==',3,4], 42], None)
        self.assertEvalTo(['if', ['==',3,3], 42, 56], 42)
        self.assertEvalTo(['if', ['==',3,4], 42, 56], 56)

        self.assertEvalTo(['cond',
            [['==', 1, 2], q("foo")],
            [['==', 2, 2], q("bar")],
            [True, q("baz")],
            ], "bar")

        self.assertEvalTo(['cond',
            [['==', 1, 2], q("foo")],
            [['==', 2, 3], q("bar")],
            [True, q("baz")],
            ], "baz")

        self.assertEvalTo(['cond',
            [False, q("foo")],
            [False, q("bar")],
            [False, q("baz")],
            ], None)

    def test_recursion(self):
        self.eval(['setq', 'factorial', ['lambda', ['n'],
            ['if', ['==', 'n', 0],
                1,
                ['*', 'n', ['factorial', ['-', 'n', 1]]]
                ]]])
        self.assertEvalTo(['factorial', 0], 1)
        self.assertEvalTo(['factorial', 1], 1)
        self.assertEvalTo(['factorial', 2], 2)
        self.assertEvalTo(['factorial', 3], 6)
        self.assertEvalTo(['factorial', 4], 24)
        self.assertEvalTo(['factorial', 5], 120)

        self.eval(['setq', 'fibonacci', ['lambda', ['n'],
            ['cond',
                [['==', 'n', 0], 0],
                [['==', 'n', 1], 1],
                [True, ['+',
                    ['fibonacci', ['-', 'n', 1]],
                    ['fibonacci', ['-', 'n', 2]]]
                    ],
                ]]])
        self.assertEvalTo(['fibonacci', 0], 0)
        self.assertEvalTo(['fibonacci', 1], 1)
        self.assertEvalTo(['fibonacci', 2], 1)
        self.assertEvalTo(['fibonacci', 3], 2)
        self.assertEvalTo(['fibonacci', 4], 3)
        self.assertEvalTo(['fibonacci', 5], 5)
        self.assertEvalTo(['fibonacci', 10], 55)

    def test_high_order_functions(self):
        self.eval(['setq', 'even',
            ['lambda', ['x'], ['==', ['%', 'x', 2], 0]]])

        self.assertEvalTo(['filter',
            ['lambda', ['x'], ['==', ['%', 'x', 2], 0]],
            q([1,2,3,4,5,6,7,8,9,10])], [2,4,6,8,10])

        self.assertEvalTo(['filter',
            'even',
            q([1,2,3,4,5,6,7,8,9,10])], [2,4,6,8,10])

        self.assertEvalTo(['filter',
            lambda ctx,x: x%2==0,
            q([1,2,3,4,5,6,7,8,9,10])], [2,4,6,8,10])

        self.assertEvalTo(['map',
            ['lambda', ['x'], ['+', 'x', 1]],
            q([1,2,3,4,5])], [2,3,4,5,6])

        self.assertEvalTo(['map',
            lambda ctx,x: x+1,
            q([1,2,3,4,5])], [2,3,4,5,6])

        self.assertEvalTo(['reduce',
            ['lambda', ['x','y'], ['+', 'x', 'y']],
            q([1,2,3,4,5])], 15)

        self.assertEvalTo(['reduce',
            '+',
            q([1,2,3,4,5])], 15)

        self.assertEvalTo(['reduce',
            lambda ctx,x,y: x+y,
            q([1,2,3,4,5])], 15)

        self.assertEvalTo(['partition', 'even', q([1,2,3,4,5,6,7,8,9])],
                [[2,4,6,8],[1,3,5,7,9]])

    def test_list_processing(self):
        self.assertEvalTo(['apply', '+', q([1,2])], 3)
        self.assertEvalTo(['list', 1,2,q(3),4,5], [1,2,3,4,5])
        self.assertEvalTo(['cons', q("abc"), q([1,2,3])], ["abc",1,2,3])
        self.assertEvalTo(['first', q([1,2,3])], 1)
        self.assertEvalTo(['rest', q([1,2,3])], [2,3])
        self.assertEvalTo(['null', q([])], True)
        self.assertEvalTo(['null', q([1])], False)
        self.assertEvalTo(['append', q([1]), q([2,3,4]), q([5,6])], [1,2,3,4,5,6])
        self.assertEvalTo(['concat', q([[1], [2,3,4], [5,6]])], [1,2,3,4,5,6])



if __name__=='__main__':
    unittest.main()
