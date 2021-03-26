
import hypothesis.strategies as st
from hypothesis import given
import unittest
from mutable import *
# lst
class TestMutableList(unittest.TestCase):
    def test_addNone(self):
        lst = dy_array()
        lst.append_to_head(None)
        self.assertEqual(lst.to_list(), [None])
        lst2 = dy_array([1, None, 2])
        self.assertEqual(lst2.to_list(), [1, None, 2])

    def test_size(self):
        self.assertEqual(dy_array().size(), 0)
        self.assertEqual(dy_array([1, 2, 3]).size(), 3)

    def test_to_list(self):
        self.assertEqual(dy_array().to_list(), [])
        self.assertEqual(dy_array([1, 2, 3]).to_list(), [1, 2, 3])

    def test_from_list(self):
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for e in test_data:
            lst = dy_array()
            lst.from_list(e)
            self.assertEqual(lst.to_list(), e)

    def test_append_to_head(self):
        lst = dy_array()
        self.assertEqual(lst.to_list(), [])
        lst.append_to_head('a')
        self.assertEqual(lst.to_list(), ['a'])
        lst.append_to_head('b')
        self.assertEqual(lst.to_list(), ['b', 'a'])

    def test_add_to_tail(self):
        lst = dy_array()
        self.assertEqual(lst.to_list(), [])
        lst.append_to_tail('a')
        self.assertEqual(lst.to_list(), ['a'])
        lst.append_to_tail('b')
        self.assertEqual(lst.to_list(), ['a', 'b'])

    def test_map(self):
        lst = dy_array()
        lst.map(str)
        self.assertEqual(lst.to_list(), [])
        lst = dy_array()
        lst.from_list([1, 2, 3])
        lst.map(str)
        self.assertEqual(lst.to_list(), ["1", "2", "3"])

    def test_reduce(self):
        lst = dy_array()
        self.assertEqual(lst.reduce(lambda st, e: st + e, 0), 0)
        lst = dy_array()
        lst.from_list([1, 2, 3])
        self.assertEqual(lst.reduce(lambda st, e: st + e, 0), 6)
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for e in test_data:
            lst = dy_array()
            lst.from_list(e)
            self.assertEqual(lst.reduce(lambda state, _: state + 1, 0), lst.size())

    def test_find(self):
        lst = dy_array()
        self.assertEqual(lst.find(1), False)
        lst = dy_array([1, 2, 3])
        self.assertEqual(lst.find(1), True)

    def test_filter(self):
        lst = dy_array()
        self.assertEqual(lst.filter(1), [])
        lst = dy_array([1, 2, 3])
        self.assertEqual(lst.filter(1), [2, 3])

    def test_combine(self):
        lst = dy_array()
        lst1 = dy_array([1, 2, 3])
        lst2 = dy_array([1, 2, 3])
        lst.combine(lst1, lst2)
        self.assertEqual(lst.to_list(), [1, 2, 3, 1, 2, 3])

    def test_remove(self):
        lst = dy_array([1, 2, 3])
        lst.remove(1)

        self.assertEqual(lst.to_list(), [2, 3])

    @given(st.lists(st.integers(), min_size=100))
    def test_from_list_to_list_equality(self, a):
        lst = dy_array()
        lst.from_list(a)
        b = lst.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        lst2 = dy_array()
        lst2.from_list(a)
        self.assertEqual(lst2.size(), len(a))

    @given(st.lists(st.integers(), min_size=100))
    def test_monoid_identity(self, li):
        lst = dy_array()
        lst.from_list(li)
        lst_test1 = dy_array()
        lst_test2 = dy_array()
        lst_test1.combine(lst.empty(), lst)
        lst_test2.combine(lst, lst.empty())
        self.assertEqual(lst_test1.to_list(), li)
        self.assertEqual(lst_test2.to_list(), li)

    @given(a=st.lists(st.integers(), min_size=100), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        lst_test1 = dy_array()
        lst1 = dy_array()
        lst2 = dy_array()
        lst3 = dy_array()
        lst1 = lst1.from_list(a)
        lst2 = lst2.from_list(b)
        lst3 = lst3.from_list(c)
        lst_test1_1 = dy_array()
        lst_test1_1.combine(lst1, lst2)
        lst_test1.combine(lst_test1_1, lst3)

        lst_test2 = dy_array()
        lst1 = dy_array()
        lst2 = dy_array()
        lst3 = dy_array()
        lst1 = lst1.from_list(a)
        lst2 = lst2.from_list(b)
        lst3 = lst3.from_list(c)
        lst_test2_2 = dy_array()
        lst_test2_2.combine(lst2, lst3)
        lst_test2.combine(lst1, lst_test2_2)

        self.assertEqual(lst_test1.to_list(), lst_test2.to_list())

    def test_iter(self):
        x = [1, 2, 3]
        lst = dy_array()
        lst.from_list(x)
        tmp = []
        for i in lst:
            tmp.append(i)
        self.assertEqual(x, tmp)
        self.assertEqual(lst.to_list(), tmp)
        i = iter(dy_array())
        self.assertRaises(StopIteration, lambda: next(i))


if __name__ == '__main__':
    unittest.main()
