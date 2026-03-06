"""
Örnek Kullanım Scripti
Ad Hominem Detection System
"""

import sys
import os

# Proje root'unu path'e ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import AdHominemDetectionSystem


def example_1_single_model():
    """Örnek 1: Tek bir model eğit"""
    print("\n" + "="*80)
    print("ÖRNEK 1: TEK BİR MODEL EĞİTİMİ".center(80))
    print("="*80 + "\n")
    
    # Sistem oluştur
    system = AdHominemDetectionSystem(dataset_path="dataset.csv")
    
    # BiGRU modelini RoBERTa ile eğit
    model, metrics, history = system.train_deep_learning_model(
        model_type='bigru',
        use_roberta=True,
        epochs=3,
        batch_size=96,
        use_focal_loss=True
    )
    
    print("\n✅ Örnek 1 tamamlandı!")
    print(f"   Model: BiGRU + RoBERTa")
    print(f"   F1-Score: {metrics['f1']:.4f}")


def example_2_ml_models():
    """Örnek 2: Machine Learning modellerini eğit"""
    print("\n" + "="*80)
    print("ÖRNEK 2: MACHINE LEARNING MODELLERİ".center(80))
    print("="*80 + "\n")
    
    system = AdHominemDetectionSystem(dataset_path="dataset.csv")
    
    # Tüm ML modellerini eğit
    ml_ensemble, all_metrics = system.train_machine_learning_models(
        use_bert=True,
        use_roberta=True,
        use_tfidf=True
    )
    
    print("\n✅ Örnek 2 tamamlandı!")


def example_3_compare_models():
    """Örnek 3: Birden fazla modeli eğit ve karşılaştır"""
    print("\n" + "="*80)
    print("ÖRNEK 3: MODELLERİ KARŞILAŞTIR".center(80))
    print("="*80 + "\n")
    
    system = AdHominemDetectionSystem(dataset_path="dataset.csv")
    
    # Farklı modelleri eğit
    models_to_train = ['bigru', 'bilstm', 'cnn']
    
    for model_type in models_to_train:
        print(f"\n🎯 {model_type.upper()} eğitiliyor...")
        try:
            system.train_deep_learning_model(
                model_type=model_type,
                use_roberta=True,
                epochs=2,  # Hızlı test için
                use_focal_loss=True
            )
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    # Tüm modelleri karşılaştır
    system.compare_all_models()
    
    # En iyi modeli bul
    best_name, best_model, best_metrics = system.get_best_model(metric='f1')
    
    print(f"\n🏆 En İyi Model: {best_name}")
    print(f"   F1-Score: {best_metrics['f1']:.4f}")
    
    print("\n✅ Örnek 3 tamamlandı!")


def example_4_predict():
    """Örnek 4: Eğitilmiş model ile tahmin yap"""
    print("\n" + "="*80)
    print("ÖRNEK 4: TAHMİN YAPMA".center(80))
    print("="*80 + "\n")
    
    system = AdHominemDetectionSystem(dataset_path="dataset.csv")
    
    # Önce bir model eğit (kısa)
    print("📚 Model eğitiliyor (bu biraz zaman alabilir)...")
    system.train_deep_learning_model(
        model_type='mlp',  # MLP daha hızlı
        use_roberta=False,  # BERT ile daha hızlı
        epochs=2,
        batch_size=64
    )
    
    # Test metinleri
    test_texts = [
        "Bu argüman mantıklı ve tutarlı görünüyor.",
        "Sen hiçbir şey bilmiyorsun, sussan daha iyi.",
        "Veriler gösteriyor ki bu yöntem daha etkili.",
        "Senin gibi cahil biri bunu anlayamaz.",
    ]
    
    print("\n📝 Tahminler yapılıyor...\n")
    
    for text in test_texts:
        result = system.predict_text(text)
        
        print(f"{'='*60}")
        print(f"Metin: {text}")
        print(f"Tahmin: {result['prediction']}")
        print(f"Güven: {result['confidence']:.4f}")
        print(f"Olasılıklar:")
        for label, prob in result['probabilities'].items():
            print(f"  {label}: {prob:.4f}")
        print()
    
    print("✅ Örnek 4 tamamlandı!")


def example_5_custom_config():
    """Örnek 5: Özel konfigürasyon ile model eğitimi"""
    print("\n" + "="*80)
    print("ÖRNEK 5: ÖZEL KONFİGÜRASYON".center(80))
    print("="*80 + "\n")
    
    from src.config.config import BiGRUConfig
    from src.models import ModelFactory
    from src.data.data_handler import DataHandler
    from src.training.trainer import ModelTrainer
    from src.training.evaluator import ModelEvaluator
    from src.utils.losses import FocalLoss
    
    # Özel konfigürasyon
    config = BiGRUConfig(
        dataset_path="dataset.csv",
        use_roberta=True,
        hidden_size=256,  # Daha büyük
        num_layers=2,     # 2 katman
        dropout_rate=0.4,
        epochs=3,
        batch_size=64,
        learning_rate=1e-5  # Daha düşük LR
    )
    
    print("⚙️ Özel Konfigürasyon:")
    print(f"  Hidden Size: {config.hidden_size}")
    print(f"  Num Layers: {config.num_layers}")
    print(f"  Dropout: {config.dropout_rate}")
    print(f"  Learning Rate: {config.learning_rate}")
    print()
    
    # Veri hazırla
    data_handler = DataHandler(config)
    texts, labels = data_handler.load_data()
    train_texts, test_texts, train_labels, test_labels = data_handler.split_data(texts, labels)
    train_loader, test_loader = data_handler.create_data_loaders(
        train_texts, test_texts, train_labels, test_labels
    )
    
    # Model oluştur
    model = ModelFactory.create_model('bigru', config)
    model.summary()
    
    # Focal Loss ile eğit
    loss_fn = FocalLoss(gamma=2.0)
    trainer = ModelTrainer(model, config, loss_fn=loss_fn)
    
    # Eğitim
    history = trainer.train(train_loader, test_loader)
    
    # Değerlendirme
    trainer.load_best_model()
    evaluator = ModelEvaluator(model, config)
    metrics = evaluator.evaluate(test_loader)
    
    print("\n✅ Örnek 5 tamamlandı!")


def main():
    """Ana fonksiyon"""
    print("\n" + "="*80)
    print("AD HOMİNEM TESPİT SİSTEMİ - ÖRNEK KULLANIMLAR".center(80))
    print("="*80)
    
    examples = {
        '1': ('Tek bir model eğit (BiGRU)', example_1_single_model),
        '2': ('Machine Learning modelleri', example_2_ml_models),
        '3': ('Modelleri karşılaştır', example_3_compare_models),
        '4': ('Tahmin yap', example_4_predict),
        '5': ('Özel konfigürasyon', example_5_custom_config),
        'all': ('Tüm örnekleri çalıştır', None),
    }
    
    print("\nÖrnek Scriptler:")
    for key, (desc, _) in examples.items():
        if key != 'all':
            print(f"  {key}. {desc}")
    print(f"  all. Tüm örnekleri çalıştır")
    print("  0. Çıkış")
    
    choice = input("\nSeçiminiz: ").strip()
    
    if choice == '0':
        print("\n👋 Güle güle!")
        return
    
    elif choice == 'all':
        for key, (_, func) in examples.items():
            if key != 'all' and func:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Örnek {key} çalıştırılırken hata: {e}")
                input("\nDevam etmek için Enter'a basın...")
    
    elif choice in examples and examples[choice][1]:
        try:
            examples[choice][1]()
        except Exception as e:
            print(f"\n❌ Hata: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    main()
