from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from .settings import (
    MONGO_CONNECTION_STRING,
    DB_NAME,
    SCORES_COLLECTION,
    SETTINGS_COLLECTION,
    AGENTS_COLLECTION
)

class GameDB:
    def __init__(self):
        # Kết nối đến MongoDB
        self.client = MongoClient(MONGO_CONNECTION_STRING)
        self.db = self.client[DB_NAME]
        
        # Khởi tạo collections
        self.scores = self.db[SCORES_COLLECTION]
        self.settings = self.db[SETTINGS_COLLECTION]
        self.agents = self.db[AGENTS_COLLECTION]
        
        # Tạo indexes cho scores collection
        self.scores.create_index([("player_name", 1)])
        self.scores.create_index([("score", -1)])
        self.scores.create_index([("timestamp", -1)])

    def save_score(self, score, agent_type, metadata=None):
        """Lưu điểm số với metadata tùy chọn"""
        document = {
            'score': score,
            'agent_type': agent_type,
            'date': datetime.now(),
            'metadata': metadata or {}
        }
        return self.scores.insert_one(document)

    def get_top_scores(self, limit=10, agent_type=None):
        """Lấy top điểm cao, có thể lọc theo loại agent"""
        query = {'agent_type': agent_type} if agent_type else {}
        return list(self.scores.find(query)
                   .sort('score', -1)
                   .limit(limit))

    def get_agent_stats(self, agent_type):
        """Lấy thống kê của một loại agent"""
        pipeline = [
            {'$match': {'agent_type': agent_type}},
            {'$group': {
                '_id': None,
                'avg_score': {'$avg': '$score'},
                'max_score': {'$max': '$score'},
                'min_score': {'$min': '$score'},
                'total_games': {'$sum': 1}
            }}
        ]
        return list(self.scores.aggregate(pipeline))

    def save_agent_settings(self, agent_type, settings):
        """Lưu cài đặt của agent"""
        document = {
            'agent_type': agent_type,
            'settings': settings,
            'last_updated': datetime.now()
        }
        self.agents.update_one(
            {'agent_type': agent_type},
            {'$set': document},
            upsert=True
        )

    def get_agent_settings(self, agent_type):
        """Lấy cài đặt của agent"""
        return self.agents.find_one({'agent_type': agent_type})

    def delete_score(self, score_id):
        """Xóa điểm theo ID"""
        try:
            # Chuyển đổi string ID thành ObjectId nếu cần
            if isinstance(score_id, str):
                score_id = ObjectId(score_id)
            result = self.scores.delete_one({'_id': score_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Lỗi khi xóa điểm: {e}")
            return False

    def close(self):
        """Đóng kết nối database"""
        self.client.close() 