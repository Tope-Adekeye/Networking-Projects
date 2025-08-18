#!/usr/bin/env python3
"""
Professional iperf3 Network Performance Testing Automation
Enterprise-grade bandwidth testing with comprehensive reporting
"""

import json
import subprocess
import time
import argparse
import logging
import statistics
from datetime import datetime, timedelta
from pathlib import Path
import concurrent.futures
import threading

class IPerf3TestSuite:
    def __init__(self, config_file=None):
        self.setup_logging()
        self.results = {}
        self.test_configs = []
        if config_file:
            self.load_config(config_file)
    
    def setup_logging(self):
        """Configure comprehensive logging for enterprise environments"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('/var/log/iperf3/automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_file):
        """Load test configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.test_configs = config.get('test_configurations', [])
                self.logger.info(f"Loaded {len(self.test_configs)} test configurations")
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
    
    def run_iperf3_test(self, server_ip, test_params):
        """Execute individual iperf3 test with specified parameters"""
        cmd = ['iperf3', '-c', server_ip, '--json']
        
        # Add test parameters
        for param, value in test_params.items():
            if param == 'time':
                cmd.extend(['-t', str(value)])
            elif param == 'parallel':
                cmd.extend(['-P', str(value)])
            elif param == 'window':
                cmd.extend(['-w', str(value)])
            elif param == 'bandwidth' and test_params.get('udp', False):
                cmd.extend(['-b', str(value)])
            elif param == 'udp' and value:
                cmd.append('-u')
            elif param == 'reverse' and value:
                cmd.append('-R')
            elif param == 'bidir' and value:
                cmd.append('--bidir')
            elif param == 'interval':
                cmd.extend(['-i', str(value)])
        
        try:
            self.logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                self.logger.error(f"iperf3 test failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            self.logger.error("iperf3 test timed out")
            return None
        except Exception as e:
            self.logger.error(f"Error running iperf3 test: {e}")
            return None
    
    def tcp_throughput_test(self, server_ip, duration=300, parallel=1, window='1M'):
        """Standard TCP throughput test"""
        params = {
            'time': duration,
            'parallel': parallel,
            'window': window,
            'interval': 10
        }
        return self.run_iperf3_test(server_ip, params)
    
    def udp_performance_test(self, server_ip, bandwidth='100M', duration=300):
        """UDP performance test with jitter and loss measurement"""
        params = {
            'udp': True,
            'bandwidth': bandwidth,
            'time': duration,
            'interval': 10
        }
        return self.run_iperf3_test(server_ip, params)
    
    def bidirectional_test(self, server_ip, duration=300, parallel=4):
        """Bidirectional throughput test"""
        params = {
            'bidir': True,
            'time': duration,
            'parallel': parallel,
            'interval': 10
        }
        return self.run_iperf3_test(server_ip, params)
    
    def buffer_optimization_test(self, server_ip, duration=180):
        """Test different TCP buffer sizes for optimization"""
        buffer_sizes = ['64K', '128K', '256K', '512K', '1M', '2M', '4M', '8M']
        results = {}
        
        for buffer_size in buffer_sizes:
            self.logger.info(f"Testing TCP buffer size: {buffer_size}")
            params = {
                'time': duration,
                'window': buffer_size,
                'parallel': 1,
                'interval': 30
            }
            result = self.run_iperf3_test(server_ip, params)
            if result:
                results[buffer_size] = result
            time.sleep(10)  # Brief pause between tests
        
        return results
    
    def parallel_streams_optimization(self, server_ip, duration=180):
        """Test different numbers of parallel streams"""
        stream_counts = [1, 2, 4, 8, 16, 32]
        results = {}
        
        for streams in stream_counts:
            self.logger.info(f"Testing with {streams} parallel streams")
            params = {
                'time': duration,
                'parallel': streams,
                'interval': 30
            }
            result = self.run_iperf3_test(server_ip, params)
            if result:
                results[f"{streams}_streams"] = result
            time.sleep(10)
        
        return results
    
    def enterprise_sla_validation(self, server_ip, sla_requirements):
        """Comprehensive SLA validation testing"""
        sla_results = {}
        
        # Long-duration TCP test for SLA compliance
        self.logger.info("Starting SLA validation - TCP throughput test")
        tcp_result = self.tcp_throughput_test(
            server_ip, 
            duration=3600,  # 1 hour
            parallel=4,
            window='2M'
        )
        if tcp_result:
            sla_results['tcp_sla_test'] = tcp_result
        
        # UDP test for latency and loss validation
        self.logger.info("Starting SLA validation - UDP performance test")
        udp_result = self.udp_performance_test(
            server_ip,
            bandwidth=sla_requirements.get('guaranteed_bandwidth', '100M'),
            duration=1800  # 30 minutes
        )
        if udp_result:
            sla_results['udp_sla_test'] = udp_result
        
        # Peak hours simulation
        self.logger.info("Starting SLA validation - Peak hours simulation")
        peak_result = self.run_iperf3_test(server_ip, {
            'time': 1800,
            'parallel': 10,
            'window': '1M',
            'interval': 60
        })
        if peak_result:
            sla_results['peak_hours_test'] = peak_result
        
        return sla_results
    
    def analyze_results(self, test_results, test_name):
        """Analyze test results and generate metrics"""
        if not test_results:
            return None
        
        analysis = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'performance_metrics': {},
            'recommendations': []
        }
        
        try:
            if 'end' in test_results and 'sum_received' in test_results['end']:
                # TCP analysis
                end_data = test_results['end']['sum_received']
                analysis['summary'] = {
                    'protocol': 'TCP',
                    'duration': end_data['seconds'],
                    'bytes_transferred': end_data['bytes'],
                    'throughput_bps': end_data['bits_per_second'],
                    'throughput_mbps': round(end_data['bits_per_second'] / 1000000, 2)
                }
                
                # Check for retransmissions
                if 'sum_sent' in test_results['end']:
                    retransmits = test_results['end']['sum_sent'].get('retransmits', 0)
                    analysis['performance_metrics']['retransmissions'] = retransmits
                    if retransmits > 0:
                        total_packets = test_results['end']['sum_sent'].get('packets', 1)
                        retrans_rate = (retransmits / total_packets) * 100
                        analysis['performance_metrics']['retransmission_rate'] = round(retrans_rate, 2)
                        
                        if retrans_rate > 1.0:
                            analysis['recommendations'].append(
                                "High retransmission rate detected. Consider TCP buffer tuning and network path analysis."
                            )
            
            elif 'end' in test_results and 'sum' in test_results['end']:
                # UDP analysis
                end_data = test_results['end']['sum']
                analysis['summary'] = {
                    'protocol': 'UDP',
                    'duration': end_data['seconds'],
                    'bytes_transferred': end_data['bytes'],
                    'throughput_bps': end_data['bits_per_second'],
                    'throughput_mbps': round(end_data['bits_per_second'] / 1000000, 2),
                    'jitter_ms': end_data.get('jitter_ms', 0),
                    'lost_packets': end_data.get('lost_packets', 0),
                    'lost_percent': end_data.get('lost_percent', 0)
                }
                
                if end_data.get('lost_percent', 0) > 0.1:
                    analysis['recommendations'].append(
                        "UDP packet loss detected. Investigate network congestion and QoS policies."
                    )
        
        except Exception as e:
            self.logger.error(f"Error analyzing results: {e}")
            return None
        
        return analysis
    
    def generate_comprehensive_report(self, all_results, output_file):
        """Generate comprehensive enterprise performance report"""
        report = {
            'report_metadata': {
                'generation_time': datetime.now().isoformat(),
                'testing_tool': 'iperf3 Enterprise Test Suite',
                'version': '1.0'
            },
            'executive_summary': {},
            'detailed_results': all_results,
            'performance_analysis': [],
            'recommendations': [],
            'sla_compliance': {}
        }
        
        # Generate executive summary
        tcp_tests = [r for r in all_results if r and r.get('summary', {}).get('protocol') == 'TCP']
        udp_tests = [r for r in all_results if r and r.get('summary', {}).get('protocol') == 'UDP']
        
        if tcp_tests:
            tcp_throughputs = [t['summary']['throughput_mbps'] for t in tcp_tests]
            report['executive_summary']['tcp'] = {
                'total_tests': len(tcp_tests),
                'average_throughput_mbps': round(statistics.mean(tcp_throughputs), 2),
                'peak_throughput_mbps': round(max(tcp_throughputs), 2),
                'min_throughput_mbps': round(min(tcp_throughputs), 2)
            }
        
        if udp_tests:
            udp_throughputs = [t['summary']['throughput_mbps'] for t in udp_tests]
            udp_loss_rates = [t['summary']['lost_percent'] for t in udp_tests if 'lost_percent' in t['summary']]
            report['executive_summary']['udp'] = {
                'total_tests': len(udp_tests),
                'average_throughput_mbps': round(statistics.mean(udp_throughputs), 2),
                'average_loss_percent': round(statistics.mean(udp_loss_rates), 3) if udp_loss_rates else 0
            }
        
        # Collect all recommendations
        all_recommendations = []
        for result in all_results:
            if result and 'recommendations' in result:
                all_recommendations.extend(result['recommendations'])
        report['recommendations'] = list(set(all_recommendations))  # Remove duplicates
        
        # Save report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Comprehensive report saved to {output_file}")
        return report
    
    def run_enterprise_test_suite(self, servers, output_dir="/var/log/iperf3/enterprise_testing"):
        """Run complete enterprise test suite"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        all_results = []
        
        for server_info in servers:
            server_ip = server_info['ip']
            server_name = server_info.get('name', server_ip)
            
            self.logger.info(f"Starting comprehensive testing for {server_name} ({server_ip})")
            
            # Basic TCP throughput test
            tcp_result = self.tcp_throughput_test(server_ip, duration=600)
            tcp_analysis = self.analyze_results(tcp_result, f"{server_name}_tcp_baseline")
            if tcp_analysis:
                all_results.append(tcp_analysis)
            
            # UDP performance test
            udp_result = self.udp_performance_test(server_ip, duration=300)
            udp_analysis = self.analyze_results(udp_result, f"{server_name}_udp_baseline")
            if udp_analysis:
                all_results.append(udp_analysis)
            
            # Bidirectional test
            bidir_result = self.bidirectional_test(server_ip, duration=300)
            bidir_analysis = self.analyze_results(bidir_result, f"{server_name}_bidirectional")
            if bidir_analysis:
                all_results.append(bidir_analysis)
            
            # Buffer optimization (if requested)
            if server_info.get('optimize_buffers', False):
                self.logger.info(f"Running buffer optimization for {server_name}")
                buffer_results = self.buffer_optimization_test(server_ip)
                for buffer_size, result in buffer_results.items():
                    analysis = self.analyze_results(result, f"{server_name}_buffer_{buffer_size}")
                    if analysis:
                        all_results.append(analysis)
            
            # SLA validation (if requirements specified)
            if 'sla_requirements' in server_info:
                self.logger.info(f"Running SLA validation for {server_name}")
                sla_results = self.enterprise_sla_validation(server_ip, server_info['sla_requirements'])
                for test_name, result in sla_results.items():
                    analysis = self.analyze_results(result, f"{server_name}_{test_name}")
                    if analysis:
                        all_results.append(analysis)
        
        # Generate comprehensive report
        report_file = f"{output_dir}/enterprise_performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        final_report = self.generate_comprehensive_report(all_results, report_file)
        
        return final_report

def main():
    parser = argparse.ArgumentParser(description='Enterprise iperf3 Testing Automation')
    parser.add_argument('--config', help='JSON configuration file')
    parser.add_argument('--server', help='Single server IP for testing')
    parser.add_argument('--output', default='/var/log/iperf3/enterprise_testing', help='Output directory')
    parser.add_argument('--sla-test', action='store_true', help='Run SLA validation tests')
    parser.add_argument('--optimize', action='store_true', help='Run optimization tests')
    
    args = parser.parse_args()
    
    test_suite = IPerf3TestSuite(args.config)
    
    if args.server:
        # Single server testing
        servers = [{
            'ip': args.server,
            'name': args.server,
            'optimize_buffers': args.optimize,
            'sla_requirements': {'guaranteed_bandwidth': '100M'} if args.sla_test else None
        }]
        
        report = test_suite.run_enterprise_test_suite(servers, args.output)
        print(f"Testing completed. Report available in {args.output}")
    else:
        print("Please specify --server or --config file for testing")

if __name__ == "__main__":
    main()
