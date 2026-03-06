"""
Custom Loss Functions
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """
    Focal Loss - Dengesiz veri setleri için geliştirilmiş loss fonksiyonu
    
    Paper: "Focal Loss for Dense Object Detection"
    https://arxiv.org/abs/1708.02002
    """
    
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        """
        Args:
            alpha: Her sınıf için ağırlık faktörü (Tensor veya None)
            gamma: Odaklama parametresi (varsayılan: 2.0)
            reduction: 'mean', 'sum' veya 'none'
        """
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        """
        Args:
            inputs: Model çıktısı (logits) - shape: [batch_size, num_classes]
            targets: Gerçek etiketler - shape: [batch_size]
            
        Returns:
            Focal loss değeri
        """
        # Log softmax uygula
        log_softmax = F.log_softmax(inputs, dim=1)
        
        # Cross entropy loss hesapla
        ce_loss = F.nll_loss(log_softmax, targets, weight=self.alpha, reduction='none')

        # Hedef sınıf için olasılıkları al
        p_t = torch.exp(-ce_loss)

        # Odaklama terimini uygula
        focal_loss = (1 - p_t) ** self.gamma * ce_loss

        # Reduction uygula
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss


class LabelSmoothingLoss(nn.Module):
    """
    Label Smoothing Loss - Overfitting'i azaltmak için
    """
    
    def __init__(self, num_classes, smoothing=0.1, reduction='mean'):
        """
        Args:
            num_classes: Sınıf sayısı
            smoothing: Smoothing faktörü (0-1 arası)
            reduction: 'mean', 'sum' veya 'none'
        """
        super(LabelSmoothingLoss, self).__init__()
        self.num_classes = num_classes
        self.smoothing = smoothing
        self.reduction = reduction
        self.confidence = 1.0 - smoothing

    def forward(self, inputs, targets):
        """
        Args:
            inputs: Model çıktısı (logits) - shape: [batch_size, num_classes]
            targets: Gerçek etiketler - shape: [batch_size]
            
        Returns:
            Label smoothing loss değeri
        """
        log_probs = F.log_softmax(inputs, dim=1)
        
        # One-hot encoding oluştur ve smoothing uygula
        with torch.no_grad():
            true_dist = torch.zeros_like(log_probs)
            true_dist.fill_(self.smoothing / (self.num_classes - 1))
            true_dist.scatter_(1, targets.unsqueeze(1), self.confidence)
        
        loss = -torch.sum(true_dist * log_probs, dim=1)
        
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss


class WeightedCrossEntropyLoss(nn.Module):
    """
    Weighted Cross Entropy Loss - Dengesiz veri setleri için
    """
    
    def __init__(self, class_weights=None, reduction='mean'):
        """
        Args:
            class_weights: Her sınıf için ağırlık (Tensor veya None)
            reduction: 'mean', 'sum' veya 'none'
        """
        super(WeightedCrossEntropyLoss, self).__init__()
        self.class_weights = class_weights
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        """
        Args:
            inputs: Model çıktısı (logits)
            targets: Gerçek etiketler
            
        Returns:
            Weighted cross entropy loss
        """
        return F.cross_entropy(inputs, targets, weight=self.class_weights, reduction=self.reduction)


def get_loss_function(loss_type='cross_entropy', **kwargs):
    """
    Loss fonksiyonu factory
    
    Args:
        loss_type: 'cross_entropy', 'focal', 'label_smoothing', 'weighted_ce'
        **kwargs: Loss fonksiyonuna özel parametreler
        
    Returns:
        Loss fonksiyonu
    """
    loss_functions = {
        'cross_entropy': nn.CrossEntropyLoss,
        'focal': FocalLoss,
        'label_smoothing': LabelSmoothingLoss,
        'weighted_ce': WeightedCrossEntropyLoss,
    }
    
    if loss_type not in loss_functions:
        raise ValueError(
            f"Bilinmeyen loss tipi: {loss_type}. "
            f"Geçerli tipler: {list(loss_functions.keys())}"
        )
    
    return loss_functions[loss_type](**kwargs)
