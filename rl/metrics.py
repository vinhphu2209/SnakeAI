import numpy as np
from collections import deque

class MetricsTracker:
    def __init__(self, window_size=100):
        """
        Khởi tạo metrics tracker
        
        Args:
            window_size: Kích thước cửa sổ để tính trung bình
        """
        self.scores = []
        self.avg_scores = []
        self.score_window = deque(maxlen=window_size)
        
    def add_score(self, score):
        """
        Thêm điểm số mới
        
        Args:
            score: Điểm số của episode
        """
        self.scores.append(score)
        self.score_window.append(score)
        self.avg_scores.append(np.mean(self.score_window))
        
    def get_stats(self):
        """
        Lấy thống kê về hiệu suất
        
        Returns:
            stats: Dictionary chứa các thống kê
        """
        if not self.scores:
            return {
                'current_score': 0,
                'avg_score': 0,
                'max_score': 0,
                'min_score': 0
            }
            
        return {
            'current_score': self.scores[-1],
            'avg_score': np.mean(self.score_window),
            'max_score': max(self.scores),
            'min_score': min(self.scores)
        }
        
    def reset(self):
        """Reset tất cả metrics"""
        self.scores = []
        self.avg_scores = []
        self.score_window.clear() 