from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Double, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Korenev:12345@77.91.86.135/isp_p_Korenev"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
"""
# Определение модели SQLAlchemy для пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(50), index=True)  # Указываем длину для VARCHAR
    email = Column(String(100), unique=True, index=True)  # Указываем длину для VARCHAR
"""
class Tenat(Base):
    __tablename__ = "tenat"
    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(30), index=True)
    middlename = Column(String(30), index=True)
    surname = Column(String(30), index=True)
    phone = Column(String(15), unique=True, index=True)

class Services(Base):
    __tablename__ = "services"
    id = Column(Integer(), primary_key=True, index=True)
    tariff = Column(Float(), index=True)
    type = Column(String(30), index=True)
    unit = Column(String(30), index=True)

class Apartments(Base):
    __tablename__ = "apartments"
    id = Column(Integer(), primary_key=True, index=True)
    address = Column(String(60), index=True)
    residents = Column(Integer(), index=True)
    square = Column(Float(), index=True)

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer(), primary_key=True, index=True)
    pay = Column(Boolean(), index=True) #уплачено да\нет
    id_services = Column(Integer(), index=True)
    id_tenet = Column(Integer(), index=True)
    paydate = Column(DateTime(), index=True) #когда платить
    datepay = Column(DateTime(), index=True) #когда уплачено
    consumption = Column(Double(), index=True)


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
"""
# Определение Pydantic модели для пользователя
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
"""
class TenatCreate(BaseModel):
    name: str
    middlename: str
    surname: str
    phone: str

class TenatResponse(BaseModel):
    id: int
    name: str
    middlename: str
    surname: str
    phone: str

    class Config:
        orm_mode = True

class ServicesCreate(BaseModel):
    tariff: float
    type: str
    unit: str

class ServicesResponse(BaseModel):
    id: int
    tariff: float
    type: str
    unit: str

    class Config:
        orm_mode = True

class ApartmentsCreate(BaseModel):
    address: str
    residents: str
    square: str

class ApartmentsResponse(BaseModel):
    id: int
    address: str
    residents: str
    square: str

    class Config:
        orm_mode = True

class PaymentCreate(BaseModel):
    pay: bool
    id_services: int
    id_tenet: int
    paydate: str
    datepay: str
    consumption: str

class PaymentResponse(BaseModel):
    id: int
    pay: bool
    id_services: int
    id_tenet: int
    paydate: datetime
    datepay: datetime
    consumption: float

    class Config:
        orm_mode = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
# Маршрут для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""
@app.get("/tenats/{tenat_id}", response_model=TenatResponse)
def read_tenat(tenat_id: int, db: Session = Depends(get_db)):
    tenat = db.query(Tenat).filter(Tenat.id == tenat_id).first()
    if tenat is None:
        raise HTTPException(status_code=404, detail="Tenat not found")
    return tenat

@app.get("/services/{service_id}", response_model=ServicesResponse)
def read_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Services).filter(Services.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/apartments/{apartment_id}", response_model=ApartmentsResponse)
def read_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartments).filter(Apartments.id == apartment_id).first()
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
"""
# Маршрут для создания нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
"""
@app.post("/tenats/", response_model=TenatResponse)
def create_tenat(tenat: TenatCreate, db: Session = Depends(get_db)):
    db_tenat = Tenat(name=tenat.name, middlename=tenat.middlename, surname=tenat.surname, phone=tenat.phone)
    try:
        db.add(db_tenat)
        db.commit()
        db.refresh(db_tenat)
        return db_tenat
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Phone number already registered")

@app.post("/services/", response_model=ServicesResponse)
def create_service(service: ServicesCreate, db: Session = Depends(get_db)):
    db_service = Services(tariff=service.tariff, type=service.type, unit=service.unit)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@app.post("/apartments/", response_model=ApartmentsResponse)
def create_apartment(apartment: ApartmentsCreate, db: Session = Depends(get_db)):
    db_apartment = Apartments(address=apartment.address, residents=apartment.residents, square=apartment.square)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment

@app.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(pay=payment.pay, id_services=payment.id_services, id_tenet=payment.id_tenet, paydate=payment.paydate, datepay=payment.datepay, consumption=payment.consumption)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment