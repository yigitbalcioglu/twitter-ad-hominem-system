"""
Model Trainer - Deep Learning modelleri için eğitim sınıfı
"""
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
from tqdm import tqdm
import os
from typing import Optional, Dict, Tuple
from ..utils.metrics import AverageMeter, EarlyStopping, calculate_batch_metrics
from ..utils.losses import get_loss_function


class ModelTrainer:
    """
    PyTorch modelleri için eğitim sınıfı
    """
    
    def __init__(self, model, config, loss_fn=None, optimizer=None, scheduler=None):
        """
        Args:
            model: Eğitilecek model
            config: Konfigürasyon objesi
            loss_fn: Loss fonksiyonu (opsiyonel)
            optimizer: Optimizer (opsiyonel)
            scheduler: Learning rate scheduler (opsiyonel)
        """
        self.model = model
        self.config = config
        self.device = config.device
        
        # Loss function
        if loss_fn is None:
            self.loss_fn = nn.CrossEntropyLoss()
        else:
            self.loss_fn = loss_fn
        
        # Optimizer
        if optimizer is None:
            self.optimizer = AdamW(
                self.model.parameters(),
                lr=config.learning_rate,
                weight_decay=config.weight_decay
            )
        else:
            self.optimizer = optimizer
        
        # Scheduler
        self.scheduler = scheduler
        
        # Early stopping
        self.early_stopping = EarlyStopping(
            patience=config.early_stopping_patience,
            mode='max',  # F1-score için
            verbose=True
        )
        
        # Training history
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'val_f1': []
        }
        
        # Best model tracking
        self.best_model_path = None
        self.best_f1 = 0.0
    
    def create_scheduler(self, train_loader, epochs=None):
        """
        Learning rate scheduler oluştur
        
        Args:
            train_loader: Training DataLoader
            epochs: Epoch sayısı
        """
        if epochs is None:
            epochs = self.config.epochs
        
        num_training_steps = len(train_loader) * epochs
        
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=self.config.warmup_steps,
            num_training_steps=num_training_steps
        )
        
        print(f"✓ Scheduler oluşturuldu (total_steps={num_training_steps})")
    
    def train_epoch(self, train_loader) -> Tuple[float, float]:
        """
        Bir epoch eğitim yap
        
        Args:
            train_loader: Training DataLoader
            
        Returns:
            (avg_loss, avg_accuracy)
        """
        self.model.train()
        
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()
        
        pbar = tqdm(train_loader, desc="Training")
        
        for batch in pbar:
            # Batch'i cihaza taşı
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(input_ids, attention_mask)
            
            # Loss hesapla
            loss = self.loss_fn(outputs, labels)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            # Optimizer step
            self.optimizer.step()
            
            if self.scheduler is not None:
                self.scheduler.step()
            
            # Metrics
            batch_metrics = calculate_batch_metrics(outputs, labels, loss.item())
            
            # Update meters
            batch_size = labels.size(0)
            loss_meter.update(loss.item(), batch_size)
            acc_meter.update(batch_metrics['accuracy'], batch_size)
            
            # Update progress bar
            pbar.set_postfix({
                'loss': f"{loss_meter.avg:.4f}",
                'acc': f"{acc_meter.avg:.4f}"
            })
        
        return loss_meter.avg, acc_meter.avg
    
    def validate(self, val_loader) -> Tuple[float, float, float, torch.Tensor, torch.Tensor]:
        """
        Validation yap
        
        Args:
            val_loader: Validation DataLoader
            
        Returns:
            (avg_loss, avg_accuracy, f1_score, all_preds, all_labels)
        """
        self.model.eval()
        
        loss_meter = AverageMeter()
        acc_meter = AverageMeter()
        
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                # Batch'i cihaza taşı
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                # Forward pass
                outputs = self.model(input_ids, attention_mask)
                
                # Loss hesapla
                loss = self.loss_fn(outputs, labels)
                
                # Predictions
                _, preds = torch.max(outputs, dim=1)
                
                # Metrics
                batch_metrics = calculate_batch_metrics(outputs, labels, loss.item())
                
                # Update meters
                batch_size = labels.size(0)
                loss_meter.update(loss.item(), batch_size)
                acc_meter.update(batch_metrics['accuracy'], batch_size)
                
                # Store predictions and labels
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        # Calculate F1-score
        from sklearn.metrics import f1_score
        f1 = f1_score(all_labels, all_preds, average='binary')
        
        return loss_meter.avg, acc_meter.avg, f1, torch.tensor(all_preds), torch.tensor(all_labels)
    
    def train(self, train_loader, val_loader, epochs=None) -> Dict:
        """
        Model eğitimi
        
        Args:
            train_loader: Training DataLoader
            val_loader: Validation DataLoader
            epochs: Epoch sayısı
            
        Returns:
            Training history
        """
        if epochs is None:
            epochs = self.config.epochs
        
        print(f"\n{'='*60}")
        print(f"EĞİTİM BAŞLIYOR - {self.model.model_name}".center(60))
        print(f"{'='*60}")
        print(f"Epochs: {epochs}")
        print(f"Batch Size: {self.config.batch_size}")
        print(f"Learning Rate: {self.config.learning_rate}")
        print(f"Device: {self.device}")
        print(f"{'='*60}\n")
        
        # Create scheduler if not exists
        if self.scheduler is None:
            self.create_scheduler(train_loader, epochs)
        
        for epoch in range(epochs):
            print(f"\n📍 Epoch {epoch+1}/{epochs}")
            print("-" * 60)
            
            # Training
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # Validation
            val_loss, val_acc, val_f1, _, _ = self.validate(val_loader)
            
            # Update history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['val_f1'].append(val_f1)
            
            # Print epoch summary
            print(f"\n📊 Epoch {epoch+1} Özeti:")
            print(f"  Train - Loss: {train_loss:.4f}, Acc: {train_acc:.4f}")
            print(f"  Val   - Loss: {val_loss:.4f}, Acc: {val_acc:.4f}, F1: {val_f1:.4f}")
            
            # Save best model
            if val_f1 > self.best_f1:
                self.best_f1 = val_f1
                self.best_model_path = os.path.join(
                    self.config.checkpoint_dir,
                    f"{self.model.model_name}_best.pth"
                )
                self.model.save_model(self.best_model_path)
                print(f"  💾 En iyi model kaydedildi! (F1: {val_f1:.4f})")
            
            # Early stopping
            if self.early_stopping(val_f1, epoch):
                print(f"\n⛔ Early stopping triggered at epoch {epoch+1}")
                break
        
        print(f"\n{'='*60}")
        print("EĞİTİM TAMAMLANDI!".center(60))
        print(f"{'='*60}")
        print(f"En iyi F1-Score: {self.best_f1:.4f}")
        print(f"En iyi model: {self.best_model_path}")
        print(f"{'='*60}\n")
        
        return self.history
    
    def load_best_model(self):
        """En iyi modeli yükle"""
        if self.best_model_path and os.path.exists(self.best_model_path):
            self.model.load_model(self.best_model_path)
            print(f"✓ En iyi model yüklendi: {self.best_model_path}")
        else:
            print("⚠ En iyi model bulunamadı!")
