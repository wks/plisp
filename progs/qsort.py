#!/usr/bin/env plisp.py

['begin',
        ['setq', 'qsort', ['lambda', ['lst'], ['if',
            ['null', 'lst'], 'lst',
            ['let',
                [
                    ['pivot', ['first', 'lst']],
                    ['others', ['rest', 'lst']],
                    ['parts', ['partition',
                        ['lambda', ['x'], ['<', 'x', 'pivot']], 'others']],
                    ['left', ['first', 'parts']],
                    ['right', ['first', ['rest', 'parts']]],
                    ],
                ['append',
                    ['qsort','left'], ['list', 'pivot'], ['qsort', 'right']]
                ]
            ]]],
        ['print', q("How many?")],
        ['setq', 'n', ['read']],
        ['setq', 'readn', ['lambda', ['to-read'], 
            ['if', ['==', 'to-read', 0], q([]),
                ['cons', ['read'], ['readn', ['-', 'to-read', 1]]]]]],
        ['setq', 'numbers', ['readn', 'n']],
        ['print', 'numbers'],
        ['print', ['qsort','numbers']],
        ]

