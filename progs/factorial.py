#!/usr/bin/env plisp.py

['begin',
        ['setq', 'factorial', ['lambda', ['x'],
            ['if', ['==','x',0],
                1,
                ['*', 'x', ['factorial', ['-','x',1]]]
                ]
            ]],
        ['map',['lambda',['y'], ['print',['factorial','y']]],
            q([0,1,2,3,4,5,6,7,8,9,10])],
        ]

