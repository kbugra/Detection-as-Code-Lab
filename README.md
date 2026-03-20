[EN]
# Detection-as-Code (DaC) Factory: Sigma Pack for Windows Security

*The Turkish (TR) version is below.*

> **Transforming threat hunting from a manual task into a continuous engineering pipeline.**

## Project Vision (Ruleset Philosophy)
Modern Security Operations Centers (SOC) must move beyond managing rule creation and testing processes manually. This project is built upon the "Detection-as-Code" (DaC) philosophy to transform traditional SIEM query writing into a **Software Engineering (CI/CD)** discipline.

Our goal is to write platform-agnostic Sigma rules, automatically validate them against industry-standard **Mordor APT simulation logs**, and convert them into Splunk (SPL) and Elasticsearch (Lucene/KQL) formats within seconds via GitHub Actions.

## System Architecture (Pipeline Automation)

1. **Code:** New Cyber Threat Intelligence (CTI) is written in YAML format (Sigma).
2. **Commit:** The code is pushed to GitHub.
3. **CI/CD (GitHub Actions):** 
   - YAML syntax checking (Linting).
   - Logical validation.
   - Rules are automatically compiled into the `/build` directory for **Splunk** and **Elasticsearch** (Build).
4. **Deploy:** The generated queries are ready to be integrated into SIEM systems.

## MITRE ATT&CK Coverage Matrix

The tactics and techniques covered by our current detection rules are mapped below:

| Tactic | Technique ID | Technique Name | Sigma Rule | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | `proc_access_win_lsass_susp_access.yml` | Active |
| **Execution** | `T1059.001` | PowerShell | `proc_creation_win_powershell_encoded.yml` | Active |
| **Persistence** | `T1053.005` | Scheduled Task/Job | `proc_creation_win_schtasks_creation.yml` | Active |
| **Impact** | `T1490` | Inhibit System Recovery (Ransomware) | `proc_creation_win_vssadmin_delete_shadows.yml` | Active |

## Validation with Golden Dataset
To avoid reinventing the wheel and to ensure industry-standard calibration, the **OTRF Mordor** open-source dataset is utilized in this project. Our rules pass through rigorous Security QA checks using real-world (APT29, etc.) simulation logs located in the `/tests/dataset/` directory.

## How to Run Locally

To test the project in your own environment or to manually generate SIEM queries:

```bash
# Install dependencies
pip install sigma-cli
sigma plugin install splunk elasticsearch sysmon

# Convert all rules to Splunk SPL
sigma convert -t splunk -p sysmon rules/sigma/

# Convert to Elasticsearch (Lucene)
sigma convert -t lucene -p sysmon rules/sigma/
```

---

[TR]
# Detection-as-Code (DaC) Factory: Sigma Pack for Windows Security

> **Transforming threat hunting from a manual task into a continuous engineering pipeline.**

## Proje Vizyonu (Ruleset Philosophy)
Modern Güvenlik Operasyon Merkezleri (SOC), kural yazımını ve test süreçlerini manuel olarak yönetmenin ötesine geçmelidir. Bu proje, geleneksel SIEM sorgu yazarlığını bir **Yazılım Mühendisliği (CI/CD)** disiplinine dönüştürmek amacıyla "Detection-as-Code" (DaC) felsefesiyle inşa edilmiştir. 

Amacımız; platform bağımsız (vendor-agnostic) Sigma kuralları yazmak, bu kuralları sektör standardı olan **Mordor APT simülasyon logları** ile otomatik olarak test etmek ve GitHub Actions aracılığıyla saniyeler içinde Splunk (SPL) ve Elasticsearch (Lucene/KQL) dillerine dönüştürmektir.

## Sistem Mimarisi (Pipeline Otomasyonu)

1. **Code:** Yeni tehdit istihbaratı (CTI) YAML formatında (Sigma) yazılır.
2. **Commit:** Kod GitHub'a pushlanır.
3. **CI/CD (GitHub Actions):** 
   - YAML syntax kontrolü yapılır (Linting).
   - Mantıksal doğrulama gerçekleştirilir.
   - Kurallar otomatik olarak `/build` klasörüne **Splunk** ve **Elasticsearch** dilleri için derlenir (Build).
4. **Deploy:** Üretilen sorgular SIEM sistemlerine entegre edilmeye hazırdır.

## MITRE ATT&CK Kapsam Matrisi

Mevcut tespit kurallarımızın kapsadığı taktik ve teknikler aşağıda haritalandırılmıştır:

| Taktik (Tactic) | Teknik ID | Teknik Adı | Sigma Kuralı | Durum |
| :--- | :--- | :--- | :--- | :---: |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | `proc_access_win_lsass_susp_access.yml` | Aktif |
| **Execution** | `T1059.001` | PowerShell | `proc_creation_win_powershell_encoded.yml` | Aktif |
| **Persistence** | `T1053.005` | Scheduled Task/Job | `proc_creation_win_schtasks_creation.yml` | Aktif |
| **Impact** | `T1490` | Inhibit System Recovery (Ransomware) | `proc_creation_win_vssadmin_delete_shadows.yml` | Aktif |

## Altın Veri Seti (Golden Dataset) İle Doğrulama
Bu projede tekerleği yeniden icat etmemek ve endüstri standartlarında kalibrasyon sağlamak için **OTRF Mordor** açık kaynak veri seti kullanılmıştır. Kurallarımız, `/tests/dataset/` dizinindeki gerçek dünya (APT29 vb.) simülasyonlarına ait loglar üzerinde kalite kontrolünden (Security QA) geçmektedir.

## Nasıl Çalıştırılır?

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