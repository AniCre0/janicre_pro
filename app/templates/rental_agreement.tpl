<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>賃貸借契約書</title>
    <style>
        body {
            font-family: "Helvetica", "Arial", sans-serif;
            line-height: 1.6;
        }
        p {
            margin: 12px 0;
        }
    </style>
</head>
<body>
    <h2>賃貸借契約書</h2>

    <p>本契約は、以下の条件に従って賃貸借契約を締結するものである。</p>

    <p><strong>第1条（契約当事者）</strong><br>
    貸主：{{ lessor_name }}<br>
    借主：{{ lessee_name }}</p>

    <p><strong>第2条（物件）</strong><br>
    物件住所：{{ property_address }}<br>
    構造：{{ property_structure }}<br>
    面積：{{ property_size }} 平方メートル</p>

    <p><strong>第3条（契約期間）</strong><br>
    本契約の期間は、{{ start_date }}から{{ end_date }}までとする。</p>

    <p><strong>第4条（賃料）</strong><br>
    月額賃料：¥{{ rent_amount }}（税込）<br>
    支払期日：毎月{{ payment_day }}日</p>

    <p><strong>第5条（敷金・礼金）</strong><br>
    敷金：¥{{ deposit_amount }}<br>
    礼金：¥{{ key_money }}</p>

    <p><strong>第6条（禁止事項）</strong><br>
    借主は以下の行為を行ってはならない：<br>
    1. 無断転貸<br>
    2. 改造・改築<br>
    3. 近隣に迷惑をかける行為</p>

    <p><strong>第7条（契約解除）</strong><br>
    契約期間中に解約する場合は、{{ notice_period }}日前までに書面にて通知すること。</p>

    <p><strong>第8条（原状回復）</strong><br>
    契約終了時、借主は物件を原状回復し返却する。</p>

    <p>本契約締結の証として、貸主および借主は本書2通を作成し、各自署名・押印の上、各1通を保有する。</p>

    <p>{{ contract_date }}</p>

    <p>貸主署名：＿＿＿＿＿＿＿＿＿＿＿＿<br>
    借主署名：＿＿＿＿＿＿＿＿＿＿＿＿</p>
</body>
</html>
