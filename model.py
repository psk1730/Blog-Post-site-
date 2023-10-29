import mysql.connector
con=mysql.connector.connect(host= 'localhost', user= 'root', password='', database='codingthunder')

cur= con.cursor()
        cur.execute('INSERT INTO contact (name, Email, phone, mes) VALUES(%s,%s,%s,%s)', (name, email,phone,message))
        con.commit()
        return render_template('contact.html')