#!/usr/bin/env python3
# chimera-vx/server/anti_cheat.py
# Anti-cheat system for Chimera-VX

import hashlib
import json
import time
import secrets
import base64
import re
import math
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import IsolationForest
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class AntiCheatSystem:
    """Advanced anti-cheat system for Chimera-VX"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Detection systems
        self.detection_modules = {
            'timing_analysis': TimingAnalyzer(),
            'solution_pattern': SolutionPatternAnalyzer(),
            'hardware_fingerprint': HardwareFingerprinter(),
            'behavioral_analysis': BehavioralAnalyzer(),
            'network_analysis': NetworkAnalyzer(),
            'resource_monitor': ResourceMonitor()
        }
        
        # Player tracking
        self.player_profiles: Dict[int, PlayerProfile] = {}
        self.suspicious_activities: Dict[int, List[Dict]] = defaultdict(list)
        self.rate_limits: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Machine learning models
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Thresholds
        self.thresholds = {
            'max_suspicion_score': 100,
            'cheat_detection_threshold': 0.8,
            'rate_limit_window': 60,  # seconds
            'rate_limit_max': 100,    # requests per window
            'min_solve_time': 10,     # seconds
            'max_solution_similarity': 0.9,
            'hardware_change_threshold': 0.7
        }
        
        # Penalties
        self.penalties = {
            'warning': {'points': 10, 'action': 'log'},
            'suspension': {'points': 30, 'action': 'suspend_24h'},
            'reset': {'points': 50, 'action': 'reset_progress'},
            'ban': {'points': 100, 'action': 'permanent_ban'}
        }
        
        logger.info("AntiCheatSystem initialized")
    
    async def check_submission(self, player_id: int, puzzle_id: int, 
                              solution: str, verification_data: Dict,
                              ip_address: str) -> Tuple[bool, Dict]:
        """Check submission for cheating"""
        start_time = time.time()
        
        try:
            # Initialize player profile if needed
            if player_id not in self.player_profiles:
                self.player_profiles[player_id] = PlayerProfile(player_id)
            
            profile = self.player_profiles[player_id]
            
            # Run all detection modules
            detections = []
            total_score = 0
            
            # 1. Timing analysis
            timing_result = await self.detection_modules['timing_analysis'].analyze(
                player_id=player_id,
                puzzle_id=puzzle_id,
                solution=solution,
                verification_data=verification_data,
                profile=profile
            )
            if timing_result['suspicious']:
                detections.append(timing_result)
                total_score += timing_result['score']
            
            # 2. Solution pattern analysis
            pattern_result = await self.detection_modules['solution_pattern'].analyze(
                player_id=player_id,
                puzzle_id=puzzle_id,
                solution=solution,
                verification_data=verification_data,
                profile=profile
            )
            if pattern_result['suspicious']:
                detections.append(pattern_result)
                total_score += pattern_result['score']
            
            # 3. Hardware fingerprint check
            hardware_result = await self.detection_modules['hardware_fingerprint'].analyze(
                player_id=player_id,
                ip_address=ip_address,
                profile=profile
            )
            if hardware_result['suspicious']:
                detections.append(hardware_result)
                total_score += hardware_result['score']
            
            # 4. Behavioral analysis
            behavioral_result = await self.detection_modules['behavioral_analysis'].analyze(
                player_id=player_id,
                profile=profile,
                submission_data={
                    'puzzle_id': puzzle_id,
                    'solution': solution,
                    'verification_data': verification_data
                }
            )
            if behavioral_result['suspicious']:
                detections.append(behavioral_result)
                total_score += behavioral_result['score']
            
            # 5. Network analysis
            network_result = await self.detection_modules['network_analysis'].analyze(
                player_id=player_id,
                ip_address=ip_address,
                profile=profile
            )
            if network_result['suspicious']:
                detections.append(network_result)
                total_score += network_result['score']
            
            # 6. Resource monitoring
            resource_result = await self.detection_modules['resource_monitor'].analyze(
                player_id=player_id,
                profile=profile,
                verification_data=verification_data
            )
            if resource_result['suspicious']:
                detections.append(resource_result)
                total_score += resource_result['score']
            
            # Update player profile
            profile.update_submission({
                'puzzle_id': puzzle_id,
                'solution': solution,
                'verification_data': verification_data,
                'detections': detections,
                'total_score': total_score,
                'timestamp': time.time()
            })
            
            # Check if cheating detected
            cheat_detected = total_score > self.thresholds['cheat_detection_threshold'] * 100
            
            # Log suspicious activity
            if detections:
                self.log_suspicious_activity(
                    player_id=player_id,
                    activity_type='submission_analysis',
                    details={
                        'puzzle_id': puzzle_id,
                        'detections': detections,
                        'total_score': total_score,
                        'cheat_detected': cheat_detected,
                        'analysis_time': time.time() - start_time
                    }
                )
            
            # Prepare result
            result_data = {
                'cheat_detected': cheat_detected,
                'total_score': total_score,
                'detections': detections,
                'profile_suspicion': profile.suspicion_score,
                'analysis_time': time.time() - start_time
            }
            
            return cheat_detected, result_data
            
        except Exception as e:
            logger.error(f"Error in anti-cheat check: {e}")
            return False, {'error': str(e)}
    
    def apply_penalty(self, player_id: int, cheat_data: Dict) -> Dict:
        """Apply penalty based on cheat severity"""
        score = cheat_data.get('total_score', 0)
        
        # Determine penalty
        penalty = None
        for level, details in self.penalties.items():
            if score >= details['points']:
                penalty = level
            else:
                break
        
        if not penalty:
            penalty = 'warning'
        
        penalty_details = self.penalties[penalty]
        
        # Apply penalty
        penalty_result = {
            'penalty_type': penalty,
            'action': penalty_details['action'],
            'score': score,
            'applied_at': time.time(),
            'duration': self.get_penalty_duration(penalty)
        }
        
        # Log penalty
        self.log_penalty(player_id, penalty_result)
        
        # Update player profile
        if player_id in self.player_profiles:
            self.player_profiles[player_id].add_penalty(penalty_result)
        
        logger.warning(f"Applied {penalty} penalty to player {player_id}")
        
        return penalty_result
    
    def get_penalty_duration(self, penalty_type: str) -> int:
        """Get penalty duration in seconds"""
        durations = {
            'warning': 0,
            'suspension': 86400,  # 24 hours
            'reset': 0,
            'ban': 31536000  # 1 year
        }
        return durations.get(penalty_type, 0)
    
    def log_suspicious_activity(self, player_id: int, activity_type: str, 
                               details: Dict):
        """Log suspicious activity"""
        activity = {
            'player_id': player_id,
            'type': activity_type,
            'details': details,
            'timestamp': time.time(),
            'ip_hash': hashlib.sha256(details.get('ip', '').encode()).hexdigest()[:16]
        }
        
        self.suspicious_activities[player_id].append(activity)
        
        # Keep only recent activities
        if len(self.suspicious_activities[player_id]) > 100:
            self.suspicious_activities[player_id] = self.suspicious_activities[player_id][-50:]
        
        logger.info(f"Logged suspicious activity for player {player_id}: {activity_type}")
    
    def log_penalty(self, player_id: int, penalty: Dict):
        """Log penalty application"""
        penalty_log = {
            'player_id': player_id,
            'penalty': penalty,
            'logged_at': time.time()
        }
        
        # Store in database or file
        log_file = f"logs/penalties/{player_id}_{int(time.time())}.json"
        try:
            import json
            with open(log_file, 'w') as f:
                json.dump(penalty_log, f, indent=2)
        except:
            pass
        
        logger.warning(f"Penalty logged for player {player_id}: {penalty['penalty_type']}")
    
    def verify_hardware(self, player_id: int, current_fingerprint: str, 
                       new_data: Dict) -> Tuple[bool, Dict]:
        """Verify hardware consistency"""
        try:
            # Get or create hardware profile
            if player_id not in self.player_profiles:
                return False, {'reason': 'Player profile not found'}
            
            profile = self.player_profiles[player_id]
            
            # Analyze hardware data
            analyzer = self.detection_modules['hardware_fingerprint']
            result = analyzer.compare(
                old_fingerprint=current_fingerprint,
                new_data=new_data
            )
            
            return result['consistent'], {
                'hardware_id': result.get('hardware_id'),
                'similarity': result.get('similarity', 0),
                'suspicious': result.get('suspicious', False)
            }
            
        except Exception as e:
            logger.error(f"Error in hardware verification: {e}")
            return False, {'error': str(e)}
    
    def add_watermark(self, puzzle_data: Dict, player_id: int, 
                     ip_address: str) -> Dict:
        """Add anti-cheat watermark to puzzle data"""
        watermark = {
            'player_id': player_id,
            'timestamp': int(time.time()),
            'watermark_id': secrets.token_hex(8),
            'ip_hash': hashlib.sha256(ip_address.encode()).hexdigest()[:16],
            'checksum': self.calculate_checksum(puzzle_data)
        }
        
        # Embed watermark in puzzle data
        if isinstance(puzzle_data, dict):
            puzzle_data['_watermark'] = watermark
        elif isinstance(puzzle_data, str):
            # For string data, append as comment or in metadata
            puzzle_data = puzzle_data + f"\n# Watermark: {json.dumps(watermark)}"
        
        return puzzle_data
    
    def calculate_checksum(self, data: Any) -> str:
        """Calculate checksum for data"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        elif isinstance(data, str):
            data_str = data
        else:
            data_str = str(data)
        
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def check_rate_limit(self, player_id: int, action: str) -> bool:
        """Check if player is rate limited"""
        key = f"{player_id}_{action}"
        now = time.time()
        
        # Clean old entries
        while (self.rate_limits[key] and 
               now - self.rate_limits[key][0] > self.thresholds['rate_limit_window']):
            self.rate_limits[key].popleft()
        
        # Check limit
        if len(self.rate_limits[key]) >= self.thresholds['rate_limit_max']:
            self.log_suspicious_activity(
                player_id=player_id,
                activity_type='rate_limit_exceeded',
                details={
                    'action': action,
                    'count': len(self.rate_limits[key]),
                    'window': self.thresholds['rate_limit_window']
                }
            )
            return False
        
        # Add current action
        self.rate_limits[key].append(now)
        return True
    
    def get_player_suspicion_score(self, player_id: int) -> float:
        """Get player's suspicion score"""
        if player_id not in self.player_profiles:
            return 0.0
        
        profile = self.player_profiles[player_id]
        return min(profile.suspicion_score / self.thresholds['max_suspicion_score'], 1.0)


