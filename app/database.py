from typing import Dict, List, Optional
from app.models import User, CallEvent, WalletCheck, GPSAlert, FamilyAlert, Report
from datetime import datetime
import uuid


class InMemoryDatabase:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.call_events: Dict[str, CallEvent] = {}
        self.wallet_checks: Dict[str, WalletCheck] = {}
        self.gps_alerts: Dict[str, GPSAlert] = {}
        self.family_alerts: Dict[str, FamilyAlert] = {}
        self.reports: Dict[str, Report] = {}
        
        self.scam_wallet_database = {
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": {"scam_type": "ponzi", "reported_count": 45},
            "3J98t1WpEZ73CNmYviecrnyiWrnqRhWNLy": {"scam_type": "phishing", "reported_count": 120},
            "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh": {"scam_type": "romance_scam", "reported_count": 89},
            "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF": {"scam_type": "tech_support", "reported_count": 234},
            "3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5": {"scam_type": "investment_fraud", "reported_count": 156},
        }
        
        self.high_risk_locations = [
            {"lat": 37.7749, "lon": -122.4194, "type": "bitcoin_atm", "name": "SF Bitcoin ATM"},
            {"lat": 40.7128, "lon": -74.0060, "type": "bitcoin_atm", "name": "NYC Bitcoin ATM"},
            {"lat": 34.0522, "lon": -118.2437, "type": "bitcoin_atm", "name": "LA Bitcoin ATM"},
            {"lat": 41.8781, "lon": -87.6298, "type": "moneygram", "name": "Chicago MoneyGram"},
            {"lat": 29.7604, "lon": -95.3698, "type": "western_union", "name": "Houston Western Union"},
        ]
    
    def create_user(self, user: User) -> User:
        self.users[user.user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def create_call_event(self, call_event: CallEvent) -> CallEvent:
        self.call_events[call_event.call_id] = call_event
        return call_event
    
    def get_call_event(self, call_id: str) -> Optional[CallEvent]:
        return self.call_events.get(call_id)
    
    def update_call_event(self, call_id: str, updates: dict) -> Optional[CallEvent]:
        if call_id in self.call_events:
            call_event = self.call_events[call_id]
            for key, value in updates.items():
                if hasattr(call_event, key):
                    setattr(call_event, key, value)
            return call_event
        return None
    
    def create_wallet_check(self, wallet_check: WalletCheck) -> WalletCheck:
        self.wallet_checks[wallet_check.check_id] = wallet_check
        return wallet_check
    
    def get_wallet_check(self, check_id: str) -> Optional[WalletCheck]:
        return self.wallet_checks.get(check_id)
    
    def create_gps_alert(self, gps_alert: GPSAlert) -> GPSAlert:
        self.gps_alerts[gps_alert.gps_id] = gps_alert
        return gps_alert
    
    def create_family_alert(self, family_alert: FamilyAlert) -> FamilyAlert:
        self.family_alerts[family_alert.alert_id] = family_alert
        return family_alert
    
    def create_report(self, report: Report) -> Report:
        self.reports[report.report_id] = report
        return report
    
    def get_report(self, report_id: str) -> Optional[Report]:
        return self.reports.get(report_id)
    
    def get_user_call_events(self, user_id: str) -> List[CallEvent]:
        return [ce for ce in self.call_events.values() if ce.user_id == user_id]
    
    def get_user_wallet_checks(self, user_id: str) -> List[WalletCheck]:
        return [wc for wc in self.wallet_checks.values() if wc.user_id == user_id]
    
    def is_scam_wallet(self, wallet_address: str) -> Optional[dict]:
        return self.scam_wallet_database.get(wallet_address)
    
    def get_nearby_risk_locations(self, lat: float, lon: float, radius_km: float = 0.5) -> List[dict]:
        import math
        
        def haversine_distance(lat1, lon1, lat2, lon2):
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            return R * c
        
        nearby = []
        for loc in self.high_risk_locations:
            distance = haversine_distance(lat, lon, loc["lat"], loc["lon"])
            if distance <= radius_km:
                nearby.append({**loc, "distance_km": distance})
        
        return nearby


db = InMemoryDatabase()
