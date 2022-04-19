from datetime import date


def any_date_before_today(given_date):
    given_date_year = int(given_date[:4])
    given_date_month = int(given_date[5:7])
    given_date_date = int(given_date[8:])
    today = str(date.today())
    today_year = int(today[:4])
    today_month = int(today[5:7])
    today_date = int(today[8:])
    is_valid = False
    if (today_year > given_date_year) or (
        (today_year == given_date_year)
        and (
            (today_month > given_date_month)
            or ((today_month == given_date_month) and (today_date > given_date_date))
        )
    ):
        is_valid = True
    return is_valid


def issue_expiry_checker(issue, expiry):
    if not any_date_before_today(issue):
        return False
    issue_year = int(issue[:4])
    issue_month = int(issue[5:7])
    issue_date = int(issue[8:])
    expiry_year = int(expiry[:4])
    expiry_month = int(expiry[5:7])
    expiry_date = int(expiry[8:])
    is_valid = False
    if (expiry_year > issue_year) or (
        (expiry_year == issue_year)
        and (
            (expiry_month > issue_month)
            or ((expiry_month == issue_month) and (expiry_date > issue_date))
        )
    ):
        is_valid = True
    return is_valid
