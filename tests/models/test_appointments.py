from model_bakery import baker


def test__total_duration():
    s1 = baker.make("med_spa.Service")
    s2 = baker.make("med_spa.Service")
    appt = baker.make("med_spa.Appointment", services=[s1, s2])
    assert appt.total_duration == s1.duration + s2.duration


def test__total_price():
    s1 = baker.make("med_spa.Service")
    s2 = baker.make("med_spa.Service")
    appt = baker.make("med_spa.Appointment", services=[s1, s2])
    assert appt.total_price == s1.price + s2.price
