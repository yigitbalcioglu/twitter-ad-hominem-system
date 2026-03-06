"""
Metrik ve Değerlendirme Fonksiyonları
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from typing import Dict, Tuple, Optional
import torch


class MetricsCalculator:
    """Değerlendirme metrikleri hesaplayıcı"""
    
    @staticmethod
    def calculate_metrics(y_true, y_pred, y_pred_proba=None, average='binary') -> Dict[str, float]:
        """
        Tüm metrikleri hesapla
        
        Args:
            y_true: Gerçek etiketler
            y_pred: Tahmin edilen etiketler
            y_pred_proba: Tahmin olasılıkları (ROC-AUC için)
            average: 'binary', 'micro', 'macro', 'weighted'
            
        Returns:
            Metrikler dictionary
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
            'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
            'f1': f1_score(y_true, y_pred, average=average, zero_division=0),
        }
        
        # ROC-AUC hesapla (eğer olasılıklar verilmişse)
        if y_pred_proba is not None:
            try:
                if average == 'binary':
                    # Binary classification için pozitif sınıf olasılığı
                    if len(y_pred_proba.shape) > 1 and y_pred_proba.shape[1] > 1:
                        y_pred_proba = y_pred_proba[:, 1]
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
                else:
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba, 
                                                        average=average, 
                                                        multi_class='ovr')
            except Exception as e:
                print(f"ROC-AUC hesaplanamadı: {e}")
                metrics['roc_auc'] = 0.0
        
        return metrics
    
    @staticmethod
    def get_confusion_matrix(y_true, y_pred) -> np.ndarray:
        """Confusion matrix hesapla"""
        return confusion_matrix(y_true, y_pred)
    
    @staticmethod
    def get_classification_report(y_true, y_pred, target_names=None) -> str:
        """Detaylı sınıflandırma raporu"""
        return classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
    
    @staticmethod
    def calculate_class_wise_metrics(y_true, y_pred) -> Dict[int, Dict[str, float]]:
        """Her sınıf için ayrı metrikler hesapla"""
        unique_classes = np.unique(y_true)
        class_metrics = {}
        
        for cls in unique_classes:
            y_true_binary = (y_true == cls).astype(int)
            y_pred_binary = (y_pred == cls).astype(int)
            
            class_metrics[int(cls)] = {
                'precision': precision_score(y_true_binary, y_pred_binary, zero_division=0),
                'recall': recall_score(y_true_binary, y_pred_binary, zero_division=0),
                'f1': f1_score(y_true_binary, y_pred_binary, zero_division=0),
            }
        
        return class_metrics


class EarlyStopping:
    """Early stopping implementasyonu"""
    
    def __init__(self, patience=3, min_delta=0.0, mode='min', verbose=True):
        """
        Args:
            patience: Kaç epoch boyunca iyileşme olmazsa dur
            min_delta: Minimum iyileşme miktarı
            mode: 'min' (loss için) veya 'max' (accuracy için)
            verbose: İlerlemeyi yazdır
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.verbose = verbose
        
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.best_epoch = 0
        
        if mode == 'min':
            self.monitor_op = lambda x, y: x < y - min_delta
            self.best_score = float('inf')
        else:
            self.monitor_op = lambda x, y: x > y + min_delta
            self.best_score = float('-inf')
    
    def __call__(self, score, epoch):
        """
        Early stopping kontrolü yap
        
        Args:
            score: İzlenen metrik değeri
            epoch: Mevcut epoch
            
        Returns:
            True ise eğitimi durdur
        """
        if self.monitor_op(score, self.best_score):
            self.best_score = score
            self.counter = 0
            self.best_epoch = epoch
            if self.verbose:
                print(f'✓ İyileşme: En iyi skor = {score:.4f}')
            return False
        else:
            self.counter += 1
            if self.verbose:
                print(f'⚠ İyileşme yok ({self.counter}/{self.patience})')
            
            if self.counter >= self.patience:
                self.early_stop = True
                if self.verbose:
                    print(f'⛔ Early stopping! En iyi epoch: {self.best_epoch}, skor: {self.best_score:.4f}')
                return True
            return False
    
    def reset(self):
        """Early stopping durumunu sıfırla"""
        self.counter = 0
        self.early_stop = False
        if self.mode == 'min':
            self.best_score = float('inf')
        else:
            self.best_score = float('-inf')


class AverageMeter:
    """Ortalama metrik takibi için yardımcı sınıf"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Değerleri sıfırla"""
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        """
        Değeri güncelle
        
        Args:
            val: Yeni değer
            n: Değer sayısı
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count if self.count > 0 else 0


def calculate_batch_metrics(outputs, targets, loss_value=None):
    """
    Batch için metrikleri hesapla (PyTorch tensors için)
    
    Args:
        outputs: Model çıktısı (logits)
        targets: Gerçek etiketler
        loss_value: Loss değeri (opsiyonel)
        
    Returns:
        Metrikler dictionary
    """
    with torch.no_grad():
        # Predictions
        _, preds = torch.max(outputs, dim=1)
        
        # Accuracy
        correct = (preds == targets).sum().item()
        total = targets.size(0)
        accuracy = correct / total
        
        metrics = {'accuracy': accuracy}
        
        if loss_value is not None:
            metrics['loss'] = loss_value
        
        return metrics


def print_metrics(metrics: Dict[str, float], title: str = "Metrics"):
    """
    Metrikleri formatlı şekilde yazdır
    
    Args:
        metrics: Metrikler dictionary
        title: Başlık
    """
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")
    
    for metric_name, value in metrics.items():
        print(f"{metric_name.upper():.<30} {value:.4f}")
    
    print(f"{'='*60}\n")
