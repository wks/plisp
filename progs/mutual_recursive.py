#!/usr/bin/env plisp.py

['begin',
        ['setq', 'f', ['lambda', ['x'], ['if',
            ['==', 0, 'x'], 1, ['*', 'x', ['g', ['-', 'x', 1]]]]]],
        ['setq', 'g', ['lambda', ['x'], ['if',
            ['==', 0, 'x'], 1, ['+', 'x', ['f', ['-', 'x', 1]]]]]],
        ['print', ['f',0]],
        ['print', ['f',1]],
        ['print', ['f',2]],
        ['print', ['f',3]],
        ['print', ['f',4]],
        ['print', ['f',5]],
        ['print', ['f',6]],
        ['print', ['f',7]],
        ['print', ['f',8]],
        ['print', ['f',9]],
        ]

