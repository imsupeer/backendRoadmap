import unittest
import os
import shutil
from src.articles_manager import (
    DATA_DIR,
    list_articles,
    get_article,
    create_article,
    update_article,
    delete_article,
)


class TestArticlesManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(os.path.dirname(__file__), "temp_articles")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.original_data_dir = DATA_DIR
        from src import articles_manager

        articles_manager.DATA_DIR = self.temp_dir

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        from src import articles_manager

        articles_manager.DATA_DIR = self.original_data_dir

    def test_create_and_get_article(self):
        article_id = create_article("Test Title", "Test Content", "2024-08-07")
        article = get_article(article_id)
        self.assertIsNotNone(article)
        self.assertEqual(article["title"], "Test Title")
        self.assertEqual(article["content"], "Test Content")
        self.assertEqual(article["date"], "2024-08-07")

    def test_list_articles(self):
        create_article("Title A", "Content A", "2024-08-07")
        create_article("Title B", "Content B", "2024-08-08")
        articles = list_articles()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]["title"], "Title B")

    def test_update_article(self):
        article_id = create_article("Old Title", "Old Content", "2024-08-07")
        updated = update_article(article_id, "New Title", "New Content", "")
        self.assertTrue(updated)
        article = get_article(article_id)
        self.assertEqual(article["title"], "New Title")
        self.assertEqual(article["content"], "New Content")

    def test_delete_article(self):
        article_id = create_article("Title Del", "Content Del", "2024-08-07")
        deleted = delete_article(article_id)
        self.assertTrue(deleted)
        article = get_article(article_id)
        self.assertIsNone(article)


if __name__ == "__main__":
    unittest.main()
