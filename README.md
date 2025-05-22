🛍️ RFM Analizi Dashboard'u

Online perakende müşteri verilerinin RFM (Recency, Frequency, Monetary) analizi için kapsamlı Streamlit uygulaması. İnteraktif görselleştirmeler ve müşteri segmentasyonu içerir.


📊 Özellikler

RFM Score Analizi: Kapsamlı RFM skorlaması ve müşteri değerlendirmesi
Müşteri Segmentasyonu: Otomatik kategorilendirme (Düşük, Orta, Yüksek müşteriler)
İnteraktif Görselleştirmeler: 3D grafikler, ısı haritaları, radar grafikleri ve istatistiksel analizler
Gerçek Zamanlı Filtreleme: Müşteri seviyeleri ve RFM score aralıkları için dinamik filtreler
Veri Dışa Aktarımı: Filtrelenmiş veri ve özet raporları indirme
Çoklu Sekme Arayüzü: Farklı perspektiflerden organize edilmiş analizler

🔧 Kullanılan Teknolojiler

Streamlit: Web uygulama çerçevesi
Pandas: Veri manipülasyonu ve analizi
Matplotlib: Statik grafik çizimi ve görselleştirme
Seaborn: İstatistiksel veri görselleştirmesi
NumPy: Sayısal hesaplama

📈 Dashboard Bölümleri

📊 Genel Bakış: Müşteri dağılımı, RFM score histogramları, korelasyon matrisi
🎯 RFM Analizi: 3D dağılım grafikleri, trend analizi, segmentlere göre kutu grafikleri
👥 Müşteri Segmentleri: Detaylı segment analizi, gelir dağılımı, radar grafikleri
📈 Detaylı Analizler: İstatistiksel analizler, en değerli müşteriler, ısı haritaları

📋 Veri Gereksinimleri
Uygulama aşağıdaki sütunları içeren bir CSV dosyası bekler:

CustomerID: Benzersiz müşteri kimliği
Recency: Son satın alımdan bu yana geçen gün sayısı
Frequency: Toplam satın alma sayısı
Monetary: Toplam satın alma tutarı
RFMScore: Hesaplanmış RFM skoru
CustomerLevel: Müşteri segmenti (Low, Middle, Top)

🚀 Kendi bilgisayarınızda nasıl çalıştırılır
Ön Gereksinimler

Python 3.7 veya üzeri
pip paket yöneticisi

Kurulum Adımları

Repository'yi klonlayın
bashgit clone https://github.com/kullanici-adiniz/rfm-analytics-dashboard.git
cd rfm-analytics-dashboard

Gereksinimleri yükleyin
bashpip install -r requirements.txt

Veri dosyanızı ekleyin

OnlineRetail_RFMSCORE.csv dosyanızı proje klasörüne yerleştirin


Uygulamayı çalıştırın
bashstreamlit run app.py

🎯 Kullanım Senaryoları

E-ticaret şirketleri için müşteri segmentasyonu
Pazarlama ekipleri için hedefleme stratejileri
CRM analistleri için müşteri değer analizi
İş zekası uzmanları için performans takibi

📱 Mobil Uyumlu
Dashboard, mobil cihazlarda da rahatlıkla kullanılabilir ve responsive tasarıma sahiptir.

*******************

Bu dashboard, RFM analizi ve müşteri segmentasyonu için geliştirilmiş kapsamlı bir araçtır. 🚀
