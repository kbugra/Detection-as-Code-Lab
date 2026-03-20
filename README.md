[EN]
# Detection-as-Code (DaC) Factory: Sigma Pack for Windows Security

*The Turkish (TR) version is below.*

> **Transforming threat hunting from a manual task into a continuous engineering pipeline.**

## Project Vision
This repository treats detection engineering as code. Sigma rules are versioned, validated against curated attack/benign fixtures, and automatically compiled into SIEM-ready queries through GitHub Actions.

## What This Repository Actually Does
1. Write vendor-agnostic Sigma rules under `/rules/sigma/`.
2. Validate those rules against positive and negative fixtures under `/tests/dataset/`.
3. Run syntax checks with Sigma CLI.
4. Build Splunk SPL and Elasticsearch Lucene outputs into `/build/`.
5. Upload generated artifacts from CI for downstream SIEM use.

## Validation Model
The validation workflow is driven by `/tests/validation_cases.json` and executed by `python tools/validate_datasets.py`.

- Positive fixtures ensure each rule fires on the intended attack sample.
- Negative fixtures ensure the same rule does not fire on curated benign activity.
- The dataset folder includes Mordor-style logs and lightweight lab fixtures formatted as Sysmon-like JSON/JSONL for deterministic CI validation.
- Enriched fixtures such as `mordor_lsass_dump.json` and `schtasks_create.json` contain small event sequences instead of a single alerting row, so rules are tested with realistic context.

## Repository Layout

```text
rules/sigma/            Sigma detection rules
tests/dataset/          Positive and negative datasets
tests/validation_cases.json
tools/validate_datasets.py
tools/run_sigma_cli.py  Offline-safe sigma wrapper
tools/build_sigma.py    Build helper for SIEM outputs
build/                  Generated artifacts
```

## MITRE ATT&CK Coverage Matrix

| Tactic | Technique ID | Technique Name | Sigma Rule | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | `proc_access_win_lsass_susp_access.yml` | Active |
| **Execution** | `T1059.001` | PowerShell Encoded Command | `proc_creation_win_powershell_encoded.yml` | Active |
| **Persistence** | `T1053.005` | Scheduled Task/Job | `proc_creation_win_schtasks_creation.yml` | Active |
| **Impact** | `T1490` | Inhibit System Recovery | `proc_creation_win_vssadmin_delete_shadows.yml` | Active |

## Local Usage

### 1. Run fixture validation
```bash
python tools/validate_datasets.py
```

### 2. Install Sigma CLI for lint/build
```bash
pip install sigma-cli
python tools/run_sigma_cli.py plugin install splunk
python tools/run_sigma_cli.py plugin install elasticsearch
python tools/run_sigma_cli.py plugin install sysmon
```

`tools/run_sigma_cli.py` is used instead of calling `sigma` directly so the project can run in restricted environments without depending on user-profile cache paths or live MITRE metadata downloads.

### 3. Run Sigma syntax checks
```bash
python tools/run_sigma_cli.py check rules/sigma/
```

### 4. Build SIEM outputs
```bash
python tools/build_sigma.py
```

Generated files:

- `build/splunk/windows_detections.spl`
- `build/elastic/windows_detections.txt`

`build/` is intentionally generated and not committed to git.

## CI/CD Flow
The GitHub Actions pipeline in `/.github/workflows/sigma_pipeline.yml` performs:

1. Fixture validation
2. Sigma syntax/lint checks
3. Splunk and Elasticsearch builds
4. Artifact upload

---

[TR]
# Detection-as-Code (DaC) Factory: Windows Security için Sigma Paketi

> **Threat hunting sürecini manuel iş yükünden sürekli çalışan bir mühendislik pipeline’ına dönüştürmek.**

## Proje Vizyonu
Bu repo detection engineering sürecini kod gibi ele alır. Sigma kuralları versiyonlanır, saldırı ve benign fixture’lar üzerinde doğrulanır, ardından GitHub Actions ile SIEM’e hazır sorgulara dönüştürülür.

