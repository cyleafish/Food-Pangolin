# 開發需要注意的東西
- 資料表問題<br>
因為將所有帳號資訊都紀錄在 user_account 表中，因此在需要獲得此使用者資訊時需要注意 id 問題<br>
ex. 獲得目前使用者 id `user_id = session.get('user_id')`<br>
在 dbUtil 的 query 需注意要將 user_account 跟該使用者角色的資料表做對應(用 username)<br>
query = """<br>
        SELECT <br>
            ua.user_id,<br>
            ua.username,<br>
            ua.role,<br>
            d.deliver_id,<br>
            d.deliver_name,<br>
            d.phone,<br>
            d.car_num<br>
        FROM user_account ua<br>
        LEFT JOIN deliver d ON ua.username = d.deliver_name<br>
        WHERE ua.role = 'deliver' AND ua.user_id = %s;<br>
    """<br>
