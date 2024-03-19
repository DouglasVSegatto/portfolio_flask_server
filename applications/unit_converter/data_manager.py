
def km_to_miles(km):
    """
    Converts kilometers to miles

    :param km: Kilometers to be converted to miles.
    :type km: Float.
    :return: Kilometers converted to miles.
    :rtype: Float
    """
    miles = km * 0.621371
    return miles


def miles_to_km(miles):
    """
    Converts miles to km

    :param miles: Miles to be converted.
    :type miles: Float.
    :return: Miles converted to kilometers.
    :rtype: Float.
    """
    km = miles * 1.60934
    return km


def l_per_100km_to_km_per_l(l_per_100km):
    """
    Converts liter per 100km to kilometers per liter

    :param l_per_100km: Liters/100km to be converted.
    :type l_per_100km: Float.
    :return: Liter/100km converted to kilometers/liter.
    :rtype: Float.
    """

    km_per_l = 100 / l_per_100km
    return km_per_l


def mpg_to_km_per_100(mpg):
    """
    Convert miles per gallon (mpg) to kilometers per 100 miles.

    :param mpg: Miles per gallon to be converted.
    :type mpg: Float.
    :return: MPG converted in kilometers per 100 miles.
    :rtype: Float.
    """

    km_per_100 = 100 / (mpg * 0.621371)  # 0.621371 is the conversion factor from miles to kilometers
    return km_per_100
