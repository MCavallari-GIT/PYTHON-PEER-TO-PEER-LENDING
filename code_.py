# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:09:43 2021


"""
#L
def insert_loan(command):
    amount=command[1]
    perc=command[2]
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("INSERT INTO progetto_cavallari.richieste (sum,perc,processed) values (%s,%s,'false');", (amount,perc))
    conn.commit()
    cur.close()
    update()

#B
def insert_bid(command):
    amount=command[1]
    perc=command[2]
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("INSERT INTO progetto_cavallari.offerte (sum,perc,processed) values (%s,%s,'false');", (amount,perc))
    conn.commit()
    cur.close()
    #conn.close()
    update()

def update():
    used=[]
    somma=0
    rate=0
    #offerte=[]
    #offerte_perc=[]
    conn2=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur1=conn2.cursor()
    cur1.execute("select * from progetto_cavallari.richieste where processed=false;")
    r=cur1.fetchall()
    #print(r)
    for richiesta in r:
        target=richiesta[3]
        target_per=richiesta[1]
        cur=conn2.cursor()
        cur.execute("select * from progetto_cavallari.offerte where processed=false and perc<=%s order by perc asc, sum desc;",([richiesta[1]]))
        o=cur.fetchall()
        #print("richiesta coorrente:    ",richiesta)
        for offerta in o:
            #print ("offerta disponiile      ",offerta)
            if(somma+offerta[3]>=richiesta[3]):
                rate=rate+((offerta[1]*(target-somma))/target)
                somma=somma+(target-somma)
                used.append(offerta)
                break
            used.append(offerta)
            somma=somma+offerta[3]
            rate=rate+((offerta[1]*offerta[3])/target)
        if somma<target:
            rate=0
            somma=0
            used=[]
        #print("finale",somma)
        #print("finale rate",rate)
        #print("offerte utilizzate",used)
        #marco anche la richiesta in questione (solo se ho trovato un asoluzione)
        if somma==target:
            cur3=conn2.cursor()
            cur3.execute("update progetto_cavallari.richieste set processed='true' where sum=%s and perc=%s and id=%s;",(richiesta[3],richiesta[1],richiesta[0]))
            conn2.commit()
        #ora bisogna salvare marcare le offerte utilizzate ed inserirle nella tabella contratti
        for tupla in used:
            cur3=conn2.cursor()
            cur3.execute("update progetto_cavallari.offerte set processed='true' where sum=%s and perc=%s and id=%s;",(tupla[3],tupla[1],tupla[0]))
            conn2.commit()
            cur=conn2.cursor()
            cur.execute("INSERT INTO progetto_cavallari.contratti (id_richiesta,id_offerta,sum,perc) values (%s,%s,%s,%s);", (richiesta[0],tupla[0],target,rate))
            conn2.commit()
        somma=0
        rate=0

#UL
def unmatched_loan():
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("select * from progetto_cavallari.richieste where processed='false';")
    unmatched=cur.fetchall()
    for i in unmatched:
        print(i[3],i[1])
    if len(unmatched)==0:
        print("No result(s)")
    conn.commit()
    cur.close()

#UB
def unmatched_bid():
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("select * from progetto_cavallari.offerte where processed='false';")
    unmatched=cur.fetchall()
    for i in unmatched:
        print(i[3],i[1])
    if len(unmatched)==0:
        print("No result(s)")
    conn.commit()
    cur.close()


#CL a c
#cancella una/più loan. Assumiamo (non essendo specificato nel testo) che si possano cancellare loans/bids se e solo se
#esse non sono ancora state utilizzate in un contratto

#è possibile siano presenti piu loans uguali sia nel amount che nell tasso di interessi. Noi andreamo ad eliminarli tutti
def cancel_loan(command):
    amount=command[1]
    perc=command[2]
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("delete from progetto_cavallari.richieste where sum=%s and perc=%s and processed='false' ;",(amount,perc))
    if cur.rowcount==0:
        print("Error")
    conn.commit()


#CB a r
#cancella una/più bid. Assumiamo (non essendo specificato nel testo) che si possano cancellare loans/bids se e solo se
#esse non sono ancora state utilizzate in un contratto

#è possibile siano presenti piu loans uguali sia nel amount che nell tasso di interessi. Noi andreamo ad eliminarli tutti
def cancel_bid(command):
    amount=command[1]
    perc=command[2]
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("delete from progetto_cavallari.offerte where sum=%s and perc=%s and processed='false' ;",(amount,perc))
    if cur.rowcount==0:
        print("Error")
    conn.commit()


#NA
def close_agreed_loans():#quelli che io ho chiamato contratti
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("WITH rows AS ( SELECT distinct id_richiesta FROM progetto_cavallari.contratti) SELECT count(*) FROM rows;")
    n=cur.fetchall()
    if n[0][0]!=0:
        print(n[0][0])
    else:
        print("No result(s)")


#NG a
def agreed_loans_at_most(command):
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("WITH rows AS ( SELECT distinct id_richiesta FROM progetto_cavallari.contratti where sum<=%s) SELECT count(*) FROM rows;",[command[1]])
    n=cur.fetchall()
    if n[0][0]!=0:
        print(n[0][0])
    else:
        print("No result(s)")


#T
def total_amount():
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("WITH rows AS ( SELECT distinct id_richiesta,sum FROM progetto_cavallari.contratti) SELECT sum(sum) FROM rows;")
    n=cur.fetchall()
    if n[0][0]!=0:
        print(n[0][0])
    else:
        print("No result(s)")


#W
def avarage():
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("SELECT distinct id_richiesta,sum,perc FROM progetto_cavallari.contratti;")
    n=cur.fetchall()
    avg=0
    sum=0
    for x in n:
        avg=avg+(x[1]*x[2])
        sum=sum+x[1]
    print(round(avg/sum,4))


#A
def all_agreed_loans():
    conn=psycopg2.connect(dbname="postgres",user="postgres",password="Cava1999",host="localhost")
    cur=conn.cursor()
    cur.execute("SELECT distinct id_richiesta,sum,perc FROM progetto_cavallari.contratti;")
    n=cur.fetchall()
    for x in n:
        print(x[1],round(x[2],4))
    if len(n)==0:
        print("No result(s)")


def is_number(b):
    try:
        float(b)
        return True
    except ValueError:
        return False

def main():
    command=['start']
    while command[0]!='X':
        command=list(map(str,input('> ').split()))
        if len(command)==0:
            break
        if command[0]=='L' and len(command)==3:
            if is_number(command[2])==True and is_number(command[1]) and float(command[2])<=100:
                insert_loan(command)
            else:
                print("Error")
        elif command[0]=='B' and len(command)==3:
            if is_number(command[2])==True and is_number(command[1]) and float(command[2])<=100:
                insert_bid(command)
            else:
                print("Error")
        elif command[0]=='UL' and len(command)==1:
            unmatched_loan()
        elif command[0]=='UB' and len(command)==1:
            unmatched_bid()
        elif command[0]=='CL' and len(command)==3:
            if is_number(command[2])==True and is_number(command[1]) and float(command[2])<=100:
                cancel_loan(command)
            else:
                print("Error")
        elif command[0]=='CB' and len(command)==3:
            if is_number(command[2])==True and is_number(command[1]) and float(command[2])<=100:
                cancel_bid(command)
            else:
                print("Error")
        elif command[0]=='NA' and len(command)==1:
            close_agreed_loans()
        elif command[0]=='NG' and len(command)==2:
            if is_number(command[1])==True:
                agreed_loans_at_most(command)
            else:
                print("Error")
        elif command[0]=='T' and len(command)==1:
            total_amount()
        elif command[0]=='W' and len(command)==1:
            avarage()
        elif command[0]=='A' and len(command)==1:
            all_agreed_loans()
        elif command[0]=='X':
            continue
        else:
            print("Error")


import psycopg2
main()
