import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc

# --- 0. BAŞLANGIÇ DEĞERLERİ ---
# Durum Vektörü x: [Konum_x, Konum_y, Hız_x, Hız_y]
x_tahmin = np.zeros((4, 1)) 
P = np.eye(4) * 500  # P_0: Başlangıç hata kovaryansı
dt = 0.04 # 25 FPS (Metrica Sports veri hızı)

# --- VERİ ÇEKME ---
url = "https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv"
df = pd.read_csv(url, skiprows=2)

# Verideki ilk mevcut oyuncunun sütunlarını otomatik buluyoruz
cols = [c for c in df.columns if 'x' in c.lower() or 'y' in c.lower()]
player_x_col, player_y_col = cols[0], cols[1]

raw_data = df[['Time [s]', player_x_col, player_y_col]].dropna().values
z_k_list = raw_data[:500, 1:3] * [105, 68] # Metrica verisini saha boyutuna (105x68m) oranlıyoruz

# --- SİSTEM MODELİ  ---
# A: Durum Geçiş Matrisi - Sistemin fiziksel dinamiklerini tanımlar
A = np.array([[1, 0, dt, 0],
              [0, 1, 0, dt],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

# H: Durumdan Ölçüme Dönüşüm Matrisi
H = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0]])

# Q: Durum Gürültüsü Kovaryans Matrisi (w_k)
Q = np.eye(4) * 0.1 

# R: Ölçüm Gürültüsü Kovaryans Matrisi (v_k)
R = np.eye(2) * 2.0 

kalman_sonuclari = []
hizlar = []

print("Kalman Filtresi Analizi Başlatıldı...")

# --- KALMAN DÖNGÜSÜ ---
for z_raw in z_k_list:
    z_k = z_raw.reshape(2, 1) # Güncel ölçüm vektörü

    # I. ADIM: Sistemin durumunu ve hata kovaryansını öngörünüz (Prediction)
    x_vurgu = A @ x_tahmin # x_k^-
    P_vurgu = A @ P @ A.T + Q # P_k^-

    # II. ADIM: Kalman kazancını hesaplayınız (Kalman Gain)
    S = H @ P_vurgu @ H.T + R
    K = P_vurgu @ H.T @ np.linalg.inv(S) # K_k

    # III. ADIM: Sistem durumunun tahminini hesaplayınız (Update)
    x_tahmin = x_vurgu + K @ (z_k - H @ x_vurgu) # x_k

    # IV. ADIM: Hata kovaryansını hesaplayınız (Covariance Update)
    P = (np.eye(4) - K @ H) @ P_vurgu # P_k

    kalman_sonuclari.append(x_tahmin[:2].flatten())
    
    # Hız büyüklüğünü hesapla ve scalar değerini çıkar (Hata düzeltildi)
    hiz_mag = np.sqrt(x_tahmin[2]**2 + x_tahmin[3]**2).item() 
    hizlar.append(hiz_mag)

# --- ANALİZ KATMANLARI ---
ivmeler = np.diff(hizlar) / dt
ivmeler = np.insert(ivmeler, 0, 0) # Boyut eşitleme
max_hiz = max(hizlar)

# --- PROFESYONEL GÖRSELLEŞTİRME ---
fig, axs = plt.subplots(1, 3, figsize=(20, 7), dpi=100)
# Seaborn stili yoksa klasik stili kullan (Hata önleyici)
try:
    plt.style.use('seaborn-v0_8-muted')
except:
    plt.style.use('ggplot')

# 1. Saha Üzeri Rota Analizi
def draw_pitch(ax):
    ax.add_patch(Rectangle((0, 0), 105, 68, edgecolor="black", facecolor="none", lw=2))
    ax.add_line(plt.Line2D([52.5, 52.5], [0, 68], color="black", lw=2))
    ax.set_xlim(-5, 110); ax.set_ylim(-5, 73)
    ax.set_aspect('equal')

draw_pitch(axs[0])
axs[0].plot(z_k_list[:, 0], z_k_list[:, 1], 'r.', alpha=0.2, label=r'Gürültülü Ölçüm ($z_k$)')
axs[0].plot(np.array(kalman_sonuclari)[:, 0], np.array(kalman_sonuclari)[:, 1], 'b-', lw=2, label=r'Kalman Tahmini ($\hat{x}_k$)')
axs[0].set_title("1. Saha Üzeri Rota Analizi", fontweight='bold')
axs[0].legend(loc='upper right')

# 2. Hız Analizi
axs[1].plot(hizlar, color='green', lw=2)
axs[1].fill_between(range(len(hizlar)), hizlar, color='green', alpha=0.1)
axs[1].set_title(f"2. Hız (Maks: {max_hiz:.2f} m/s)", fontweight='bold')
axs[1].set_ylabel("Hız (m/s)")

# 3. İvme / Patlayıcı Güç Analizi
axs[2].plot(ivmeler, color='orange', lw=1.5)
axs[2].set_title(f"3. İvme (Maks: {max(ivmeler):.2f} m/s²)", fontweight='bold')
axs[2].set_ylabel("İvme (m/s²)")

plt.suptitle("Spor Analitiği ve Dinamik Sistem Modelleme: Kalman Filtresi Uygulaması", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

print("Analiz Tamamlandı. Grafikler Oluşturuluyor...")

plt.show()
