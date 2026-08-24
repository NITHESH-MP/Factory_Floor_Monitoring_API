from sqlalchemy import select
from sqlalchemy.orm import Session


class Repository:
    
    def __init__(self, db : Session):
        self.db = db
    
    # CREATE METHOD
    def create(self, model):
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        except Exception:
            self.db.rollback()
            raise 
        
        return model
    
    
    # READ METHOD
    def read(self, model, **feilds):
        try:
            statement = select(model)
            
            for feild, value in feilds.items():
                if value is not None:
                    statement = statement.where(
                        getattr(model, feild) == value
                    )
                    
            result = self.db.execute(statement)
            
            return result.scalars().all()
        except Exception:
            self.db.rollback()
            raise 
    
            
    # UPDATE METHOD
    def update(self, model):
        try:
            self.db.commit()
            self.db.refresh(model)
        except Exception:
            self.db.rollback()
            raise
        
        return model
    
    
    # DELETE METHOD
    def delete(self, model):
        try:
            self.db.delete(model)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
    
    

    


