# Enterprise TLS/SSL Security Assessment Laboratory

## 🎯 **Assessment Overview**
This comprehensive laboratory demonstrates professional TLS/SSL security assessment using testssl.sh for enterprise environments, covering certificate validation, cipher strength analysis, protocol security evaluation, and compliance verification for mission-critical web services.

## 🔒 **TLS/SSL Security Assessment Framework**

### **Security Assessment Methodology**
```
1. Reconnaissance & Discovery
   ├── Service enumeration and identification
   ├── TLS endpoint discovery
   └── Initial security posture assessment

2. Certificate Analysis
   ├── Certificate chain validation
   ├── Expiration and renewal tracking
   └── Certificate authority verification

3. Protocol Security Evaluation
   ├── Supported protocol versions
   ├── Cipher suite analysis
   └── Key exchange mechanisms

4. Vulnerability Assessment
   ├── Known vulnerability scanning
   ├── Configuration weakness detection
   └── Compliance gap analysis

5. Compliance Verification
   ├── Industry standard compliance (PCI DSS, HIPAA)
   ├── Best practice implementation
   └── Regulatory requirement validation
```

## 🌐 **Scenario 1: Enterprise Web Application Security Assessment**

### **Business Context**
Large enterprise requires comprehensive TLS/SSL security assessment of customer-facing web applications to ensure data protection compliance and prevent security breaches.

### **Assessment Infrastructure**
```bash
# Target applications for assessment
Corporate Website:     https://www.company.com
Customer Portal:       https://portal.company.com
API Gateway:          https://api.company.com
E-commerce Platform:  https://shop.company.com
Partner Extranet:     https://partners.company.com
```

### **Professional Assessment Procedures**

#### **Comprehensive TLS/SSL Analysis**
```bash
# Basic security assessment
./testssl.sh --quiet --color 0 https://www.company.com

# Detailed security assessment with full reporting
./testssl.sh \
    --quiet \
    --color 0 \
    --html \
    --htmlfile /var/log/testssl/company_assessment.html \
    --logfile /var/log/testssl/company_assessment.log \
    --jsonfile /var/log/testssl/company_assessment.json \
    https://www.company.com

# Certificate-focused assessment
./testssl.sh \
    --quiet \
    --cert-transparency \
    --cert-compression \
    --cert-signature-algo \
    --htmlfile /var/log/testssl/company_certificate_analysis.html \
    https://www.company.com
```

#### **Vulnerability-Specific Testing**
```bash
# Heartbleed vulnerability check
./testssl.sh --heartbleed https://www.company.com

# BEAST attack vulnerability
./testssl.sh --beast https://www.company.com

# CRIME compression attack
./testssl.sh --crime https://www.company.com

# BREACH vulnerability assessment
./testssl.sh --breach https://www.company.com

# POODLE attack vulnerability
./testssl.sh --poodle https://www.company.com

# TLS_FALLBACK_SCSV support
./testssl.sh --fallback https://www.company.com

# Sweet32 birthday attack
./testssl.sh --sweet32 https://www.company.com

# FREAK attack vulnerability
./testssl.sh --freak https://www.company.com

# LOGJAM vulnerability
./testssl.sh --logjam https://www.company.com

# DROWN attack vulnerability
./testssl.sh --drown https://www.company.com

# Robot attack vulnerability
./testssl.sh --robot https://www.company.com
```

#### **Protocol and Cipher Analysis**
```bash
# Protocol version analysis
./testssl.sh --protocols https://www.company.com

# Cipher suite enumeration
./testssl.sh --ciphers https://www.company.com

# Perfect Forward Secrecy analysis
./testssl.sh --pfs https://www.company.com

# Server preferences analysis
./testssl.sh --server-preference https://www.company.com

# Server defaults analysis
./testssl.sh --server-defaults https://www.company.com

# Header security analysis
./testssl.sh --headers https://www.company.com
```

