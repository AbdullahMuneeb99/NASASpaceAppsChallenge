# backend/space_vitals/services/medical_service.py

from datetime import datetime
import random


class MedicalService:
    """
    Simulates astronaut health monitoring and provides basic medical protocols.
    Tracks vital signs like heart rate, blood pressure, and temperature.
    """

    def __init__(self):
        self.vitals = {
            "heart_rate": 72,                # beats per minute
            "blood_pressure": "120/80",      # mmHg
            "body_temperature": 36.8,        # Celsius
            "last_checked": datetime.utcnow().isoformat()
        }

    def get_vitals(self):
        """
        Returns the astronaut's latest vital readings.
        """
        return self.vitals

    def simulate_vital_changes(self):
        """
        Randomly fluctuates vital signs to simulate changing health readings.
        Useful for testing and dashboard animations.
        """
        heart_rate = max(50, min(110, self.vitals["heart_rate"] + random.randint(-3, 3)))
        systolic = random.randint(110, 130)
        diastolic = random.randint(70, 85)
        temperature = round(max(35.5, min(38.5, self.vitals["body_temperature"] + random.uniform(-0.2, 0.2))), 1)

        self.vitals.update({
            "heart_rate": heart_rate,
            "blood_pressure": f"{systolic}/{diastolic}",
            "body_temperature": temperature,
            "last_checked": datetime.utcnow().isoformat()
        })

        return self.vitals

    def get_health_status(self):
        """
        Interprets vitals and provides a simple health assessment message.
        """
        hr = self.vitals["heart_rate"]
        temp = self.vitals["body_temperature"]
        bp = self.vitals["blood_pressure"]

        status_messages = []

        # Heart Rate
        if hr < 60:
            status_messages.append("💤 Heart rate low — maybe calm breathing, or you’re just that relaxed?")
        elif hr > 100:
            status_messages.append("❤️ Elevated heart rate — are we nervous, excited, or running from space spiders?")
        else:
            status_messages.append("✅ Heart rate normal.")

        # Body Temperature
        if temp < 36.0:
            status_messages.append("🥶 Body temperature slightly low — warm yourself with some cosmic cocoa.")
        elif temp > 37.5:
            status_messages.append("🔥 Temperature slightly high — stay hydrated and avoid overexertion.")
        else:
            status_messages.append("🌡️ Body temperature stable.")

        # Blood Pressure (simple check)
        sys, dia = map(int, bp.split("/"))
        if sys > 130 or dia > 85:
            status_messages.append("⚠️ Blood pressure slightly elevated — maybe lay off the freeze-dried chips.")
        elif sys < 100 or dia < 65:
            status_messages.append("🩸 Blood pressure a bit low — a little rest might help.")
        else:
            status_messages.append("💪 Blood pressure normal.")

        return {
            "vitals": self.vitals,
            "assessment": status_messages
        }

    def get_first_aid_protocol(self):
        """
        Returns a friendly, standardized first-aid protocol text.
        (In a real system, this might come from a database or handbook.)
        """
        protocol = [
            "🚑 **SpaceVitals First-Aid Protocol**",
            "",
            "1. **Stay calm** — panic burns oxygen, and we kinda need that.",
            "2. **Check for breathing and pulse** — if none, alert mission control immediately.",
            "3. **Apply pressure to bleeding wounds** — use clean materials (not the snack napkins).",
            "4. **If dizziness or nausea** occurs, sit down, hydrate, and notify the onboard medic bot.",
            "5. **For burns** — cool with clean water for 10 minutes. Do NOT apply space lube.",
            "6. **For fractures or sprains** — immobilize the area and wait for recovery instructions.",
            "",
            "Remember: SpaceVitals is here for you — unless you’re trying to perform surgery with duct tape again."
        ]

        return {
            "title": "First-Aid Protocol",
            "steps": protocol,
            "last_updated": datetime.utcnow().isoformat()
        }
