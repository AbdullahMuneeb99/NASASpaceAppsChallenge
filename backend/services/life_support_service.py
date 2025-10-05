# backend/space_vitals/services/life_support_service.py

import random
from datetime import datetime

class LifeSupportService:
    def __init__(self):
        # Initial system state
        self.oxygen_level = 98.0       # in percentage
        self.air_pressure = 101.3      # in kPa (normal pressure)
        self.water_reserve = 100.0      # in percentage
        self.last_check = datetime.now()
        self.alerts = []
        self.leak_detected = False

    def get_status(self):
        """
        Returns the current life support system data.
        """
        self._check_conditions()
        return {
            "oxygen_level": round(self.oxygen_level, 1),
            "air_pressure": round(self.air_pressure, 2),
            "water_reserve": round(self.water_reserve, 1),
            "leak_detected": self.leak_detected,
            "alerts": self.alerts,
            "last_checked": self.last_check.strftime("%Y-%m-%d %H:%M:%S")
        }

    def simulate_environment(self):
        """
        Randomly changes system levels to mimic real environmental fluctuations.
        """
        self.oxygen_level = max(80.0, min(100.0, self.oxygen_level + random.uniform(-0.5, 0.5)))
        self.air_pressure = max(95.0, min(105.0, self.air_pressure + random.uniform(-0.3, 0.3)))
        self.water_reserve = max(0.0, min(100.0, self.water_reserve - random.uniform(0.1, 0.5)))

        # 3% chance of leak detection event
        self.leak_detected = random.random() < 0.03

        self.last_check = datetime.now()
        self._check_conditions()
        return self.get_status()

    def _check_conditions(self):
        """
        Evaluates system conditions and adds alerts if necessary.
        """
        self.alerts.clear()

        if self.oxygen_level < 90:
            self._add_alert("🫁 Oxygen levels below safe threshold!")
        if self.air_pressure < 97 or self.air_pressure > 104:
            self._add_alert("💨 Air pressure anomaly detected.")
        if self.water_reserve < 25:
            self._add_alert("🚰 Portable water reserves low.")
        if self.leak_detected:
            self._add_alert("⚠️ Possible cabin leak detected!")

    def _add_alert(self, message):
        """
        Adds unique alerts to avoid duplicates.
        """
        if message not in self.alerts:
            self.alerts.append(message)

    def refill_water(self):
        """
        Refills the portable water reserves.
        """
        self.water_reserve = 100.0
        self._check_conditions()
        return {
            "message": "💧 Water reserves fully refilled.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def repair_leak(self):
        """
        Repairs any detected leak and clears alert.
        """
        if self.leak_detected:
            self.leak_detected = False
            self._check_conditions()
            return {"message": "🔧 Leak successfully repaired."}
        return {"message": "No leaks detected. System stable ✅"}

