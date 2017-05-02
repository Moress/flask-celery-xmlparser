import unittest
from tasks import xml_parse


class XMLParserTestCase(unittest.TestCase):

    def setUp(self):
        self.graph_count = 0
        self.graph_weight = 0

    def tearDown(self):
        self.graph_count = 0
        self.graph_weight = 0

    def test_acceptance(self):
        path = "fixtures/acceptance_test.xml"

        for (count, weight) in xml_parse(path):
            self.graph_count = count
            self.graph_weight = weight

        self.assertEqual(self.graph_count, 2)
        self.assertEqual(self.graph_weight, 1)

    def test_complex_graph_data(self):
        path = "fixtures/complex_graph_data.xml"

        for (count, weight) in xml_parse(path):
            self.graph_count = count
            self.graph_weight = weight

        self.assertEqual(self.graph_count, 10)
        self.assertEqual(self.graph_weight, 7)

    def test_cycle_graph(self):
        path = "fixtures/cycle_graph_data.xml"

        for (count, weight) in xml_parse(path):
            self.graph_count = count
            self.graph_weight = weight

        self.assertEqual(self.graph_count, 5)
        self.assertEqual(self.graph_weight, 5)

    def test_self_cycle_items(self):
        path = "fixtures/self_cycle_items.xml"

        for (count, weight) in xml_parse(path):
            self.graph_count = count
            self.graph_weight = weight

        self.assertEqual(self.graph_count, 3)
        self.assertEqual(self.graph_weight, 3)

    def test_duplicate_item_ids(self):
        path = "fixtures/duplicate_item_ids.xml"
        with self.assertRaises(Exception) as context:
            for (count, weight) in xml_parse(path):
                self.graph_count = count
                self.graph_weight = weight

        self.assertTrue('Duplicate id in file structure' in str(context.exception))

    def test_duplicate_item_ids(self):
        path = "fixtures/orphan_parents.xml"
        with self.assertRaises(Exception) as context:
            for (count, weight) in xml_parse(path):
                self.graph_count = count
                self.graph_weight = weight

        self.assertTrue('Exist orphan parents' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
