from unittest import TestCase

import pytest as pytest

from btree import Node
import jsonpickle


def is_equal(btree_one: Node, btree_two: Node):
    assert btree_one.keys == btree_two.keys
    for i, child in enumerate(btree_one.children):
        try:
            is_equal(child, btree_two.children[i])
        except:
            raise Exception("nodes have not the same size of children")


class TestNode(TestCase):
    # insert 4 into empty tree
    # => [4, 5]
    # insert 5
    # => [4, 5]
    def test_insert_trivial(self):
        btree_m2 = Node(2, [4, 5], None, None)
        assert btree_m2.keys == [4, 5]

    # insert 4,5,6
    # => [5]
    #   /  \
    # [4]  [6]
    def test_insert_split_root_one(self):
        btree = Node(2, [4, 5], None, None, True)
        btree = btree.insert(6)
        assert btree.keys == [5]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [4]
        assert btree.children[1].keys == [6]

    # insert 4,5,6,7,8
    # => [5 , 7]
    #   /  |  \
    # [4] [6] [8]
    def test_insert_split_child_right(self):
        btree = Node(2, [4, 5], None, None, True)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        assert btree.keys == [5, 7]
        assert len(btree.children) == 3
        assert btree.children[0].keys == [4]
        assert btree.children[1].keys == [6]
        assert btree.children[2].keys == [8]

    # insert 4, 6, 5
    # => [5]
    #   /  \
    # [4]  [6]
    def test_insert_split_root_two(self):
        btree = Node(2, [4, 6], None, None, True)
        btree = btree.insert(5)
        assert btree.keys == [5]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [4]
        assert btree.children[1].keys == [6]

    # insert 4, 5, 6, 7
    # => [5]
    #   /  \
    # [4]  [6, 7]
    def test_insert_split_m3_one(self):
        btree = Node(3, [4, 5, 6], None, None, True)
        btree = btree.insert(7)
        assert btree.keys == [5]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [4]
        assert btree.children[1].keys == [6, 7]

    # insert 5, 6, 7, 4
    # => [5]
    #   /  \
    # [4]  [6, 7]
    def test_insert_split_m3_two(self):
        btree = Node(3, [5, 6, 7], None, None, True)
        btree = btree.insert(4)
        assert btree.keys == [5]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [4]
        assert btree.children[1].keys == [6, 7]

    # insert 4,5,6,7,8,9,10
    # =>    [7]
    #     /   \
    #    [5]  [9]
    #   /  |  |  \
    # [4] [6] [8] [10]
    def test_insert_split_child_right(self):
        btree = Node(2, [4, 5], None, None, True)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        btree = btree.insert(9)
        btree = btree.insert(10)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [5]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 2
        assert btree.children[0].children[0].keys == [4]
        assert btree.children[0].children[1].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[1].keys == [10]

    # insert 10,9,8,7.6.5.4
    # =>    [7]
    #     /   \
    #    [5]  [9]
    #   /  |  |  \
    # [4] [6] [8] [10]
    def test_insert_split_child_left(self):
        btree = Node(2, [9, 10], None, None, True)
        btree = btree.insert(8)
        btree = btree.insert(7)
        btree = btree.insert(6)
        btree = btree.insert(5)
        btree = btree.insert(4)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [5]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 2
        assert btree.children[0].children[0].keys == [4]
        assert btree.children[0].children[1].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[1].keys == [10]

    # Tree with m=4
    # insert 1, 2, 3, 4, 5, 6, 7, 8, 9
    #           [3, 6]
    #         /    |   \
    #    [1, 2] [4, 5] [7, 8, 9]
    def test_insert_m_4(self):
        btree = Node(4, [], None, None, True)
        btree = btree.insert(1)
        btree = btree.insert(2)
        btree = btree.insert(3)
        btree = btree.insert(4)
        btree = btree.insert(5)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        btree = btree.insert(9)
        assert btree.keys == [3, 6]
        assert len(btree.children) == 3
        assert btree.children[0].keys == [1, 2]
        assert btree.children[1].keys == [4, 5]
        assert btree.children[2].keys == [7, 8, 9]

    # Tree with m=4
    # insert 1, 2, 3, 4, 5, 6, 7, 8, 9
    #           [3, 6]
    #         /    |   \
    #    [1, 2] [4, 5] [7, 8, 9]
    def test_search(self):
        btree = Node(4, [], is_leaf=True)
        btree = btree.insert(1)
        btree = btree.insert(2)
        btree = btree.insert(3)
        btree = btree.insert(4)
        btree = btree.insert(5)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        btree = btree.insert(9)

        success, node = btree.search(3)
        assert success
        is_equal(btree, node)

        success, node = btree.search(9)
        assert success
        is_equal(btree.children[-1], node)


        success, node = btree.search(1)
        assert success
        is_equal(btree.children[0], node)

        success, node = btree.search(10)
        assert not success
        is_equal(btree.children[-1], node)

    def test_serialize(self):
        btree = Node(4, [], is_leaf=True)
        btree = btree.insert(1)
        btree = btree.insert(2)
        btree = btree.insert(3)
        btree = btree.insert(4)
        btree = btree.insert(5)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        btree = btree.insert(9)
        y = jsonpickle.encode(btree)
        f = open("data/btree_test.json", "w")
        f.write(y)

    def test_desirialize(self):
        btree = Node(4, [], is_leaf=True)
        btree = btree.insert(1)
        btree = btree.insert(2)
        btree = btree.insert(3)
        btree = btree.insert(4)
        btree = btree.insert(5)
        btree = btree.insert(6)
        btree = btree.insert(7)
        btree = btree.insert(8)
        btree = btree.insert(9)

        btree_json = open("data/btree_test.json", "r").read()
        btree_from_json = jsonpickle.decode(btree_json)

        is_equal(btree, btree_from_json)

    # insert 10,9,8,7.6.5.4
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    #         [7]
    #        [3,5][9]
    #     [22][4][6][8][10]
    def test_serialize_delete_tree_before(self):
        btree = Node(2, [9, 10], is_leaf=True)
        btree = btree.insert(8)
        btree = btree.insert(7)
        btree = btree.insert(6)
        btree = btree.insert(5)
        btree = btree.insert(4)
        btree = btree.insert(3)
        btree = btree.insert(2)
        btree = btree.insert(1)
        btree = btree.insert(11)
        y = jsonpickle.encode(btree)
        f = open("data/btree_before_delete.json", "w")
        f.write(y)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].parent.keys == [7]
        assert btree.children[0].keys == [3, 5]
        assert btree.children[1].parent.keys == [7]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 3
        assert btree.children[0].children[0].parent.keys == [3,5]
        assert btree.children[0].children[0].keys == [1, 2]
        assert btree.children[0].children[1].parent.keys == [3,5]
        assert btree.children[0].children[1].keys == [4]
        assert btree.children[0].children[2].parent.keys == [3,5]
        assert btree.children[0].children[2].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].parent.keys == [9]
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[0].parent.keys == [9]
        assert btree.children[1].children[1].keys == [10, 11]

    # insert 10,9,8,7.6.5.4
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [2] [4] [6] [8] [10]
    def test_serialize_delete_tree_after(self):
        btree = Node(2, [9, 10], is_leaf=True)
        btree = btree.insert(8)
        btree = btree.insert(7)
        btree = btree.insert(6)
        btree = btree.insert(5)
        btree = btree.insert(4)
        btree = btree.insert(3)
        btree = btree.insert(2)
        y = jsonpickle.encode(btree)
        f = open("data/btree_after_delete.json", "w")
        f.write(y)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [3, 5]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 3
        assert btree.children[0].children[0].keys == [2]
        assert btree.children[0].children[1].keys == [4]
        assert btree.children[0].children[2].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[1].keys == [10]

    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 1,11
    # after deletion should be:
    #
    # =>    [7]
    #     /    \
    #    [2,5]   [9]
    #   /  |  \   |  \
    # [2]  [3] [6] [8] [10]
    def test_delete_leaf(self):
        btree_json = open("data/btree_before_delete.json", "r").read()
        btree = jsonpickle.decode(btree_json)

        btree.delete(11)
        btree.delete(1)

        btree_json = open("data/btree_after_delete.json", "r").read()
        btree_after_delete = jsonpickle.decode(btree_json)

        is_equal(btree, btree_after_delete)

    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 1,11
    # after deletion should be:
    #
    # =>    [7]
    #     /      \
    #    [2,5]     [9]
    #   /  |  \    |  \
    # [1]  [3] [6] [8] [10, 11]
    def test_delete_leaf_rotate_right(self):
        btree_json = open("data/btree_before_delete.json", "r").read()
        btree = jsonpickle.decode(btree_json)

        btree.delete(4)

        assert len(btree.children[0].children) == 3
        assert btree.children[0].keys == [2, 5]
        assert btree.children[0].children[0].keys == [1]
        assert btree.children[0].children[1].keys == [3]
        assert btree.children[0].children[2].keys == [6]

    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 1,11
    # after deletion should be:
    #
    # =>    [7]
    #     /      \
    #    [3,5]      [10]
    #   /  |  \      |  \
    # [1,2]  [3] [6] [9]  [11]
    def test_delete_leaf_rotate_left(self):
        btree_json = open("data/btree_before_delete.json", "r").read()
        btree = jsonpickle.decode(btree_json)

        btree.delete(8)

        assert len(btree.children[1].children) == 2
        assert btree.children[1].keys == [10]
        assert btree.children[1].children[0].keys == [9]
        assert btree.children[1].children[1].keys == [11]

    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 4
    # after deletion should be:
    #
    # =>    [7]
    #     /    \
    #    [2,5]   [9]
    #   /  |  \   |  \
    # [1]  [3] [6] [8] [10, 11]
    def test_delete_leaf_leaf_two(self):

        with open("data/btree_before_delete.json", "r") as btree_file:
            btree = jsonpickle.decode(btree_file.read())

        btree.delete(4)

        assert [2,5] == btree.children[0].keys
        assert [1] == btree.children[0].children[0].keys
        assert [3] == btree.children[0].children[1].keys

    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 6
    # after deletion should be:
    #
    # =>    [7]
    #     /    \
    #    [3]          [9]
    #   /  |          |  \
    # [1,2]  [4,5]  [8] [10, 11]
    def test_delete_leaf_node_is_removed(self):

        with open("data/btree_before_delete.json", "r") as btree_file:
            btree = jsonpickle.decode(btree_file.read())

        btree.delete(6)

        assert btree.children[0].keys == [3]
        assert len(btree.children[0].children) == 2
        assert btree.children[0].children[0].keys == [1,2]
        assert btree.children[0].children[0].parent.keys == [3]
        assert btree.children[0].children[1].keys == [4,5]
        assert btree.children[0].children[1].parent.keys == [3]
    # start tree:
    # =>    [7]
    #     /    \
    #    [3,5]    [9]
    #   /  |  \    |  \
    # [1,2] [4] [6] [8] [10, 11]
    # delete 4
    # after deletion should be:
    #
    # =>    [7]
    #     /    \
    #    [2,5]   [9]
    #   /  |  \   |  \
    # [1]  [3] [6] [8] [10, 11]
    def test_delete_key_not_present_should_throw(self):

        with open("data/btree_before_delete.json", "r") as btree_file:
            btree = jsonpickle.decode(btree_file.read())

        with pytest.raises(Exception):
            btree.delete(20)

    # insert 10,9,8,7.6.5.4
    # =>    [7]
    #     /   \
    #    [5]  [9,10]
    #   /  |  |  \
    # [4] [6] [8] [11]
    # delete 7
    #    [6,9]
    #   /  |  \
    # [4,5][8] [10]
    def test_delete_root(self):
        btree = Node(2, [9, 10], None, None, True)
        btree = btree.insert(8)
        btree = btree.insert(7)
        btree = btree.insert(6)
        btree = btree.insert(5)
        btree = btree.insert(4)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [5]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 2
        assert btree.children[0].children[0].keys == [4]
        assert btree.children[0].children[1].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[1].keys == [10]

        btree.delete(7)
        assert btree.keys == [6,9]
        assert btree.children[0].keys == [4,5]
        assert btree.children[1].keys == [8]
        assert btree.children[2].keys == [10]

    # insert 10,9,8,7.6.5.4
    # =>    [7]
    #     /   \
    #    [5]  [9,10]
    #   /  |  |  \
    # [4] [6] [8] [11]
    # delete 7
    #    [7,9]
    #   /  |  \
    # [4,5][8] [10]
    def test_delete_internal_node(self):
        btree = Node(2, [9, 10], None, None, True)
        btree = btree.insert(8)
        btree = btree.insert(7)
        btree = btree.insert(6)
        btree = btree.insert(5)
        btree = btree.insert(4)
        assert btree.keys == [7]
        assert len(btree.children) == 2
        assert btree.children[0].keys == [5]
        assert btree.children[1].keys == [9]
        assert len(btree.children[0].children) == 2
        assert btree.children[0].children[0].keys == [4]
        assert btree.children[0].children[1].keys == [6]
        assert len(btree.children[1].children) == 2
        assert btree.children[1].children[0].keys == [8]
        assert btree.children[1].children[1].keys == [10]

        btree.delete(5)
        assert btree.keys == [7,9]
        assert btree.children[0].keys == [4,6]
        assert btree.children[1].keys == [8]
        assert btree.children[2].keys == [10]



