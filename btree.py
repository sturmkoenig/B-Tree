from __future__ import annotations
import bisect
from typing import List, Tuple


class Node:
    parent: Node
    keys = List[int]
    m: int
    children = List['Node']
    is_leaf: bool

    def __init__(self, m: int, keys: List[int]=[], children: List[Node]=[], parent: Node=None, is_leaf: bool = False):
        self.parent = parent
        self.keys = keys or []
        self.children = children or []
        if children:
            for child in children:
                child.parent = self
        self.m = m
        self.is_leaf = is_leaf

    def insert(self, key):
        # Initial case
        if len(self.keys) == 0:
            self.keys.append(key)
            return self

        # Case: Node is leaf => Insert Key
        if self.is_leaf:
            self._insert_key(key)
            return self.parent or self
        
        # Case: Not LeafNode => traverse to child
        success, entry_node = self.search(key)
        if success:
            return self
        else:
            entry_node._insert_key(key)
            return self.parent or self

    def rebalance(self):
        if not self.parent:
            return
        # enough keys
        if len(self.keys) >= self.m//2:
            return
        # not enough keys for removal
        else:
            # CASE: sibling has enough keys
            # 1. Find left/right sibling
            left_sibling = None
            right_sibling = None
            separation_key = None
            for i,child in enumerate(self.parent.children):
                if child.keys == self.keys:
                    if i != 0 :
                        left_sibling = self.parent.children[i-1]
                        separation_key = self.parent.keys[i-1]
                        break
                    if i != len(self.parent.children):
                        right_sibling = self.parent.children[i+1]
                        separation_key = self.parent.keys[i]
                        break
            # 2.A IF left_sibling AND left_sibling has enough keys
            #       => roll right
            if left_sibling and len(left_sibling.keys) > self.m//2:
                new_separation_key = left_sibling.keys.pop()
                self.parent.keys = [new_key if new_key != separation_key else new_separation_key for new_key in self.parent.keys]
                self.keys = [separation_key] + self.keys
                return
            # 2.B IF right_sibling AND right_sibling has enough keys
            #       => roll left
            if right_sibling and len(right_sibling.keys) > self.m//2:
                new_separation_key = right_sibling.keys.pop(0)
                self.parent.keys = [new_key if new_key != separation_key else new_separation_key for new_key in self.parent.keys]
                self.keys = self.keys + [separation_key]
                return
            # 2.C neither left nor right sibling has enough keys
            # => has left child -> put everything to left and delete self
            if left_sibling:
                left_sibling.keys.append(separation_key)
                self.parent.keys.remove(separation_key)
                self.parent._remove_child(self)
                for transfer_key in self.keys:
                    left_sibling.keys.append(transfer_key)
                for transfer_child in self.children:
                    left_sibling.children.append(transfer_child)
            # => has right child -> put everything to self and delete right
            elif right_sibling:
                self.keys.append(separation_key)
                self.parent.keys.remove(separation_key)
                self.parent._remove_child(right_sibling)
                for transfer_key in right_sibling.keys:
                    self.keys.append(transfer_key)
                for transfer_child in right_sibling.children:
                    self.children.append(transfer_child)
            self.parent.rebalance()

            # shrink tree if necessary
            if len(self.parent.keys) == 0:
                self.parent.children = self.children
                self.parent.keys = self.keys
            # is tree still balanced?


    def delete(self, key):
        has_key, node_with_key = self.search(key)
        if not has_key:
            raise Exception("%s was not found", key)
        node_with_key._delete_key(key)

    def _delete_key(self, delete_key):
        # CASE 0 is root
        if not self.parent and self.is_leaf:
            self.keys = [x for x in self.keys if x != delete_key]
        # CASE I is leaf
        if self.is_leaf:
            self.keys.remove(delete_key)
            self.rebalance()
                # 2.D parent is shrinking
        # CASE II is internal node
        else:
            leaf_with_max = None
            max_in_left = None
            for i, child in enumerate(self.children):
                if delete_key > child.keys[-1]:
                    leaf_with_max, max_in_left = Node.get_max(self.children[i])
                    break
            self.keys = [key if key != delete_key else max_in_left for key in self.keys]
            leaf_with_max._delete_key(max_in_left)
            self.rebalance()

    def _insert_key(self, key):
        bisect.insort(self.keys, key)
        self.split()

    def split(self):
        if len(self.keys) <= self.m:
            return
        if not self.parent:
            self.parent = Node(self.m, [], [self], None, False)
        new_right_node = Node(self.m, self.keys[self.m // 2+1:], self.children[self.m // 2+1:], self.parent,
                              self.is_leaf)
        self.children = self.children[:self.m//2+1]
        middle_key = self.keys[self.m//2]
        self.keys = self.keys[:self.m//2]
        self.parent._add_child(new_right_node)
        self.parent._insert_key(middle_key)

    def _add_child(self, new_child: Node):
        for i,child in enumerate(self.children):
            if child and new_child.keys[-1] < child.keys[0]:
                self.children.insert(i, new_child)
                return
        self.children.append(new_child)

    def _remove_child(self, remove_child: Node):
        self.children = [child for child in self.children if child.keys != remove_child.keys ]

    @classmethod
    def get_min(cls, node):
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    @classmethod
    def get_max(cls, node):
        return_node = node
        while not return_node.is_leaf:
            return_node = return_node.children[-1]
        return return_node, return_node.keys[-1]

    # returns key_found,node_which_should_have_key
    def search(self, search_key) -> Tuple[bool, Node]:
        for i, key in enumerate(self.keys):
            if search_key == self.keys[i]:
                return True, self
            if search_key < self.keys[i] and not self.is_leaf:
                return self.children[i].search(search_key)
        if not self.is_leaf:
            return self.children[-1].search(search_key)
        else:
            return False, self
