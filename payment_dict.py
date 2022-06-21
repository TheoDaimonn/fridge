from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime, PaymentMethods

QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImV2bm8xNi0wMCIsInVzZXJfaWQiOiI3OTI1NTgzMzg5OSIsInNlY3JldCI6ImI1ODVmNmQ4ZjRiMjk2NjdhMGFmYzMxMjNhNDM4MjRkZTQ4OGZhMzc1M2Y0MjYwMDcxNmNhMWI0ZGRjOTA4MTQifX0="

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
def create_de_trans(id):
    # Выставим счет на сумму 228 рублей который будет работать 45 минут
    new_bill = p2p.bill(bill_id=id, amount=50, lifetime=45)

    return new_bill.pay_url

def check_status(id):
    return p2p.check(bill_id=id).status
    #WAITING/PAID