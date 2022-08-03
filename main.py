import requests
import pprint
import json

def get_data_from_yanoshin():
    
    base_url = "https://webapi.yanoshin.jp/webapi/tdnet/list/"
    condition = "today"
    format = "json"
    query = "limit=False"
    res = requests.get(base_url+condition+'.'+format+'?'+query)
    res_loads = json.loads(res.content)
    pprint.pprint(res_loads)

    return res_loads

def pickup_growth_possibility_material(data):
    
    output = []
    for x in data['items']:
        if "月度" in x["Tdnet"]["title"]:
            output.append([x['Tdnet']['company_name'], x['Tdnet']['document_url']])

    return output

def send_email(data):
    # メール送信関係
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    from_adress = "o.fukushi@gmail.com"  # 送付もとメールアドレス、gmailを前提
    from_adress_pass = "ntnzrxobhdjfneys"  # Google accountから発行されるアプリパスワードに変更（２要素認証）
    to_adress = "o.fukushi@gmail.com"  # 受信メールアドレス

    string = ""

    if len(data):
        for i in range(len(data)):
            string = string + str(data[i][0]) + "\n" + str(data[i][1])
    else:
        string = "本日は対象データがありません"

    msg = MIMEText("月次売上速報 \n\n" + string, "plain")
    msg["Subject"] = Header("from_bot 月次売上速報")

    smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(from_adress, from_adress_pass)
    smtp_obj.sendmail(from_adress, to_adress, msg.as_string())
    smtp_obj.quit()

if __name__ == '__main__':
    data = get_data_from_yanoshin()
    pickup_data = pickup_growth_possibility_material(data)
    pprint.pprint(pickup_data)
    send_email(pickup_data)