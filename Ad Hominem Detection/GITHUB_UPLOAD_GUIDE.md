# GitHub'a Yükleme Rehberi

## Adım 1: GitHub'da Repository Oluştur

1. https://github.com adresine git
2. Sağ üstte **"+"** işaretine tıkla → **"New repository"**
3. Repository bilgilerini gir:
   - **Repository name**: `Ad-Hominem-Detection-Turkish`
   - **Description**: `Ad Hominem Detection in Turkish Texts Using Machine Learning and Deep Learning Models - OOP Architecture`
   - **Public** veya **Private** seç
   - ❌ **"Initialize this repository with a README"** işaretleme (zaten var)
   - ❌ **".gitignore"** ekleme (zaten var)
   - ✅ **License**: MIT seçebilirsin (zaten eklendi)
4. **"Create repository"** butonuna tıkla

## Adım 2: Git Başlat ve Yükle

### Terminal'de (PowerShell) şu komutları çalıştır:

```powershell
# 1. Proje dizinine git
cd "C:\Users\PC\Desktop\Bachelor Thesis-Ad Hominem Detection in Turkish Texts Using Machine Learning and Deep Learning Models"

# 2. Git repository'sini başlat
git init

# 3. Tüm dosyaları ekle
git add .

# 4. İlk commit'i yap
git commit -m "Initial commit: Complete OOP-based Ad Hominem Detection System"

# 5. Ana branch'i main olarak ayarla
git branch -M main

# 6. GitHub repository'sini remote olarak ekle
# ⚠️ DİKKAT: <KULLANICI_ADI> kısmını kendi GitHub kullanıcı adınla değiştir
git remote add origin https://github.com/<KULLANICI_ADI>/Ad-Hominem-Detection-Turkish.git

# 7. Kodu GitHub'a yükle
git push -u origin main
```

### Örnek (kullanıcı adın "johndoe" ise):
```powershell
git remote add origin https://github.com/johndoe/Ad-Hominem-Detection-Turkish.git
git push -u origin main
```

## Adım 3: GitHub Credentials

İlk push sırasında GitHub kimlik bilgilerini isteyebilir:
- **Username**: GitHub kullanıcı adın
- **Password**: GitHub **Personal Access Token** (şifre değil!)

### Personal Access Token Oluşturma:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. İzinleri seç: `repo` (tüm kutuları işaretle)
4. "Generate token" → Token'ı kopyala ve sakla!

## Adım 4: Doğrulama

Yükleme başarılı olduysa:
```powershell
git status
```
"Your branch is up to date" mesajını görmelisin.

## Alternatif: GitHub Desktop Kullanımı

Komut satırı yerine GitHub Desktop tercih ediyorsan:

1. **GitHub Desktop**'ı indir: https://desktop.github.com/
2. Uygulamayı aç → "Add" → "Add Existing Repository"
3. Proje klasörünü seç
4. "Publish repository" butonuna tıkla
5. Repository bilgilerini gir ve yükle

## Sonraki Güncellemeler İçin

Projeye değişiklik yaptığında:

```powershell
# Değişiklikleri görüntüle
git status

# Tüm değişiklikleri ekle
git add .

# Commit yap
git commit -m "Açıklayıcı mesaj buraya"

# GitHub'a yükle
git push
```

## Önemli Notlar

### ⚠️ Dataset Dosyası

Eğer `dataset.csv` dosyan çok büyükse (>100MB) veya hassas veri içeriyorsa:

1. `.gitignore` dosyasındaki `# dataset.csv` satırının başındaki `#` işaretini kaldır
2. README'de dataset'in nereden edinilebileceğini belirt

### 📝 README Badge'leri (Opsiyonel)

README.md'nin başına badge'ler ekleyebilirsin:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

### 🎯 Repository Ayarları

GitHub'da repository'ne girdikten sonra:
- **Settings → General**: Description ve website ekle
- **Settings → Topics**: `nlp`, `turkish`, `deep-learning`, `machine-learning`, `bert`, `ad-hominem`, `text-classification` ekle
- **About**: Repository açıklaması güncelle

## Hata Giderme

### Hata: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/<KULLANICI_ADI>/repo-adi.git
```

### Hata: "Updates were rejected"
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Hata: Large files (>100MB)
```powershell
# Git LFS kullan
git lfs install
git lfs track "*.pth"
git add .gitattributes
git commit -m "Add Git LFS"
```

## ✅ Tamamlandı!

Artık projen GitHub'da! 🎉

Repository link'ini README.md'ye ekleyebilirsin:
```markdown
## 🔗 Repository
https://github.com/<KULLANICI_ADI>/Ad-Hominem-Detection-Turkish
```
