"""
Model Evaluator - Model değerlendirme sınıfı
"""
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from typing import Optional, Dict, List
from tqdm import tqdm
from ..utils.metrics import MetricsCalculator, print_metrics


class ModelEvaluator:
    """
    Model değerlendirme ve analiz sınıfı
    """
    
    def __init__(self, model, config):
        """
        Args:
            model: Değerlendirilecek model
            config: Konfigürasyon objesi
        """
        self.model = model
        self.config = config
        self.device = config.device
        self.metrics_calculator = MetricsCalculator()
    
    def predict(self, data_loader) -> tuple:
        """
        Tahminlerde bulun
        
        Args:
            data_loader: DataLoader
            
        Returns:
            (predictions, true_labels, probabilities)
        """
        self.model.eval()
        
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for batch in tqdm(data_loader, desc="Predicting"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                # Forward pass
                outputs = self.model(input_ids, attention_mask)
                
                # Predictions
                probs = torch.softmax(outputs, dim=1)
                _, preds = torch.max(outputs, dim=1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        return np.array(all_preds), np.array(all_labels), np.array(all_probs)
    
    def evaluate(self, data_loader, return_preds=False) -> Dict:
        """
        Modeli değerlendir
        
        Args:
            data_loader: DataLoader
            return_preds: Tahminleri de döndür
            
        Returns:
            Metrikler dictionary
        """
        print(f"\n{'='*60}")
        print("MODEL DEĞERLENDİRİLİYOR".center(60))
        print(f"{'='*60}\n")
        
        # Predictions
        predictions, true_labels, probabilities = self.predict(data_loader)
        
        # Calculate metrics
        metrics = self.metrics_calculator.calculate_metrics(
            true_labels, predictions, probabilities, average='binary'
        )
        
        # Print metrics
        print_metrics(metrics, "Test Metrikleri")
        
        # Classification report
        print("\n📋 Detaylı Sınıflandırma Raporu:")
        print("-" * 60)
        report = self.metrics_calculator.get_classification_report(
            true_labels, predictions, target_names=['Not Ad Hominem', 'Ad Hominem']
        )
        print(report)
        
        if return_preds:
            return metrics, predictions, true_labels, probabilities
        
        return metrics
    
    def plot_confusion_matrix(self, data_loader, save_path: Optional[str] = None):
        """
        Confusion matrix görselleştir
        
        Args:
            data_loader: DataLoader
            save_path: Kayıt yolu (opsiyonel)
        """
        # Predictions
        predictions, true_labels, _ = self.predict(data_loader)
        
        # Confusion matrix
        cm = self.metrics_calculator.get_confusion_matrix(true_labels, predictions)
        
        # Plot
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Not Ad Hominem', 'Ad Hominem'],
                    yticklabels=['Not Ad Hominem', 'Ad Hominem'])
        plt.title(f'Confusion Matrix - {self.model.model_name}')
        plt.ylabel('Gerçek')
        plt.xlabel('Tahmin')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Confusion matrix kaydedildi: {save_path}")
        
        plt.show()
    
    def plot_training_history(self, history: Dict, save_path: Optional[str] = None):
        """
        Eğitim geçmişini görselleştir
        
        Args:
            history: Training history dictionary
            save_path: Kayıt yolu (opsiyonel)
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Loss plot
        axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
        axes[0].plot(history['val_loss'], label='Val Loss', marker='s')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss')
        axes[0].set_title('Training and Validation Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Accuracy plot
        axes[1].plot(history['train_acc'], label='Train Accuracy', marker='o')
        axes[1].plot(history['val_acc'], label='Val Accuracy', marker='s')
        if 'val_f1' in history:
            axes[1].plot(history['val_f1'], label='Val F1-Score', marker='^')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Score')
        axes[1].set_title('Training and Validation Metrics')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.model.model_name} - Training History', fontsize=14, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Training history kaydedildi: {save_path}")
        
        plt.show()
    
    def analyze_errors(self, data_loader, texts: List[str], top_k: int = 10):
        """
        Hatalı tahminleri analiz et
        
        Args:
            data_loader: DataLoader
            texts: Orijinal metinler
            top_k: Gösterilecek örnek sayısı
        """
        # Predictions
        predictions, true_labels, probabilities = self.predict(data_loader)
        
        # Find incorrect predictions
        incorrect_indices = np.where(predictions != true_labels)[0]
        
        if len(incorrect_indices) == 0:
            print("✓ Hiç hata yok! Tüm tahminler doğru.")
            return
        
        print(f"\n{'='*60}")
        print(f"HATA ANALİZİ - Toplam {len(incorrect_indices)} hata".center(60))
        print(f"{'='*60}\n")
        
        # Get confidence scores for errors
        error_confidences = []
        for idx in incorrect_indices:
            pred_class = predictions[idx]
            confidence = probabilities[idx][pred_class]
            error_confidences.append((idx, confidence))
        
        # Sort by confidence (highest confidence errors are most interesting)
        error_confidences.sort(key=lambda x: x[1], reverse=True)
        
        # Display top-k errors
        print(f"En Yüksek Güvenle Yapılan İlk {min(top_k, len(error_confidences))} Hata:\n")
        
        for i, (idx, confidence) in enumerate(error_confidences[:top_k], 1):
            true_label = true_labels[idx]
            pred_label = predictions[idx]
            text = texts[idx] if idx < len(texts) else "Text not available"
            
            print(f"{i}. Örnek (Index: {idx})")
            print(f"   Metin: {text[:100]}...")
            print(f"   Gerçek: {'Ad Hominem' if true_label == 1 else 'Not Ad Hominem'}")
            print(f"   Tahmin: {'Ad Hominem' if pred_label == 1 else 'Not Ad Hominem'}")
            print(f"   Güven: {confidence:.4f}")
            print()
    
    def compare_models(self, results: Dict[str, Dict]):
        """
        Birden fazla modelin sonuçlarını karşılaştır
        
        Args:
            results: Model sonuçları {model_name: metrics}
        """
        print(f"\n{'='*80}")
        print("MODEL KARŞILAŞTIRMASI".center(80))
        print(f"{'='*80}\n")
        
        # Create comparison table
        metrics_names = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        print(f"{'Model':<20}", end='')
        for metric in metrics_names:
            print(f"{metric.upper():>12}", end='')
        print()
        print("-" * 80)
        
        for model_name, metrics in results.items():
            print(f"{model_name:<20}", end='')
            for metric in metrics_names:
                value = metrics.get(metric, 0.0)
                print(f"{value:>12.4f}", end='')
            print()
        
        print(f"{'='*80}\n")
        
        # Find best model for each metric
        print("🏆 En İyi Modeller:")
        for metric in metrics_names:
            best_model = max(results.items(), key=lambda x: x[1].get(metric, 0.0))
            print(f"  {metric.upper():<12} : {best_model[0]} ({best_model[1].get(metric, 0.0):.4f})")