### **Enterprise Batch Assessment Script**
```bash
#!/bin/bash
# Enterprise TLS/SSL Security Assessment Automation

# Configuration
ASSESSMENT_DATE=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="/var/log/testssl/enterprise_assessment_${ASSESSMENT_DATE}"
mkdir -p $RESULTS_DIR

# Target applications
TARGETS=(
    "https://www.company.com"
    "https://portal.company.com"
    "https://api.company.com"
    "https://shop.company.com"
    "https://partners.company.com"
)

# Assessment configuration
TESTSSL_OPTS="--quiet --color 0 --html --jsonfile-pretty"

echo "=== Enterprise TLS/SSL Security Assessment Started ===" | tee $RESULTS_DIR/assessment.log
echo "Assessment Date: $(date)" | tee -a $RESULTS_DIR/assessment.log
echo "Total Targets: ${#TARGETS[@]}" | tee -a $RESULTS_DIR/assessment.log

for target in "${TARGETS[@]}"; do
    # Extract hostname for file naming
    hostname=$(echo $target | sed 's|https://||' | sed 's|/.*||')
    echo "Assessing: $hostname" | tee -a $RESULTS_DIR/assessment.log
    
    # Comprehensive assessment
    ./testssl.sh $TESTSSL_OPTS \
        --htmlfile $RESULTS_DIR/${hostname}_full_assessment.html \
        --jsonfile $RESULTS_DIR/${hostname}_full_assessment.json \
        --logfile $RESULTS_DIR/${hostname}_full_assessment.log \
        $target
    
    # Vulnerability-specific checks
    echo "Running vulnerability checks for $hostname..." | tee -a $RESULTS_DIR/assessment.log
    ./testssl.sh --quiet --color 0 \
        --heartbleed --beast --crime --breach --poodle \
        --fallback --sweet32 --freak --logjam --drown --robot \
        --jsonfile $RESULTS_DIR/${hostname}_vulnerabilities.json \
        $target
    
    # Certificate analysis
    echo "Analyzing certificates for $hostname..." | tee -a $RESULTS_DIR/assessment.log
    ./testssl.sh --quiet --color 0 \
        --cert-transparency --cert-compression --cert-signature-algo \
        --jsonfile $RESULTS_DIR/${hostname}_certificates.json \
        $target
    
    # Protocol and cipher analysis
    echo "Analyzing protocols and ciphers for $hostname..." | tee -a $RESULTS_DIR/assessment.log
    ./testssl.sh --quiet --color 0 \
        --protocols --ciphers --pfs --server-preference \
        --jsonfile $RESULTS_DIR/${hostname}_protocols.json \
        $target
    
    echo "Assessment completed for $hostname" | tee -a $RESULTS_DIR/assessment.log
    echo "----------------------------------------" | tee -a $RESULTS_DIR/assessment.log
done

echo "=== Enterprise Assessment Completed ===" | tee -a $RESULTS_DIR/assessment.log
echo "Results directory: $RESULTS_DIR" | tee -a $RESULTS_DIR/assessment.log
```

## 🏢 **Scenario 2: PCI DSS Compliance Assessment**

### **Compliance Context**
E-commerce platform requires PCI DSS compliance validation for credit card processing, focusing on TLS/SSL security requirements and data protection standards.

### **PCI DSS TLS/SSL Requirements Assessment**
```bash
# PCI DSS 4.1 - Strong cryptography implementation
./testssl.sh \
    --protocols \
    --ciphers \
    --pfs \
    --server-preference \
    --jsonfile /var/log/testssl/pci_dss_cryptography.json \
    https://shop.company.com

# PCI DSS 2.3 - Default passwords and security parameters
./testssl.sh \
    --server-defaults \
    --headers \
    --jsonfile /var/log/testssl/pci_dss_defaults.json \
    https://shop.company.com

# PCI DSS 6.2 - Known vulnerabilities assessment
./testssl.sh \
    --heartbleed --beast --crime --breach --poodle \
    --fallback --sweet32 --freak --logjam --drown --robot \
    --jsonfile /var/log/testssl/pci_dss_vulnerabilities.json \
    https://shop.company.com
```

