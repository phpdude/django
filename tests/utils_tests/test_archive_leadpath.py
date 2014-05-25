import os
import shutil
import tempfile
import unittest

from django.utils.archive import Archive
from django.utils._os import upath


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'archives_leadpath')


class ArchiveLeadPathTester(object):
    archive = None

    def setUp(self):
        """
        Create temporary directory for testing extraction.
        """
        self.old_cwd = os.getcwd()
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir)
        self.archive_path = os.path.join(TEST_DIR, self.archive)
        # Always start off in TEST_DIR.
        os.chdir(TEST_DIR)

    def tearDown(self):
        os.chdir(self.old_cwd)

    def test_extract_method(self):
        with Archive(self.archive) as archive:
            archive.extract(self.tmpdir)
        self.check_files(self.tmpdir)

    def check_files(self, tmpdir):
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, '2')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', '2')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', 'bar', '1')))
        self.assertTrue(os.path.isfile(os.path.join(self.tmpdir, 'foo', 'bar', '2')))


class TestZip(ArchiveLeadPathTester, unittest.TestCase):
    archive = 'foobar.zip'


class TestTar(ArchiveLeadPathTester, unittest.TestCase):
    archive = 'foobar.tar'


class TestGzipTar(ArchiveLeadPathTester, unittest.TestCase):
    archive = 'foobar.tar.gz'


class TestBzip2Tar(ArchiveLeadPathTester, unittest.TestCase):
    archive = 'foobar.tar.bz2'
