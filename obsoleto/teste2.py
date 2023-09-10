client_id = 'nbars8s2na3nae8zap2lfy05l8i2ja'
client_secret = 'geowab7ix4v0ua2z31cd5q9a381er7'
code_type = 'END_URL&'
code = None
grant_type = 'None'
redirect_uri = 'https://localhost:3000'
url_form = f'client_id={client_id}&client_secret={client_secret}&{code_type}={code}&grant_type={grant_type}&redirect_uri={redirect_uri}'
print(url_form[:url_form.index('&END_URL&')])