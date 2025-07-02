<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>業務委託契約書</title>
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
    <h2>業務委託契約書</h2>

    <p>本契約は、以下の通り業務委託契約を締結する。</p>

    <p><strong>第1条（契約当事者）</strong><br>
    委託者：{{ client_name }}<br>
    受託者：{{ contractor_name }}</p>

    <p><strong>第2条（業務内容）</strong><br>
    受託者は、以下の業務を遂行する。<br>
    業務内容：{{ task_description }}</p>

    <p><strong>第3条（契約期間）</strong><br>
    本契約の期間は、{{ start_date }}から{{ end_date }}までとする。</p>

    <p><strong>第4条（報酬および支払方法）</strong><br>
    報酬総額：¥{{ total_fee }}（税込）<br>
    支払方法：{{ payment_method }}<br>
    支払期日：{{ payment_due_date }}</p>

    <p><strong>第5条（秘密保持）</strong><br>
    受託者は業務上知り得た情報を第三者に漏洩してはならない。</p>

    <p><strong>第6条（再委託の禁止）</strong><br>
    受託者は、委託者の書面による同意なしに業務を第三者に再委託してはならない。</p>

    <p><strong>第7条（著作権）</strong><br>
    本業務により作成された成果物の著作権は、{{ copyright_holder }} に帰属する。</p>

    <p><strong>第8条（契約解除）</strong><br>
    以下の場合、各当事者は契約を解除できる：<br>
    - 相手方が契約違反を是正しないとき<br>
    - やむを得ない理由があるとき</p>

    <p>{{ contract_date }}</p>

    <p>委託者署名：＿＿＿＿＿＿＿＿＿＿＿＿<br>
    受託者署名：＿＿＿＿＿＿＿＿＿＿＿＿</p>
</body>
</html>
