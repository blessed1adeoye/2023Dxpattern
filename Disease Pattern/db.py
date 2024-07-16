import sqlite3


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.c = self.con.cursor()
        self.c.execute(""" CREATE TABLE IF NOT EXISTS disease ( 
                                                            Diagnosis TEXT,
                                                            Code TEXT,
                                                            male_less_than_1_yr TEXT,
                                                            female_less_than_1_yr TEXT,
                                                            male_1_14 TEXT,
                                                            female_1_14 TEXT,
                                                            male_15_44 TEXT,
                                                            female_15_44 TEXT,
                                                            male_45_64 TEXT,
                                                            female_45_64 TEXT,
                                                            male_65_above TEXT,
                                                            female_65_above TEXT,
                                                            male_total TEXT,
                                                            female_total TEXT,
                                                            Grand_total TEXT    )                                        
                       """)

        self.con.commit()

    def fetchRecord(self, query):
        self.c.execute(query)
        rows = self.c.fetchall()
        return rows

    def insertDx(
            self, dxs, code, m_l_1, fm_l_1, m_1_14,
            fm_1_14, m_15_44, fm_15_44, m_45_64,
            fm_45_64, m_65_above, fm_65_above, m_t, f_t, t_grand):
        self.c.execute(
            "INSERT INTO disease VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (dxs, code, m_l_1, fm_l_1, m_1_14,
             fm_1_14, m_15_44, fm_15_44, m_45_64,
             fm_45_64, m_65_above, fm_65_above, m_t, f_t, t_grand
             )
        )
        self.con.commit()

    def removeDx(self, rwid):
        self.c.execute("DELETE FROM disease WHERE rowid=?", (rwid,))
        self.con.commit()

    def removeUser(self, rwid):
        self.c.execute("DELETE FROM userTable WHERE rowid=?", (rwid))
        self.con.commit()

    def updateUser(self,txt_id, txt_name, txt_pass,rid):
        self.c.execute(
            "UPDATE userTable SET RegNo=?, Username=?, Password=?, rowid",
            (txt_id, txt_name,txt_pass,rid)
        )
        self.con.commit()

    def updateDx(self, dxs, code, m_l_1, fm_l_1, m_1_14,
                 fm_1_14, m_15_44, fm_15_44, m_45_64,
                 fm_45_64, m_65_above, fm_65_above, m_t, f_t, t_grand, rid):
        self.c.execute(
            "UPDATE  disease SET Diagnosis=?, Code=?, male_less_than_1_yr=?, female_less_than_1_yr=?, male_1_14=?, female_1_14=?,male_15_44=?, female_15_44=?, male_45_64=?, female_45_64=?, male_65_above=?, female_65_above=?, male_total=?, female_total=?, Grand_total=?, rowid",
            (dxs, code, m_l_1, fm_l_1, m_1_14,
             fm_1_14, m_15_44, fm_15_44, m_45_64,
             fm_45_64, m_65_above, fm_65_above, m_t, f_t, t_grand, rid)
        )
        self.con.commit()

    def bhuwah(self):
        self.c.execute("DROP TABLE IF EXISTS disease")
        self.con.commit()

    def __del__(self):
        self.con.close()
