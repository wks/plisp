#!/usr/bin/env plisp.py

['dowhile',
        ['setq', 'inp', ['read']],
        ['if', ['==', 'inp', q('exit')],
            False,
            ['begin',
                ['print', ['eval', 'inp']],
                True],
            ]
        ]
        
