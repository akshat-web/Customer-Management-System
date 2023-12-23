import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    
st.markdown('<center><h1>LIFE LINE FOR CUSTOMERS</h1></center>',unsafe_allow_html=True)
choice = st.sidebar.selectbox('Menu',('Home','Login','Feedback','FAQ','Video Help','Contact Us','About Us','Write To Us'))
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXd9tEfZizLNBWvvdXI2aFKYCs0MjoO0qAZw&usqp=CAU')

if choice == 'Home':
    st.image('https://www.insightly.com/assets/images/pages/190701-why-insightly-crm_relationship-linking_2x.gif?_cchid=589b4e8de32aa9c082d87b56c554bdc9')
    st.markdown('<center><h1>Customer Management System</h1></center>',unsafe_allow_html=True)
    
elif choice == 'Login':
    if 'login' not in st.session_state:
        st.session_state['login']=False

    user = st.text_input('Admin Username')
    code = st.text_input('Password',type='password')

    if st.button('Login'):
        db = mysql.connector.connect(host='localhost',username='root',password='hello_sql',database='customer')
        cur = db.cursor()
        cur.execute('select*from admin')
        for row in cur:
            if user==row[0] and code==row[1]:
                st.session_state['login']=True       
                break

        if st.session_state['login']==False:
            st.subheader('Incorrrect username or password')

    if st.session_state['login']:
        st.subheader('Login Successful')
        select = st.selectbox('Options',('None','Add Customer','Delete Customer','Customer Basic Information','Customer Contacts','Customer Buying Preferences','Customer Payment Preferences','Visualize Customer Purchases','Complaints Recieved','Customer Interaction','Marking For Discount','Selecting For Gift Coupon','Analyze Feedback'))
        
        if select == 'Add Customer':
            ID = st.text_input('Create Id')
            first = st.text_input('First Name')
            last = st.text_input('Last Name')
            age = st.text_input('Age')
            gender = st.text_input('Gender')

            if st.button('Add'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                sql = ('insert into basic_information (customer_ID, first_name, last_name, age, gender) values (%s, %s, %s, %s, %s);')
                data = (ID, first, last, age, gender)
                cur.execute(sql,data)
                db.commit()
                st.write('Added Successfully')

        elif select == 'Delete Customer':
            ID = st.text_input('Enter Id')

            if st.button('Delete'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('delete from basic_information where customer_id = %s',(ID,))
                db.commit()
                st.write('Deleted Successfully')
                

        elif select == 'Customer Basic Information':
            unique = st.text_input('Enter Id')
            if st.button('Click'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from basic_information')
                l1 = []
                for row in cur:
                    if row[0] == unique:
                        l1.append(row)
                        break

                if l1 != []:
                    d = pd.DataFrame(data=l1,columns=['Customer ID','First Name','Last Name','Age','Gender'])
                    st.dataframe(d)
                else:
                    st.subheader("No Such Customer")


            
        elif select == 'Customer Contacts':
            unique = st.text_input('Enter Id')
            if st.button('Click'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from contacts')
                l2 = []
                for row2 in cur:
                    if row2[0] == unique:
                        l2.append(row2)
                        break

                if l2 != []:
                    d2 = pd.DataFrame(data=l2,columns=['Customer ID','Phone','E-mail','Address'])
                    st.dataframe(d2)
                else:
                    st.subheader("No Such Customer")

        elif select == 'Customer Buying Preferences':
            unique = st.text_input('Enter Id')
            if st.button('Click'):    
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from preference')
                l3 = []
                for row3 in cur:
                    if row3[0] == unique:
                        l3.append(row3)
                        break

                if l3 != []:
                    d3 = pd.DataFrame(data=l3,columns=['Customer ID','Most Bought Category','Least Bought Category'])
                    st.dataframe(d3)
                else:
                    st.subheader("No Such Customer")

        elif select == 'Customer Payment Preferences':
            unique = st.text_input('Enter Id')
            if st.button('Click'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from payment')
                l4 = []
                for row4 in cur:
                    if row4[0] == unique:
                        l4.append(row4)
                        break

                if l4 != []:
                    d4 = pd.DataFrame(data=l4,columns=['Customer ID','Cash','Card','UPI'])
                    st.dataframe(d4)
                else:
                    st.subheader("No Such Customer")
                
        elif select ==('Visualize Customer Purchases'):
            unique = st.text_input('Enter Id')
            if st.button('Click'):     
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from sales')
                l5 = []
                for col in cur:
                    if col[0] == unique:
                        l5.append(col)
                        break

                if l5 != []:
                    categories = ['Clothes','Foods','Electronics','Furniture','Make-Up']
                    fig = px.pie(values=[col[1],col[2],col[3],col[4],col[5]],names= categories)
                    st.plotly_chart(fig)
                else:
                    st.subheader("No Such Customer")
                
             

        elif select == 'Complaints Recieved':
            db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
            cur = db.cursor()
            cur.execute('select*from complaints')
            l6 = []
            for row6 in cur:
                l6.append(row6)

            d6 = pd.DataFrame(data=l6,columns=['Customer ID','Complaint','Resolved?'])
            st.dataframe(d6)

        elif select == 'Customer Interaction':
            sender_email = st.text_input("Sender's Email")
            sender_password = st.text_input("Sender's Password",type='password')
            recipient_email = st.text_input("Customer's Email")
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=200)
            attachment = st.file_uploader("Attachment (optional)")
            if st.button("Send Email"):
                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                #Create the email message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject

                #Attach the message body
                msg.attach(MIMEText(message, 'plain'))

                #Attach the file if provided
                if attachment is not None:
                    file_content = attachment.read()
                    attachment = MIMEApplication(file_content)
                    attachment.add_header('Content-Disposition', 'attachment', filename=attachment.name)
                    msg.attach(attachment)

                #Send the email
                try:
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    server.quit()
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        elif select == 'Marking For Discount':
            unique = st.text_input('Customer ID')

            if st.button('Find'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from sales')

                total_sales = 0
           
                l7 = []
                for col in cur:
                    if col[0] == unique:
                        total_sales = sum(col[1:])
                        break

                if total_sales == 0:
                    st.subheader('No Such Customer')
                else:
                    if total_sales>15000:
                        st.subheader('Eligible for discount for the next purchase')
                    else:
                        st.subheader('Not eligible for discount for the next purchase')

        elif select == 'Selecting For Gift Coupon':
            unique = st.text_input('Customer ID')

            if st.button('Find'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from payment')

                flag = 0
                for col in cur:
                    if col[0] == unique and col[3] == 'always':
                        flag = 1
                        break

                if flag == 1:
                    st.subheader('Customer Is Eligible For Gift Coupon')
                else:
                    st.subheader('Customer Is Not Eligible For Gift Coupon')

        elif select == 'Analyze Feedback':
            unique = st.text_input('Customer ID')

            if st.button('Find'):
                db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
                cur = db.cursor()
                cur.execute('select*from feedback')
                
                model = SentimentIntensityAnalyzer()
                flag = 0

                for row in cur:
                    if row[2] == unique:
                        flag = 1
                        x = row[1]
                        break

                if flag==1:
                    pred = model.polarity_scores(x)
                else:
                    st.subheader('No Such Customer')

                if pred['compound'] > 0.5:
                    st.subheader('Positive')
                elif -0.5 <  pred['compound'] < 0.5:
                    st.subheader('Neutral')
                else:
                    st.subheader('Negative')

                    
                                    
                
    if st.button('Log Out'):
        st.subheader('You Are Logged Out')
        st.session_state['login']=False
        st.rerun()

elif choice == 'Feedback':
    st.subheader('What Do You Think About Us?')
    name = st.text_input('Name')
    ID = st.text_input('Customer ID')
    feed = st.text_input('Feedback')
    if st.button('click'):
        db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
        cur = db.cursor()
        cur.execute('select*from basic_information')
        flag=0
        for row in cur:
            if row[0] == ID:
                flag=1
                break

        if flag==1:
            db = mysql.connector.connect(host='localhost',user='root',password='hello_sql',database='customer')
            cur = db.cursor()
            cur.execute('insert into feedback (names,review,customer_id) values (%s,%s,%s)',(name,feed,ID))
            db.commit()
            st.write('Submitted Successfully')
        else:
            st.write('No such customer')
    
elif choice == 'FAQ':
    st.subheader('Frequently Asked Questions(FAQs)')
    
    st.write('1. What is a "Customer Management System?"')
    st.write("Ans. It's a software solution or a set of tools and processes designed to help businesses manage and maintain relationships with their customers.")
    st.write('2. Why to use it?')
    st.write('Ans. It is easy to use and efficient and it is really helpful for building and maintaing relationship with customers and for benefit of both, the organization and the customers.')
    st.write('3. How to use it?')
    st.write('Ans. Just fill up the information as asked')

elif choice == 'Video Help':
    st.subheader('For knowledge about "Customer Management System/Customer Relation Management", watch the following video:')
    st.video('https://www.youtube.com/watch?v=ndPabqQ4osk')

elif choice == 'Contact Us':
    st.subheader('If you have any queries, contact us:')
    st.write('Email : green2red@gmail.com')
    st.write('Phone : 2230909')
    st.image('https://media.sciencephoto.com/c0/55/40/76/c0554076-800px-wm.jpg')

elif choice == 'About Us':
    st.write('1. We are "XYZ Corporations" - one of the leading corporations in database management sphere')
    st.write("2. 'Life Line For Customers' is our most successful customer management system")
    st.write("3. 'Life Line For Customers' manages customer data for betterment of customer-organization relations")
    st.image('https://www.invensislearning.com/blog/wp-content/uploads/2020/09/How-To-Set-Up-A-Quality-Management-System-1068x552-1.jpg')

elif choice == 'Write To Us':
    st.subheader('You can write to us here:')
    st.write('Email : green2red@gmail.com')
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7NF7VXHOOk-CW_eNyVlsAyi-R0c4hotVuJg&usqp=CAU')



                        

                

        
                    
                    
             




       
