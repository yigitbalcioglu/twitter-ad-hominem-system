"""
Quick Start Guide
Hızlı başlangıç için temel kullanım örnekleri
"""

import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import AdHominemDetectionSystem


def quickstart():
    """Hızlı başlangıç - En basit kullanım"""
    
    print("\n" + "="*80)
    print("HİZLİ BAŞLANGIÇ - AD HOMİNEM TESPİT SİSTEMİ".center(80))
    print("="*80 + "\n")
    
    # 1. Sistem oluştur
    print("1️⃣ Sistem başlatılıyor...")
    system = AdHominemDetectionSystem(dataset_path="dataset.csv")
    
    # 2. Bir model eğit (hızlı test için MLP, 2 epoch)
    print("\n2️⃣ Model eğitiliyor (MLP + BERT, 2 epoch)...")
    print("   ⚠️ Bu işlem birkaç dakika sürebilir...\n")
    
    model, metrics, history = system.train_deep_learning_model(
        model_type='mlp',
        use_roberta=False,  # BERT daha hızlı
        epochs=2,
        batch_size=64
    )
    
    # 3. Sonuçları göster
    print("\n3️⃣ Sonuçlar:")
    print(f"   Accuracy: {metrics['accuracy']:.4f}")
    print(f"   F1-Score: {metrics['f1']:.4f}")
    
    # 4. Örnek tahminler
    print("\n4️⃣ Örnek tahminler yapılıyor...\n")
    
    test_texts = [
        "Bu argüman mantıklı ve veriye dayalı.",
        "Sen hiçbir şey bilmiyorsun, cahil!",
    ]
    
    for text in test_texts:
        result = system.predict_text(text)
        print(f"📝 Metin: {text}")
        print(f"   ➡️ Tahmin: {result['prediction']}")
        print(f"   ➡️ Güven: {result['confidence']:.2%}\n")
    
    print("="*80)
    print("✅ BAŞARILI! Sistem hazır.".center(80))
    print("="*80)
    print("\nBir sonraki adımlar:")
    print("  • Daha fazla model eğitmek için: python src/main.py")
    print("  • Örnekleri görmek için: python run_example.py")
    print("  • Tüm modelleri eğitmek için: system.train_all_models()")


if __name__ == "__main__":
    try:
        quickstart()
    except FileNotFoundError:
        print("\n❌ HATA: dataset.csv dosyası bulunamadı!")
        print("   Lütfen dataset.csv dosyanızı proje klasörüne koyun.")
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
