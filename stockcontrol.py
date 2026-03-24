from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, VARCHAR    # import used types
from sqlalchemy.orm import declarative_base, sessionmaker

import os   #clear screen

from utils import fanymodules as fm    # my own "lib"

from datetime import datetime    # import day and hour

from tabulate import tabulate   # print a beautiful table

from colorama import init, Back, Style    # colors
init()


DATABASE_URL = # postgresql+psycopg2://usuario:senha@localhost:5432/your_database


engine = create_engine(DATABASE_URL)   # connect with the database
Session = sessionmaker(bind=engine)
Base = declarative_base()



#------------------- MENU -------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    #clear screen


def menu():
    clear_screen()
    print(f'{Back.CYAN}========== M E N U =========={Style.RESET_ALL}')
    print('0 - finish program')
    print('1 - register product')
    print('2 - register sale')
    print('3 - remove product')
    print('4 - verify item in stock')
    print('5 - verify alerts')
    print('6 - verify results')
    print('7 - check tables')


    choice = fm.input_choice(
            msg = 'enter the option here: ',
            valid_options = (0, 1, 2, 3, 4, 5, 6, 7),
            error_msg = 'Invalid option.',
            use_color = True
        )
    return choice



#------------------- CLASSES -------------------

class StockTable(Base):   # class is mandatory with database
    __tablename__ = 'stock'   # creating table stock
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    quantity = Column(Integer)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    profit_reais = Column(Float)
    profit_percent = Column(Float)
    date = Column(TIMESTAMP)



class SalesTable(Base):   # class is mandatory with database
    __tablename__ = 'sales'   # creating table sales
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    quantity = Column(Integer)
    sale_unit_price = Column(Float)
    sale_total_price = Column(Float)
    sale_profit = Column(Float)
    profitsale_percent = Column(Float)
    date = Column(TIMESTAMP)



class ExcludeTable(Base):   # class is mandatory with database
    __tablename__ = 'excluded'   # creating table excluded
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    unit_prejudice = Column(Float)
    total_prejudice = Column(Float)
    quantity = Column(Integer)
    reason = Column(String)
    date = Column(TIMESTAMP)


Base.metadata.create_all(engine) # create all tables in database



#------------------- FUNÇÕES -------------------

def option_1():  # register product
    while True:
        
        
        product = fm.input_alpha(msg = 'enter the new product name: ',
                                 error_msg = 'Invalid name.',
                                 case = 'title',
                                 use_color = True)


        product_type = fm.input_alpha(msg = 'enter the product type: ',
                                     error_msg = 'Invalid type.',
                                     case = 'title',
                                     use_color = True)


        size = fm.input_non_empty(msg = 'enter the product size here: ',
                                  error_msg = 'Invalid size.',
                                  case = 'title',
                                  use_color = True)

        
        quantity = fm.input_int(msg = 'enter the quantity: ',
                                min_value = 1,
                                max_value = 100,
                                error_msg = 'Invalid number.',
                                use_color = True)


        with Session() as session:  #create session

            existing_product = session.query(StockTable).filter_by(     # verify if product already exists using the variables below
                    product=product,
                    product_type=product_type,
                    size=size
                ).first()


            if existing_product:    # if product already exists, just update the quantity
                existing_product.quantity = existing_product.quantity + quantity
                session.commit()
                print(f'{Back.GREEN}Product already exists in Stock, quantity updated to: {existing_product.quantity}!{Style.RESET_ALL}')


            else:    # if not, create new register
                
                
                purchase_price = fm.input_float(msg = 'enter the price of each item here: ',
                                                min_value = 0.10, max_value = 1000,
                                                error_msg = 'Invalid price.',
                                                use_color = True)


                sale_price = fm.input_float(msg = 'enter the sale price of each item here: ',
                                                min_value = 0.10, max_value = 1000,
                                                error_msg = 'Invalid price.',
                                                use_color = True)


                profit_reais = sale_price - purchase_price  # profit reais


                profit_percent = (sale_price - purchase_price) / sale_price * 100   # profit percent


                date = datetime.now()   # date
            
            
                try:
                    new_record = StockTable(product=product, product_type=product_type, size=size, quantity=quantity,
                                            purchase_price=purchase_price, sale_price=sale_price,
                                            profit_reais=profit_reais, profit_percent=profit_percent, date=date)
                        
                    session.add(new_record)
                    session.commit()     # enter in PostgreSQL
                    print(f'{Back.GREEN}Product registered with success in stock table!{Style.RESET_ALL}')
                    
                except Exception as error:
                    session.rollback()
                    print(f'{Back.RED}ERROR: {error}{Style.RESET_ALL}')
                


        if not fm.get_confirm(msg = 'Do you want to insert other item in stock? (yes/no): ',
                          yes = 'yes',
                          no = 'no',
                          error_msg = 'Invalid option.'
                          , use_color = True):
            break