# ==================== DETECTION MODULES ====================


    class DetectionModule:
    """Base class for detection modules"""
    
    async def analyze(self, **kwargs) -> Dict:
        """Analyze data for cheating - to be implemented by subclasses"""
        raise NotImplementedError


class TimingAnalyzer(DetectionModule):
    """Analyze timing patterns for cheating"""
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        verification_data = kwargs.get('verification_data', {})
        profile = kwargs.get('profile')
        
        solve_time = verification_data.get('solve_time', 0)
        
        # Check minimum solve time
        if solve_time < 10:  # Less than 10 seconds is suspicious
            return {
                'suspicious': True,
                'score': 40,
                'reason': 'solve_time_too_fast',
                'details': {
                    'solve_time': solve_time,
                    'threshold': 10
                }
            }
        
        # Check consistency with previous solves
        if profile and hasattr(profile, 'average_solve_time'):
            avg_time = profile.average_solve_time
            if avg_time > 0:
                ratio = solve_time / avg_time
                if ratio < 0.1:  # 10x faster than average
                    return {
                        'suspicious': True,
                        'score': 30,
                        'reason': 'solve_time_inconsistent',
                        'details': {
                            'solve_time': solve_time,
                            'average_time': avg_time,
                            'ratio': ratio
                        }
                    }
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'timing_normal'
        }


