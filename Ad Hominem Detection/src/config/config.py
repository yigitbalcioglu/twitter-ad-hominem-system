"""
Konfigürasyon Yönetimi
Tüm model hiperparametreleri ve sistem ayarları
"""
import torch
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ModelConfig:
    """Genel model konfigürasyonu"""
    # Cihaz ayarları
    device: torch.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Veri ayarları
    dataset_path: str = "dataset.csv"
    max_length: int = 128
    batch_size: int = 48
    test_size: float = 0.2
    random_state: int = 42
    
    # Eğitim ayarları
    epochs: int = 5
    learning_rate: float = 2e-5
    dropout_rate: float = 0.3
    weight_decay: float = 0.01
    warmup_steps: int = 0
    
    # Model kaydetme
    checkpoint_dir: str = "checkpoints"
    save_best_only: bool = True
    
    # Early stopping
    early_stopping_patience: int = 3
    
    def __post_init__(self):
        """Otomatik olarak checkpoint dizini oluştur"""
        import os
        os.makedirs(self.checkpoint_dir, exist_ok=True)


@dataclass
class BERTModelConfig(ModelConfig):
    """BERT tabanlı modeller için özel konfigürasyon"""
    # BERT ayarları
    bert_model_name: str = "dbmdz/bert-base-turkish-cased"
    roberta_model_name: str = "TURKCELL/roberta-base-turkish-uncased"
    freeze_bert: bool = False
    use_roberta: bool = False  # True ise RoBERTa, False ise BERT kullan
    
    @property
    def transformer_model_name(self) -> str:
        """Kullanılacak transformer modelini döndür"""
        return self.roberta_model_name if self.use_roberta else self.bert_model_name


@dataclass
class BiGRUConfig(BERTModelConfig):
    """BiGRU modeli için özel konfigürasyon"""
    model_type: str = "BiGRU"
    hidden_size: int = 128
    num_layers: int = 1
    bidirectional: bool = True
    batch_size: int = 96
    epochs: int = 5


@dataclass
class BiLSTMConfig(BERTModelConfig):
    """BiLSTM modeli için özel konfigürasyon"""
    model_type: str = "BiLSTM"
    hidden_size: int = 128
    num_layers: int = 1
    bidirectional: bool = True
    batch_size: int = 96
    epochs: int = 5


@dataclass
class BiRNNConfig(BERTModelConfig):
    """BiRNN modeli için özel konfigürasyon"""
    model_type: str = "BiRNN"
    hidden_size: int = 128
    num_layers: int = 1
    bidirectional: bool = True
    batch_size: int = 96
    epochs: int = 5


@dataclass
class CNNConfig(BERTModelConfig):
    """CNN modeli için özel konfigürasyon"""
    model_type: str = "CNN"
    num_filters: int = 128
    kernel_sizes: tuple = (3, 4, 5)
    batch_size: int = 48
    epochs: int = 4


@dataclass
class MLPConfig(BERTModelConfig):
    """MLP modeli için özel konfigürasyon"""
    model_type: str = "MLP"
    hidden_dims: tuple = (512, 256, 128)
    batch_size: int = 64
    epochs: int = 5


@dataclass
class MLConfig(ModelConfig):
    """Geleneksel Machine Learning modelleri için konfigürasyon"""
    model_type: str = "ML"
    
    # Embedding yöntemleri
    use_bert_embeddings: bool = True
    use_roberta_embeddings: bool = True
    use_tfidf_embeddings: bool = True
    
    # TF-IDF ayarları
    max_features: int = 5000
    ngram_range: tuple = (1, 2)
    
    # ML model ayarları
    ml_models: Dict[str, Any] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.ml_models is None:
            from sklearn.linear_model import LogisticRegression
            from sklearn.svm import SVC
            from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
            from sklearn.naive_bayes import MultinomialNB
            
            self.ml_models = {
                'Logistic Regression': LogisticRegression(max_iter=1000, random_state=self.random_state),
                'SVM': SVC(kernel='rbf', random_state=self.random_state),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=self.random_state),
                'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=self.random_state),
                'Naive Bayes': MultinomialNB()
            }


class ConfigFactory:
    """Konfigürasyon nesnelerini oluşturan factory class"""
    
    _config_mapping = {
        'bigru': BiGRUConfig,
        'bilstm': BiLSTMConfig,
        'birnn': BiRNNConfig,
        'cnn': CNNConfig,
        'mlp': MLPConfig,
        'ml': MLConfig,
    }
    
    @classmethod
    def create_config(cls, model_type: str, **kwargs) -> ModelConfig:
        """
        Verilen model tipi için uygun konfigürasyon nesnesi oluştur
        
        Args:
            model_type: Model tipi ('bigru', 'bilstm', vb.)
            **kwargs: Konfigürasyon parametrelerini override et
            
        Returns:
            İlgili konfigürasyon nesnesi
        """
        model_type = model_type.lower()
        
        if model_type not in cls._config_mapping:
            raise ValueError(
                f"Bilinmeyen model tipi: {model_type}. "
                f"Geçerli tipler: {list(cls._config_mapping.keys())}"
            )
        
        config_class = cls._config_mapping[model_type]
        return config_class(**kwargs)
    
    @classmethod
    def get_available_models(cls) -> list:
        """Mevcut tüm model tiplerini döndür"""
        return list(cls._config_mapping.keys())


# Varsayılan konfigürasyonlar
DEFAULT_CONFIG = ModelConfig()
