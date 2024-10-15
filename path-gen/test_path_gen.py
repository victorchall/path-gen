import unittest
import path_gen
import os
from typing import Generator, Iterable

TEST_DATA_PATH = "./testdata"
TEST_DATA_SUBPATH = TEST_DATA_PATH + "/subfolder"

class TestsByExt(unittest.TestCase):
    def test_by_ext_single_is_generator(self):
        results = path_gen.by_ext(root=TEST_DATA_PATH, exts=["ext1"], recursive=False)
        self.assertIsInstance(results, Generator)
        self.assertIsInstance(results, Iterable)

    def test_by_ext_single(self):
        results = path_gen.by_ext(root=TEST_DATA_PATH, exts=["ext1"], recursive=False)

        results = list(results)

        self.assertIn(os.path.join(TEST_DATA_PATH,"file.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_PATH,"file2.ext1"), results)
        
        self.assertEqual(len(results), 2)

    def test_by_ext_single_recursive_is_default(self):
        results = path_gen.by_ext(root=TEST_DATA_PATH, exts=["ext1"])

        results = list(results)

        self.assertIn(os.path.join(TEST_DATA_PATH,"file.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_PATH,"file2.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_SUBPATH,"subfile.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_SUBPATH,"subfile2.ext1"), results)
        self.assertEqual(len(results), 4)

    def test_by_ext_single_recursive(self):
        results = path_gen.by_ext(root=TEST_DATA_PATH, exts=["ext1"], recursive=True)

        results = list(results)

        self.assertIn(os.path.join(TEST_DATA_PATH,"file.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_PATH,"file2.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_SUBPATH,"subfile.ext1"), results)
        self.assertIn(os.path.join(TEST_DATA_SUBPATH,"subfile2.ext1"), results)
        self.assertEqual(len(results), 4)
    
    def test_by_ext_fails_if_any_ext_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext(root="foo", exts=[None,"bar"], recursive=True).__next__())

    def test_by_ext_fails_if_ext_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext(root="foo", exts=[None], recursive=True).__next__())

    def test_by_ext_fails_if_exts_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext(root=None, exts=None, recursive=True).__next__())

class TestsByExtFirstPairs(unittest.TestCase):
    def test_by_ext_first_pairs(self):
        results = path_gen.by_ext_first_pairs(root=TEST_DATA_PATH,ext_key="ext1",paired_exts=["ext2"], recursive=False)

        results = list(results)

        self.assertIn((os.path.join(TEST_DATA_PATH,"file.ext1"),os.path.join(TEST_DATA_PATH,"file.ext2")), results)
        self.assertEqual(len(results), 1)

    def test_by_ext_first_pairs_only_one_pair_for_ext_key(self):
        results = path_gen.by_ext_first_pairs(root=TEST_DATA_PATH,ext_key="ext1",paired_exts=["ext2","ext3"], recursive=False)

        results = list(results)

        matched_ext2 = (os.path.join(TEST_DATA_PATH,"file.ext1"),os.path.join(TEST_DATA_PATH,"file.ext2")) in results
        matched_ext3 = (os.path.join(TEST_DATA_PATH,"file.ext1"),os.path.join(TEST_DATA_PATH,"file.ext3")) in results

        # Note: *which* pair is returned is not gauranteed behavior on purpose
        self.assertTrue(matched_ext2 != matched_ext3)
        self.assertEqual(len(results), 1)

    def test_by_ext_first_pairs_no_recursive(self):
        results = path_gen.by_ext_first_pairs(root=TEST_DATA_PATH,ext_key="ext1",paired_exts=["ext2"], recursive=False)

        results = list(results)

        self.assertIn((os.path.join(TEST_DATA_PATH,"file.ext1"),os.path.join(TEST_DATA_PATH,"file.ext2")), results)
        self.assertEqual(len(results), 1)
    
    def test_by_ext_first_pairs_is_generator(self):
        results = path_gen.by_ext_first_pairs(root=TEST_DATA_PATH,ext_key="ext1",paired_exts=["ext2"])
        self.assertIsInstance(results, Generator)
        self.assertIsInstance(results, Iterable)

    def test_by_ext_fails_if_paired_exts_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext_first_pairs(root="foo", ext_key="bar",paired_exts=None).__next__())

    def test_by_ext_first_pairs_fails_if_root_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext_first_pairs(root=None,  ext_key="bar", paired_exts=["foo"]).__next__())

    def test_by_ext_first_pairs_fails_if_any_paired_exts_is_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext_first_pairs(root="foo",  ext_key="bar", paired_exts=["foo",None]).__next__())

    def test_by_ext_first_pairs_fails_if_ext_key_is_none(self):
        self.assertRaises(AssertionError, lambda:path_gen.by_ext_first_pairs(root="foo",  ext_key=None, paired_exts=["bar","baz"]).__next__())

    def test_by_ext_first_pairs_fails_if_ext_key_is_none(self):
        foo_value = "foo"
        self.assertRaises(AssertionError, lambda:path_gen.by_ext_first_pairs(root="bar",  ext_key=foo_value, paired_exts=[foo_value,"baz"]).__next__())
if __name__ == '__main__':
    unittest.main()