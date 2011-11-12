#!/usr/bin/env plisp.py

['begin',
        ['setq', 'f', ['let',
            [['a', 42]],
            ['lambda', ['x'], ['+', 'x', 'a']],
            ]],
        ['let',
            [['a', 100]],
            ['print', ['f', 5]],
            ],
        ]

