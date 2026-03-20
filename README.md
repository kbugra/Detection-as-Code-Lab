# 🛡️ Detection-as-Code (DaC) Factory: Sigma Pack for Windows Security

> **Transforming threat hunting from a manual task into a continuous engineering pipeline.**

## 🚀 Proje Vizyonu (Ruleset Philosophy)
Modern Güvenlik Operasyon Merkezleri (SOC), kural yazımını ve test süreçlerini manuel olarak yönetmenin ötesine geçmelidir. Bu proje, geleneksel SIEM sorgu yazarlığını bir **Yazılım Mühendisliği (CI/CD)** disiplinine dönüştürmek amacıyla "Detection-as-Code" (DaC) felsefesiyle inşa edilmiştir. 

Amacımız; platform bağımsız (vendor-agnostic) Sigma kuralları yazmak, bu kuralları sektör standardı olan **Mordor APT simülasyon logları** ile otomatik olarak test etmek ve GitHub Actions aracılığıyla saniyeler içinde Splunk (SPL) ve Elasticsearch (Lucene/KQL) dillerine dönüştürmektir.

## 🏗️ Sistem Mimarisi (Pipeline Otomasyonu)

1. **Code:** Yeni tehdit istihbaratı (CTI) YAML formatında (Sigma) yazılır.
2. **Commit:** Kod GitHub'a pushlanır.
3. **CI/CD (GitHub Actions):** - YAML syntax kontrolü yapılır (Linting).
   - Mantıksal doğrulama gerçekleştirilir.
   - Kurallar otomatik olarak `/build` klasörüne **Splunk** ve **Elasticsearch** dilleri için derlenir (Build).
4. **Deploy:** Üretilen sorgular SIEM sistemlerine entegre edilmeye hazırdır.

## 🎯 MITRE ATT&CK Kapsam Matrisi (Coverage Matrix)

Mevcut tespit kurallarımızın kapsadığı taktik ve teknikler aşağıda haritalandırılmıştır:

| Tactic | Technique ID | Technique Name | Sigma Rule | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | `proc_access_win_lsass_susp_access.yml` | 🟢 Active |
| **Execution** | `T1059.001` | PowerShell | `proc_creation_win_powershell_encoded.yml` | 🟢 Active |
| **Persistence** | `T1053.005` | Scheduled Task/Job | `proc_creation_win_schtasks_creation.yml` | 🟢 Active |
| **Impact** | `T1490` | Inhibit System Recovery (Ransomware) | `proc_creation_win_vssadmin_delete_shadows.yml` | 🟢 Active |

## 🧪 Altın Veri Seti (Golden Dataset) İle Doğrulama
Bu projede tekerleği yeniden icat etmemek ve endüstri standartlarında kalibrasyon sağlamak için **OTRF Mordor** açık kaynak veri seti kullanılmıştır. Kurallarımız, `/tests/dataset/` dizinindeki gerçek dünya (APT29 vb.) simülasyonlarına ait loglar üzerinde kalite kontrolünden (Security QA) geçmektedir.

## 🛠️ Nasıl Çalıştırılır?

Projeyi kendi ortamınızda test etmek veya SIEM sorgularını üretmek için:

```bash
# Bağımlılıkları yükleyin
pip install sigma-cli
sigma plugin install splunk elasticsearch sysmon

# Tüm kuralları Splunk'a dönüştürün
sigma convert -t splunk -p sysmon rules/sigma/

# Elasticsearch için dönüştürün
sigma convert -t lucene -p sysmon rules/sigma/
```