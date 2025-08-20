#!/usr/bin/env python3
"""
Enterprise TLS/SSL Security Assessment Automation
Professional-grade SSL/TLS testing with comprehensive reporting and compliance validation
"""

import json
import subprocess
import argparse
import logging
import concurrent.futures
import time
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import yaml

class EnterpriseSSLScanner:
    def __init__(self, config_file=None):
        self.setup_logging()
        self.config = self.load_config(config_file) if config_file else {}
        self.results = {}
        self.testssl_path = self.config.get('testssl_path', './testssl.sh')
        
    def setup_logging(self):
        """Configure comprehensive logging for enterprise environments"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('/var/log/testssl/ssl_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                self.logger.info(f"Configuration loaded from {config_file}")
                return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def run_testssl_assessment(self, target, assessment_type='comprehensive'):
        """Execute testssl.sh assessment with specified parameters"""
        hostname = target.replace('https://', '').replace('http://', '').split('/')[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Base command
        cmd = [
            self.testssl_path,
            '--quiet',
            '--color', '0',
            '--jsonfile-pretty'
        ]
        
        # Assessment-specific parameters
        if assessment_type == 'comprehensive':
            cmd.extend([
                '--protocols',
                '--ciphers',
                '--pfs',
                '--server-preference',
                '--server-defaults',
                '--headers',
                '--cert-transparency',
                '--cert-compression',
                '--cert-signature-algo'
            ])
        elif assessment_type == 'vulnerabilities':
            cmd.extend([
                '--heartbleed',
                '--beast',
                '--crime',
                '--breach',
                '--poodle',
                '--fallback',
                '--sweet32',
                '--freak',
                '--logjam',
                '--drown',
                '--robot'
            ])
        elif assessment_type == 'quick':
            cmd.extend([
                '--protocols',
                '--server-defaults'
            ])
        
        # Output files
        json_file = f'/var/log/testssl/{hostname}_{assessment_type}_{timestamp}.json'
        html_file = f'/var/log/testssl/{hostname}_{assessment_type}_{timestamp}.html'
        log_file = f'/var/log/testssl/{hostname}_{assessment_type}_{timestamp}.log'
        
        cmd.extend([
            '--jsonfile', json_file,
            '--htmlfile', html_file,
            '--logfile', log_file,
            target
        ])
        
        try:
            self.logger.info(f"Starting {assessment_type} assessment for {hostname}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            
            if result.returncode == 0:
                self.logger.info(f"Assessment completed successfully for {hostname}")
                return {
                    'target': target,
                    'hostname': hostname,
                    'assessment_type': assessment_type,
                    'status': 'success',
                    'json_file': json_file,
                    'html_file': html_file,
                    'log_file': log_file,
                    'timestamp': timestamp
                }
            else:
                self.logger.error(f"Assessment failed for {hostname}: {result.stderr}")
                return {
                    'target': target,
                    'hostname': hostname,
                    'assessment_type': assessment_type,
                    'status': 'failed',
                    'error': result.stderr,
                    'timestamp': timestamp
                }
        
        except subprocess.TimeoutExpired:
            self.logger.error(f"Assessment timed out for {hostname}")
            return {
                'target': target,
                'hostname': hostname,
                'assessment_type': assessment_type,
                'status': 'timeout',
                'timestamp': timestamp
            }
        except Exception as e:
            self.logger.error(f"Error during assessment of {hostname}: {e}")
            return {
                'target': target,
                'hostname': hostname,
                'assessment_type': assessment_type,
                'status': 'error',
                'error': str(e),
                'timestamp': timestamp
            }
    
    def analyze_ssl_results(self, json_file):
        """Analyze testssl.sh JSON results for security metrics"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading JSON file {json_file}: {e}")
            return None
        
        analysis = {
            'target': data.get('target_host', 'unknown'),
            'assessment_time': data.get('startTime', ''),
            'security_metrics': {
                'overall_grade': 'UNKNOWN',
                'protocol_security_score': 0,
                'cipher_strength_score': 0,
                'certificate_score': 0,
                'vulnerability_count': 0,
                'critical_issues': []
            },
            'compliance': {
                'pci_dss_compliant': False,
                'hipaa_compliant': False,
                'nist_compliant': False
            },
            'recommendations': []
        }
        
        # Protocol analysis
        protocols = data.get('protocols', [])
        secure_protocols = 0
        insecure_protocols = []
        
        for protocol in protocols:
            protocol_id = protocol.get('id', '')
            finding = protocol.get('finding', '').lower()
            
            if finding == 'offered':
                if 'TLS 1.2' in protocol_id or 'TLS 1.3' in protocol_id:
                    secure_protocols += 1
                elif any(weak in protocol_id for weak in ['SSLv2', 'SSLv3', 'TLS 1.0', 'TLS 1.1']):
                    insecure_protocols.append(protocol_id)
                    analysis['security_metrics']['critical_issues'].append(f"Insecure protocol {protocol_id} enabled")
        
        total_protocols = len([p for p in protocols if p.get('finding', '').lower() == 'offered'])
        if total_protocols > 0:
            analysis['security_metrics']['protocol_security_score'] = (secure_protocols / total_protocols) * 100
        
        # Cipher analysis
        ciphers = data.get('ciphers', [])
        strong_ciphers = 0
        weak_ciphers = []
        
        for cipher in ciphers:
            finding = cipher.get('finding', '').lower()
            cipher_id = cipher.get('id', '')
            
            if 'high' in finding or 'aes' in finding.lower():
                strong_ciphers += 1
            elif any(weak in finding.lower() for weak in ['null', 'export', 'des', 'rc4']):
                weak_ciphers.append(cipher_id)
                analysis['security_metrics']['critical_issues'].append(f"Weak cipher {cipher_id} enabled")
        
        total_ciphers = len(ciphers)
        if total_ciphers > 0:
            analysis['security_metrics']['cipher_strength_score'] = (strong_ciphers / total_ciphers) * 100
        
        # Vulnerability analysis
        vulnerabilities = data.get('vulnerabilities', [])
        critical_vulns = 0
        
        for vuln in vulnerabilities:
            finding = vuln.get('finding', '').lower()
            vuln_id = vuln.get('id', '')
            
            if any(status in finding for status in ['vulnerable', 'likely vulnerable']):
                critical_vulns += 1
                analysis['security_metrics']['critical_issues'].append(f"Vulnerability detected: {vuln_id}")
        
        analysis['security_metrics']['vulnerability_count'] = critical_vulns
        
        # Certificate analysis
        cert_info = data.get('certificates', [])
        cert_score = 100  # Start with perfect score
        
        for cert in cert_info:
            if 'expired' in cert.get('finding', '').lower():
                cert_score -= 50
                analysis['security_metrics']['critical_issues'].append("Expired certificate detected")
            elif 'weak' in cert.get('finding', '').lower():
                cert_score -= 25
                analysis['security_metrics']['critical_issues'].append("Weak certificate signature detected")
        
        analysis['security_metrics']['certificate_score'] = max(0, cert_score)
        
        # Overall grade calculation
        avg_score = (
            analysis['security_metrics']['protocol_security_score'] +
            analysis['security_metrics']['cipher_strength_score'] +
            analysis['security_metrics']['certificate_score']
        ) / 3
        
        if avg_score >= 95 and critical_vulns == 0:
            analysis['security_metrics']['overall_grade'] = 'A+'
        elif avg_score >= 90 and critical_vulns <= 1:
            analysis['security_metrics']['overall_grade'] = 'A'
        elif avg_score >= 80 and critical_vulns <= 2:
            analysis['security_metrics']['overall_grade'] = 'B'
        elif avg_score >= 70:
            analysis['security_metrics']['overall_grade'] = 'C'
        elif avg_score >= 60:
            analysis['security_metrics']['overall_grade'] = 'D'
        else:
            analysis['security_metrics']['overall_grade'] = 'F'
        
        # Compliance analysis
        analysis['compliance']['pci_dss_compliant'] = (
            len(insecure_protocols) == 0 and
            len(weak_ciphers) == 0 and
            critical_vulns == 0
        )
        
        analysis['compliance']['hipaa_compliant'] = analysis['compliance']['pci_dss_compliant']
        analysis['compliance']['nist_compliant'] = analysis['compliance']['pci_dss_compliant']
        
        # Generate recommendations
        if insecure_protocols:
            analysis['recommendations'].append(
                f"Disable insecure protocols: {', '.join(insecure_protocols)}"
            )
        
        if weak_ciphers:
            analysis['recommendations'].append(
                f"Remove weak ciphers: {', '.join(weak_ciphers[:3])}..."
            )
        
        if critical_vulns > 0:
            analysis['recommendations'].append(
                "Apply security patches to address identified vulnerabilities"
            )
        
        if analysis['security_metrics']['protocol_security_score'] < 100:
            analysis['recommendations'].append(
                "Enable only TLS 1.2 and TLS 1.3 protocols"
            )
        
        return analysis
    
    def run_batch_assessment(self, targets, assessment_types=['comprehensive'], max_workers=5):
        """Run batch SSL/TLS assessments for multiple targets"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all assessment tasks
            future_to_target = {}
            
            for target in targets:
                for assessment_type in assessment_types:
                    future = executor.submit(self.run_testssl_assessment, target, assessment_type)
                    future_to_target[future] = (target, assessment_type)
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_target):
                target, assessment_type = future_to_target[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Analyze results if successful
                    if result['status'] == 'success' and 'json_file' in result:
                        analysis = self.analyze_ssl_results(result['json_file'])
                        if analysis:
                            result['analysis'] = analysis
                            
                except Exception as e:
                    self.logger.error(f"Error processing result for {target}: {e}")
                    results.append({
                        'target': target,
                        'assessment_type': assessment_type,
                        'status': 'error',
                        'error': str(e)
                    })
        
        return results
    
    def generate_executive_report(self, assessment_results, output_file):
        """Generate executive-level security assessment report"""
        successful_assessments = [r for r in assessment_results if r['status'] == 'success' and 'analysis' in r]
        
        if not successful_assessments:
            self.logger.error("No successful assessments to report")
            return None
        
        # Calculate summary statistics
        total_targets = len(successful_assessments)
        grade_distribution = {}
        compliance_stats = {'pci_dss': 0, 'hipaa': 0, 'nist': 0}
        total_vulnerabilities = 0
        critical_issues = []
        
        for result in successful_assessments:
            analysis = result['analysis']
            
            # Grade distribution
            grade = analysis['security_metrics']['overall_grade']
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
            
            # Compliance statistics
            if analysis['compliance']['pci_dss_compliant']:
                compliance_stats['pci_dss'] += 1
            if analysis['compliance']['hipaa_compliant']:
                compliance_stats['hipaa'] += 1
            if analysis['compliance']['nist_compliant']:
                compliance_stats['nist'] += 1
            
            # Vulnerability count
            total_vulnerabilities += analysis['security_metrics']['vulnerability_count']
            
            # Critical issues
            critical_issues.extend(analysis['security_metrics']['critical_issues'])
        
        # Generate HTML report
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enterprise SSL/TLS Security Assessment Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
                .card {{ background: white; padding: 25px; margin: 20px 0; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
                .metric {{ text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }}
                .metric-value {{ font-size: 2.5em; font-weight: bold; color: #495057; }}
                .metric-label {{ color: #6c757d; font-weight: 500; }}
                .grade-a {{ color: #28a745; }}
                .grade-b {{ color: #ffc107; }}
                .grade-c {{ color: #fd7e14; }}
                .grade-d {{ color: #dc3545; }}
                .grade-f {{ color: #dc3545; }}
                .compliance-good {{ background: #d4edda; color: #155724; }}
                .compliance-poor {{ background: #f8d7da; color: #721c24; }}
                .issues-list {{ max-height: 300px; overflow-y: auto; background: #fff3cd; padding: 15px; border-radius: 5px; }}
                .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }}
                .table th {{ background: #e9ecef; font-weight: 600; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔒 Enterprise SSL/TLS Security Assessment</h1>
                    <p><strong>Assessment Date:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
                    <p><strong>Total Targets Assessed:</strong> {total_targets}</p>
                    <p><strong>Assessment Scope:</strong> Comprehensive SSL/TLS Security Analysis</p>
                </div>
                
                <div class="card">
                    <h2>📊 Executive Summary</h2>
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-value">{total_targets}</div>
                            <div class="metric-label">Total Hosts</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" style="color: {'#28a745' if total_vulnerabilities == 0 else '#dc3545'}">{total_vulnerabilities}</div>
                            <div class="metric-label">Critical Vulnerabilities</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{compliance_stats['pci_dss']}/{total_targets}</div>
                            <div class="metric-label">PCI DSS Compliant</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{len(critical_issues)}</div>
                            <div class="metric-label">Security Issues</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🏆 Security Grade Distribution</h2>
                    <div class="metric-grid">
        """
        
        for grade in ['A+', 'A', 'B', 'C', 'D', 'F']:
            count = grade_distribution.get(grade, 0)
            percentage = (count / total_targets * 100) if total_targets > 0 else 0
            grade_class = f"grade-{grade.lower().replace('+', '')}"
            
            report_html += f"""
                        <div class="metric">
                            <div class="metric-value {grade_class}">{count}</div>
                            <div class="metric-label">Grade {grade} ({percentage:.1f}%)</div>
                        </div>
            """
        
        report_html += f"""
                    </div>
                </div>
                
                <div class="card">
                    <h2>📋 Compliance Status</h2>
                    <div class="metric-grid">
                        <div class="metric {'compliance-good' if compliance_stats['pci_dss'] == total_targets else 'compliance-poor'}">
                            <div class="metric-value">{(compliance_stats['pci_dss']/total_targets*100):.1f}%</div>
                            <div class="metric-label">PCI DSS Compliance</div>
                        </div>
                        <div class="metric {'compliance-good' if compliance_stats['hipaa'] == total_targets else 'compliance-poor'}">
                            <div class="metric-value">{(compliance_stats['hipaa']/total_targets*100):.1f}%</div>
                            <div class="metric-label">HIPAA Compliance</div>
                        </div>
                        <div class="metric {'compliance-good' if compliance_stats['nist'] == total_targets else 'compliance-poor'}">
                            <div class="metric-value">{(compliance_stats['nist']/total_targets*100):.1f}%</div>
                            <div class="metric-label">NIST Compliance</div>
                        </div>
                    </div>
                </div>
        """
        
        if critical_issues:
            report_html += f"""
                <div class="card">
                    <h2>⚠️ Critical Security Issues ({len(critical_issues)} Total)</h2>
                    <div class="issues-list">
            """
            
            # Show first 20 issues to avoid overwhelming the report
            for issue in critical_issues[:20]:
                report_html += f"<div>• {issue}</div>"
            
            if len(critical_issues) > 20:
                report_html += f"<div><em>... and {len(critical_issues) - 20} more issues</em></div>"
            
            report_html += """
                    </div>
                </div>
            """
        
        # Detailed results table
        report_html += """
                <div class="card">
                    <h2>📈 Detailed Assessment Results</h2>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Target</th>
                                <th>Grade</th>
                                <th>Protocol Security</th>
                                <th>Cipher Strength</th>
                                <th>Certificate Score</th>
                                <th>Vulnerabilities</th>
                                <th>PCI DSS</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        for result in successful_assessments:
            analysis = result['analysis']
            metrics = analysis['security_metrics']
            compliance = analysis['compliance']
            
            grade_class = f"grade-{metrics['overall_grade'].lower().replace('+', '')}"
            
            report_html += f"""
                            <tr>
                                <td>{analysis['target']}</td>
                                <td class="{grade_class}"><strong>{metrics['overall_grade']}</strong></td>
                                <td>{metrics['protocol_security_score']:.1f}%</td>
                                <td>{metrics['cipher_strength_score']:.1f}%</td>
                                <td>{metrics['certificate_score']:.1f}%</td>
                                <td style="color: {'#28a745' if metrics['vulnerability_count'] == 0 else '#dc3545'}">{metrics['vulnerability_count']}</td>
                                <td style="color: {'#28a745' if compliance['pci_dss_compliant'] else '#dc3545'}">{'✓' if compliance['pci_dss_compliant'] else '✗'}</td>
                            </tr>
            """
        
        report_html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(report_html)
        
        self.logger.info(f"Executive report generated: {output_file}")
        
        return {
            'report_file': output_file,
            'total_targets': total_targets,
            'grade_distribution': grade_distribution,
            'compliance_stats': compliance_stats,
            'total_vulnerabilities': total_vulnerabilities,
            'critical_issues_count': len(critical_issues)
        }
    
    def send_alert_notification(self, assessment_results, smtp_config):
        """Send alert notifications for critical security issues"""
        critical_hosts = []
        
        for result in assessment_results:
            if result['status'] == 'success' and 'analysis' in result:
                analysis = result['analysis']
                if (analysis['security_metrics']['overall_grade'] in ['D', 'F'] or
                    analysis['security_metrics']['vulnerability_count'] > 0):
                    critical_hosts.append({
                        'target': analysis['target'],
                        'grade': analysis['security_metrics']['overall_grade'],
                        'vulnerabilities': analysis['security_metrics']['vulnerability_count'],
                        'critical_issues': analysis['security_metrics']['critical_issues'][:5]  # First 5 issues
                    })
        
        if not critical_hosts:
            self.logger.info("No critical security issues found - no alerts sent")
            return
        
        # Compose alert email
        subject = f"URGENT: SSL/TLS Security Issues Detected ({len(critical_hosts)} hosts affected)"
        
        body = f"""
        ENTERPRISE SSL/TLS SECURITY ALERT
        
        Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Critical Hosts: {len(critical_hosts)}
        
        AFFECTED SYSTEMS:
        """
        
        for host in critical_hosts:
            body += f"""
        
        Host: {host['target']}
        Security Grade: {host['grade']}
        Vulnerabilities: {host['vulnerabilities']}
        Critical Issues:
        """
            for issue in host['critical_issues']:
                body += f"  • {issue}\n"
        
        body += f"""
        
        IMMEDIATE ACTIONS REQUIRED:
        1. Review detailed assessment reports
        2. Apply security patches for identified vulnerabilities
        3. Update SSL/TLS configurations to meet security standards
        4. Verify compliance with regulatory requirements
        
        Full assessment reports are available in the security dashboard.
        
        This is an automated security alert from the Enterprise SSL/TLS Monitoring System.
        """
        
        try:
            msg = MimeMultipart()
            msg['From'] = smtp_config['from_address']
            msg['To'] = ', '.join(smtp_config['to_addresses'])
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            if smtp_config.get('use_tls', True):
                server.starttls()
            if smtp_config.get('username') and smtp_config.get('password'):
                server.login(smtp_config['username'], smtp_config['password'])
            
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Alert notification sent to {len(smtp_config['to_addresses'])} recipients")
            
        except Exception as e:
            self.logger.error(f"Failed to send alert notification: {e}")

def main():
    parser = argparse.ArgumentParser(description='Enterprise SSL/TLS Security Assessment Automation')
    parser.add_argument('--config', help='YAML configuration file')
    parser.add_argument('--targets', nargs='+', help='Target URLs for assessment')
    parser.add_argument('--assessment-type', choices=['comprehensive', 'vulnerabilities', 'quick'], 
                       default='comprehensive', help='Type of assessment to perform')
    parser.add_argument('--output-dir', default='/var/log/testssl', help='Output directory for results')
    parser.add_argument('--workers', type=int, default=5, help='Number of parallel workers')
    parser.add_argument('--report-only', action='store_true', help='Generate report from existing results')
    parser.add_argument('--send-alerts', action='store_true', help='Send email alerts for critical issues')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    scanner = EnterpriseSSLScanner(args.config)
    
    if args.report_only:
        # Generate report from existing results
        json_files = list(Path(args.output_dir).glob('*_comprehensive_*.json'))
        if not json_files:
            print("No assessment results found for report generation")
            return
        
        results = []
        for json_file in json_files:
            analysis = scanner.analyze_ssl_results(str(json_file))
            if analysis:
                results.append({
                    'status': 'success',
                    'json_file': str(json_file),
                    'analysis': analysis
                })
        
        if results:
            report_file = f"{args.output_dir}/executive_ssl_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            scanner.generate_executive_report(results, report_file)
            print(f"Executive report generated: {report_file}")
    
    elif args.targets:
        # Run new assessments
        results = scanner.run_batch_assessment(
            args.targets, 
            [args.assessment_type], 
            args.workers
        )
        
        # Generate executive report
        report_file = f"{args.output_dir}/executive_ssl_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_data = scanner.generate_executive_report(results, report_file)
        
        if report_data:
            print(f"Assessment completed:")
            print(f"  Targets assessed: {report_data['total_targets']}")
            print(f"  Critical vulnerabilities: {report_data['total_vulnerabilities']}")
            print(f"  Report file: {report_data['report_file']}")
        
        # Send alerts if requested
        if args.send_alerts and scanner.config.get('smtp'):
            scanner.send_alert_notification(results, scanner.config['smtp'])
    
    else:
        print("Please specify --targets for assessment or --report-only for report generation")

if __name__ == "__main__":
    main()
