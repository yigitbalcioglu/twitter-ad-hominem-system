"""
Veri İşleme ve Yükleme
"""
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import AutoTokenizer, AutoModel
from typing import Tuple, List, Optional, Dict
from tqdm import tqdm


class TextDataset(Dataset):
    """PyTorch Dataset - Tokenize edilmiş metinler için"""
    
    def __init__(self, input_ids, attention_masks, labels=None):
        """
        Args:
            input_ids: Token ID'leri
            attention_masks: Attention mask'ler
            labels: Etiketler (opsiyonel)
        """
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels
    
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        item = {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_masks[idx]
        }
        
        if self.labels is not None:
            item['labels'] = self.labels[idx]
        
        return item


class DataHandler:
    """Veri yükleme ve ön işleme için ana sınıf"""
    
    def __init__(self, config):
        """
        Args:
            config: Konfigürasyon objesi
        """
        self.config = config
        self.tokenizer = None
        self.tfidf_vectorizer = None
        self.scaler = StandardScaler()
        
    def load_data(self, filepath: str = None) -> Tuple[List[str], np.ndarray]:
        """
        Veriyi CSV'den yükle
        
        Args:
            filepath: CSV dosya yolu (opsiyonel, config'den alınır)
            
        Returns:
            (metinler, etiketler) tuple
        """
        if filepath is None:
            filepath = self.config.dataset_path
        
        print(f"📁 Veri yükleniyor: {filepath}")
        df = pd.read_csv(filepath)
        
        if 'text' not in df.columns or 'label' not in df.columns:
            raise ValueError("CSV dosyası 'text' ve 'label' sütunlarını içermelidir!")
        
        texts = df['text'].values.tolist()
        labels = df['label'].values
        
        print(f"✓ {len(texts)} örnek yüklendi")
        print(f"  - Sınıf dağılımı: {np.bincount(labels)}")
        
        return texts, labels
    
    def split_data(self, texts: List[str], labels: np.ndarray, 
                   test_size: float = None, random_state: int = None):
        """
        Veriyi train-test olarak böl
        
        Args:
            texts: Metinler listesi
            labels: Etiketler
            test_size: Test set oranı
            random_state: Random seed
            
        Returns:
            train_texts, test_texts, train_labels, test_labels
        """
        if test_size is None:
            test_size = self.config.test_size
        if random_state is None:
            random_state = self.config.random_state
        
        return train_test_split(
            texts, labels,
            test_size=test_size,
            random_state=random_state,
            stratify=labels
        )
    
    def create_tokenizer(self, model_name: str = None):
        """
        Transformer tokenizer oluştur
        
        Args:
            model_name: Model adı (opsiyonel, config'den alınır)
        """
        if model_name is None:
            if hasattr(self.config, 'transformer_model_name'):
                model_name = self.config.transformer_model_name
            else:
                model_name = "dbmdz/bert-base-turkish-cased"
        
        print(f"🔤 Tokenizer yükleniyor: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        return self.tokenizer
    
    def tokenize_texts(self, texts: List[str], max_length: int = None):
        """
        Metinleri tokenize et
        
        Args:
            texts: Metinler listesi
            max_length: Maksimum sequence uzunluğu
            
        Returns:
            Tokenize edilmiş veriler (input_ids, attention_masks)
        """
        if self.tokenizer is None:
            self.create_tokenizer()
        
        if max_length is None:
            max_length = self.config.max_length
        
        print(f"🔤 Metinler tokenize ediliyor...")
        encodings = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors='pt'
        )
        
        return encodings['input_ids'], encodings['attention_mask']
    
    def create_data_loaders(self, train_texts, test_texts, train_labels, test_labels,
                           batch_size: int = None) -> Tuple[DataLoader, DataLoader]:
        """
        PyTorch DataLoader'lar oluştur
        
        Args:
            train_texts: Eğitim metinleri
            test_texts: Test metinleri
            train_labels: Eğitim etiketleri
            test_labels: Test etiketleri
            batch_size: Batch boyutu
            
        Returns:
            (train_loader, test_loader)
        """
        if batch_size is None:
            batch_size = self.config.batch_size
        
        # Tokenize
        train_input_ids, train_attention_masks = self.tokenize_texts(train_texts)
        test_input_ids, test_attention_masks = self.tokenize_texts(test_texts)
        
        # Convert labels to tensors
        train_labels_tensor = torch.tensor(train_labels, dtype=torch.long)
        test_labels_tensor = torch.tensor(test_labels, dtype=torch.long)
        
        # Create datasets
        train_dataset = TextDataset(train_input_ids, train_attention_masks, train_labels_tensor)
        test_dataset = TextDataset(test_input_ids, test_attention_masks, test_labels_tensor)
        
        # Create dataloaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        print(f"✓ DataLoader'lar oluşturuldu (batch_size={batch_size})")
        print(f"  - Train batches: {len(train_loader)}")
        print(f"  - Test batches: {len(test_loader)}")
        
        return train_loader, test_loader
    
    def extract_transformer_embeddings(self, texts: List[str], 
                                      model_name: str = None,
                                      batch_size: int = 32,
                                      max_length: int = 128) -> np.ndarray:
        """
        BERT/RoBERTa embedding'leri çıkar (ML modelleri için)
        
        Args:
            texts: Metinler listesi
            model_name: Transformer model adı
            batch_size: Batch boyutu
            max_length: Maksimum uzunluk
            
        Returns:
            Embedding matrisi [n_samples, embedding_dim]
        """
        if model_name is None:
            if hasattr(self.config, 'transformer_model_name'):
                model_name = self.config.transformer_model_name
            else:
                model_name = "dbmdz/bert-base-turkish-cased"
        
        print(f"🧠 {model_name} embeddings çıkarılıyor...")
        
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name).to(self.config.device)
        model.eval()
        
        all_embeddings = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Embedding extraction"):
            batch_texts = texts[i:i+batch_size]
            
            # Tokenize
            encodings = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors='pt'
            )
            
            input_ids = encodings['input_ids'].to(self.config.device)
            attention_mask = encodings['attention_mask'].to(self.config.device)
            
            # Extract embeddings
            with torch.no_grad():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                embeddings = outputs.pooler_output.cpu().numpy()
                all_embeddings.append(embeddings)
        
        embeddings_matrix = np.vstack(all_embeddings)
        print(f"✓ Embedding boyutu: {embeddings_matrix.shape}")
        
        return embeddings_matrix
    
    def create_tfidf_features(self, train_texts: List[str], test_texts: List[str],
                             max_features: int = 5000,
                             ngram_range: Tuple[int, int] = (1, 2)) -> Tuple[np.ndarray, np.ndarray]:
        """
        TF-IDF özellikleri oluştur
        
        Args:
            train_texts: Eğitim metinleri
            test_texts: Test metinleri
            max_features: Maksimum özellik sayısı
            ngram_range: N-gram aralığı
            
        Returns:
            (train_features, test_features)
        """
        print(f"📊 TF-IDF özellikleri oluşturuluyor (max_features={max_features})...")
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range
        )
        
        train_features = self.tfidf_vectorizer.fit_transform(train_texts).toarray()
        test_features = self.tfidf_vectorizer.transform(test_texts).toarray()
        
        print(f"✓ TF-IDF boyutu: {train_features.shape}")
        
        return train_features, test_features
    
    def prepare_ml_features(self, train_texts, test_texts,
                           use_bert=True, use_roberta=True, use_tfidf=True):
        """
        Machine Learning modelleri için özellikler hazırla
        
        Args:
            train_texts: Eğitim metinleri
            test_texts: Test metinleri
            use_bert: BERT embeddings kullan
            use_roberta: RoBERTa embeddings kullan
            use_tfidf: TF-IDF özellikleri kullan
            
        Returns:
            (train_features, test_features)
        """
        feature_list_train = []
        feature_list_test = []
        
        # BERT embeddings
        if use_bert:
            bert_train = self.extract_transformer_embeddings(
                train_texts, "dbmdz/bert-base-turkish-cased"
            )
            bert_test = self.extract_transformer_embeddings(
                test_texts, "dbmdz/bert-base-turkish-cased"
            )
            feature_list_train.append(bert_train)
            feature_list_test.append(bert_test)
        
        # RoBERTa embeddings
        if use_roberta:
            roberta_train = self.extract_transformer_embeddings(
                train_texts, "TURKCELL/roberta-base-turkish-uncased"
            )
            roberta_test = self.extract_transformer_embeddings(
                test_texts, "TURKCELL/roberta-base-turkish-uncased"
            )
            feature_list_train.append(roberta_train)
            feature_list_test.append(roberta_test)
        
        # TF-IDF features
        if use_tfidf:
            tfidf_train, tfidf_test = self.create_tfidf_features(train_texts, test_texts)
            feature_list_train.append(tfidf_train)
            feature_list_test.append(tfidf_test)
        
        # Concatenate all features
        train_features = np.concatenate(feature_list_train, axis=1)
        test_features = np.concatenate(feature_list_test, axis=1)
        
        # Scale features
        print("📈 Özellikler normalize ediliyor...")
        train_features = self.scaler.fit_transform(train_features)
        test_features = self.scaler.transform(test_features)
        
        print(f"✓ Final özellik boyutu: {train_features.shape}")
        
        return train_features, test_features