def option_2():  # register sale
    while True:
        
       
        product = fm.input_alpha(msg = 'enter the product name here: ',
                                     error_msg = 'Invalid name.',
                                     case = 'title',
                                     use_color = True)


        product_type = fm.input_alpha(msg = 'enter the product type: ',
                                     error_msg = 'Invalid type.',
                                     case = 'title',
                                     use_color = True)


        size = fm.input_non_empty(msg = 'enter the product size here: ',
                                  error_msg = 'Invalid size.',
                                  case = 'title',
                                  use_color = True)


        sale_unit_price = fm.input_float(msg = 'enter the sold price: ',
                                        min_value = 0.10,
                                        max_value = 1000,
                                        error_msg = 'Invalid price.',
                                        use_color = True)


        quantity = fm.input_int(msg = 'enter the sold quantity here: ',
                                min_value = 1,
                                max_value = 100,
                                error_msg = 'Invalid quantity.',
                                use_color = True)


        sale_total_price = sale_unit_price * quantity   #total sale price
        
        
        date = datetime.now()   # date


        with Session() as session:  #create session


            # search item in stock
            stock_item = session.query(StockTable).filter_by(
                product=product,
                product_type=product_type,
                size=size
                ).first()


            # check if exist
            if not stock_item:
                print(f'{Back.RED}ERROR: {product} {product_type} {size} Does not exist in stock.{Style.RESET_ALL}')

                if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                yes = 'yes',
                                no = 'no',
                                error_msg = 'Invalid option.',
                                use_color = True):  # verify if the program will repeat or no
                    break
                else:
                    continue


            # check if quantity is enough
            if stock_item.quantity < quantity:
                print(f'{Back.RED}ERROR: You tried to sell {quantity}, but you have {stock_item.quantity} in stock.{Style.RESET_ALL}')

                if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                yes = 'yes',
                                no = 'no',
                                error_msg = 'Invalid option.',
                                use_color = True):    # verify if the program will repeat or no
                    break
                else:
                    continue


            sale_profit = sale_total_price - stock_item.purchase_price * quantity   # create sale_profit
            
            
            if sale_unit_price > stock_item.purchase_price:
                print(f'{Back.GREEN}Profit per item: {sale_profit / quantity} reais {Style.RESET_ALL}')
                print(f'{Back.GREEN}Total profit: {sale_profit} reais {Style.RESET_ALL}')
            else:
                print(f'{Back.RED}Loss per item: {sale_profit / quantity} reais {Style.RESET_ALL}')
                print(f'{Back.RED}Total loss: {sale_profit} reais {Style.RESET_ALL}')  
    

            profit_sale_percent = (sale_unit_price - stock_item.purchase_price) / sale_unit_price * 100    # profit per product with percent 


            stock_item.quantity = stock_item.quantity - quantity    # update quantity


            if stock_item.quantity == 0:    # Remove if 0
                session.delete(stock_item)


            try:
                new_record = SalesTable(product=product, product_type=product_type, size=size, quantity=quantity, sale_unit_price=sale_unit_price,
                                        sale_total_price=sale_total_price,sale_profit=sale_profit, 
                                        profitsale_percent=profit_sale_percent, date=date)
                
                session.add(new_record)
                session.commit()    # enter in PostgreSQL
                print(f'{Back.GREEN}Sale registered with success in sales table!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Back.RED}ERROR: {error}{Style.RESET_ALL}')


        if not fm.get_confirm(msg = 'Do you want to insert other sale? (yes/no): ',
                                yes = 'yes',
                                no = 'no',
                                error_msg = 'Invalid option.',
                                use_color = True):   # verify if the program will repeat or no
            break



