# backend/space_vitals/services/power_service.py

import random
from datetime import datetime

class PowerService:
    def __init__(self):
        self.battery_level = 100.0  # percentage
        self.backup_battery_ready = True
        self.last_maintenance = datetime.now()
        self.maintenance_alerts = []
        self._check_maintenance_schedule()

    def get_power_status(self):
        """
        Returns the current system power levels and redundancy info.
        """
        return {
            "battery_level": round(self.battery_level, 2),
            "backup_battery_ready": self.backup_battery_ready,
            "last_maintenance": self.last_maintenance.strftime("%Y-%m-%d %H:%M:%S"),
            "maintenance_alerts": self.maintenance_alerts
        }

    def simulate_power_usage(self):
        """
        Simulates battery drain and occasional maintenance warnings.
        """
        drain = random.uniform(0.5, 3.0)
        self.battery_level = max(0, self.battery_level - drain)

        # Simulate rare random backup system failure
        if random.random() < 0.05:
            self.backup_battery_ready = False
            self._add_alert("⚠️ Backup battery offline. Immediate maintenance required.")
        else:
            self.backup_battery_ready = True

        # Generate maintenance alerts when thresholds are reached
        self._check_maintenance_schedule()

        return self.get_power_status()

    def _check_maintenance_schedule(self):
        """
        Adds alerts if system conditions meet maintenance thresholds.
        """
        self.maintenance_alerts.clear()
        if self.battery_level < 25:
            self._add_alert("🔋 Low power detected — consider recharging soon.")
        if (datetime.now() - self.last_maintenance).days >= 7:
            self._add_alert("🧰 Scheduled maintenance overdue (7+ days).")
        if not self.backup_battery_ready:
            self._add_alert("⚠️ Backup system not operational.")

    def _add_alert(self, message):
        """
        Appends a maintenance alert message.
        """
        if message not in self.maintenance_alerts:
            self.maintenance_alerts.append(message)

    def perform_maintenance(self):
        """
        Performs maintenance to restore system health.
        """
        self.battery_level = 100.0
        self.backup_battery_ready = True
        self.last_maintenance = datetime.now()
        self.maintenance_alerts.clear()
        return {
            "message": "✅ Maintenance completed successfully.",
            "timestamp": self.last_maintenance.strftime("%Y-%m-%d %H:%M:%S")
        }
