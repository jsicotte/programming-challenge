import unittest
from TextScore import edit_distance
from TextScore import sentence_score
from TextScore import text_score


class TestWordDistance(unittest.TestCase):

    def test_distant_match(self):
        """
        Test a case where only the beginning and end are the same
        """
        test_word_b = "abcdef"
        test_word_a = "azzzf"
        expected_score = 4

        score = edit_distance(test_word_a, test_word_b)

        self.assertEqual(expected_score, score)

        # also test that the reverse works

        score = edit_distance(test_word_b, test_word_a)

        self.assertEqual(expected_score, score)

    def test_delete_detection(self):
        """
        Make sure that the delete action is not too aggressive.
        """
        test_word_a = "abcda"
        test_word_b = "pbcda"
        expected_score = 1

        score = edit_distance(test_word_b, test_word_a)

        self.assertEqual(expected_score, score)

    def test_no_similarity(self):
        """
        Make sure that the delete action is not too aggressive.
        """
        test_word_a = "aaaa"
        test_word_b = "bbbb"
        expected_score = 4

        score = edit_distance(test_word_b, test_word_a)

        self.assertEqual(expected_score, score)

    def test_same_word(self):
        """
        Make sure that the delete action is not too aggressive.
        """
        test_word_a = "aaaa"
        test_word_b = "aaaa"
        expected_score = 0

        score = edit_distance(test_word_b, test_word_a)

        self.assertEqual(expected_score, score)

    def test_sentence_word_difference(self):
        test_sentence_a = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
        test_sentence_b = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ut incididunt"

        score = sentence_score(test_sentence_a, test_sentence_b)

        self.assertEqual(7, score.edit_distance)
        self.assertEqual(90, score.max_score)

    def test_sentence_equality(self):
        test_sentence_a = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
        test_sentence_b = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"

        score = sentence_score(test_sentence_a, test_sentence_b)

        self.assertEqual(0, score.edit_distance)
        self.assertEqual(90, score.max_score)

    def test_document_score_additional_sentence(self):
        text_a = """Lorem ipsum dolor sit amet. Consectetur adipiscing elit."""

        text_b = """Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Sed do eiusmod tempor incididunt"""

        document_score = text_score(text_a, text_b)

        print()

    def test_example(self):
        one = """The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you."""
        two = """The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."""
        three = """We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."""

        one_two_score = text_score(one, two).percentage_score()
        one_tree_score = text_score(one, three).percentage_score()

        self.assertTrue(one_two_score > one_tree_score)
