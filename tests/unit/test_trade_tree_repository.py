from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository


def test_template():
    trade_tree = TradeTreeRepository(
        'trade_tree_title', True, '2022-04-04', '2022-04-05')
    assert trade_tree.title == 'trade_tree_title'
    assert trade_tree.isActive
    assert trade_tree.createdAt == '2022-04-04'
    assert trade_tree.updatedAt == '2022-04-05'