## Bu Repo Gerçekte Ne Yapıyor?
1. Vendor-agnostic Sigma kuralları `/rules/sigma/` altında tutulur.
2. Kurallar `/tests/dataset/` altındaki pozitif ve negatif fixture’lara karşı test edilir.
3. Sigma CLI ile syntax/lint kontrolü yapılır.
4. Splunk SPL ve Elasticsearch Lucene çıktıları `/build/` altına üretilir.
5. CI çıktıları artifact olarak yüklenir ve SIEM entegrasyonu için hazır hale gelir.

## Doğrulama Modeli
Doğrulama akışı `/tests/validation_cases.json` ile tanımlanır ve `python tools/validate_datasets.py` ile çalıştırılır.

- Pozitif fixture’lar her kuralın hedeflenen saldırı örneğinde tetiklendiğini doğrular.
- Negatif fixture’lar aynı kuralın benign aktivitede tetiklenmediğini doğrular.
- Dataset klasörü, deterministik CI doğrulaması için Mordor tarzı loglar ve Sysmon benzeri JSON/JSONL formatında hafif lab fixture’ları içerir.
- `mordor_lsass_dump.json` ve `schtasks_create.json` gibi zenginleştirilmiş fixture’lar tek event yerine küçük bir event akışı içerir; böylece kurallar daha gerçekçi bağlamda test edilir.

## Repo Yapısı

```text
rules/sigma/            Sigma kuralları
tests/dataset/          Pozitif ve negatif datasetler
tests/validation_cases.json
tools/validate_datasets.py
tools/run_sigma_cli.py  Offline uyumlu sigma wrapper'ı
tools/build_sigma.py    SIEM build helper'ı
build/                  Üretilen artifact'ler
```

## MITRE ATT&CK Kapsam Matrisi

| Taktik | Teknik ID | Teknik Adı | Sigma Kuralı | Durum |
| :--- | :--- | :--- | :--- | :---: |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | `proc_access_win_lsass_susp_access.yml` | Aktif |
| **Execution** | `T1059.001` | PowerShell Encoded Command | `proc_creation_win_powershell_encoded.yml` | Aktif |
| **Persistence** | `T1053.005` | Scheduled Task/Job | `proc_creation_win_schtasks_creation.yml` | Aktif |
| **Impact** | `T1490` | Inhibit System Recovery | `proc_creation_win_vssadmin_delete_shadows.yml` | Aktif |

## Lokal Kullanım

### 1. Fixture validation çalıştır
```bash
python tools/validate_datasets.py
```

### 2. Sigma CLI kur
```bash
pip install sigma-cli
python tools/run_sigma_cli.py plugin install splunk
python tools/run_sigma_cli.py plugin install elasticsearch
python tools/run_sigma_cli.py plugin install sysmon
```

`sigma` komutunu doğrudan çağırmak yerine `tools/run_sigma_cli.py` kullanılıyor; bunun nedeni kısıtlı ortamlarda kullanıcı profilindeki cache dizinlerine veya canlı MITRE metadata indirmelerine bağımlı kalmamak.

### 3. Sigma syntax kontrolü çalıştır
```bash
python tools/run_sigma_cli.py check rules/sigma/
```

### 4. SIEM çıktıları üret
```bash
python tools/build_sigma.py
```

Üretilen dosyalar:

- `build/splunk/windows_detections.spl`
- `build/elastic/windows_detections.txt`

`build/` klasörü bilinçli olarak generate edilir ve git’e commit edilmez.

## CI/CD Akışı
`/.github/workflows/sigma_pipeline.yml` aşağıdaki adımları çalıştırır:

1. Fixture validation
2. Sigma syntax/lint kontrolü
3. Splunk ve Elasticsearch build
4. Artifact upload
