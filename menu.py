import mysql.connector


class Menu:
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        database="examenpy",
        user="root",
        password=""
    )
    cursor = conn.cursor()

    @staticmethod
    def ajouteAide():
        designation = str(input("Designation : "))
        print("Type :")
        print("1. Couverture")
        print("2. Denree Alimentaire")
        print("3. Matlas")
        types=""
        res = int(input())
        if res == 1:
            types="couverture"
        elif res == 2:
            types = "denree alimentaire"
        else:
            types = "matlas"
        quantite = int(input("Quantite :"))
        query = "Select * from aide where designation=%s"
        value = [designation]
        Menu.cursor.execute(query, value)
        row=Menu.cursor.fetchone()
        if row is None:
            query = "INSERT INTO aide (designation,type,quantite) VALUES (%s,%s,%s)"
            value = (designation, types, quantite)
            Menu.conn.commit()
        else:
            query = "UPDATE aide SET quantite=quantite+%s where designation=%s"
            value = (quantite, designation)
        Menu.cursor.execute(query, value)
        Menu.conn.commit()

    @staticmethod
    def afficheAide():
        Menu.cursor.execute("SELECT * FROM aide")
        rows = Menu.cursor.fetchall()

        for row in rows:
            print(row)

    @staticmethod
    def afficheFamille():
        Menu.cursor.execute("SELECT * FROM famille")
        rows = Menu.cursor.fetchall()

        for row in rows:
            print(row)

    @staticmethod
    def afficheMinMax():
        Menu.cursor.execute("SELECT * FROM aide WHERE quantite = (SELECT MAX(quantite) FROM aide)")
        rows = Menu.cursor.fetchall()

        print("Les aides qui ont la plus grande quantite :")
        for row in rows:
            print(row)

        Menu.cursor.execute("SELECT * FROM aide WHERE quantite = (SELECT MIN(quantite) FROM aide)")
        rows = Menu.cursor.fetchall()

        print("Les aides qui ont la plus petite quantite :")
        for row in rows:
            print(row)

    @staticmethod
    def controleStock():
        Menu.cursor.execute("SELECT * FROM aide WHERE quantite<=5")
        rows = Menu.cursor.fetchall()

        for row in rows:
            print(row)

    @staticmethod
    def ajouteFamille():
        cin = input("CIN de chef du famille : ")
        Menu.cursor.execute("SELECT * FROM famille WHERE cin=%s", [cin])
        row=Menu.cursor.fetchone()
        clean=Menu.cursor.fetchall()
        if row is not None:
            print("Famille deja existante ! ")
        else:
            nbr = int(input("Nombre des membres de la famille : "))
            delegation = input("La delegation associee : ")
            Menu.cursor.execute("INSERT INTO famille (cin,nombre,delegation) VALUES (%s,%s,%s)",
                                (cin, nbr, delegation))
            Menu.conn.commit()

    @staticmethod
    def affecteAide():
        Menu.cursor.execute("SELECT designation,type,quantite FROM aide WHERE type=%s order by quantite desc ", ["couverture"])
        row1 = Menu.cursor.fetchone()
        clean=Menu.cursor.fetchall()
        quantite1 = row1[2]
        Menu.cursor.execute("SELECT designation,type,quantite FROM aide WHERE type=%s order by quantite desc ", ["matlas"])
        row2 = Menu.cursor.fetchone()
        clean = Menu.cursor.fetchall()
        quantite2 = row2[2]
        quantite = min(quantite1, quantite2)
        Menu.cursor.execute("SELECT designation,type,quantite FROM aide WHERE type=%s", ["denree alimentaire"])
        res=Menu.cursor.fetchone()
        clean = Menu.cursor.fetchall()
        Menu.cursor.execute("SELECT cin,nombre,delegation FROM famille WHERE nombre<=%s order by nombre desc ", [quantite])
        row = Menu.cursor.fetchone()
        clean = Menu.cursor.fetchall()
        if row is None or res is None:
            print("On peut pas affecter une aide")
        else:
            try:
                Menu.cursor.execute("Delete From famille WHERE cin = %s", [row[0]])
                query = "UPDATE aide SET quantite = quantite-%s WHERE designation = %s and type= %s "
                values = [row[1], row1[0], row1[1]]
                Menu.cursor.execute(query, values)

                query2 = "UPDATE aide SET quantite = quantite-%s WHERE designation = %s and type= %s "
                values2 = [row[1], row2[0], row2[1]]
                Menu.cursor.execute(query2, values2)

                query3 = "UPDATE aide SET quantite = quantite-%s WHERE designation = %s and type= %s "
                values3 = [1, res[0], res[1]]
                Menu.cursor.execute(query3, values3)

                Menu.conn.commit()

                print("Tables updated successfully.")

            except mysql.connector.Error as error:
                Menu.conn.rollback()
                print(error)
