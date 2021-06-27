from wait_service import Wait

w = Wait(driver="", timeout=5)

w.wait_until_alert_present()