def option_3():  # delete product
    while True:
        
        
        product = fm.input_alpha(msg = 'enter the product that you want to remove: ',
                                 error_msg = 'Invalid name.',
                                 case = 'title',
                                 use_color = True)


        product_type = fm.input_alpha(msg = 'enter the product type: ',
                                     error_msg = 'Invalid type.',
                                     case = 'title',
                                     use_color = True)


        size = fm.input_non_empty(msg = 'enter the product size here: ',
                                        error_msg = 'Invalid size.',
                                        case = 'title',
                                        use_color = True)


        quantity = fm.input_int(msg = 'enter the quantity that you want to remove: ',
                                min_value = 1,
                                max_value = 100,
                                error_msg = 'Invalid quantity.',
                                use_color = True)


        reason = fm.input_non_empty(msg = 'enter the remove reason here: ',
                                        error_msg = 'Invalid reason.',
                                        case = 'title',
                                        use_color = True) 
        
        
        date = datetime.now()    # date
        
        
        with Session() as session:  #create session


            # search item in stock
            stock_item = session.query(StockTable).filter_by(
                product=product,
                product_type=product_type,
                size=size
                ).first()
            
            
            # check if exist
            if not stock_item:
                print(f'{Back.RED}ERROR: {product} {product_type} {size} Does not exist in stock.{Style.RESET_ALL}')
                
                if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no
                    break
                else:
                    continue


            # check if quantity is enough
            if stock_item.quantity < quantity:
                print(f'{Back.RED}ERROR: You tried to remove {quantity}, but you have {stock_item.quantity} in stock.{Style.RESET_ALL}')
                
                if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no 
                    break
                else:
                    continue


            stock_item.quantity = stock_item.quantity - quantity    # update quantity
            
            
            total_prejudice = stock_item.purchase_price * quantity 
            unit_prejudice = total_prejudice / quantity     
            
            print(f'{Back.RED}Loss per item: {unit_prejudice} reais {Style.RESET_ALL}')
            print(f'{Back.RED}Total loss: {total_prejudice} reais {Style.RESET_ALL}') 
            
            
            if stock_item.quantity == 0:    # Remove if 0
                session.delete(stock_item)


            try:
                new_record = ExcludeTable(product=product, product_type=product_type, size=size, unit_prejudice=unit_prejudice,
                                        total_prejudice=total_prejudice, quantity=quantity,
                                        reason=reason, date=date)
                
                session.add(new_record)
                session.commit()    # enter in PostgreSQL
                print(f'{Back.GREEN}Product registered with success in exclude table!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Back.RED}ERROR: {error}{Style.RESET_ALL}')


        if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no:
                break
        else:
            continue



