"""
Custom search backend for Wagtail that combines MySQL and MongoDB search results.

This backend prevents duplicate content storage by:
1. Using MongoDB for BlogPage content search
2. Using MySQL for all other content types
3. Merging results from both sources
"""
import logging
import time
from itertools import chain

from django.db.models import Q
from django.core.paginator import Paginator

# 正确的导入路径
from wagtail.search.backends.base import BaseSearchBackend, BaseSearchResults
# 不需要BaseSearchQuery，因为它不在base模块中
from wagtail.search.backends.database.fallback import DatabaseSearchBackend
from wagtail.search.index import class_is_indexed
from blog.models import BlogPage
from blog.utils import get_mongo_db

logger = logging.getLogger(__name__)


class MongoSearchResults(BaseSearchResults):
    """Search results from MongoDB"""
    
    def __init__(self, backend, query_compiler, prefetch_related=None):
        super().__init__(backend, query_compiler, prefetch_related)
        self._mongo_results = None
        self._score_field = None

    def _get_mongodb_results(self):
        """Execute search in MongoDB and return results"""
        query_string = self.query_compiler.query.query_string
        if not query_string:
            return [], {}
            
        # Get MongoDB connection
        mongo_db = get_mongo_db()
        if not mongo_db:
            logger.error("Failed to connect to MongoDB")
            return [], {}
            
        # Start timing
        start_time = time.time()
        
        try:
            # Perform text search in MongoDB
            mongo_collection = mongo_db['blog_contents']
            
            # Create text search query
            search_query = {'$text': {'$search': query_string}}
            
            # Get document score
            projection = {'score': {'$meta': 'textScore'}}
            
            # Execute search and sort by relevance
            mongo_results = list(mongo_collection.find(
                search_query,
                projection
            ).sort([('score', {'$meta': 'textScore'})]))
            
            # Extract page IDs and their scores
            page_ids = []
            scores = {}
            
            for doc in mongo_results:
                if 'page_id' in doc:
                    page_id = doc['page_id']
                    page_ids.append(page_id)
                    scores[page_id] = doc['score']
            
            # Log performance
            search_time = time.time() - start_time
            logger.info(f"MongoDB search for '{query_string}' took {search_time:.3f}s. Found {len(page_ids)} results.")
            
            return page_ids, scores
            
        except Exception as e:
            logger.error(f"MongoDB search error: {e}")
            return [], {}
            
    def _do_search(self):
        """Perform the search"""
        model = self.query_compiler.queryset.model
        
        # Only search BlogPage model
        if model is not BlogPage and not issubclass(model, BlogPage):
            return []
            
        # Get MongoDB results
        page_ids, self._score_field = self._get_mongodb_results()
        
        if not page_ids:
            return []
            
        # Get the BlogPage objects
        queryset = BlogPage.objects.filter(id__in=page_ids)
        
        # Apply prefetch_related
        if self.prefetch_related:
            queryset = queryset.prefetch_related(self.prefetch_related)
            
        # Order by MongoDB score (manual sorting since we can't add the score to the queryset)
        results = sorted(
            queryset,
            key=lambda page: self._score_field.get(page.id, 0),
            reverse=True
        )
        
        # Apply limits
        if self.stop is not None:
            results = results[self.start:self.stop]
        else:
            results = results[self.start:]
            
        return results
        
    def _do_count(self):
        """Count the results"""
        page_ids, _ = self._get_mongodb_results()
        return len(page_ids)


