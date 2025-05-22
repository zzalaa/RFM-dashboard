import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="RFM Analizi Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Matplotlib stil ayarları
plt.style.use('default')
sns.set_palette("husl")

# Başlık ve açıklama
st.title("🛍️ RFM Analizi Dashboard")
st.markdown("---")

# Dosya yükleme veya varsayılan dosya kullanma
st.subheader("📁 Veri Kaynağı Seçimi")
data_source = st.radio(
    "Veri kaynağınızı seçin:",
    ["Varsayılan dosyayı kullan (OnlineRetail_RFMSCORE.csv)", "Kendi dosyamı yükle"]
)

uploaded_file = None
if data_source == "Kendi dosyamı yükle":
    uploaded_file = st.file_uploader(
        "RFM analizi verilerinizi yükleyin (CSV formatında)",
        type=['csv'],
        help="CSV dosyanızda CustomerID, Recency, Frequency, Monetary, RFMScore, CustomerLevel sütunları bulunmalıdır."
    )
else:
    # Varsayılan dosya yolu
    default_file = "OnlineRetail_RFMSCORE.csv"

if uploaded_file is not None or data_source == "Varsayılan dosyayı kullan (OnlineRetail_RFMSCORE.csv)":
    # Veriyi yükle
    try:
        if data_source == "Varsayılan dosyayı kullan (OnlineRetail_RFMSCORE.csv)":
            try:
                df = pd.read_csv("OnlineRetail_RFMSCORE.csv")
                st.success("✅ OnlineRetail_RFMSCORE.csv dosyası başarıyla yüklendi!")
            except FileNotFoundError:
                st.error("❌ OnlineRetail_RFMSCORE.csv dosyası bulunamadı! Lütfen dosyanın aynı klasörde olduğundan emin olun.")
                st.info("💡 Alternatif olarak 'Kendi dosyamı yükle' seçeneğini kullanabilirsiniz.")
                st.stop()
        else:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Dosya başarıyla yüklendi!")
        
        # Gerekli sütunların varlığını kontrol et
        required_columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFMScore', 'CustomerLevel']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Eksik sütunlar: {', '.join(missing_columns)}")
            st.stop()
        
        # Sidebar - Filtreler
        st.sidebar.header("📋 Filtreler")
        
        # Müşteri seviyesi filtresi
        customer_levels = st.sidebar.multiselect(
            "Müşteri Seviyesi Seçin:",
            options=df['CustomerLevel'].unique(),
            default=df['CustomerLevel'].unique()
        )
        
        # RFM Score aralığı
        rfm_range = st.sidebar.slider(
            "RFM Score Aralığı:",
            min_value=int(df['RFMScore'].min()),
            max_value=int(df['RFMScore'].max()),
            value=(int(df['RFMScore'].min()), int(df['RFMScore'].max()))
        )
        
        # Veriyi filtrele
        filtered_df = df[
            (df['CustomerLevel'].isin(customer_levels)) &
            (df['RFMScore'] >= rfm_range[0]) &
            (df['RFMScore'] <= rfm_range[1])
        ]
        
        # Ana metrikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Toplam Müşteri",
                value=f"{len(filtered_df):,}",
                delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
            )
        
        with col2:
            st.metric(
                label="Ortalama RFM Score",
                value=f"{filtered_df['RFMScore'].mean():.1f}",
                delta=f"{filtered_df['RFMScore'].mean() - df['RFMScore'].mean():.1f}" if len(filtered_df) != len(df) else None
            )
        
        with col3:
            st.metric(
                label="Ortalama Monetary Değer",
                value=f"${filtered_df['Monetary'].mean():,.2f}",
                delta=f"${filtered_df['Monetary'].mean() - df['Monetary'].mean():,.2f}" if len(filtered_df) != len(df) else None
            )
        
        with col4:
            st.metric(
                label="Ortalama Frequency",
                value=f"{filtered_df['Frequency'].mean():.1f}",
                delta=f"{filtered_df['Frequency'].mean() - df['Frequency'].mean():.1f}" if len(filtered_df) != len(df) else None
            )
        
        st.markdown("---")
        
        # Görselleştirmeler
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Bakış", "🎯 RFM Analizi", "👥 Müşteri Segmentleri", "📈 Detaylı Analizler"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Müşteri seviyesi dağılımı - Pie Chart
                st.subheader("Müşteri Seviyesi Dağılımı")
                level_counts = filtered_df['CustomerLevel'].value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 6))
                colors = sns.color_palette("husl", len(level_counts))
                wedges, texts, autotexts = ax.pie(level_counts.values, labels=level_counts.index, 
                                                 autopct='%1.1f%%', colors=colors, startangle=90)
                ax.set_title("Müşteri Seviyesi Dağılımı", fontsize=14, fontweight='bold')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                # RFM Score dağılımı - Histogram
                st.subheader("RFM Score Dağılımı")
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.hist(filtered_df['RFMScore'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax.set_xlabel('RFM Score')
                ax.set_ylabel('Müşteri Sayısı')
                ax.set_title('RFM Score Dağılımı', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            # RFM bileşenlerinin korelasyon matrisi
            st.subheader("RFM Bileşenleri Korelasyon Matrisi")
            corr_data = filtered_df[['Recency', 'Frequency', 'Monetary', 'RFMScore']].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr_data, dtype=bool))
            sns.heatmap(corr_data, mask=mask, annot=True, cmap='RdBu_r', center=0,
                       square=True, linewidths=.5, ax=ax)
            ax.set_title('RFM Bileşenleri Korelasyon Matrisi', fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # 3D Scatter Plot - RFM
                st.subheader("3D RFM Analizi")
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                
                # Müşteri seviyelerine göre renklendirme
                unique_levels = filtered_df['CustomerLevel'].unique()
                colors = sns.color_palette("husl", len(unique_levels))
                color_map = dict(zip(unique_levels, colors))
                
                for level in unique_levels:
                    level_data = filtered_df[filtered_df['CustomerLevel'] == level]
                    ax.scatter(level_data['Recency'], level_data['Frequency'], 
                              level_data['Monetary'], c=[color_map[level]], 
                              label=level, alpha=0.6, s=50)
                
                ax.set_xlabel('Recency (Gün)')
                ax.set_ylabel('Frequency (Adet)')
                ax.set_zlabel('Monetary ($)')
                ax.set_title('3D RFM Analizi', fontsize=14, fontweight='bold')
                ax.legend()
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                # RFM Score vs Monetary
                st.subheader("RFM Score vs Monetary Değer")
                fig, ax = plt.subplots(figsize=(10, 8))
                
                for level in unique_levels:
                    level_data = filtered_df[filtered_df['CustomerLevel'] == level]
                    ax.scatter(level_data['RFMScore'], level_data['Monetary'], 
                              label=level, alpha=0.6, s=60)
                
                # Trend line
                z = np.polyfit(filtered_df['RFMScore'], filtered_df['Monetary'], 1)
                p = np.poly1d(z)
                ax.plot(filtered_df['RFMScore'].sort_values(), 
                       p(filtered_df['RFMScore'].sort_values()), 
                       "r--", alpha=0.8, linewidth=2)
                
                ax.set_xlabel('RFM Score')
                ax.set_ylabel('Monetary Değer ($)')
                ax.set_title('RFM Score vs Monetary Değer', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            # RFM bileşenlerinin müşteri seviyesine göre box plot'u
            st.subheader("Müşteri Seviyesine Göre RFM Bileşenleri")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.boxplot(data=filtered_df, x='CustomerLevel', y='Recency', ax=ax)
                ax.set_title('Recency Dağılımı', fontsize=12, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.boxplot(data=filtered_df, x='CustomerLevel', y='Frequency', ax=ax)
                ax.set_title('Frequency Dağılımı', fontsize=12, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col3:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.boxplot(data=filtered_df, x='CustomerLevel', y='Monetary', ax=ax)
                ax.set_title('Monetary Dağılımı', fontsize=12, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
        
        with tab3:
            # Müşteri segmentlerinin detaylı analizi
            segment_analysis = filtered_df.groupby('CustomerLevel').agg({
                'CustomerID': 'count',
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': 'mean',
                'RFMScore': 'mean'
            }).round(2)
            segment_analysis.rename(columns={'CustomerID': 'Müşteri Sayısı'}, inplace=True)
            
            st.subheader("Müşteri Segmentleri Detaylı Analizi")
            st.dataframe(segment_analysis, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Segmentlere göre gelir dağılımı
                st.subheader("Segmentlere Göre Toplam Gelir")
                revenue_by_segment = filtered_df.groupby('CustomerLevel')['Monetary'].sum()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(revenue_by_segment.index, revenue_by_segment.values, 
                             color=sns.color_palette("husl", len(revenue_by_segment)))
                ax.set_xlabel('Müşteri Seviyesi')
                ax.set_ylabel('Toplam Gelir ($)')
                ax.set_title('Segmentlere Göre Toplam Gelir', fontsize=14, fontweight='bold')
                
                # Bar değerlerini göster
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'${height/1000:.1f}K', ha='center', va='bottom')
                
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                # Segmentlere göre ortalama RFM score
                st.subheader("Segmentlere Göre Ortalama RFM Score")
                avg_rfm_by_segment = filtered_df.groupby('CustomerLevel')['RFMScore'].mean()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(avg_rfm_by_segment.index, avg_rfm_by_segment.values,
                             color=sns.color_palette("viridis", len(avg_rfm_by_segment)))
                ax.set_xlabel('Müşteri Seviyesi')
                ax.set_ylabel('Ortalama RFM Score')
                ax.set_title('Segmentlere Göre Ortalama RFM Score', fontsize=14, fontweight='bold')
                
                # Bar değerlerini göster
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}', ha='center', va='bottom')
                
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            # Segmentlere göre radar chart
            st.subheader("Müşteri Segmentleri Radar Analizi")
            
            # Her segment için normalize edilmiş değerler
            segment_radar = filtered_df.groupby('CustomerLevel').agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': 'mean',
                'RFMScore': 'mean'
            })
            
            # Normalize et (0-1 arası)
            for col in segment_radar.columns:
                segment_radar[col] = (segment_radar[col] - segment_radar[col].min()) / (segment_radar[col].max() - segment_radar[col].min())
            
            # Radar chart
            categories = ['Recency (Ters)', 'Frequency', 'Monetary', 'RFM Score']
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
            angles += angles[:1]  # Döngüyü tamamla
            
            colors = sns.color_palette("husl", len(segment_radar))
            
            for i, (segment, color) in enumerate(zip(segment_radar.index, colors)):
                values = [
                    1 - segment_radar.loc[segment, 'Recency'],  # Recency için ters
                    segment_radar.loc[segment, 'Frequency'],
                    segment_radar.loc[segment, 'Monetary'],
                    segment_radar.loc[segment, 'RFMScore']
                ]
                values += values[:1]  # Döngüyü tamamla
                
                ax.plot(angles, values, 'o-', linewidth=2, label=segment, color=color)
                ax.fill(angles, values, alpha=0.25, color=color)
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 1)
            ax.set_title('Müşteri Segmentleri Radar Analizi', fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
            ax.grid(True)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with tab4:
            st.subheader("Detaylı İstatistiksel Analizler")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # RFM Score dağılımının istatistikleri
                st.write("**RFM Score İstatistikleri:**")
                rfm_stats = filtered_df['RFMScore'].describe()
                st.dataframe(rfm_stats.to_frame().T, use_container_width=True)
                
                # Quantile analizi
                st.write("**RFM Score Quantile Analizi:**")
                quantiles = [0.25, 0.5, 0.75, 0.9, 0.95]
                quantile_values = filtered_df['RFMScore'].quantile(quantiles)
                quantile_df = pd.DataFrame({
                    'Quantile': [f"{q*100}%" for q in quantiles],
                    'RFM Score': quantile_values.values
                })
                st.dataframe(quantile_df, use_container_width=True)
            
            with col2:
                # Monetary değer dağılımı
                st.subheader("Monetary Değer Dağılımı")
                fig, ax = plt.subplots(figsize=(8, 6))
                
                # Log scale için pozitif değerleri filtrele
                positive_monetary = filtered_df[filtered_df['Monetary'] > 0]['Monetary']
                ax.hist(np.log10(positive_monetary), bins=30, alpha=0.7, color='green', edgecolor='black')
                ax.set_xlabel('Log10(Monetary Değer)')
                ax.set_ylabel('Müşteri Sayısı')
                ax.set_title('Monetary Değer Dağılımı (Log Scale)', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            # Top müşteriler
            st.subheader("En Değerli Müşteriler (RFM Score'a Göre)")
            top_customers = filtered_df.nlargest(10, 'RFMScore')[
                ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFMScore', 'CustomerLevel']
            ]
            st.dataframe(top_customers, use_container_width=True)
            
            # Heatmap - RFM Score vs Customer Level
            st.subheader("RFM Score ve Müşteri Seviyesi Heatmap")
            
            # RFM Score'u kategorilere ayır
            filtered_df['RFM_Category'] = pd.cut(
                filtered_df['RFMScore'], 
                bins=5, 
                labels=['Düşük', 'Düşük-Orta', 'Orta', 'Orta-Yüksek', 'Yüksek']
            )
            
            heatmap_data = pd.crosstab(filtered_df['CustomerLevel'], filtered_df['RFM_Category'])
            
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_title('Müşteri Seviyesi vs RFM Kategorisi', fontsize=14, fontweight='bold')
            ax.set_xlabel('RFM Kategorisi')
            ax.set_ylabel('Müşteri Seviyesi')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            
            # Violin plot - RFM Score dağılımı
            st.subheader("Müşteri Seviyelerine Göre RFM Score Dağılımı")
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.violinplot(data=filtered_df, x='CustomerLevel', y='RFMScore', ax=ax)
            ax.set_title('Müşteri Seviyelerine Göre RFM Score Dağılımı', fontsize=14, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        # İndirilecek özet rapor
        st.markdown("---")
        st.subheader("📄 Özet Rapor")
        
        summary_report = f"""
        ## RFM Analizi Özet Raporu
        
        **Genel Bilgiler:**
        - Toplam Müşteri Sayısı: {len(filtered_df):,}
        - Ortalama RFM Score: {filtered_df['RFMScore'].mean():.2f}
        - Ortalama Monetary Değer: ${filtered_df['Monetary'].mean():,.2f}
        - Ortalama Frequency: {filtered_df['Frequency'].mean():.2f}
        - Ortalama Recency: {filtered_df['Recency'].mean():.1f} gün
        
        **Müşteri Segmentleri:**
        {segment_analysis.to_string()}
        
        **Öneriler:**
        - **Top Müşteriler**: RFM score'u yüksek müşterilere özel kampanyalar düzenleyin
        - **Middle Müşteriler**: Frequency artırıcı aktiviteler planlayın
        - **Low Müşteriler**: Reaktivasyon kampanyaları ile geri kazanmaya odaklanın
        """
        
        st.markdown(summary_report)
        
        # CSV indirme butonu
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Filtrelenmiş Veriyi İndir (CSV)",
            data=csv,
            file_name="rfm_analizi_filtered.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {str(e)}")
        st.info("Lütfen CSV dosyanızın doğru formatta olduğundan emin olun.")

else:
    st.info("👆 Lütfen RFM analizi verilerinizi yükleyin.")
    
    # Örnek veri formatı göster
    st.subheader("📋 Beklenen Veri Formatı")
    sample_data = {
        'CustomerID': [12347, 12348, 12350],
        'Recency': [5006, 5131, 5222],
        'Frequency': [106, 5, 17],
        'Monetary': [2540.29, 367.0, 334.40],
        'RFMScore': [311, 143, 133],
        'CustomerLevel': ['Low', 'Middle', 'Middle']
    }
    st.dataframe(pd.DataFrame(sample_data))
    
    st.markdown("""
    **Gerekli Sütunlar:**
    - `CustomerID`: Müşteri kimlik numarası
    - `Recency`: Son satın alımdan bu yana geçen gün sayısı
    - `Frequency`: Toplam satın alma sayısı
    - `Monetary`: Toplam harcama miktarı
    - `RFMScore`: Hesaplanmış RFM skoru
    - `CustomerLevel`: Müşteri segmenti (Low, Middle, Top vb.)
    """)

# Footer
st.markdown("---")
st.markdown("*Bu dashboard RFM analizi sonuçlarınızı görselleştirmek için tasarlanmıştır.*")
