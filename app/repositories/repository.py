from sqlalchemy import select
from sqlalchemy.orm import Session


class Repository:
    
    def __init__(self, db : Session):
        self.db = db
    
    # CREATE METHOD
    def create(self, model_obj):
        try:
            self.db.add(model_obj)
            self.db.commit()
            self.db.refresh(model_obj)
        except Exception:
            self.db.rollback()
            raise 
        
        return model_obj
    
    
    # READ METHOD
    def read(self, model_obj, **feilds):
        try:
            statement = select(model_obj)
            
            for feild, value in feilds.items():
                if value is not None:
                    statement = statement.where(
                        getattr(model_obj, feild) == value
                    )
                    
            result = self.db.execute(statement)
            
            return result.scalars().all()
        except Exception:
            self.db.rollback()
            raise 
    
            
    # UPDATE METHOD
    def update(self, model_obj):
        try:
            self.db.commit()
            self.db.refresh(model_obj)
        except Exception:
            self.db.rollback()
            raise
        
        return model_obj
    
    
    # DELETE METHOD
    def delete(self, model_obj):
        try:
            self.db.delete(model_obj)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
    
    

    