class HybridSearchResults(BaseSearchResults):
    """
    Search results from both MongoDB and MySQL
    """
    def __init__(self, backend, query_compiler, database_results=None, mongo_results=None, prefetch_related=None):
        super().__init__(backend, query_compiler, prefetch_related)
        self.database_results = database_results
        self.mongo_results = mongo_results
        
    def _do_search(self):
        # If we only have database results
        if self.mongo_results is None:
            results = list(self.database_results)
        # If we only have mongo results
        elif self.database_results is None:
            results = list(self.mongo_results)
        else:
            # Get results from both sources
            database_results = list(self.database_results)
            mongo_results = list(self.mongo_results)
            
            # Get IDs from database results to avoid duplicates
            database_ids = {obj.id for obj in database_results}
            
            # Add MongoDB results that aren't in database results
            results = database_results + [
                obj for obj in mongo_results if obj.id not in database_ids
            ]
            
        # Apply limits
        if self.stop is not None:
            return results[self.start:self.stop]
        else:
            return results[self.start:]
    
    def _do_count(self):
        # Count in the way that prevents loading all results
        if self.mongo_results is None:
            return self.database_results.count()
        elif self.database_results is None:
            return self.mongo_results.count()
        else:
            # We need to deduplicate when combining results
            database_ids = {obj.id for obj in self.database_results}
            mongo_count = sum(1 for obj in self.mongo_results if obj.id not in database_ids)
            return len(database_ids) + mongo_count


class HybridSearchBackend(BaseSearchBackend):
    """
    A search backend that combines MySQL and MongoDB search
    """
    results_class = HybridSearchResults
    
    def __init__(self, params):
        super().__init__(params)
        self.database_backend = DatabaseSearchBackend(params)
        
    def reset_index(self):
        self.database_backend.reset_index()
        # MongoDB doesn't need to be reset
        
    def add_type(self, model):
        # Only add to database backend if it's not a BlogPage
        if model is not BlogPage and not issubclass(model, BlogPage):
            self.database_backend.add_type(model)
            
    def refresh_index(self):
        self.database_backend.refresh_index()
        # MongoDB doesn't need to be refreshed
        
    def add(self, obj):
        # Only add to database backend if it's not a BlogPage
        if not isinstance(obj, BlogPage):
            self.database_backend.add(obj)
        # BlogPage content is synced to MongoDB separately
        
    def add_bulk(self, model, obj_list):
        # Filter out BlogPage objects
        non_blog_objects = [obj for obj in obj_list if not isinstance(obj, BlogPage)]
        if non_blog_objects:
            self.database_backend.add_bulk(model, non_blog_objects)
        # BlogPage content is synced to MongoDB separately
        
    def delete(self, obj):
        # Only delete from database backend if it's not a BlogPage
        if not isinstance(obj, BlogPage):
            self.database_backend.delete(obj)
        # BlogPage content is removed from MongoDB separately
        
    def search(self, query, model_or_queryset, fields=None, operator=None, order_by_relevance=True):
        """
        Search across multiple models
        """
        start_time = time.time()
        
        # 判断是查询单一模型还是queryset
        if hasattr(model_or_queryset, 'model'):
            model = model_or_queryset.model
            queryset = model_or_queryset
        else:
            model = model_or_queryset
            queryset = model_or_queryset.objects.all()
            
        # 如果不是可索引的模型，返回空结果
        if not class_is_indexed(model):
            return self.results_class(self, None)
            
        # 检查是否是空查询
        if query == "":
            return self.results_class(self, None)
            
        if model is BlogPage or issubclass(model, BlogPage):
            # 对BlogPage使用混合搜索
            # 1. 首先使用数据库后端搜索
            database_results = self.database_backend.search(
                query, queryset, fields, operator, order_by_relevance
            )
            
            # 2. 然后使用MongoDB搜索
            # 为MongoDB搜索创建特殊的查询编译器
            query_compiler = self.database_backend.query_compiler_class(
                queryset, query, fields, operator, order_by_relevance
            )
            mongo_results = MongoSearchResults(self, query_compiler)
            
            # 3. 合并结果
            results = self.results_class(
                self,
                query_compiler,
                database_results=database_results,
                mongo_results=mongo_results
            )
        else:
            # 对其他模型仅使用数据库后端
            results = self.database_backend.search(
                query, queryset, fields, operator, order_by_relevance
            )
        
        search_time = time.time() - start_time
        logger.info(f"Hybrid search for '{query}' took {search_time:.3f}s")
        
        return results
        
    def get_indexed_models(self):
        """
        Get all models that are indexed
        """
        return self.database_backend.get_indexed_models()