### **PCI DSS Compliance Report Generation**
```python
#!/usr/bin/env python3
"""
PCI DSS TLS/SSL Compliance Assessment Report Generator
"""

import json
import sys
from datetime import datetime

def analyze_pci_compliance(json_file):
    """Analyze testssl.sh results for PCI DSS compliance"""
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None
    
    compliance_report = {
        'assessment_date': datetime.now().isoformat(),
        'target': data.get('target_host', 'Unknown'),
        'pci_dss_requirements': {},
        'compliance_status': 'UNKNOWN',
        'findings': [],
        'recommendations': []
    }
    
    # PCI DSS 4.1 - Strong Cryptography
    protocols = data.get('protocols', [])
    weak_protocols = ['SSLv2', 'SSLv3', 'TLS 1.0', 'TLS 1.1']
    
    strong_crypto_compliant = True
    for protocol in protocols:
        if any(weak in protocol.get('id', '') for weak in weak_protocols):
            if protocol.get('finding', '').lower() == 'offered':
                strong_crypto_compliant = False
                compliance_report['findings'].append(
                    f"Weak protocol {protocol.get('id')} is enabled"
                )
    
    compliance_report['pci_dss_requirements']['4.1_strong_cryptography'] = {
        'compliant': strong_crypto_compliant,
        'requirement': 'Use strong cryptography and security protocols'
    }
    
    # PCI DSS 2.3 - Default passwords and security parameters
    server_defaults = data.get('server_defaults', [])
    default_compliant = True
    
    for default in server_defaults:
        if 'default' in default.get('finding', '').lower():
            default_compliant = False
            compliance_report['findings'].append(
                f"Default configuration detected: {default.get('id')}"
            )
    
    compliance_report['pci_dss_requirements']['2.3_default_security'] = {
        'compliant': default_compliant,
        'requirement': 'Do not use vendor-supplied defaults for system passwords'
    }
    
    # PCI DSS 6.2 - Known vulnerabilities
    vulnerabilities = data.get('vulnerabilities', [])
    vuln_compliant = True
    
    critical_vulns = ['HEARTBLEED', 'BEAST', 'CRIME', 'POODLE', 'FREAK', 'LOGJAM', 'DROWN']
    for vuln in vulnerabilities:
        vuln_id = vuln.get('id', '').upper()
        if any(critical in vuln_id for critical in critical_vulns):
            if vuln.get('finding', '').lower() in ['vulnerable', 'likely vulnerable']:
                vuln_compliant = False
                compliance_report['findings'].append(
                    f"Critical vulnerability detected: {vuln.get('id')}"
                )
    
    compliance_report['pci_dss_requirements']['6.2_known_vulnerabilities'] = {
        'compliant': vuln_compliant,
        'requirement': 'Ensure all systems are protected from known vulnerabilities'
    }
    
    # Overall compliance determination
    all_requirements = [
        compliance_report['pci_dss_requirements']['4.1_strong_cryptography']['compliant'],
        compliance_report['pci_dss_requirements']['2.3_default_security']['compliant'],
        compliance_report['pci_dss_requirements']['6.2_known_vulnerabilities']['compliant']
    ]
    
    compliance_report['compliance_status'] = 'COMPLIANT' if all(all_requirements) else 'NON-COMPLIANT'
    
    # Generate recommendations
    if not strong_crypto_compliant:
        compliance_report['recommendations'].append(
            "Disable weak SSL/TLS protocols (SSLv2, SSLv3, TLS 1.0, TLS 1.1)"
        )
        compliance_report['recommendations'].append(
            "Enable only TLS 1.2 and TLS 1.3 with strong cipher suites"
        )
    
    if not default_compliant:
        compliance_report['recommendations'].append(
            "Review and harden server default configurations"
        )
        compliance_report['recommendations'].append(
            "Implement custom security headers and configurations"
        )
    
    if not vuln_compliant:
        compliance_report['recommendations'].append(
            "Apply security patches to address identified vulnerabilities"
        )
        compliance_report['recommendations'].append(
            "Implement regular vulnerability scanning and remediation processes"
        )
    
    return compliance_report

def generate_pci_report(compliance_data, output_file):
    """Generate PCI DSS compliance report"""
    
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PCI DSS TLS/SSL Compliance Assessment Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .compliant {{ color: green; font-weight: bold; }}
            .non-compliant {{ color: red; font-weight: bold; }}
            .finding {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            .recommendation {{ background: #d1ecf1; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>PCI DSS TLS/SSL Compliance Assessment</h1>
            <p><strong>Target:</strong> {compliance_data['target']}</p>
            <p><strong>Assessment Date:</strong> {compliance_data['assessment_date']}</p>
            <p><strong>Overall Status:</strong> 
                <span class="{'compliant' if compliance_data['compliance_status'] == 'COMPLIANT' else 'non-compliant'}">
                    {compliance_data['compliance_status']}
                </span>
            </p>
        </div>
        
        <h2>PCI DSS Requirements Assessment</h2>
    """
    
    for req_id, req_data in compliance_data['pci_dss_requirements'].items():
        status_class = 'compliant' if req_data['compliant'] else 'non-compliant'
        status_text = 'COMPLIANT' if req_data['compliant'] else 'NON-COMPLIANT'
        
        report_html += f"""
        <h3>{req_id.replace('_', ' ').title()}</h3>
        <p><strong>Requirement:</strong> {req_data['requirement']}</p>
        <p><strong>Status:</strong> <span class="{status_class}">{status_text}</span></p>
        """
    
    if compliance_data['findings']:
        report_html += "<h2>Security Findings</h2>"
        for finding in compliance_data['findings']:
            report_html += f'<div class="finding">⚠️ {finding}</div>'
    
    if compliance_data['recommendations']:
        report_html += "<h2>Recommendations</h2>"
        for recommendation in compliance_data['recommendations']:
            report_html += f'<div class="recommendation">💡 {recommendation}</div>'
    
    report_html += """
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(report_html)
    
    print(f"PCI DSS compliance report generated: {output_file}")

# Usage example
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pci_compliance_analyzer.py <testssl_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    compliance_data = analyze_pci_compliance(json_file)
    
    if compliance_data:
        output_file = f"pci_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        generate_pci_report(compliance_data, output_file)
        
        print(f"\nPCI DSS Compliance Status: {compliance_data['compliance_status']}")
        if compliance_data['findings']:
            print(f"Security Findings: {len(compliance_data['findings'])}")
        if compliance_data['recommendations']:
            print(f"Recommendations: {len(compliance_data['recommendations'])}")
```

