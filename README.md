# Kalman Filter ile Spor Analitiği ve Performans Takibi ⚽📊

Bu proje, gürültülü (noisy) sporcu takip verilerini işlemek ve anlamlı performans metrikleri üretmek için geliştirilmiş bir **Lineer Kalman Filtresi** uygulamasıdır.

## 🚀 Proje Özeti
Kamera veya sensörlerden gelen konum verileri her zaman sapmalar içerir. Bu projede, matematiksel modelleme kullanarak:
- Ham verideki gürültüyü eledim.
- Oyuncunun pürüzsüz rotasını çıkardım.
- Doğrudan ölçülemeyen **hız** ve **ivme (patlayıcı güç)** verilerini türettim.

## 🛠 Teknik Detaylar
Algoritma, akademik prensiplere dayanarak 4 ana adımda çalışmaktadır:
1. **Öngörü (Prediction):** Fiziksel kurallar kullanılarak bir sonraki durum tahmin edilir.
2. **Kalman Kazancı ($K_k$):** Ölçüm gürültüsü ile tahmin belirsizliği dengelenir.
3. **Tahmin Güncelleme:** Gerçek zamanlı ölçümle öngörü harmanlanır.
4. **Hata Kovaryansı Güncelleme:** Sistemin hata payı bir sonraki adım için optimize edilir.

## 📈 Sonuçlar
Proje çıktısında oyuncunun saha üzerindeki rotası, anlık hız grafiği ve ivme değerleri profesyonel bir dashboard üzerinde görselleştirilmiştir.

---
*Bu çalışma, üniversite eğitimimdeki dinamik sistem modelleme notları rehberliğinde Python kullanılarak geliştirilmiştir.*
