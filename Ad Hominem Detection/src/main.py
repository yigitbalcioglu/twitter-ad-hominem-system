"""
Ana Interface - Kullanıcı arayüzü ve model çalıştırma sistemi
"""
import os
import sys
import torch
from typing import Optional, Dict, List

# Proje root'unu sys.path'e ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config.config import ConfigFactory
from src.data.data_handler import DataHandler
from src.models import ModelFactory, ModelRegistry
from src.models.ml_models import MLEnsemble
from src.training.trainer import ModelTrainer
from src.training.evaluator import ModelEvaluator
from src.utils.losses import FocalLoss


class AdHominemDetectionSystem:
    """
    Ad Hominem Tespit Sistemi - Ana Sınıf
    
    Bu sınıf tüm sistemi yönetir ve kullanıcıya kolay bir arayüz sunar
    """
    
    def __init__(self, dataset_path: str = "dataset.csv"):
        """
        Args:
            dataset_path: Dataset dosya yolu
        """
        self.dataset_path = dataset_path
        self.registry = ModelRegistry()
        
        print("\n" + "="*80)
        print("AD HOMİNEM TESPİT SİSTEMİ".center(80))
        print("="*80)
        print("Türkçe Metinlerde Ad Hominem Saldırı Tespiti")
        print("Deep Learning & Machine Learning Modelleri")
        print("="*80 + "\n")
    
    def list_available_models(self):
        """Mevcut tüm modelleri listele"""
        ModelFactory.list_models()
    
    def train_deep_learning_model(
        self,
        model_type: str,
        use_roberta: bool = False,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        learning_rate: Optional[float] = None,
        use_focal_loss: bool = False,
        **kwargs
    ):
        """
        Deep Learning modeli eğit
        
        Args:
            model_type: Model tipi ('bigru', 'bilstm', 'birnn', 'cnn', 'mlp')
            use_roberta: RoBERTa kullan (False ise BERT)
            epochs: Epoch sayısı
            batch_size: Batch boyutu
            learning_rate: Learning rate
            use_focal_loss: Focal loss kullan
            **kwargs: Ek parametreler
        """
        print(f"\n{'='*80}")
        print(f"{model_type.upper()} MODELİ EĞİTİLİYOR".center(80))
        print(f"{'='*80}\n")
        
        # Konfigürasyon oluştur
        config_kwargs = {
            'use_roberta': use_roberta,
            'dataset_path': self.dataset_path,
            **kwargs
        }
        
        if epochs is not None:
            config_kwargs['epochs'] = epochs
        if batch_size is not None:
            config_kwargs['batch_size'] = batch_size
        if learning_rate is not None:
            config_kwargs['learning_rate'] = learning_rate
        
        config = ConfigFactory.create_config(model_type, **config_kwargs)
        
        # Veri yükle
        print("📊 Veri yükleniyor...")
        data_handler = DataHandler(config)
        texts, labels = data_handler.load_data()
        
        # Train-test split
        train_texts, test_texts, train_labels, test_labels = data_handler.split_data(texts, labels)
        
        # DataLoader'lar oluştur
        train_loader, test_loader = data_handler.create_data_loaders(
            train_texts, test_texts, train_labels, test_labels
        )
        
        # Model oluştur
        print(f"\n🤖 Model oluşturuluyor...")
        model = ModelFactory.create_model(model_type, config)
        model.summary()
        
        # Loss function
        loss_fn = FocalLoss(gamma=2.0) if use_focal_loss else None
        
        # Trainer oluştur
        trainer = ModelTrainer(model, config, loss_fn=loss_fn)
        
        # Eğitim
        history = trainer.train(train_loader, test_loader)
        
        # En iyi modeli yükle
        trainer.load_best_model()
        
        # Değerlendirme
        evaluator = ModelEvaluator(model, config)
        metrics = evaluator.evaluate(test_loader)
        
        # Görselleştirmeler
        evaluator.plot_confusion_matrix(test_loader)
        evaluator.plot_training_history(history)
        
        # Registry'e kaydet
        model_name = f"{model_type.upper()}_{'RoBERTa' if use_roberta else 'BERT'}"
        self.registry.register(model_name, model, config, metrics)
        
        print(f"\n✅ {model_name} eğitimi tamamlandı!")
        
        return model, metrics, history
    
    def train_machine_learning_models(
        self,
        use_bert: bool = True,
        use_roberta: bool = True,
        use_tfidf: bool = True,
        models_to_train: Optional[List[str]] = None
    ):
        """
        Machine Learning modellerini eğit
        
        Args:
            use_bert: BERT embeddings kullan
            use_roberta: RoBERTa embeddings kullan
            use_tfidf: TF-IDF özellikleri kullan
            models_to_train: Eğitilecek modeller (None ise tümü)
        """
        print(f"\n{'='*80}")
        print("MACHINE LEARNING MODELLERİ EĞİTİLİYOR".center(80))
        print(f"{'='*80}\n")
        
        # Konfigürasyon
        config = ConfigFactory.create_config('ml', dataset_path=self.dataset_path)
        
        # Veri yükle
        print("📊 Veri yükleniyor...")
        data_handler = DataHandler(config)
        texts, labels = data_handler.load_data()
        
        # Train-test split
        train_texts, test_texts, train_labels, test_labels = data_handler.split_data(texts, labels)
        
        # Özellik çıkarma
        print("\n🔧 Özellikler hazırlanıyor...")
        train_features, test_features = data_handler.prepare_ml_features(
            train_texts, test_texts,
            use_bert=use_bert,
            use_roberta=use_roberta,
            use_tfidf=use_tfidf
        )
        
        # ML Ensemble oluştur ve eğit
        ml_ensemble = MLEnsemble(config)
        
        # Eğitim
        ml_ensemble.train_all(train_features, train_labels)
        
        # Değerlendirme
        all_metrics = ml_ensemble.evaluate_all(test_features, test_labels)
        
        # En iyi modeli bul
        best_model_name, best_model, best_score = ml_ensemble.get_best_model(
            test_features, test_labels, metric='f1'
        )
        
        # Registry'e kaydet
        for model_name, metrics in all_metrics.items():
            full_name = f"ML_{model_name.replace(' ', '_')}"
            self.registry.register(full_name, ml_ensemble.models[model_name], config, metrics)
        
        print(f"\n✅ Machine Learning modelleri eğitimi tamamlandı!")
        
        return ml_ensemble, all_metrics
    
    def train_all_models(self, quick_mode: bool = False):
        """
        Tüm modelleri eğit
        
        Args:
            quick_mode: Hızlı mod (daha az epoch)
        """
        print(f"\n{'='*80}")
        print("TÜM MODELLER EĞİTİLİYOR".center(80))
        print(f"{'='*80}\n")
        
        epochs = 2 if quick_mode else 5
        
        # Deep Learning modelleri
        dl_models = ['bigru', 'bilstm', 'birnn', 'cnn', 'mlp']
        
        for model_type in dl_models:
            try:
                print(f"\n{'='*80}")
                print(f"🎯 {model_type.upper()} modeli eğitiliyor...")
                print(f"{'='*80}")
                
                self.train_deep_learning_model(
                    model_type,
                    use_roberta=True,
                    epochs=epochs,
                    use_focal_loss=True
                )
            except Exception as e:
                print(f"❌ {model_type.upper()} eğitiminde hata: {e}")
                continue
        
        # Machine Learning modelleri
        try:
            print(f"\n{'='*80}")
            print("🎯 Machine Learning modelleri eğitiliyor...")
            print(f"{'='*80}")
            
            self.train_machine_learning_models()
        except Exception as e:
            print(f"❌ ML modelleri eğitiminde hata: {e}")
        
        # Tüm sonuçları karşılaştır
        self.compare_all_models()
        
        print(f"\n{'='*80}")
        print("✅ TÜM MODELLERİN EĞİTİMİ TAMAMLANDI!".center(80))
        print(f"{'='*80}\n")
    
    def compare_all_models(self):
        """Tüm eğitilmiş modelleri karşılaştır"""
        self.registry.compare_all()
    
    def get_best_model(self, metric: str = 'f1'):
        """En iyi modeli getir"""
        return self.registry.get_best_model(metric)
    
    def predict_text(self, text: str, model_name: Optional[str] = None):
        """
        Tek bir metin için tahmin yap
        
        Args:
            text: Tahmin yapılacak metin
            model_name: Model adı (None ise en iyi model)
        """
        if model_name is None:
            model_name, model, _ = self.get_best_model()
        else:
            model = self.registry.get_model(model_name)
        
        config = self.registry.get_config(model_name)
        
        # Data handler
        data_handler = DataHandler(config)
        data_handler.create_tokenizer()
        
        # Tokenize
        input_ids, attention_mask = data_handler.tokenize_texts([text])
        
        # Predict
        model.eval()
        with torch.no_grad():
            input_ids = input_ids.to(config.device)
            attention_mask = attention_mask.to(config.device)
            
            outputs = model(input_ids, attention_mask)
            probs = torch.softmax(outputs, dim=1)
            pred = torch.argmax(probs, dim=1)
        
        result = {
            'text': text,
            'prediction': 'Ad Hominem' if pred.item() == 1 else 'Not Ad Hominem',
            'confidence': probs[0][pred.item()].item(),
            'probabilities': {
                'Not Ad Hominem': probs[0][0].item(),
                'Ad Hominem': probs[0][1].item()
            }
        }
        
        return result