class SolutionPatternAnalyzer(DetectionModule):
    """Analyze solution patterns for cheating"""
    
    def __init__(self):
        self.common_patterns = self.load_common_patterns()
        self.solution_cache = {}  # Cache of recent solutions
    
    def load_common_patterns(self) -> List[str]:
        """Load common cheat solution patterns"""
        return [
            r'^FLAG\{.*\}$',
            r'^CTF\{.*\}$',
            r'^HACK\{.*\}$',
            r'^SECRET\{.*\}$',
            r'^ADMIN\{.*\}$',
            r'^ROOT\{.*\}$'
        ]
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        solution = kwargs.get('solution', '')
        puzzle_id = kwargs.get('puzzle_id')
        
        # Check for common cheat patterns
        for pattern in self.common_patterns:
            if re.match(pattern, solution, re.IGNORECASE):
                return {
                    'suspicious': True,
                    'score': 50,
                    'reason': 'common_cheat_pattern',
                    'details': {
                        'pattern': pattern,
                        'solution_sample': solution[:50]
                    }
                }
        
        # Check solution length
        if len(solution) < 4 or len(solution) > 1024:
            return {
                'suspicious': True,
                'score': 20,
                'reason': 'solution_length_anomaly',
                'details': {
                    'length': len(solution),
                    'min_length': 4,
                    'max_length': 1024
                }
            }
        
        # Check for binary data (might be encoded)
        try:
            solution.encode('ascii')
        except UnicodeEncodeError:
            # Contains non-ASCII characters
            return {
                'suspicious': True,
                'score': 15,
                'reason': 'non_ascii_solution',
                'details': {
                    'sample': solution[:100]
                }
            }
        
        # Check for known exploit strings
        exploit_patterns = [
            'union select',
            'drop table',
            'exec(',
            'system(',
            'eval(',
            '<script>'
        ]
        
        solution_lower = solution.lower()
        for exploit in exploit_patterns:
            if exploit in solution_lower:
                return {
                    'suspicious': True,
                    'score': 60,
                    'reason': 'possible_exploit_code',
                    'details': {
                        'exploit_pattern': exploit,
                        'solution_sample': solution[:100]
                    }
                }
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'solution_pattern_normal'
        }


