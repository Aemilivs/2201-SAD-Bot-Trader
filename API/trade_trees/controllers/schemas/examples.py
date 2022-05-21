post_trade_tree_example = {
    'title': 'Titlee',
    'is_active': True,
    'child': {
        'discriminator': 'AND',
        'children': [
            {
                'discriminator': 'AND',
                'children': [
                    {
                        'discriminator': 'TIME_SERIES',
                        'schema_path': '1. open',
                        'discriminant': 'USD;10',
                        'operation': 'TIME_SERIES_AVERAGE_MORE_OR_EQUAL_COMPARISON'
                    },
                    {
                        'discriminator': 'TIME_SERIES',
                        'schema_path': '2. high',
                        'discriminant': 'USD;10',
                        'operation': 'TIME_SERIES_MEAN_MORE_COMPARISON'
                    }
                ]
            },
            {
                'discriminator': 'TIME_SERIES',
                'schema_path': '5. volume',
                'discriminant': 'USD;10',
                'operation': 'TIME_SERIES_MAX_LESS_OR_EQUAL_COMPARISON'
            }
        ]
    },
    'outcomes': [
        {
            'operation': 'OPEN_POSITION',
            'operand': '1',
            'target': 'BTC'
        },
        {
            'operation': 'CLOSE_POSITION',
            'operand': '1',
            'target': 'ETH'
        }
    ]
}