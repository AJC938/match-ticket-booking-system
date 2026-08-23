import unittest

from src.modules.hash_table import HashTable
from src.modules.priority_queue import PriorityQueue
from src.modules.models import BookingRequest, User
from src.modules.searching import binary_search, linear_search
from src.modules.seat_grid import SeatGrid
from src.modules.sorting import bubble_sort, merge_sort


class DataStructureTests(unittest.TestCase):
    def test_hash_table_insert_search_delete(self):
        table = HashTable()
        table.insert("A", 10)
        table.insert("B", 20)
        self.assertEqual(table.search("A"), 10)
        self.assertEqual(table.search("B"), 20)
        self.assertTrue(table.delete("A"))
        self.assertIsNone(table.search("A"))

    def test_priority_queue_orders_by_request_priority(self):
        queue = PriorityQueue()
        queue.push(BookingRequest(3, 1.0, "GEN", "M", ["GEN-R00-C00"]))
        queue.push(BookingRequest(1, 3.0, "VIP2", "M", ["VIP-R00-C00"]))
        queue.push(BookingRequest(1, 2.0, "VIP1", "M", ["VIP-R00-C01"]))
        self.assertEqual(queue.pop().user_id, "VIP1")
        self.assertEqual(queue.pop().user_id, "VIP2")
        self.assertEqual(queue.pop().user_id, "GEN")

    def test_seat_grid_assignment(self):
        grid = SeatGrid("VIP", 2, 3)
        self.assertTrue(grid.is_free(0, 1))
        self.assertTrue(grid.assign(0, 1, "VIP001"))
        self.assertFalse(grid.assign(0, 1, "VIP002"))
        self.assertEqual(grid.get(0, 1), "VIP001")
        self.assertEqual(grid.occupied_count(), 1)

    def test_search_algorithms_find_same_user(self):
        users = [User("A", "A"), User("B", "B"), User("C", "C")]
        sorted_users = sorted(users, key=lambda user: user.user_id)
        self.assertEqual(linear_search(users, "B").user_id, "B")
        self.assertEqual(binary_search(sorted_users, "B").user_id, "B")
        self.assertIsNone(linear_search(users, "Z"))

    def test_sort_algorithms_produce_same_order(self):
        users = [User("A", "A", attendance=30), User("B", "B", attendance=90), User("C", "C", attendance=60)]
        merge_ids = [u.user_id for u in merge_sort(users, key=lambda u: u.attendance)]
        bubble_ids = [u.user_id for u in bubble_sort(users, key=lambda u: u.attendance)]
        self.assertEqual(merge_ids, ["B", "C", "A"])
        self.assertEqual(merge_ids, bubble_ids)


if __name__ == "__main__":
    unittest.main()