class HardwareFingerprinter(DetectionModule):
    """Analyze hardware fingerprints for cheating"""
    
    def __init__(self):
        self.fingerprint_cache = {}
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        ip_address = kwargs.get('ip_address')
        profile = kwargs.get('profile')
        
        # Generate current fingerprint
        current_fp = self.generate_fingerprint(ip_address, kwargs)
        
        # Check against stored fingerprint
        if profile and hasattr(profile, 'hardware_fingerprint'):
            stored_fp = profile.hardware_fingerprint
            similarity = self.compare_fingerprints(stored_fp, current_fp)
            
            if similarity < 0.7:  # 70% similarity threshold
                return {
                    'suspicious': True,
                    'score': 40,
                    'reason': 'hardware_fingerprint_mismatch',
                    'details': {
                        'similarity': similarity,
                        'threshold': 0.7,
                        'stored_fp': stored_fp[:20] if stored_fp else None,
                        'current_fp': current_fp[:20]
                    }
                }
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'hardware_fingerprint_normal'
        }
    
    def generate_fingerprint(self, ip_address: str, data: Dict) -> str:
        """Generate hardware fingerprint"""
        components = [
            ip_address,
            str(data.get('user_agent', '')),
            str(time.time() // 3600)  # Hour bucket
        ]
        
        fingerprint_data = '|'.join(components)
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def compare_fingerprints(self, fp1: str, fp2: str) -> float:
        """Compare two fingerprints"""
        if not fp1 or not fp2:
            return 0.0
        
        # Simple Hamming distance for hex strings
        if len(fp1) != len(fp2):
            return 0.0
        
        matches = sum(1 for a, b in zip(fp1, fp2) if a == b)
        return matches / len(fp1)
    
    def compare(self, old_fingerprint: str, new_data: Dict) -> Dict:
        """Compare fingerprints for verification"""
        new_fp = self.generate_fingerprint('', new_data)
        similarity = self.compare_fingerprints(old_fingerprint, new_fp)
        
        return {
            'consistent': similarity >= 0.7,
            'similarity': similarity,
            'hardware_id': new_fp[:16],
            'suspicious': similarity < 0.3
        }


class BehavioralAnalyzer(DetectionModule):
    """Analyze player behavior for cheating"""
    
    def __init__(self):
        self.behavior_profiles = {}
        self.anomaly_detector = IsolationForest(
            contamination=0.05,
            random_state=42
        )
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        profile = kwargs.get('profile')
        submission_data = kwargs.get('submission_data', {})
        
        if not profile or not hasattr(profile, 'behavior_history'):
            return {
                'suspicious': False,
                'score': 0,
                'reason': 'insufficient_behavior_data'
            }
        
        # Extract features from current submission
        features = self.extract_features(submission_data, profile)
        
        # Check for anomalies
        if len(profile.behavior_history) >= 10:  # Need enough data
            is_anomaly = self.detect_anomaly(features, profile.behavior_history)
            
            if is_anomaly:
                return {
                    'suspicious': True,
                    'score': 35,
                    'reason': 'behavioral_anomaly',
                    'details': {
                        'features': features,
                        'history_size': len(profile.behavior_history)
                    }
                }
        
        # Update behavior history
        profile.behavior_history.append(features)
        if len(profile.behavior_history) > 100:
            profile.behavior_history = profile.behavior_history[-50:]
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'behavior_normal'
        }
    
    def extract_features(self, submission_data: Dict, profile) -> List[float]:
        """Extract behavioral features"""
        features = []
        
        # Time-based features
        solve_time = submission_data.get('verification_data', {}).get('solve_time', 0)
        features.append(min(solve_time, 3600) / 3600)  # Normalized to 1 hour
        
        # Solution length feature
        solution = submission_data.get('solution', '')
        features.append(min(len(solution), 1024) / 1024)  # Normalized
        
        # Time of day feature
        hour = datetime.now().hour
        features.append(hour / 24)
        
        # Day of week feature
        day = datetime.now().weekday()
        features.append(day / 7)
        
        return features
    
    def detect_anomaly(self, features: List[float], history: List[List[float]]) -> bool:
        """Detect behavioral anomalies"""
        if len(history) < 10:
            return False
        
        # Train anomaly detector
        try:
            self.anomaly_detector.fit(history)
            prediction = self.anomaly_detector.predict([features])
            return prediction[0] == -1  # -1 indicates anomaly
        except:
            return False


