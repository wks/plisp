#!/usr/bin/env plisp.py

['begin',
        ['setq', 'fibonacci', ['lambda', ['x'],
            ['fibonacci_', 'x', 0, 1]]],
        ['setq', 'fibonacci_', ['lambda', ['x', 'a', 'b'],
            ['if', ['==', 'x', 0],
                'a',
                ['fibonacci_', ['-', 'x', 1], 'b', ['+', 'a', 'b']]
                ]]],
        ['map',['lambda',['y'], ['print',['fibonacci','y']]],
            q([0,1,2,3,4,5,6,7,8,9,10])],
        ]