## 🔍 **Scenario 3: Continuous Security Monitoring**

### **Automated Security Monitoring Framework**
```bash
#!/bin/bash
# Continuous TLS/SSL Security Monitoring

MONITORING_CONFIG="/etc/testssl/monitoring.conf"
RESULTS_DIR="/var/log/testssl/continuous_monitoring"
ALERT_THRESHOLD_DAYS=30

# Load monitoring configuration
source $MONITORING_CONFIG

# Create results directory
mkdir -p $RESULTS_DIR

# Function to check certificate expiration
check_certificate_expiration() {
    local target=$1
    local hostname=$(echo $target | sed 's|https://||' | sed 's|/.*||')
    
    # Get certificate expiration
    cert_info=$(./testssl.sh --quiet --color 0 --cert-transparency $target 2>/dev/null | grep "Certificate Validity")
    expiry_date=$(echo "$cert_info" | grep "expires" | sed 's/.*expires //' | sed 's/ .*//')
    
    # Calculate days until expiration
    if [ -n "$expiry_date" ]; then
        expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null)
        current_epoch=$(date +%s)
        days_until_expiry=$(( ($expiry_epoch - $current_epoch) / 86400 ))
        
        echo "$hostname,$expiry_date,$days_until_expiry" >> $RESULTS_DIR/certificate_monitoring.csv
        
        # Alert if certificate expires soon
        if [ $days_until_expiry -lt $ALERT_THRESHOLD_DAYS ]; then
            echo "ALERT: Certificate for $hostname expires in $days_until_expiry days" | \
                mail -s "Certificate Expiration Alert" security-team@company.com
        fi
    fi
}

# Function to check for new vulnerabilities
check_vulnerabilities() {
    local target=$1
    local hostname=$(echo $target | sed 's|https://||' | sed 's|/.*||')
    local current_date=$(date +%Y%m%d)
    
    # Run vulnerability assessment
    ./testssl.sh --quiet --color 0 \
        --heartbleed --beast --crime --breach --poodle \
        --fallback --sweet32 --freak --logjam --drown --robot \
        --jsonfile $RESULTS_DIR/${hostname}_vulns_${current_date}.json \
        $target
    
    # Check for critical vulnerabilities
    if grep -q "vulnerable" $RESULTS_DIR/${hostname}_vulns_${current_date}.json; then
        echo "ALERT: New vulnerabilities detected for $hostname" | \
            mail -s "TLS/SSL Vulnerability Alert" security-team@company.com
    fi
}

# Function to monitor configuration changes
monitor_configuration_changes() {
    local target=$1
    local hostname=$(echo $target | sed 's|https://||' | sed 's|/.*||')
    local current_date=$(date +%Y%m%d)
    local previous_config="$RESULTS_DIR/${hostname}_config_previous.json"
    local current_config="$RESULTS_DIR/${hostname}_config_${current_date}.json"
    
    # Get current configuration
    ./testssl.sh --quiet --color 0 \
        --protocols --ciphers --server-preference \
        --jsonfile $current_config \
        $target
    
    # Compare with previous configuration
    if [ -f "$previous_config" ]; then
        if ! diff -q "$previous_config" "$current_config" > /dev/null; then
            echo "ALERT: TLS/SSL configuration changed for $hostname" | \
                mail -s "TLS/SSL Configuration Change Alert" security-team@company.com
        fi
    fi
    
    # Update previous configuration
    cp "$current_config" "$previous_config"
}

# Main monitoring loop
echo "Starting continuous TLS/SSL security monitoring..."
for target in "${MONITORING_TARGETS[@]}"; do
    echo "Monitoring: $target"
    
    check_certificate_expiration "$target"
    check_vulnerabilities "$target"
    monitor_configuration_changes "$target"
    
    echo "Monitoring completed for $target"
done

echo "Continuous monitoring cycle completed at $(date)"
```