class NetworkAnalyzer(DetectionModule):
    """Analyze network patterns for cheating"""
    
    def __init__(self):
        self.ip_blacklist = self.load_ip_blacklist()
        self.geo_patterns = {}
    
    def load_ip_blacklist(self) -> set:
        """Load IP blacklist"""
        # In production, this would load from file/database
        return set()
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        ip_address = kwargs.get('ip_address')
        
        # Check blacklist
        if ip_address in self.ip_blacklist:
            return {
                'suspicious': True,
                'score': 80,
                'reason': 'blacklisted_ip',
                'details': {
                    'ip_address': ip_address
                }
            }
        
        # Check for VPN/Tor exit nodes
        if self.is_suspicious_ip(ip_address):
            return {
                'suspicious': True,
                'score': 25,
                'reason': 'suspicious_ip_type',
                'details': {
                    'ip_address': ip_address,
                    'risk_factors': ['vpn_proxy']
                }
            }
        
        # Check geographic anomalies
        geo_result = await self.check_geographic_anomaly(player_id, ip_address)
        if geo_result['suspicious']:
            return geo_result
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'network_normal'
        }
    
    def is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP is suspicious"""
        # Simple check for localhost or private IPs
        suspicious_patterns = [
            '127.0.0.1',
            'localhost',
            '192.168.',
            '10.',
            '172.16.',
            '172.31.'
        ]
        
        for pattern in suspicious_patterns:
            if ip_address.startswith(pattern):
                return True
        
        # Check for VPN/Proxy patterns (simplified)
        # In production, use IP intelligence service
        return False
    
    async def check_geographic_anomaly(self, player_id: int, ip_address: str) -> Dict:
        """Check for geographic anomalies"""
        # This would use GeoIP service in production
        # For now, return normal result
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'geographic_check_not_implemented'
        }


class ResourceMonitor(DetectionModule):
    """Monitor resource usage for cheating"""
    
    async def analyze(self, **kwargs) -> Dict:
        player_id = kwargs.get('player_id')
        verification_data = kwargs.get('verification_data', {})
        
        # Check verification time
        verification_time = verification_data.get('verification_time', 0)
        
        if verification_time > 30:  # More than 30 seconds is suspicious
            return {
                'suspicious': True,
                'score': 20,
                'reason': 'excessive_verification_time',
                'details': {
                    'verification_time': verification_time,
                    'threshold': 30
                }
            }
        
        # Check memory usage (simulated)
        # In production, this would monitor actual resource usage
        memory_usage = verification_data.get('memory_usage', 0)
        if memory_usage > 1024 * 1024 * 1024:  # More than 1GB
            return {
                'suspicious': True,
                'score': 25,
                'reason': 'excessive_memory_usage',
                'details': {
                    'memory_usage_mb': memory_usage / (1024 * 1024),
                    'threshold_mb': 1024
                }
            }
        
        return {
            'suspicious': False,
            'score': 0,
            'reason': 'resource_usage_normal'
        }

# ==================== PLAYER PROFILE ====================

class PlayerProfile:
    """Track player behavior and patterns"""
    
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.hardware_fingerprint = None
        self.behavior_history = []
        self.submission_history = []
        self.solve_times = []
        self.suspicion_score = 0
        self.penalties = []
        self.created_at = time.time()
        self.last_updated = time.time()
        
        # Statistics
        self.total_submissions = 0
        self.correct_submissions = 0
        self.total_solve_time = 0
    
    @property
    def average_solve_time(self) -> float:
        """Calculate average solve time"""
        if not self.solve_times:
            return 0.0
        return sum(self.solve_times) / len(self.solve_times)
    
    def update_submission(self, submission_data: Dict):
        """Update profile with new submission"""
        self.submission_history.append(submission_data)
        self.total_submissions += 1
        
        # Update solve times
        solve_time = submission_data.get('verification_data', {}).get('solve_time', 0)
        if solve_time > 0:
            self.solve_times.append(solve_time)
            self.total_solve_time += solve_time
        
        # Update suspicion score
        total_score = submission_data.get('total_score', 0)
        self.suspicion_score += total_score
        
        # Keep history manageable
        if len(self.submission_history) > 100:
            self.submission_history = self.submission_history[-50:]
        if len(self.solve_times) > 100:
            self.solve_times = self.solve_times[-50:]
        
        self.last_updated = time.time()
    
    def add_penalty(self, penalty: Dict):
        """Add penalty to profile"""
        self.penalties.append(penalty)
        self.suspicion_score += 10  # Additional score for penalties
        
        if len(self.penalties) > 20:
            self.penalties = self.penalties[-10:]
    
    def get_statistics(self) -> Dict:
        """Get player statistics"""
        return {
            'player_id': self.player_id,
            'total_submissions': self.total_submissions,
            'correct_submissions': self.correct_submissions,
            'average_solve_time': self.average_solve_time,
            'total_solve_time': self.total_solve_time,
            'suspicion_score': self.suspicion_score,
            'penalty_count': len(self.penalties),
            'profile_age_hours': (time.time() - self.created_at) / 3600
        }


# Test the anti-cheat system
if __name__ == "__main__":
    import asyncio
    
    config = {}
    anti_cheat = AntiCheatSystem(config)
    
    async def test():
        # Test cheating detection
        cheat_detected, result = await anti_cheat.check_submission(
            player_id=1,
            puzzle_id=1,
            solution="FLAG{THIS_IS_CHEATING}",
            verification_data={
                'solve_time': 5,  # Too fast!
                'verification_time': 1
            },
            ip_address="127.0.0.1"
        )
        
        print(f"Cheat detected: {cheat_detected}")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        if cheat_detected:
            penalty = anti_cheat.apply_penalty(1, result)
            print(f"Penalty applied: {penalty}")
    
    asyncio.run(test())
```
