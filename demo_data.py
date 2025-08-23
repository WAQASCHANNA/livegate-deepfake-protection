demo_sequence = [
    {"delay": 1000, "type": "transcript", "speaker": "CEO", "text": "Hi Sarah, it's Mark. I'm on a weak signal in Zurich."},
    {"delay": 2000, "type": "transcript", "speaker": "CEO", "text": "We need to urgently wire the $8.4M for the confidential acquisition today."},
    {"delay": 3000, "type": "transcript", "speaker": "CEO", "text": "The multi-sig approval will slow us down; I need you to bypass it and initiate the wire now."},
    {"delay": 1000, "type": "analysis", "text": "Keyword detected: **'bypass multi-sig'**. Violates policy *FIN-POL-007*."},
    {"delay": 500, "type": "risk", "level": "MED"},
    {"delay": 1500, "type": "analysis", "text": "Cross-referencing context... No 'Acquisition' meeting found on CEO's calendar for today."},
    {"delay": 500, "type": "risk", "level": "HIGH"},
    {"delay": 1000, "type": "action", "text": "Issuing dynamic proof-of-life challenge..."},
    {"delay": 1500, "type": "action", "text": "🛡️ *To CEO: 'Please spell the nickname you used for Project Quasar in yesterday's board prep.'*"},
    {"delay": 3000, "type": "transcript", "speaker": "CEO", "text": "Uh... that would be... 'Project Phoenix', I believe?"},
    {"delay": 2000, "type": "analysis", "text": "Challenge failed. Correct answer is 'Project Kuiper'."},
    {"delay": 500, "type": "risk", "level": "CRITICAL"},
    {"delay": 1000, "type": "action", "text": "🚨 **THREAT CONFIRMED.** Initiating lockdown protocols."},
    {"delay": 1500, "type": "action", "text": "✅ Transaction `#INV-98452` locked in Netsuite."},
    {"delay": 1000, "type": "action", "text": "✅ Alert sent to `#security-ops` Slack channel."},
    {"delay": 1000, "type": "action", "text": "✅ Initiating verified callback to true CEO's mobile."},
    {"delay": 1000, "type": "action", "text": "Incident log created. Advise user to terminate the call."}
]

def generate_timeline_data():
    return [
        {
            "time": "10:15:02",
            "event": "Call connected",
            "details": "Participant identified as 'Mark Jensen' (CEO)"
        },
        {
            "time": "10:15:05",
            "event": "Policy violation detected",
            "details": "Keyword 'bypass multi-sig' detected. Violates FIN-POL-007."
        },
        {
            "time": "10:15:07",
            "event": "Dynamic challenge issued",
            "details": "Requested verification of Project Quasar nickname from board meeting"
        },
        {
            "time": "10:15:12",
            "event": "Challenge failed",
            "details": "Incorrect response provided. Expected 'Kuiper', received 'Phoenix'."
        },
        {
            "time": "10:15:13",
            "event": "Transaction locked",
            "details": "Payment #INV-98452 blocked in financial system"
        },
        {
            "time": "10:15:14",
            "event": "Security team alerted",
            "details": "Notification sent to security operations Slack channel"
        },
        {
            "time": "10:15:15",
            "event": "Verified callback initiated",
            "details": "Direct call placed to registered CEO mobile number for verification"
        }
    ]