## 📊 **Professional Reporting and Documentation**

### **Executive Security Dashboard**
```python
#!/usr/bin/env python3
"""
Executive TLS/SSL Security Dashboard Generator
"""

import json
import glob
import statistics
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class TLSSecurityDashboard:
    def __init__(self, results_directory):
        self.results_dir = results_directory
        self.security_metrics = {}
        
    def load_assessment_results(self):
        """Load all testssl.sh assessment results"""
        json_files = glob.glob(f"{self.results_dir}/*_full_assessment.json")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    hostname = data.get('target_host', 'unknown')
                    self.security_metrics[hostname] = self.analyze_security_posture(data)
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
    
    def analyze_security_posture(self, assessment_data):
        """Analyze security posture from assessment data"""
        metrics = {
            'overall_grade': 'UNKNOWN',
            'protocol_security': 0,
            'cipher_strength': 0,
            'certificate_security': 0,
            'vulnerability_count': 0,
            'compliance_score': 0
        }
        
        # Protocol security analysis
        protocols = assessment_data.get('protocols', [])
        secure_protocols = sum(1 for p in protocols if 'TLS 1.2' in p.get('id', '') or 'TLS 1.3' in p.get('id', ''))
        total_protocols = len(protocols)
        metrics['protocol_security'] = (secure_protocols / total_protocols * 100) if total_protocols > 0 else 0
        
        # Cipher strength analysis
        ciphers = assessment_data.get('ciphers', [])
        strong_ciphers = sum(1 for c in ciphers if 'HIGH' in c.get('finding', ''))
        total_ciphers = len(ciphers)
        metrics['cipher_strength'] = (strong_ciphers / total_ciphers * 100) if total_ciphers > 0 else 0
        
        # Vulnerability count
        vulnerabilities = assessment_data.get('vulnerabilities', [])
        critical_vulns = sum(1 for v in vulnerabilities if v.get('severity', '').upper() in ['HIGH', 'CRITICAL'])
        metrics['vulnerability_count'] = critical_vulns
        
        # Overall grade calculation
        avg_security = (metrics['protocol_security'] + metrics['cipher_strength']) / 2
        if avg_security >= 90 and metrics['vulnerability_count'] == 0:
            metrics['overall_grade'] = 'A+'
        elif avg_security >= 80 and metrics['vulnerability_count'] <= 1:
            metrics['overall_grade'] = 'A'
        elif avg_security >= 70 and metrics['vulnerability_count'] <= 2:
            metrics['overall_grade'] = 'B'
        elif avg_security >= 60:
            metrics['overall_grade'] = 'C'
        else:
            metrics['overall_grade'] = 'F'
        
        return metrics
    
    def generate_security_dashboard(self, output_file):
        """Generate executive security dashboard"""
        # Calculate overall statistics
        total_hosts = len(self.security_metrics)
        if total_hosts == 0:
            print("No security metrics available")
            return
        
        grade_distribution = {}
        total_vulnerabilities = 0
        avg_protocol_security = 0
        avg_cipher_strength = 0
        
        for hostname, metrics in self.security_metrics.items():
            grade = metrics['overall_grade']
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
            total_vulnerabilities += metrics['vulnerability_count']
            avg_protocol_security += metrics['protocol_security']
            avg_cipher_strength += metrics['cipher_strength']
        
        avg_protocol_security /= total_hosts
        avg_cipher_strength /= total_hosts
        
        # Generate HTML dashboard
        dashboard_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enterprise TLS/SSL Security Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .dashboard {{ max-width: 1200px; margin: 0 auto; }}
                .card {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric {{ display: inline-block; text-align: center; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
                .metric-value {{ font-size: 2em; font-weight: bold; }}
                .grade-a {{ color: #28a745; }}
                .grade-b {{ color: #ffc107; }}
                .grade-c {{ color: #fd7e14; }}
                .grade-f {{ color: #dc3545; }}
                .vulnerability-critical {{ background: #f8d7da; color: #721c24; }}
                .host-list {{ max-height: 300px; overflow-y: auto; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="card">
                    <h1>Enterprise TLS/SSL Security Dashboard</h1>
                    <p><strong>Assessment Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Total Hosts Assessed:</strong> {total_hosts}</p>
                </div>
                
                <div class="card">
                    <h2>Security Metrics Overview</h2>
                    <div class="metric">
                        <div class="metric-value">{avg_protocol_security:.1f}%</div>
                        <div>Protocol Security</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{avg_cipher_strength:.1f}%</div>
                        <div>Cipher Strength</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value {'vulnerability-critical' if total_vulnerabilities > 0 else ''}">{total_vulnerabilities}</div>
                        <div>Total Vulnerabilities</div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Security Grade Distribution</h2>
        """
        
        for grade, count in sorted(grade_distribution.items()):
            percentage = (count / total_hosts) * 100
            grade_class = f"grade-{grade.lower().replace('+', '')}"
            dashboard_html += f"""
                    <div class="metric">
                        <div class="metric-value {grade_class}">{count}</div>
                        <div>Grade {grade} ({percentage:.1f}%)</div>
                    </div>
            """
        
        dashboard_html += """
                </div>
                
                <div class="card">
                    <h2>Host Security Details</h2>
                    <div class="host-list">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: #e9ecef;">
                                    <th style="padding: 10px; text-align: left;">Hostname</th>
                                    <th style="padding: 10px; text-align: center;">Grade</th>
                                    <th style="padding: 10px; text-align: center;">Protocol Security</th>
                                    <th style="padding: 10px; text-align: center;">Cipher Strength</th>
                                    <th style="padding: 10px; text-align: center;">Vulnerabilities</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for hostname, metrics in sorted(self.security_metrics.items()):
            grade_class = f"grade-{metrics['overall_grade'].lower().replace('+', '')}"
            vuln_class = 'vulnerability-critical' if metrics['vulnerability_count'] > 0 else ''
            
            dashboard_html += f"""
                                <tr>
                                    <td style="padding: 8px;">{hostname}</td>
                                    <td style="padding: 8px; text-align: center;" class="{grade_class}"><strong>{metrics['overall_grade']}</strong></td>
                                    <td style="padding: 8px; text-align: center;">{metrics['protocol_security']:.1f}%</td>
                                    <td style="padding: 8px; text-align: center;">{metrics['cipher_strength']:.1f}%</td>
                                    <td style="padding: 8px; text-align: center;" class="{vuln_class}"><strong>{metrics['vulnerability_count']}</strong></td>
                                </tr>
            """
        
        dashboard_html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(dashboard_html)
        
        print(f"Security dashboard generated: {output_file}")

# Usage example
if __name__ == "__main__":
    dashboard = TLSSecurityDashboard('/var/log/testssl/enterprise_assessment_latest')
    dashboard.load_assessment_results()
    dashboard.generate_security_dashboard('enterprise_tls_security_dashboard.html')
```

## 🎯 **Best Practices and Quality Assurance**

### **Professional Assessment Standards**
```bash
# Enterprise assessment checklist
□ Comprehensive protocol version testing (SSLv2, SSLv3, TLS 1.0-1.3)
□ Complete cipher suite analysis and strength assessment
□ Certificate chain validation and expiration monitoring
□ Known vulnerability scanning (HEARTBLEED, BEAST, CRIME, etc.)
□ Perfect Forward Secrecy (PFS) implementation verification
□ HTTP Strict Transport Security (HSTS) configuration check
□ Certificate Transparency (CT) compliance verification
□ Server preference and default configuration analysis
```

### **Compliance and Regulatory Requirements**
```bash
# Industry compliance validation
PCI DSS 4.1:     Strong cryptography implementation
HIPAA Security:  Data encryption in transit requirements
SOX Compliance:  Financial data protection standards
ISO 27001:       Information security management standards
NIST Guidelines: Cryptographic standards and best practices
GDPR Article 32: Security of processing requirements
```

---

**Related Assessments**: [Wireshark TLS Analysis](../../wireshark/protocol-labs/), [Network Security](../../gns3-labs/), [Performance Impact](../../iperf3/)