def interactive_menu():
    """İnteraktif menü"""
    system = AdHominemDetectionSystem()
    
    while True:
        print("\n" + "="*80)
        print("ANA MENÜ".center(80))
        print("="*80)
        print("\n1. Mevcut modelleri listele")
        print("2. Deep Learning modeli eğit")
        print("3. Machine Learning modelleri eğit")
        print("4. Tüm modelleri eğit")
        print("5. Eğitilmiş modelleri karşılaştır")
        print("6. Metin tahmin et")
        print("0. Çıkış")
        
        choice = input("\nSeçiminiz: ").strip()
        
        if choice == '0':
            print("\n👋 Güle güle!")
            break
        
        elif choice == '1':
            system.list_available_models()
        
        elif choice == '2':
            print("\nDeep Learning Model Tipleri:")
            print("1. BiGRU")
            print("2. BiLSTM")
            print("3. BiRNN")
            print("4. CNN")
            print("5. MLP")
            
            model_choice = input("Model seçin (1-5): ").strip()
            model_map = {'1': 'bigru', '2': 'bilstm', '3': 'birnn', '4': 'cnn', '5': 'mlp'}
            
            if model_choice in model_map:
                use_roberta = input("RoBERTa kullan? (e/h): ").strip().lower() == 'e'
                system.train_deep_learning_model(model_map[model_choice], use_roberta=use_roberta)
        
        elif choice == '3':
            system.train_machine_learning_models()
        
        elif choice == '4':
            quick = input("Hızlı mod? (e/h): ").strip().lower() == 'e'
            system.train_all_models(quick_mode=quick)
        
        elif choice == '5':
            system.compare_all_models()
        
        elif choice == '6':
            text = input("\nTahmin edilecek metni girin: ").strip()
            if text:
                result = system.predict_text(text)
                print(f"\n{'='*60}")
                print(f"Tahmin: {result['prediction']}")
                print(f"Güven: {result['confidence']:.4f}")
                print(f"{'='*60}")


if __name__ == "__main__":
    # İnteraktif menüyü başlat
    interactive_menu()