def option_4():  # check item
    while True:

        
        product = fm.input_alpha(msg = 'enter the product name that you want to check: ',
                                     error_msg = 'Invalid name.',
                                     case = 'title',
                                     use_color = True)


        
        product_type = fm.input_alpha(msg = 'enter the product type here: ',
                                     error_msg = 'Invalid type.',
                                     case = 'title',
                                     use_color = True)


        size= fm.input_non_empty(msg = 'enter the product size: ',
                                        error_msg = 'Invalid size.',
                                        case = 'title',
                                        use_color = True)


        with Session() as session:  #create session


            # search item in stock
            stock_item = session.query(StockTable).filter_by(
                product=product,
                product_type=product_type,
                size=size
                ).first()


            # if exist
            if stock_item:
                print(f'{Back.GREEN}{product} {product_type} {size} Exists in stock with {stock_item.quantity} items.{Style.RESET_ALL}')

            # if not exist
            else:
                print(f'{Back.RED}{product} {product_type} {size} Does not exist in stock.{Style.RESET_ALL}')


        if not fm.get_confirm(msg = 'Do you want to insert other item? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no
            break   



def option_5():  # alerts 
    
    with Session() as session:  #create session
        
        stock_item = session.query(StockTable).all()  #stock_item = all in StockTable
            
        if stock_item:
            print(f'{Back.YELLOW}============= ALERTS ============={Style.RESET_ALL}')
                
            for i in stock_item:
                if i.quantity < 5:
                    print(f'\n{Back.RED}The product {i.product} {i.product_type} size {i.size} only has in stock {i.quantity} units{Style.RESET_ALL}')
            
        else:
            print(f'\n{Back.GREEN}there are no alerts at the moment{Style.RESET_ALL}')
    
    
    
def option_6():  # results
    while True:
        
        start_date, end_date = fm.input_date_range(start_msg = 'Start date (DD/MM/YYYY): ',
                                                   end_msg = 'End date (DD/MM/YYYY): ',
                                                   format_error_msg = 'Invalid date. Use DD/MM/YYYY.',
                                                   range_error_msg = 'End date must be after start date.',
                                                   use_color = True)

        with Session() as session:  # create session
        
        
            # taking sales in the period
            sales = session.query(SalesTable).filter(
                SalesTable.date >= start_date,
                SalesTable.date <= end_date
            ).all()
            
            
            # taking exclude in the period
            prejudice = session.query(ExcludeTable).filter(
                ExcludeTable.date >= start_date,
                ExcludeTable.date <= end_date
            ).all()

            
            if not sales:
                print(f'{Back.RED}There are no sales in this period.{Style.RESET_ALL}')
            else:
                # calculate profit
                total_profit = 0
                for s in sales:
                    total_profit = total_profit + s.sale_profit      # sum of all sale_profit in SalesTable


                total_prejudice_value = 0
                for p in prejudice:
                    total_prejudice_value = total_prejudice_value + p.total_prejudice    # sum of all total_prejudice in ExcludeTable


                total_real_profit = total_profit - total_prejudice_value


                total_sale = 0
                for s in sales:
                    total_sale = total_sale + s.sale_total_price
                
                
                print(f'{Back.GREEN}Total sold in this period: R${total_sale:.2f}{Style.RESET_ALL}')
                print(f'{Back.GREEN}Total profit in this period: R${total_profit:.2f}{Style.RESET_ALL}')
                print(f'{Back.RED}Total loss with removed items in this period: R${total_prejudice_value:.2f}{Style.RESET_ALL}')
                print(f'{Back.GREEN}Total final profit in this period: R${total_real_profit:.2f}{Style.RESET_ALL}')
        break   



def option_7():  # tables
    while True:
        
        table_choice = fm.input_choice(msg = 'which table do you want to view? | 1 - stock | 2 - sales | 3 - exclude |: ',
                                       valid_options = (1, 2, 3),
                                       error_msg = 'Invalid option.',
                                       use_color = True)
            
            
        with Session() as session:  # create session
            
            
            # table choice
            if table_choice == 1:
                table_class = StockTable
                
            elif table_choice == 2:
                table_class = SalesTable
                
            else:
                table_class = ExcludeTable
                
            
            start_date , end_date = fm.input_date_range(start_msg = 'Start date (DD/MM/YYYY): ',
                                                        end_msg = 'End date (DD/MM/YYYY): ',
                                                        format_error_msg = 'Invalid date. Use DD/MM/YYYY.',
                                                        range_error_msg = 'End date must be after start date.',
                                                        use_color = True)
                
                
            records_period = session.query(table_class).filter(
                table_class.date >= start_date,
                table_class.date <= end_date
                ).order_by(table_class.date).all()
            
            
            if not records_period:
                print(f'\n{Back.YELLOW}No records found {table_class.__tablename__} in this period!{Style.RESET_ALL}')
                
                if not fm.get_confirm(msg = 'Do you want to view other table? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no  
                    return
                else:
                    continue


            print(f'\n{Back.CYAN}================== TABLE {table_class.__tablename__.upper()} =================={Style.RESET_ALL}')
            print(f'{start_date} <-----> {end_date}')
            
            
            # take Columns name
            columns = table_class.__table__.columns.keys()  # __table__ is a entire table in SQLAlchemy and columns.keys() return a list with columns name
            
            
            # create data list
            table_data = []


            for r in records_period:
                row = []  # create empty list

                for col in columns:  # go through each column name
                    value = getattr(r, col)  # get the value of that column
                    row.append(value)  # add the value to the row
                    
                table_data.append(row)  # add the row to the table data

            # showing the table
            print(tabulate(table_data, headers=columns, tablefmt="fancy_grid"))
            
            
        if not fm.get_confirm(msg = 'Do you want to view other table? (yes/no): ',
                                    yes = 'yes',
                                    no = 'no',
                                    error_msg = 'Invalid option.',
                                    use_color = True):   # verify if the program will repeat or no
            break   

        
        

#------------------- MAIN LOOP -------------------

while True:
    
    choice = menu()

    if choice == 1:   # register product 
        option_1()

    elif choice == 2:   # register sale  
        option_2()

    elif choice == 3:   # register exclusion
        option_3()

    elif choice == 4:   # check if product in StockTable
        option_4()
        
    elif choice == 5:   # check alerts
        option_5()
        
    elif choice == 6:   # check results
        option_6()
        
    elif choice == 7:   # check tables
        option_7()


    else:
        print(f'\n{Back.WHITE}========== FINISHED PROGRAM =========={Style.RESET_ALL}')
        break


    if not fm.get_confirm(msg = 'Do you want to return to menu? (yes/no): ',
                         yes = 'yes',
                         no = 'no',
                         error_msg = 'Invalid option.',
                         use_color = True):
        print(f'\n{Back.WHITE}========== FINISHED PROGRAM =========={Style.RESET_ALL}')
        break
